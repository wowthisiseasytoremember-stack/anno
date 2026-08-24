import ARKit
import OSLog
import PilgrimCore
import QuartzCore
import RealityKit
import simd

/// visionOS implementation of the platform AR seam.
///
/// Uses the visionOS ARKit surface (`ARKitSession` + data providers) with
/// `RealityView` instead of `ARView`:
///
/// - `WorldTrackingProvider` — head pose (gaze ray) + `WorldAnchor`s that
///   pin reliquaries to the room across the immersive session.
/// - `PlaneDetectionProvider(.horizontal)` — readiness signal for "a
///   surface exists under the reticle".
/// - `SceneReconstructionProvider` — invisible collision meshes of the
///   room; hit-testing of the gaze ray runs against them via
///   `Scene.raycast(from:to:)`.
///
/// Divergences from the iOS implementation (by design, behind the seam):
/// no screen-space raycast (there is no 2-D touch surface — aim is the
/// head-pose reticle); world sensing requires explicit authorization
/// (`NSWorldSensingUsageDescription`); providers only deliver while the
/// app occupies a Full Space (the immersive scene).
@MainActor
public final class ImmersiveReliquarySessionService: NSObject, ReliquarySessionServicing {
    public let supportsScreenSpacePlacement = false
    public let events: AsyncStream<ReliquarySessionEvent>

    /// Invisible scene-reconstruction collision (added to the RealityView).
    public let reconstructionRoot = Entity()
    /// World-anchored reliquaries + the gaze reticle.
    public let worldRoot = Entity()

    /// Set by `ReliquaryImmersiveView` — required for raycasting.
    var realityScene: Scene?

    private let arSession = ARKitSession()
    private let worldTracking = WorldTrackingProvider()
    private let planeDetection = PlaneDetectionProvider(alignments: [.horizontal])
    private let sceneReconstruction = SceneReconstructionProvider()

    private let continuation: AsyncStream<ReliquarySessionEvent>.Continuation
    private var providerTasks: [Task<Void, Never>] = []
    private var isActive = false

    private var reconstructionMeshes: [UUID: ModelEntity] = [:]
    private var horizontalPlaneIDs: Set<UUID> = []
    private var lastSurfaceReady = false

    private struct Placement {
        let anchor: WorldAnchor
        let entity: Entity
    }

    private var placementsByHandle: [ReliquaryPlacementHandle: Placement] = [:]
    private var placementsByAnchorID: [UUID: ReliquaryPlacementHandle] = [:]

    public override init() {
        var localContinuation: AsyncStream<ReliquarySessionEvent>.Continuation!
        events = AsyncStream { localContinuation = $0 }
        continuation = localContinuation
        super.init()
    }

    // MARK: - ReliquarySessionServicing

    public func activate() async throws {
        guard !isActive else { return }

        // World-sensing permission (planes + reconstruction). Requesting
        // explicitly surfaces a denial as an event instead of a crash on
        // `run(_:)`.
        let statuses = await arSession.requestAuthorization(for: [.worldSensing])
        if let status = statuses[.worldSensing], status == .denied {
            emit(.authorizationDenied(
                "World sensing was denied. Enable it in Settings → Privacy & Security to place reliquaries."
            ))
            return
        }

        try await arSession.run([worldTracking, planeDetection, sceneReconstruction])
        isActive = true
        emit(.trackingStateChanged(.initializing))
        startProviderLoops()
        PilgrimCoreLog.ar.info("visionOS ARKit session running (world tracking + planes + reconstruction)")
    }

    public func deactivate() {
        providerTasks.forEach { $0.cancel() }
        providerTasks.removeAll()
        arSession.stop()
        isActive = false
    }

    public var currentViewRay: WorldRay? {
        // Head pose as the "view" — the reticle aims where the wearer looks.
        guard let device = worldTracking.queryDeviceAnchor(atTimestamp: CACurrentMediaTime()) else {
            return nil
        }
        let transform = device.originFromAnchorTransform
        return WorldRay(
            origin: transform.columns.3.xyz,
            direction: -simd_normalize(transform.columns.2.xyz)
        )
    }

    public func surfaceHit(atScreenPoint point: CGPoint) -> SurfaceHit? {
        nil // no 2-D touch surface in a head-mounted display
    }

    public func surfaceHit(along ray: WorldRay, maxLength: Float) -> SurfaceHit? {
        guard let scene = realityScene else { return nil }
        let destination = PlacementMath.destination(of: ray, maxLength: maxLength)
        let hits = scene.raycast(from: ray.origin, to: destination, query: .closest, mask: .all)

        for hit in hits {
            // Only real-world geometry (reconstruction meshes) counts —
            // don't place reliquaries on other reliquaries.
            guard isDescendant(of: reconstructionRoot, entity: hit.entity) else { continue }

            var normal = hit.normal
            if normal.y < 0 { normal = -normal } // mesh winding may flip
            guard abs(normal.y) > 0.4 else { continue } // horizontal-ish surfaces only

            var transform = matrix_identity_float4x4
            transform.columns.3 = SIMD4(hit.position, 1)
            return SurfaceHit(worldTransform: transform, surfaceNormal: simd_normalize(normal))
        }
        return nil
    }

    public func place(
        _ entity: Entity,
        at worldTransform: simd_float4x4
    ) async throws -> ReliquaryPlacementHandle {
        let anchor = WorldAnchor(originFromAnchorTransform: worldTransform)
        try await worldTracking.addAnchor(anchor)

        let handle = ReliquaryPlacementHandle()
        placementsByHandle[handle] = Placement(anchor: anchor, entity: entity)
        placementsByAnchorID[anchor.id] = handle

        // Apply immediately for responsiveness; the anchorUpdates loop
        // keeps the transform pinned as tracking refines.
        worldRoot.addChild(entity)
        entity.transform = Transform(matrix: worldTransform)
        return handle
    }

    public func removePlacement(_ handle: ReliquaryPlacementHandle) {
        guard let placement = placementsByHandle.removeValue(forKey: handle) else { return }
        placementsByAnchorID[placement.anchor.id] = nil
        worldTracking.removeAnchor(placement.anchor)
        placement.entity.removeFromParent()
    }

    public func addTransientEntity(_ entity: Entity) {
        worldRoot.addChild(entity)
    }

    public func removeTransientEntity(_ entity: Entity) {
        entity.removeFromParent()
    }

    // MARK: - Provider loops

    private func startProviderLoops() {
        providerTasks.forEach { $0.cancel() }
        providerTasks = []

        // Session-level events: authorization changes, provider issues.
        let sessionEvents = arSession.events
        providerTasks.append(Task { [weak self] in
            for await event in sessionEvents {
                guard let self else { return }
                switch event {
                case let .authorizationChanged(type, status)
                where type == .worldSensing && status == .denied:
                    self.emit(.authorizationDenied(
                        "World sensing was denied. Enable it in Settings → Privacy & Security."
                    ))
                case .dataProviderChanged:
                    PilgrimCoreLog.ar.info("Data providers changed: \(event)")
                default:
                    break
                }
            }
        })

        // Scene reconstruction → invisible collision meshes for raycasting.
        let reconstructionUpdates = sceneReconstruction.anchorUpdates
        providerTasks.append(Task { [weak self] in
            for await update in reconstructionUpdates {
                guard let self else { return }
                switch update.event {
                case .added, .updated:
                    if let mesh = self.meshEntity(for: update.anchor) {
                        if let existing = self.reconstructionMeshes[update.anchor.id] {
                            existing.removeFromParent()
                        }
                        self.reconstructionRoot.addChild(mesh)
                        self.reconstructionMeshes[update.anchor.id] = mesh
                        self.emitSurfaceReadinessIfNeeded()
                    }
                case .removed:
                    if let existing = self.reconstructionMeshes.removeValue(forKey: update.anchor.id) {
                        existing.removeFromParent()
                        self.emitSurfaceReadinessIfNeeded()
                    }
                }
            }
        })

        // Plane detection → surface readiness signal.
        let planeUpdates = planeDetection.anchorUpdates
        providerTasks.append(Task { [weak self] in
            for await update in planeUpdates {
                guard let self else { return }
                switch update.event {
                case .added:
                    self.horizontalPlaneIDs.insert(update.anchor.id)
                    self.emitSurfaceReadinessIfNeeded()
                case .removed:
                    self.horizontalPlaneIDs.remove(update.anchor.id)
                    self.emitSurfaceReadinessIfNeeded()
                case .updated:
                    break
                }
            }
        })

        // World anchors → keep placed reliquaries pinned to the room.
        let worldAnchorUpdates = worldTracking.anchorUpdates
        providerTasks.append(Task { [weak self] in
            for await update in worldAnchorUpdates {
                guard let self else { return }
                guard let handle = self.placementsByAnchorID[update.anchor.id],
                      let placement = self.placementsByHandle[handle]
                else { continue }
                switch update.event {
                case .added, .updated:
                    placement.entity.transform = Transform(matrix: update.anchor.originFromAnchorTransform)
                case .removed:
                    self.placementsByHandle[handle] = nil
                    self.placementsByAnchorID[update.anchor.id] = nil
                    placement.entity.removeFromParent()
                }
            }
        })
    }

    // MARK: - Reconstruction meshes

    /// Mesh → collision-only entity (occlusion material: invisible but
    /// occludes placed content correctly, and raycastable).
    private func meshEntity(for anchor: MeshAnchor) -> ModelEntity? {
        do {
            let descriptor = MeshDescriptor(name: anchor.id.description)
            descriptor.positions = MeshBuffer(anchor.geometry.vertices)
            descriptor.primitives = .triangles(anchor.geometry.faces.indices.map { UInt32($0) })
            let resource = try MeshResource.generate(from: [descriptor])
            let entity = ModelEntity(mesh: resource, materials: [OcclusionMaterial()])
            entity.generateCollisionShapes(recursive: true)
            entity.transform = Transform(matrix: anchor.originFromAnchorTransform)
            return entity
        } catch {
            PilgrimCoreLog.ar.warning("Reconstruction mesh build failed: \(error.localizedDescription)")
            return nil
        }
    }

    private func emitSurfaceReadinessIfNeeded() {
        let ready = !reconstructionMeshes.isEmpty || !horizontalPlaneIDs.isEmpty
        guard ready != lastSurfaceReady else { return }
        lastSurfaceReady = ready
        emit(.surfaceAvailabilityChanged(isReady: ready))
    }

    private func isDescendant(of root: Entity, entity: Entity) -> Bool {
        var current: Entity? = entity
        while let node = current {
            if node === root { return true }
            current = node.parent
        }
        return false
    }

    private func emit(_ event: ReliquarySessionEvent) {
        continuation.yield(event)
    }
}

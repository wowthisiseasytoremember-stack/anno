import ARKit
import Foundation
import OSLog
import PilgrimCore
import RealityKit
import simd

/// iOS/iPadOS implementation of the platform AR seam.
///
/// Owns an `ARView` (created once, vended to the SwiftUI representable),
/// runs an `ARWorldTrackingConfiguration` with horizontal plane detection,
/// and bridges `ARSessionDelegate` callbacks into
/// `ReliquarySessionEvent`s. Placement uses real `ARAnchor`s so placed
/// reliquaries survive tracking interruptions and relocalization.
///
/// UIKit surface area is confined to this file and the AR screen:
/// `ARView` is not available in the same form on visionOS, which is
/// exactly why it lives below the `ReliquarySessionServicing` seam and
/// cannot leak into shared code.
@MainActor
public final class ARKitReliquarySessionService: NSObject, ReliquarySessionServicing {
    public let supportsScreenSpacePlacement = true

    public private(set) var arView: ARView?
    public let events: AsyncStream<ReliquarySessionEvent>

    private let continuation: AsyncStream<ReliquarySessionEvent>.Continuation
    private var lastSurfaceReadyEmitted: Bool?

    private enum PlacementError: LocalizedError {
        case sessionUnavailable
        case anchorNotAccepted

        var errorDescription: String? {
            switch self {
            case .sessionUnavailable: return "AR session is not running."
            case .anchorNotAccepted: return "ARKit did not accept the placement anchor in time."
            }
        }
    }

    /// One in-flight placement: echoes through `session(_:didAdd:)`.
    private final class PendingPlacement {
        let entity: Entity
        var resumed = false
        var continuation: CheckedContinuation<ReliquaryPlacementHandle, Error>?
        init(entity: Entity) { self.entity = entity }
    }

    private var pending: [UUID: PendingPlacement] = [:]
    private var handles: [ReliquaryPlacementHandle: (arAnchor: ARAnchor, anchorEntity: AnchorEntity)] = [:]
    private var anchorIDToHandle: [UUID: ReliquaryPlacementHandle] = [:]
    private var transientAnchors: [ObjectIdentifier: AnchorEntity] = [:]
    private var horizontalPlaneIDs: Set<UUID> = []

    public override init() {
        var localContinuation: AsyncStream<ReliquarySessionEvent>.Continuation!
        events = AsyncStream { localContinuation = $0 }
        continuation = localContinuation
        super.init()
    }

    // MARK: - ARView lifecycle

    /// Called by `ReliquaryARViewContainer.makeUIView`.
    public func makeARView() -> ARView {
        if let arView { return arView }
        let view = ARView(frame: .zero)
        view.automaticallyConfigureSession = false
        view.environment.sceneUnderstanding.options.insert(.occlusion)
        view.session.delegate = self
        arView = view
        return view
    }

    // MARK: - ReliquarySessionServicing

    public func activate() async throws {
        guard ARWorldTrackingConfiguration.isSupported else {
            emit(.sessionFailed("World tracking is not supported on this device."))
            return
        }
        guard let arView else {
            emit(.sessionFailed("ARView not attached before activation."))
            return
        }

        let configuration = ARWorldTrackingConfiguration()
        configuration.planeDetection = [.horizontal]
        configuration.environmentTexturing = .automatic
        configuration.isLightEstimationEnabled = true

        // NOTE: no [.resetTracking] on re-activate so anchors survive.
        arView.session.run(configuration)
        PilgrimCoreLog.ar.info("ARKit world tracking session running (horizontal planes)")
    }

    public func deactivate() {
        arView?.session.pause()
    }

    public var currentViewRay: WorldRay? {
        guard let camera = arView?.camera else { return nil }
        let transform = camera.transform
        let origin = transform.columns.3.xyz
        let direction = -simd_normalize(transform.columns.2.xyz)
        return WorldRay(origin: origin, direction: direction)
    }

    public func surfaceHit(atScreenPoint point: CGPoint) -> SurfaceHit? {
        guard let arView else { return nil }
        // Prefer tracked plane geometry; fall back to ARKit's estimated
        // horizontal plane so placement still works mid-discovery.
        let result =
            arView.raycast(from: point, allowing: .existingPlaneGeometry, alignment: .horizontal).first
            ?? arView.raycast(from: point, allowing: .estimatedPlane, alignment: .horizontal).first
        guard let result else { return nil }
        return SurfaceHit(worldTransform: result.worldTransform, surfaceNormal: normal(for: result))
    }

    public func surfaceHit(along ray: WorldRay, maxLength: Float) -> SurfaceHit? {
        guard let session = arView?.session else { return nil }
        let length = simd_length(ray.direction)
        guard length > 1e-6 else { return nil }
        let direction = ray.direction / length

        func query(_ target: ARRaycastQuery.Target) -> ARRaycastQuery {
            ARRaycastQuery(origin: ray.origin, direction: direction, allowing: target, alignment: .horizontal)
        }
        let result =
            session.raycast(query(.existingPlaneGeometry)).first
            ?? session.raycast(query(.estimatedPlane)).first
        guard let result else { return nil }
        return SurfaceHit(worldTransform: result.worldTransform, surfaceNormal: normal(for: result))
    }

    public func place(
        _ entity: Entity,
        at worldTransform: simd_float4x4
    ) async throws -> ReliquaryPlacementHandle {
        guard let session = arView?.session, arView?.scene != nil else {
            throw PlacementError.sessionUnavailable
        }

        let arAnchor = ARAnchor(transform: worldTransform)
        let pendingPlacement = PendingPlacement(entity: entity)
        pending[arAnchor.identifier] = pendingPlacement
        session.add(anchor: arAnchor)

        // ARKit echoes the anchor back via session(_:didAdd:) within a few
        // frames; guard with a deadline so a paused session can't hang the
        // caller forever.
        return try await withCheckedThrowingContinuation { cont in
            pendingPlacement.continuation = cont
            let anchorID = arAnchor.identifier
            Deadline.schedule(after: 2.0) { [weak self, weak pendingPlacement] in
                guard let self, let placement = pendingPlacement, !placement.resumed else { return }
                placement.resumed = true
                self.pending[anchorID] = nil
                cont.resume(throwing: PlacementError.anchorNotAccepted)
            }
        }
    }

    public func removePlacement(_ handle: ReliquaryPlacementHandle) {
        guard let entry = handles[handle] else { return }
        arView?.session.remove(anchor: entry.arAnchor)
        entry.anchorEntity.removeFromParent()
        handles[handle] = nil
        anchorIDToHandle[entry.arAnchor.identifier] = nil
    }

    public func addTransientEntity(_ entity: Entity) {
        guard arView != nil else { return }
        let anchor = AnchorEntity()
        anchor.addChild(entity)
        arView?.scene.addAnchor(anchor)
        transientAnchors[ObjectIdentifier(entity)] = anchor
    }

    public func removeTransientEntity(_ entity: Entity) {
        if let anchor = transientAnchors.removeValue(forKey: ObjectIdentifier(entity)) {
            anchor.removeFromParent()
        }
    }

    // MARK: - ARSessionDelegate (callbacks arrive on the main thread)

    public nonisolated func session(
        _ session: ARSession,
        cameraDidChangeTrackingState camera: ARCamera
    ) {
        Task { @MainActor in self.handleTrackingState(camera.trackingState) }
    }

    public nonisolated func sessionWasInterrupted(_ session: ARSession) {
        Task { @MainActor in
            self.emit(.interruptionBegan("Session interrupted (multitasking, phone call, control center)."))
        }
    }

    public nonisolated func sessionInterruptionEnded(_ session: ARSession) {
        Task { @MainActor in self.emit(.interruptionEnded) }
    }

    /// Attempt relocalization after interruptions so anchors — and thus
    /// placed reliquaries — snap back to their real-world positions.
    public nonisolated func sessionShouldAttemptRelocalization(_ session: ARSession) -> Bool {
        true
    }

    public nonisolated func session(_ session: ARSession, didFailWithError error: Error) {
        Task { @MainActor in self.emit(.sessionFailed(error.localizedDescription)) }
    }

    public nonisolated func session(_ session: ARSession, didAdd anchors: [ARAnchor]) {
        Task { @MainActor in self.handleAdded(anchors) }
    }

    public nonisolated func session(_ session: ARSession, didRemove anchors: [ARAnchor]) {
        Task { @MainActor in self.handleRemoved(anchors) }
    }

    // MARK: - Internals

    @MainActor
    private func handleTrackingState(_ state: ARCamera.TrackingState) {
        let mapped: ReliquaryTrackingState
        switch state {
        case .normal:
            mapped = .normal
        case .notAvailable:
            mapped = .unavailable(reason: "Tracking unavailable.")
        case .limited(let reason):
            switch reason {
            case .excessiveMotion: mapped = .limited(reason: .excessiveMotion)
            case .insufficientFeatures: mapped = .limited(reason: .insufficientFeatures)
            case .initializing: mapped = .limited(reason: .initializing)
            case .relocalizing: mapped = .limited(reason: .relocalizing)
            @unknown default: mapped = .limited(reason: .initializing)
            }
        }
        emit(.trackingStateChanged(mapped))
    }

    @MainActor
    private func handleAdded(_ anchors: [ARAnchor]) {
        for anchor in anchors {
            if let placement = pending[anchor.identifier] {
                let anchorEntity = AnchorEntity(anchor: anchor)
                anchorEntity.addChild(placement.entity)
                arView?.scene.addAnchor(anchorEntity)

                let handle = ReliquaryPlacementHandle()
                handles[handle] = (anchor, anchorEntity)
                anchorIDToHandle[anchor.identifier] = handle
                pending[anchor.identifier] = nil

                if !placement.resumed {
                    placement.resumed = true
                    placement.continuation?.resume(returning: handle)
                }
            }
            if let plane = anchor as? ARPlaneAnchor, plane.alignment == .horizontal {
                horizontalPlaneIDs.insert(plane.identifier)
                emitSurfaceReadinessIfNeeded()
            }
        }
    }

    @MainActor
    private func handleRemoved(_ anchors: [ARAnchor]) {
        for anchor in anchors {
            if let handle = anchorIDToHandle[anchor.identifier] {
                handles[handle]?.anchorEntity.removeFromParent()
                handles[handle] = nil
                anchorIDToHandle[anchor.identifier] = nil
            }
            if let plane = anchor as? ARPlaneAnchor, plane.alignment == .horizontal {
                horizontalPlaneIDs.remove(plane.identifier)
                emitSurfaceReadinessIfNeeded()
            }
        }
    }

    @MainActor
    private func emitSurfaceReadinessIfNeeded() {
        let ready = !horizontalPlaneIDs.isEmpty
        guard lastSurfaceReadyEmitted != ready else { return }
        lastSurfaceReadyEmitted = ready
        emit(.surfaceAvailabilityChanged(isReady: ready))
    }

    private func normal(for result: ARRaycastResult) -> SIMD3<Float> {
        switch result.targetAlignment {
        case .horizontal:
            return SIMD3<Float>(0, 1, 0)
        default:
            // Vertical/none: approximate the surface normal with the hit
            // transform's Y axis.
            let y = result.worldTransform.columns.1.xyz
            return simd_length(y) > 1e-6 ? simd_normalize(y) : SIMD3<Float>(0, 1, 0)
        }
    }

    private func emit(_ event: ReliquarySessionEvent) {
        continuation.yield(event)
    }
}

/// Main-thread deadline helper.
@MainActor
private enum Deadline {
    static func schedule(after seconds: TimeInterval, action: @escaping @MainActor () -> Void) {
        Task { @MainActor in
            try? await Task.sleep(nanoseconds: UInt64(seconds * 1_000_000_000))
            action()
        }
    }
}

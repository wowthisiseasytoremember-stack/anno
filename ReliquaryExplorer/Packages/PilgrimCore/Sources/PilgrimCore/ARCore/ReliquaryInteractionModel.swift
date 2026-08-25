import Foundation
import Observation
import RealityKit
import simd

/// User-visible state machine for the AR viewer, shared verbatim by
/// iOS/iPadOS and visionOS.
public enum ReliquaryPhase: Equatable, Sendable {
    case idle
    case loadingAsset
    /// Session running; surfaces not yet understood well enough.
    case searchingSurface
    /// Surfaces ready — awaiting the placement gesture.
    case readyToPlace
    case placed(itemID: String)
    case failed(String)

    public var allowsPlacement: Bool {
        switch self {
        case .readyToPlace, .placed: true
        default: false
        }
    }
}

/// The shared brain of the AR Reliquary Viewer.
///
/// Platform views translate their native gestures into this model's
/// intent APIs and nothing more:
///
/// - iOS (`ReliquaryARScreen`): `UITapGestureRecognizer` →
///   `confirmPlacement(atScreenPoint:)`; `UIPinchGestureRecognizer` →
///   `handleScaleDelta`; `UIRotationGestureRecognizer` → `handleYawDelta`.
/// - visionOS (`ReliquaryImmersiveView`): `SpatialTapGesture` →
///   `confirmPlacement(atScreenPoint: nil)` (reticle-aimed);
///   `MagnifyGesture`/`RotateGesture3D` targeted at an entity →
///   `handleScaleDelta`/`handleYawDelta(on:)`.
///
/// All placement math funnels through `PlacementMath`, all world
/// interaction through `ReliquarySessionServicing` — which is what keeps
/// the two implementations duplication-free.
@MainActor
@Observable
public final class ReliquaryInteractionModel {
    public let session: any ReliquarySessionServicing
    private let assetLoader: @MainActor (ReliquaryItem) async -> Entity

    // MARK: - Published state (drives HUD on both platforms)

    public private(set) var phase: ReliquaryPhase = .idle
    public private(set) var trackingState: ReliquaryTrackingState = .initializing
    public private(set) var isInterrupted = false
    public private(set) var placements: [PlacedReliquary] = []
    public private(set) var latestReticleHit: SurfaceHit?
    public internal(set) var selectedReliquary: ReliquaryItem

    /// Flips briefly when a placement gesture finds no surface — used to
    /// shake/pulse the "no surface here" hint.
    public private(set) var surfaceMissPulse = false

    public private(set) var isSessionActive = false

    // MARK: - Private

    private var eventsTask: Task<Void, Never>?
    private var gazeTask: Task<Void, Never>?
    private var preloadedEntity: Entity?
    private var missResetTask: Task<Void, Never>?
    private var reticleEntity: Entity?

    public init(
        session: any ReliquarySessionServicing,
        initialSelection: ReliquaryItem = ReliquaryItem.catalog[0],
        assetLoader: (@MainActor (ReliquaryItem) async -> Entity)? = nil
    ) {
        self.session = session
        self.selectedReliquary = initialSelection
        self.assetLoader = assetLoader ?? { item in
            await ReliquaryAssetLoader.loadRootEntity(for: item)
        }
    }

    deinit {
        eventsTask?.cancel()
        gazeTask?.cancel()
        missResetTask?.cancel()
    }

    // MARK: - Session lifecycle

    public func beginSession() async {
        guard !isSessionActive else { return }
        phase = .loadingAsset
        do {
            try await session.activate()
        } catch {
            PilgrimCoreLog.ar.error("Session activation failed: \(error.localizedDescription)")
            phase = .failed(error.localizedDescription)
            return
        }
        isSessionActive = true
        trackingState = .initializing
        phase = .searchingSurface
        startEventLoop()
        startGazeLoopIfNeeded()
        installReticleIfNeeded()
        await preloadSelected()
    }

    public func endSession() {
        eventsTask?.cancel(); eventsTask = nil
        gazeTask?.cancel(); gazeTask = nil
        missResetTask?.cancel(); missResetTask = nil
        isSessionActive = false
        removeAllPlacements()
        if let reticleEntity {
            session.removeTransientEntity(reticleEntity)
        }
        reticleEntity = nil
        latestReticleHit = nil
        preloadedEntity = nil
        session.deactivate()
        phase = .idle
    }

    // MARK: - Selection & preloading

    public func selectReliquary(_ item: ReliquaryItem) {
        guard item.id != selectedReliquary.id else { return }
        selectedReliquary = item
        preloadedEntity = nil
        Task { await preloadSelected() }
        if isSessionActive, isSurfaceReadyForPlacement {
            phase = .readyToPlace
        }
    }

    private func preloadSelected() async {
        guard preloadedEntity == nil else { return }
        preloadedEntity = await assetLoader(selectedReliquary)
        if phase == .loadingAsset || phase == .searchingSurface, isSurfaceReadyForPlacement {
            phase = .readyToPlace
        }
    }

    private var isSurfaceReadyForPlacement: Bool {
        switch trackingState {
        case .normal: return true
        case .limited: return true // planes may already be good enough
        default: return false
        }
    }

    // MARK: - Placement

    /// iOS passes the touch point (screen-space raycast); visionOS passes
    /// `nil` to place at the gaze reticle.
    public func confirmPlacement(atScreenPoint point: CGPoint?) async {
        guard phase.allowsPlacement else { return }

        let hit: SurfaceHit?
        if let point, session.supportsScreenSpacePlacement {
            hit = session.surfaceHit(atScreenPoint: point)
        } else {
            updateGazeReticle()
            hit = latestReticleHit
        }

        guard let hit else {
            pulseSurfaceMiss()
            return
        }

        let entity = preloadedEntity ?? await assetLoader(selectedReliquary)
        preloadedEntity = nil

        let worldTransform = PlacementMath.uprightTransform(
            position: hit.position,
            surfaceNormal: hit.surfaceNormal,
            facing: session.currentViewRay?.origin
        )

        do {
            let handle = try await session.place(entity, at: worldTransform)
            placements.append(
                PlacedReliquary(id: handle, item: selectedReliquary, root: entity)
            )
            phase = .placed(itemID: selectedReliquary.id)
            Task { await preloadSelected() } // ready the next placement
            PilgrimCoreLog.ar.info("Placed \(self.selectedReliquary.title)")
        } catch {
            PilgrimCoreLog.ar.error("Placement failed: \(error.localizedDescription)")
            pulseSurfaceMiss()
        }
    }

    public func removePlacements(containing entity: Entity) {
        let targets = placements.filter { $0.contains(entity) }
        targets.forEach { session.removePlacement($0.id) }
        placements.removeAll { placed in targets.contains(where: { $0.id == placed.id }) }
    }

    public func removeAllPlacements() {
        placements.forEach { session.removePlacement($0.id) }
        placements.removeAll()
    }

    /// Resolves a gesture's hit entity back to the reliquary it belongs to
    /// (visionOS targeted gestures; iOS hit-testing if needed later).
    public func reliquary(containing entity: Entity) -> PlacedReliquary? {
        placements.first { $0.contains(entity) }
    }

    // MARK: - Manipulation

    /// Pinch/magnify delta. `on` nil → most recent placement (iOS two-
    /// finger pinch has no entity target).
    public func handleScaleDelta(_ delta: Float, on entity: Entity? = nil) {
        guard let index = indexOfTarget(entity) else { return }
        placements[index].applyScaleDelta(delta)
    }

    /// Rotation delta (radians). Sign is normalized by the caller so both
    /// platforms feel natural.
    public func handleYawDelta(_ radians: Float, on entity: Entity? = nil) {
        guard let index = indexOfTarget(entity) else { return }
        placements[index].applyYawDelta(radians)
    }

    /// Called by views when a scale gesture ends, so collision shapes
    /// track the final rendered size (gesture targeting stays accurate).
    public func settleScale(on entity: Entity? = nil) {
        guard let index = indexOfTarget(entity) else { return }
        placements[index].regenerateCollision()
    }

    // MARK: - Start-anchored gestures (visionOS)

    /// visionOS `MagnifyGesture`/`RotateGesture3D` deliver **absolute**
    /// magnification/rotation since gesture start (UIKit recognizers, by
    /// contrast, can be zeroed each callback). This API applies those
    /// absolute values against a snapshot taken at gesture start. The
    /// math is still shared `PlacementMath` — only the gesture value
    /// semantics differ per platform, and that difference is isolated
    /// here.
    private var gestureAnchor: (index: Int, startScaleMultiplier: Float, startOrientation: simd_quatf)?

    public func updateGesture(
        magnification: Float,
        yawFromGestureStart radians: Float,
        on entity: Entity?
    ) {
        let index: Int
        if let entity, let resolved = placements.firstIndex(where: { $0.contains(entity) }) {
            index = resolved
        } else if let anchor = gestureAnchor {
            index = anchor.index // keep gesture sticky to its start target
        } else if let last = placements.indices.last {
            index = last
        } else {
            return
        }

        if gestureAnchor == nil {
            gestureAnchor = (
                index,
                placements[index].scaleMultiplier,
                placements[index].root.orientation
            )
        }
        guard let anchor = gestureAnchor, anchor.index == index else { return }

        let item = placements[index].item
        let multiplier = PlacementMath.clampedUniformScale(
            current: anchor.startScaleMultiplier,
            delta: max(magnification, 0.01),
            bounds: PlacedReliquary.multiplierBounds(for: item)
        )
        placements[index].scaleMultiplier = multiplier
        placements[index].root.scale = SIMD3<Float>(repeating: item.defaultScale * multiplier)
        placements[index].root.orientation = PlacementMath.yawDelta(radians) * anchor.startOrientation
    }

    public func endGesture() {
        if let anchor = gestureAnchor, placements.indices.contains(anchor.index) {
            placements[anchor.index].regenerateCollision()
        }
        gestureAnchor = nil
    }

    private func indexOfTarget(_ entity: Entity?) -> Int? {
        if let entity, let index = placements.firstIndex(where: { $0.contains(entity) }) {
            return index
        }
        return placements.indices.last
    }

    // MARK: - Gaze reticle (visionOS aim)

    @discardableResult
    public func updateGazeReticle() -> SurfaceHit? {
        guard let ray = session.currentViewRay else {
            latestReticleHit = nil
            return nil
        }
        let hit = session.surfaceHit(along: ray, maxLength: 5.0)
        latestReticleHit = hit

        if let reticleEntity {
            if let hit {
                reticleEntity.position = hit.position
                reticleEntity.components.set(OpacityComponent(level: 1))
            } else {
                reticleEntity.components.set(OpacityComponent(level: 0))
            }
        }
        return hit
    }

    // MARK: - Event loops

    private func startEventLoop() {
        eventsTask?.cancel()
        let stream = session.events
        eventsTask = Task { [weak self] in
            for await event in stream {
                await self?.handle(event)
            }
        }
    }

    private func handle(_ event: ReliquarySessionEvent) {
        switch event {
        case let .trackingStateChanged(state):
            trackingState = state
            if isSurfaceReadyForPlacement, phase == .searchingSurface {
                phase = .readyToPlace
            }

        case let .surfaceAvailabilityChanged(ready):
            if ready, phase == .searchingSurface {
                phase = .readyToPlace
            } else if !ready, phase == .readyToPlace {
                phase = .searchingSurface
            }

        case let .interruptionBegan(reason):
            isInterrupted = true
            trackingState = .limited(reason: .interrupted)
            PilgrimCoreLog.ar.warning("Session interrupted: \(reason)")

        case .interruptionEnded:
            isInterrupted = false
            trackingState = .initializing // relocalizing

        case let .sessionFailed(message):
            isSessionActive = false
            phase = .failed(message)
            PilgrimCoreLog.ar.error("Session failed: \(message)")

        case let .authorizationDenied(message):
            isSessionActive = false
            phase = .failed(message)
        }
    }

    private func startGazeLoopIfNeeded() {
        guard !session.supportsScreenSpacePlacement else { return }
        gazeTask?.cancel()
        gazeTask = Task { [weak self] in
            // ~15 Hz: ARKit's guidance is to avoid querying head pose at
            // frame rate for non-rendering logic.
            while !Task.isCancelled {
                self?.updateGazeReticle()
                try? await Task.sleep(nanoseconds: 66_000_000)
            }
        }
    }

    private func installReticleIfNeeded() {
        guard !session.supportsScreenSpacePlacement, reticleEntity == nil else { return }
        let sphere = ModelEntity(
            mesh: .generateSphere(radius: 0.008),
            materials: [UnlitMaterial(color: .init(red: 1.0, green: 0.85, blue: 0.4, alpha: 0.9))]
        )
        sphere.name = "gaze_reticle"
        sphere.components.set(OpacityComponent(level: 0))
        reticleEntity = sphere
        session.addTransientEntity(sphere)
    }

    private func pulseSurfaceMiss() {
        surfaceMissPulse = true
        missResetTask?.cancel()
        missResetTask = Task { [weak self] in
            try? await Task.sleep(nanoseconds: 1_200_000_000)
            self?.surfaceMissPulse = false
        }
    }
}

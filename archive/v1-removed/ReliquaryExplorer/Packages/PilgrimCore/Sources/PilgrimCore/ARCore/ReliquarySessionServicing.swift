import CoreGraphics
import Foundation
import RealityKit
import simd

/// A ray in world/session space.
public struct WorldRay: Sendable, Equatable {
    public var origin: SIMD3<Float>
    public var direction: SIMD3<Float>

    public init(origin: SIMD3<Float>, direction: SIMD3<Float>) {
        self.origin = origin
        self.direction = direction
    }
}

/// A resolved real-world surface point to place onto.
public struct SurfaceHit: Sendable, Equatable {
    /// World-space transform at the hit (position on the surface).
    public var worldTransform: simd_float4x4
    /// World-space surface normal (≈ +Y for a horizontal plane).
    public var surfaceNormal: SIMD3<Float>

    public var position: SIMD3<Float> {
        worldTransform.columns.3.xyz
    }

    public init(worldTransform: simd_float4x4, surfaceNormal: SIMD3<Float>) {
        self.worldTransform = worldTransform
        self.surfaceNormal = surfaceNormal
    }
}

/// How healthy world tracking currently is. Platform implementations map
/// their native states into this shared vocabulary.
public enum ReliquaryTrackingState: Equatable, Sendable {
    case initializing
    case normal
    case limited(reason: LimitedReason)
    case unavailable(reason: String)

    public enum LimitedReason: String, Sendable {
        case excessiveMotion
        case insufficientFeatures
        case relocalizing
        case interrupted
        case initializing
    }
}

/// Lifecycle/health events surfaced by a `ReliquarySessionServicing`.
public enum ReliquarySessionEvent: Sendable {
    case trackingStateChanged(ReliquaryTrackingState)
    /// Whether enough surface understanding exists to attempt placement
    /// (iOS: ≥1 tracked horizontal plane; visionOS: ≥1 detected plane or
    /// reconstruction collision available).
    case surfaceAvailabilityChanged(isReady: Bool)
    case interruptionBegan(String)
    case interruptionEnded
    case sessionFailed(String)
    case authorizationDenied(String)
}

/// Opaque handle to a persistent, world-anchored placement.
public struct ReliquaryPlacementHandle: Sendable, Equatable {
    public let id: UUID
    public init(id: UUID = UUID()) { self.id = id }
}

/// THE platform seam of the AR subsystem.
///
/// Everything above this protocol — gesture interpretation, placement
/// policy, scale/rotation math, UI state — is written once in
/// `ReliquaryInteractionModel` and shared verbatim across iOS/iPadOS and
/// visionOS. The two implementations diverge *only* below this line:
///
/// | Aspect | iOS / iPadOS (`ARKitReliquarySessionService`) | visionOS (`ImmersiveReliquarySessionService`) |
/// |---|---|---|
/// | Session | `ARView.session.run(ARWorldTrackingConfiguration)` | `ARKitSession.run([WorldTrackingProvider, PlaneDetectionProvider, SceneReconstructionProvider])` |
/// | Surfaces | ARKit plane detection + `ARView.raycast(from:allowing:alignment:)` from the 2-D touch point | plane-detection provider for readiness; RealityKit `scene.raycast(from:to:)` against scene-reconstruction collision for gaze-ray hit testing |
/// | Placement anchor | `ARAnchor` added to the session, wrapped by `AnchorEntity(anchor:)` | `WorldAnchor` via `WorldTrackingProvider.addAnchor`, transform applied on `anchorUpdates` |
/// | "Aim" | the touch ray itself (screen-space raycast) | head-pose ray (`queryDeviceAnchor(atTimestamp:)`) + reticle |
/// | Permission | camera (ARKit on iOS) | world sensing (`NSWorldSensingUsageDescription`) |
/// | Interruption/relocalization | explicit `ARSessionDelegate` callbacks | provider state via `ARKitSession.events`; OS handles recovery |
@MainActor
public protocol ReliquarySessionServicing: AnyObject {
    var events: AsyncStream<ReliquarySessionEvent> { get }

    /// True when placement is aimed via 2-D screen points (iOS/iPadOS).
    /// False when aimed by head gaze + reticle (visionOS).
    var supportsScreenSpacePlacement: Bool { get }

    /// Current viewing ray (iOS: through screen center; visionOS: head
    /// pose). Used to orient placed objects toward the viewer and to
    /// drive the visionOS reticle.
    var currentViewRay: WorldRay? { get }

    /// Runs the session/providers, surfacing authorization needs via
    /// events. Idempotent.
    func activate() async throws

    func deactivate()

    // MARK: Hit testing

    /// Screen-space raycast (iOS/iPadOS touch). Returns nil when this
    /// platform aims by gaze instead.
    func surfaceHit(atScreenPoint point: CGPoint) -> SurfaceHit?

    /// World-space raycast (visionOS head gaze; also usable on iOS).
    func surfaceHit(along ray: WorldRay, maxLength: Float) -> SurfaceHit?

    // MARK: Placement

    /// Anchors `entity` at a world transform and returns a handle.
    /// iOS: adds an `ARAnchor` (survives tracking hiccups/relocalization).
    /// visionOS: adds a `WorldAnchor` (OS-managed persistence within the
    /// immersive session).
    func place(_ entity: Entity, at worldTransform: simd_float4x4) async throws -> ReliquaryPlacementHandle

    func removePlacement(_ handle: ReliquaryPlacementHandle)

    // MARK: Unanchored scene content (reticles, guides)

    func addTransientEntity(_ entity: Entity)
    func removeTransientEntity(_ entity: Entity)
}

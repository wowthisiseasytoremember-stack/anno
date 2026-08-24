import PilgrimCore
import RealityKit
import SwiftUI
import simd

/// Mixed-immersion scene for reliquary placement on visionOS.
///
/// Gesture mapping (all interpretation delegates to the shared model):
/// - `SpatialTapGesture` → confirm placement at the gaze reticle.
/// - `RotateGesture3D(.y)` + `MagnifyGesture` (simultaneous, targeted at
///   the reliquary) → scale + yaw via the shared start-anchored gesture
///   API on `ReliquaryInteractionModel`.
struct ReliquaryImmersiveView: View {
    let service: ImmersiveReliquarySessionService
    @Bindable var model: ReliquaryInteractionModel
    let coordinator: PilgrimGuideCoordinator

    @Environment(\.realityKitScene) private var realityScene

    var body: some View {
        RealityView { content in
            content.add(service.reconstructionRoot)
            content.add(service.worldRoot)
        }
        .onAppear {
            service.realityScene = realityScene
            coordinator.arViewerActive = true
            Task { await model.beginSession() }
        }
        .onDisappear {
            model.endSession()
            coordinator.arViewerActive = false
        }
        .gesture(
            SpatialTapGesture()
                .onEnded { _ in
                    Task { @MainActor in
                        await model.confirmPlacement(atScreenPoint: nil)
                    }
                }
        )
        .gesture(manipulationGesture)
    }

    /// Two-hand "pinch + twist + spread" on a placed reliquary.
    ///
    /// visionOS gestures deliver *absolute* values since gesture start
    /// (unlike UIKit's incremental recognizers), so the flow is
    /// begin/update/end against a snapshot — the shared model owns the
    /// snapshot and the math (`PlacementMath`), keeping this struct thin.
    private var manipulationGesture: some Gesture {
        RotateGesture3D(constrainedToAxis: .y)
            .simultaneously(with: MagnifyGesture())
            .targetedToAnyEntity()
            .onChanged { value in
                let yaw = Self.yawRadians(from: value.first?.rotation)
                let magnification = value.second?.magnification ?? 1
                model.updateGesture(
                    magnification: Float(magnification),
                    yawFromGestureStart: yaw,
                    on: value.entity
                )
            }
            .onEnded { _ in
                model.endGesture()
            }
    }

    private static func yawRadians(from rotation: Rotation3D?) -> Float {
        guard let rotation else { return 0 }
        let sign: Float = rotation.axis.y >= 0 ? 1 : -1
        return sign * Float(rotation.angle.radians)
    }
}

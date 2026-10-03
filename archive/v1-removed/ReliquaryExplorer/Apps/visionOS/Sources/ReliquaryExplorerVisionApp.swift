import PilgrimCore
import SwiftUI

@main
struct ReliquaryExplorerVisionApp: App {
    @State private var coordinator: PilgrimGuideCoordinator
    @State private var arService: ImmersiveReliquarySessionService
    @State private var arModel: ReliquaryInteractionModel

    @Environment(\.openImmersiveSpace) private var openImmersiveSpace
    @Environment(\.dismissImmersiveSpace) private var dismissImmersiveSpace

    init() {
        let monitor = MuseumModeSanctuaryMonitor()
        let player = AudioHagiographyPlayer(
            narrationResolver: { PilgrimSettings.narrationResolver() }
        )
        let catalog = (try? SanctuaryCatalog.load()) ?? SanctuaryCatalog(sites: [])
        _coordinator = State(
            initialValue: PilgrimGuideCoordinator(
                catalog: catalog,
                monitor: monitor,
                player: player,
                // No local-notification provider on visionOS: the app is
                // always visible when frontmost; backgrounded apps can't
                // play audio here by design.
                notifier: nil,
                appPhase: nil
            )
        )

        let service = ImmersiveReliquarySessionService()
        _arService = State(initialValue: service)
        _arModel = State(
            initialValue: ReliquaryInteractionModel(session: service)
        )
    }

    var body: some Scene {
        WindowGroup {
            PilgrimRootView { [arModel] item in
                arModel.selectReliquary(item)
                Task {
                    // ARKit data providers only deliver in a Full Space.
                    _ = await openImmersiveSpace(id: Self.immersiveSpaceID)
                }
            }
            .environment(coordinator)
            .task { coordinator.startGuidance() } // arms museum mode (no-op geofencing)
            .overlay(alignment: .bottom) {
                // In-window control strip while the immersive viewer runs.
                if arModel.phase != .idle {
                    VisionARControlPanel(
                        model: arModel,
                        close: { Task { await dismissImmersiveSpace() } }
                    )
                    .padding(.bottom, 12)
                }
            }
        }
        .defaultSize(width: 900, height: 640)

        ImmersiveSpace(id: Self.immersiveSpaceID) {
            ReliquaryImmersiveView(
                service: arService,
                model: arModel,
                coordinator: coordinator
            )
        }
        .immersionStyle(selection: .constant(.mixed), in: .mixed)
    }

    private static let immersiveSpaceID = "reliquary-viewer"
}

/// Compact window controls mirroring the iOS AR HUD: status, catalog
/// switcher, clear, and close. (Gestures themselves live in the
/// immersive view; scale/rotate are indirect-pinch driven there.)
struct VisionARControlPanel: View {
    @Bindable var model: ReliquaryInteractionModel
    let close: () -> Void

    var body: some View {
        HStack(spacing: 16) {
            VStack(alignment: .leading, spacing: 2) {
                Text(model.phase == .placed(model.selectedReliquary.id) ? "Placed — look + tap to add more" : "Look at a surface, then tap to place")
                    .font(.caption.weight(.bold))
                Text("Pinch the reliquary: spread to scale, twist to rotate")
                    .font(.caption2)
                    .foregroundStyle(.secondary)
            }

            Divider()
                .frame(height: 34)

            Menu {
                ForEach(ReliquaryItem.catalog) { candidate in
                    Button(candidate.title) {
                        model.selectReliquary(candidate)
                    }
                }
            } label: {
                Label("Switch reliquary", systemImage: "cross.vial.fill")
            }

            Button(role: .destructive) {
                model.removeAllPlacements()
            } label: {
                Label("Clear", systemImage: "trash")
            }
            .disabled(model.placements.isEmpty)

            Button(action: close) {
                Label("Done", systemImage: "xmark.circle.fill")
            }
        }
        .padding(.horizontal, 18)
        .padding(.vertical, 12)
        .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 18))
    }
}

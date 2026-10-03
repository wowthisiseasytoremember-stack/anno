import PilgrimCore
import SwiftUI
import UIKit

@main
struct ReliquaryExplorerApp: App {
    /// App-phase bridge so the coordinator knows when arrivals should be
    /// surfaced as local notifications (audio keeps playing regardless).
    @MainActor
    private final class ApplicationPhaseProvider: AppPhaseProviding {
        var isApplicationBackgrounded: Bool {
            UIApplication.shared.applicationState != .active
        }
    }

    @State private var coordinator: PilgrimGuideCoordinator
    @State private var arViewerItem: ReliquaryItem?
    @Environment(\.scenePhase) private var scenePhase

    init() {
        let monitor = CoreLocationSanctuaryMonitor()
        let player = AudioHagiographyPlayer(
            narrationResolver: { PilgrimSettings.narrationResolver() }
        )
        let catalog = (try? SanctuaryCatalog.load()) ?? SanctuaryCatalog(sites: [])
        let coordinator = PilgrimGuideCoordinator(
            catalog: catalog,
            monitor: monitor,
            player: player,
            notifier: LocalVisitNotifier(),
            appPhase: ApplicationPhaseProvider()
        )
        // Significant (cell/Wi-Fi-scale) location moves flow to the
        // coordinator so region sets are re-ranked and persisted.
        monitor.onSignificantLocationChange = { [weak coordinator] location in
            coordinator?.recordSignificantLocation(location)
        }
        _coordinator = State(initialValue: coordinator)
    }

    var body: some Scene {
        WindowGroup {
            PilgrimRootView { [coordinator] item in
                arViewerItem = item
            }
            .environment(coordinator)
            .preferredColorScheme(.dark)
            .task { coordinator.startGuidance() } // arms geofencing on launch
            .fullScreenCover(item: $arViewerItem) { item in
                ReliquaryARScreen(coordinator: coordinator, item: item)
            }
        }
        .onChange(of: scenePhase) { _, phase in
            // Re-arming is idempotent; this also recovers monitoring after
            // the system relaunches us for a region event.
            if phase == .active {
                coordinator.startGuidance()
            }
        }
    }
}

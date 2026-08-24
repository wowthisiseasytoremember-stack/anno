import SwiftUI

/// Shared root UI for iOS, iPadOS, and visionOS.
///
/// The only platform branch in the shared UI is *how the AR viewer is
/// presented*: the app targets inject a `launchARViewer` closure
/// (iOS: full-screen cover; visionOS: open the immersive space). The
/// package itself never links an AR session implementation.
public struct PilgrimRootView: View {
    @Bindable var coordinator: PilgrimGuideCoordinator
    let launchARViewer: @MainActor (ReliquaryItem) -> Void

    @State private var selectedTab: Tab = .sanctuaries

    public enum Tab: Hashable {
        case sanctuaries, reliquaries, guide
    }

    public init(
        coordinator: PilgrimGuideCoordinator,
        launchARViewer: @escaping (ReliquaryItem) -> Void
    ) {
        self.coordinator = coordinator
        self.launchARViewer = launchARViewer
    }

    public var body: some View {
        TabView(selection: $selectedTab) {
            SanctuaryMapView(coordinator: coordinator)
                .tabItem { Label("Sanctuaries", systemImage: "map.fill") }
                .tag(Tab.sanctuaries)

            ReliquaryCatalogView(coordinator: coordinator, launchARViewer: launchARViewer)
                .tabItem { Label("Reliquaries", systemImage: "cross.vial.fill") }
                .tag(Tab.reliquaries)

            GuideSettingsView(coordinator: coordinator)
                .tabItem { Label("Guide", systemImage: "person.walk.fill") }
                .tag(Tab.guide)
        }
        .overlay(alignment: .top) {
            // Proximity audio must stay visible in every context *except*
            // the immersive/full-screen AR viewer, which overlays its own
            // copy so the banner survives presentation covers.
            HagiographyBanner(coordinator: coordinator)
                .padding(.horizontal, 12)
        }
    }
}

/// Amber accent shared across the app.
extension Color {
    public static let pilgrimGold = Color(red: 0.88, green: 0.68, blue: 0.15)
}

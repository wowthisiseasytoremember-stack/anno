import CoreSpotlight
import Foundation
import SwiftUI

struct RootView: View {
    @Environment(AppSettings.self) private var settings
    @StateObject private var store: FixtureStore
    @State private var language: LanguageMode = .english
    @State private var selectedTab: AppTab = .launchDefault
    @State private var showingSources = false
    @State private var showingSettings = false
    @State private var showWelcome = false

    init(store: FixtureStore) {
        _store = StateObject(wrappedValue: store)

        let tabAppearance = UITabBarAppearance()
        tabAppearance.configureWithOpaqueBackground()
        tabAppearance.backgroundColor = UIColor(red: 0x13/255, green: 0x11/255, blue: 0x0E/255, alpha: 1)
        tabAppearance.shadowColor = UIColor(red: 0x2E/255, green: 0x2A/255, blue: 0x24/255, alpha: 1)
        UITabBar.appearance().standardAppearance = tabAppearance
        UITabBar.appearance().scrollEdgeAppearance = tabAppearance
    }

    var body: some View {
        TabView(selection: $selectedTab) {
            NavigationStack {
                TodayView(
                    entry: store.selectedEntry,
                    language: $language,
                    onShowSources: { showingSources = true }
                )
                .toolbar {
                    ToolbarItem(placement: .topBarLeading) {
                        Button {
                            Haptics.light()
                            showingSettings = true
                        } label: {
                            Image(systemName: AnnoSymbol.settings)
                                .foregroundStyle(AnnoTheme.incense)
                        }
                        .accessibilityLabel(language == .vietnamese ? "Cài đặt" : "Settings")
                    }
                }
            }
            .tabItem { Label(language == .vietnamese ? "Hôm nay" : "Today", systemImage: AnnoSymbol.today) }
            .tag(AppTab.today)

            NavigationStack {
                MonthCalendarView(
                    entries: store.allEntries,
                    language: language,
                    onSelectEntry: { entry in
                        store.select(entry)
                        selectedTab = .today
                    }
                )
            }
            .tabItem { Label(language == .vietnamese ? "Lịch" : "Calendar", systemImage: AnnoSymbol.calendar) }
            .tag(AppTab.calendar)

            NavigationStack {
                SacredSiteMapView(
                    entries: store.weekEntries,
                    currentEntry: store.selectedEntry,
                    language: language
                )
            }
            .tabItem { Label(language == .vietnamese ? "Bản đồ" : "Map", systemImage: AnnoSymbol.pilgrimage) }
            .tag(AppTab.map)
        }
        .tint(AnnoTheme.goldLeaf)
        .sensoryFeedback(.selection, trigger: selectedTab)
        .environment(settings)
        .sheet(isPresented: $showingSources) {
            SourceSheet(entry: store.selectedEntry, language: language)
        }
        .sheet(isPresented: $showingSettings) {
            SettingsView(language: $language)
        }
        .sheet(isPresented: $showWelcome) {
            WelcomeView {
                settings.hasSeenWelcome = true
                showWelcome = false
            }
            .interactiveDismissDisabled()
        }
        .onAppear {
            if !settings.hasSeenWelcome && !shouldSkipWelcomeForScreenshot {
                showWelcome = true
            }
        }
        .task {
            await SpotlightIndexer.indexContent(
                entries: store.allEntries,
                routes: SacredGeographyLoader.shared.routes
            )
        }
        .onContinueUserActivity(CSSearchableItemActionType) { activity in
            handleSpotlightActivity(activity)
        }
        .onOpenURL { url in
            handleDeepLink(url)
        }
    }

    private func handleDeepLink(_ url: URL) {
        guard let deepLink = AnnoDeepLink(url: url) else {
            return
        }

        switch deepLink {
        case .today(let entryId):
            if let entryId,
               let entry = store.allEntries.first(where: { $0.id == entryId }) {
                store.select(entry)
            }
            selectedTab = .today

        case .pilgrimage(let routeId, let stationId):
            let geography = SacredGeographyLoader.shared

            guard let route = geography.routes.first(where: {
                $0.routeId == routeId
            }) else {
                return
            }

            geography.selectedRoute = route

            if let stationId,
               let waypoint = route.waypoints.first(where: {
                   $0.waypointId == stationId
               }) {
                geography.selectedWaypoint = waypoint

                let moment = PilgrimageMomentRegistry.shared.moment(
                    routeId: route.routeId,
                    waypointId: waypoint.waypointId
                )

                Haptics.sacredArrival(
                    moment?.level.sacredIntensity ?? .feast
                )
            } else {
                geography.selectedWaypoint = route.waypoints.first
                Haptics.sacredArrival(.feast)
            }

            selectedTab = .map
        }
    }

    private func handleSpotlightActivity(_ activity: NSUserActivity) {
        guard let identifier = activity.userInfo?[CSSearchableItemActivityIdentifier] as? String else {
            return
        }

        if identifier.hasPrefix(SpotlightIndexer.entryPrefix) {
            let entryID = String(identifier.dropFirst(SpotlightIndexer.entryPrefix.count))
            guard let entry = store.allEntries.first(where: { $0.id == entryID }) else {
                return
            }
            store.select(entry)
            selectedTab = .today
            return
        }

        if identifier.hasPrefix(SpotlightIndexer.routePrefix) {
            let routeID = String(identifier.dropFirst(SpotlightIndexer.routePrefix.count))
            let geography = SacredGeographyLoader.shared
            if let route = geography.routes.first(where: { $0.routeId == routeID }) {
                geography.selectedRoute = route
                geography.selectedWaypoint = route.waypoints.first
            }
            selectedTab = .map
        }
    }

    private var shouldSkipWelcomeForScreenshot: Bool {
        #if DEBUG
        ProcessInfo.processInfo.environment["ANNO_SKIP_WELCOME"] == "1"
        #else
        false
        #endif
    }
}

private enum AppTab: String {
    case today
    case calendar
    case map

    static var launchDefault: AppTab {
        #if DEBUG
        if let rawValue = ProcessInfo.processInfo.environment["ANNO_SCREENSHOT_TAB"],
           let tab = AppTab(rawValue: rawValue) {
            return tab
        }
        #endif
        return .today
    }
}

#Preview {
    RootView(store: .preview)
        .preferredColorScheme(.dark)
        .environment(AppSettings())
}

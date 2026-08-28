import SwiftUI

struct RootView: View {
    @Environment(AppSettings.self) private var settings
    @StateObject private var store: FixtureStore
    @State private var language: LanguageMode = .english
    @State private var selectedTab: AppTab = .today
    @State private var showingSources = false
    @State private var showingSettings = false
    @State private var showWelcome = false

    init(store: FixtureStore) {
        _store = StateObject(wrappedValue: store)

        // Style the tab bar for the ecclesial dark theme
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
                            Image(systemName: "gearshape")
                                .foregroundStyle(AnnoTheme.incense)
                        }
                        .accessibilityLabel(language == .vietnamese ? "Cài đặt" : "Settings")
                    }
                }
            }
            .tabItem { Label(language == .vietnamese ? "Hôm nay" : "Today", systemImage: "sun.max") }
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
            .tabItem { Label(language == .vietnamese ? "Lịch" : "Calendar", systemImage: "calendar") }
            .tag(AppTab.calendar)

            NavigationStack {
                SacredSiteMapView(
                    entries: store.weekEntries,
                    currentEntry: store.selectedEntry,
                    language: language
                )
            }
            .tabItem { Label(language == .vietnamese ? "Bản đồ" : "Map", systemImage: "map") }
            .tag(AppTab.map)

            NavigationStack {
                SavedView(language: language)
            }
            .tabItem { Label(language == .vietnamese ? "Đã lưu" : "Saved", systemImage: "bookmark") }
            .tag(AppTab.saved)
        }
        .tint(AnnoTheme.goldLeaf)
        .environment(settings)
        .sheet(isPresented: $showingSources) {
            SourceSheet(entry: store.selectedEntry, language: language)
        }
        .sheet(isPresented: $showingSettings) {
            SettingsView(language: $language)
        }
        .sheet(isPresented: $showWelcome) {
            WelcomeView { showWelcome = false }
        }
        .onAppear {
            if !settings.hasSeenWelcome {
                showWelcome = true
                settings.hasSeenWelcome = true
            }
        }
    }
}

private enum AppTab {
    case today
    case calendar
    case map
    case saved
}

#Preview {
    RootView(store: .preview)
        .preferredColorScheme(.dark)
        .environment(AppSettings())
}

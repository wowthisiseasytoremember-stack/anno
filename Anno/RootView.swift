import SwiftUI

struct RootView: View {
    @StateObject private var store: FixtureStore
    @State private var language: LanguageMode = .english
    @State private var selectedTab: AppTab = .today
    @State private var showingSources = false

    init(store: FixtureStore) {
        _store = StateObject(wrappedValue: store)
    }

    var body: some View {
        TabView(selection: $selectedTab) {
            TodayView(
                entry: store.selectedEntry,
                language: $language,
                onShowSources: { showingSources = true }
            )
            .tabItem { Label("Today", systemImage: "sun.max") }
            .tag(AppTab.today)

            WeekCalendarView(store: store, language: language)
                .tabItem { Label("Calendar", systemImage: "calendar") }
                .tag(AppTab.calendar)

            SacredSiteMapView(entries: store.weekEntries, language: language)
                .tabItem { Label("Map", systemImage: "map") }
                .tag(AppTab.map)

            SavedView(language: language)
                .tabItem { Label("Saved", systemImage: "bookmark") }
                .tag(AppTab.saved)
        }
        .tint(AnnoTheme.goldLeaf)
        .background(AnnoTheme.narthex)
        .sheet(isPresented: $showingSources) {
            SourceSheet(entry: store.selectedEntry, language: language)
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
}

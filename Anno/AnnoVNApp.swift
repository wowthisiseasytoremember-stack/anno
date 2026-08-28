import SwiftUI
import SwiftData

/// Entry point for the free EN/VI Vietnamese devotional build
/// ("Lời Nguyện Hàng Ngày"). Shares all Anno sources except the
/// StoreKit/RevenueCat/paywall layer. Excluded from the premium `Anno`
/// target (which keeps AnnoApp.swift) to avoid a duplicate `@main`.
@main
struct AnnoVNApp: App {
    var body: some Scene {
        WindowGroup {
            RootView(store: FixtureStore.loadBundledOrPreview())
                .preferredColorScheme(.dark)
                .environment(AppSettings())
        }
        .modelContainer(for: [
            AnnoEntry.self,
            SacredPlace.self,
            Artwork.self,
            PilgrimageRoute.self,
            PilgrimageWaypoint.self,
            Journey.self,
            Visit.self,
            FieldNote.self
        ])
    }
}

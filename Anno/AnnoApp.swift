import SwiftUI
import SwiftData

@main
struct AnnoApp: App {
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

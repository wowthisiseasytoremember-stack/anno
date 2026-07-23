import SwiftUI

@main
struct AnnoApp: App {
    var body: some Scene {
        WindowGroup {
            RootView(store: FixtureStore.loadBundledOrPreview())
                .preferredColorScheme(.dark)
        }
    }
}

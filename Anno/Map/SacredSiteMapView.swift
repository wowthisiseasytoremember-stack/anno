import MapKit
import SwiftUI

struct SacredSiteMapView: View {
    let entries: [AnnoEntry]
    let language: LanguageMode

    private var siteEntries: [AnnoEntry] {
        entries.filter { $0.place != nil }
    }

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                Map {
                    ForEach(siteEntries) { entry in
                        if let place = entry.place {
                            Marker(
                                LocalizedEntryText(entry: entry, language: language).title,
                                coordinate: CLLocationCoordinate2D(latitude: place.latitude, longitude: place.longitude)
                            )
                            .tint(AnnoTheme.confidenceColor(place.confidence))
                        }
                    }
                }
                .frame(minHeight: 260)

                SacredSiteListView(entries: siteEntries, language: language)
            }
            .background(AnnoTheme.narthex)
            .navigationTitle(language == .vietnamese ? "Bản đồ" : "Map")
        }
    }
}

import SwiftUI

struct SacredSiteListView: View {
    let entries: [AnnoEntry]
    let language: LanguageMode

    var body: some View {
        List(entries) { entry in
            if let place = entry.place {
                VStack(alignment: .leading, spacing: 7) {
                    Text(LocalizedEntryText(entry: entry, language: language).title)
                        .font(.headline)
                        .foregroundStyle(AnnoTheme.vellum)
                        .fixedSize(horizontal: false, vertical: true)

                    Text(place.name)
                        .font(.subheadline)
                        .foregroundStyle(AnnoTheme.incense)
                        .fixedSize(horizontal: false, vertical: true)

                    Text("\(place.latitude.formatted(.number.precision(.fractionLength(4)))), \(place.longitude.formatted(.number.precision(.fractionLength(4))))")
                        .font(.caption.monospacedDigit())
                        .foregroundStyle(AnnoTheme.incense)

                    Link(destination: URL(string: "http://maps.apple.com/?ll=\(place.latitude),\(place.longitude)")!) {
                        Label(language == .vietnamese ? "Mở trong Bản đồ" : "Open in Maps", systemImage: "arrow.triangle.turn.up.right.diamond")
                    }
                    .font(.callout)
                    .foregroundStyle(AnnoTheme.goldLeaf)
                }
                .padding(.vertical, 8)
                .listRowBackground(AnnoTheme.narthex)
            }
        }
        .scrollContentBackground(.hidden)
    }
}

import SwiftUI

struct SacredSiteListView: View {
    let entries: [AnnoEntry]
    let language: LanguageMode
    
    @State private var appeared = false

    var body: some View {
        VStack(spacing: 16) {
            ForEach(Array(entries.enumerated()), id: \.element.id) { index, entry in
                if let place = entry.place {
                    siteRow(entry: entry, place: place)
                        .opacity(appeared ? 1 : 0)
                        .offset(y: appeared ? 0 : 16)
                        .animation(
                            .spring(response: 0.5, dampingFraction: 0.8)
                                .delay(0.1 * Double(index)),
                            value: appeared
                        )
                }
            }
        }
        .onAppear {
            appeared = true
        }
    }
    
    private func siteRow(entry: AnnoEntry, place: SacredPlace) -> some View {
        HStack(spacing: 12) {
            // Colored left accent bar
            RoundedRectangle(cornerRadius: 2)
                .fill(AnnoTheme.confidenceColor(place.confidence))
                .frame(width: 4)

            VStack(alignment: .leading, spacing: 8) {
                // Header: Place Name and Entry Title
                VStack(alignment: .leading, spacing: 2) {
                    Text(place.name)
                        .font(Typography.headlineSerif)
                        .foregroundStyle(AnnoTheme.vellum)
                        .fixedSize(horizontal: false, vertical: true)

                    Text(LocalizedEntryText(entry: entry, language: language).title)
                        .font(Typography.caption)
                        .foregroundStyle(AnnoTheme.incense)
                        .fixedSize(horizontal: false, vertical: true)
                }

                // Coordinates
                Text("\(place.latitude.formatted(.number.precision(.fractionLength(4)))), \(place.longitude.formatted(.number.precision(.fractionLength(4))))")
                    .font(.caption2.monospacedDigit())
                    .foregroundStyle(AnnoTheme.incense.opacity(0.8))

                // Footer: Confidence Badge & Map Link
                HStack(alignment: .bottom) {
                    ConfidenceBadge(
                        label: LocalizedEntryText(entry: entry, language: language).confidenceLabel,
                        confidence: place.confidence
                    )

                    Spacer()

                    if let mapsUrl = appleMapsUrl(latitude: place.latitude, longitude: place.longitude) {
                        Link(destination: mapsUrl) {
                            HStack(spacing: 4) {
                                Text(language == .vietnamese ? "Bản đồ" : "Maps")
                                    .font(Typography.captionMedium)
                                Image(systemName: "arrow.triangle.turn.up.right.diamond.fill")
                                    .font(Typography.caption)
                            }
                            .foregroundStyle(AnnoTheme.goldLeaf)
                            .padding(.horizontal, 10)
                            .padding(.vertical, 6)
                            .background(
                                Capsule()
                                    .strokeBorder(AnnoTheme.goldLeaf.opacity(0.3), lineWidth: 1)
                                    .background(Capsule().fill(AnnoTheme.goldLeaf.opacity(0.1)))
                            )
                        }
                    }
                }
            }
            .padding(.vertical, 4)
        }
        .annoCard()
        .accessibilityElement(children: .combine)
        .accessibilityLabel(
            language == .vietnamese
                ? "Địa điểm: \(place.name). \(LocalizedEntryText(entry: entry, language: language).title). Tọa độ: \(place.latitude), \(place.longitude)."
                : "Place: \(place.name). \(LocalizedEntryText(entry: entry, language: language).title). Coordinates: \(place.latitude), \(place.longitude)."
        )
    }
    
    private func appleMapsUrl(latitude: Double, longitude: Double) -> URL? {
        var components = URLComponents()
        components.scheme = "http"
        components.host = "maps.apple.com"
        components.queryItems = [
            URLQueryItem(name: "ll", value: "\(latitude),\(longitude)")
        ]
        return components.url
    }
}

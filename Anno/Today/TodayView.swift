import SwiftUI

struct TodayView: View {
    let entry: AnnoEntry
    @Binding var language: LanguageMode
    let onShowSources: () -> Void

    private var text: LocalizedEntryText {
        LocalizedEntryText(entry: entry, language: language)
    }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 18) {
                    Picker("Language", selection: $language) {
                        ForEach(LanguageMode.allCases) { mode in
                            Text(mode.rawValue).tag(mode)
                        }
                    }
                    .pickerStyle(.segmented)
                    .padding(.bottom, 4)

                    VStack(alignment: .leading, spacing: 10) {
                        Text(entry.dateDisplay(language: language))
                            .font(.subheadline.monospacedDigit())
                            .foregroundStyle(AnnoTheme.incense)

                        Text(text.title)
                            .font(.largeTitle.weight(.semibold))
                            .foregroundStyle(AnnoTheme.vellum)
                            .fixedSize(horizontal: false, vertical: true)

                        Text(text.heroLine)
                            .font(.title3)
                            .foregroundStyle(AnnoTheme.gilt)
                            .fixedSize(horizontal: false, vertical: true)
                    }

                    VStack(alignment: .leading, spacing: 10) {
                        HStack(alignment: .firstTextBaseline) {
                            Text(entry.liturgical.rank)
                                .font(.caption.weight(.semibold))
                                .foregroundStyle(AnnoTheme.goldLeaf)
                            Spacer()
                            Text(entry.liturgical.color.capitalized)
                                .font(.caption)
                                .foregroundStyle(AnnoTheme.incense)
                        }

                        Text(text.liturgicalTitle)
                            .font(.headline)
                            .foregroundStyle(AnnoTheme.vellum)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                    .annoCard()

                    ArtworkCandidateView(artwork: entry.artwork)

                    ConfidenceBadge(label: text.confidenceLabel, confidence: entry.primary.confidence)

                    Text(text.summary)
                        .font(.body)
                        .foregroundStyle(AnnoTheme.vellum)
                        .lineSpacing(4)
                        .fixedSize(horizontal: false, vertical: true)

                    placeSection

                    VStack(alignment: .leading, spacing: 8) {
                        Label(language == .vietnamese ? "Lời nguyện" : "Prayer prompt", systemImage: "hands.sparkles")
                            .font(.headline)
                            .foregroundStyle(AnnoTheme.goldLeaf)

                        Text(text.prayerPrompt)
                            .font(.body)
                            .foregroundStyle(AnnoTheme.vellum)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                    .annoCard()

                    VStack(alignment: .leading, spacing: 8) {
                        Label(language == .vietnamese ? "Độ tin cậy của nguồn" : "Source confidence", systemImage: "checkmark.seal")
                            .font(.headline)
                            .foregroundStyle(AnnoTheme.goldLeaf)
                        Text(text.confidenceNote)
                            .font(.callout)
                            .foregroundStyle(AnnoTheme.incense)
                            .fixedSize(horizontal: false, vertical: true)
                        Button(action: onShowSources) {
                            Label(language == .vietnamese ? "Xem nguồn" : "Read sources", systemImage: "link")
                        }
                        .buttonStyle(.bordered)
                        .tint(AnnoTheme.goldLeaf)
                    }
                    .annoCard()

                    CalendarConversionGrid(calendars: entry.calendars)
                }
                .padding(20)
            }
            .background(AnnoTheme.narthex.ignoresSafeArea())
            .navigationTitle("Anno")
            .navigationBarTitleDisplayMode(.inline)
        }
    }

    @ViewBuilder
    private var placeSection: some View {
        if let place = entry.place {
            VStack(alignment: .leading, spacing: 8) {
                Label(place.name, systemImage: "mappin.and.ellipse")
                    .font(.headline)
                    .foregroundStyle(AnnoTheme.vellum)
                    .fixedSize(horizontal: false, vertical: true)
                Text("\(place.latitude.formatted(.number.precision(.fractionLength(4)))), \(place.longitude.formatted(.number.precision(.fractionLength(4))))")
                    .font(.caption.monospacedDigit())
                    .foregroundStyle(AnnoTheme.incense)
                ConfidenceBadge(label: place.confidence.rawValue.capitalized, confidence: place.confidence)
            }
            .annoCard()
        } else {
            Text(language == .vietnamese ? "Không có địa điểm cố định đã xác minh" : "No fixed site verified")
                .font(.callout)
                .foregroundStyle(AnnoTheme.incense)
                .annoCard()
        }
    }
}

private extension AnnoEntry {
    func dateDisplay(language: LanguageMode) -> String {
        guard let parsedDate else {
            return "\(date) • \(weekday)"
        }

        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: language == .vietnamese ? "vi_VN" : "en_US")
        formatter.dateFormat = language == .vietnamese ? "d MMMM • EEEE" : "EEEE, MMMM d"
        return formatter.string(from: parsedDate)
    }
}

#Preview {
    TodayView(entry: FixtureStore.preview.selectedEntry, language: .constant(.english), onShowSources: {})
        .preferredColorScheme(.dark)
}

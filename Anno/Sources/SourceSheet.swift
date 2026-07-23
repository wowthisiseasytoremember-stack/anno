import SwiftUI

struct SourceSheet: View {
    let entry: AnnoEntry
    let language: LanguageMode
    @Environment(\.dismiss) private var dismiss

    // MARK: - Computed Properties

    private var localizedText: LocalizedEntryText {
        LocalizedEntryText(entry: entry, language: language)
    }

    private var groupedSources: [(String, [SourceRef])] {
        Dictionary(grouping: entry.sources, by: \.type)
            .map { ($0.key, $0.value) }
            .sorted { $0.0 < $1.0 }
    }

    private var totalSourceCount: Int {
        entry.sources.count
    }

    // MARK: - Bilingual Helpers

    private var sheetTitle: String {
        language == .vietnamese ? "Nguồn" : "Sources"
    }

    private var confidenceSectionTitle: String {
        language == .vietnamese ? "Độ Tin Cậy" : "Confidence"
    }

    private var closeLabel: String {
        language == .vietnamese ? "Đóng" : "Close"
    }

    /// Bilingual display name for a raw source type key.
    private func sectionTitle(for type: String) -> String {
        let key = type.lowercased()
        switch key {
        case "liturgical":
            return language == .vietnamese ? "Phụng Vụ" : "Liturgical"
        case "historical":
            return language == .vietnamese ? "Lịch Sử" : "Historical"
        case "church_biography":
            return language == .vietnamese ? "Tiểu Sử Giáo Hội" : "Church Biography"
        case "academic":
            return language == .vietnamese ? "Học Thuật" : "Academic"
        default:
            return type.replacingOccurrences(of: "_", with: " ").capitalized
        }
    }

    // MARK: - Body

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: AnnoTheme.lg) {
                    confidenceCard
                    sourcesList
                }
                .padding(.horizontal, AnnoTheme.md)
                .padding(.vertical, AnnoTheme.lg)
            }
            .background(AnnoTheme.narthex)
            .navigationTitle(sheetTitle)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    sourceCountBadge
                }
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        dismiss()
                    } label: {
                        Image(systemName: "xmark.circle.fill")
                            .font(.system(size: 18))
                            .symbolRenderingMode(.hierarchical)
                            .foregroundStyle(AnnoTheme.incense)
                    }
                    .accessibilityLabel(closeLabel)
                }
            }
            .toolbarBackground(AnnoTheme.choir, for: .navigationBar)
            .toolbarBackground(.visible, for: .navigationBar)
        }
    }

    // MARK: - Confidence Card

    private var confidenceCard: some View {
        VStack(alignment: .leading, spacing: AnnoTheme.sm) {
            // Section label
            Text(confidenceSectionTitle.uppercased())
                .font(AnnoTheme.caption(11, weight: .bold))
                .foregroundStyle(AnnoTheme.goldLeaf)
                .tracking(1.2)

            HStack(spacing: AnnoTheme.sm) {
                // Confidence badge
                Circle()
                    .fill(AnnoTheme.confidenceColor(entry.primary.confidence))
                    .frame(width: 10, height: 10)
                    .accessibilityHidden(true)

                Text(localizedText.confidenceLabel)
                    .font(AnnoTheme.body(15, weight: .semibold))
                    .foregroundStyle(AnnoTheme.confidenceColor(entry.primary.confidence))
            }

            // Confidence note
            Text(localizedText.confidenceNote)
                .font(AnnoTheme.body(14))
                .foregroundStyle(AnnoTheme.vellum.opacity(0.85))
                .fixedSize(horizontal: false, vertical: true)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .annoCard()
        .shadow(
            color: AnnoTheme.cardShadow.color,
            radius: AnnoTheme.cardShadow.radius,
            x: AnnoTheme.cardShadow.x,
            y: AnnoTheme.cardShadow.y
        )
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(confidenceSectionTitle): \(localizedText.confidenceLabel). \(localizedText.confidenceNote)")
    }

    // MARK: - Sources List

    private var sourcesList: some View {
        VStack(spacing: AnnoTheme.lg) {
            ForEach(groupedSources, id: \.0) { type, sources in
                VStack(alignment: .leading, spacing: AnnoTheme.sm) {
                    // Section header
                    Text(sectionTitle(for: type).uppercased())
                        .font(AnnoTheme.caption(11, weight: .bold))
                        .foregroundStyle(AnnoTheme.goldLeaf)
                        .tracking(1.2)
                        .padding(.leading, AnnoTheme.xs)
                        .accessibilityAddTraits(.isHeader)

                    VStack(spacing: 0) {
                        ForEach(Array(sources.enumerated()), id: \.element.id) { index, source in
                            SourceRow(source: source)
                                .padding(.horizontal, AnnoTheme.md)

                            // Separator between rows, not after the last one
                            if index < sources.count - 1 {
                                Rectangle()
                                    .fill(AnnoTheme.ash)
                                    .frame(height: 1)
                                    .padding(.leading, 60) // aligned past the icon
                                    .accessibilityHidden(true)
                            }
                        }
                    }
                    .annoCard()
                    .shadow(
                        color: AnnoTheme.subtleShadow.color,
                        radius: AnnoTheme.subtleShadow.radius,
                        x: AnnoTheme.subtleShadow.x,
                        y: AnnoTheme.subtleShadow.y
                    )
                }
            }
        }
    }

    // MARK: - Source Count Badge

    private var sourceCountBadge: some View {
        Text("\(totalSourceCount)")
            .font(AnnoTheme.caption(11, weight: .bold))
            .foregroundStyle(AnnoTheme.narthex)
            .padding(.horizontal, AnnoTheme.sm)
            .padding(.vertical, AnnoTheme.xs)
            .background(AnnoTheme.goldLeaf)
            .clipShape(Capsule())
            .accessibilityLabel(
                language == .vietnamese
                    ? "\(totalSourceCount) nguồn"
                    : "\(totalSourceCount) sources"
            )
    }
}

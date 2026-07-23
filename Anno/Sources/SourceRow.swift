import SwiftUI

struct SourceRow: View {
    let source: SourceRef

    // MARK: - Source Type Mapping

    /// SF Symbol name for the given source type string.
    private var sourceIcon: String {
        switch source.type.lowercased() {
        case "liturgical":      return "book.closed"
        case "historical":      return "clock"
        case "church_biography": return "globe"
        case "academic":        return "doc.text"
        default:                return "text.book.closed"
        }
    }

    /// Accent color for the source type badge.
    private var sourceTypeColor: Color {
        switch source.type.lowercased() {
        case "liturgical":       return AnnoTheme.goldLeaf
        case "historical":       return AnnoTheme.lapis
        case "church_biography": return AnnoTheme.verdigris
        case "academic":         return AnnoTheme.advent
        default:                 return AnnoTheme.incense
        }
    }

    /// Human-readable display name for the source type.
    private var sourceTypeLabel: String {
        source.type
            .replacingOccurrences(of: "_", with: " ")
            .capitalized
    }

    // MARK: - Body

    var body: some View {
        HStack(alignment: .top, spacing: AnnoTheme.md) {
            // Source type icon
            Image(systemName: sourceIcon)
                .font(.system(size: 18, weight: .medium))
                .foregroundStyle(sourceTypeColor)
                .frame(width: 32, height: 32)
                .background(sourceTypeColor.opacity(0.12))
                .clipShape(RoundedRectangle(cornerRadius: 6))
                .accessibilityHidden(true)

            VStack(alignment: .leading, spacing: AnnoTheme.sm) {
                // Source label
                Text(source.label)
                    .font(AnnoTheme.body(16, weight: .semibold))
                    .foregroundStyle(AnnoTheme.vellum)
                    .fixedSize(horizontal: false, vertical: true)

                // Type badge
                Text(sourceTypeLabel)
                    .font(AnnoTheme.caption(11, weight: .semibold))
                    .foregroundStyle(sourceTypeColor)
                    .padding(.horizontal, AnnoTheme.sm)
                    .padding(.vertical, AnnoTheme.xs)
                    .background(sourceTypeColor.opacity(0.12))
                    .clipShape(Capsule())

                // Link button
                if let url = URL(string: source.url) {
                    Link(destination: url) {
                        HStack(spacing: AnnoTheme.xs) {
                            Image(systemName: "safari")
                                .font(.system(size: 12, weight: .semibold))
                            Text("Open Source")
                                .font(AnnoTheme.caption(12, weight: .semibold))
                        }
                        .foregroundStyle(AnnoTheme.narthex)
                        .padding(.horizontal, AnnoTheme.md)
                        .padding(.vertical, AnnoTheme.sm)
                        .background(AnnoTheme.goldLeaf)
                        .clipShape(Capsule())
                    }
                    .accessibilityLabel("Open \(source.label) in browser")
                }
            }
        }
        .padding(.vertical, AnnoTheme.sm)
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(sourceTypeLabel) source: \(source.label)")
    }
}

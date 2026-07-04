import SwiftUI

struct SourceRow: View {
    let source: SourceRef

    var body: some View {
        VStack(alignment: .leading, spacing: 7) {
            Text(source.label)
                .font(.headline)
                .foregroundStyle(AnnoTheme.vellum)
                .fixedSize(horizontal: false, vertical: true)

            Text(source.url)
                .font(.caption)
                .foregroundStyle(AnnoTheme.incense)
                .lineLimit(2)

            if let url = URL(string: source.url) {
                Link(destination: url) {
                    Label("Open link", systemImage: "safari")
                }
                .font(.callout)
                .foregroundStyle(AnnoTheme.goldLeaf)
            }
        }
        .padding(.vertical, 6)
    }
}

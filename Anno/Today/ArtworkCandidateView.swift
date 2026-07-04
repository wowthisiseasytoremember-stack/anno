import SwiftUI

struct ArtworkCandidateView: View {
    let artwork: ArtworkCandidate

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            ZStack {
                Rectangle()
                    .fill(AnnoTheme.ash)
                    .aspectRatio(1.35, contentMode: .fit)
                Image(systemName: "photo.on.rectangle.angled")
                    .font(.system(size: 34, weight: .light))
                    .foregroundStyle(AnnoTheme.goldLeaf)
            }
            .clipShape(RoundedRectangle(cornerRadius: 8))

            VStack(alignment: .leading, spacing: 4) {
                Text(artwork.title)
                    .font(.headline)
                    .foregroundStyle(AnnoTheme.vellum)
                    .fixedSize(horizontal: false, vertical: true)
                Text("\(artwork.maker) • \(artwork.dateLabel)")
                    .font(.caption)
                    .foregroundStyle(AnnoTheme.incense)
                Text(artwork.status.replacingOccurrences(of: "_", with: " ").capitalized)
                    .font(.caption.weight(.semibold))
                    .foregroundStyle(AnnoTheme.goldLeaf)
            }
        }
        .annoCard()
    }
}

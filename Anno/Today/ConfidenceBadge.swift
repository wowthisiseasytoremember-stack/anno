import SwiftUI

struct ConfidenceBadge: View {
    let label: String
    let confidence: ConfidenceLevel

    var body: some View {
        Label(label, systemImage: iconName)
            .font(.caption.weight(.semibold))
            .padding(.horizontal, 10)
            .padding(.vertical, 6)
            .foregroundStyle(AnnoTheme.confidenceColor(confidence))
            .background(AnnoTheme.confidenceColor(confidence).opacity(0.12))
            .clipShape(Capsule())
    }

    private var iconName: String {
        switch confidence {
        case .confirmed:
            return "checkmark.seal"
        case .traditional:
            return "book.closed"
        case .disputed:
            return "exclamationmark.triangle"
        case .contextual:
            return "scope"
        }
    }
}

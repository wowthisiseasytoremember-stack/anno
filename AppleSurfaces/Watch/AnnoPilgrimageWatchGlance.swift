import SwiftUI

/// Glance-first Apple Watch companion for an active pilgrimage.
///
/// Stage this in a watchOS target later; do not turn the Watch into a full
/// route browser. The Watch's job is presence, next-step context, and prayer.
struct AnnoPilgrimageWatchGlance: View {
    let routeTitle: String
    let chapterTitle: String
    let stationTitle: String
    let nextStationTitle: String?
    let visitedCount: Int
    let totalCount: Int
    let phase: Phase

    enum Phase: String, Sendable {
        case traveling
        case arrived
        case praying
        case completed
    }

    private var progress: Double {
        guard totalCount > 0 else { return 0 }
        return min(1, max(0, Double(visitedCount) / Double(totalCount)))
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 10) {
                HStack {
                    Image(systemName: phaseSymbol)
                        .symbolRenderingMode(.hierarchical)

                    Text(routeTitle)
                        .font(.caption2.weight(.semibold))
                        .lineLimit(1)

                    Spacer()

                    Text("\(visitedCount)/\(totalCount)")
                        .font(.caption2.monospacedDigit().weight(.bold))
                }
                .foregroundStyle(.secondary)

                Text(stationTitle)
                    .font(.headline)
                    .fontDesign(.serif)
                    .lineLimit(3)

                ProgressView(value: progress)
                    .tint(.yellow)

                Text(chapterTitle.uppercased())
                    .font(.caption2.weight(.semibold))
                    .foregroundStyle(.secondary)
                    .tracking(0.8)

                if phase == .arrived {
                    Label("You’ve arrived", systemImage: "mappin.and.ellipse")
                        .font(.caption.weight(.semibold))
                }

                if phase == .praying {
                    Label("Prayer moment", systemImage: "hands.sparkles.fill")
                        .font(.caption.weight(.semibold))
                }

                if let nextStationTitle, phase != .completed {
                    VStack(alignment: .leading, spacing: 2) {
                        Text("NEXT")
                            .font(.caption2.weight(.bold))
                            .foregroundStyle(.secondary)
                        Text(nextStationTitle)
                            .font(.caption)
                            .lineLimit(2)
                    }
                }

                if phase == .completed {
                    Label("Pilgrimage complete", systemImage: "sparkles")
                        .font(.caption.weight(.semibold))
                }
            }
        }
    }

    private var phaseSymbol: String {
        switch phase {
        case .traveling:
            return "figure.walk.motion"
        case .arrived:
            return "mappin.and.ellipse"
        case .praying:
            return "hands.sparkles.fill"
        case .completed:
            return "checkmark.seal.fill"
        }
    }
}

/// Compact view intended for a WidgetKit watch complication / Smart Stack.
struct AnnoPilgrimageWatchComplicationView: View {
    let stationTitle: String
    let visitedCount: Int
    let totalCount: Int

    var body: some View {
        VStack(alignment: .leading, spacing: 2) {
            Label(
                "\(visitedCount)/\(totalCount)",
                systemImage: "figure.walk.motion"
            )
            .font(.caption2.weight(.bold))

            Text(stationTitle)
                .font(.caption2)
                .lineLimit(2)
        }
    }
}

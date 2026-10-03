import ActivityKit
import SwiftUI
import WidgetKit

/// Staged WidgetKit presentation for an active Anno pilgrimage.
///
/// This file intentionally lives outside the shipping target until a Widget
/// Extension is activated and validated in Xcode.
struct AnnoPilgrimageLiveActivityWidget: Widget {
    var body: some WidgetConfiguration {
        ActivityConfiguration(for: AnnoPilgrimageActivityAttributes.self) { context in
            lockScreen(context)
                .activityBackgroundTint(Color(red: 0.075, green: 0.067, blue: 0.055))
                .activitySystemActionForegroundColor(
                    Color(red: 0.85, green: 0.75, blue: 0.43)
                )
        } dynamicIsland: { context in
            DynamicIsland {
                DynamicIslandExpandedRegion(.leading) {
                    VStack(alignment: .leading, spacing: 2) {
                        Image(systemName: context.state.phase == .completed
                              ? "checkmark.seal.fill"
                              : "cross.fill")
                        Text("\(context.state.visitedCount)/\(context.state.totalCount)")
                            .font(.caption2.weight(.bold))
                    }
                    .foregroundStyle(.secondary)
                }

                DynamicIslandExpandedRegion(.trailing) {
                    Image(systemName: phaseSymbol(context.state.phase))
                        .font(.headline)
                        .symbolRenderingMode(.hierarchical)
                }

                DynamicIslandExpandedRegion(.center) {
                    VStack(spacing: 2) {
                        Text(context.state.currentStationTitle)
                            .font(.headline)
                            .fontDesign(.serif)
                            .lineLimit(1)

                        Text(context.state.chapterTitle)
                            .font(.caption2)
                            .foregroundStyle(.secondary)
                            .lineLimit(1)
                    }
                }

                DynamicIslandExpandedRegion(.bottom) {
                    VStack(alignment: .leading, spacing: 6) {
                        progressBar(context.state.progress)

                        if let next = context.state.nextStationTitle,
                           context.state.phase != .completed {
                            Label(next, systemImage: "arrow.right")
                                .font(.caption)
                                .lineLimit(1)
                        } else if context.state.phase == .completed {
                            Label("Pilgrimage complete", systemImage: "sparkles")
                                .font(.caption.weight(.semibold))
                        }
                    }
                }
            } compactLeading: {
                Image(systemName: context.state.phase == .completed
                      ? "checkmark.seal.fill"
                      : "cross.fill")
                    .foregroundStyle(
                        context.state.phase == .completed
                            ? Color(red: 0.85, green: 0.75, blue: 0.43)
                            : .primary
                    )
            } compactTrailing: {
                Text("\(context.state.visitedCount)/\(context.state.totalCount)")
                    .font(.caption2.monospacedDigit().weight(.bold))
            } minimal: {
                Image(systemName: phaseSymbol(context.state.phase))
            }
            .keylineTint(Color(red: 0.85, green: 0.75, blue: 0.43))
        }
    }

    @ViewBuilder
    private func lockScreen(
        _ context: ActivityViewContext<AnnoPilgrimageActivityAttributes>
    ) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack(spacing: 8) {
                Image(systemName: context.state.phase == .completed
                      ? "checkmark.seal.fill"
                      : "figure.walk.motion")
                    .symbolRenderingMode(.hierarchical)

                Text(context.attributes.routeTitle)
                    .font(.caption.weight(.semibold))
                    .lineLimit(1)

                Spacer()

                Text("\(context.state.visitedCount)/\(context.state.totalCount)")
                    .font(.caption.monospacedDigit().weight(.bold))
            }

            Text(context.state.currentStationTitle)
                .font(.headline)
                .fontDesign(.serif)
                .lineLimit(2)

            progressBar(context.state.progress)

            if let next = context.state.nextStationTitle,
               context.state.phase != .completed {
                Text("Next · \(next)")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .lineLimit(1)
            }
        }
        .padding()
    }

    private func progressBar(_ progress: Double) -> some View {
        GeometryReader { proxy in
            ZStack(alignment: .leading) {
                Capsule().fill(.secondary.opacity(0.22))
                Capsule()
                    .fill(
                        LinearGradient(
                            colors: [
                                Color(red: 0.19, green: 0.29, blue: 0.52),
                                Color(red: 0.79, green: 0.66, blue: 0.30)
                            ],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .frame(width: proxy.size.width * progress)
            }
        }
        .frame(height: 6)
    }

    private func phaseSymbol(
        _ phase: AnnoPilgrimageActivityAttributes.ContentState.Phase
    ) -> String {
        switch phase {
        case .traveling:
            return "figure.walk.motion"
        case .arrived:
            return "mappin.and.ellipse"
        case .praying:
            return "hands.sparkles.fill"
        case .completed:
            return "sparkles"
        }
    }
}

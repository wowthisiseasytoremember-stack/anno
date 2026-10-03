import SwiftUI

enum AnnoSurfaceKind {
    case base
    case raised
    case devotional
    case research

    fileprivate var fill: Color {
        switch self {
        case .base:
            return AnnoTheme.surfaceBase
        case .raised:
            return AnnoTheme.surfaceRaised
        case .devotional:
            return AnnoTheme.surfaceRaised
        case .research:
            return AnnoTheme.surfaceInset
        }
    }

    fileprivate var border: Color {
        switch self {
        case .base, .raised:
            return AnnoTheme.borderSubtle
        case .devotional:
            return AnnoTheme.goldLeaf.opacity(0.28)
        case .research:
            return AnnoTheme.lapis.opacity(0.42)
        }
    }

    fileprivate var shadowColor: Color {
        switch self {
        case .raised, .devotional:
            return Color.black.opacity(0.32)
        case .base, .research:
            return .clear
        }
    }
}

private struct AnnoSurfaceModifier: ViewModifier {
    let kind: AnnoSurfaceKind
    let padding: CGFloat
    let cornerRadius: CGFloat

    func body(content: Content) -> some View {
        content
            .padding(padding)
            .background {
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .fill(kind.fill)
            }
            .overlay {
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .strokeBorder(kind.border, lineWidth: 1)
            }
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius, style: .continuous))
            .shadow(color: kind.shadowColor, radius: 10, y: 5)
    }
}

extension View {
    func annoSurface(
        _ kind: AnnoSurfaceKind = .base,
        padding: CGFloat = AnnoTheme.md,
        cornerRadius: CGFloat = AnnoTheme.radiusCard
    ) -> some View {
        modifier(
            AnnoSurfaceModifier(
                kind: kind,
                padding: padding,
                cornerRadius: cornerRadius
            )
        )
    }

    func annoTapTarget() -> some View {
        frame(minWidth: AnnoTheme.minimumTapTarget, minHeight: AnnoTheme.minimumTapTarget)
            .contentShape(Rectangle())
    }
}

struct AnnoSectionLabel: View {
    let title: String
    var symbol: String?
    var accent: Color = AnnoTheme.goldLeaf

    var body: some View {
        HStack(spacing: AnnoTheme.sm) {
            if let symbol {
                AnnoSymbolImage(
                    name: symbol,
                    color: accent,
                    font: Typography.captionSemibold
                )
            }

            Text(title.uppercased())
                .font(Typography.captionSemiboldSerif)
                .foregroundStyle(accent)
                .tracking(1.6)

            Spacer(minLength: 0)
        }
        .accessibilityElement(children: .combine)
        .accessibilityAddTraits(.isHeader)
    }
}

struct AnnoIconBadge: View {
    let symbol: String
    var tint: Color = AnnoTheme.goldLeaf
    var size: CGFloat = AnnoTheme.minimumTapTarget

    var body: some View {
        AnnoSymbolImage(name: symbol, color: tint)
            .frame(width: size, height: size)
            .background {
                RoundedRectangle(cornerRadius: AnnoTheme.radiusCompact, style: .continuous)
                    .fill(tint.opacity(AnnoTheme.subtleFillOpacity))
            }
            .overlay {
                RoundedRectangle(cornerRadius: AnnoTheme.radiusCompact, style: .continuous)
                    .strokeBorder(tint.opacity(0.22), lineWidth: 1)
            }
    }
}

struct AnnoMetadataPill: View {
    let text: String
    var tint: Color = AnnoTheme.textSecondary

    var body: some View {
        Text(text)
            .font(Typography.caption2Medium)
            .foregroundStyle(tint)
            .padding(.horizontal, 10)
            .padding(.vertical, 6)
            .background {
                Capsule()
                    .fill(AnnoTheme.surfaceInset)
            }
            .overlay {
                Capsule()
                    .strokeBorder(AnnoTheme.borderSubtle, lineWidth: 1)
            }
    }
}


struct AnnoStateView: View {
    let symbol: String
    let title: String
    let message: String
    var tint: Color = AnnoTheme.incense
    var actionTitle: String?
    var action: (() -> Void)?

    var body: some View {
        VStack(spacing: AnnoTheme.md) {
            AnnoIconBadge(symbol: symbol, tint: tint, size: 54)

            VStack(spacing: AnnoTheme.sm) {
                Text(title)
                    .font(Typography.headlineSerif)
                    .foregroundStyle(AnnoTheme.textPrimary)
                    .multilineTextAlignment(.center)

                Text(message)
                    .font(Typography.subheadlineSerif)
                    .foregroundStyle(AnnoTheme.textSecondary)
                    .multilineTextAlignment(.center)
                    .fixedSize(horizontal: false, vertical: true)
            }

            if let actionTitle, let action {
                Button(actionTitle, action: action)
                    .font(Typography.subheadlineSemiboldSerif)
                    .foregroundStyle(AnnoTheme.narthex)
                    .padding(.horizontal, AnnoTheme.md)
                    .padding(.vertical, 10)
                    .background(AnnoTheme.goldLeaf)
                    .clipShape(Capsule())
                    .buttonStyle(.plain)
                    .annoTapTarget()
            }
        }
        .frame(maxWidth: .infinity)
        .annoSurface(.raised)
        .accessibilityElement(children: .combine)
    }
}


struct SacredMomentBanner: View {
    let title: String
    var subtitle: String?
    var symbol: String = AnnoSymbol.sacred
    var intensity: SacredIntensity = .feast
    var tint: Color = AnnoTheme.goldLeaf

    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var revealed = false

    var body: some View {
        HStack(spacing: 12) {
            ZStack {
                if intensity == .solemnity {
                    SacredAureole(
                        tint: tint,
                        intensity: .solemnity,
                        diameter: 46
                    )
                }

                Image(systemName: symbol)
                    .font(Typography.iconBody)
                    .symbolRenderingMode(.hierarchical)
                    .foregroundStyle(intensity == .solemnity ? AnnoTheme.narthex : tint)
                    .frame(width: 38, height: 38)
                    .background {
                        Circle()
                            .fill(
                                intensity == .solemnity
                                    ? AnnoTheme.goldLeaf
                                    : tint.opacity(0.14)
                            )
                    }
            }

            VStack(alignment: .leading, spacing: 2) {
                Text(title.uppercased())
                    .font(Typography.captionBold)
                    .foregroundStyle(
                        intensity == .solemnity
                            ? AnnoTheme.gilt
                            : tint
                    )
                    .tracking(1.2)

                if let subtitle {
                    Text(subtitle)
                        .font(Typography.subheadlineSemiboldSerif)
                        .foregroundStyle(AnnoTheme.textPrimary)
                        .lineLimit(2)
                }
            }

            Spacer(minLength: 0)

            if intensity == .solemnity {
                Image(systemName: "sparkles")
                    .foregroundStyle(AnnoTheme.gilt)
                    .symbolEffect(.appear, value: revealed)
            }
        }
        .padding(12)
        .background {
            RoundedRectangle(cornerRadius: AnnoTheme.radiusCard, style: .continuous)
                .fill(
                    LinearGradient(
                        colors: intensity == .solemnity
                            ? [
                                AnnoTheme.goldLeaf.opacity(0.22),
                                AnnoTheme.surfaceRaised,
                                AnnoTheme.candleGlow.opacity(0.12)
                            ]
                            : [
                                tint.opacity(0.10),
                                AnnoTheme.surfaceRaised
                            ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
        }
        .overlay {
            RoundedRectangle(cornerRadius: AnnoTheme.radiusCard, style: .continuous)
                .strokeBorder(
                    intensity == .solemnity
                        ? AnnoTheme.gilt.opacity(0.72)
                        : tint.opacity(0.34),
                    lineWidth: intensity == .solemnity ? 1.4 : 1
                )
        }
        .shadow(
            color: intensity == .solemnity
                ? AnnoTheme.goldLeaf.opacity(0.28)
                : .clear,
            radius: intensity == .solemnity ? 14 : 0,
            y: 4
        )
        .scaleEffect(reduceMotion || revealed ? 1 : 0.96)
        .opacity(revealed ? 1 : 0)
        .animation(reduceMotion ? nil : AnnoMotion.reveal, value: revealed)
        .accessibilityElement(children: .combine)
        .onAppear {
            revealed = true
        }
    }
}

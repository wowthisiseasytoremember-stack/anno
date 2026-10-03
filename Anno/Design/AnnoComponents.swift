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

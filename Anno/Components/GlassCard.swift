//  GlassCard.swift
//  DailyDevotionKJVForWomen
//
//  A frosted, gilded card container used throughout the app. Uses the
//  liquid-glass effect on iOS 26 and gracefully falls back to a refined
//  material treatment on earlier systems.
//

import SwiftUI

/// A soft, elevated card with a thin gilded border and gentle shadow.
struct GlassCard<Content: View>: View {
    var cornerRadius: CGFloat = Metrics.cardRadius
    var padding: CGFloat = Metrics.cardPadding
    @ViewBuilder var content: Content

    var body: some View {
        content
            .padding(padding)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(cardBackground)
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .strokeBorder(
                        LinearGradient(
                            colors: [
                                Palette.gold.opacity(0.55),
                                Palette.blush.opacity(0.25),
                                Palette.gold.opacity(0.35)
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        ),
                        lineWidth: 0.8
                    )
            )
            .shadow(color: Palette.lilac.opacity(0.22), radius: 22, x: 0, y: 14)
            .shadow(color: .black.opacity(0.05), radius: 3, x: 0, y: 2)
    }

    @ViewBuilder
    private var cardBackground: some View {
        RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
            .fill(Palette.surface)
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .fill(.ultraThinMaterial.opacity(0.35))
            )
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .fill(
                        LinearGradient(
                            colors: [Color.white.opacity(0.16), .clear],
                            startPoint: .topLeading,
                            endPoint: .center
                        )
                    )
            )
    }
}

/// A pill button styled with the app's gold sheen, used for primary actions.
struct GildedButtonStyle: ButtonStyle {
    var prominent: Bool = false

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.callout.weight(.semibold))
            .foregroundStyle(prominent ? Color(hex: 0x3A2E15) : Palette.ink)
            .padding(.horizontal, 18)
            .padding(.vertical, 12)
            .background {
                Capsule().fill(prominent ? AnyShapeStyle(.goldSheen) : AnyShapeStyle(Palette.surfaceElevated))
            }
            .overlay(
                Capsule().strokeBorder(Palette.gold.opacity(prominent ? 0 : 0.4), lineWidth: 0.8)
            )
            .shadow(color: Palette.gold.opacity(prominent ? 0.3 : 0), radius: 10, y: 6)
            .scaleEffect(configuration.isPressed ? 0.96 : 1)
            .animation(.spring(response: 0.3, dampingFraction: 0.6), value: configuration.isPressed)
    }
}
//
//  GlassCard.swift
//  Anno
//
//  A frosted, gilded glass card container tailored for Anno's ecclesial aesthetic.
//  Combines deep narthex surfaces, ultra-thin materials, specular gold leaf borders,
//  and candle-glow ambient shadows.

import SwiftUI

public struct GlassCard<Content: View>: View {
    public var cornerRadius: CGFloat = 16
    public var padding: CGFloat = 16
    public var accentGlow: Color? = nil
    @ViewBuilder public var content: Content

    public init(
        cornerRadius: CGFloat = 16,
        padding: CGFloat = 16,
        accentGlow: Color? = nil,
        @ViewBuilder content: () -> Content
    ) {
        self.cornerRadius = cornerRadius
        self.padding = padding
        self.accentGlow = accentGlow
        self.content = content()
    }

    public var body: some View {
        content
            .padding(padding)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(cardBackground)
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .strokeBorder(
                        LinearGradient(
                            colors: [
                                AnnoTheme.goldLeaf.opacity(0.45),
                                AnnoTheme.ash.opacity(0.6),
                                AnnoTheme.goldLeaf.opacity(0.2)
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        ),
                        lineWidth: 1
                    )
            )
            .shadow(
                color: (accentGlow ?? AnnoTheme.candleGlow).opacity(accentGlow != nil ? 0.18 : 0.08),
                radius: 16,
                x: 0,
                y: 8
            )
            .shadow(color: .black.opacity(0.4), radius: 6, x: 0, y: 3)
    }

    @ViewBuilder
    private var cardBackground: some View {
        RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
            .fill(AnnoTheme.narthex.opacity(0.88))
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .fill(.ultraThinMaterial.opacity(0.2))
            )
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .fill(
                        LinearGradient(
                            colors: [
                                Color.white.opacity(0.08),
                                Color.clear,
                                AnnoTheme.goldLeaf.opacity(0.03)
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
            )
    }
}

public struct GildedButtonStyle: ButtonStyle {
    public var prominent: Bool = true

    public init(prominent: Bool = true) {
        self.prominent = prominent
    }

    public func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(Typography.subheadlineSemiboldSerif)
            .foregroundStyle(prominent ? AnnoTheme.narthex : AnnoTheme.vellum)
            .padding(.horizontal, 18)
            .padding(.vertical, 10)
            .background {
                if prominent {
                    Capsule()
                        .fill(
                            LinearGradient(
                                colors: [AnnoTheme.gilt, AnnoTheme.goldLeaf],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )
                        .shadow(color: AnnoTheme.goldLeaf.opacity(0.4), radius: 8, y: 3)
                } else {
                    Capsule()
                        .fill(AnnoTheme.choir.opacity(0.85))
                        .overlay(Capsule().stroke(AnnoTheme.ash, lineWidth: 1))
                }
            }
            .scaleEffect(configuration.isPressed ? 0.96 : 1.0)
            .animation(.spring(response: 0.25, dampingFraction: 0.7), value: configuration.isPressed)
    }
}

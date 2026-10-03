//  WelcomeView.swift
//  Anno
//
//  First-run welcome for the narrow v1 product.

import SwiftUI

struct WelcomeView: View {
    var onContinue: () -> Void

    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var appear = false

    var body: some View {
        ZStack {
            AnnoTheme.narthex.ignoresSafeArea()

            VStack(spacing: AnnoTheme.lg) {
                Spacer()

                ZStack {
                    SolemnityBloom(
                        tint: AnnoTheme.goldLeaf,
                        active: true
                    )
                    .frame(width: 220, height: 160)

                    SacredAureole(
                        tint: AnnoTheme.goldLeaf,
                        intensity: .solemnity,
                        diameter: 92
                    )

                    Image(systemName: AnnoSymbol.welcome)
                        .font(Typography.iconHeroLarge)
                        .foregroundStyle(AnnoTheme.goldLeaf)
                }
                .opacity(appear ? 1 : 0)
                .scaleEffect(appear || reduceMotion ? 1 : 0.9)
                .accessibilityHidden(true)

                VStack(spacing: 12) {
                    Text("Welcome to Anno")
                        .font(Typography.largeTitleBoldSerif)
                        .foregroundStyle(AnnoTheme.vellum)
                        .multilineTextAlignment(.center)
                        .accessibilityAddTraits(.isHeader)

                    SacredDivider(
                        tint: AnnoTheme.goldLeaf,
                        intensity: .solemnity
                    )
                    .frame(maxWidth: 180)

                    Text("A Catholic daily companion for sourced devotional history, sacred art, and five flagship pilgrimage routes.")
                        .font(Typography.bodySerif)
                        .foregroundStyle(AnnoTheme.incense)
                        .multilineTextAlignment(.center)
                        .fixedSize(horizontal: false, vertical: true)
                        .padding(.horizontal, AnnoTheme.lg)
                }
                .opacity(appear ? 1 : 0)
                .offset(y: appear || reduceMotion ? 0 : 12)

                Spacer()

                VStack(spacing: 14) {
                    featureRow(
                        icon: AnnoSymbol.today,
                        title: "Daily Devotional",
                        subtitle: "Sourced Catholic history, prayer, art, and confidence labels"
                    )
                    featureRow(
                        icon: AnnoSymbol.route,
                        title: "Start Close to Home",
                        subtitle: "Begin with the Orange County La Vang pilgrimage, then explore Jerusalem, Rome, Santiago, and Guadalupe"
                    )
                    featureRow(
                        icon: AnnoSymbol.language,
                        title: "English-first",
                        subtitle: "Vietnamese support is included and expands from the major-feast v1 baseline"
                    )
                }
                .padding(.horizontal, AnnoTheme.lg)
                .opacity(appear ? 1 : 0)
                .offset(y: appear || reduceMotion ? 0 : 16)

                Spacer()

                Button {
                    Haptics.soft()
                    onContinue()
                } label: {
                    Text("Begin")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(AnnoGildedButtonStyle(prominent: true))
                .padding(.horizontal, AnnoTheme.lg)
                .padding(.bottom, 20)
                .opacity(appear ? 1 : 0)
                .accessibilityHint("Opens the Anno daily devotional")
            }
        }
        .presentationBackground(.clear)
        .onAppear {
            if reduceMotion {
                appear = true
            } else {
                withAnimation(AnnoMotion.reveal) {
                    appear = true
                }
            }
        }
    }

    private func featureRow(icon: String, title: String, subtitle: String) -> some View {
        HStack(spacing: 14) {
            Image(systemName: icon)
                .font(Typography.headlineSerif)
                .foregroundStyle(AnnoTheme.goldLeaf)
                .frame(width: 40, height: 40)
                .background(Circle().fill(AnnoTheme.choir))
                .overlay(Circle().strokeBorder(AnnoTheme.ash, lineWidth: 0.8))
                .accessibilityHidden(true)

            VStack(alignment: .leading, spacing: 3) {
                Text(title)
                    .font(Typography.subheadlineSemiboldSerif)
                    .foregroundStyle(AnnoTheme.vellum)
                Text(subtitle)
                    .font(Typography.captionSerif)
                    .foregroundStyle(AnnoTheme.incense)
                    .fixedSize(horizontal: false, vertical: true)
            }

            Spacer(minLength: 0)
        }
        .accessibilityElement(children: .combine)
    }
}

/// Button style matching Anno's restrained gilded aesthetic.
struct AnnoGildedButtonStyle: ButtonStyle {
    var prominent: Bool = false

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(Typography.headlineSerif)
            .foregroundStyle(prominent ? AnnoTheme.narthex : AnnoTheme.goldLeaf)
            .padding(.vertical, 14)
            .frame(maxWidth: .infinity)
            .background(
                RoundedRectangle(cornerRadius: AnnoTheme.radiusCard, style: .continuous)
                    .fill(prominent ? AnnoTheme.goldLeaf : AnnoTheme.choir)
                    .overlay(
                        RoundedRectangle(cornerRadius: AnnoTheme.radiusCard, style: .continuous)
                            .stroke(AnnoTheme.ash, lineWidth: 1)
                    )
            )
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .animation(.easeOut(duration: 0.1), value: configuration.isPressed)
    }
}

#Preview {
    WelcomeView(onContinue: {})
        .preferredColorScheme(.dark)
}

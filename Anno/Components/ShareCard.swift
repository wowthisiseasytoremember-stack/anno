//  ShareCard.swift
//  DailyDevotionKJVForWomen
//
//  A beautiful, self-contained card rendered to an image for sharing via
//  ImageRenderer. Designed to look elegant on social feeds.
//

import SwiftUI

/// The visual layout of a shareable verse card.
struct ShareCard: View {
    let verse: String
    let reference: String

    var body: some View {
        VStack(spacing: 22) {
            ChapterOrnament()

            Text("\u{201C}")
                .font(.serifDisplay(64, weight: .bold))
                .foregroundStyle(Palette.gold.opacity(0.5))
                .frame(height: 30)

            Text(verse)
                .font(.serifDisplay(27, weight: .medium))
                .foregroundStyle(Palette.ink)
                .multilineTextAlignment(.center)
                .lineSpacing(8)
                .fixedSize(horizontal: false, vertical: true)

            GoldDivider(width: 120)

            Text(reference.uppercased())
                .font(.system(.subheadline, design: .serif).weight(.semibold))
                .tracking(3)
                .foregroundStyle(Palette.rose)

            Text("KJV for Women — Daily Devotional")
                .font(.caption2)
                .tracking(1)
                .foregroundStyle(Palette.inkTertiary)
        }
        .padding(44)
        .frame(width: 540, height: 540)
        .background {
            ZStack {
                LinearGradient(
                    colors: [Palette.bgTop, Palette.bgMid, Palette.bgBottom],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                RadialGradient(colors: [Palette.blush.opacity(0.5), .clear], center: .topLeading, startRadius: 0, endRadius: 400)
                RadialGradient(colors: [Palette.gold.opacity(0.18), .clear], center: .bottomTrailing, startRadius: 0, endRadius: 380)
            }
        }
        .overlay(
            RoundedRectangle(cornerRadius: 0)
                .inset(by: 16)
                .strokeBorder(Palette.gold.opacity(0.45), lineWidth: 1)
        )
    }
}

/// Renders a `ShareCard` into a UIImage for ShareLink.
@MainActor
enum ShareCardRenderer {
    static func render(verse: String, reference: String) -> UIImage? {
        let renderer = ImageRenderer(
            content: ShareCard(verse: verse, reference: reference)
                .environment(\.colorScheme, .light)
        )
        renderer.scale = 3
        return renderer.uiImage
    }
}
//
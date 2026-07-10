//  Typography.swift
//  DailyDevotionKJVForWomen
//
//  Elegant serif display type for titles & scripture headings, paired with
//  San Francisco for body. All fonts scale with Dynamic Type.
//

import SwiftUI

extension Font {
    /// Large serif display used for the app title & hero headings.
    static func serifDisplay(_ size: CGFloat, weight: Font.Weight = .regular) -> Font {
        .system(size: size, weight: weight, design: .serif)
    }

    /// Serif title scaled relative to a text style for Dynamic Type support.
    static func serif(_ style: Font.TextStyle, weight: Font.Weight = .regular) -> Font {
        .system(style, design: .serif).weight(weight)
    }
}

extension View {
    /// Applies serif styling that still honours Dynamic Type by scaling
    /// against a reference text style.
    func serifTitle(_ style: Font.TextStyle = .title, weight: Font.Weight = .semibold) -> some View {
        font(.serif(style, weight: weight))
            .foregroundStyle(Palette.ink)
    }
}
//
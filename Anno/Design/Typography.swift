//  Typography.swift
//  Anno
//
//  Semantic typography tokens. Text styles use Dynamic Type rather than
//  hard-coded point sizes so the v1 remains readable at accessibility sizes.

import SwiftUI

enum Typography {

    // MARK: - Display / Title

    static let largeTitleBoldSerif = Font.system(.largeTitle, design: .serif, weight: .bold)
    static let title2BoldSerif = Font.system(.title2, design: .serif, weight: .bold)
    static let title3ItalicSerif = Font.system(.title3, design: .serif, weight: .regular).italic()
    static let headlineSerif = Font.system(.headline, design: .serif, weight: .semibold)

    /// Use only for intentionally art-directed display text.
    static func displaySerif(size: CGFloat, weight: Font.Weight = .regular) -> Font {
        Font.system(size: size, weight: weight, design: .serif)
    }

    // MARK: - Body

    static let bodySerif = Font.system(.body, design: .serif, weight: .regular)
    static let bodySerifItalic = Font.system(.body, design: .serif, weight: .regular).italic()
    static let subheadlineSemiboldSerif = Font.system(.subheadline, design: .serif, weight: .semibold)
    static let subheadlineSerif = Font.system(.subheadline, design: .serif, weight: .regular)
    static let subheadlineMediumSerif = Font.system(.subheadline, design: .serif, weight: .medium)

    // MARK: - Caption / Small

    static let captionSemiboldSerif = Font.system(.caption, design: .serif, weight: .semibold)
    static let captionSerif = Font.system(.caption, design: .serif, weight: .regular)
    static let captionMedium = Font.system(.caption, weight: .medium)
    static let captionSemibold = Font.system(.caption, weight: .semibold)
    static let captionBold = Font.system(.caption, weight: .bold)
    static let captionBoldSerif = Font.system(.caption, design: .serif, weight: .bold)
    static let caption2Bold = Font.system(.caption2, weight: .bold)
    static let caption2Medium = Font.system(.caption2, weight: .medium)
    static let caption2 = Font.system(.caption2, weight: .regular)
    static let caption2MonospacedSemibold = Font.system(.caption2, weight: .semibold).monospacedDigit()
    static let captionItalic = Font.system(.caption, design: .serif, weight: .regular).italic()

    // MARK: - Icon size tokens (SF Symbols)

    // Keep even micro UI legible; these values are decorative symbol sizes,
    // not body text, but the previous 4–6 pt tokens were unnecessarily tiny.
    static let iconMicro = Font.system(size: 8, weight: .black)
    static let iconTiny = Font.system(size: 8, weight: .regular)
    static let iconSmall = Font.system(size: 10, weight: .semibold)
    static let iconCaption = Font.system(size: 11, weight: .medium)
    static let iconCaption2 = Font.system(size: 12, weight: .semibold)
    static let iconBody = Font.system(size: 16, weight: .semibold)
    static let iconTitle = Font.system(size: 24, weight: .regular)
    static let iconTitle2 = Font.system(size: 28, weight: .regular)
    static let iconLarge = Font.system(size: 36, weight: .regular)
    static let iconHero = Font.system(size: 44, weight: .light)
    static let iconSacredPin = Font.system(size: 30, weight: .bold)
    static let iconHeroLarge = Font.system(size: 52, weight: .light)

    // MARK: - Non-serif utilities

    static let subheadlineSemibold = Font.system(.subheadline, weight: .semibold)

    /// Section title — uses heading semantics for Dynamic Type.
    static let title = Font.system(.title3, design: .serif, weight: .semibold)
}

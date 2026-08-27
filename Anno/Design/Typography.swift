//  Typography.swift
//  Anno
//
//  Typography namespace wrapping AnnoTheme font functions for semantic clarity.

import SwiftUI

enum Typography {

    // MARK: - Display / Title

    static let largeTitleBoldSerif = AnnoTheme.display(34, weight: .bold)
    static let title2BoldSerif = AnnoTheme.display(22, weight: .bold)
    static let title3ItalicSerif = AnnoTheme.display(20, weight: .regular).italic()
    static let headlineSerif = AnnoTheme.heading(17, weight: .semibold)

    /// Dynamic display sizing for ShareCard etc.
    static func displaySerif(size: CGFloat, weight: Font.Weight = .regular) -> Font {
        AnnoTheme.display(size, weight: weight)
    }

    // MARK: - Body

    static let bodySerif = AnnoTheme.body(17, weight: .regular)
    static let bodySerifItalic = AnnoTheme.body(17, weight: .regular).italic()
    static let subheadlineSemiboldSerif = AnnoTheme.body(15, weight: .semibold)

    // MARK: - Caption / Small

    static let captionSemiboldSerif = AnnoTheme.caption(12, weight: .semibold)
    static let captionSerif = AnnoTheme.caption(12, weight: .regular)
    static let captionMedium = AnnoTheme.caption(12, weight: .medium)
    static let captionSemibold = AnnoTheme.caption(12, weight: .semibold)
    static let captionBold = AnnoTheme.caption(12, weight: .bold)
    static let captionBoldSerif = AnnoTheme.caption(12, weight: .bold)
    static let caption2Bold = AnnoTheme.caption(11, weight: .bold)
    static let caption2Medium = AnnoTheme.caption(11, weight: .medium)
    static let caption2 = AnnoTheme.caption(11, weight: .regular)
    static let caption2MonospacedSemibold = AnnoTheme.caption(11, weight: .semibold).monospacedDigit()
    static let captionItalic = AnnoTheme.caption(12, weight: .regular).italic()

    // MARK: - Non-serif utilities

    static let subheadlineSemibold = Font.system(.subheadline, weight: .semibold)
    static let subheadlineSerif = AnnoTheme.body(15, weight: .regular)
    static let subheadlineMediumSerif = AnnoTheme.body(15, weight: .medium)

    /// Section title — uses heading weight for prominent labels.
    static let title = AnnoTheme.heading(20, weight: .semibold)
}

import SwiftUI

enum AnnoTheme {

    // MARK: - Core Ecclesial Colors

    static let narthex = Color(hex: 0x13110E)
    static let choir = Color(hex: 0x1F1B16)
    static let goldLeaf = Color(hex: 0xC9A84C)
    static let gilt = Color(hex: 0xD9C06E)
    static let lapis = Color(hex: 0x2B4A7C)
    static let crimson = Color(hex: 0x8C2F3B)
    static let vellum = Color(hex: 0xEDE7DA)
    static let incense = Color(hex: 0x9B9085)
    static let ash = Color(hex: 0x2E2A24)
    static let verdigris = Color(hex: 0x3B6B52)
    static let advent = Color(hex: 0x5C3D6E)
    static let easter = Color(hex: 0xF5F0E8)
    static let rose = Color(hex: 0xC96E7E)
    static let candleGlow = Color(hex: 0xEDB84C)

    // MARK: - Confidence Colors

    static func confidenceColor(_ confidence: ConfidenceLevel) -> Color {
        switch confidence {
        case .confirmed:
            return goldLeaf
        case .traditional:
            return lapis
        case .disputed:
            return crimson
        case .contextual:
            return incense
        }
    }

    // MARK: - Liturgical Color Resolvers

    static func liturgicalColor(_ type: LiturgicalColorType) -> Color {
        type.primaryTint
    }

    static func liturgicalColor(named name: String) -> Color {
        LiturgicalColorType.from(rawName: name).primaryTint
    }

    static func liturgicalAccent(named name: String) -> Color {
        LiturgicalColorType.from(rawName: name).secondaryAccent
    }

    static func liturgicalGlow(named name: String) -> Color {
        LiturgicalColorType.from(rawName: name).ambientGlowColor
    }

    // MARK: - Typography

    /// Large display text — e.g. hero titles, splash screens.
    static func display(_ size: CGFloat = 28, weight: Font.Weight = .bold) -> Font {
        Font.system(size: size, weight: weight, design: .serif)
    }

    /// Section headings and navigation titles.
    static func heading(_ size: CGFloat = 20, weight: Font.Weight = .semibold) -> Font {
        Font.system(size: size, weight: weight, design: .serif)
    }

    /// Body / reading text.
    static func body(_ size: CGFloat = 16, weight: Font.Weight = .regular) -> Font {
        Font.system(size: size, weight: weight, design: .serif)
    }

    /// Small captions, metadata, timestamps.
    static func caption(_ size: CGFloat = 12, weight: Font.Weight = .regular) -> Font {
        Font.system(size: size, weight: weight, design: .serif)
    }

    // MARK: - Shadows

    /// Shadow for elevated card surfaces.
    static let cardShadow: (color: Color, radius: CGFloat, x: CGFloat, y: CGFloat) = (
        color: Color.black.opacity(0.45),
        radius: 8,
        x: 0,
        y: 4
    )

    /// Subtle shadow for inline elements and badges.
    static let subtleShadow: (color: Color, radius: CGFloat, x: CGFloat, y: CGFloat) = (
        color: Color.black.opacity(0.25),
        radius: 3,
        x: 0,
        y: 2
    )

    // MARK: - Spacing

    static let xs: CGFloat = 4
    static let sm: CGFloat = 8
    static let md: CGFloat = 16
    static let lg: CGFloat = 24
    static let xl: CGFloat = 32

    /// Transparent row background for List/Form sections.
    static let clearRow = Color.clear

    // MARK: - Animations

    /// Smooth spring used for card reveals and interactive transitions.
    static let cardSpring = Animation.spring(response: 0.4, dampingFraction: 0.75)

    /// Tactile spring for pinch-zoom recovery and double tap toggles.
    static let canvasSpring = Animation.spring(response: 0.35, dampingFraction: 0.8)
}

// MARK: - Color Hex Initializer

extension Color {
    init(hex: UInt, opacity: Double = 1) {
        self.init(
            .sRGB,
            red: Double((hex >> 16) & 0xff) / 255,
            green: Double((hex >> 8) & 0xff) / 255,
            blue: Double(hex & 0xff) / 255,
            opacity: opacity
        )
    }
}

// MARK: - AnnoCard View Modifier

struct AnnoCard: ViewModifier {
    var cornerRadius: CGFloat = 8

    func body(content: Content) -> some View {
        content
            .padding(16)
            .background(AnnoTheme.choir)
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius)
                    .stroke(AnnoTheme.ash, lineWidth: 1)
            )
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius))
    }
}

extension View {
    func annoCard(cornerRadius: CGFloat = 8) -> some View {
        modifier(AnnoCard(cornerRadius: cornerRadius))
    }
}

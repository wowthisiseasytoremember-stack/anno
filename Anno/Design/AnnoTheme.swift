import SwiftUI

enum AnnoTheme {
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
}

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

struct AnnoCard: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding(16)
            .background(AnnoTheme.choir)
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(AnnoTheme.ash, lineWidth: 1)
            )
            .clipShape(RoundedRectangle(cornerRadius: 8))
    }
}

extension View {
    func annoCard() -> some View {
        modifier(AnnoCard())
    }
}

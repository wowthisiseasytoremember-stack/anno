//  LiturgicalThemeModifier.swift
//  Anno
//
//  Dynamic Liturgical Ambient Theming.
//  Provides adaptive ecclesial background gradients, subtle ambient glows,
//  and accent tints matching the liturgical color of the day
//  (White/Gold, Roman Red, Violet/Purple, Rose, Green, Black).

import SwiftUI

// MARK: - Liturgical Color Type

enum LiturgicalColorType: String, CaseIterable, Identifiable, Codable {
    case white = "White"
    case gold = "Gold"
    case red = "Red"
    case violet = "Violet"
    case rose = "Rose"
    case green = "Green"
    case black = "Black"

    var id: String { rawValue }

    // MARK: - Parser

    static func from(rawName: String) -> LiturgicalColorType {
        let normalized = rawName.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
        switch normalized {
        case "red", "đỏ", "passion red", "roman red", "scarlet":
            return .red
        case "white", "trắng", "bạch", "solemnity white":
            return .white
        case "gold", "vàng", "gold leaf", "gilt":
            return .gold
        case "violet", "purple", "tím", "advent violet", "penitential purple":
            return .violet
        case "rose", "hồng", "gaudete rose", "laetare rose":
            return .rose
        case "green", "xanh", "xanh lá", "ordinary time green", "verdigris":
            return .green
        case "black", "đen", "requiem black":
            return .black
        default:
            return .gold
        }
    }

    // MARK: - Localized Names

    var displayNameEn: String {
        switch self {
        case .white: return "Liturgical White"
        case .gold: return "Solemn Gold"
        case .red: return "Roman Red"
        case .violet: return "Penitential Violet"
        case .rose: return "Gaudete Rose"
        case .green: return "Ordinary Green"
        case .black: return "Requiem Black"
        }
    }

    var displayNameVi: String {
        switch self {
        case .white: return "Trắng Phụng Vụ"
        case .gold: return "Vàng Hoàng Kim"
        case .red: return "Đỏ Tử Đạo"
        case .violet: return "Tím Sám Hối"
        case .rose: return "Hồng Hân Hoan"
        case .green: return "Xanh Thường Niên"
        case .black: return "Đen Cầu Hồn"
        }
    }

    func displayName(for language: LanguageMode) -> String {
        language == .vietnamese ? displayNameVi : displayNameEn
    }

    // MARK: - Color Tokens

    var primaryTint: Color {
        switch self {
        case .white:
            return Color(hex: 0xF8F4EB)
        case .gold:
            return AnnoTheme.goldLeaf
        case .red:
            return AnnoTheme.crimson
        case .violet:
            return AnnoTheme.advent
        case .rose:
            return Color(hex: 0xC96E7E)
        case .green:
            return AnnoTheme.verdigris
        case .black:
            return AnnoTheme.ash
        }
    }

    var secondaryAccent: Color {
        switch self {
        case .white:
            return AnnoTheme.gilt
        case .gold:
            return Color(hex: 0xEDB84C)
        case .red:
            return Color(hex: 0xB53243)
        case .violet:
            return Color(hex: 0x8A52A3)
        case .rose:
            return Color(hex: 0xE08D9B)
        case .green:
            return Color(hex: 0x4D8E6F)
        case .black:
            return AnnoTheme.incense
        }
    }

    var ambientGlowColor: Color {
        switch self {
        case .white:
            return Color(hex: 0xF5ECD7).opacity(0.18)
        case .gold:
            return Color(hex: 0xC9A84C).opacity(0.22)
        case .red:
            return Color(hex: 0x8C2F3B).opacity(0.24)
        case .violet:
            return Color(hex: 0x5C3D6E).opacity(0.25)
        case .rose:
            return Color(hex: 0xB3666E).opacity(0.22)
        case .green:
            return Color(hex: 0x3B6B52).opacity(0.22)
        case .black:
            return Color(hex: 0x2E2A24).opacity(0.15)
        }
    }

    var borderHighlight: Color {
        switch self {
        case .white:
            return Color(hex: 0xF5ECD7).opacity(0.40)
        case .gold:
            return AnnoTheme.goldLeaf.opacity(0.45)
        case .red:
            return AnnoTheme.crimson.opacity(0.50)
        case .violet:
            return AnnoTheme.advent.opacity(0.50)
        case .rose:
            return Color(hex: 0xC96E7E).opacity(0.45)
        case .green:
            return AnnoTheme.verdigris.opacity(0.50)
        case .black:
            return AnnoTheme.ash.opacity(0.60)
        }
    }

    // MARK: - Ambient Gradients

    func backgroundGradient(intensity: Double = 0.85) -> some View {
        ZStack {
            AnnoTheme.narthex
                .ignoresSafeArea()

            RadialGradient(
                gradient: Gradient(colors: [
                    ambientGlowColor.opacity(intensity),
                    ambientGlowColor.opacity(intensity * 0.4),
                    Color.clear
                ]),
                center: .top,
                startRadius: 20,
                endRadius: 420
            )
            .ignoresSafeArea(edges: .top)

            LinearGradient(
                gradient: Gradient(colors: [
                    ambientGlowColor.opacity(intensity * 0.3),
                    Color.clear,
                    AnnoTheme.narthex.opacity(0.9)
                ]),
                startPoint: .top,
                endPoint: .bottom
            )
            .ignoresSafeArea()
        }
    }
}

// MARK: - Liturgical Atmosphere Modifier

struct LiturgicalAtmosphereModifier: ViewModifier {
    let liturgicalColor: LiturgicalColorType
    var intensity: Double = 0.85

    func body(content: Content) -> some View {
        content
            .background {
                liturgicalColor.backgroundGradient(intensity: intensity)
            }
    }
}

// MARK: - Liturgical Ambient Glow Modifier

struct LiturgicalAmbientGlowModifier: ViewModifier {
    let liturgicalColor: LiturgicalColorType
    var radius: CGFloat = 14
    var opacity: Double = 0.35

    func body(content: Content) -> some View {
        content
            .shadow(
                color: liturgicalColor.ambientGlowColor.opacity(opacity),
                radius: radius,
                x: 0,
                y: 4
            )
    }
}

// MARK: - Liturgical Card Modifier

struct LiturgicalCardModifier: ViewModifier {
    let liturgicalColor: LiturgicalColorType
    var cornerRadius: CGFloat = 12

    func body(content: Content) -> some View {
        content
            .padding(16)
            .background(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .fill(AnnoTheme.choir)
                    .overlay(
                        RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                            .fill(
                                LinearGradient(
                                    colors: [
                                        liturgicalColor.ambientGlowColor.opacity(0.12),
                                        Color.clear
                                    ],
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                            )
                    )
            )
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .strokeBorder(
                        LinearGradient(
                            colors: [
                                liturgicalColor.borderHighlight,
                                AnnoTheme.ash.opacity(0.8)
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        ),
                        lineWidth: 1
                    )
            )
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius, style: .continuous))
            .shadow(color: Color.black.opacity(0.35), radius: 10, x: 0, y: 4)
    }
}

// MARK: - View Extensions

extension View {
    /// Applies a dynamic ecclesial ambient background matching the given liturgical color.
    func liturgicalAtmosphere(color: LiturgicalColorType, intensity: Double = 0.85) -> some View {
        modifier(LiturgicalAtmosphereModifier(liturgicalColor: color, intensity: intensity))
    }

    /// Convenience modifier parsing raw liturgical color strings (e.g. "Red", "Tím", "Gold").
    func liturgicalAtmosphere(named colorName: String, intensity: Double = 0.85) -> some View {
        modifier(LiturgicalAtmosphereModifier(liturgicalColor: LiturgicalColorType.from(rawName: colorName), intensity: intensity))
    }

    /// Adds a soft ambient glow halo tinted to the liturgical color.
    func liturgicalGlow(color: LiturgicalColorType, radius: CGFloat = 14, opacity: Double = 0.35) -> some View {
        modifier(LiturgicalAmbientGlowModifier(liturgicalColor: color, radius: radius, opacity: opacity))
    }

    /// Convenience glow modifier parsing raw liturgical color strings.
    func liturgicalGlow(named colorName: String, radius: CGFloat = 14, opacity: Double = 0.35) -> some View {
        modifier(LiturgicalAmbientGlowModifier(liturgicalColor: LiturgicalColorType.from(rawName: colorName), radius: radius, opacity: opacity))
    }

    /// Styles a card container with subtle liturgical gradient highlights and tinted borders.
    func liturgicalCard(color: LiturgicalColorType, cornerRadius: CGFloat = 12) -> some View {
        modifier(LiturgicalCardModifier(liturgicalColor: color, cornerRadius: cornerRadius))
    }

    /// Convenience card modifier parsing raw liturgical color strings.
    func liturgicalCard(named colorName: String, cornerRadius: CGFloat = 12) -> some View {
        modifier(LiturgicalCardModifier(liturgicalColor: LiturgicalColorType.from(rawName: colorName), cornerRadius: cornerRadius))
    }
}

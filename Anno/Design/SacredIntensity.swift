import SwiftUI

enum SacredIntensity: Int, Comparable, Sendable {
    case ordinary = 0
    case feast = 1
    case solemnity = 2

    static func < (lhs: SacredIntensity, rhs: SacredIntensity) -> Bool {
        lhs.rawValue < rhs.rawValue
    }

    static func from(rank: String) -> SacredIntensity {
        switch rank.trimmingCharacters(in: .whitespacesAndNewlines).lowercased() {
        case "solemnity":
            return .solemnity
        case "sunday", "feast", "memorial", "optional memorial":
            return .feast
        default:
            return .ordinary
        }
    }

    var atmosphereIntensity: Double {
        switch self {
        case .ordinary: return 0.52
        case .feast: return 0.72
        case .solemnity: return 0.96
        }
    }

    var aureoleOpacity: Double {
        switch self {
        case .ordinary: return 0
        case .feast: return 0.28
        case .solemnity: return 0.62
        }
    }

    var revealDistance: CGFloat {
        switch self {
        case .ordinary: return 8
        case .feast: return 12
        case .solemnity: return 18
        }
    }
}

struct SacredAureole: View {
    let tint: Color
    let intensity: SacredIntensity
    var diameter: CGFloat = 44

    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var revealed = false

    var body: some View {
        ZStack {
            Circle()
                .stroke(
                    AngularGradient(
                        colors: [
                            tint.opacity(0.05),
                            AnnoTheme.gilt.opacity(intensity.aureoleOpacity),
                            tint.opacity(0.12),
                            AnnoTheme.goldLeaf.opacity(intensity.aureoleOpacity),
                            tint.opacity(0.05)
                        ],
                        center: .center
                    ),
                    lineWidth: intensity == .solemnity ? 2 : 1
                )

            if intensity == .solemnity {
                Circle()
                    .stroke(AnnoTheme.gilt.opacity(0.16), lineWidth: 6)
                    .blur(radius: 5)
            }
        }
        .frame(width: diameter, height: diameter)
        .scaleEffect(reduceMotion || revealed ? 1 : 0.82)
        .opacity(revealed ? 1 : 0)
        .animation(reduceMotion ? nil : AnnoMotion.immersive, value: revealed)
        .allowsHitTesting(false)
        .accessibilityHidden(true)
        .onAppear {
            revealed = true
        }
    }
}

struct SolemnityBloom: View {
    let tint: Color
    let active: Bool

    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var visible = false

    var body: some View {
        RadialGradient(
            colors: [
                AnnoTheme.gilt.opacity(active ? 0.22 : 0.08),
                tint.opacity(active ? 0.12 : 0.04),
                .clear
            ],
            center: .center,
            startRadius: 0,
            endRadius: active ? 180 : 120
        )
        .scaleEffect(reduceMotion || visible ? 1 : 0.72)
        .opacity(visible ? 1 : 0)
        .animation(reduceMotion ? nil : .easeOut(duration: 1.1), value: visible)
        .allowsHitTesting(false)
        .accessibilityHidden(true)
        .onAppear {
            visible = true
        }
    }
}


struct SacredDivider: View {
    let tint: Color
    let intensity: SacredIntensity

    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var revealed = false

    var body: some View {
        HStack(spacing: 10) {
            Rectangle()
                .fill(
                    LinearGradient(
                        colors: [.clear, tint.opacity(0.7)],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .frame(height: 1)
                .scaleEffect(x: reduceMotion || revealed ? 1 : 0, anchor: .trailing)

            Image(systemName: AnnoSymbol.sacred)
                .font(Typography.caption2)
                .foregroundStyle(intensity == .solemnity ? AnnoTheme.gilt : tint)
                .symbolEffect(.appear, value: revealed)

            Rectangle()
                .fill(
                    LinearGradient(
                        colors: [tint.opacity(0.7), .clear],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .frame(height: 1)
                .scaleEffect(x: reduceMotion || revealed ? 1 : 0, anchor: .leading)
        }
        .opacity(revealed ? 1 : 0)
        .animation(reduceMotion ? nil : AnnoMotion.reveal, value: revealed)
        .accessibilityHidden(true)
        .onAppear {
            revealed = true
        }
    }
}

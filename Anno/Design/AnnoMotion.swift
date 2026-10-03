import SwiftUI

enum AnnoMotion {
    /// Quiet entrance/reveal animation for cards and sections.
    static let reveal = Animation.spring(response: 0.48, dampingFraction: 0.86)

    /// Short, tactile state change.
    static let selection = Animation.spring(response: 0.28, dampingFraction: 0.78)

    /// Larger canvas or artwork transition.
    static let immersive = Animation.spring(response: 0.58, dampingFraction: 0.9)

    /// Ambient transitions should be slow enough to feel atmospheric, not busy.
    static let atmosphere = Animation.easeInOut(duration: 0.65)
}

private struct AnnoRevealModifier: ViewModifier {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    let isVisible: Bool
    let distance: CGFloat
    let delay: Double

    func body(content: Content) -> some View {
        content
            .opacity(isVisible ? 1 : 0)
            .offset(y: reduceMotion || isVisible ? 0 : distance)
            .animation(
                reduceMotion ? nil : AnnoMotion.reveal.delay(delay),
                value: isVisible
            )
    }
}

extension View {
    /// Standard Anno reveal that automatically becomes opacity-only when
    /// Reduce Motion is enabled.
    func annoReveal(
        isVisible: Bool,
        distance: CGFloat = 12,
        delay: Double = 0
    ) -> some View {
        modifier(
            AnnoRevealModifier(
                isVisible: isVisible,
                distance: distance,
                delay: delay
            )
        )
    }
}

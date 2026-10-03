import SwiftUI

/// Semantic icon vocabulary for Anno.
///
/// Keep product meaning here instead of scattering raw SF Symbol names
/// throughout views. Custom symbols can replace individual entries later
/// without rewriting the UI.
enum AnnoSymbol {
    static let today = "sun.max.fill"
    static let calendar = "calendar"
    static let pilgrimage = "figure.walk.motion"
    static let sources = "books.vertical.fill"
    static let settings = "gearshape"
    static let artworkExpand = "arrow.up.left.and.arrow.down.right"
    static let artworkUnavailable = "photo.on.rectangle.angled"
    static let prayer = "hands.sparkles.fill"
    static let confidence = "checkmark.seal.fill"
    static let route = "map.fill"
    static let waypoint = "mappin.circle.fill"
    static let language = "character.book.closed.fill"
    static let close = "xmark.circle.fill"
    static let sacred = "cross.fill"
    static let welcome = "cross.case.fill"
}

struct AnnoSymbolImage: View {
    let name: String
    var color: Color = AnnoTheme.goldLeaf
    var font: Font = Typography.iconBody

    var body: some View {
        Image(systemName: name)
            .font(font)
            .symbolRenderingMode(.hierarchical)
            .foregroundStyle(color)
            .accessibilityHidden(true)
    }
}

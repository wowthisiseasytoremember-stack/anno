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
    static let externalLink = "arrow.up.right"
    static let retry = "arrow.clockwise"
    static let historical = "clock.fill"
    static let liturgical = "book.closed.fill"
    static let churchBiography = "building.columns.fill"
    static let academic = "doc.text.magnifyingglass"
    static let genericSource = "text.book.closed.fill"
    static let marian = "heart.fill"
    static let apostolic = "cross.fill"
    static let martyr = "flame.fill"
    static let eucharistic = "sun.max.fill"
    static let monastic = "mountain.2.fill"

    static func sourceType(_ rawValue: String) -> String {
        switch rawValue.lowercased() {
        case "liturgical":
            return liturgical
        case "historical":
            return historical
        case "church_biography":
            return churchBiography
        case "academic":
            return academic
        default:
            return genericSource
        }
    }

    static func confidence(_ value: ConfidenceLevel) -> String {
        switch value {
        case .confirmed:
            return "checkmark.seal.fill"
        case .traditional:
            return "scroll.fill"
        case .disputed:
            return "questionmark.diamond.fill"
        case .contextual:
            return "info.circle.fill"
        }
    }

    static func spiritualCalling(_ calling: SpiritualCalling) -> String {
        switch calling {
        case .all:
            return "sparkles"
        case .marian:
            return marian
        case .apostolic:
            return apostolic
        case .martyrs:
            return martyr
        case .eucharisticPassion:
            return eucharistic
        case .monasticDesert:
            return monastic
        }
    }
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

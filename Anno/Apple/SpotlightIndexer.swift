import CoreSpotlight
import Foundation
import UniformTypeIdentifiers

@MainActor
enum SpotlightIndexer {
    static let entryPrefix = "entry:"
    static let routePrefix = "route:"

    private static let index = CSSearchableIndex(name: "AnnoPublicContent")

    static func indexContent(entries: [AnnoEntry], routes: [PilgrimageRoute]) async {
        let entryItems = entries.map(makeEntryItem)
        let routeItems = routes.map(makeRouteItem)

        do {
            try await index.indexSearchableItems(entryItems + routeItems)
        } catch {
            // Spotlight is an enhancement, never a blocker for devotional content.
            #if DEBUG
            print("Anno Spotlight indexing failed: \(error)")
            #endif
        }
    }

    private static func makeEntryItem(_ entry: AnnoEntry) -> CSSearchableItem {
        let attributes = CSSearchableItemAttributeSet(contentType: .text)
        attributes.title = entry.primary.titleEn
        attributes.displayName = entry.primary.titleEn
        attributes.contentDescription = entry.primary.summaryEn
        attributes.keywords = [
            "Anno",
            "Catholic",
            "devotional",
            "saint",
            "feast",
            entry.date,
            entry.liturgical.rank,
            entry.liturgical.titleEn
        ]

        return CSSearchableItem(
            uniqueIdentifier: entryPrefix + entry.id,
            domainIdentifier: "org.anno.entries",
            attributeSet: attributes
        )
    }

    private static func makeRouteItem(_ route: PilgrimageRoute) -> CSSearchableItem {
        let attributes = CSSearchableItemAttributeSet(contentType: .text)
        attributes.title = route.titleEn
        attributes.displayName = route.titleEn
        attributes.contentDescription = route.overviewEn
        var keywords = [
            "Anno",
            "Catholic",
            "pilgrimage",
            "route",
            route.region,
            route.spiritualThemeEn
        ]

        if route.routeId == "socal_vietnamese_catholic_pilgrimage_la_vang" {
            keywords.append(contentsOf: [
                "Our Lady of La Vang",
                "La Vang",
                "Vietnamese Catholic",
                "Vietnamese Catholic Orange County",
                "Orange County",
                "Garden Grove",
                "Santa Ana",
                "Little Saigon"
            ])
        }

        attributes.keywords = keywords

        return CSSearchableItem(
            uniqueIdentifier: routePrefix + route.routeId,
            domainIdentifier: "org.anno.routes",
            attributeSet: attributes
        )
    }
}

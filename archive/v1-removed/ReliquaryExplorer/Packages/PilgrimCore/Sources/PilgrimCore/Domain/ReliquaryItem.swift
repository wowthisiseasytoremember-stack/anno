import Foundation

/// A 3-D reliquary or Passion-textile model exposed by the AR viewer.
///
/// Assets are assumed to be produced and optimized upstream (`.usdz` or
/// `.reality`). `modelAssetName` is the bundle resource name **without**
/// extension — `Entity.loadAsync(named:)` resolves either extension.
/// The asset contract (documented in the README):
///
/// - Pivot at the **base center** of the object (so upright placement sits
///   on the surface without offset math).
/// - Natural size at scale `1.0`; `defaultScale` is applied on placement.
/// - Y+ is up; forward (Z-) faces the viewer at yaw `0`.
public struct ReliquaryItem: Identifiable, Codable, Hashable, Sendable {
    public let id: String
    public let title: String
    public let era: String
    public let modelAssetName: String
    public let defaultScale: Float
    public let scaleBounds: ClosedRange<Float>
    public let historicalNotes: String

    public init(
        id: String,
        title: String,
        era: String,
        modelAssetName: String,
        defaultScale: Float,
        scaleBounds: ClosedRange<Float> = 0.05...3.0,
        historicalNotes: String
    ) {
        self.id = id
        self.title = title
        self.era = era
        self.modelAssetName = modelAssetName
        self.defaultScale = defaultScale
        self.scaleBounds = scaleBounds
        self.historicalNotes = historicalNotes
    }

    /// Static catalog. Like sanctuary coordinates, this can be moved into
    /// JSON later; it is kept in code because the set of curated 3-D items
    /// changes with the art pipeline, not with site data.
    public static let catalog: [ReliquaryItem] = [
        ReliquaryItem(
            id: "reliquary_passion_cross",
            title: "Cruciform Passion Reliquary",
            era: "12th Century Romanesque",
            modelAssetName: "CruciformReliquary",
            defaultScale: 0.35,
            historicalNotes: "Gilded silver repoussé adorned with cabochon sapphires and micro-filigree filters."
        ),
        ReliquaryItem(
            id: "reliquary_passion_textile",
            title: "Holy Textile Casket",
            era: "14th Century Byzantine",
            modelAssetName: "TextileCasket",
            defaultScale: 0.40,
            historicalNotes: "Embroidered silk samite with gold-spun thread depictions of the entombment."
        ),
        ReliquaryItem(
            id: "reliquary_silver_casket",
            title: "Apostolic Silver Casket",
            era: "9th Century Carolingian",
            modelAssetName: "SilverApostolicCasket",
            defaultScale: 0.30,
            historicalNotes: "Oxidized silver chassis with arcade of apostle figures under arcuated gables."
        ),
    ]

    public static func item(withID id: String) -> ReliquaryItem? {
        catalog.first { $0.id == id }
    }
}

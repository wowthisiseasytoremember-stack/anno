import SwiftUI
import MapKit
import SwiftData
import CoreLocation

// MARK: - Localization Catalog
/// All UI chrome strings pass through here. Historical content remains in fixture data (English v0).
enum L {
    // Sections
    static let sacredAtlas       = LocalizedStringKey("anno.section.sacredAtlas")
    static let pilgrimMode       = LocalizedStringKey("anno.section.pilgrimMode")
    static let routePacks        = LocalizedStringKey("anno.section.routePacks")
    static let passport          = LocalizedStringKey("anno.section.passport")
    static let nearby            = LocalizedStringKey("anno.section.nearby")
    static let today             = LocalizedStringKey("anno.section.today")
    static let whyItMatters      = LocalizedStringKey("anno.section.whyItMatters")
    static let connectedEvents   = LocalizedStringKey("anno.section.connectedEvents")
    static let visitingHours     = LocalizedStringKey("anno.section.visitingHours")
    static let onThisGround      = LocalizedStringKey("anno.section.onThisGround")
    
    // Traditions
    static let all               = LocalizedStringKey("anno.tradition.all")
    static let catholic          = LocalizedStringKey("anno.tradition.catholic")
    static let orthodox          = LocalizedStringKey("anno.tradition.orthodox")
    static let jewish            = LocalizedStringKey("anno.tradition.jewish")
    static let islamic           = LocalizedStringKey("anno.tradition.islamic")
    static let interfaith        = LocalizedStringKey("anno.tradition.interfaith")
    
    // Confidence
    static let confirmed         = LocalizedStringKey("anno.confidence.confirmed")
    static let traditional       = LocalizedStringKey("anno.confidence.traditional")
    static let disputed          = LocalizedStringKey("anno.confidence.disputed")
    
    // Categories
    static let catMartyrdom      = LocalizedStringKey("anno.cat.martyrdom")
    static let catCouncil        = LocalizedStringKey("anno.cat.council")
    static let catRelic          = LocalizedStringKey("anno.cat.relic")
    static let catMarian         = LocalizedStringKey("anno.cat.marian")
    static let catMonastic       = LocalizedStringKey("anno.cat.monastic")
    static let catBiblical       = LocalizedStringKey("anno.cat.biblical")
    static let catPilgrimage     = LocalizedStringKey("anno.cat.pilgrimage")
    static let catBasilica       = LocalizedStringKey("anno.cat.basilica")
    
    // Actions
    static let readMore          = LocalizedStringKey("anno.action.readMore")
    static let save              = LocalizedStringKey("anno.action.save")
    static let saved             = LocalizedStringKey("anno.action.saved")
    static let share             = LocalizedStringKey("anno.action.share")
    static let directions        = LocalizedStringKey("anno.action.directions")
    static let sources           = LocalizedStringKey("anno.action.sources")
    static let markVisited       = LocalizedStringKey("anno.action.markVisited")
    static let addNote           = LocalizedStringKey("anno.action.addNote")
    static let startPilgrimage   = LocalizedStringKey("anno.action.startPilgrimage")
    static let continueJourney   = LocalizedStringKey("anno.action.continueJourney")
    static let pauseJourney      = LocalizedStringKey("anno.action.pauseJourney")
    static let endJourney        = LocalizedStringKey("anno.action.endJourney")
    static let previewRoute      = LocalizedStringKey("anno.action.previewRoute")
    static let unlock            = LocalizedStringKey("anno.action.unlock")
    static let restore           = LocalizedStringKey("anno.action.restore")
    static let terms             = LocalizedStringKey("anno.action.terms")
    static let privacy           = LocalizedStringKey("anno.action.privacy")
    
    // Filters
    static let layers            = LocalizedStringKey("anno.filter.layers")
    static let tradition         = LocalizedStringKey("anno.filter.tradition")
    static let category          = LocalizedStringKey("anno.filter.category")
    static let confidence        = LocalizedStringKey("anno.filter.confidence")
    static let clear             = LocalizedStringKey("anno.filter.clear")
    
    // Pilgrim
    static let activeJourney     = LocalizedStringKey("anno.pilgrim.active")
    static let nextStop          = LocalizedStringKey("anno.pilgrim.nextStop")
    static let visitedStops      = LocalizedStringKey("anno.pilgrim.visited")
    static let totalDistance     = LocalizedStringKey("anno.pilgrim.distance")
    static let elapsed           = LocalizedStringKey("anno.pilgrim.elapsed")
    static let fieldNotes        = LocalizedStringKey("anno.pilgrim.fieldNotes")
    static let stamps            = LocalizedStringKey("anno.pilgrim.stamps")
    static let noStampsYet       = LocalizedStringKey("anno.pilgrim.noStampsYet")
    static let noNotesYet        = LocalizedStringKey("anno.pilgrim.noNotesYet")
    static let journeysCompleted = LocalizedStringKey("anno.pilgrim.journeysCompleted")
    static let sitesVisited      = LocalizedStringKey("anno.pilgrim.sitesVisited")
    static let allStopsVisited   = LocalizedStringKey("anno.pilgrim.allStopsVisited")
    
    // Paywall
    static let unlockAtlasTitle  = LocalizedStringKey("anno.paywall.title")
    static let unlockAtlasBody   = LocalizedStringKey("anno.paywall.body")
    static let bestValue         = LocalizedStringKey("anno.paywall.bestValue")
    static let noAdsNoAiSlop     = LocalizedStringKey("anno.paywall.noAdsNoAiSlop")
    static let sourcesOnEvery    = LocalizedStringKey("anno.paywall.sourcesOnEvery")
    static let pilgrimHero       = LocalizedStringKey("anno.paywall.pilgrimHero")
    
    // Empty / permission
    static let noLocationTitle   = LocalizedStringKey("anno.empty.noLocationTitle")
    static let noLocationBody    = LocalizedStringKey("anno.empty.noLocationBody")
    static let enableLocation    = LocalizedStringKey("anno.empty.enableLocation")
    static let browseWithoutGPS  = LocalizedStringKey("anno.empty.browseWithoutGPS")
    
    // Tiers
    static let tierFree          = LocalizedStringKey("anno.tier.freePreview")
    static let tierPremium       = LocalizedStringKey("anno.tier.premium")
    static let tierPilgrim       = LocalizedStringKey("anno.tier.pilgrimAnnual")
    
    // Units
    static func kmAway(_ km: Double) -> LocalizedStringKey {
        LocalizedStringKey("\(String(format: "%.1f", km)) km")
    }
    static func stops(_ n: Int) -> LocalizedStringKey {
        LocalizedStringKey("anno.units.stops.\(n)")
    }
}

// MARK: - Visual Theme
/// Anno visual system: dark sacred atlas with ivory parchment and gold ink accents.
enum AnnoTheme {
    // Background ink layers (obsidian family)
    static let ink        = Color(red: 0.06, green: 0.07, blue: 0.09)
    static let ink2       = Color(red: 0.10, green: 0.12, blue: 0.15)
    static let ink3       = Color(red: 0.14, green: 0.16, blue: 0.20)
    static let hairline   = Color.white.opacity(0.08)
    
    // Parchment (card surfaces, elevated content)
    static let parchment  = Color(red: 0.96, green: 0.92, blue: 0.84)
    static let parchment2 = Color(red: 0.91, green: 0.86, blue: 0.75)
    
    // Gold (primary accent — liturgical, authoritative)
    static let gold       = Color(red: 0.78, green: 0.60, blue: 0.29)
    static let goldMuted  = Color(red: 0.55, green: 0.43, blue: 0.22)
    
    // Text hierarchy
    static let textPrimary   = Color(red: 0.94, green: 0.91, blue: 0.85)
    static let textSecondary = Color.white.opacity(0.62)
    static let textTertiary  = Color.white.opacity(0.38)
    
    // Tradition colors — each faith tradition gets a distinct accent
    static let catholic   = Color(red: 0.78, green: 0.60, blue: 0.29)
    static let orthodox   = Color(red: 0.53, green: 0.40, blue: 0.68)
    static let jewish     = Color(red: 0.38, green: 0.58, blue: 0.36)
    static let islamic    = Color(red: 0.25, green: 0.51, blue: 0.53)
    static let interfaith = Color(red: 0.48, green: 0.51, blue: 0.58)
    
    // Confidence (trustworthiness of historical claims)
    static let confirmed    = Color(red: 0.36, green: 0.60, blue: 0.42)
    static let traditional  = Color(red: 0.78, green: 0.60, blue: 0.29)
    static let disputed     = Color(red: 0.72, green: 0.36, blue: 0.32)
    
    // Radii
    static let rSmall: CGFloat = 8
    static let rMed:   CGFloat = 14
    static let rLarge: CGFloat = 22
    
    // Typography — use system serif as proxy for custom font (e.g., Cormorant Garamond in production)
    static func serifTitle(_ size: CGFloat = 28) -> Font {
        .system(size: size, weight: .regular, design: .serif)
    }
    static func serifBody(_ size: CGFloat = 16) -> Font {
        .system(size: size, weight: .regular, design: .serif)
    }
    static func label(_ size: CGFloat = 12) -> Font {
        .system(size: size, weight: .medium, design: .default).smallCaps()
    }
}

// MARK: - Convenience View Modifiers
struct AnnoPanel: ViewModifier {
    var padding: CGFloat = 16
    var radius:  CGFloat = AnnoTheme.rMed
    func body(content: Content) -> some View {
        content
            .padding(padding)
            .background(AnnoTheme.ink2, in: RoundedRectangle(cornerRadius: radius, style: .continuous))
            .overlay(
                RoundedRectangle(cornerRadius: radius, style: .continuous)
                    .strokeBorder(AnnoTheme.hairline, lineWidth: 0.5)
            )
    }
}

extension View {
    func annoPanel(padding: CGFloat = 16, radius: CGFloat = AnnoTheme.rMed) -> some View {
        modifier(AnnoPanel(padding: padding, radius: radius))
    }
}

// MARK: - Domain Models

enum Tradition: String, CaseIterable, Codable, Identifiable, Hashable {
    case catholic, orthodox, jewish, islamic, interfaith
    var id: String { rawValue }
    
    var label: LocalizedStringKey {
        switch self {
        case .catholic:   return L.catholic
        case .orthodox:   return L.orthodox
        case .jewish:     return L.jewish
        case .islamic:    return L.islamic
        case .interfaith: return L.interfaith
        }
    }
    
    var tint: Color {
        switch self {
        case .catholic:   return AnnoTheme.catholic
        case .orthodox:   return AnnoTheme.orthodox
        case .jewish:     return AnnoTheme.jewish
        case .islamic:    return AnnoTheme.islamic
        case .interfaith: return AnnoTheme.interfaith
        }
    }
    
    var symbol: String {
        switch self {
        case .catholic:   return "cross.fill"
        case .orthodox:   return "cross.fill"
        case .jewish:     return "star.fill"
        case .islamic:    return "moon.stars.fill"
        case .interfaith: return "circle.hexagongrid.fill"
        }
    }
}

enum Confidence: String, CaseIterable, Codable, Hashable {
    case confirmed, traditional, disputed
    
    var label: LocalizedStringKey {
        switch self {
        case .confirmed:   return L.confirmed
        case .traditional: return L.traditional
        case .disputed:    return L.disputed
        }
    }
    
    var color: Color {
        switch self {
        case .confirmed:   return AnnoTheme.confirmed
        case .traditional: return AnnoTheme.traditional
        case .disputed:    return AnnoTheme.disputed
        }
    }
}

enum SacredCategory: String, CaseIterable, Codable, Hashable, Identifiable {
    case martyrdom, council, relic, marian, monastic, biblical, pilgrimage, basilica
    var id: String { rawValue }
    
    var label: LocalizedStringKey {
        switch self {
        case .martyrdom:  return L.catMartyrdom
        case .council:    return L.catCouncil
        case .relic:      return L.catRelic
        case .marian:     return L.catMarian
        case .monastic:   return L.catMonastic
        case .biblical:   return L.catBiblical
        case .pilgrimage: return L.catPilgrimage
        case .basilica:   return L.catBasilica
        }
    }
    
    var systemImage: String {
        switch self {
        case .martyrdom:  return "flame"
        case .council:    return "building.columns"
        case .relic:      return "shippingbox"
        case .marian:     return "rosette"
        case .monastic:   return "building.2"
        case .biblical:   return "book.closed"
        case .pilgrimage: return "figure.walk"
        case .basilica:   return "building.columns.fill"
        }
    }
}

struct SacredLocation: Identifiable, Hashable {
    let id: String
    let name: String
    let latitude: Double
    let longitude: Double
    let modernAddress: String
    let country: String
    let region: String?
    let tradition: Tradition
    let categories: [SacredCategory]
    let confidence: Confidence
    let shortWhyItMatters: String
    let visitingHours: String?
    let associatedEventIDs: [String]
    let artworkID: String?
    let sourceIDs: [String]
    let routePackIDs: [String]
    
    var coordinate: CLLocationCoordinate2D {
        .init(latitude: latitude, longitude: longitude)
    }
    
    var displayCity: String {
        [region, country].compactMap { $0 }.joined(separator: ", ")
    }
}

struct SacredEvent: Identifiable, Hashable {
    let id: String
    let date: DateComponents
    let title: String
    let narrative: String
    let tradition: Tradition
    let liturgicalColor: String?
    let locationID: String?
    let artworkID: String?
    let sourceIDs: [String]
    let confidence: Confidence
}

struct Artwork: Identifiable, Hashable {
    let id: String
    let title: String
    let artist: String
    let period: String
    let provenance: String
    let sourceCredit: String
    let systemImage: String
    let wikidata: String?
}

struct SourceCitation: Identifiable, Hashable {
    let id: String
    let title: String
    let author: String
    let url: URL?
    let reliability: Confidence
}

struct RoutePack: Identifiable, Hashable {
    let id: String
    let title: String
    let subtitle: String
    let region: String
    let stopIDs: [String]
    let estimatedKm: Double
    let estimatedHours: Double
    let traditions: [Tradition]
    let requiredTier: EntitlementTier
    let previewStopCount: Int
    let heroSymbol: String
}

extension SacredLocation {
    func distance(from coord: CLLocationCoordinate2D) -> CLLocationDistance {
        CLLocation(latitude: latitude, longitude: longitude)
            .distance(from: CLLocation(latitude: coord.latitude, longitude: coord.longitude))
    }
}

// MARK: - Entitlement Tiers
enum EntitlementTier: String, Comparable, Codable {
    case free, premium, pilgrim
    static func < (lhs: EntitlementTier, rhs: EntitlementTier) -> Bool {
        let order: [EntitlementTier] = [.free, .premium, .pilgrim]
        return order.firstIndex(of: lhs)! < order.firstIndex(of: rhs)!
    }
    
    var headerLabel: LocalizedStringKey {
        switch self {
        case .free:    return L.tierFree
        case .premium: return L.tierPremium
        case .pilgrim: return L.tierPilgrim
        }
    }
}

// MARK: - SwiftData Persistence (local-only, never leaves device)
@Model
final class JourneySession {
    @Attribute(.unique) var id: UUID
    var startedAt: Date
    var endedAt: Date?
    var routePackID: String?
    var routePackTitle: String
    var visitedStopIDs: [String]
    @Relationship(deleteRule: .cascade) var notes: [FieldNote]
    @Relationship(deleteRule: .cascade) var stamps: [PassportStamp]
    
    init(routePackID: String?, routePackTitle: String) {
        self.id = UUID()
        self.startedAt = .now
        self.endedAt = nil
        self.routePackID = routePackID
        self.routePackTitle = routePackTitle
        self.visitedStopIDs = []
        self.notes = []
        self.stamps = []
    }
    
    var isActive: Bool { endedAt == nil }
    var elapsedSeconds: TimeInterval {
        (endedAt ?? .now).timeIntervalSince(startedAt)
    }
}

@Model
final class FieldNote {
    @Attribute(.unique) var id: UUID
    var createdAt: Date
    var body: String
    var locationID: String?
    
    init(body: String, locationID: String?) {
        self.id = UUID()
        self.createdAt = .now
        self.body = body
        self.locationID = locationID
    }
}

@Model
final class PassportStamp {
    @Attribute(.unique) var id: UUID
    var visitedAt: Date
    var locationID: String
    var locationName: String
    var traditionRaw: String
    
    init(location: SacredLocation) {
        self.id = UUID()
        self.visitedAt = .now
        self.locationID = location.id
        self.locationName = location.name
        self.traditionRaw = location.tradition.rawValue
    }
    
    var tradition: Tradition { Tradition(rawValue: traditionRaw) ?? .catholic }
}

// MARK: - Repository Protocol + Mock Implementation
protocol SacredRepository {
    var locations: [SacredLocation] { get }
    var events: [SacredEvent] { get }
    var artworks: [Artwork] { get }
    var sources: [SourceCitation] { get }
    var routePacks: [RoutePack] { get }
    
    func location(id: String) -> SacredLocation?
    func events(for locationID: String) -> [SacredEvent]
    func artwork(id: String?) -> Artwork?
    func sources(ids: [String]) -> [SourceCitation]
    func routePack(id: String) -> RoutePack?
    func stops(for pack: RoutePack) -> [SacredLocation]
    func todaysEvents(on date: Date) -> [SacredEvent]
}

final class MockSacredRepository: SacredRepository {
    static let shared = MockSacredRepository()
    
    let locations: [SacredLocation]
    let events: [SacredEvent]
    let artworks: [Artwork]
    let sources: [SourceCitation]
    let routePacks: [RoutePack]
    
    private init() {
        // Artwork fixtures
        artworks = [
            .init(id: "art.holbein.more", title: "Sir Thomas More", artist: "Hans Holbein the Younger",
                  period: "1527", provenance: "Frick Collection, New York",
                  sourceCredit: "Frick Collection", systemImage: "person.crop.rectangle",
                  wikidata: "Q1050093"),
            .init(id: "art.caravaggio.peter", title: "Crucifixion of St. Peter", artist: "Caravaggio",
                  period: "1601", provenance: "Santa Maria del Popolo, Rome",
                  sourceCredit: "Wikimedia", systemImage: "photo.artframe",
                  wikidata: "Q670230"),
            .init(id: "art.giotto.francis", title: "St. Francis Preaching to the Birds", artist: "Giotto",
                  period: "c.1299", provenance: "Basilica of Saint Francis, Assisi",
                  sourceCredit: "Wikimedia", systemImage: "photo.artframe", wikidata: nil),
        ]
        
        // Source fixtures
        sources = [
            .init(id: "src.foxe", title: "The Acts of the Martyrs", author: "John Foxe",
                  url: URL(string: "https://example.org/foxe"), reliability: .traditional),
            .init(id: "src.yale", title: "Letters of St. Thomas More", author: "Yale University Press",
                  url: URL(string: "https://example.org/more"), reliability: .confirmed),
            .init(id: "src.cathencyc", title: "Catholic Encyclopedia",
                  author: "Robert Appleton Company",
                  url: URL(string: "https://example.org/cathenc"), reliability: .confirmed),
            .init(id: "src.dnb", title: "Dictionary of National Biography",
                  author: "Oxford University Press",
                  url: URL(string: "https://example.org/dnb"), reliability: .confirmed),
            .init(id: "src.eusebius", title: "Ecclesiastical History", author: "Eusebius of Caesarea",
                  url: nil, reliability: .traditional),
            .init(id: "src.disputed.mamertine", title: "Peter at Mamertine — Historiographical Note",
                  author: "Various", url: nil, reliability: .disputed),
        ]
        
        // Location fixtures (~18 curated sites across traditions and regions)
        locations = [
            .init(id: "loc.mamertine", name: "Mamertine Prison",
                  latitude: 41.8931, longitude: 12.4842,
                  modernAddress: "Clivo Argentario, 1, Rome",
                  country: "Italy", region: "Rome",
                  tradition: .catholic, categories: [.martyrdom, .relic],
                  confidence: .traditional,
                  shortWhyItMatters: "According to tradition, Sts. Peter and Paul were held here before their martyrdoms in the mid-first century.",
                  visitingHours: "9:00–17:00",
                  associatedEventIDs: ["evt.peterpaul.mamertine"],
                  artworkID: "art.caravaggio.peter",
                  sourceIDs: ["src.eusebius", "src.disputed.mamertine"],
                  routePackIDs: ["route.romeSeven"]),
            
            .init(id: "loc.stpeters", name: "St. Peter's Basilica",
                  latitude: 41.9022, longitude: 12.4539,
                  modernAddress: "Piazza San Pietro, Vatican City",
                  country: "Vatican", region: "Rome",
                  tradition: .catholic, categories: [.basilica, .relic, .pilgrimage],
                  confidence: .confirmed,
                  shortWhyItMatters: "Built over the traditional burial site of St. Peter; papal basilica and center of Western Christendom.",
                  visitingHours: "7:00–19:00",
                  associatedEventIDs: [], artworkID: nil,
                  sourceIDs: ["src.cathencyc"],
                  routePackIDs: ["route.romeSeven"]),
            
            .init(id: "loc.stpaul.walls", name: "St. Paul Outside the Walls",
                  latitude: 41.8586, longitude: 12.4770,
                  modernAddress: "Piazzale San Paolo, 1, Rome",
                  country: "Italy", region: "Rome",
                  tradition: .catholic, categories: [.basilica, .relic],
                  confidence: .confirmed,
                  shortWhyItMatters: "One of the four papal basilicas; built over the tomb of St. Paul the Apostle.",
                  visitingHours: "7:00–18:30",
                  associatedEventIDs: [], artworkID: nil,
                  sourceIDs: ["src.cathencyc"], routePackIDs: ["route.romeSeven"]),
            
            .init(id: "loc.assisi", name: "Basilica of Saint Francis of Assisi",
                  latitude: 43.0748, longitude: 12.6058,
                  modernAddress: "Piazza Inferiore di S. Francesco, 2, Assisi",
                  country: "Italy", region: "Umbria",
                  tradition: .catholic, categories: [.monastic, .pilgrimage],
                  confidence: .confirmed,
                  shortWhyItMatters: "Mother church of the Franciscan Order; burial site of St. Francis. UNESCO World Heritage.",
                  visitingHours: "6:00–19:00",
                  associatedEventIDs: ["evt.assisi.francis.death"],
                  artworkID: "art.giotto.francis",
                  sourceIDs: ["src.cathencyc"], routePackIDs: []),
            
            .init(id: "loc.holysep", name: "Church of the Holy Sepulchre",
                  latitude: 31.7784, longitude: 35.2298,
                  modernAddress: "Christian Quarter, Old City, Jerusalem",
                  country: "Israel/Palestine", region: "Jerusalem",
                  tradition: .interfaith, categories: [.biblical, .pilgrimage, .relic],
                  confidence: .traditional,
                  shortWhyItMatters: "Traditional site of the Crucifixion and Resurrection; shared custody among Christian communities.",
                  visitingHours: "5:00–21:00",
                  associatedEventIDs: [], artworkID: nil, sourceIDs: ["src.eusebius"],
                  routePackIDs: ["route.passionWalk"]),
            
            .init(id: "loc.viadolorosa", name: "Via Dolorosa · Station I",
                  latitude: 31.7802, longitude: 35.2358,
                  modernAddress: "Muslim Quarter, Old City, Jerusalem",
                  country: "Israel/Palestine", region: "Jerusalem",
                  tradition: .catholic, categories: [.biblical, .pilgrimage],
                  confidence: .traditional,
                  shortWhyItMatters: "Traditional starting station of the Way of the Cross.",
                  visitingHours: nil, associatedEventIDs: [], artworkID: nil,
                  sourceIDs: [], routePackIDs: ["route.passionWalk"]),
            
            .init(id: "loc.bethlehem", name: "Church of the Nativity",
                  latitude: 31.7042, longitude: 35.2076,
                  modernAddress: "Manger Square, Bethlehem",
                  country: "Palestine", region: "Bethlehem",
                  tradition: .interfaith, categories: [.biblical, .pilgrimage],
                  confidence: .traditional,
                  shortWhyItMatters: "Built over the grotto traditionally identified as the birthplace of Jesus.",
                  visitingHours: "6:30–17:30",
                  associatedEventIDs: [], artworkID: nil, sourceIDs: [], routePackIDs: []),
            
            .init(id: "loc.sinai", name: "Saint Catherine's Monastery",
                  latitude: 28.5560, longitude: 33.9764,
                  modernAddress: "Mount Sinai, South Sinai",
                  country: "Egypt", region: "Sinai",
                  tradition: .orthodox, categories: [.monastic, .biblical, .relic],
                  confidence: .confirmed,
                  shortWhyItMatters: "Oldest continually inhabited Christian monastery. Traditional site of the Burning Bush.",
                  visitingHours: "9:00–12:00",
                  associatedEventIDs: [], artworkID: nil, sourceIDs: [],
                  routePackIDs: ["route.desertFathers"]),
            
            .init(id: "loc.athos", name: "Great Lavra, Mount Athos",
                  latitude: 40.1707, longitude: 24.3211,
                  modernAddress: "Karyes, Mount Athos",
                  country: "Greece", region: "Mount Athos",
                  tradition: .orthodox, categories: [.monastic],
                  confidence: .confirmed,
                  shortWhyItMatters: "First and largest of the ruling monasteries of the Athonite peninsula. Founded 963 AD.",
                  visitingHours: nil, associatedEventIDs: [], artworkID: nil,
                  sourceIDs: [], routePackIDs: []),
            
            .init(id: "loc.constantinople", name: "Hagia Sophia",
                  latitude: 41.0086, longitude: 28.9802,
                  modernAddress: "Sultan Ahmet, Fatih, İstanbul",
                  country: "Turkey", region: "Constantinople",
                  tradition: .orthodox, categories: [.council, .basilica],
                  confidence: .confirmed,
                  shortWhyItMatters: "Great Church of Constantinople from 537. Site of the definitive break of 1054.",
                  visitingHours: "9:00–19:00",
                  associatedEventIDs: [], artworkID: nil, sourceIDs: [],
                  routePackIDs: ["route.councils"]),
            
            .init(id: "loc.nicaea", name: "Nicaea (İznik)",
                  latitude: 40.4297, longitude: 29.7181,
                  modernAddress: "İznik, Bursa",
                  country: "Turkey", region: "Bithynia",
                  tradition: .interfaith, categories: [.council],
                  confidence: .confirmed,
                  shortWhyItMatters: "Site of the First (325) and Seventh (787) Ecumenical Councils.",
                  visitingHours: nil, associatedEventIDs: [], artworkID: nil,
                  sourceIDs: [], routePackIDs: ["route.councils"]),
            
            .init(id: "loc.santiago", name: "Cathedral of Santiago de Compostela",
                  latitude: 42.8806, longitude: -8.5449,
                  modernAddress: "Praza do Obradoiro, s/n, Santiago",
                  country: "Spain", region: "Galicia",
                  tradition: .catholic, categories: [.pilgrimage, .relic, .basilica],
                  confidence: .traditional,
                  shortWhyItMatters: "Traditional resting place of the Apostle James. Terminus of the Camino.",
                  visitingHours: "7:00–20:30",
                  associatedEventIDs: [], artworkID: nil, sourceIDs: [],
                  routePackIDs: ["route.camino"]),
            
            .init(id: "loc.canterbury", name: "Canterbury Cathedral",
                  latitude: 51.2798, longitude: 1.0830,
                  modernAddress: "Cathedral House, Canterbury",
                  country: "United Kingdom", region: "Kent",
                  tradition: .catholic, categories: [.martyrdom, .pilgrimage, .basilica],
                  confidence: .confirmed,
                  shortWhyItMatters: "Site of the martyrdom of St. Thomas Becket in 1170. Chaucer's destination.",
                  visitingHours: "9:00–17:00",
                  associatedEventIDs: [], artworkID: nil, sourceIDs: [],
                  routePackIDs: ["route.londonSaints"]),
            
            .init(id: "loc.towerhill", name: "Tower Hill",
                  latitude: 51.5090, longitude: -0.0760,
                  modernAddress: "Tower Hill, London",
                  country: "United Kingdom", region: "London",
                  tradition: .catholic, categories: [.martyrdom],
                  confidence: .confirmed,
                  shortWhyItMatters: "Site of the martyrdom of St. Thomas More, 6 July 1535.",
                  visitingHours: nil,
                  associatedEventIDs: ["evt.more.martyrdom"],
                  artworkID: "art.holbein.more",
                  sourceIDs: ["src.foxe", "src.yale", "src.dnb"],
                  routePackIDs: ["route.londonSaints"]),
            
            .init(id: "loc.lourdes", name: "Sanctuary of Our Lady of Lourdes",
                  latitude: 43.0977, longitude: -0.0562,
                  modernAddress: "1 Av. Mgr Théas, Lourdes",
                  country: "France", region: "Occitanie",
                  tradition: .catholic, categories: [.marian, .pilgrimage],
                  confidence: .confirmed,
                  shortWhyItMatters: "Site of the 1858 Marian apparitions to St. Bernadette Soubirous.",
                  visitingHours: "5:00–24:00",
                  associatedEventIDs: [], artworkID: nil, sourceIDs: [],
                  routePackIDs: ["route.marian"]),
            
            .init(id: "loc.fatima", name: "Sanctuary of Fátima",
                  latitude: 39.6316, longitude: -8.6725,
                  modernAddress: "Fátima, Ourém",
                  country: "Portugal", region: "Santarém",
                  tradition: .catholic, categories: [.marian, .pilgrimage],
                  confidence: .confirmed,
                  shortWhyItMatters: "Site of the 1917 Marian apparitions to three shepherd children.",
                  visitingHours: "6:00–23:00",
                  associatedEventIDs: [], artworkID: nil, sourceIDs: [],
                  routePackIDs: ["route.marian"]),
            
            .init(id: "loc.hebron", name: "Cave of the Patriarchs",
                  latitude: 31.5246, longitude: 35.1108,
                  modernAddress: "Hebron",
                  country: "Palestine", region: "West Bank",
                  tradition: .interfaith, categories: [.biblical, .pilgrimage],
                  confidence: .traditional,
                  shortWhyItMatters: "Traditional burial site of Abraham, Isaac, Jacob, Sarah, Rebekah, and Leah.",
                  visitingHours: nil, associatedEventIDs: [], artworkID: nil,
                  sourceIDs: [], routePackIDs: []),
            
            .init(id: "loc.tiberias", name: "Sea of Galilee — Tabgha",
                  latitude: 32.8722, longitude: 35.5478,
                  modernAddress: "Tabgha, north shore of the Sea of Galilee",
                  country: "Israel", region: "Galilee",
                  tradition: .catholic, categories: [.biblical, .pilgrimage],
                  confidence: .traditional,
                  shortWhyItMatters: "Traditional site of the Multiplication of the Loaves and Fishes.",
                  visitingHours: "8:00–17:00",
                  associatedEventIDs: [], artworkID: nil, sourceIDs: [], routePackIDs: []),
        ]
        
        // Event fixtures
        events = [
            .init(id: "evt.more.martyrdom",
                  date: DateComponents(year: 1535, month: 7, day: 6),
                  title: "Martyrdom of St. Thomas More",
                  narrative: "Beheaded on Tower Hill for refusing the Oath of Supremacy.",
                  tradition: .catholic, liturgicalColor: "Red",
                  locationID: "loc.towerhill", artworkID: "art.holbein.more",
                  sourceIDs: ["src.foxe", "src.yale", "src.dnb"],
                  confidence: .confirmed),
            .init(id: "evt.peterpaul.mamertine",
                  date: DateComponents(year: 67, month: 6, day: 29),
                  title: "Martyrdom of Sts. Peter and Paul",
                  narrative: "Traditional date of the martyrdoms in Rome under Nero.",
                  tradition: .catholic, liturgicalColor: "Red",
                  locationID: "loc.mamertine", artworkID: "art.caravaggio.peter",
                  sourceIDs: ["src.eusebius"], confidence: .traditional),
            .init(id: "evt.assisi.francis.death",
                  date: DateComponents(year: 1226, month: 10, day: 3),
                  title: "Transitus of St. Francis of Assisi",
                  narrative: "The Poverello's passing at the Porziuncola.",
                  tradition: .catholic, liturgicalColor: "White",
                  locationID: "loc.assisi", artworkID: "art.giotto.francis",
                  sourceIDs: ["src.cathencyc"], confidence: .confirmed),
        ]
        
        // Route packs
        routePacks = [
            .init(id: "route.romeSeven",
                  title: "Seven Churches of Rome",
                  subtitle: "The classic Roman pilgrimage set by St. Philip Neri in the 16th century.",
                  region: "Rome, Italy",
                  stopIDs: ["loc.stpeters", "loc.stpaul.walls", "loc.mamertine"],
                  estimatedKm: 19.0, estimatedHours: 6.5,
                  traditions: [.catholic],
                  requiredTier: .premium, previewStopCount: 1,
                  heroSymbol: "building.columns.fill"),
            .init(id: "route.passionWalk",
                  title: "Jerusalem · Passion Walk",
                  subtitle: "The Via Dolorosa from Antonia Fortress to the Holy Sepulchre.",
                  region: "Jerusalem",
                  stopIDs: ["loc.viadolorosa", "loc.holysep"],
                  estimatedKm: 0.6, estimatedHours: 1.5,
                  traditions: [.catholic, .interfaith],
                  requiredTier: .premium, previewStopCount: 1,
                  heroSymbol: "figure.walk"),
            .init(id: "route.londonSaints",
                  title: "Saints of London",
                  subtitle: "From Tower Hill to Tyburn — English recusant memory.",
                  region: "London, England",
                  stopIDs: ["loc.towerhill", "loc.canterbury"],
                  estimatedKm: 3.2, estimatedHours: 2.0,
                  traditions: [.catholic],
                  requiredTier: .pilgrim, previewStopCount: 1,
                  heroSymbol: "crown"),
            .init(id: "route.camino",
                  title: "Camino · Sacred Stops",
                  subtitle: "Curated stops along the French Way to Santiago.",
                  region: "Spain",
                  stopIDs: ["loc.santiago"],
                  estimatedKm: 780.0, estimatedHours: 168,
                  traditions: [.catholic],
                  requiredTier: .pilgrim, previewStopCount: 1,
                  heroSymbol: "shell"),
            .init(id: "route.marian",
                  title: "Marian Apparitions of Europe",
                  subtitle: "Lourdes, Fátima, and the great Marian shrines.",
                  region: "Europe",
                  stopIDs: ["loc.lourdes", "loc.fatima"],
                  estimatedKm: 1120.0, estimatedHours: 24,
                  traditions: [.catholic],
                  requiredTier: .premium, previewStopCount: 1,
                  heroSymbol: "rosette"),
            .init(id: "route.desertFathers",
                  title: "Desert Fathers of Egypt",
                  subtitle: "Monastic cradle of Christianity — Sinai and the Wadi Natrun.",
                  region: "Egypt",
                  stopIDs: ["loc.sinai"],
                  estimatedKm: 480.0, estimatedHours: 20,
                  traditions: [.orthodox, .catholic],
                  requiredTier: .pilgrim, previewStopCount: 1,
                  heroSymbol: "sun.max"),
            .init(id: "route.councils",
                  title: "Constantinople & the Councils",
                  subtitle: "Nicaea, Constantinople, Chalcedon — where doctrine was set.",
                  region: "Turkey",
                  stopIDs: ["loc.constantinople", "loc.nicaea"],
                  estimatedKm: 130.0, estimatedHours: 6,
                  traditions: [.orthodox, .catholic],
                  requiredTier: .premium, previewStopCount: 1,
                  heroSymbol: "building.columns"),
        ]
    }
    
    func location(id: String) -> SacredLocation? { locations.first { $0.id == id } }
    func events(for locationID: String) -> [SacredEvent] {
        events.filter { $0.locationID == locationID }
    }
    func artwork(id: String?) -> Artwork? {
        guard let id else { return nil }
        return artworks.first { $0.id == id }
    }
    func sources(ids: [String]) -> [SourceCitation] {
        sources.filter { ids.contains($0.id) }
    }
    func routePack(id: String) -> RoutePack? { routePacks.first { $0.id == id } }
    func stops(for pack: RoutePack) -> [SacredLocation] {
        pack.stopIDs.compactMap { location(id: $0) }
    }
    func todaysEvents(on date: Date) -> [SacredEvent] {
        let comps = Calendar(identifier: .gregorian).dateComponents([.month, .day], from: date)
        return events.filter { $0.date.month == comps.month && $0.date.day == comps.day }
    }
}

// MARK: - Services

@Observable
final class EntitlementService {
    var tier: EntitlementTier
    
    init(tier: EntitlementTier = .free) { self.tier = tier }
    
    func has(_ required: EntitlementTier) -> Bool { tier >= required }
    
    var canBrowseFullAtlas: Bool     { has(.premium) }
    var canReadFullDossier: Bool     { has(.premium) }
    var canUseConfidenceLayer: Bool  { has(.premium) }
    var canStartPilgrimage: Bool     { has(.pilgrim) }
    var canDownloadOffline: Bool     { has(.pilgrim) }
    var canExportPassport: Bool      { has(.pilgrim) }
    var maxFreePins: Int             { 3 }
}

@Observable
final class LocationService: NSObject, CLLocationManagerDelegate {
    enum Authorization { case unknown, denied, authorized }
    
    var authorization: Authorization = .unknown
    var currentCoordinate: CLLocationCoordinate2D?
    var isSimulating: Bool = false
    
    private let manager = CLLocationManager()
    private var simulationTimer: Timer?
    
    let browseFallback = CLLocationCoordinate2D(latitude: 41.9028, longitude: 12.4964)
    
    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyHundredMeters
        applyStatus(manager.authorizationStatus)
    }
    
    var effectiveCoordinate: CLLocationCoordinate2D {
        currentCoordinate ?? browseFallback
    }
    
    func requestWhenInUse() { manager.requestWhenInUseAuthorization() }
    func startUpdates() {
        guard authorization == .authorized else { return }
        manager.startUpdatingLocation()
    }
    func stopUpdates() { manager.stopUpdatingLocation() }
    
    func startSimulating(alongRoute stops: [SacredLocation]) {
        stopSimulating()
        guard !stops.isEmpty else { return }
        isSimulating = true
        var index = 0
        currentCoordinate = stops[0].coordinate
        simulationTimer = Timer.scheduledTimer(withTimeInterval: 3.0, repeats: true) { [weak self] _ in
            guard let self else { return }
            index = (index + 1) % stops.count
            currentCoordinate = stops[index].coordinate
        }
    }
    
    func stopSimulating() {
        simulationTimer?.invalidate()
        simulationTimer = nil
        isSimulating = false
    }
    
    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        applyStatus(manager.authorizationStatus)
    }
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        currentCoordinate = locations.last?.coordinate
    }
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) { }
    
    private func applyStatus(_ status: CLAuthorizationStatus) {
        switch status {
        case .notDetermined:                  authorization = .unknown
        case .restricted, .denied:            authorization = .denied
        case .authorizedAlways, .authorizedWhenInUse: authorization = .authorized
        @unknown default:                     authorization = .unknown
        }
    }
}

// MARK: - Atlas ViewModel
@Observable
final class SacredAtlasViewModel {
    let repo: SacredRepository
    let entitlements: EntitlementService
    let location: LocationService
    
    var selectedTraditions: Set<Tradition> = []
    var selectedCategories: Set<SacredCategory> = []
    var selectedConfidence: Set<Confidence> = []
    var showTodayOnly: Bool = false
    
    var cameraPosition: MapCameraPosition
    var selectedLocationID: String?
    var isNearbyOpen: Bool = false
    var isFiltersOpen: Bool = false
    var isRoutesOpen: Bool = false
    var isPassportOpen: Bool = false
    var isPaywallOpen: Bool = false
    
    var savedLocationIDs: Set<String> = []
    
    init(repo: SacredRepository, entitlements: EntitlementService, location: LocationService) {
        self.repo = repo
        self.entitlements = entitlements
        self.location = location
        self.cameraPosition = .region(MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: 41.9028, longitude: 12.4964),
            span: MKCoordinateSpan(latitudeDelta: 24, longitudeDelta: 24)
        ))
    }
    
    var filteredLocations: [SacredLocation] {
        var xs = repo.locations
        if !selectedTraditions.isEmpty {
            xs = xs.filter { selectedTraditions.contains($0.tradition) }
        }
        if !selectedCategories.isEmpty {
            xs = xs.filter { !Set($0.categories).isDisjoint(with: selectedCategories) }
        }
        if !selectedConfidence.isEmpty {
            xs = xs.filter { selectedConfidence.contains($0.confidence) }
        }
        if showTodayOnly {
            let todayLocIDs = Set(repo.todaysEvents(on: .now).compactMap(\.locationID))
            xs = xs.filter { todayLocIDs.contains($0.id) }
        }
        return xs
    }
    
    var visibleLocations: [SacredLocation] {
        if entitlements.canBrowseFullAtlas { return filteredLocations }
        return Array(filteredLocations.prefix(entitlements.maxFreePins))
    }
    
    var lockedLocations: [SacredLocation] {
        if entitlements.canBrowseFullAtlas { return [] }
        return Array(filteredLocations.dropFirst(entitlements.maxFreePins))
    }
    
    func nearby(limit: Int = 5) -> [(SacredLocation, CLLocationDistance)] {
        let coord = location.effectiveCoordinate
        let ranked = filteredLocations
            .map { ($0, $0.distance(from: coord)) }
            .sorted { $0.1 < $1.1 }
        let cap = entitlements.canBrowseFullAtlas ? limit : min(limit, 2)
        return Array(ranked.prefix(cap))
    }
    
    func nearbyCountSummary() -> (total: Int, today: Int, traditional: Int, disputed: Int) {
        let coord = location.effectiveCoordinate
        let within = repo.locations.filter { $0.distance(from: coord) < 400_000 }
        let todayIDs = Set(repo.todaysEvents(on: .now).compactMap(\.locationID))
        let today = within.filter { todayIDs.contains($0.id) }.count
        let traditional = within.filter { $0.confidence == .traditional }.count
        let disputed    = within.filter { $0.confidence == .disputed }.count
        return (within.count, today, traditional, disputed)
    }
    
    func select(_ location: SacredLocation) {
        selectedLocationID = location.id
        withAnimation(.easeInOut(duration: 0.3)) {
            cameraPosition = .region(MKCoordinateRegion(
                center: location.coordinate,
                span: MKCoordinateSpan(latitudeDelta: 0.15, longitudeDelta: 0.15)))
        }
    }
    
    func deselect() { selectedLocationID = nil }
    
    func toggleSaved(_ location: SacredLocation) {
        if savedLocationIDs.contains(location.id) { savedLocationIDs.remove(location.id) }
        else { savedLocationIDs.insert(location.id) }
    }
    
    func isSaved(_ location: SacredLocation) -> Bool {
        savedLocationIDs.contains(location.id)
    }
    
    func attemptOpen(_ location: SacredLocation) -> Bool {
        if entitlements.canBrowseFullAtlas { return true }
        if visibleLocations.contains(where: { $0.id == location.id }) {
            return true
        }
        isPaywallOpen = true
        return false
    }
    
    func toggle(tradition: Tradition) {
        if selectedTraditions.contains(tradition) { selectedTraditions.remove(tradition) }
        else { selectedTraditions.insert(tradition) }
    }
    
    func toggle(category: SacredCategory) {
        if selectedCategories.contains(category) { selectedCategories.remove(category) }
        else { selectedCategories.insert(category) }
    }
    
    func toggle(confidence: Confidence) {
        guard entitlements.canUseConfidenceLayer else { isPaywallOpen = true; return }
        if selectedConfidence.contains(confidence) { selectedConfidence.remove(confidence) }
        else { selectedConfidence.insert(confidence) }
    }
    
    func clearFilters() {
        selectedTraditions.removeAll()
        selectedCategories.removeAll()
        selectedConfidence.removeAll()
        showTodayOnly = false
    }
}

// MARK: - Journey ViewModel
@Observable
final class PilgrimJourneyViewModel {
    let repo: SacredRepository
    let entitlements: EntitlementService
    let location: LocationService
    
    var currentSession: JourneySession?
    var currentPack: RoutePack?
    var modelContext: ModelContext?
    
    init(repo: SacredRepository, entitlements: EntitlementService, location: LocationService) {
        self.repo = repo
        self.entitlements = entitlements
        self.location = location
    }
    
    func startJourney(pack: RoutePack) {
        guard entitlements.canStartPilgrimage else { return }
        let session = JourneySession(routePackID: pack.id, routePackTitle: pack.title)
        currentSession = session
        currentPack = pack
        modelContext?.insert(session)
        try? modelContext?.save()
        
        let stops = repo.stops(for: pack)
        location.startSimulating(alongRoute: stops)
    }
    
    func endJourney() {
        currentSession?.endedAt = .now
        try? modelContext?.save()
        location.stopSimulating()
        currentSession = nil
        currentPack = nil
    }
    
    var stops: [SacredLocation] {
        guard let pack = currentPack else { return [] }
        return repo.stops(for: pack)
    }
    
    var visitedCount: Int { currentSession?.visitedStopIDs.count ?? 0 }
    
    var nextStop: SacredLocation? {
        guard let session = currentSession else { return nil }
        return stops.first { !session.visitedStopIDs.contains($0.id) }
    }
    
    func isVisited(_ loc: SacredLocation) -> Bool {
        currentSession?.visitedStopIDs.contains(loc.id) ?? false
    }
    
    func markVisited(_ loc: SacredLocation) {
        guard let session = currentSession, !session.visitedStopIDs.contains(loc.id) else { return }
        session.visitedStopIDs.append(loc.id)
        session.stamps.append(PassportStamp(location: loc))
        try? modelContext?.save()
    }
    
    func addNote(_ text: String, at loc: SacredLocation?) {
        guard let session = currentSession, !text.isEmpty else { return }
        session.notes.append(FieldNote(body: text, locationID: loc?.id))
        try? modelContext?.save()
    }
    
    var totalRouteKm: Double { currentPack?.estimatedKm ?? 0 }
    
    var elapsedString: String {
        guard let s = currentSession else { return "—" }
        let secs = Int(s.elapsedSeconds)
        let h = secs / 3600, m = (secs % 3600) / 60
        return String(format: "%d:%02d", h, m)
    }
    
    var progressFraction: Double {
        guard !stops.isEmpty else { return 0 }
        return Double(visitedCount) / Double(stops.count)
    }
}

// MARK: - Public Entry Point
public struct AnnoMapFeature: View {
    @State private var entitlements: EntitlementService
    @State private var locationSvc:  LocationService
    @State private var atlas:        SacredAtlasViewModel
    @State private var journey:      PilgrimJourneyViewModel
    
    public init(tier: EntitlementTier = .free) {
        let ent = EntitlementService(tier: tier)
        let loc = LocationService()
        let repo = MockSacredRepository.shared
        _entitlements = State(initialValue: ent)
        _locationSvc  = State(initialValue: loc)
        _atlas        = State(initialValue: .init(repo: repo, entitlements: ent, location: loc))
        _journey      = State(initialValue: .init(repo: repo, entitlements: ent, location: loc))
    }
    
    public var body: some View {
        SacredAtlasMapView()
            .environment(atlas)
            .environment(journey)
            .environment(entitlements)
            .environment(locationSvc)
            .modelContainer(for: [JourneySession.self, PassportStamp.self, FieldNote.self])
            .preferredColorScheme(.dark)
    }
}

// MARK: - Main Map Surface
struct SacredAtlasMapView: View {
    @Environment(SacredAtlasViewModel.self)   private var vm
    @Environment(PilgrimJourneyViewModel.self) private var journey
    @Environment(EntitlementService.self)     private var entitlements
    @Environment(LocationService.self)        private var location
    @Environment(\.modelContext)              private var modelContext
    
    var body: some View {
        @Bindable var vmb = vm
        
        ZStack(alignment: .top) {
            mapLayer.ignoresSafeArea()
            
            VStack(spacing: 12) {
                topBar
                LayerFilterBar()
                if journey.currentSession != nil {
                    ActiveJourneyBanner()
                        .transition(.move(edge: .top).combined(with: .opacity))
                }
                Spacer()
            }
            .padding(.top, 8)
            
            VStack {
                Spacer()
                NearbyPeekBar()
                    .padding(.horizontal)
                    .padding(.bottom, 8)
            }
        }
        .sheet(isPresented: $vmb.isNearbyOpen) {
            NearbyInSacredHistoryView()
                .presentationDetents([.medium, .large])
                .presentationBackground(AnnoTheme.ink)
        }
        .sheet(isPresented: $vmb.isFiltersOpen) {
            LayerFiltersSheet()
                .presentationDetents([.medium])
                .presentationBackground(AnnoTheme.ink)
        }
        .sheet(isPresented: $vmb.isRoutesOpen) {
            RoutePacksView()
                .presentationDetents([.large])
                .presentationBackground(AnnoTheme.ink)
        }
        .sheet(isPresented: $vmb.isPassportOpen) {
            PilgrimPassportView()
                .presentationDetents([.medium, .large])
                .presentationBackground(AnnoTheme.ink)
        }
        .sheet(isPresented: $vmb.isPaywallOpen) {
            PaywallSheet()
                .presentationDetents([.medium, .large])
                .presentationBackground(AnnoTheme.ink)
        }
        .sheet(item: Binding(
            get: { vm.selectedLocationID.flatMap { vm.repo.location(id: $0) } },
            set: { if $0 == nil { vm.deselect() } }
        )) { loc in
            LocationDetailSheet(location: loc)
                .presentationDetents([.medium, .large])
                .presentationBackground(AnnoTheme.ink)
        }
        .onAppear {
            if journey.modelContext == nil {
                journey.modelContext = modelContext
            }
        }
        .background(AnnoTheme.ink)
    }
    
    @ViewBuilder
    private var mapLayer: some View {
        @Bindable var vmb = vm
        Map(position: $vmb.cameraPosition, selection: $vmb.selectedLocationID) {
            ForEach(vm.visibleLocations) { loc in
                Annotation(loc.name, coordinate: loc.coordinate, anchor: .bottom) {
                    SacredPinView(
                        tradition: loc.tradition,
                        category: loc.categories.first,
                        selected: vm.selectedLocationID == loc.id,
                        locked: false,
                        visited: journey.isVisited(loc)
                    )
                    .onTapGesture { vm.select(loc) }
                }
                .tag(loc.id as String?)
            }
            ForEach(vm.lockedLocations) { loc in
                Annotation(loc.name, coordinate: loc.coordinate, anchor: .bottom) {
                    SacredPinView(
                        tradition: loc.tradition,
                        category: loc.categories.first,
                        selected: false, locked: true, visited: false
                    )
                    .onTapGesture { vm.isPaywallOpen = true }
                }
            }
            if journey.currentSession != nil, journey.stops.count > 1 {
                MapPolyline(coordinates: journey.stops.map(\.coordinate))
                    .stroke(AnnoTheme.gold.opacity(0.9),
                            style: StrokeStyle(lineWidth: 3, dash: [6, 8]))
            }
            if let user = location.currentCoordinate {
                Annotation("", coordinate: user, anchor: .center) {
                    UserDotView()
                }
            }
        }
        .mapStyle(.standard(elevation: .realistic,
                            emphasis: .muted,
                            pointsOfInterest: .excluding(.all)))
        .mapControls {
            MapCompass()
            MapScaleView()
        }
        .tint(AnnoTheme.gold)
    }
    
    private var topBar: some View {
        HStack(spacing: 10) {
            VStack(alignment: .leading, spacing: 2) {
                Text(L.sacredAtlas)
                    .font(AnnoTheme.serifTitle(22))
                    .foregroundStyle(AnnoTheme.textPrimary)
                Text(entitlements.tier.headerLabel)
                    .font(AnnoTheme.label())
                    .foregroundStyle(AnnoTheme.gold)
            }
            Spacer()
            TopIconButton(system: "line.3.horizontal.decrease") { vm.isFiltersOpen = true }
            TopIconButton(system: "map.circle") { vm.isRoutesOpen = true }
            TopIconButton(system: "seal") { vm.isPassportOpen = true }
        }
        .padding(.horizontal)
        .padding(.vertical, 8)
        .background(.ultraThinMaterial, in: Capsule())
        .overlay(Capsule().strokeBorder(AnnoTheme.hairline, lineWidth: 0.5))
        .padding(.horizontal)
    }
}

// MARK: - Sacred Pin (Teardrop Shape)
struct SacredPinView: View {
    let tradition: Tradition
    let category: SacredCategory?
    let selected: Bool
    let locked: Bool
    let visited: Bool
    
    var body: some View {
        ZStack {
            TeardropShape()
                .fill(tradition.tint.opacity(locked ? 0.35 : 1.0))
                .overlay(
                    TeardropShape()
                        .stroke(selected ? AnnoTheme.parchment : Color.black.opacity(0.3),
                                lineWidth: selected ? 1.5 : 0.5)
                )
                .frame(width: selected ? 34 : 28, height: selected ? 44 : 36)
                .shadow(color: .black.opacity(0.35), radius: 3, y: 2)
            
            Image(systemName: locked ? "lock.fill" : tradition.symbol)
                .font(.system(size: selected ? 13 : 11, weight: .semibold))
                .foregroundStyle(.white)
                .offset(y: -4)
            
            if visited {
                Image(systemName: "checkmark.seal.fill")
                    .font(.system(size: 12))
                    .foregroundStyle(AnnoTheme.gold)
                    .background(Circle().fill(AnnoTheme.ink).frame(width: 14, height: 14))
                    .offset(x: 12, y: -14)
            }
        }
        .animation(.spring(duration: 0.25), value: selected)
        .accessibilityLabel(Text(tradition.label))
    }
}

private struct TeardropShape: Shape {
    func path(in rect: CGRect) -> Path {
        var p = Path()
        let w = rect.width, h = rect.height
        let r = w / 2
        p.addArc(center: CGPoint(x: r, y: r), radius: r,
                 startAngle: .degrees(180), endAngle: .degrees(0), clockwise: false)
        p.addLine(to: CGPoint(x: w, y: r))
        p.addQuadCurve(to: CGPoint(x: r, y: h), control: CGPoint(x: w * 0.85, y: h * 0.75))
        p.addQuadCurve(to: CGPoint(x: 0, y: r), control: CGPoint(x: w * 0.15, y: h * 0.75))
        p.closeSubpath()
        return p
    }
}

private struct UserDotView: View {
    var body: some View {
        ZStack {
            Circle().fill(AnnoTheme.gold.opacity(0.25)).frame(width: 22, height: 22)
            Circle().fill(AnnoTheme.gold).frame(width: 10, height: 10)
                .overlay(Circle().strokeBorder(.white, lineWidth: 1.5))
        }
    }
}

private struct TopIconButton: View {
    let system: String
    let action: () -> Void
    var body: some View {
        Button(action: action) {
            Image(systemName: system)
                .font(.system(size: 16, weight: .medium))
                .foregroundStyle(AnnoTheme.textPrimary)
                .frame(width: 34, height: 34)
                .background(AnnoTheme.ink3, in: Circle())
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Component Library

struct TraditionChip: View {
    let tradition: Tradition
    var body: some View {
        HStack(spacing: 6) {
            Image(systemName: tradition.symbol)
                .font(.system(size: 10, weight: .semibold))
            Text(tradition.label).font(AnnoTheme.label(11))
        }
        .foregroundStyle(tradition.tint)
        .padding(.horizontal, 10).padding(.vertical, 5)
        .background(tradition.tint.opacity(0.14), in: Capsule())
        .overlay(Capsule().strokeBorder(tradition.tint.opacity(0.4), lineWidth: 0.75))
    }
}

struct ConfidenceBadge: View {
    let confidence: Confidence
    var body: some View {
        HStack(spacing: 4) {
            Circle().fill(confidence.color).frame(width: 6, height: 6)
            Text(confidence.label).font(AnnoTheme.label(10))
        }
        .foregroundStyle(confidence.color)
        .padding(.horizontal, 8).padding(.vertical, 4)
        .background(confidence.color.opacity(0.12), in: Capsule())
        .overlay(Capsule().strokeBorder(confidence.color.opacity(0.4)))
    }
}

struct PrimaryButton: View {
    let title: LocalizedStringKey
    let system: String
    let action: () -> Void
    var body: some View {
        Button(action: action) {
            HStack(spacing: 8) {
                Image(systemName: system)
                Text(title).font(AnnoTheme.serifBody(15).weight(.medium))
            }
            .foregroundStyle(AnnoTheme.ink)
            .padding(.vertical, 12).frame(maxWidth: .infinity)
            .background(AnnoTheme.gold, in: RoundedRectangle(cornerRadius: 12, style: .continuous))
        }
        .buttonStyle(.plain)
    }
}

struct SmallActionButton: View {
    let title: LocalizedStringKey
    let system: String
    let action: () -> Void
    var body: some View {
        Button(action: action) {
            HStack(spacing: 6) {
                Image(systemName: system).font(.system(size: 12, weight: .semibold))
                Text(title).font(AnnoTheme.label(11))
            }
            .foregroundStyle(AnnoTheme.textPrimary)
            .padding(.horizontal, 12).padding(.vertical, 10)
            .background(AnnoTheme.ink3, in: RoundedRectangle(cornerRadius: 10))
            .overlay(RoundedRectangle(cornerRadius: 10).strokeBorder(AnnoTheme.hairline))
        }
        .buttonStyle(.plain)
    }
}

struct SectionLabel: View {
    let title: LocalizedStringKey
    init(_ title: LocalizedStringKey) { self.title = title }
    var body: some View {
        HStack {
            Text(title).font(AnnoTheme.label()).foregroundStyle(AnnoTheme.gold)
            Rectangle().fill(AnnoTheme.gold.opacity(0.3)).frame(height: 0.5)
        }
    }
}

struct MetaTile: View {
    let icon: String
    let title: LocalizedStringKey
    let value: LocalizedStringKey
    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack(spacing: 6) {
                Image(systemName: icon).font(.caption).foregroundStyle(AnnoTheme.gold)
                Text(title).font(AnnoTheme.label(10)).foregroundStyle(AnnoTheme.textSecondary)
            }
            Text(value).font(AnnoTheme.serifBody(14)).foregroundStyle(AnnoTheme.textPrimary)
        }
        .padding(12)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(AnnoTheme.ink2, in: RoundedRectangle(cornerRadius: 10))
        .overlay(RoundedRectangle(cornerRadius: 10).strokeBorder(AnnoTheme.hairline))
    }
}

struct MetaInline: View {
    let icon: String
    let text: String
    var body: some View {
        HStack(spacing: 4) {
            Image(systemName: icon).font(.caption)
            Text(text).font(.caption)
        }
        .foregroundStyle(AnnoTheme.textSecondary)
    }
}

struct ArtworkFrame: View {
    let artwork: Artwork
    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            ZStack {
                RoundedRectangle(cornerRadius: 6, style: .continuous)
                    .fill(AnnoTheme.ink3)
                Image(systemName: artwork.systemImage)
                    .font(.system(size: 44, weight: .ultraLight))
                    .foregroundStyle(AnnoTheme.parchment2.opacity(0.8))
            }
            .frame(height: 180)
            .overlay(
                RoundedRectangle(cornerRadius: 6, style: .continuous)
                    .strokeBorder(AnnoTheme.gold.opacity(0.6), lineWidth: 3)
                    .padding(1)
            )
            HStack {
                Text(artwork.title).font(AnnoTheme.serifBody(13).italic())
                    .foregroundStyle(AnnoTheme.textPrimary)
                Spacer()
                Text(artwork.period).font(.caption)
                    .foregroundStyle(AnnoTheme.textSecondary)
            }
            Text(LocalizedStringKey("\(artwork.artist) · \(artwork.provenance)"))
                .font(.caption2)
                .foregroundStyle(AnnoTheme.textTertiary)
        }
    }
}

struct ProgressRing: View {
    let fraction: Double
    var body: some View {
        ZStack {
            Circle().stroke(AnnoTheme.hairline, lineWidth: 2)
            Circle().trim(from: 0, to: fraction)
                .stroke(AnnoTheme.gold, style: StrokeStyle(lineWidth: 2, lineCap: .round))
                .rotationEffect(.degrees(-90))
        }
    }
}

// MARK: - Location Detail Sheet
struct LocationDetailSheet: View {
    let location: SacredLocation
    
    @Environment(SacredAtlasViewModel.self)   private var vm
    @Environment(PilgrimJourneyViewModel.self) private var journey
    @Environment(EntitlementService.self)     private var entitlements
    @Environment(\.dismiss)                   private var dismiss
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                header
                
                if let artwork = vm.repo.artwork(id: location.artworkID) {
                    ArtworkFrame(artwork: artwork)
                }
                
                whyItMatters
                
                if !location.categories.isEmpty {
                    chipsRow
                }
                
                connectedEvents
                metadataGrid
                actionsRow
                
                if !entitlements.canReadFullDossier {
                    PaywallCardView(
                        title: L.unlockAtlasTitle,
                        body: L.unlockAtlasBody,
                        specifics: [
                            LocalizedStringKey("2,400+ sacred sites"),
                            LocalizedStringKey("Source dossiers & citations"),
                            LocalizedStringKey("Art gallery & lightbox"),
                            LocalizedStringKey("Curated pilgrimage route packs"),
                        ]
                    )
                }
                
                Color.clear.frame(height: 12)
            }
            .padding(20)
        }
        .background(AnnoTheme.ink.ignoresSafeArea())
    }
    
    private var header: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack(alignment: .top) {
                VStack(alignment: .leading, spacing: 4) {
                    Text(location.name)
                        .font(AnnoTheme.serifTitle(26))
                        .foregroundStyle(AnnoTheme.textPrimary)
                    Text(location.displayCity)
                        .font(.subheadline)
                        .foregroundStyle(AnnoTheme.textSecondary)
                }
                Spacer()
                Button { dismiss() } label: {
                    Image(systemName: "xmark")
                        .font(.system(size: 14, weight: .semibold))
                        .foregroundStyle(AnnoTheme.textSecondary)
                        .frame(width: 32, height: 32)
                        .background(AnnoTheme.ink3, in: Circle())
                }.buttonStyle(.plain)
            }
            HStack(spacing: 8) {
                TraditionChip(tradition: location.tradition)
                ConfidenceBadge(confidence: location.confidence)
                Spacer()
            }
        }
    }
    
    private var whyItMatters: some View {
        VStack(alignment: .leading, spacing: 8) {
            SectionLabel(L.whyItMatters)
            Text(location.shortWhyItMatters)
                .font(AnnoTheme.serifBody(16))
                .foregroundStyle(AnnoTheme.textPrimary)
                .lineSpacing(3)
        }
        .annoPanel()
    }
    
    private var chipsRow: some View {
        HStack(spacing: 6) {
            ForEach(location.categories, id: \.self) { cat in
                Label(cat.label, systemImage: cat.systemImage)
                    .font(AnnoTheme.label(11))
                    .foregroundStyle(AnnoTheme.textSecondary)
                    .padding(.horizontal, 10).padding(.vertical, 6)
                    .background(AnnoTheme.ink3, in: Capsule())
                    .overlay(Capsule().strokeBorder(AnnoTheme.hairline))
            }
        }
    }
    
    @ViewBuilder
    private var connectedEvents: some View {
        let events = vm.repo.events(for: location.id)
        if !events.isEmpty {
            VStack(alignment: .leading, spacing: 12) {
                SectionLabel(L.connectedEvents)
                ForEach(events) { e in
                    HStack(alignment: .top, spacing: 12) {
                        Text(eventYearString(e.date))
                            .font(AnnoTheme.serifBody(15))
                            .foregroundStyle(AnnoTheme.gold)
                            .frame(width: 56, alignment: .leading)
                        VStack(alignment: .leading, spacing: 3) {
                            Text(e.title)
                                .font(AnnoTheme.serifBody(15))
                                .foregroundStyle(AnnoTheme.textPrimary)
                            Text(e.narrative)
                                .font(.footnote)
                                .foregroundStyle(AnnoTheme.textSecondary)
                        }
                    }
                    .padding(.vertical, 4)
                    if e.id != events.last?.id {
                        Divider().background(AnnoTheme.hairline)
                    }
                }
            }
            .annoPanel()
        }
    }
    
    private var metadataGrid: some View {
        HStack(spacing: 12) {
            MetaTile(icon: "clock",
                     title: L.visitingHours,
                     value: LocalizedStringKey(location.visitingHours ?? "—"))
            MetaTile(icon: "text.book.closed",
                     title: L.sources,
                     value: LocalizedStringKey("\(location.sourceIDs.count)"))
        }
    }
    
    private var actionsRow: some View {
        HStack(spacing: 10) {
            SmallActionButton(title: vm.isSaved(location) ? L.saved : L.save,
                              system: vm.isSaved(location) ? "bookmark.fill" : "bookmark") {
                vm.toggleSaved(location)
            }
            SmallActionButton(title: L.directions, system: "arrow.turn.up.right") { }
            if entitlements.canStartPilgrimage {
                PrimaryButton(title: L.startPilgrimage, system: "figure.walk") {
                    if let packID = location.routePackIDs.first,
                       let pack = vm.repo.routePack(id: packID) {
                        journey.startJourney(pack: pack)
                    }
                }
            } else {
                PrimaryButton(title: L.startPilgrimage, system: "lock.fill") {
                    vm.isPaywallOpen = true
                }
                .opacity(0.85)
            }
        }
    }
    
    private func eventYearString(_ dc: DateComponents) -> String {
        guard let y = dc.year else { return "—" }
        return "\(y)"
    }
}

// MARK: - Filter Bar & Sheet
struct LayerFilterBar: View {
    @Environment(SacredAtlasViewModel.self) private var vm
    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                Chip(text: L.all, isOn: vm.selectedTraditions.isEmpty) {
                    vm.selectedTraditions.removeAll()
                }
                ForEach(Tradition.allCases) { t in
                    Chip(text: t.label, isOn: vm.selectedTraditions.contains(t),
                         tint: t.tint) { vm.toggle(tradition: t) }
                }
                Divider().frame(height: 14).background(AnnoTheme.hairline)
                Chip(text: L.today, isOn: vm.showTodayOnly, tint: AnnoTheme.gold) {
                    vm.showTodayOnly.toggle()
                }
            }
            .padding(.horizontal)
        }
    }
    
    struct Chip: View {
        let text: LocalizedStringKey
        let isOn: Bool
        var tint: Color = AnnoTheme.gold
        let action: () -> Void
        var body: some View {
            Button(action: action) {
                Text(text)
                    .font(AnnoTheme.label(11))
                    .foregroundStyle(isOn ? AnnoTheme.ink : AnnoTheme.textPrimary)
                    .padding(.horizontal, 12).padding(.vertical, 7)
                    .background(isOn ? tint : AnnoTheme.ink3, in: Capsule())
                    .overlay(Capsule().strokeBorder(isOn ? tint : AnnoTheme.hairline, lineWidth: 0.5))
            }
            .buttonStyle(.plain)
        }
    }
}

struct LayerFiltersSheet: View {
    @Environment(SacredAtlasViewModel.self) private var vm
    @Environment(EntitlementService.self)   private var entitlements
    @Environment(\.dismiss)                 private var dismiss
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 18) {
                    section(L.category) {
                        LazyVGrid(columns: [.init(.adaptive(minimum: 100), spacing: 8)], spacing: 8) {
                            ForEach(SacredCategory.allCases) { c in
                                LayerFilterBar.Chip(
                                    text: c.label,
                                    isOn: vm.selectedCategories.contains(c)
                                ) { vm.toggle(category: c) }
                            }
                        }
                    }
                    section(L.confidence) {
                        HStack(spacing: 8) {
                            ForEach(Confidence.allCases, id: \.self) { c in
                                LayerFilterBar.Chip(
                                    text: c.label,
                                    isOn: vm.selectedConfidence.contains(c),
                                    tint: c.color
                                ) { vm.toggle(confidence: c) }
                            }
                        }
                        if !entitlements.canUseConfidenceLayer {
                            Text(LocalizedStringKey("Confidence layers are a Premium feature."))
                                .font(.caption).foregroundStyle(AnnoTheme.gold)
                        }
                    }
                    Button {
                        vm.clearFilters()
                    } label: {
                        Text(L.clear)
                            .font(AnnoTheme.label())
                            .foregroundStyle(AnnoTheme.textSecondary)
                            .padding(.top, 10)
                    }
                }
                .padding(20)
            }
            .background(AnnoTheme.ink)
            .navigationTitle(Text(L.layers))
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Done") { dismiss() }.foregroundStyle(AnnoTheme.gold)
                }
            }
        }
    }
    
    @ViewBuilder
    func section<C: View>(_ title: LocalizedStringKey, @ViewBuilder content: () -> C) -> some View {
        VStack(alignment: .leading, spacing: 10) { SectionLabel(title); content() }
    }
}

// MARK: - Nearby
struct NearbyPeekBar: View {
    @Environment(SacredAtlasViewModel.self) private var vm
    @Environment(LocationService.self)      private var location
    
    var body: some View {
        let items = vm.nearby(limit: 3)
        Button { vm.isNearbyOpen = true } label: {
            HStack(spacing: 10) {
                Image(systemName: "location.magnifyingglass")
                    .foregroundStyle(AnnoTheme.gold)
                VStack(alignment: .leading, spacing: 2) {
                    Text(L.nearby).font(AnnoTheme.label()).foregroundStyle(AnnoTheme.gold)
                    if let first = items.first {
                        Text(first.0.name).font(AnnoTheme.serifBody(14))
                            .foregroundStyle(AnnoTheme.textPrimary).lineLimit(1)
                    } else {
                        Text(LocalizedStringKey("No sacred sites in current filter"))
                            .font(AnnoTheme.serifBody(13))
                            .foregroundStyle(AnnoTheme.textSecondary)
                    }
                }
                Spacer()
                if let first = items.first {
                    Text(L.kmAway(first.1 / 1000))
                        .font(.caption2)
                        .foregroundStyle(AnnoTheme.textSecondary)
                }
                Image(systemName: "chevron.up").font(.caption2)
                    .foregroundStyle(AnnoTheme.textTertiary)
            }
            .padding(.horizontal, 14).padding(.vertical, 12)
            .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 14))
            .overlay(RoundedRectangle(cornerRadius: 14).strokeBorder(AnnoTheme.hairline))
        }
        .buttonStyle(.plain)
    }
}

struct NearbyInSacredHistoryView: View {
    @Environment(SacredAtlasViewModel.self) private var vm
    @Environment(EntitlementService.self)   private var entitlements
    @Environment(\.dismiss)                 private var dismiss
    
    var body: some View {
        let items = vm.nearby(limit: 12)
        let summary = vm.nearbyCountSummary()
        
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 14) {
                    Text(L.nearby).font(AnnoTheme.serifTitle(24))
                        .foregroundStyle(AnnoTheme.textPrimary)
                    Text(LocalizedStringKey("Sacred sites within 400 km, ranked by proximity."))
                        .font(.footnote).foregroundStyle(AnnoTheme.textSecondary)
                    
                    ForEach(items, id: \.0.id) { (loc, dist) in
                        Button {
                            vm.select(loc); dismiss()
                        } label: {
                            HStack(spacing: 12) {
                                SacredPinView(tradition: loc.tradition,
                                              category: loc.categories.first,
                                              selected: false, locked: false, visited: false)
                                    .frame(width: 30, height: 40)
                                VStack(alignment: .leading, spacing: 3) {
                                    Text(loc.name).font(AnnoTheme.serifBody(15))
                                        .foregroundStyle(AnnoTheme.textPrimary)
                                    Text(loc.displayCity).font(.caption)
                                        .foregroundStyle(AnnoTheme.textSecondary)
                                }
                                Spacer()
                                Text(L.kmAway(dist / 1000))
                                    .font(.caption).foregroundStyle(AnnoTheme.gold)
                            }
                            .padding(.vertical, 6)
                        }
                        .buttonStyle(.plain)
                        Divider().background(AnnoTheme.hairline)
                    }
                    
                    if !entitlements.canBrowseFullAtlas {
                        PaywallCardView(
                            title: LocalizedStringKey("Near you in sacred history"),
                            body: LocalizedStringKey("\(summary.total) sites within 400 km · \(summary.today) connected to today's feasts · \(summary.traditional) traditional · \(summary.disputed) disputed."),
                            specifics: [
                                LocalizedStringKey("Full nearby list without limits"),
                                LocalizedStringKey("Confidence-layer filters"),
                                LocalizedStringKey("Source dossiers on every site"),
                                LocalizedStringKey("Curated route packs"),
                            ]
                        )
                    }
                }
                .padding(20)
            }
            .background(AnnoTheme.ink)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }.foregroundStyle(AnnoTheme.gold)
                }
            }
        }
    }
}

// MARK: - Route Packs
struct RoutePacksView: View {
    @Environment(SacredAtlasViewModel.self)    private var vm
    @Environment(EntitlementService.self)      private var entitlements
    @Environment(\.dismiss)                    private var dismiss
    @State private var openedPack: RoutePack?
    
    var body: some View {
        NavigationStack {
            ScrollView {
                LazyVStack(spacing: 14) {
                    ForEach(vm.repo.routePacks) { pack in
                        RoutePackCard(pack: pack)
                            .onTapGesture { openedPack = pack }
                    }
                }
                .padding(16)
            }
            .background(AnnoTheme.ink)
            .navigationTitle(Text(L.routePacks))
            .navigationBarTitleDisplayMode(.inline)
            .toolbarBackground(AnnoTheme.ink, for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }
                        .foregroundStyle(AnnoTheme.gold)
                }
            }
        }
        .sheet(item: $openedPack) { pack in
            RoutePackDetailView(pack: pack)
                .presentationDetents([.large])
                .presentationBackground(AnnoTheme.ink)
        }
    }
}

struct RoutePackCard: View {
    let pack: RoutePack
    @Environment(EntitlementService.self) private var entitlements
    
    var isLocked: Bool { !entitlements.has(pack.requiredTier) }
    
    var body: some View {
        HStack(alignment: .top, spacing: 14) {
            ZStack {
                RoundedRectangle(cornerRadius: 12, style: .continuous)
                    .fill(AnnoTheme.ink3)
                Image(systemName: pack.heroSymbol)
                    .font(.system(size: 26, weight: .light))
                    .foregroundStyle(AnnoTheme.gold)
            }
            .frame(width: 68, height: 68)
            
            VStack(alignment: .leading, spacing: 6) {
                HStack {
                    Text(pack.title)
                        .font(AnnoTheme.serifTitle(18))
                        .foregroundStyle(AnnoTheme.textPrimary)
                    Spacer()
                    if isLocked {
                        Image(systemName: pack.requiredTier == .pilgrim ? "crown.fill" : "lock.fill")
                            .foregroundStyle(AnnoTheme.gold)
                    }
                }
                Text(pack.subtitle)
                    .font(.footnote)
                    .foregroundStyle(AnnoTheme.textSecondary)
                    .lineLimit(2)
                HStack(spacing: 10) {
                    Label("\(pack.stopIDs.count) sites", systemImage: "mappin.and.ellipse")
                    Label(String(format: "%.0f km", pack.estimatedKm), systemImage: "figure.walk")
                    Label(String(format: "%.0f h", pack.estimatedHours), systemImage: "clock")
                }
                .font(.caption2)
                .foregroundStyle(AnnoTheme.textTertiary)
            }
        }
        .annoPanel()
    }
}

struct RoutePackDetailView: View {
    let pack: RoutePack
    @Environment(SacredAtlasViewModel.self)     private var vm
    @Environment(PilgrimJourneyViewModel.self)  private var journey
    @Environment(EntitlementService.self)       private var entitlements
    @Environment(\.dismiss)                     private var dismiss
    
    var isLocked: Bool { !entitlements.has(pack.requiredTier) }
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 18) {
                header
                stopsList
                if isLocked {
                    lockedPreview
                } else if entitlements.canStartPilgrimage {
                    startButton
                } else {
                    PaywallCardView(
                        title: LocalizedStringKey("Upgrade to Pilgrim to start this route"),
                        body: LocalizedStringKey("Pilgrim Mode adds live journey tracking, field notes, artifact stamps, and offline route prep."),
                        specifics: [
                            LocalizedStringKey("Live route tracking"),
                            LocalizedStringKey("Local-only Pilgrim Passport"),
                            LocalizedStringKey("Offline stop cards & prayers"),
                            LocalizedStringKey("Exportable pilgrimage record"),
                        ]
                    )
                }
                Color.clear.frame(height: 24)
            }
            .padding(20)
        }
        .background(AnnoTheme.ink.ignoresSafeArea())
    }
    
    private var header: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: pack.heroSymbol)
                    .font(.system(size: 36, weight: .light))
                    .foregroundStyle(AnnoTheme.gold)
                Spacer()
                Button { dismiss() } label: {
                    Image(systemName: "xmark")
                        .font(.system(size: 14, weight: .semibold))
                        .foregroundStyle(AnnoTheme.textSecondary)
                        .frame(width: 32, height: 32)
                        .background(AnnoTheme.ink3, in: Circle())
                }.buttonStyle(.plain)
            }
            Text(pack.title).font(AnnoTheme.serifTitle(28))
                .foregroundStyle(AnnoTheme.textPrimary)
            Text(pack.subtitle).font(AnnoTheme.serifBody(15))
                .foregroundStyle(AnnoTheme.textSecondary)
            HStack(spacing: 10) {
                ForEach(pack.traditions, id: \.self) { TraditionChip(tradition: $0) }
            }
            HStack(spacing: 16) {
                MetaInline(icon: "mappin.and.ellipse", text: "\(pack.stopIDs.count) sites")
                MetaInline(icon: "figure.walk", text: String(format: "%.0f km", pack.estimatedKm))
                MetaInline(icon: "clock", text: String(format: "%.0f h", pack.estimatedHours))
            }
        }
    }
    
    private var stopsList: some View {
        let stops = vm.repo.stops(for: pack)
        let visibleCount = isLocked ? pack.previewStopCount : stops.count
        return VStack(alignment: .leading, spacing: 10) {
            SectionLabel(LocalizedStringKey("Stops"))
            ForEach(Array(stops.prefix(visibleCount).enumerated()), id: \.offset) { i, stop in
                HStack(spacing: 12) {
                    ZStack {
                        Circle().stroke(AnnoTheme.gold, lineWidth: 1).frame(width: 26, height: 26)
                        Text("\(i+1)").font(.caption).foregroundStyle(AnnoTheme.gold)
                    }
                    VStack(alignment: .leading, spacing: 2) {
                        Text(stop.name).font(AnnoTheme.serifBody(15))
                            .foregroundStyle(AnnoTheme.textPrimary)
                        Text(stop.displayCity).font(.caption)
                            .foregroundStyle(AnnoTheme.textSecondary)
                    }
                    Spacer()
                    ConfidenceBadge(confidence: stop.confidence).font(.caption2)
                }
                .padding(.vertical, 6)
            }
            if isLocked && stops.count > visibleCount {
                Text(LocalizedStringKey("+ \(stops.count - visibleCount) more stops in Premium"))
                    .font(.footnote)
                    .foregroundStyle(AnnoTheme.gold)
                    .padding(.top, 4)
            }
        }
        .annoPanel()
    }
    
    private var lockedPreview: some View {
        PaywallCardView(
            title: LocalizedStringKey("Unlock this route"),
            body: LocalizedStringKey("\(pack.stopIDs.count) source-backed stops · \(Int(pack.estimatedKm)) km · offline prep · pilgrimage passport."),
            specifics: [
                LocalizedStringKey("All route stops with source citations"),
                LocalizedStringKey("Offline route prep"),
                LocalizedStringKey("Live Pilgrim Mode tracking"),
                LocalizedStringKey("Private local Pilgrim Passport"),
            ]
        )
    }
    
    private var startButton: some View {
        PrimaryButton(title: L.startPilgrimage, system: "figure.walk") {
            journey.startJourney(pack: pack)
            dismiss()
        }
    }
}

// MARK: - Pilgrim Views
struct ActiveJourneyBanner: View {
    @Environment(PilgrimJourneyViewModel.self) private var journey
    @Environment(SacredAtlasViewModel.self)    private var vm
    
    var body: some View {
        if let pack = journey.currentPack {
            Button {
                vm.isPassportOpen = true
            } label: {
                HStack(spacing: 12) {
                    Image(systemName: "figure.walk.circle.fill")
                        .foregroundStyle(AnnoTheme.gold)
                        .font(.system(size: 22))
                    VStack(alignment: .leading, spacing: 2) {
                        Text(pack.title).font(AnnoTheme.serifBody(14))
                            .foregroundStyle(AnnoTheme.textPrimary)
                        Text(LocalizedStringKey("\(journey.visitedCount)/\(journey.stops.count) visited · \(journey.elapsedString) elapsed"))
                            .font(.caption2)
                            .foregroundStyle(AnnoTheme.textSecondary)
                    }
                    Spacer()
                    ProgressRing(fraction: journey.progressFraction)
                        .frame(width: 26, height: 26)
                }
                .padding(.horizontal, 14).padding(.vertical, 10)
                .background(AnnoTheme.ink3, in: Capsule())
                .overlay(Capsule().strokeBorder(AnnoTheme.gold.opacity(0.5)))
                .padding(.horizontal)
            }
            .buttonStyle(.plain)
        }
    }
}

struct PilgrimPassportView: View {
    @Environment(PilgrimJourneyViewModel.self) private var journey
    @Environment(SacredAtlasViewModel.self)    private var vm
    @Environment(EntitlementService.self)      private var entitlements
    @Environment(\.dismiss)                    private var dismiss
    @Query(sort: \PassportStamp.visitedAt, order: .reverse) private var allStamps: [PassportStamp]
    @Query(sort: \JourneySession.startedAt, order: .reverse) private var allSessions: [JourneySession]
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 18) {
                    if !entitlements.canStartPilgrimage {
                        PaywallCardView(
                            title: LocalizedStringKey("Pilgrim Mode"),
                            body: LocalizedStringKey("A private, local pilgrimage record — stamps, notes, and journeys — that never leaves your device."),
                            specifics: [
                                LocalizedStringKey("Visited-site stamps"),
                                LocalizedStringKey("Local field notes & prayers"),
                                LocalizedStringKey("Route completion timeline"),
                                LocalizedStringKey("Exportable pilgrimage record"),
                            ]
                        )
                    }
                    
                    if journey.currentSession != nil {
                        ActiveSessionPanel()
                    }
                    
                    summaryHeader
                    stampsSection
                    completedJourneysSection
                    Color.clear.frame(height: 24)
                }
                .padding(20)
            }
            .background(AnnoTheme.ink)
            .navigationTitle(Text(L.passport))
            .navigationBarTitleDisplayMode(.inline)
            .toolbarBackground(AnnoTheme.ink, for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }.foregroundStyle(AnnoTheme.gold)
                }
            }
        }
    }
    
    private var summaryHeader: some View {
        HStack(spacing: 12) {
            StatTile(number: "\(allSessions.filter { !$0.isActive }.count)",
                     label: L.journeysCompleted)
            StatTile(number: "\(allStamps.count)", label: L.sitesVisited)
            StatTile(number: "\(allSessions.flatMap { $0.notes }.count)", label: L.fieldNotes)
        }
    }
    
    @ViewBuilder
    private var stampsSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            SectionLabel(L.stamps)
            if allStamps.isEmpty {
                Text(L.noStampsYet)
                    .font(AnnoTheme.serifBody(14))
                    .foregroundStyle(AnnoTheme.textSecondary)
                    .padding(.vertical, 20)
                    .frame(maxWidth: .infinity)
            } else {
                LazyVGrid(columns: [.init(.adaptive(minimum: 88), spacing: 10)], spacing: 10) {
                    ForEach(allStamps) { s in
                        StampView(stamp: s)
                    }
                }
            }
        }
        .annoPanel()
    }
    
    @ViewBuilder
    private var completedJourneysSection: some View {
        let completed = allSessions.filter { !$0.isActive }
        if !completed.isEmpty {
            VStack(alignment: .leading, spacing: 10) {
                SectionLabel(LocalizedStringKey("Completed Journeys"))
                ForEach(completed) { s in
                    HStack {
                        Image(systemName: "checkmark.seal.fill").foregroundStyle(AnnoTheme.gold)
                        VStack(alignment: .leading, spacing: 2) {
                            Text(s.routePackTitle).font(AnnoTheme.serifBody(15))
                                .foregroundStyle(AnnoTheme.textPrimary)
                            Text(s.startedAt, style: .date).font(.caption2)
                                .foregroundStyle(AnnoTheme.textSecondary)
                        }
                        Spacer()
                        Text("\(s.visitedStopIDs.count)").font(AnnoTheme.serifBody(14))
                            .foregroundStyle(AnnoTheme.gold)
                    }
                    .padding(.vertical, 6)
                    if s.id != completed.last?.id {
                        Divider().background(AnnoTheme.hairline)
                    }
                }
            }
            .annoPanel()
        }
    }
}

private struct StampView: View {
    let stamp: PassportStamp
    var body: some View {
        VStack(spacing: 6) {
            ZStack {
                Circle().stroke(stamp.tradition.tint, lineWidth: 1.5)
                    .frame(width: 58, height: 58)
                Image(systemName: stamp.tradition.symbol)
                    .font(.system(size: 20))
                    .foregroundStyle(stamp.tradition.tint)
            }
            Text(stamp.locationName)
                .font(.caption2).multilineTextAlignment(.center)
                .foregroundStyle(AnnoTheme.textPrimary)
                .lineLimit(2)
            Text(stamp.visitedAt, style: .date)
                .font(.system(size: 9))
                .foregroundStyle(AnnoTheme.textTertiary)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 8)
    }
}

private struct StatTile: View {
    let number: String
    let label: LocalizedStringKey
    var body: some View {
        VStack(spacing: 4) {
            Text(number).font(AnnoTheme.serifTitle(28)).foregroundStyle(AnnoTheme.gold)
            Text(label).font(AnnoTheme.label(10)).foregroundStyle(AnnoTheme.textSecondary)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 14)
        .background(AnnoTheme.ink2, in: RoundedRectangle(cornerRadius: 12, style: .continuous))
        .overlay(RoundedRectangle(cornerRadius: 12, style: .continuous).strokeBorder(AnnoTheme.hairline))
    }
}

struct ActiveSessionPanel: View {
    @Environment(PilgrimJourneyViewModel.self) private var journey
    @State private var noteDraft: String = ""
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text(L.activeJourney).font(AnnoTheme.label()).foregroundStyle(AnnoTheme.gold)
                Spacer()
                Text(journey.elapsedString).font(.caption).foregroundStyle(AnnoTheme.textSecondary)
            }
            if let next = journey.nextStop {
                VStack(alignment: .leading, spacing: 4) {
                    Text(L.nextStop).font(AnnoTheme.label(10))
                        .foregroundStyle(AnnoTheme.textTertiary)
                    Text(next.name).font(AnnoTheme.serifTitle(20))
                        .foregroundStyle(AnnoTheme.textPrimary)
                    Text(next.displayCity).font(.caption)
                        .foregroundStyle(AnnoTheme.textSecondary)
                }
                HStack {
                    SmallActionButton(title: L.markVisited, system: "checkmark.seal") {
                        journey.markVisited(next)
                    }
                    Spacer()
                }
            } else {
                Text(L.allStopsVisited)
                    .font(AnnoTheme.serifBody(14))
                    .foregroundStyle(AnnoTheme.textSecondary)
            }
            
            VStack(alignment: .leading, spacing: 6) {
                SectionLabel(L.addNote)
                HStack {
                    TextField("", text: $noteDraft, prompt: Text("Field note…")
                        .foregroundStyle(AnnoTheme.textTertiary))
                        .textFieldStyle(.plain)
                        .foregroundStyle(AnnoTheme.textPrimary)
                        .padding(.horizontal, 10).padding(.vertical, 8)
                        .background(AnnoTheme.ink3, in: RoundedRectangle(cornerRadius: 10))
                    Button {
                        journey.addNote(noteDraft, at: journey.nextStop)
                        noteDraft = ""
                    } label: {
                        Image(systemName: "arrow.up.circle.fill")
                            .font(.system(size: 26)).foregroundStyle(AnnoTheme.gold)
                    }
                    .disabled(noteDraft.isEmpty)
                }
            }
            
            HStack {
                Button(role: .destructive) {
                    journey.endJourney()
                } label: {
                    Label(L.endJourney, systemImage: "flag.checkered")
                        .font(.subheadline)
                        .foregroundStyle(AnnoTheme.disputed)
                }
                Spacer()
                ProgressView(value: journey.progressFraction)
                    .tint(AnnoTheme.gold)
                    .frame(width: 140)
            }
        }
        .annoPanel()
    }
}

// MARK: - Paywall
struct PaywallCardView: View {
    let title: LocalizedStringKey
    let body:  LocalizedStringKey
    let specifics: [LocalizedStringKey]
    
    @Environment(SacredAtlasViewModel.self) private var vm
    
    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack(spacing: 8) {
                Image(systemName: "crown.fill").foregroundStyle(AnnoTheme.gold)
                Text(title).font(AnnoTheme.serifTitle(18))
                    .foregroundStyle(AnnoTheme.textPrimary)
            }
            Text(body).font(AnnoTheme.serifBody(14))
                .foregroundStyle(AnnoTheme.textSecondary)
            VStack(alignment: .leading, spacing: 6) {
                ForEach(specifics, id: \.self) { s in
                    HStack(spacing: 8) {
                        Image(systemName: "checkmark").foregroundStyle(AnnoTheme.gold).font(.caption)
                        Text(s).font(.footnote).foregroundStyle(AnnoTheme.textPrimary)
                    }
                }
            }
            .padding(.top, 4)
            PrimaryButton(title: L.unlock, system: "lock.open.fill") { vm.isPaywallOpen = true }
                .padding(.top, 4)
        }
        .padding(16)
        .background(
            LinearGradient(colors: [AnnoTheme.ink3, AnnoTheme.ink2],
                           startPoint: .topLeading, endPoint: .bottomTrailing),
            in: RoundedRectangle(cornerRadius: AnnoTheme.rMed, style: .continuous))
        .overlay(RoundedRectangle(cornerRadius: AnnoTheme.rMed, style: .continuous)
            .strokeBorder(AnnoTheme.gold.opacity(0.5), lineWidth: 0.75))
    }
}

struct PaywallSheet: View {
    @Environment(EntitlementService.self) private var entitlements
    @Environment(\.dismiss)               private var dismiss
    
    var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                Image(systemName: "crown.fill")
                    .font(.system(size: 44)).foregroundStyle(AnnoTheme.gold)
                Text(L.unlockAtlasTitle)
                    .font(AnnoTheme.serifTitle(26))
                    .foregroundStyle(AnnoTheme.textPrimary)
                Text(L.unlockAtlasBody)
                    .multilineTextAlignment(.center)
                    .font(AnnoTheme.serifBody(15))
                    .foregroundStyle(AnnoTheme.textSecondary)
                    .padding(.horizontal)
                
                VStack(spacing: 10) {
                    PlanRow(price: "$69.99 / year", subtitle: L.bestValue, tier: .pilgrim,
                            isRecommended: true) {
                        entitlements.tier = .pilgrim; dismiss()
                    }
                    PlanRow(price: "$5.99 / month", subtitle: LocalizedStringKey("Premium"),
                            tier: .premium, isRecommended: false) {
                        entitlements.tier = .premium; dismiss()
                    }
                }
                .padding(.horizontal, 20)
                
                Text(L.noAdsNoAiSlop).font(.footnote)
                    .foregroundStyle(AnnoTheme.textSecondary)
                Text(L.sourcesOnEvery).font(.footnote)
                    .foregroundStyle(AnnoTheme.textSecondary)
                
                HStack(spacing: 20) {
                    Button(L.restore) { }.foregroundStyle(AnnoTheme.textTertiary)
                    Button(L.terms)   { }.foregroundStyle(AnnoTheme.textTertiary)
                    Button(L.privacy) { }.foregroundStyle(AnnoTheme.textTertiary)
                }
                .font(.caption2)
                .padding(.top, 20)
            }
            .padding(.top, 30)
        }
        .background(AnnoTheme.ink.ignoresSafeArea())
        .overlay(alignment: .topTrailing) {
            Button { dismiss() } label: {
                Image(systemName: "xmark").font(.system(size: 14, weight: .semibold))
                    .foregroundStyle(AnnoTheme.textSecondary)
                    .frame(width: 32, height: 32)
                    .background(AnnoTheme.ink3, in: Circle())
            }.buttonStyle(.plain).padding()
        }
    }
    
    struct PlanRow: View {
        let price: String
        let subtitle: LocalizedStringKey
        let tier: EntitlementTier
        let isRecommended: Bool
        let action: () -> Void
        var body: some View {
            Button(action: action) {
                HStack {
                    VStack(alignment: .leading, spacing: 2) {
                        Text(price).font(AnnoTheme.serifTitle(20))
                            .foregroundStyle(isRecommended ? AnnoTheme.ink : AnnoTheme.textPrimary)
                        Text(subtitle).font(AnnoTheme.label(10))
                            .foregroundStyle(isRecommended ? AnnoTheme.ink.opacity(0.7) : AnnoTheme.textSecondary)
                    }
                    Spacer()
                    Image(systemName: "chevron.right")
                        .foregroundStyle(isRecommended ? AnnoTheme.ink : AnnoTheme.textSecondary)
                }
                .padding(.horizontal, 16).padding(.vertical, 14)
                .background(isRecommended ? AnnoTheme.gold : AnnoTheme.ink3,
                            in: RoundedRectangle(cornerRadius: 12))
                .overlay(RoundedRectangle(cornerRadius: 12)
                    .strokeBorder(isRecommended ? AnnoTheme.gold : AnnoTheme.hairline))
            }
            .buttonStyle(.plain)
        }
    }
}

// MARK: - Previews
struct PreviewHarness<Content: View>: View {
    let tier: EntitlementTier
    let content: () -> Content
    let container: ModelContainer
    
    init(tier: EntitlementTier, @ViewBuilder content: @escaping () -> Content) {
        self.tier = tier
        self.content = content
        let schema = Schema([JourneySession.self, PassportStamp.self, FieldNote.self])
        let cfg = ModelConfiguration(schema: schema, isStoredInMemoryOnly: true)
        self.container = try! ModelContainer(for: schema, configurations: [cfg])
    }
    
    var body: some View {
        let ent = EntitlementService(tier: tier)
        let loc = LocationService()
        let atlas = SacredAtlasViewModel(repo: MockSacredRepository.shared,
                                         entitlements: ent, location: loc)
        let journey = PilgrimJourneyViewModel(repo: MockSacredRepository.shared,
                                              entitlements: ent, location: loc)
        journey.modelContext = container.mainContext
        return content()
            .environment(atlas)
            .environment(journey)
            .environment(ent)
            .environment(loc)
            .modelContainer(container)
            .preferredColorScheme(.dark)
    }
}

#Preview("Map — Free tier") {
    PreviewHarness(tier: .free) { SacredAtlasMapView() }
}

#Preview("Map — Premium tier") {
    PreviewHarness(tier: .premium) { SacredAtlasMapView() }
}

#Preview("Map — Pilgrim tier") {
    PreviewHarness(tier: .pilgrim) { SacredAtlasMapView() }
}

#Preview("Location Detail — Tower Hill") {
    PreviewHarness(tier: .premium) {
        LocationDetailSheet(location: MockSacredRepository.shared.location(id: "loc.towerhill")!)
    }
}

#Preview("Route Packs") {
    PreviewHarness(tier: .free) { RoutePacksView() }
}

#Preview("Route Detail — Seven Churches (locked)") {
    PreviewHarness(tier: .free) {
        RoutePackDetailView(pack: MockSacredRepository.shared.routePack(id: "route.romeSeven")!)
    }
}

#Preview("Passport — Empty") {
    PreviewHarness(tier: .pilgrim) { PilgrimPassportView() }
}

#Preview("Paywall") {
    PreviewHarness(tier: .free) { PaywallSheet() }
}

#Preview("Vietnamese chrome") {
    PreviewHarness(tier: .premium) { SacredAtlasMapView() }
        .environment(\.locale, Locale(identifier: "vi"))
}

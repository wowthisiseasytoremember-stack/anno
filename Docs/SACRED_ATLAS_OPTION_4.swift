File 1: AnnoTheme.swift
Swift

import SwiftUI

// MARK: - Design Tokens
/// Centralized visual language for the Sacred Atlas feature.
/// Dark sacred atlas, ivory parchment, gold ink, restrained Catholic visual language.

enum AnnoTheme {
    // MARK: Colors
    static let background = Color(hex: "0D0F14")
    static let cardBackground = Color(hex: "1A1714")
    static let cardElevated = Color(hex: "252119")
    static let ivory = Color(hex: "F5F0E8")
    static let ivoryDim = Color(hex: "C8C0B0")
    static let gold = Color(hex: "C9A84C")
    static let goldDim = Color(hex: "8B7332")
    static let goldBright = Color(hex: "E5C95C")
    static let mutedText = Color(hex: "9A9080")
    static let separator = Color(hex: "332E26")

    // MARK: Tradition Colors
    static let catholicColor = Color(hex: "E8D5A3")
    static let orthodoxColor = Color(hex: "7B6CE7")
    static let jewishColor = Color(hex: "4A7FB5")
    static let islamicColor = Color(hex: "2D8B57")
    static let interfaithColor = Color(hex: "8A9BAE")

    // MARK: Confidence Colors
    static let confirmedColor = Color(hex: "4CAF50")
    static let traditionalColor = Color(hex: "C9A84C")
    static let disputedColor = Color(hex: "E57373")

    // MARK: Spacing
    static let spacingXS: CGFloat = 4
    static let spacingSM: CGFloat = 8
    static let spacingMD: CGFloat = 12
    static let spacingLG: CGFloat = 16
    static let spacingXL: CGFloat = 24
    static let spacingXXL: CGFloat = 32

    // MARK: Radii
    static let radiusSM: CGFloat = 6
    static let radiusMD: CGFloat = 10
    static let radiusLG: CGFloat = 14
    static let radiusXL: CGFloat = 20

    // MARK: Fonts
    static let headingLarge = Font.serifBold(size: 28)
    static let headingMedium = Font.serifBold(size: 22)
    static let headingSmall = Font.serifBold(size: 17)
    static let bodyLarge = Font.system(size: 17, weight: .regular, design: .default)
    static let bodyMedium = Font.system(size: 15, weight: .regular, design: .default)
    static let bodySmall = Font.system(size: 13, weight: .regular, design: .default)
    static let caption = Font.system(size: 11, weight: .medium, design: .default)
    static let captionSerif = Font.serifRegular(size: 11)
}

// MARK: - Font Helpers
extension Font {
    static func serifBold(size: CGFloat) -> Font {
        .system(size: size, weight: .bold, design: .serif)
    }
    static func serifRegular(size: CGFloat) -> Font {
        .system(size: size, weight: .regular, design: .serif)
    }
    static func serifItalic(size: CGFloat) -> Font {
        .system(size: size, weight: .regular, design: .serif)
        // Note: italic trait would need attributed string in Text;
        // this is a placeholder for the design intent.
    }
}

// MARK: - Color Extension
extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 6:
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8:
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }
        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}

// MARK: - View Modifiers
struct AtlasCardModifier: ViewModifier {
    var elevated: Bool = false
    func body(content: Content) -> some View {
        content
            .background(elevated ? AnnoTheme.cardElevated : AnnoTheme.cardBackground)
            .clipShape(RoundedRectangle(cornerRadius: AnnoTheme.radiusLG))
            .shadow(color: .black.opacity(0.4), radius: 8, y: 4)
    }
}

extension View {
    func atlasCard(elevated: Bool = false) -> some View {
        modifier(AtlasCardModifier(elevated: elevated))
    }
}
File 2: Models.swift
Swift

import Foundation
import CoreLocation
import SwiftData

// MARK: - Tradition
enum Tradition: String, Codable, CaseIterable, Identifiable {
    case catholic
    case orthodox
    case jewish
    case islamic
    case interfaith

    var id: String { rawValue }

    var color: String {
        switch self {
        case .catholic: return "E8D5A3"
        case .orthodox: return "7B6CE7"
        case .jewish: return "4A7FB5"
        case .islamic: return "2D8B57"
        case .interfaith: return "8A9BAE"
        }
    }

    var symbol: String {
        switch self {
        case .catholic: return "✝"
        case .orthodox: return "☦"
        case .jewish: return "✡"
        case .islamic: return "☪"
        case .interfaith: return "◎"
        }
    }
}

// MARK: - Confidence Label
enum ConfidenceLabel: String, Codable, CaseIterable, Identifiable {
    case confirmed
    case traditional
    case disputed

    var id: String { rawValue }
}

// MARK: - Sacred Site Category
enum SacredSiteCategory: String, Codable, CaseIterable, Identifiable {
    case saints
    case martyrs
    case councils
    case relics
    case marian
    case monasteries
    case biblical
    case pilgrimage

    var id: String { rawValue }

    var symbol: String {
        switch self {
        case .saints: return "hand.raised"
        case .martyrs: return "flame"
        case .councils: return "building.columns"
        case .relics: return "cross.case"
        case .marian: return "star.circle"
        case .monasteries: return "building.2"
        case .biblical: return "book.closed"
        case .pilgrimage: return "point.topleft.down.to.point.bottomright.curvepath"
        }
    }
}

// MARK: - Map Layer Filter
enum SacredLayer: String, CaseIterable, Identifiable {
    case today
    case saints
    case martyrs
    case councils
    case relics
    case marian
    case monasteries
    case biblical
    case pilgrimage

    var id: String { rawValue }

    var category: SacredSiteCategory? {
        switch self {
        case .today: return nil
        case .saints: return .saints
        case .martyrs: return .martyrs
        case .councils: return .councils
        case .relics: return .relics
        case .marian: return .marian
        case .monasteries: return .monasteries
        case .biblical: return .biblical
        case .pilgrimage: return .pilgrimage
        }
    }
}

// MARK: - Sacred Location
struct SacredLocation: Identifiable, Equatable {
    let id: String
    let placeName: String
    let latitude: Double
    let longitude: Double
    let modernAddress: String?
    let country: String
    let region: String
    let traditions: [Tradition]
    let categories: [SacredSiteCategory]
    let confidence: ConfidenceLabel
    let shortNarrative: String
    let onThisGroundNarrative: String
    let associatedEventIDs: [String]
    let artworkIDs: [String]
    let sourceIDs: [String]
    let visitingHours: String?
    let routePackIDs: [String]
    let isTodayConnected: Bool  // connected to today's date

    var coordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
    }

    static func == (lhs: SacredLocation, rhs: SacredLocation) -> Bool {
        lhs.id == rhs.id
    }
}

// MARK: - Historical Event
struct HistoricalEvent: Identifiable {
    let id: String
    let dateDescription: String  // "c. 64 AD", "Nov 9", "Sep 17, 1224"
    let title: String
    let shortNarrative: String
    let tradition: Tradition
    let liturgicalColor: String?
    let locationID: String?
    let artworkID: String?
    let sourceIDs: [String]
    let confidence: ConfidenceLabel
    let gregorianMonth: Int?  // for "today" matching
    let gregorianDay: Int?
}

// MARK: - Artwork
struct Artwork: Identifiable {
    let id: String
    let title: String
    let artist: String?
    let datePeriod: String?
    let provenance: String?
    let sourceCredit: String?
    let imageName: String?  // SF Symbol or asset name for mock
    let wikidataLink: String?
}

// MARK: - Source
struct Source: Identifiable {
    let id: String
    let title: String
    let author: String?
    let url: String?
    let reliability: Reliability

    enum Reliability: String, Codable {
        case primary, scholarly, popular, traditional
    }
}

// MARK: - Route Pack
struct RoutePack: Identifiable {
    let id: String
    let title: String
    let subtitle: String
    let region: String
    let traditionTags: [Tradition]
    let stops: [RouteStop]
    let estimatedDistance: String
    let estimatedTime: String
    let isPremium: Bool
    let previewStopCount: Int  // how many stops free users can see
    let description: String

    var totalStops: Int { stops.count }
}

// MARK: - Route Stop
struct RouteStop: Identifiable {
    let id: String
    let locationID: String
    let order: Int
    let title: String
    let subtitle: String?
    let distanceFromPrevious: String?
    let directionNote: String?  // "Walk northeast along Via di San Giovanni"
}

// MARK: - Entitlement Tier
enum EntitlementTier: String, CaseIterable {
    case free
    case premium
    case pilgrim

    var canAccessFullAtlas: Bool { self != .free }
    var canAccessSources: Bool { self != .free }
    var canAccessArt: Bool { self != .free }
    var canSaveUnlimited: Bool { self != .free }
    var canAccessRoutePacks: Bool { self == .pilgrim }
    var canStartPilgrimage: Bool { self == .pilgrim }
    var canKeepPassport: Bool { self == .pilgrim }
    var canWriteFieldNotes: Bool { self == .pilgrim }
    var canAccessOffline: Bool { self == .pilgrim }
    var maxFreeSaves: Int { 5 }
    var maxFreeNearbyDetail: Int { 3 }
}

// MARK: - Map Style
enum AtlasMapStyle: String, CaseIterable {
    case atlas    // muted standard
    case satellite
    case hybrid

    var displayName: String {
        switch self {
        case .atlas: return L.mapStyleAtlas
        case .satellite: return L.mapStyleSatellite
        case .hybrid: return L.mapStyleHybrid
        }
    }
}

// MARK: - Journey Status
enum JourneyStatus: String, Codable {
    case active
    case paused
    case completed
    case abandoned
}

// MARK: - SwiftData Models
@Model
final class Journey {
    var id: UUID = UUID()
    var startDate: Date = Date()
    var endDate: Date?
    var routePackID: String?
    var routePackTitle: String?
    var statusRaw: String = JourneyStatus.active.rawValue
    var totalDistanceWalked: Double = 0.0

    @Relationship(deleteRule: .cascade)
    var visits: [Visit] = []

    @Relationship(deleteRule: .cascade)
    var notes: [FieldNote] = []

    var status: JourneyStatus {
        get { JourneyStatus(rawValue: statusRaw) ?? .active }
        set { statusRaw = newValue.rawValue }
    }

    init(
        routePackID: String? = nil,
        routePackTitle: String? = nil
    ) {
        self.id = UUID()
        self.startDate = Date()
        self.routePackID = routePackID
        self.routePackTitle = routePackTitle
    }
}

@Model
final class Visit {
    var id: UUID = UUID()
    var locationID: String = ""
    var placeName: String = ""
    var traditionRaw: String = Tradition.catholic.rawValue
    var arrivalDate: Date = Date()
    var noteText: String?
    var latitude: Double = 0
    var longitude: Double = 0

    var tradition: Tradition {
        get { Tradition(rawValue: traditionRaw) ?? .catholic }
        set { traditionRaw = newValue.rawValue }
    }

    var journey: Journey?

    init(
        locationID: String,
        placeName: String,
        tradition: Tradition = .catholic,
        latitude: Double = 0,
        longitude: Double = 0
    ) {
        self.id = UUID()
        self.locationID = locationID
        self.placeName = placeName
        self.traditionRaw = tradition.rawValue
        self.latitude = latitude
        self.longitude = longitude
        self.arrivalDate = Date()
    }
}

@Model
final class FieldNote {
    var id: UUID = UUID()
    var timestamp: Date = Date()
    var locationID: String?
    var locationName: String?
    var text: String = ""
    var hasPhoto: Bool = false

    var journey: Journey?

    init(text: String, locationID: String? = nil, locationName: String? = nil) {
        self.id = UUID()
        self.timestamp = Date()
        self.locationID = locationID
        self.locationName = locationName
        self.text = text
    }
}
File 3: L.swift
Swift

import Foundation

/// Localization abstraction for Anno Sacred Atlas.
/// In production, this wraps NSLocalizedString / String Catalogs.
/// For v0, provides English and Vietnamese chrome strings.

enum L {
    // MARK: - Tab & Navigation
    static let map = L.tr("map")
    static let today = L.tr("today")
    static let saved = L.tr("saved")
    static let nearby = L.tr("nearby")
    static let atlas = L.tr("atlas")

    // MARK: - Sacred Atlas
    static let sacredAtlas = L.tr("sacred_atlas")
    static let onThisGround = L.tr("on_this_ground")
    static let whyThisPlaceMatters = L.tr("why_this_place_matters")
    static let nearYouInSacredHistory = L.tr("near_you_in_sacred_history")
    static let sacredSitesNearYou = L.tr("sacred_sites_near_you")
    static let connectedToToday = L.tr("connected_to_today")
    static let sitesConnectedToToday = L.tr("sites_connected_to_today")

    // MARK: - Traditions
    static let all = L.tr("all")
    static let catholic = L.tr("catholic")
    static let orthodox = L.tr("orthodox")
    static let jewish = L.tr("jewish")
    static let islamic = L.tr("islamic")
    static let interfaith = L.tr("interfaith")

    // MARK: - Confidence
    static let confirmed = L.tr("confirmed")
    static let traditional = L.tr("traditional")
    static let disputed = L.tr("disputed")
    static let sources = L.tr("sources")
    static let sourceCount = L.tr("source_count")  // "%d Sources"

    // MARK: - Layers
    static let layers = L.tr("layers")
    static let todayLayer = L.tr("today_layer")
    static let saints = L.tr("saints")
    static let martyrs = L.tr("martyrs")
    static let councils = L.tr("councils")
    static let relics = L.tr("relics")
    static let marian = L.tr("marian")
    static let monasteries = L.tr("monasteries")
    static let biblical = L.tr("biblical")
    static let pilgrimage = L.tr("pilgrimage")

    // MARK: - Pilgrim Mode
    static let pilgrimMode = L.tr("pilgrim_mode")
    static let startPilgrimage = L.tr("start_pilgrimage")
    static let continueJourney = L.tr("continue_journey")
    static let endJourney = L.tr("end_journey")
    static let pauseJourney = L.tr("pause_journey")
    static let resumeJourney = L.tr("resume_journey")
    static let nextStop = L.tr("next_stop")
    static let visited = L.tr("visited")
    static let visitCount = L.tr("visit_count")  // "%d visited"
    static let fieldNotes = L.tr("field_notes")
    static let addNote = L.tr("add_note")
    static let journeyProgress = L.tr("journey_progress")

    // MARK: - Passport
    static let passport = L.tr("passport")
    static let stamps = L.tr("stamps")
    static let journeys = L.tr("journeys")
    static let routeCompleted = L.tr("route_completed")
    static let exportJourney = L.tr("export_journey")

    // MARK: - Route Packs
    static let routePacks = L.tr("route_packs")
    static let stops = L.tr("stops")
    static let stopCount = L.tr("stop_count")  // "%d stops"
    static let estimatedDistance = L.tr("estimated_distance")
    static let estimatedTime = L.tr("estimated_time")
    static let startRoute = L.tr("start_route")
    static let previewRoute = L.tr("preview_route")

    // MARK: - Actions
    static let save = L.tr("save")
    static let share = L.tr("share")
    static let directions = L.tr("directions")
    static let readMore = L.tr("read_more")
    static let unlock = L.tr("unlock")
    static let locateMe = L.tr("locate_me")
    static let close = L.tr("close")

    // MARK: - Premium
    static let unlockSacredAtlas = L.tr("unlock_sacred_atlas")
    static let unlockFullAtlas = L.tr("unlock_full_atlas")
    static let unlockPilgrimMode = L.tr("unlock_pilgrim_mode")
    static let exploreSites = L.tr("explore_sites")  // "Explore %d+ sacred sites"
    static let sitesAvailable = L.tr("sites_available")
    static let premium = L.tr("premium")
    static let pilgrim = L.tr("pilgrim")

    // MARK: - Map Style
    static let mapStyleAtlas = L.tr("map_style_atlas")
    static let mapStyleSatellite = L.tr("map_style_satellite")
    static let mapStyleHybrid = L.tr("map_style_hybrid")

    // MARK: - Location Permission
    static let enableLocation = L.tr("enable_location")
    static let locationExplanation = L.tr("location_explanation")
    static let exploreWithoutLocation = L.tr("explore_without_location")

    // MARK: - Events
    static let events = L.tr("events")
    static let associatedEvents = L.tr("associated_events")
    static let feastDay = L.tr("feast_day")
    static let art = L.tr("art")
    static let openHours = L.tr("open_hours")

    // MARK: - Implementation
    private static var languageOverride: String?

    static func setLanguage(_ code: String) {
        languageOverride = code
    }

    private static func tr(_ key: String) -> String {
        let lang = languageOverride ?? Locale.current.language.languageCode?.identifier ?? "en"
        return strings[key]?[lang] ?? strings[key]?["en"] ?? key.replacingOccurrences(of: "_", with: " ").capitalized
    }

    // String table: [key: [lang: value]]
    private static let strings: [String: [String: String]] = [
        "map": ["en": "Map", "vi": "Bản đồ"],
        "today": ["en": "Today", "vi": "Hôm nay"],
        "saved": ["en": "Saved", "vi": "Đã lưu"],
        "nearby": ["en": "Nearby", "vi": "Gần đây"],
        "atlas": ["en": "Atlas", "vi": "Bản đồ Thánh"],
        "sacred_atlas": ["en": "Sacred Atlas", "vi": "Bản đồ Thánh"],
        "on_this_ground": ["en": "On This Ground", "vi": "Trên Mảnh đất Này"],
        "why_this_place_matters": ["en": "Why This Place Matters", "vi": "Nơi Này Quan Trọng Thế Nào"],
        "near_you_in_sacred_history": ["en": "Near You in Sacred History", "vi": "Lịch Sử Thánh Gần Bạn"],
        "sacred_sites_near_you": ["en": "Sacred sites near you", "vi": "Địa điểm thánh gần bạn"],
        "connected_to_today": ["en": "Connected to today", "vi": "Liên kết hôm nay"],
        "sites_connected_to_today": ["en": "sites connected to today", "vi": "địa điểm liên kết hôm nay"],
        "all": ["en": "All", "vi": "Tất cả"],
        "catholic": ["en": "Catholic", "vi": "Công giáo"],
        "orthodox": ["en": "Orthodox", "vi": "Chính thống"],
        "jewish": ["en": "Jewish", "vi": "Do thái"],
        "islamic": ["en": "Islamic", "vi": "Hồi giáo"],
        "interfaith": ["en": "Interfaith", "vi": "Liên tôn"],
        "confirmed": ["en": "Confirmed", "vi": "Đã xác nhận"],
        "traditional": ["en": "Traditional", "vi": "Theo truyền thống"],
        "disputed": ["en": "Disputed", "vi": "Tranh chấp"],
        "sources": ["en": "Sources", "vi": "Nguồn"],
        "source_count": ["en": "Sources", "vi": "Nguồn"],
        "layers": ["en": "Layers", "vi": "Lớp"],
        "today_layer": ["en": "Today", "vi": "Hôm nay"],
        "saints": ["en": "Saints", "vi": "Thánh"],
        "martyrs": ["en": "Martyrs", "vi": "Tử đạo"],
        "councils": ["en": "Councils", "vi": "Công đồng"],
        "relics": ["en": "Relics", "vi": "Thánh tích"],
        "marian": ["en": "Marian", "vi": "Đức Mẹ"],
        "monasteries": ["en": "Monasteries", "vi": "Tu viện"],
        "biblical": ["en": "Biblical", "vi": "Kinh Thánh"],
        "pilgrimage": ["en": "Pilgrimage", "vi": "Hành hương"],
        "pilgrim_mode": ["en": "Pilgrim Mode", "vi": "Chế độ Hành hương"],
        "start_pilgrimage": ["en": "Start Pilgrimage", "vi": "Bắt đầu Hành hương"],
        "continue_journey": ["en": "Continue Journey", "vi": "Tiếp tục Hành trình"],
        "end_journey": ["en": "End Journey", "vi": "Kết thúc Hành trình"],
        "pause_journey": ["en": "Pause", "vi": "Tạm dừng"],
        "resume_journey": ["en": "Resume", "vi": "Tiếp tục"],
        "next_stop": ["en": "Next Stop", "vi": "Trạm tiếp theo"],
        "visited": ["en": "Visited", "vi": "Đã thăm"],
        "visit_count": ["en": "visited", "vi": "đã thăm"],
        "field_notes": ["en": "Field Notes", "vi": "Ghi chú"],
        "add_note": ["en": "Add Note", "vi": "Thêm ghi chú"],
        "journey_progress": ["en": "Journey Progress", "vi": "Tiến trình Hành trình"],
        "passport": ["en": "Passport", "vi": "Hộ chiếu"],
        "stamps": ["en": "Stamps", "vi": "Con dấu"],
        "journeys": ["en": "Journeys", "vi": "Hành trình"],
        "route_completed": ["en": "Route Completed", "vi": "Hoàn thành Lộ trình"],
        "export_journey": ["en": "Export Journey", "vi": "Xuất Hành trình"],
        "route_packs": ["en": "Route Packs", "vi": "Lộ trình"],
        "stops": ["en": "Stops", "vi": "Trạm"],
        "stop_count": ["en": "stops", "vi": "trạm"],
        "estimated_distance": ["en": "Distance", "vi": "Khoảng cách"],
        "estimated_time": ["en": "Time", "vi": "Thời gian"],
        "start_route": ["en": "Start Route", "vi": "Bắt đầu Lộ trình"],
        "preview_route": ["en": "Preview Route", "vi": "Xem trước Lộ trình"],
        "save": ["en": "Save", "vi": "Lưu"],
        "share": ["en": "Share", "vi": "Chia sẻ"],
        "directions": ["en": "Directions", "vi": "Chỉ đường"],
        "read_more": ["en": "Read More", "vi": "Đọc thêm"],
        "unlock": ["en": "Unlock", "vi": "Mở khóa"],
        "locate_me": ["en": "Locate Me", "vi": "Định vị"],
        "close": ["en": "Close", "vi": "Đóng"],
        "unlock_sacred_atlas": ["en": "Unlock the Sacred Atlas", "vi": "Mở khóa Bản đồ Thánh"],
        "unlock_full_atlas": ["en": "Unlock the Full Sacred Atlas", "vi": "Mở khóa Toàn bộ Bản đồ Thánh"],
        "unlock_pilgrim_mode": ["en": "Unlock Pilgrim Mode", "vi": "Mở khóa Chế độ Hành hương"],
        "explore_sites": ["en": "Explore sacred sites", "vi": "Khám phá địa điểm thánh"],
        "sites_available": ["en": "sites available", "vi": "địa điểm có sẵn"],
        "premium": ["en": "Premium", "vi": "Cao cấp"],
        "pilgrim": ["en": "Pilgrim", "vi": "Hành hương"],
        "map_style_atlas": ["en": "Atlas", "vi": "Bản đồ"],
        "map_style_satellite": ["en": "Satellite", "vi": "Vệ tinh"],
        "map_style_hybrid": ["en": "Hybrid", "vi": "Kết hợp"],
        "enable_location": ["en": "Enable Location", "vi": "Bật Định vị"],
        "location_explanation": ["en": "Anno uses your location to show nearby sacred sites. Your location is never uploaded or shared.", "vi": "Anno sử dụng vị trí để hiển thị địa điểm thánh gần bạn. Vị trí không bao giờ được tải lên hay chia sẻ."],
        "explore_without_location": ["en": "Explore Without Location", "vi": "Khám phá không Định vị"],
        "events": ["en": "Events", "vi": "Sự kiện"],
        "associated_events": ["en": "Associated Events", "vi": "Sự kiện Liên quan"],
        "feast_day": ["en": "Feast Day", "vi": "Lễ kính"],
        "art": ["en": "Art", "vi": "Nghệ thuật"],
        "open_hours": ["en": "Visiting Hours", "vi": "Giờ mở cửa"],
    ]
}
File 4: MockData.swift
Swift

import Foundation
import CoreLocation

/// Mock data for the Sacred Atlas feature.
/// In production, this would be replaced by a data repository backed
/// by local JSON/SQLite datasets and a content pipeline.

enum MockData {

    // MARK: - Locations

    static let locations: [SacredLocation] = [
        // Rome
        SacredLocation(
            id: "loc-mamertine",
            placeName: "Mamertine Prison",
            latitude: 41.8925, longitude: 12.4833,
            modernAddress: "Clivo Argentario 1, Rome",
            country: "Italy", region: "Lazio",
            traditions: [.catholic],
            categories: [.saints, .martyrs],
            confidence: .traditional,
            shortNarrative: "The ancient Roman prison where, according to tradition, Saints Peter and Paul were held before their martyrdom.",
            onThisGroundNarrative: "According to tradition, St. Peter was imprisoned here before his crucifixion, and St. Paul before his beheading. The site has been venerated since at least the 4th century.",
            associatedEventIDs: ["evt-peter-imprisoned", "evt-paul-mamertine"],
            artworkIDs: ["art-peter-crucifixion"],
            sourceIDs: ["src-butler", "src-cath-enc-mamertine"],
            visitingHours: "9:00–17:00 daily",
            routePackIDs: ["rp-seven-churches"],
            isTodayConnected: true
        ),
        SacredLocation(
            id: "loc-st-peters",
            placeName: "St. Peter's Basilica",
            latitude: 41.9022, longitude: 12.4539,
            modernAddress: "Piazza San Pietro, Vatican City",
            country: "Vatican City", region: "Vatican City",
            traditions: [.catholic],
            categories: [.saints, .relics, .pilgrimage],
            confidence: .confirmed,
            shortNarrative: "The largest church in the world, built over the tomb of St. Peter, the first pope and apostle of Christ.",
            onThisGroundNarrative: "Beneath this basilica lies the tomb of St. Peter, fisherman of Galilee and rock upon which Christ built His Church. Excavations confirmed the ancient burial site in the 1940s.",
            associatedEventIDs: ["evt-peter-martyrdom", "evt-vatican-ii"],
            artworkIDs: ["art-pieta"],
            sourceIDs: ["src-butler", "src-vatican-excavations"],
            visitingHours: "7:00–19:00 daily",
            routePackIDs: ["rp-seven-churches"],
            isTodayConnected: false
        ),
        SacredLocation(
            id: "loc-st-paul-otw",
            placeName: "Basilica of St. Paul Outside the Walls",
            latitude: 41.8869, longitude: 12.4736,
            modernAddress: "Via Ostiense 186, Rome",
            country: "Italy", region: "Lazio",
            traditions: [.catholic, .orthodox],
            categories: [.saints, .martyrs, .pilgrimage],
            confidence: .confirmed,
            shortNarrative: "Built over the burial place of St. Paul, this basilica has been a pilgrimage site since the time of Constantine.",
            onThisGroundNarrative: "The Apostle to the Gentiles was buried here after his beheading under Nero. The basilica has marked this place of burial since the 4th century.",
            associatedEventIDs: ["evt-paul-martyrdom"],
            artworkIDs: [],
            sourceIDs: ["src-butler", "src-cath-enc-paul"],
            visitingHours: "7:00–18:30 daily",
            routePackIDs: ["rp-seven-churches"],
            isTodayConnected: true
        ),
        SacredLocation(
            id: "loc-st-john-lateran",
            placeName: "St. John Lateran",
            latitude: 41.8854, longitude: 12.5060,
            modernAddress: "Piazza di S. Giovanni in Laterano 4, Rome",
            country: "Italy", region: "Lazio",
            traditions: [.catholic],
            categories: [.saints, .pilgrimage],
            confidence: .confirmed,
            shortNarrative: "The cathedral of Rome and mother church of the Catholic world. The pope's seat as Bishop of Rome.",
            onThisGroundNarrative: "This is the cathedral of the Bishop of Rome — the pope's own church. Constantine donated the land in the early 4th century, making it the oldest public church in the West.",
            associatedEventIDs: ["evt-lateran-dedication"],
            artworkIDs: [],
            sourceIDs: ["src-cath-enc-lateran"],
            visitingHours: "7:00–18:30 daily",
            routePackIDs: ["rp-seven-churches"],
            isTodayConnected: false
        ),
        SacredLocation(
            id: "loc-santa-maria-maggiore",
            placeName: "Santa Maria Maggiore",
            latitude: 41.8972, longitude: 12.4983,
            modernAddress: "Piazza di S. Maria Maggiore 42, Rome",
            country: "Italy", region: "Lazio",
            traditions: [.catholic],
            categories: [.marian, .relics, .pilgrimage],
            confidence: .confirmed,
            shortNarrative: "The largest Marian church in Rome, traditionally built after a miraculous summer snowfall in 352 AD.",
            onThisGroundNarrative: "According to tradition, the Virgin Mary appeared in a dream to Pope Liberius and a Roman patrician, requesting a church be built where snow would fall on the Esquiline Hill — in August. Snow fell, and the basilica rose.",
            associatedEventIDs: ["evt-maria-maggiore-snow"],
            artworkIDs: [],
            sourceIDs: ["src-butler"],
            visitingHours: "7:00–18:45 daily",
            routePackIDs: ["rp-seven-churches"],
            isTodayConnected: false
        ),
        SacredLocation(
            id: "loc-santa-croce",
            placeName: "Santa Croce in Gerusalemme",
            latitude: 41.8879, longitude: 12.5103,
            modernAddress: "Piazza di S. Croce in Gerusalemme 12, Rome",
            country: "Italy", region: "Lazio",
            traditions: [.catholic],
            categories: [.relics, .pilgrimage],
            confidence: .traditional,
            shortNarrative: "Houses relics of the Passion brought from Jerusalem by St. Helena, mother of Constantine, in the 4th century.",
            onThisGroundNarrative: "St. Helena, mother of the emperor Constantine, brought earth from Jerusalem and relics of Christ's Passion to this site. The church stands on ground that is, in a sense, Jerusalem itself — earth from the Holy Land laid on Roman soil.",
            associatedEventIDs: ["evt-helena-relics"],
            artworkIDs: [],
            sourceIDs: ["src-butler", "src-cath-enc-helena"],
            visitingHours: "7:00–12:45, 15:30–18:30",
            routePackIDs: ["rp-seven-churches"],
            isTodayConnected: false
        ),
        SacredLocation(
            id: "loc-san-lorenzo",
            placeName: "San Lorenzo Fuori le Mura",
            latitude: 41.8867, longitude: 12.5172,
            modernAddress: "Piazzale del Verano 3, Rome",
            country: "Italy", region: "Lazio",
            traditions: [.catholic],
            categories: [.saints, .martyrs],
            confidence: .confirmed,
            shortNarrative: "The shrine of St. Lawrence, the deacon martyred by roasting on a gridiron in 258 AD.",
            onThisGroundNarrative: "St. Lawrence, deacon of Rome, was martyred here in 258 AD. According to tradition, as he was burned on a gridiron, he told his executioners: 'Turn me over — this side is done.'",
            associatedEventIDs: ["evt-lawrence-martyrdom"],
            artworkIDs: [],
            sourceIDs: ["src-butler"],
            visitingHours: "7:00–12:00, 16:00–19:00",
            routePackIDs: ["rp-seven-churches"],
            isTodayConnected: false
        ),
        SacredLocation(
            id: "loc-catacombs-callixtus",
            placeName: "Catacombs of Callixtus",
            latitude: 41.8787, longitude: 12.5038,
            modernAddress: "Via Appia Antica 110, Rome",
            country: "Italy", region: "Lazio",
            traditions: [.catholic],
            categories: [.saints, .martyrs],
            confidence: .confirmed,
            shortNarrative: "The most important catacomb of early Christianity, containing the crypts of nine early popes and many martyrs.",
            onThisGroundNarrative: "In these underground passages, early Christians buried their dead, celebrated the Eucharist, and preserved the memory of martyrs. Nine popes of the 3rd century rest in its crypts.",
            associatedEventIDs: ["evt-callixtus-crypt"],
            artworkIDs: [],
            sourceIDs: ["src-cath-enc-catacombs"],
            visitingHours: "9:00–12:00, 14:00–17:00 (closed Wed)",
            routePackIDs: [],
            isTodayConnected: false
        ),

        // Jerusalem
        SacredLocation(
            id: "loc-holy-sepulchre",
            placeName: "Church of the Holy Sepulchre",
            latitude: 31.7787, longitude: 35.2296,
            modernAddress: "Christian Quarter Rd, Jerusalem",
            country: "Israel", region: "Jerusalem",
            traditions: [.catholic, .orthodox, .interfaith],
            categories: [.biblical, .saints, .pilgrimage],
            confidence: .confirmed,
            shortNarrative: "The site of Christ's crucifixion, burial, and resurrection. The most sacred place in Christianity.",
            onThisGroundNarrative: "Here, on this ground, Christ was crucified, buried, and rose from the dead. The site was identified by St. Helena in 326 AD and has been venerated continuously since.",
            associatedEventIDs: ["evt-crucifixion", "evt-resurrection", "evt-helena-sepulchre"],
            artworkIDs: [],
            sourceIDs: ["src-jerusalem-pilgrim", "src-butler"],
            visitingHours: "5:00–20:00 (varies by season)",
            routePackIDs: ["rp-passion-walk"],
            isTodayConnected: true
        ),
        SacredLocation(
            id: "loc-via-dolorosa",
            placeName: "Via Dolorosa",
            latitude: 31.7810, longitude: 35.2285,
            modernAddress: "Old City, Jerusalem",
            country: "Israel", region: "Jerusalem",
            traditions: [.catholic, .orthodox],
            categories: [.biblical, .pilgrimage],
            confidence: .traditional,
            shortNarrative: "The traditional path walked by Christ to Calvary, marked by the fourteen Stations of the Cross.",
            onThisGroundNarrative: "Along these stones, tradition holds that Christ carried His cross to Golgotha. Each station marks a moment of the Passion — a fall, a meeting, a word spoken.",
            associatedEventIDs: ["evt-stations-tradition"],
            artworkIDs: [],
            sourceIDs: ["src-jerusalem-pilgrim"],
            visitingHours: "Open street, accessible anytime",
            routePackIDs: ["rp-passion-walk"],
            isTodayConnected: false
        ),
        SacredLocation(
            id: "loc-gethsemane",
            placeName: "Garden of Gethsemane",
            latitude: 31.7783, longitude: 35.2412,
            modernAddress: "Jericho Rd, Jerusalem",
            country: "Israel", region: "Jerusalem",
            traditions: [.catholic, .orthodox, .interfaith],
            categories: [.biblical],
            confidence: .confirmed,
            shortNarrative: "Where Christ prayed in agony before His arrest. Ancient olive trees still stand here.",
            onThisGroundNarrative: "Here, on this ground, Christ prayed: 'Father, if it be possible, let this cup pass from me.' Some of the olive trees still living may date to the time of Christ.",
            associatedEventIDs: ["evt-gethsemane-prayer"],
            artworkIDs: [],
            sourceIDs: ["src-jerusalem-pilgrim"],
            visitingHours: "8:00–17:30",
            routePackIDs: ["rp-passion-walk"],
            isTodayConnected: false
        ),
        SacredLocation(
            id: "loc-western-wall",
            placeName: "Western Wall",
            latitude: 31.7767, longitude: 35.2343,
            modernAddress: "Jewish Quarter, Old City, Jerusalem",
            country: "Israel", region: "Jerusalem",
            traditions: [.jewish],
            categories: [.biblical, .pilgrimage],
            confidence: .confirmed,
            shortNarrative: "The last remaining wall of the Second Temple, the holiest site in Judaism.",
            onThisGroundNarrative: "This wall is all that remains of the Temple Mount platform built by Herod the Great. For two thousand years, Jews have prayed here — the closest place to the Holy of Holies.",
            associatedEventIDs: ["evt-temple-destruction"],
            artworkIDs: [],
            sourceIDs: ["src-jewish-heritage"],
            visitingHours: "24 hours",
            routePackIDs: [],
            isTodayConnected: false
        ),
        SacredLocation(
            id: "loc-temple-mount",
            placeName: "Temple Mount / Haram al-Sharif",
            latitude: 31.7790, longitude: 35.2354,
            modernAddress: "Old City, Jerusalem",
            country: "Israel", region: "Jerusalem",
            traditions: [.jewish, .islamic, .interfaith],
            categories: [.biblical, .pilgrimage],
            confidence: .confirmed,
            shortNarrative: "Sacred to Judaism, Christianity, and Islam. Site of the ancient Temples and the Dome of the Rock.",
            onThisGroundNarrative: "Abraham prepared to sacrifice Isaac here. Solomon built the First Temple here. Muhammad ascended to heaven from here. No other place on earth is sacred to so many.",
            associatedEventIDs: ["evt-temple-destruction", "evt-ascension-muhammad"],
            artworkIDs: [],
            sourceIDs: ["src-jewish-heritage", "src-islamic-heritage"],
            visitingHours: "Limited hours, check locally",
            routePackIDs: [],
            isTodayConnected: false
        ),
        SacredLocation(
            id: "loc-mount-zion",
            placeName: "Mount Zion",
            latitude: 31.7750, longitude: 35.2290,
            modernAddress: "Mount Zion, Jerusalem",
            country: "Israel", region: "Jerusalem",
            traditions: [.catholic, .jewish, .interfaith],
            categories: [.biblical],
            confidence: .traditional,
            shortNarrative: "Site of the Last Supper, Pentecost, and the Tomb of David — sacred to Jews and Christians alike.",
            onThisGroundNarrative: "Here Christ shared the Last Supper with His disciples. Here the Holy Spirit descended at Pentecost. Here King David is traditionally buried. A hill dense with sacred memory.",
            associatedEventIDs: ["evt-last-supper", "evt-pentecost"],
            artworkIDs: [],
            sourceIDs: ["src-jerusalem-pilgrim"],
            visitingHours: "Varies by site",
            routePackIDs: ["rp-passion-walk"],
            isTodayConnected: false
        ),

        // Other Sacred Sites
        SacredLocation(
            id: "loc-santiago",
            placeName: "Santiago de Compostela",
            latitude: 42.8806, longitude: -8.5447,
            modernAddress: "Praza do Obradoiro, Santiago de Compostela",
            country: "Spain", region: "Galicia",
            traditions: [.catholic],
            categories: [.saints, .pilgrimage],
            confidence: .traditional,
            shortNarrative: "The traditional burial place of St. James the Greater and destination of the Camino de Santiago.",
            onThisGroundNarrative: "According to tradition, the remains of St. James the Greater were brought here after his martyrdom in Jerusalem. The cathedral built over his tomb has drawn pilgrims for over a thousand years.",
            associatedEventIDs: ["evt-james-discovery"],
            artworkIDs: [],
            sourceIDs: ["src-butler", "src-camino-history"],
            visitingHours: "7:00–21:00",
            routePackIDs: ["rp-camino-sacred"],
            isTodayConnected: false
        ),
        SacredLocation(
            id: "loc-lourdes",
            placeName: "Lourdes",
            latitude: 43.0962, longitude: -0.0453,
            modernAddress: "1 Av. Mgr Théas, Lourdes",
            country: "France", region: "Occitanie",
            traditions: [.catholic],
            categories: [.marian, .pilgrimage],
            confidence: .confirmed,
            shortNarrative: "Where the Virgin Mary appeared to Bernadette Soubirous in 1858, now the most visited pilgrimage site in France.",
            onThisGroundNarrative: "On this ground, a young girl named Bernadette saw a lady in the grotto — a lady who said 'I am the Immaculate Conception.' The spring she uncovered has drawn millions seeking healing.",
            associatedEventIDs: ["evt-lourdes-apparition"],
            artworkIDs: [],
            sourceIDs: ["src-butler", "src-lourdes-official"],
            visitingHours: "Open daily",
            routePackIDs: ["rp-marian-europe"],
            isTodayConnected: false
        ),
        SacredLocation(
            id: "loc-fatima",
            placeName: "Fátima",
            latitude: 39.6179, longitude: -8.6733,
            modernAddress: "Fátima, Portugal",
            country: "Portugal", region: "Centro",
            traditions: [.catholic],
            categories: [.marian, .pilgrimage],
            confidence: .confirmed,
            shortNarrative: "Site of the Marian apparitions to three shepherd children in 1917, culminating in the Miracle of the Sun.",
            onThisGroundNarrative: "On May 13, 1917, three children — Lucia, Francisco, and Jacinta — saw a lady brighter than the sun. She appeared six times, asking for prayer and penance. On October 13, 70,000 witnesses saw the sun dance.",
            associatedEventIDs: ["evt-fatima-apparition"],
            artworkIDs: [],
            sourceIDs: ["src-butler", "src-fatima-official"],
            visitingHours: "Open daily",
            routePackIDs: ["rp-marian-europe"],
            isTodayConnected: true
        ),
        SacredLocation(
            id: "loc-assisi",
            placeName: "Assisi",
            latitude: 43.0707, longitude: 12.6043,
            modernAddress: "Piazza Santa Chiara, Assisi",
            country: "Italy", region: "Umbria",
            traditions: [.catholic],
            categories: [.saints, .monasteries, .pilgrimage],
            confidence: .confirmed,
            shortNarrative: "Birthplace of St. Francis and St. Clare, and home to the basilica containing the saint's tomb.",
            onThisGroundNarrative: "Here, Francis of Assisi stripped off his wealthy clothes and embraced Lady Poverty. Here, he received the stigmata on Mount La Verna. Here, Clare founded her order and lived in radical simplicity.",
            associatedEventIDs: ["evt-francis-stigmata", "evt-francis-death"],
            artworkIDs: ["art-giotto-francis"],
            sourceIDs: ["src-butler", "src-celano"],
            visitingHours: "6:30–19:00",
            routePackIDs: [],
            isTodayConnected: false
        ),
        SacredLocation(
            id: "loc-canterbury",
            placeName: "Canterbury Cathedral",
            latitude: 51.2797, longitude: 1.2603,
            modernAddress: "Cathedral House, 11 The Precincts, Canterbury",
            country: "England", region: "Kent",
            traditions: [.catholic, .orthodox],
            categories: [.saints, .martyrs, .pilgrimage],
            confidence: .confirmed,
            shortNarrative: "Site of St. Thomas Becket's martyrdom in 1170 and destination of the Canterbury pilgrimage since medieval times.",
            onThisGroundNarrative: "On December 29, 1170, four knights of King Henry II struck down Archbishop Thomas Becket in his own cathedral. His martyrdom made Canterbury one of the great pilgrimage destinations of Christendom.",
            associatedEventIDs: ["evt-becket-martyrdom"],
            artworkIDs: [],
            sourceIDs: ["src-butler"],
            visitingHours: "9:00–17:00 Mon–Sat, 12:30–14:30 Sun",
            routePackIDs: ["rp-canterbury-walk"],
            isTodayConnected: false
        ),
        SacredLocation(
            id: "loc-mount-sinai",
            placeName: "Mount Sinai",
            latitude: 28.5564, longitude: 33.9756,
            modernAddress: "Saint Katherine, South Sinai",
            country: "Egypt", region: "South Sinai",
            traditions: [.catholic, .orthodox, .jewish, .islamic, .interfaith],
            categories: [.biblical, .monasteries, .pilgrimage],
            confidence: .traditional,
            shortNarrative: "Where Moses received the Ten Commandments. Site of the ancient Monastery of St. Catherine.",
            onThisGroundNarrative: "According to tradition, this is the mountain where Moses encountered the burning bush and received the Law. At its foot stands the Monastery of St. Catherine, continuously inhabited since the 6th century.",
            associatedEventIDs: ["evt-moses-tablets"],
            artworkIDs: [],
            sourceIDs: ["src-sinai-tradition"],
            visitingHours: "Monastery: 9:00–12:00 (Fri–Sun closed)",
            routePackIDs: [],
            isTodayConnected: false
        ),
    ]

    // MARK: - Events

    static let events: [HistoricalEvent] = [
        HistoricalEvent(
            id: "evt-peter-imprisoned",
            dateDescription: "c. 64 AD",
            title: "St. Peter Imprisoned at the Mamertine",
            shortNarrative: "Before his crucifixion on Vatican Hill, Peter was held in the Tullianum — the lower chamber of the Mamertine Prison — according to tradition.",
            tradition: .catholic, liturgicalColor: "red",
            locationID: "loc-mamertine",
            artworkID: nil,
            sourceIDs: ["src-butler"],
            confidence: .traditional,
            gregorianMonth: 6, gregorianDay: 29
        ),
        HistoricalEvent(
            id: "evt-paul-mamertine",
            dateDescription: "c. 67 AD",
            title: "St. Paul Imprisoned Before Beheading",
            shortNarrative: "St. Paul was held here before his execution by beheading on the Ostian Way, during the persecution under Nero.",
            tradition: .catholic, liturgicalColor: "red",
            locationID: "loc-mamertine",
            artworkID: nil,
            sourceIDs: ["src-butler"],
            confidence: .traditional,
            gregorianMonth: 6, gregorianDay: 30
        ),
        HistoricalEvent(
            id: "evt-peter-martyrdom",
            dateDescription: "c. 64 AD",
            title: "Martyrdom of St. Peter",
            shortNarrative: "St. Peter was crucified upside down on Vatican Hill at his own request, deeming himself unworthy to die in the same manner as Christ.",
            tradition: .catholic, liturgicalColor: "red",
            locationID: "loc-st-peters",
            artworkID: "art-pieta",
            sourceIDs: ["src-butler", "src-vatican-excavations"],
            confidence: .traditional,
            gregorianMonth: 6, gregorianDay: 29
        ),
        HistoricalEvent(
            id: "evt-paul-martyrdom",
            dateDescription: "c. 67 AD",
            title: "Martyrdom of St. Paul",
            shortNarrative: "St. Paul was beheaded on the Ostian Way outside Rome's walls, as was the right of a Roman citizen.",
            tradition: .catholic, liturgicalColor: "red",
            locationID: "loc-st-paul-otw",
            artworkID: nil,
            sourceIDs: ["src-butler"],
            confidence: .traditional,
            gregorianMonth: 6, gregorianDay: 30
        ),
        HistoricalEvent(
            id: "evt-lateran-dedication",
            dateDescription: "Nov 9, 324 AD",
            title: "Dedication of the Lateran Basilica",
            shortNarrative: "The cathedral of Rome, dedicated to Christ the Savior, was consecrated by Pope Sylvester I. It remains the mother church of all churches.",
            tradition: .catholic, liturgicalColor: "white",
            locationID: "loc-st-john-lateran",
            artworkID: nil,
            sourceIDs: ["src-cath-enc-lateran"],
            confidence: .confirmed,
            gregorianMonth: 11, gregorianDay: 9
        ),
        HistoricalEvent(
            id: "evt-lawrence-martyrdom",
            dateDescription: "Aug 10, 258 AD",
            title: "Martyrdom of St. Lawrence",
            shortNarrative: "The deacon Lawrence was roasted on a gridiron during the persecution of Valerian. 'Turn me over,' he said, 'I am done on this side.'",
            tradition: .catholic, liturgicalColor: "red",
            locationID: "loc-san-lorenzo",
            artworkID: nil,
            sourceIDs: ["src-butler"],
            confidence: .traditional,
            gregorianMonth: 8, gregorianDay: 10
        ),
        HistoricalEvent(
            id: "evt-crucifixion",
            dateDescription: "c. 30–33 AD",
            title: "The Crucifixion of Christ",
            shortNarrative: "Jesus of Nazareth was crucified at Golgotha, outside the walls of Jerusalem, under Pontius Pilate.",
            tradition: .catholic, liturgicalColor: "red",
            locationID: "loc-holy-sepulchre",
            artworkID: nil,
            sourceIDs: ["src-jerusalem-pilgrim"],
            confidence: .confirmed,
            gregorianMonth: nil, gregorianDay: nil  // moves with Easter
        ),
        HistoricalEvent(
            id: "evt-resurrection",
            dateDescription: "c. 30–33 AD",
            title: "The Resurrection",
            shortNarrative: "On the third day after the Crucifixion, Christ rose from the dead. The empty tomb was found by the women who came to anoint His body.",
            tradition: .catholic, liturgicalColor: "white",
            locationID: "loc-holy-sepulchre",
            artworkID: nil,
            sourceIDs: ["src-jerusalem-pilgrim"],
            confidence: .confirmed,
            gregorianMonth: nil, gregorianDay: nil
        ),
        HistoricalEvent(
            id: "evt-helena-sepulchre",
            dateDescription: "326 AD",
            title: "St. Helena Discovers the True Cross",
            shortNarrative: "St. Helena, mother of Constantine, identified the site of Golgotha and the tomb of Christ, and is said to have discovered the True Cross.",
            tradition: .catholic, liturgicalColor: "white",
            locationID: "loc-holy-sepulchre",
            artworkID: nil,
            sourceIDs: ["src-butler"],
            confidence: .traditional,
            gregorianMonth: 9, gregorianDay: 14
        ),
        HistoricalEvent(
            id: "evt-gethsemane-prayer",
            dateDescription: "c. 30–33 AD",
            title: "Christ Prays in Gethsemane",
            shortNarrative: "On the night before His Passion, Christ prayed in agony: 'Father, if it be possible, let this cup pass from me. Nevertheless, not as I will, but as You will.'",
            tradition: .catholic, liturgicalColor: "green",
            locationID: "loc-gethsemane",
            artworkID: nil,
            sourceIDs: ["src-jerusalem-pilgrim"],
            confidence: .confirmed,
            gregorianMonth: nil, gregorianDay: nil
        ),
        HistoricalEvent(
            id: "evt-lourdes-apparition",
            dateDescription: "Feb 11, 1858",
            title: "First Apparition at Lourdes",
            shortNarrative: "Bernadette Soubirous saw a lady in the grotto of Massabielle — the first of eighteen apparitions of the Virgin Mary at Lourdes.",
            tradition: .catholic, liturgicalColor: "white",
            locationID: "loc-lourdes",
            artworkID: nil,
            sourceIDs: ["src-butler", "src-lourdes-official"],
            confidence: .confirmed,
            gregorianMonth: 2, gregorianDay: 11
        ),
        HistoricalEvent(
            id: "evt-fatima-apparition",
            dateDescription: "May 13, 1917",
            title: "First Apparition at Fátima",
            shortNarrative: "Three shepherd children — Lucia, Francisco, and Jacinta — saw a lady brighter than the sun near the holm oak tree at Cova da Iria.",
            tradition: .catholic, liturgicalColor: "white",
            locationID: "loc-fatima",
            artworkID: nil,
            sourceIDs: ["src-butler", "src-fatima-official"],
            confidence: .confirmed,
            gregorianMonth: 5, gregorianDay: 13
        ),
        HistoricalEvent(
            id: "evt-francis-stigmata",
            dateDescription: "Sep 17, 1224",
            title: "St. Francis Receives the Stigmata",
            shortNarrative: "While praying on Mount La Verna, Francis received the wounds of Christ — the first recorded case of stigmata.",
            tradition: .catholic, liturgicalColor: "white",
            locationID: "loc-assisi",
            artworkID: "art-giotto-francis",
            sourceIDs: ["src-butler", "src-celano"],
            confidence: .confirmed,
            gregorianMonth: 9, gregorianDay: 17
        ),
        HistoricalEvent(
            id: "evt-becket-martyrdom",
            dateDescription: "Dec 29, 1170",
            title: "Martyrdom of St. Thomas Becket",
            shortNarrative: "Archbishop Thomas Becket was murdered in Canterbury Cathedral by four knights of King Henry II.",
            tradition: .catholic, liturgicalColor: "red",
            locationID: "loc-canterbury",
            artworkID: nil,
            sourceIDs: ["src-butler"],
            confidence: .confirmed,
            gregorianMonth: 12, gregorianDay: 29
        ),
        HistoricalEvent(
            id: "evt-james-discovery",
            dateDescription: "c. 814 AD",
            title: "Discovery of the Tomb of St. James",
            shortNarrative: "A hermit named Pelagius saw strange lights over a field, leading to the discovery of the tomb of St. James the Greater at Compostela.",
            tradition: .catholic, liturgicalColor: "white",
            locationID: "loc-santiago",
            artworkID: nil,
            sourceIDs: ["src-camino-history"],
            confidence: .traditional,
            gregorianMonth: 7, gregorianDay: 25
        ),
        HistoricalEvent(
            id: "evt-temple-destruction",
            dateDescription: "Aug 5, 70 AD / Aug 4, 586 BC",
            title: "Destruction of the Temple",
            shortNarrative: "Both the First Temple (586 BC) and the Second Temple (70 AD) were destroyed — the latter by Rome, leaving only the Western Wall.",
            tradition: .jewish, liturgicalColor: nil,
            locationID: "loc-western-wall",
            artworkID: nil,
            sourceIDs: ["src-jewish-heritage"],
            confidence: .confirmed,
            gregorianMonth: nil, gregorianDay: nil
        ),
    ]

    // MARK: - Artworks

    static let artworks: [Artwork] = [
        Artwork(
            id: "art-pieta",
            title: "Pietà",
            artist: "Michelangelo Buonarroti",
            datePeriod: "1498–1499",
            provenance: "St. Peter's Basilica, Vatican City",
            sourceCredit: "Vatican Museums",
            imageName: "cross.case",
            wikidataLink: nil
        ),
        Artwork(
            id: "art-giotto-francis",
            title: "St. Francis Receiving the Stigmata",
            artist: "Giotto di Bondone",
            datePeriod: "c. 1295–1300",
            provenance: "Musée du Louvre, Paris",
            sourceCredit: "Louvre Museum",
            imageName: "paintbrush",
            wikidataLink: nil
        ),
    ]

    // MARK: - Sources

    static let sources: [Source] = [
        Source(id: "src-butler", title: "Butler's Lives of the Saints", author: "Alban Butler", url: nil, reliability: .traditional),
        Source(id: "src-cath-enc-mamertine", title: "Catholic Encyclopedia: Mamertine Prison", author: "Catholic Encyclopedia (1913)", url: nil, reliability: .scholarly),
        Source(id: "src-cath-enc-paul", title: "Catholic Encyclopedia: St. Paul", author: "Catholic Encyclopedia (1911)", url: nil, reliability: .scholarly),
        Source(id: "src-cath-enc-lateran", title: "Catholic Encyclopedia: Lateran Basilica", author: "Catholic Encyclopedia (1910)", url: nil, reliability: .scholarly),
        Source(id: "src-cath-enc-helena", title: "Catholic Encyclopedia: St. Helena", author: "Catholic Encyclopedia (1910)", url: nil, reliability: .scholarly),
        Source(id: "src-cath-enc-catacombs", title: "Catholic Encyclopedia: Roman Catacombs", author: "Catholic Encyclopedia (1908)", url: nil, reliability: .scholarly),
        Source(id: "src-vatican-excavations", title: "The Tomb of St. Peter", author: "Margherita Guarducci", url: nil, reliability: .scholarly),
        Source(id: "src-jerusalem-pilgrim", title: "Jerusalem: A Pilgrim's Companion", author: "Various", url: nil, reliability: .traditional),
        Source(id: "src-jewish-heritage", title: "Jewish Heritage in Jerusalem", author: "Israel Antiquities Authority", url: nil, reliability: .scholarly),
        Source(id: "src-islamic-heritage", title: "Islamic Heritage of Jerusalem", author: "Various", url: nil, reliability: .scholarly),
        Source(id: "src-lourdes-official", title: "Sanctuary of Our Lady of Lourdes: Official Guide", author: "Sanctuary of Lourdes", url: nil, reliability: .primary),
        Source(id: "src-fatima-official", title: "Sanctuary of Fátima: Official Documentation", author: "Sanctuary of Fátima", url: nil, reliability: .primary),
        Source(id: "src-celano", title: "First Life of St. Francis", author: "Thomas of Celano", url: nil, reliability: .primary),
        Source(id: "src-camino-history", title: "The Camino: A History of Pilgrimage", author: "Various", url: nil, reliability: .scholarly),
        Source(id: "src-sinai-tradition", title: "Sinai: A Pilgrimage Through History", author: "Various", url: nil, reliability: .traditional),
    ]

    // MARK: - Route Packs

    static let routePacks: [RoutePack] = [
        RoutePack(
            id: "rp-seven-churches",
            title: "Seven Churches of Rome",
            subtitle: "The ancient pilgrimage of the seven station churches",
            region: "Rome, Italy",
            traditionTags: [.catholic],
            stops: [
                RouteStop(id: "rs-1", locationID: "loc-st-john-lateran", order: 1, title: "St. John Lateran", subtitle: "Mother Church of Christendom", distanceFromPrevious: nil, directionNote: "Begin at the cathedral of Rome"),
                RouteStop(id: "rs-2", locationID: "loc-st-peters", order: 2, title: "St. Peter's Basilica", subtitle: "Tomb of the Apostle", distanceFromPrevious: "4.2 km", directionNote: "Walk west along Via della Conciliazione"),
                RouteStop(id: "rs-3", locationID: "loc-st-paul-otw", order: 3, title: "St. Paul Outside the Walls", subtitle: "Tomb of the Apostle to the Gentiles", distanceFromPrevious: "3.8 km", directionNote: "Continue south on Via Ostiense"),
                RouteStop(id: "rs-4", locationID: "loc-santa-maria-maggiore", order: 4, title: "Santa Maria Maggiore", subtitle: "Our Lady of the Snows", distanceFromPrevious: "5.1 km", directionNote: "Walk northeast to the Esquiline Hill"),
                RouteStop(id: "rs-5", locationID: "loc-santa-croce", order: 5, title: "Santa Croce in Gerusalemme", subtitle: "Relics of the Passion", distanceFromPrevious: "1.4 km", directionNote: "Walk southeast along Via di Santa Croce"),
                RouteStop(id: "rs-6", locationID: "loc-san-lorenzo", order: 6, title: "San Lorenzo Fuori le Mura", subtitle: "Shrine of the Martyr Deacon", distanceFromPrevious: "0.8 km", directionNote: "Walk northeast to Verano"),
                RouteStop(id: "rs-7", locationID: "loc-catacombs-callixtus", order: 7, title: "Catacombs of Callixtus", subtitle: "Crypts of the Early Popes", distanceFromPrevious: "3.5 km", directionNote: "Walk south on Via Appia Antica"),
            ],
            estimatedDistance: "11.8 mi (19 km)",
            estimatedTime: "5–7 hours",
            isPremium: true,
            previewStopCount: 2,
            description: "The traditional seven-church pilgrimage of Rome, walked by pilgrims since the early centuries of Christianity. Visit the major basilicas and catacombs, tracing the lives and deaths of the apostles and martyrs who founded the Church in the Eternal City."
        ),
        RoutePack(
            id: "rp-passion-walk",
            title: "Jerusalem: Passion Walk",
            subtitle: "Follow the final hours of Christ through the Holy City",
            region: "Jerusalem, Israel",
            traditionTags: [.catholic, .orthodox],
            stops: [
                RouteStop(id: "rs-pw1", locationID: "loc-gethsemane", order: 1, title: "Garden of Gethsemane", subtitle: "Where Christ prayed in agony", distanceFromPrevious: nil, directionNote: "Begin at the foot of the Mount of Olives"),
                RouteStop(id: "rs-pw2", locationID: "loc-via-dolorosa", order: 2, title: "Via Dolorosa", subtitle: "The Way of the Cross", distanceFromPrevious: "1.0 km", directionNote: "Enter the Old City through St. Stephen's Gate"),
                RouteStop(id: "rs-pw3", locationID: "loc-holy-sepulchre", order: 3, title: "Church of the Holy Sepulchre", subtitle: "Calvary and the Empty Tomb", distanceFromPrevious: "0.5 km", directionNote: "End at the most sacred place in Christendom"),
                RouteStop(id: "rs-pw4", locationID: "loc-mount-zion", order: 4, title: "Mount Zion", subtitle: "Upper Room and Pentecost", distanceFromPrevious: "0.8 km", directionNote: "Walk south to the Upper Room"),
            ],
            estimatedDistance: "1.5 mi (2.4 km)",
            estimatedTime: "2–3 hours",
            isPremium: true,
            previewStopCount: 2,
            description: "Walk the path of Christ's Passion through the streets of Jerusalem, from the Garden of Gethsemane to Calvary and the Empty Tomb. A journey through the most consequential hours in human history."
        ),
        RoutePack(
            id: "rp-marian-europe",
            title: "Marian Apparitions of Europe",
            subtitle: "Sites where the Virgin Mary has appeared",
            region: "France, Portugal",
            traditionTags: [.catholic],
            stops: [
                RouteStop(id: "rs-ma1", locationID: "loc-lourdes", order: 1, title: "Lourdes", subtitle: "Our Lady of Lourdes, 1858", distanceFromPrevious: nil, directionNote: nil),
                RouteStop(id: "rs-ma2", locationID: "loc-fatima", order: 2, title: "Fátima", subtitle: "Our Lady of Fátima, 1917", distanceFromPrevious: "~1,200 km", directionNote: "Multi-city pilgrimage; plan travel between stops"),
            ],
            estimatedDistance: "Multi-city",
            estimatedTime: "3–5 days travel",
            isPremium: true,
            previewStopCount: 1,
            description: "Visit the most significant Marian apparition sites in Europe. From Lourdes to Fátima, these are the places where the Virgin Mary appeared and the messages she brought to the world."
        ),
        RoutePack(
            id: "rp-canterbury-walk",
            title: "Canterbury Pilgrim Walk",
            subtitle: "In the footsteps of medieval pilgrims",
            region: "Canterbury, England",
            traditionTags: [.catholic, .orthodox],
            stops: [
                RouteStop(id: "rs-cw1", locationID: "loc-canterbury", order: 1, title: "Canterbury Cathedral", subtitle: "Martyrdom of St. Thomas Becket", distanceFromPrevious: nil, directionNote: "Enter through the Christ Church Gate"),
            ],
            estimatedDistance: "0.5 mi within cathedral precincts",
            estimatedTime: "1–2 hours",
            isPremium: true,
            previewStopCount: 1,
            description: "Explore the cathedral where Archbishop Thomas Becket was martyred in 1170 — an event that made Canterbury one of the greatest pilgrimage destinations in Christendom."
        ),
    ]

    // MARK: - Helpers

    static func location(by id: String) -> SacredLocation? {
        locations.first { $0.id == id }
    }

    static func events(for locationID: String) -> [HistoricalEvent] {
        events.filter { $0.locationID == locationID }
    }

    static func artwork(by id: String) -> Artwork? {
        artworks.first { $0.id == id }
    }

    static func source(by id: String) -> Source? {
        sources.first { $0.id == id }
    }

    static func sources(for ids: [String]) -> [Source] {
        ids.compactMap { source(by: $0) }
    }

    static func routePack(by id: String) -> RoutePack? {
        routePacks.first { $0.id == id }
    }

    static func routePacks(for locationID: String) -> [RoutePack] {
        routePacks.filter { pack in
            pack.stops.contains { $0.locationID == locationID }
        }
    }

    /// Total site count for premium messaging
    static let totalSiteCount = 2400  // mock; represents full atlas size

    /// How many sites are "near" in mock (for free tier preview)
    static let nearbySiteCount = 12

    /// Sites connected to today's date (mock)
    static let todayConnectedCount = 3
}
File 5: Services.swift
Swift

import Foundation
import CoreLocation
import Observation

// MARK: - Entitlement Service
/// Mock entitlement state. In production, this wraps StoreKit / RevenueCat / server validation.

@Observable
final class EntitlementService {
    var currentTier: EntitlementTier = .free

    static let shared = EntitlementService()

    private init() {}

    /// Whether the user can access full detail for a given location
    func canAccessDetail(for location: SacredLocation) -> Bool {
        if currentTier.canAccessFullAtlas { return true }
        // Free users: today's connected pin + limited nearby
        if location.isTodayConnected { return true }
        return false
    }

    /// Whether the user can access a route pack
    func canAccessRoutePack(_ pack: RoutePack) -> Bool {
        if !pack.isPremium { return true }
        return currentTier.canAccessRoutePacks
    }

    /// How many stops of a route pack a free user can preview
    func previewStopCount(for pack: RoutePack) -> Int {
        if currentTier.canAccessRoutePacks { return pack.totalStops }
        return pack.previewStopCount
    }

    /// Number of nearby sites a free user can see in detail
    var maxFreeNearbyDetail: Int {
        currentTier.maxFreeNearbyDetail
    }
}

// MARK: - Location Service
/// Manages GPS permissions and user location.
/// Designed for testability: can be mocked without actual CLLocationManager.

@Observable
final class LocationService: NSObject, CLLocationManagerDelegate {
    var authorizationStatus: CLAuthorizationStatus = .notDetermined
    var userLocation: CLLocation?
    var isLocationAvailable: Bool { authorizationStatus == .authorizedWhenInUse || authorizationStatus == .authorizedAlways }

    private let manager = CLLocationManager()

    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyHundredMeters
    }

    func requestPermission() {
        manager.requestWhenInUseAuthorization()
    }

    func startUpdating() {
        guard isLocationAvailable else { return }
        manager.startUpdatingLocation()
    }

    func stopUpdating() {
        manager.stopUpdatingLocation()
    }

    // CLLocationManagerDelegate
    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        authorizationStatus = status
        if isLocationAvailable {
            startUpdating()
        }
    }

    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        userLocation = locations.last
    }

    // MARK: - Distance Calculation
    func distance(to location: SacredLocation) -> CLLocationDistance? {
        guard let userLocation else { return nil }
        let target = CLLocation(latitude: location.latitude, longitude: location.longitude)
        return userLocation.distance(from: target)
    }

    func isNearSite(_ location: SacredLocation, threshold: CLLocationDistance = 100) -> Bool {
        guard let distance = distance(to: location) else { return false }
        return distance <= threshold
    }
}

// MARK: - Mock Location Service (for previews)
@Observable
final class MockLocationService {
    var authorizationStatus: CLAuthorizationStatus = .authorizedWhenInUse
    var userLocation: CLLocation? = CLLocation(latitude: 41.9028, longitude: 12.4964)  // Rome
    var isLocationAvailable: Bool { authorizationStatus == .authorizedWhenInUse || authorizationStatus == .authorizedAlways }

    func distance(to location: SacredLocation) -> CLLocationDistance? {
        guard let userLocation else { return nil }
        let target = CLLocation(latitude: location.latitude, longitude: location.longitude)
        return userLocation.distance(from: target)
    }

    func isNearSite(_ location: SacredLocation, threshold: CLLocationDistance = 100) -> Bool {
        guard let distance = distance(to: location) else { return false }
        return distance <= threshold
    }
}

// MARK: - Pilgrimage Service
/// Manages active journey state and SwiftData persistence.

@Observable
final class PilgrimageService {
    var activeJourney: Journey?
    var isPilgrimModeActive: Bool { activeJourney?.status == .active }

    func startJourney(routePackID: String? = nil, routePackTitle: String? = nil, context: ModelContext?) {
        let journey = Journey(routePackID: routePackID, routePackTitle: routePackTitle)
        activeJourney = journey
        context?.insert(journey)
        try? context?.save()
    }

    func pauseJourney(context: ModelContext?) {
        activeJourney?.statusRaw = JourneyStatus.paused.rawValue
        try? context?.save()
    }

    func resumeJourney(context: ModelContext?) {
        activeJourney?.statusRaw = JourneyStatus.active.rawValue
        try? context?.save()
    }

    func endJourney(context: ModelContext?) {
        activeJourney?.statusRaw = JourneyStatus.completed.rawValue
        activeJourney?.endDate = Date()
        try? context?.save()
        activeJourney = nil
    }

    func recordVisit(location: SacredLocation, note: String? = nil, context: ModelContext?) {
        guard let journey = activeJourney else { return }
        let visit = Visit(
            locationID: location.id,
            placeName: location.placeName,
            tradition: location.traditions.first ?? .catholic,
            latitude: location.latitude,
            longitude: location.longitude
        )
        visit.noteText = note
        visit.journey = journey
        journey.visits.append(visit)
        context?.insert(visit)
        try? context?.save()
    }

    func addFieldNote(text: String, locationID: String? = nil, locationName: String? = nil, context: ModelContext?) {
        guard let journey = activeJourney else { return }
        let note = FieldNote(text: text, locationID: locationID, locationName: locationName)
        note.journey = journey
        journey.notes.append(note)
        context?.insert(note)
        try? context?.save()
    }

    func hasVisited(locationID: String) -> Bool {
        activeJourney?.visits.contains { $0.locationID == locationID } ?? false
    }
}
File 6: ViewModels.swift
Swift

import Foundation
import CoreLocation
import MapKit
import Observation

// MARK: - Sacred Atlas ViewModel

@Observable
final class SacredAtlasViewModel {
    // MARK: State
    var filteredLocations: [SacredLocation] = []
    var selectedLocation: SacredLocation?
    var searchText: String = ""

    // Filters
    var selectedTradition: Tradition? = nil
    var selectedConfidence: ConfidenceLabel? = nil
    var selectedLayer: SacredLayer? = nil
    var activeLayers: Set<SacredLayer> = [.today]

    // Map state
    var cameraPosition: MapCameraPosition = .automatic
    var mapStyle: AtlasMapStyle = .atlas

    // UI state
    var showLocationDetail: Bool = false
    var showRoutePacks: Bool = false
    var showPassport: Bool = false
    var showPilgrimMode: Bool = false
    var showLayers: Bool = false
    var showLocationPermission: Bool = false
    var showPremiumUnlock: Bool = false
    var showNearbyCard: Bool = true

    // Services
    let entitlement: EntitlementService
    let locationService: LocationService

    // MARK: Init
    init(
        entitlement: EntitlementService = .shared,
        locationService: LocationService = LocationService()
    ) {
        self.entitlement = entitlement
        self.locationService = locationService
        applyFilters()
    }

    // MARK: Filtering
    func applyFilters() {
        var results = MockData.locations

        // Tradition filter
        if let tradition = selectedTradition {
            results = results.filter { $0.traditions.contains(tradition) }
        }

        // Confidence filter
        if let confidence = selectedConfidence {
            results = results.filter { $0.confidence == confidence }
        }

        // Layer filter
        if let layer = selectedLayer {
            if layer == .today {
                results = results.filter { $0.isTodayConnected }
            } else if let category = layer.category {
                results = results.filter { $0.categories.contains(category) }
            }
        }

        // Search
        if !searchText.isEmpty {
            results = results.filter {
                $0.placeName.localizedCaseInsensitiveContains(searchText) ||
                $0.region.localizedCaseInsensitiveContains(searchText) ||
                $0.country.localizedCaseInsensitiveContains(searchText)
            }
        }

        filteredLocations = results
    }

    func toggleTradition(_ tradition: Tradition) {
        if selectedTradition == tradition {
            selectedTradition = nil
        } else {
            selectedTradition = tradition
        }
        applyFilters()
    }

    func toggleConfidence(_ confidence: ConfidenceLabel) {
        if selectedConfidence == confidence {
            selectedConfidence = nil
        } else {
            selectedConfidence = confidence
        }
        applyFilters()
    }

    func selectLayer(_ layer: SacredLayer?) {
        selectedLayer = layer
        applyFilters()
    }

    // MARK: Location Selection
    func selectLocation(_ location: SacredLocation) {
        selectedLocation = location
        withAnimation(.easeInOut(duration: 0.3)) {
            showLocationDetail = true
        }
    }

    func deselectLocation() {
        selectedLocation = nil
        withAnimation(.easeInOut(duration: 0.2)) {
            showLocationDetail = false
        }
    }

    // MARK: Nearby
    var nearbyLocations: [(location: SacredLocation, distance: CLLocationDistance)] {
        guard locationService.isLocationAvailable else { return [] }
        return MockData.locations.compactMap { loc in
            guard let dist = locationService.distance(to: loc) else { return nil }
            return (loc, dist)
        }
        .sorted { $0.distance < $1.distance }
    }

    var nearbySummary: String {
        let count = nearbyLocations.count
        let todayCount = nearbyLocations.filter { $0.location.isTodayConnected }.count
        return "\(count) \(L.sacredSitesNearYou), \(todayCount) \(L.sitesConnectedToToday)"
    }

    // MARK: Premium Checks
    func isLocationLocked(_ location: SacredLocation) -> Bool {
        !entitlement.canAccessDetail(for: location)
    }

    func canAccessRoutePack(_ pack: RoutePack) -> Bool {
        entitlement.canAccessRoutePack(pack)
    }

    // MARK: Camera
    func moveToLocation(_ location: SacredLocation) {
        withAnimation {
            cameraPosition = .region(
                MKCoordinateRegion(
                    center: location.coordinate,
                    span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01)
                )
            )
        }
    }

    func moveToUser() {
        withAnimation {
            cameraPosition = .userLocation(fallback: .automatic)
        }
    }

    func moveToWorld() {
        withAnimation {
            cameraPosition = .region(
                MKCoordinateRegion(
                    center: CLLocationCoordinate2D(latitude: 41.9, longitude: 12.5),
                    span: MKCoordinateSpan(latitudeDelta: 40, longitudeDelta: 40)
                )
            )
        }
    }
}

// MARK: - Pilgrim Mode ViewModel

@Observable
final class PilgrimModeViewModel {
    let pilgrimageService: PilgrimageService
    let entitlement: EntitlementService

    var activeRoutePack: RoutePack?
    var currentStopIndex: Int = 0
    var showFieldNoteSheet: Bool = false
    var fieldNoteText: String = ""
    var showCompletionCelebration: Bool = false

    init(
        pilgrimageService: PilgrimageService = PilgrimageService(),
        entitlement: EntitlementService = .shared
    ) {
        self.pilgrimageService = pilgrimageService
        self.entitlement = entitlement
    }

    var currentJourney: Journey? {
        pilgrimageService.activeJourney
    }

    var isActive: Bool {
        pilgrimageService.isPilgrimModeActive
    }

    var visitedCount: Int {
        currentJourney?.visits.count ?? 0
    }

    var nextStop: RouteStop? {
        guard let pack = activeRoutePack, currentStopIndex < pack.stops.count else { return nil }
        return pack.stops[currentStopIndex]
    }

    var progress: Double {
        guard let pack = activeRoutePack, pack.totalStops > 0 else { return 0 }
        return Double(visitedCount) / Double(pack.totalStops)
    }

    var isJourneyComplete: Bool {
        guard let pack = activeRoutePack else { return false }
        return visitedCount >= pack.totalStops
    }

    func startJourney(routePack: RoutePack, context: ModelContext?) {
        activeRoutePack = routePack
        currentStopIndex = 0
        pilgrimageService.startJourney(
            routePackID: routePack.id,
            routePackTitle: routePack.title,
            context: context
        )
    }

    func visitCurrentStop(context: ModelContext?) {
        guard let stop = nextStop,
              let location = MockData.location(by: stop.locationID) else { return }
        pilgrimageService.recordVisit(location: location, context: context)
        currentStopIndex += 1

        if isJourneyComplete {
            showCompletionCelebration = true
        }
    }

    func pauseJourney(context: ModelContext?) {
        pilgrimageService.pauseJourney(context: context)
    }

    func resumeJourney(context: ModelContext?) {
        pilgrimageService.resumeJourney(context: context)
    }

    func endJourney(context: ModelContext?) {
        pilgrimageService.endJourney(context: context)
        activeRoutePack = nil
        currentStopIndex = 0
    }

    func addFieldNote(context: ModelContext?) {
        guard !fieldNoteText.isEmpty else { return }
        let locationID = nextStop?.locationID
        let locationName = nextStop?.title
        pilgrimageService.addFieldNote(
            text: fieldNoteText,
            locationID: locationID,
            locationName: locationName,
            context: context
        )
        fieldNoteText = ""
        showFieldNoteSheet = false
    }

    func hasVisited(locationID: String) -> Bool {
        pilgrimageService.hasVisited(locationID: locationID)
    }
}

// MARK: - Passport ViewModel

@Observable
final class PassportViewModel {
    var allJourneys: [Journey] = []
    var allVisits: [Visit] = []
    var allNotes: [FieldNote] = []

    var totalVisits: Int { allVisits.count }
    var totalJourneys: Int { allJourneys.filter { $0.status == .completed }.count }
    var totalNotes: Int { allNotes.count }

    func loadFromContext(_ context: ModelContext) {
        let journeyDescriptor = FetchDescriptor<Journey>(sortBy: [SortDescriptor(\.startDate, order: .reverse)])
        let visitDescriptor = FetchDescriptor<Visit>(sortBy: [SortDescriptor(\.arrivalDate, order: .reverse)])
        let noteDescriptor = FetchDescriptor<FieldNote>(sortBy: [SortDescriptor(\.timestamp, order: .reverse)])

        allJourneys = (try? context.fetch(journeyDescriptor)) ?? []
        allVisits = (try? context.fetch(visitDescriptor)) ?? []
        allNotes = (try? context.fetch(noteDescriptor)) ?? []
    }

    /// For preview with mock data
    func loadMockData() {
        let journey1 = Journey(routePackID: "rp-seven-churches", routePackTitle: "Seven Churches of Rome")
        journey1.statusRaw = JourneyStatus.completed.rawValue
        journey1.endDate = Date().addingTimeInterval(-86400)

        let visit1 = Visit(locationID: "loc-st-peters", placeName: "St. Peter's Basilica", tradition: .catholic, latitude: 41.9022, longitude: 12.4539)
        visit1.arrivalDate = Date().addingTimeInterval(-172800)
        visit1.journey = journey1

        let visit2 = Visit(locationID: "loc-st-paul-otw", placeName: "St. Paul Outside the Walls", tradition: .catholic, latitude: 41.8869, longitude: 12.4736)
        visit2.arrivalDate = Date().addingTimeInterval(-170000)
        visit2.journey = journey1

        let visit3 = Visit(locationID: "loc-santa-maria-maggiore", placeName: "Santa Maria Maggiore", tradition: .catholic, latitude: 41.8972, longitude: 12.4983)
        visit3.arrivalDate = Date().addingTimeInterval(-168000)
        visit3.journey = journey1

        journey1.visits = [visit1, visit2, visit3]

        let note1 = FieldNote(text: "The light through the dome was extraordinary. I understood, for a moment, what it means to say 'the gates of hell shall not prevail.'", locationID: "loc-st-peters", locationName: "St. Peter's Basilica")
        note1.journey = journey1

        journey1.notes = [note1]

        allJourneys = [journey1]
        allVisits = [visit1, visit2, visit3]
        allNotes = [note1]
    }
}
File 7: Components.swift
Swift

import SwiftUI
import MapKit

// MARK: - Sacred Pin View
/// Custom map pin with tradition color, category icon, and state indicators.

struct SacredPinView: View {
    let tradition: Tradition
    let category: SacredSiteCategory?
    let isToday: Bool
    let isSelected: Bool
    let isLocked: Bool

    var body: some View {
        ZStack {
            // Outer ring for today
            if isToday {
                Circle()
                    .stroke(AnnoTheme.goldBright, lineWidth: 2)
                    .frame(width: 36, height: 36)
            }

            // Main pin
            Circle()
                .fill(isLocked ? Color.gray.opacity(0.4) : Color(hex: tradition.color))
                .frame(width: isSelected ? 32 : 26, height: isSelected ? 32 : 26)
                .shadow(color: .black.opacity(0.5), radius: 3, y: 2)

            // Icon
            if let cat = category {
                Image(systemName: cat.symbol)
                    .font(.system(size: isSelected ? 14 : 11, weight: .semibold))
                    .foregroundStyle(isLocked ? .gray : .black)
            }

            // Lock indicator
            if isLocked {
                Image(systemName: "lock.fill")
                    .font(.system(size: 8, weight: .bold))
                    .foregroundStyle(.white)
                    .offset(y: 12)
            }
        }
        .animation(.easeInOut(duration: 0.2), value: isSelected)
    }
}

// MARK: - Tradition Filter Bar
/// Horizontal scrollable tradition filter pills.

struct TraditionFilterBar: View {
    @Bindable var viewModel: SacredAtlasViewModel

    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: AnnoTheme.spacingSM) {
                // All
                FilterPill(
                    title: L.all,
                    isSelected: viewModel.selectedTradition == nil,
                    color: AnnoTheme.ivory
                ) {
                    viewModel.selectedTradition = nil
                    viewModel.applyFilters()
                }

                ForEach(Tradition.allCases) { tradition in
                    FilterPill(
                        title: L.tr(tradition.rawValue),
                        isSelected: viewModel.selectedTradition == tradition,
                        color: Color(hex: tradition.color)
                    ) {
                        viewModel.toggleTradition(tradition)
                    }
                }
            }
            .padding(.horizontal, AnnoTheme.spacingLG)
        }
    }
}

private extension L {
    static func tr(_ traditionRaw: String) -> String {
        guard let tradition = Tradition(rawValue: traditionRaw) else { return traditionRaw }
        switch tradition {
        case .catholic: return L.catholic
        case .orthodox: return L.orthodox
        case .jewish: return L.jewish
        case .islamic: return L.islamic
        case .interfaith: return L.interfaith
        }
    }
}

// MARK: - Filter Pill

struct FilterPill: View {
    let title: String
    let isSelected: Bool
    let color: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .font(AnnoTheme.caption)
                .foregroundStyle(isSelected ? AnnoTheme.background : color)
                .padding(.horizontal, AnnoTheme.spacingMD)
                .padding(.vertical, AnnoTheme.spacingXS + 2)
                .background(
                    isSelected ? color : color.opacity(0.15),
                    in: Capsule()
                )
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Confidence Badge

struct ConfidenceBadge: View {
    let confidence: ConfidenceLabel

    var color: Color {
        switch confidence {
        case .confirmed: return AnnoTheme.confirmedColor
        case .traditional: return AnnoTheme.traditionalColor
        case .disputed: return AnnoTheme.disputedColor
        }
    }

    var label: String {
        switch confidence {
        case .confirmed: return L.confirmed
        case .traditional: return L.traditional
        case .disputed: return L.disputed
        }
    }

    var body: some View {
        HStack(spacing: AnnoTheme.spacingXS) {
            Circle()
                .fill(color)
                .frame(width: 6, height: 6)
            Text(label)
                .font(AnnoTheme.caption)
                .foregroundStyle(color)
        }
    }
}

// MARK: - Tradition Tag

struct TraditionTag: View {
    let tradition: Tradition

    var body: some View {
        HStack(spacing: 3) {
            Text(tradition.symbol)
                .font(.system(size: 10))
            Text(L.tr(tradition.rawValue))
                .font(AnnoTheme.caption)
        }
        .foregroundStyle(Color(hex: tradition.color))
        .padding(.horizontal, AnnoTheme.spacingSM)
        .padding(.vertical, 2)
        .background(Color(hex: tradition.color).opacity(0.12), in: Capsule())
    }
}

// MARK: - On This Ground Card
/// The compact location card that appears when a pin is selected.

struct OnThisGroundCard: View {
    let location: SacredLocation
    let isLocked: Bool
    let onTap: () -> Void

    var body: some View {
        Button(action: onTap) {
            VStack(alignment: .leading, spacing: AnnoTheme.spacingSM) {
                // Tradition tags
                HStack(spacing: AnnoTheme.spacingXS) {
                    ForEach(location.traditions, id: \.self) { tradition in
                        TraditionTag(tradition: tradition)
                    }
                    Spacer()
                    ConfidenceBadge(confidence: location.confidence)
                }

                // Place name
                Text(location.placeName)
                    .font(AnnoTheme.headingSmall)
                    .foregroundStyle(AnnoTheme.ivory)
                    .lineLimit(1)

                // "On This Ground" label
                if !isLocked {
                    HStack(spacing: AnnoTheme.spacingXS) {
                        Image(systemName: "mappin.and.ellipse")
                            .font(.system(size: 10, weight: .semibold))
                        Text(L.onThisGround)
                            .font(AnnoTheme.captionSerif)
                    }
                    .foregroundStyle(AnnoTheme.gold)

                    Text(location.onThisGroundNarrative)
                        .font(AnnoTheme.bodySmall)
                        .foregroundStyle(AnnoTheme.ivoryDim)
                        .lineLimit(3)
                } else {
                    // Locked preview
                    Text(location.shortNarrative)
                        .font(AnnoTheme.bodySmall)
                        .foregroundStyle(AnnoTheme.mutedText)
                        .lineLimit(2)

                    HStack(spacing: AnnoTheme.spacingXS) {
                        Image(systemName: "lock.fill")
                            .font(.system(size: 9))
                        Text(L.unlock)
                            .font(AnnoTheme.caption)
                    }
                    .foregroundStyle(AnnoTheme.goldDim)
                }
            }
            .padding(AnnoTheme.spacingLG)
            .background(AnnoTheme.cardElevated)
            .clipShape(RoundedRectangle(cornerRadius: AnnoTheme.radiusLG))
            .shadow(color: .black.opacity(0.5), radius: 10, y: 5)
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Nearby History Card
/// Summary card showing nearby sacred history.

struct NearbyHistoryCard: View {
    let nearbyCount: Int
    let todayCount: Int
    let isFreeUser: Bool
    let onTap: () -> Void

    var body: some View {
        Button(action: onTap) {
            HStack(spacing: AnnoTheme.spacingMD) {
                // Icon
                Image(systemName: "mappin.circle.fill")
                    .font(.system(size: 24))
                    .foregroundStyle(AnnoTheme.gold)

                VStack(alignment: .leading, spacing: 2) {
                    Text(L.nearYouInSacredHistory)
                        .font(AnnoTheme.caption)
                        .foregroundStyle(AnnoTheme.gold)
                    Text("\(nearbyCount) \(L.sacredSitesNearYou)")
                        .font(AnnoTheme.bodyMedium)
                        .foregroundStyle(AnnoTheme.ivory)
                    if todayCount > 0 {
                        Text("\(todayCount) \(L.sitesConnectedToToday)")
                            .font(AnnoTheme.bodySmall)
                            .foregroundStyle(AnnoTheme.goldDim)
                    }
                }

                Spacer()

                if isFreeUser {
                    Text("\(3) / \(nearbyCount)")
                        .font(AnnoTheme.caption)
                        .foregroundStyle(AnnoTheme.mutedText)
                }

                Image(systemName: "chevron.right")
                    .font(.system(size: 12, weight: .semibold))
                    .foregroundStyle(AnnoTheme.mutedText)
            }
            .padding(AnnoTheme.spacingMD)
            .background(AnnoTheme.cardElevated)
            .clipShape(RoundedRectangle(cornerRadius: AnnoTheme.radiusMD))
            .shadow(color: .black.opacity(0.4), radius: 6, y: 3)
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Pilgrim Stamp View
/// A visual "stamp" for a visited location, displayed in the passport.

struct PilgrimStampView: View {
    let placeName: String
    let tradition: Tradition
    let dateVisited: Date
    let hasNote: Bool

    private let stampSize: CGFloat = 72

    var body: some View {
        VStack(spacing: AnnoTheme.spacingXS) {
            ZStack {
                // Outer circle
                Circle()
                    .stroke(Color(hex: tradition.color), lineWidth: 1.5)
                    .frame(width: stampSize, height: stampSize)

                // Inner decoration
                Circle()
                    .stroke(Color(hex: tradition.color).opacity(0.3), lineWidth: 0.5)
                    .frame(width: stampSize - 8, height: stampSize - 8)

                // Tradition symbol
                Text(tradition.symbol)
                    .font(.system(size: 20))

                // Note indicator
                if hasNote {
                    Image(systemName: "note.text")
                        .font(.system(size: 8))
                        .foregroundStyle(AnnoTheme.gold)
                        .offset(x: stampSize/2 - 10, y: -stampSize/2 + 10)
                }
            }

            Text(placeName)
                .font(AnnoTheme.captionSerif)
                .foregroundStyle(AnnoTheme.ivoryDim)
                .lineLimit(1)

            Text(dateVisited, style: .date)
                .font(.system(size: 9))
                .foregroundStyle(AnnoTheme.mutedText)
        }
        .frame(width: 90)
    }
}

// MARK: - Journey Progress View

struct JourneyProgressView: View {
    let progress: Double
    let visitedCount: Int
    let totalCount: Int

    var body: some View {
        VStack(spacing: AnnoTheme.spacingSM) {
            // Progress bar
            GeometryReader { geometry in
                ZStack(alignment: .leading) {
                    // Track
                    RoundedRectangle(cornerRadius: 2)
                        .fill(AnnoTheme.separator)
                        .frame(height: 4)

                    // Fill
                    RoundedRectangle(cornerRadius: 2)
                        .fill(AnnoTheme.gold)
                        .frame(width: geometry.size.width * min(progress, 1.0), height: 4)
                }
            }
            .frame(height: 4)

            // Labels
            HStack {
                Text("\(visitedCount) / \(totalCount) \(L.stops.lowercased())")
                    .font(AnnoTheme.caption)
                    .foregroundStyle(AnnoTheme.mutedText)

                Spacer()

                Text("\(Int(progress * 100))%")
                    .font(AnnoTheme.caption)
                    .foregroundStyle(AnnoTheme.gold)
            }
        }
    }
}

// MARK: - Premium Lock Overlay

struct PremiumLockOverlay: View {
    let title: String
    let subtitle: String
    let siteCount: Int
    let action: () -> Void

    var body: some View {
        VStack(spacing: AnnoTheme.spacingMD) {
            Image(systemName: "lock.shield.fill")
                .font(.system(size: 28))
                .foregroundStyle(AnnoTheme.gold)

            Text(title)
                .font(AnnoTheme.headingSmall)
                .foregroundStyle(AnnoTheme.ivory)
                .multilineTextAlignment(.center)

            Text(subtitle)
                .font(AnnoTheme.bodySmall)
                .foregroundStyle(AnnoTheme.ivoryDim)
                .multilineTextAlignment(.center)

            Text("\(siteCount)+ \(L.sitesAvailable)")
                .font(AnnoTheme.caption)
                .foregroundStyle(AnnoTheme.mutedText)

            Button(action: action) {
                Text(L.unlock)
                    .font(AnnoTheme.caption)
                    .fontWeight(.semibold)
                    .foregroundStyle(AnnoTheme.background)
                    .padding(.horizontal, AnnoTheme.spacingXL)
                    .padding(.vertical, AnnoTheme.spacingSM)
                    .background(AnnoTheme.gold, in: Capsule())
            }
            .buttonStyle(.plain)
        }
        .padding(AnnoTheme.spacingXL)
        .frame(maxWidth: .infinity)
        .background(AnnoTheme.cardElevated)
        .clipShape(RoundedRectangle(cornerRadius: AnnoTheme.radiusLG))
    }
}

// MARK: - Map Style Selector

struct MapStyleSelector: View {
    @Bindable var viewModel: SacredAtlasViewModel

    var body: some View {
        VStack(spacing: AnnoTheme.spacingXS) {
            ForEach(AtlasMapStyle.allCases, id: \.self) { style in
                Button {
                    viewModel.mapStyle = style
                } label: {
                    HStack {
                        Text(style.displayName)
                            .font(AnnoTheme.bodySmall)
                        Spacer()
                        if viewModel.mapStyle == style {
                            Image(systemName: "checkmark")
                                .font(.system(size: 12, weight: .bold))
                        }
                    }
                    .foregroundStyle(viewModel.mapStyle == style ? AnnoTheme.gold : AnnoTheme.ivoryDim)
                    .padding(.horizontal, AnnoTheme.spacingMD)
                    .padding(.vertical, AnnoTheme.spacingSM)
                }
                .buttonStyle(.plain)
            }
        }
        .padding(AnnoTheme.spacingSM)
        .background(AnnoTheme.cardElevated)
        .clipShape(RoundedRectangle(cornerRadius: AnnoTheme.radiusMD))
    }
}

// MARK: - Layer Filter Panel

struct LayerFilterPanel: View {
    @Bindable var viewModel: SacredAtlasViewModel

    var body: some View {
        VStack(alignment: .leading, spacing: AnnoTheme.spacingSM) {
            Text(L.layers)
                .font(AnnoTheme.caption)
                .foregroundStyle(AnnoTheme.gold)
                .textCase(.uppercase)

            LazyVGrid(columns: [
                GridItem(.flexible()),
                GridItem(.flexible()),
            ], spacing: AnnoTheme.spacingSM) {
                ForEach(SacredLayer.allCases) { layer in
                    Button {
                        viewModel.selectLayer(viewModel.selectedLayer == layer ? nil : layer)
                    } label: {
                        HStack(spacing: 4) {
                            Image(systemName: layerIcon(layer))
                                .font(.system(size: 10))
                            Text(layerName(layer))
                                .font(AnnoTheme.caption)
                        }
                        .foregroundStyle(viewModel.selectedLayer == layer ? AnnoTheme.gold : AnnoTheme.ivoryDim)
                        .padding(.horizontal, AnnoTheme.spacingSM)
                        .padding(.vertical, AnnoTheme.spacingXS + 2)
                        .background(
                            viewModel.selectedLayer == layer ? AnnoTheme.gold.opacity(0.15) : AnnoTheme.separator.opacity(0.3),
                            in: Capsule()
                        )
                    }
                    .buttonStyle(.plain)
                }
            }
        }
        .padding(AnnoTheme.spacingMD)
        .background(AnnoTheme.cardElevated)
        .clipShape(RoundedRectangle(cornerRadius: AnnoTheme.radiusMD))
    }

    private func layerIcon(_ layer: SacredLayer) -> String {
        switch layer {
        case .today: return "sun.max"
        case .saints: return "hand.raised"
        case .martyrs: return "flame"
        case .councils: return "building.columns"
        case .relics: return "cross.case"
        case .marian: return "star.circle"
        case .monasteries: return "building.2"
        case .biblical: return "book.closed"
        case .pilgrimage: return "point.topleft.down.to.point.bottomright.curvepath"
        }
    }

    private func layerName(_ layer: SacredLayer) -> String {
        switch layer {
        case .today: return L.todayLayer
        case .saints: return L.saints
        case .martyrs: return L.martyrs
        case .councils: return L.councils
        case .relics: return L.relics
        case .marian: return L.marian
        case .monasteries: return L.monasteries
        case .biblical: return L.biblical
        case .pilgrimage: return L.pilgrimage
        }
    }
}

// MARK: - Field Note Row

struct FieldNoteRow: View {
    let note: FieldNote

    var body: some View {
        VStack(alignment: .leading, spacing: AnnoTheme.spacingXS) {
            HStack {
                if let name = note.locationName {
                    Text(name)
                        .font(AnnoTheme.caption)
                        .foregroundStyle(AnnoTheme.gold)
                }
                Spacer()
                Text(note.timestamp, style: .date)
                    .font(.system(size: 10))
                    .foregroundStyle(AnnoTheme.mutedText)
            }
            Text(note.text)
                .font(AnnoTheme.bodySmall)
                .foregroundStyle(AnnoTheme.ivoryDim)
        }
        .padding(AnnoTheme.spacingMD)
        .background(AnnoTheme.cardBackground)
        .clipShape(RoundedRectangle(cornerRadius: AnnoTheme.radiusSM))
    }
}

// MARK: - No Location Permission View

struct NoLocationPermissionView: View {
    let onEnable: () -> Void
    let onExplore: () -> Void

    var body: some View {
        VStack(spacing: AnnoTheme.spacingLG) {
            Image(systemName: "location.slash")
                .font(.system(size: 36))
                .foregroundStyle(AnnoTheme.mutedText)

            Text(L.enableLocation)
                .font(AnnoTheme.headingSmall)
                .foregroundStyle(AnnoTheme.ivory)

            Text(L.locationExplanation)
                .font(AnnoTheme.bodySmall)
                .foregroundStyle(AnnoTheme.ivoryDim)
                .multilineTextAlignment(.center)
                .padding(.horizontal, AnnoTheme.spacingXL)

            Button(action: onEnable) {
                Text(L.enableLocation)
                    .font(AnnoTheme.bodyMedium)
                    .fontWeight(.semibold)
                    .foregroundStyle(AnnoTheme.background)
                    .padding(.horizontal, AnnoTheme.spacingXL)
                    .padding(.vertical, AnnoTheme.spacingSM)
                    .background(AnnoTheme.gold, in: Capsule())
            }

            Button(action: onExplore) {
                Text(L.exploreWithoutLocation)
                    .font(AnnoTheme.bodySmall)
                    .foregroundStyle(AnnoTheme.goldDim)
            }
        }
        .padding(AnnoTheme.spacingXXL)
        .background(AnnoTheme.cardElevated)
        .clipShape(RoundedRectangle(cornerRadius: AnnoTheme.radiusXL))
    }
}
File 8: SacredAtlasView.swift
Swift

import SwiftUI
import MapKit
import SwiftData

// MARK: - Sacred Atlas View
/// The main map experience. Full-screen map with sacred pins, filters,
/// nearby discovery, and entry points to Pilgrim Mode and Passport.

struct SacredAtlasView: View {
    @Environment(\.modelContext) private var modelContext
    @State private var viewModel = SacredAtlasViewModel()
    @State private var pilgrimageService = PilgrimageService()

    var body: some View {
        ZStack {
            // Map
            mapLayer

            // Overlays
            VStack(spacing: 0) {
                // Top bar: filters + controls
                topBar

                Spacer()

                // Bottom content
                bottomContent
            }
        }
        .background(AnnoTheme.background)
        .ignoresSafeArea(.keyboard)
        .sheet(isPresented: $viewModel.showLocationDetail) {
            if let location = viewModel.selectedLocation {
                LocationDetailView(
                    location: location,
                    isLocked: viewModel.isLocationLocked(location),
                    pilgrimageService: pilgrimageService,
                    onDismiss: { viewModel.deselectLocation() }
                )
            }
        }
        .sheet(isPresented: $viewModel.showRoutePacks) {
            RoutePackListView()
        }
        .fullScreenCover(isPresented: $viewModel.showPilgrimMode) {
            PilgrimModeView()
        }
        .sheet(isPresented: $viewModel.showPassport) {
            PilgrimPassportView()
        }
        .sheet(isPresented: $viewModel.showPremiumUnlock) {
            PremiumUnlockView()
        }
        .onAppear {
            viewModel.moveToWorld()
        }
    }

    // MARK: - Map Layer

    @ViewBuilder
    private var mapLayer: some View {
        Map(position: $viewModel.cameraPosition, interactionModes: .all) {
            UserAnnotation()

            ForEach(viewModel.filteredLocations) { location in
                Annotation(location.placeName, coordinate: location.coordinate) {
                    SacredPinView(
                        tradition: location.traditions.first ?? .catholic,
                        category: location.categories.first,
                        isToday: location.isTodayConnected,
                        isSelected: viewModel.selectedLocation?.id == location.id,
                        isLocked: viewModel.isLocationLocked(location)
                    )
                    .onTapGesture {
                        viewModel.selectLocation(location)
                        viewModel.moveToLocation(location)
                    }
                }
            }
        }
        .mapStyle(mapStyleFor(viewModel.mapStyle))
        .mapControls {
            MapCompass()
            MapScaleView()
        }
    }

    private func mapStyleFor(_ style: AtlasMapStyle) -> MapStyle {
        switch style {
        case .atlas:
            return .standard(elevation: .flat, emphasis: .muted, pointsOfInterest: .excludingAll)
        case .satellite:
            return .imagery(elevation: .flat)
        case .hybrid:
            return .hybrid(elevation: .flat, pointsOfInterest: .excludingAll)
        }
    }

    // MARK: - Top Bar

    private var topBar: some View {
        VStack(spacing: AnnoTheme.spacingSM) {
            // Tradition filters
            TraditionFilterBar(viewModel: viewModel)

            // Layer / confidence / style controls
            HStack(spacing: AnnoTheme.spacingSM) {
                // Layers button
                Button {
                    withAnimation { viewModel.showLayers.toggle() }
                } label: {
                    Image(systemName: "line.3.horizontal.decrease.circle")
                        .font(.system(size: 16, weight: .medium))
                        .foregroundStyle(AnnoTheme.ivoryDim)
                        .padding(AnnoTheme.spacingSM)
                        .background(AnnoTheme.cardElevated.opacity(0.9), in: Circle())
                }

                // Confidence filter
                Menu {
                    Button(L.all) {
                        viewModel.selectedConfidence = nil
                        viewModel.applyFilters()
                    }
                    ForEach(ConfidenceLabel.allCases) { conf in
                        Button {
                            viewModel.toggleConfidence(conf)
                        } label: {
                            Label(
                                conf == .confirmed ? L.confirmed : conf == .traditional ? L.traditional : L.disputed,
                                systemImage: conf == .confirmed ? "checkmark.circle" : conf == .traditional ? "circle.lefthalf.filled" : "questionmark.circle"
                            )
                        }
                    }
                } label: {
                    Image(systemName: "shield.checkered")
                        .font(.system(size: 16, weight: .medium))
                        .foregroundStyle(viewModel.selectedConfidence != nil ? AnnoTheme.gold : AnnoTheme.ivoryDim)
                        .padding(AnnoTheme.spacingSM)
                        .background(AnnoTheme.cardElevated.opacity(0.9), in: Circle())
                }

                Spacer()

                // Route packs
                Button {
                    viewModel.showRoutePacks = true
                } label: {
                    Image(systemName: "map")
                        .font(.system(size: 16, weight: .medium))
                        .foregroundStyle(AnnoTheme.ivoryDim)
                        .padding(AnnoTheme.spacingSM)
                        .background(AnnoTheme.cardElevated.opacity(0.9), in: Circle())
                }

                // Passport
                Button {
                    viewModel.showPassport = true
                } label: {
                    Image(systemName: "book.closed")
                        .font(.system(size: 16, weight: .medium))
                        .foregroundStyle(AnnoTheme.ivoryDim)
                        .padding(AnnoTheme.spacingSM)
                        .background(AnnoTheme.cardElevated.opacity(0.9), in: Circle())
                }

                // Map style
                Menu {
                    ForEach(AtlasMapStyle.allCases, id: \.self) { style in
                        Button {
                            viewModel.mapStyle = style
                        } label: {
                            if viewModel.mapStyle == style {
                                Label(style.displayName, systemImage: "checkmark")
                            } else {
                                Text(style.displayName)
                            }
                        }
                    }
                } label: {
                    Image(systemName: "layer.group")
                        .font(.system(size: 16, weight: .medium))
                        .foregroundStyle(AnnoTheme.ivoryDim)
                        .padding(AnnoTheme.spacingSM)
                        .background(AnnoTheme.cardElevated.opacity(0.9), in: Circle())
                }
            }
            .padding(.horizontal, AnnoTheme.spacingLG)

            // Expandable layer panel
            if viewModel.showLayers {
                LayerFilterPanel(viewModel: viewModel)
                    .padding(.horizontal, AnnoTheme.spacingLG)
                    .transition(.opacity.combined(with: .move(edge: .top)))
            }

            // Nearby card (if location available)
            if viewModel.locationService.isLocationAvailable && viewModel.showNearbyCard {
                NearbyHistoryCard(
                    nearbyCount: MockData.nearbySiteCount,
                    todayCount: MockData.todayConnectedCount,
                    isFreeUser: viewModel.entitlement.currentTier == .free
                ) {
                    // Scroll to nearest
                    if let first = viewModel.nearbyLocations.first {
                        viewModel.moveToLocation(first.location)
                        viewModel.selectLocation(first.location)
                    }
                }
                .padding(.horizontal, AnnoTheme.spacingLG)
            }
        }
        .padding(.top, 50)  // safe area
    }

    // MARK: - Bottom Content

    private var bottomContent: some View {
        VStack(spacing: AnnoTheme.spacingMD) {
            Spacer()

            // Selected location card
            if let location = viewModel.selectedLocation {
                OnThisGroundCard(
                    location: location,
                    isLocked: viewModel.isLocationLocked(location)
                ) {
                    viewModel.showLocationDetail = true
                }
                .padding(.horizontal, AnnoTheme.spacingLG)
                .transition(.move(edge: .bottom).combined(with: .opacity))
            }

            // Bottom action bar
            HStack {
                // Locate me
                Button {
                    if viewModel.locationService.authorizationStatus == .notDetermined {
                        viewModel.showLocationPermission = true
                        viewModel.locationService.requestPermission()
                    } else if viewModel.locationService.isLocationAvailable {
                        viewModel.moveToUser()
                    } else {
                        viewModel.showLocationPermission = true
                    }
                } label: {
                    Image(systemName: viewModel.locationService.isLocationAvailable ? "location.fill" : "location")
                        .font(.system(size: 16, weight: .medium))
                        .foregroundStyle(viewModel.locationService.isLocationAvailable ? AnnoTheme.gold : AnnoTheme.ivoryDim)
                        .padding(AnnoTheme.spacingMD)
                        .background(AnnoTheme.cardElevated, in: Circle())
                        .shadow(color: .black.opacity(0.3), radius: 4, y: 2)
                }

                Spacer()

                // Pilgrim mode entry
                if pilgrimageService.isPilgrimModeActive {
                    Button {
                        viewModel.showPilgrimMode = true
                    } label: {
                        HStack(spacing: AnnoTheme.spacingXS) {
                            Image(systemName: "figure.walk")
                            Text(L.continueJourney)
                        }
                        .font(AnnoTheme.caption)
                        .fontWeight(.semibold)
                        .foregroundStyle(AnnoTheme.background)
                        .padding(.horizontal, AnnoTheme.spacingLG)
                        .padding(.vertical, AnnoTheme.spacingMD)
                        .background(AnnoTheme.gold, in: Capsule())
                    }
                } else if viewModel.entitlement.currentTier.canStartPilgrimage {
                    Button {
                        viewModel.showRoutePacks = true
                    } label: {
                        HStack(spacing: AnnoTheme.spacingXS) {
                            Image(systemName: "figure.walk")
                            Text(L.startPilgrimage)
                        }
                        .font(AnnoTheme.caption)
                        .fontWeight(.semibold)
                        .foregroundStyle(AnnoTheme.gold)
                        .padding(.horizontal, AnnoTheme.spacingLG)
                        .padding(.vertical, AnnoTheme.spacingMD)
                        .background(AnnoTheme.gold.opacity(0.15), in: Capsule())
                    }
                } else {
                    // Free user: show locked pilgrim CTA
                    Button {
                        viewModel.showPremiumUnlock = true
                    } label: {
                        HStack(spacing: AnnoTheme.spacingXS) {
                            Image(systemName: "lock.fill")
                            Text(L.pilgrimMode)
                        }
                        .font(AnnoTheme.caption)
                        .foregroundStyle(AnnoTheme.mutedText)
                        .padding(.horizontal, AnnoTheme.spacingLG)
                        .padding(.vertical, AnnoTheme.spacingMD)
                        .background(AnnoTheme.cardElevated, in: Capsule())
                    }
                }
            }
            .padding(.horizontal, AnnoTheme.spacingLG)
            .padding(.bottom, 20)  // home indicator area
        }
    }
}
File 9: LocationDetailView.swift
Swift

import SwiftUI
import MapKit

// MARK: - Location Detail View
/// Rich place detail sheet with narrative, events, art, sources, and actions.

struct LocationDetailView: View {
    let location: SacredLocation
    let isLocked: Bool
    let pilgrimageService: PilgrimageService
    let onDismiss: () -> Void

    @Environment(\.modelContext) private var modelContext
    @State private var showPremiumUnlock = false
    @State private var isSaved = false

    private var events: [HistoricalEvent] {
        MockData.events(for: location.id)
    }

    private var sources: [Source] {
        MockData.sources(for: location.sourceIDs)
    }

    private var artworks: [Artwork] {
        location.artworkIDs.compactMap { MockData.artwork(by: $0) }
    }

    private var routePacks: [RoutePack] {
        MockData.routePacks(for: location.id)
    }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: AnnoTheme.spacingXL) {
                    // Header
                    headerSection

                    if isLocked {
                        // Locked content
                        lockedPreviewSection
                    } else {
                        // Full content
                        onThisGroundSection
                        eventsSection
                        if !artworks.isEmpty { artSection }
                        sourcesSection
                        if location.visitingHours != nil { visitingHoursSection }
                        routePacksSection
                    }

                    // Actions (always visible)
                    actionsSection
                }
                .padding(AnnoTheme.spacingLG)
            }
            .background(AnnoTheme.background)
            .navigationTitle("")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button(L.close) { onDismiss() }
                        .foregroundStyle(AnnoTheme.gold)
                }
            }
            .sheet(isPresented: $showPremiumUnlock) {
                PremiumUnlockView()
            }
        }
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
        .presentationBackground(AnnoTheme.background)
    }

    // MARK: - Header

    private var headerSection: some View {
        VStack(alignment: .leading, spacing: AnnoTheme.spacingMD) {
            // Tradition tags
            HStack(spacing: AnnoTheme.spacingXS) {
                ForEach(location.traditions, id: \.self) { tradition in
                    TraditionTag(tradition: tradition)
                }
                Spacer()
                ConfidenceBadge(confidence: location.confidence)
            }

            // Place name
            Text(location.placeName)
                .font(AnnoTheme.headingLarge)
                .foregroundStyle(AnnoTheme.ivory)

            // Region
            HStack(spacing: AnnoTheme.spacingXS) {
                Image(systemName: "mappin")
                    .font(.system(size: 11))
                Text([location.region, location.country].filter { !$0.isEmpty }.joined(separator: ", "))
                    .font(AnnoTheme.bodySmall)
            }
            .foregroundStyle(AnnoTheme.mutedText)

            if let address = location.modernAddress {
                Text(address)
                    .font(AnnoTheme.caption)
                    .foregroundStyle(AnnoTheme.mutedText)
            }
        }
    }

    // MARK: - On This Ground

    private var onThisGroundSection: some View {
        VStack(alignment: .leading, spacing: AnnoTheme.spacingMD) {
            HStack(spacing: AnnoTheme.spacingXS) {
                Image(systemName: "mappin.and.ellipse")
                    .font(.system(size: 12, weight: .semibold))
                Text(L.onThisGround)
                    .font(AnnoTheme.caption)
                    .textCase(.uppercase)
            }
            .foregroundStyle(AnnoTheme.gold)

            Text(location.onThisGroundNarrative)
                .font(AnnoTheme.bodyLarge)
                .foregroundStyle(AnnoTheme.ivory)
                .lineSpacing(4)
        }
    }

    // MARK: - Events

    private var eventsSection: some View {
        VStack(alignment: .leading, spacing: AnnoTheme.spacingMD) {
            HStack(spacing: AnnoTheme.spacingXS) {
                Image(systemName: "clock.arrow.circlepath")
                    .font(.system(size: 12, weight: .semibold))
                Text(L.associatedEvents)
                    .font(AnnoTheme.caption)
                    .textCase(.uppercase)
            }
            .foregroundStyle(AnnoTheme.gold)

            ForEach(events) { event in
                eventRow(event)
            }
        }
    }

    private func eventRow(_ event: HistoricalEvent) -> some View {
        VStack(alignment: .leading, spacing: AnnoTheme.spacingXS) {
            HStack {
                Text(event.dateDescription)
                    .font(AnnoTheme.caption)
                    .foregroundStyle(AnnoTheme.goldDim)
                if let color = event.liturgicalColor {
                    Circle()
                        .fill(liturgicalColor(color))
                        .frame(width: 8, height: 8)
                }
                Spacer()
                ConfidenceBadge(confidence: event.confidence)
            }

            Text(event.title)
                .font(AnnoTheme.headingSmall)
                .foregroundStyle(AnnoTheme.ivory)

            Text(event.shortNarrative)
                .font(AnnoTheme.bodySmall)
                .foregroundStyle(AnnoTheme.ivoryDim)
                .lineLimit(4)
        }
        .padding(AnnoTheme.spacingMD)
        .background(AnnoTheme.cardBackground)
        .clipShape(RoundedRectangle(cornerRadius: AnnoTheme.radiusMD))
    }

    private func liturgicalColor(_ name: String) -> Color {
        switch name {
        case "red": return .red
        case "white": return .white
        case "green": return .green
        case "purple", "violet": return .purple
        case "rose": return .pink
        case "black": return .gray
        default: return AnnoTheme.mutedText
        }
    }

    // MARK: - Art

    private var artSection: some View {
        VStack(alignment: .leading, spacing: AnnoTheme.spacingMD) {
            HStack(spacing: AnnoTheme.spacingXS) {
                Image(systemName: "paintbrush")
                    .font(.system(size: 12, weight: .semibold))
                Text(L.art)
                    .font(AnnoTheme.caption)
                    .textCase(.uppercase)
            }
            .foregroundStyle(AnnoTheme.gold)

            ForEach(artworks) { artwork in
                artworkRow(artwork)
            }
        }
    }

    private func artworkRow(_ artwork: Artwork) -> some View {
        HStack(spacing: AnnoTheme.spacingMD) {
            // Thumbnail placeholder
            if let imageName = artwork.imageName {
                Image(systemName: imageName)
                    .font(.system(size: 28))
                    .foregroundStyle(AnnoTheme.goldDim)
                    .frame(width: 60, height: 60)
                    .background(AnnoTheme.separator)
                    .clipShape(RoundedRectangle(cornerRadius: AnnoTheme.radiusSM))
            }

            VStack(alignment: .leading, spacing: 2) {
                Text(artwork.title)
                    .font(AnnoTheme.headingSmall)
                    .foregroundStyle(AnnoTheme.ivory)
                if let artist = artwork.artist {
                    Text(artist)
                        .font(AnnoTheme.bodySmall)
                        .foregroundStyle(AnnoTheme.ivoryDim)
                }
                if let period = artwork.datePeriod {
                    Text(period)
                        .font(AnnoTheme.caption)
                        .foregroundStyle(AnnoTheme.mutedText)
                }
            }
        }
        .padding(AnnoTheme.spacingMD)
        .background(AnnoTheme.cardBackground)
        .clipShape(RoundedRectangle(cornerRadius: AnnoTheme.radiusMD))
    }

    // MARK: - Sources

    private var sourcesSection: some View {
        VStack(alignment: .leading, spacing: AnnoTheme.spacingMD) {
            HStack(spacing: AnnoTheme.spacingXS) {
                Image(systemName: "book")
                    .font(.system(size: 12, weight: .semibold))
                Text("\(L.sources) (\(sources.count))")
                    .font(AnnoTheme.caption)
                    .textCase(.uppercase)
            }
            .foregroundStyle(AnnoTheme.gold)

            ForEach(sources) { source in
                sourceRow(source)
            }
        }
    }

    private func sourceRow(_ source: Source) -> some View {
        HStack(spacing: AnnoTheme.spacingSM) {
            VStack(alignment: .leading, spacing: 2) {
                Text(source.title)
                    .font(AnnoTheme.bodyMedium)
                    .foregroundStyle(AnnoTheme.ivory)
                if let author = source.author {
                    Text(author)
                        .font(AnnoTheme.caption)
                        .foregroundStyle(AnnoTheme.mutedText)
                }
            }
            Spacer()
            Text(source.reliability.rawValue.capitalized)
                .font(.system(size: 9))
                .foregroundStyle(AnnoTheme.mutedText)
                .padding(.horizontal, 6)
                .padding(.vertical, 2)
                .background(AnnoTheme.separator.opacity(0.5), in: Capsule())
        }
        .padding(AnnoTheme.spacingSM)
        .background(AnnoTheme.cardBackground.opacity(0.5))
        .clipShape(RoundedRectangle(cornerRadius: AnnoTheme.radiusSM))
    }

    // MARK: - Visiting Hours

    private var visitingHoursSection: some View {
        VStack(alignment: .leading, spacing: AnnoTheme.spacingXS) {
            HStack(spacing: AnnoTheme.spacingXS) {
                Image(systemName: "clock")
                    .font(.system(size: 12, weight: .semibold))
                Text(L.openHours)
                    .font(AnnoTheme.caption)
                    .textCase(.uppercase)
            }
            .foregroundStyle(AnnoTheme.gold)

            Text(location.visitingHours ?? "")
                .font(AnnoTheme.bodyMedium)
                .foregroundStyle(AnnoTheme.ivoryDim)
        }
    }

    // MARK: - Route Packs

    private var routePacksSection: some View {
        VStack(alignment: .leading, spacing: AnnoTheme.spacingMD) {
            if !routePacks.isEmpty {
                HStack(spacing: AnnoTheme.spacingXS) {
                    Image(systemName: "map")
                        .font(.system(size: 12, weight: .semibold))
                    Text(L.routePacks)
                        .font(AnnoTheme.caption)
                        .textCase(.uppercase)
                }
                .foregroundStyle(AnnoTheme.gold)

                ForEach(routePacks) { pack in
                    HStack {
                        VStack(alignment: .leading, spacing: 2) {
                            Text(pack.title)
                                .font(AnnoTheme.bodyMedium)
                                .foregroundStyle(AnnoTheme.ivory)
                            Text("\(pack.totalStops) \(L.stops.lowercased()) · \(pack.estimatedTime)")
                                .font(AnnoTheme.caption)
                                .foregroundStyle(AnnoTheme.mutedText)
                        }
                        Spacer()
                        Image(systemName: "chevron.right")
                            .font(.system(size: 10, weight: .semibold))
                            .foregroundStyle(AnnoTheme.mutedText)
                    }
                    .padding(AnnoTheme.spacingSM)
                    .background(AnnoTheme.cardBackground.opacity(0.5))
                    .clipShape(RoundedRectangle(cornerRadius: AnnoTheme.radiusSM))
                }
            }
        }
    }

    // MARK: - Locked Preview

    private var lockedPreviewSection: some View {
        PremiumLockOverlay(
            title: L.unlockFullAtlas,
            subtitle: "Explore \(MockData.totalSiteCount)+ sacred sites, source-backed place histories, and curated pilgrimage routes.",
            siteCount: MockData.totalSiteCount,
            action: { showPremiumUnlock = true }
        )
    }

    // MARK: - Actions

    private var actionsSection: some View {
        VStack(spacing: AnnoTheme.spacingMD) {
            // Primary actions
            HStack(spacing: AnnoTheme.spacingMD) {
                // Save
                Button {
                    isSaved.toggle()
                } label: {
                    Label(isSaved ? L.saved : L.save, systemImage: isSaved ? "bookmark.fill" : "bookmark")
                        .font(AnnoTheme.bodySmall)
                        .foregroundStyle(isSaved ? AnnoTheme.gold : AnnoTheme.ivoryDim)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, AnnoTheme.spacingMD)
                        .background(AnnoTheme.cardBackground)
                        .clipShape(RoundedRectangle(cornerRadius: AnnoTheme.radiusMD))
                }

                // Directions
                Button {
                    openDirections()
                } label: {
                    Label(L.directions, systemImage: "arrow.triangle.turn.up.right.diamond")
                        .font(AnnoTheme.bodySmall)
                        .foregroundStyle(AnnoTheme.ivoryDim)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, AnnoTheme.spacingMD)
                        .background(AnnoTheme.cardBackground)
                        .clipShape(RoundedRectangle(cornerRadius: AnnoTheme.radiusMD))
                }
            }

            // Pilgrim action
            if !isLocked {
                let entitlement = EntitlementService.shared
                if entitlement.currentTier.canStartPilgrimage {
                    Button {
                        // Add to current journey or start new
                        if pilgrimageService.isPilgrimModeActive {
                            pilgrimageService.recordVisit(location: location, context: modelContext)
                        }
                    } label: {
                        Label(
                            pilgrimageService.hasVisited(locationID: location.id) ? L.visited : L.startPilgrimage,
                            systemImage: pilgrimageService.hasVisited(locationID: location.id) ? "checkmark.circle.fill" : "figure.walk"
                        )
                        .font(AnnoTheme.bodyMedium)
                        .fontWeight(.semibold)
                        .foregroundStyle(AnnoTheme.background)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, AnnoTheme.spacingMD)
                        .background(AnnoTheme.gold, in: RoundedRectangle(cornerRadius: AnnoTheme.radiusMD))
                    }
                } else {
                    Button {
                        showPremiumUnlock = true
                    } label: {
                        Label(L.pilgrimMode, systemImage: "lock.fill")
                            .font(AnnoTheme.bodySmall)
                            .foregroundStyle(AnnoTheme.mutedText)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, AnnoTheme.spacingMD)
                            .background(AnnoTheme.cardElevated, in: RoundedRectangle(cornerRadius: AnnoTheme.radiusMD))
                    }
                }
            }
        }
    }

    // MARK: - Helpers

    private func openDirections() {
        let coordinate = location.coordinate
        let placemark = MKPlacemark(coordinate: coordinate)
        let mapItem = MKMapItem(placemark: placemark)
        mapItem.name = location.placeName
        map
       
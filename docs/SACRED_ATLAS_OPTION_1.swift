// MARK: - File: Models.swift

import Foundation
import CoreLocation

// ─── Enums ───────────────────────────────────────────────

enum Tradition: String, CaseIterable, Codable, Identifiable {
    case catholic, orthodox, jewish, islamic, interfaith
    var id: String { rawValue }
}

enum SacredCategory: String, CaseIterable, Codable, Identifiable {
    case martyrdom, relic, marian, monastery, biblical
    case council, shrine, church, apparition
    var id: String { rawValue }
}

enum ConfidenceLabel: String, CaseIterable, Codable, Identifiable {
    case confirmed, traditional, disputed
    var id: String { rawValue }
}

enum EntitlementTier: Sendable {
    case free, premium
}

// ─── Data Models ─────────────────────────────────────────

struct SacredLocation: Identifiable, Equatable {
    let id: UUID
    let placeName: String
    let latitude: Double
    let longitude: Double
    let modernAddress: String?
    let country: String
    let region: String
    let traditions: [Tradition]
    let categories: [SacredCategory]
    let confidence: ConfidenceLabel
    let whyThisPlaceMatters: String
    let associatedEventIDs: [UUID]
    let visitingHours: String?
    let sourceCount: Int
    let routePackIDs: [UUID]
    let isTodayConnected: Bool

    var coordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
    }

    static func == (lhs: Self, rhs: Self) -> Bool {
        lhs.id == rhs.id
    }
}

struct HistoricalEvent: Identifiable {
    let id: UUID
    let date: Date
    let title: String
    let shortNarrative: String
    let tradition: Tradition
    let liturgicalColor: String?
    let locationID: UUID?
    let sourceIDs: [UUID]
    let confidence: ConfidenceLabel
}

struct SourceCitation: Identifiable {
    let id: UUID
    let title: String
    let author: String?
    let url: String?
    let reliability: String
    let confidence: ConfidenceLabel
}

struct Artwork: Identifiable {
    let id: UUID
    let title: String
    let artist: String?
    let period: String?
    let sourceCredit: String?
}

struct RoutePack: Identifiable {
    let id: UUID
    let title: String
    let subtitle: String
    let region: String
    let traditionTags: [Tradition]
    let stopIDs: [UUID]
    let estimatedDistance: String
    let estimatedTime: String
    let isPremium: Bool
}

// ─── Journey / Passport Models (local-only) ──────────────

struct JourneySession: Identifiable {
    let id: UUID
    let routePackID: UUID?
    let startedAt: Date
    var endedAt: Date?
    var visitedLocationIDs: [UUID]
    var isActive: Bool
    var totalDistanceWalked: Double

    static func new(routePackID: UUID? = nil) -> JourneySession {
        JourneySession(
            id: UUID(),
            routePackID: routePackID,
            startedAt: Date(),
            endedAt: nil,
            visitedLocationIDs: [],
            isActive: true,
            totalDistanceWalked: 0
        )
    }
}

struct VisitedSite: Identifiable {
    let id: UUID
    let locationID: UUID
    let locationName: String
    let tradition: Tradition
    let visitedAt: Date
    var note: String?
    var prayer: String?

    var stampLabel: String {
        let f = DateFormatter()
        f.dateStyle = .medium
        return f.string(from: visitedAt)
    }
}

struct FieldNote: Identifiable {
    let id: UUID
    let locationID: UUID
    let createdAt: Date
    var text: String
}

// ─── Map Display Models ──────────────────────────────────

struct NearbySiteRow: Identifiable {
    let id: UUID
    let location: SacredLocation
    let distance: CLLocationDistance?
    let isTodayConnected: Bool
}
Swift

// MARK: - File: MockData.swift

import Foundation
import CoreLocation

enum MockData {

    // ─── Sources ──────────────────────────────────────────

    static let sources: [SourceCitation] = [
        SourceCitation(id: UUID(), title: "Butler's Lives of the Saints", author: "Alban Butler", url: nil, reliability: "Scholarly", confidence: .traditional),
        SourceCitation(id: UUID(), title: "Acta Sanctorum", author: "Bollandists", url: nil, reliability: "Scholarly", confidence: .traditional),
        SourceCitation(id: UUID(), title: "Catholic Encyclopedia (1913)", author: nil, url: nil, reliability: "Reference", confidence: .confirmed),
        SourceCitation(id: UUID(), title: "Eusebius, Ecclesiastical History", author: "Eusebius of Caesarea", url: nil, reliability: "Primary", confidence: .traditional),
        SourceCitation(id: UUID(), title: "Liber Pontificalis", author: nil, url: nil, reliability: "Primary", confidence: .traditional),
        SourceCitation(id: UUID(), title: "New Advent Catholic Encyclopedia", author: nil, url: nil, reliability: "Reference", confidence: .confirmed),
    ]

    // ─── Artworks ─────────────────────────────────────────

    static let artworks: [Artwork] = [
        Artwork(id: UUID(), title: "St. Peter in Prison", artist: "Gerrit van Honthorst", period: "c. 1618–1620", sourceCredit: "Gemäldegalerie, Berlin"),
        Artwork(id: UUID(), title: "The Martyrdom of St. Paul", artist: "Ludovico Carracci", period: "c. 1603–1604", sourceCredit: "Musei Vaticani"),
        Artwork(id: UUID(), title: "The Apparition at Lourdes", artist: "Émile-Hippolyte Motte", period: "19th century", sourceCredit: "Basilica of Lourdes"),
        Artwork(id: UUID(), title: "The Miracle of the Sun at Fatima", artist: "Unknown", period: "20th century", sourceCredit: "Sanctuary of Fátima"),
    ]

    // ─── Location IDs ─────────────────────────────────────

    static let mamertineID = UUID()
    static let stPetersID = UUID()
    static let stPaulOutsideID = UUID()
    static let sanSebastianoID = UUID()
    static let santaCroceID = UUID()
    static let sanLorenzoID = UUID()
    static let santaMariaMaggioreID = UUID()
    static let sanGiovanniID = UUID()
    static let holySepulchreID = UUID()
    static let viaDolorosaID = UUID()
    static let gethsemaneID = UUID()
    static let mountZionID = UUID()
    static let bethlehemID = UUID()
    static let santiagoID = UUID()
    static let lourdesID = UUID()
    static let fatimaID = UUID()
    static let assisiID = UUID()
    static let canterburyID = UUID()
    static let mountSinaiID = UUID()
    static let hagiaSophiaID = UUID()

    // ─── Route Pack IDs ───────────────────────────────────

    static let sevenChurchesPackID = UUID()
    static let passionWalkPackID = UUID()
    static let marianPackID = UUID()
    static let canterburyPackID = UUID()
    static let desertFathersPackID = UUID()
    static let constantinoplePackID = UUID()
    static let londonSaintsPackID = UUID()
    static let caminoPackID = UUID()

    // ─── Event IDs ────────────────────────────────────────

    private static let peterImprisonedID = UUID()
    private static let paulMartyrdomID = UUID()
    private static let councilNicaeaID = UUID()
    private static let francisStigmataID = UUID()
    private static let lourdesApparitionID = UUID()
    private static let fatimaApparitionID = UUID()
    private static let becketMartyrdomID = UUID()
    private static let jamesDiscoveryID = UUID()

    // ─── Locations ────────────────────────────────────────

    static let locations: [SacredLocation] = [
        SacredLocation(
            id: mamertineID, placeName: "Mamertine Prison",
            latitude: 41.8924, longitude: 12.4853,
            modernAddress: "Clivo Argentario 1, Rome", country: "Italy", region: "Lazio",
            traditions: [.catholic], categories: [.martyrdom, .relic],
            confidence: .traditional,
            whyThisPlaceMatters: "According to tradition, Saints Peter and Paul were imprisoned here before their martyrdoms under Nero. The Tullianum, the lowest chamber, is venerated as the site where Peter baptized his jailers with water miraculously springing from the floor.",
            associatedEventIDs: [peterImprisonedID],
            visitingHours: "9:00 AM – 7:00 PM (seasonal)", sourceCount: 5,
            routePackIDs: [sevenChurchesPackID], isTodayConnected: true
        ),
        SacredLocation(
            id: stPetersID, placeName: "St. Peter's Basilica",
            latitude: 41.9022, longitude: 12.4539,
            modernAddress: "Piazza San Pietro, Vatican City", country: "Vatican City", region: "Vatican",
            traditions: [.catholic], categories: [.martyrdom, .relic, .church],
            confidence: .confirmed,
            whyThisPlaceMatters: "Built over the traditional burial site of St. Peter, the first pope and apostle, martyred upside-down on the Vatican Hill c. 64 AD. The current basilica, consecrated in 1626, is the largest church in the world and the heart of Catholic Christendom.",
            associatedEventIDs: [peterImprisonedID],
            visitingHours: "7:00 AM – 7:00 PM", sourceCount: 12,
            routePackIDs: [sevenChurchesPackID], isTodayConnected: true
        ),
        SacredLocation(
            id: stPaulOutsideID, placeName: "Basilica of St. Paul Outside the Walls",
            latitude: 41.8570, longitude: 12.4756,
            modernAddress: "Via Ostiense 186, Rome", country: "Italy", region: "Lazio",
            traditions: [.catholic], categories: [.martyrdom, .church],
            confidence: .confirmed,
            whyThisPlaceMatters: "Built over the burial place of St. Paul, apostle to the Gentiles, beheaded under Nero c. 67 AD. The basilica's medallions depict every pope from Peter to Francis — the unbroken visual record of apostolic succession.",
            associatedEventIDs: [paulMartyrdomID],
            visitingHours: "7:00 AM – 6:30 PM", sourceCount: 8,
            routePackIDs: [sevenChurchesPackID], isTodayConnected: false
        ),
        SacredLocation(
            id: sanSebastianoID, placeName: "San Sebastiano fuori le Mura",
            latitude: 41.8791, longitude: 12.5049,
            modernAddress: "Via Appia Antica 136, Rome", country: "Italy", region: "Lazio",
            traditions: [.catholic], categories: [.martyrdom, .church, .relic],
            confidence: .traditional,
            whyThisPlaceMatters: "Built over the catacombs where St. Sebastian was buried after his martyrdom. The catacombs also temporarily housed the remains of Sts. Peter and Paul during the Valerian persecution. One of Rome's seven pilgrimage churches.",
            associatedEventIDs: [], visitingHours: "9:00 AM – 5:00 PM", sourceCount: 4,
            routePackIDs: [sevenChurchesPackID], isTodayConnected: false
        ),
        SacredLocation(
            id: santaCroceID, placeName: "Santa Croce in Gerusalemme",
            latitude: 41.8877, longitude: 12.5105,
            modernAddress: "Piazza di Santa Croce in Gerusalemme 12, Rome", country: "Italy", region: "Lazio",
            traditions: [.catholic], categories: [.relic, .church],
            confidence: .traditional,
            whyThisPlaceMatters: "Founded by St. Helena in the 4th century to house relics of the True Passion brought from Jerusalem — including fragments of the True Cross, thorns from the Crown, and a nail from the Crucifixion. The floor was covered with earth from Jerusalem, giving the church its name.",
            associatedEventIDs: [], visitingHours: "7:00 AM – 12:45 PM, 3:30 – 7:30 PM", sourceCount: 6,
            routePackIDs: [sevenChurchesPackID], isTodayConnected: false
        ),
        SacredLocation(
            id: sanLorenzoID, placeName: "San Lorenzo fuori le Mura",
            latitude: 41.8979, longitude: 12.5125,
            modernAddress: "Piazzale del Verano 3, Rome", country: "Italy", region: "Lazio",
            traditions: [.catholic], categories: [.martyrdom, .church],
            confidence: .confirmed,
            whyThisPlaceMatters: "Shrine of St. Lawrence the Deacon, martyred by being roasted on a gridiron in 258 AD. His cheerful last words — 'Turn me over, I'm done on this side' — made him the patron saint of cooks and comedians. The catacombs below are among Rome's oldest.",
            associatedEventIDs: [], visitingHours: "7:00 AM – 12:00 PM, 4:00 – 7:00 PM", sourceCount: 5,
            routePackIDs: [sevenChurchesPackID], isTodayConnected: false
        ),
        SacredLocation(
            id: santaMariaMaggioreID, placeName: "Santa Maria Maggiore",
            latitude: 41.8982, longitude: 12.4983,
            modernAddress: "Piazza di Santa Maria Maggiore 42, Rome", country: "Italy", region: "Lazio",
            traditions: [.catholic], categories: [.marian, .relic, .church],
            confidence: .confirmed,
            whyThisPlaceMatters: "The largest Marian church in Rome, built after the Council of Ephesus (431) affirmed Mary as Theotokos. According to tradition, the Virgin Mary appeared in a dream to Pope Liberius and outlined the plan of the church in snow — miraculously falling on the Esquiline Hill in August.",
            associatedEventIDs: [], visitingHours: "7:00 AM – 7:00 PM", sourceCount: 9,
            routePackIDs: [sevenChurchesPackID], isTodayConnected: false
        ),
        SacredLocation(
            id: sanGiovanniID, placeName: "San Giovanni in Laterano",
            latitude: 41.8851, longitude: 12.5060,
            modernAddress: "Piazza di San Giovanni in Laterano 4, Rome", country: "Italy", region: "Lazio",
            traditions: [.catholic], categories: [.church, .relic],
            confidence: .confirmed,
            whyThisPlaceMatters: "The cathedral of the Bishop of Rome — the pope's own church. Dedicated to Christ the Savior, St. John the Baptist, and St. John the Evangelist. The Lateran is the mother of all churches. The Scala Sancta, the Holy Stairs climbed by Christ during his Passion, stand across the square.",
            associatedEventIDs: [], visitingHours: "7:00 AM – 6:30 PM", sourceCount: 11,
            routePackIDs: [sevenChurchesPackID], isTodayConnected: true
        ),
        SacredLocation(
            id: holySepulchreID, placeName: "Church of the Holy Sepulchre",
            latitude: 31.7787, longitude: 35.2297,
            modernAddress: "Christian Quarter St, Jerusalem", country: "Israel", region: "Jerusalem",
            traditions: [.catholic, .orthodox], categories: [.biblical, .martyrdom, .shrine],
            confidence: .confirmed,
            whyThisPlaceMatters: "The most sacred site in Christendom. Built over the site of Christ's crucifixion at Golgotha and his burial and resurrection. Constantine's mother Helena identified the site in 326 AD. Six Christian denominations share custody under the Status Quo — a living testament to both unity and division.",
            associatedEventIDs: [], visitingHours: "5:00 AM – 8:00 PM (varies by season)", sourceCount: 15,
            routePackIDs: [passionWalkPackID], isTodayConnected: true
        ),
        SacredLocation(
            id: viaDolorosaID, placeName: "Via Dolorosa",
            latitude: 31.7804, longitude: 35.2307,
            modernAddress: "Old City, Jerusalem", country: "Israel", region: "Jerusalem",
            traditions: [.catholic, .orthodox], categories: [.biblical, .shrine],
            confidence: .traditional,
            whyThisPlaceMatters: "The traditional path walked by Christ from his condemnation to his crucifixion, marked by the fourteen Stations of the Cross. Pilgrims have walked these streets for over sixteen centuries. The route has shifted over time — the current fourteen-station form was formalized in the 18th century.",
            associatedEventIDs: [], visitingHours: "Open street", sourceCount: 7,
            routePackIDs: [passionWalkPackID], isTodayConnected: true
        ),
        SacredLocation(
            id: gethsemaneID, placeName: "Garden of Gethsemane",
            latitude: 31.7780, longitude: 35.2414,
            modernAddress: "Jerusalem", country: "Israel", region: "Jerusalem",
            traditions: [.catholic, .orthodox], categories: [.biblical, .shrine],
            confidence: .traditional,
            whyThisPlaceMatters: "Where Christ prayed in agony before his arrest: 'Father, if it be possible, let this cup pass from me.' The ancient olive trees in the garden may descend from those present at the time of Christ. The Church of All Nations stands at the rock of the agony.",
            associatedEventIDs: [], visitingHours: "8:00 AM – 5:30 PM", sourceCount: 6,
            routePackIDs: [passionWalkPackID], isTodayConnected: false
        ),
        SacredLocation(
            id: mountZionID, placeName: "Mount Zion — Cenacle",
            latitude: 31.7700, longitude: 35.2293,
            modernAddress: "Mount Zion, Jerusalem", country: "Israel", region: "Jerusalem",
            traditions: [.catholic, .jewish], categories: [.biblical, .shrine],
            confidence: .traditional,
            whyThisPlaceMatters: "Traditionally identified as the site of the Upper Room — the Cenacle — where Christ instituted the Eucharist at the Last Supper, where the Holy Spirit descended at Pentecost, and where the earliest Christians gathered in prayer. Also venerated as the tomb of King David.",
            associatedEventIDs: [], visitingHours: "8:00 AM – 6:00 PM", sourceCount: 5,
            routePackIDs: [passionWalkPackID], isTodayConnected: false
        ),
        SacredLocation(
            id: bethlehemID, placeName: "Church of the Nativity",
            latitude: 31.7054, longitude: 35.2027,
            modernAddress: "Manger Square, Bethlehem", country: "Palestine", region: "West Bank",
            traditions: [.catholic, .orthodox], categories: [.biblical, .shrine],
            confidence: .traditional,
            whyThisPlaceMatters: "Built over the cave venerated as the birthplace of Christ. The original basilica, commissioned by Constantine in 327 AD and rebuilt by Justinian in the 6th century, is one of the oldest continuously operating churches in the world. The star marking the exact spot reads: 'Here Jesus Christ was born of the Virgin Mary.'",
            associatedEventIDs: [], visitingHours: "6:30 AM – 4:30 PM (varies)", sourceCount: 10,
            routePackIDs: [], isTodayConnected: false
        ),
        SacredLocation(
            id: santiagoID, placeName: "Cathedral of Santiago de Compostela",
            latitude: 42.8806, longitude: -8.5445,
            modernAddress: "Praza do Obradoiro, Santiago de Compostela", country: "Spain", region: "Galicia",
            traditions: [.catholic], categories: [.relic, .church, .shrine],
            confidence: .traditional,
            whyThisPlaceMatters: "The destination of the Camino de Santiago, one of the three great pilgrimages of Christendom. The cathedral houses the relics of St. James the Greater, discovered here in the 9th century. Millions have walked these paths over a thousand years — the botafumeiro swings for them still.",
            associatedEventIDs: [jamesDiscoveryID],
            visitingHours: "7:00 AM – 9:00 PM", sourceCount: 8,
            routePackIDs: [caminoPackID], isTodayConnected: false
        ),
        SacredLocation(
            id: lourdesID, placeName: "Sanctuary of Our Lady of Lourdes",
            latitude: 43.0965, longitude: -0.0500,
            modernAddress: "1 Avenue Monseigneur Théas, Lourdes", country: "France", region: "Occitanie",
            traditions: [.catholic], categories: [.marian, .apparition, .shrine],
            confidence: .confirmed,
            whyThisPlaceMatters: "In 1858, the Virgin Mary appeared eighteen times to Bernadette Soubirous, a poor miller's daughter, in the grotto of Massabielle. The spring Bernadette uncovered at Mary's direction has been associated with thousands of documented healings. Seventy confirmed miracles are officially recognized.",
            associatedEventIDs: [lourdesApparitionID],
            visitingHours: "Open daily", sourceCount: 7,
            routePackIDs: [marianPackID], isTodayConnected: true
        ),
        SacredLocation(
            id: fatimaID, placeName: "Sanctuary of Fátima",
            latitude: 39.6172, longitude: -8.6762,
            modernAddress: "Fátima", country: "Portugal", region: "Santarém",
            traditions: [.catholic], categories: [.marian, .apparition, .shrine],
            confidence: .confirmed,
            whyThisPlaceMatters: "On May 13, 1917, the Virgin Mary appeared to three shepherd children — Lucia, Francisco, and Jacinta — revealing her message of prayer, penance, and peace. The Miracle of the Sun on October 13, witnessed by 70,000 people, remains one of the most widely attested events in modern religious history.",
            associatedEventIDs: [fatimaApparitionID],
            visitingHours: "Open daily", sourceCount: 9,
            routePackIDs: [marianPackID], isTodayConnected: false
        ),
        SacredLocation(
            id: assisiID, placeName: "Basilica of St. Francis of Assisi",
            latitude: 43.0707, longitude: 12.6044,
            modernAddress: "Piazza San Francesco, Assisi", country: "Italy", region: "Umbria",
            traditions: [.catholic], categories: [.church, .relic],
            confidence: .confirmed,
            whyThisPlaceMatters: "Burial place of St. Francis, the 13th-century friar who rebuilt the Church through radical poverty and joy. The basilica's fresco cycles by Giotto and Cimabue are cornerstones of Western art. Francis received the stigmata at nearby La Verna in 1224 — the first recorded case in Christian history.",
            associatedEventIDs: [francisStigmataID],
            visitingHours: "8:30 AM – 6:30 PM", sourceCount: 7,
            routePackIDs: [], isTodayConnected: false
        ),
        SacredLocation(
            id: canterburyID, placeName: "Canterbury Cathedral",
            latitude: 51.2799, longitude: 1.2597,
            modernAddress: "Cathedral House, 11 The Precincts, Canterbury", country: "England", region: "Kent",
            traditions: [.catholic, .orthodox], categories: [.martyrdom, .church],
            confidence: .confirmed,
            whyThisPlaceMatters: "Site of St. Thomas Becket's martyrdom in 1170, murdered in his own cathedral by four knights of King Henry II. The martyrdom transformed Canterbury into one of Europe's greatest pilgrimage destinations — the journey fictionalized in Chaucer's Canterbury Tales. Becket's shrine was destroyed in 1538; a candle still burns at the site.",
            associatedEventIDs: [becketMartyrdomID],
            visitingHours: "9:00 AM – 5:00 PM (Mon–Sat)", sourceCount: 6,
            routePackIDs: [canterburyPackID], isTodayConnected: false
        ),
        SacredLocation(
            id: mountSinaiID, placeName: "St. Catherine's Monastery, Mount Sinai",
            latitude: 28.5564, longitude: 33.9756,
            modernAddress: "South Sinai Governorate", country: "Egypt", region: "Sinai",
            traditions: [.catholic, .orthodox, .jewish, .islamic], categories: [.biblical, .monastery],
            confidence: .traditional,
            whyThisPlaceMatters: "Built at the foot of Mount Sinai where Moses received the Ten Commandments. The monastery, founded in the 6th century by Justinian, houses one of the oldest continuously operating libraries in the world, including the Codex Sinaiticus — one of the oldest nearly-complete Bibles in existence. A living bridge between Abrahamic traditions.",
            associatedEventIDs: [], visitingHours: "9:00 AM – 12:00 PM (Mon–Thu, Sat)", sourceCount: 8,
            routePackIDs: [desertFathersPackID], isTodayConnected: false
        ),
        SacredLocation(
            id: hagiaSophiaID, placeName: "Hagia Sophia",
            latitude: 41.0086, longitude: 28.9802,
            modernAddress: "Sultan Ahmet, Istanbul", country: "Turkey", region: "Istanbul",
            traditions: [.orthodox, .islamic], categories: [.church, .council],
            confidence: .confirmed,
            whyThisPlaceMatters: "Built by Emperor Justinian in 537 AD, Hagia Sophia — Holy Wisdom — was the largest cathedral in the world for nearly a thousand years. The Second Council of Nicaea (787) and other pivotal councils shaped Christian doctrine within its walls. Converted to a mosque in 1453, then a museum, then a mosque again. Its mosaics of Christ Pantocrator and the Theotokos endure beneath the calligraphy.",
            associatedEventIDs: [councilNicaeaID],
            visitingHours: "Limited (active mosque)", sourceCount: 11,
            routePackIDs: [constantinoplePackID], isTodayConnected: false
        ),
    ]

    // ─── Events ───────────────────────────────────────────

    static let events: [HistoricalEvent] = [
        HistoricalEvent(
            id: peterImprisonedID,
            date: Date().addingTimeInterval(-86400 * 2), // 2 days ago for "today" feel
            title: "St. Peter Imprisoned at the Mamertine",
            shortNarrative: "During the Neronian persecution, St. Peter was held in the Tullianum, the lower chamber of the Mamertine Prison. Tradition holds that he baptized his jailers Processus and Martinian with water that miraculously sprang from the stone floor.",
            tradition: .catholic, liturgicalColor: "red",
            locationID: mamertineID, sourceIDs: Array(sources.prefix(3)),
            confidence: .traditional
        ),
        HistoricalEvent(
            id: paulMartyrdomID,
            date: Date().addingTimeInterval(-86400 * 5),
            title: "St. Paul Beheaded on the Ostian Way",
            shortNarrative: "As a Roman citizen, Paul was beheaded rather than crucified. The site, Tre Fontane on the Via Ostia, is venerated as the place where his head bounced three times and three springs emerged.",
            tradition: .catholic, liturgicalColor: "red",
            locationID: stPaulOutsideID, sourceIDs: Array(sources.prefix(4)),
            confidence: .traditional
        ),
        HistoricalEvent(
            id: councilNicaeaID,
            date: Date().addingTimeInterval(-86400 * 100),
            title: "First Council of Nicaea Convenes",
            shortNarrative: "Called by Emperor Constantine in 325 AD, the council produced the Nicene Creed, affirming Christ's divinity against Arian claims. Over 300 bishops attended — the first ecumenical council of the Church.",
            tradition: .catholic, liturgicalColor: "white",
            locationID: nil, sourceIDs: Array(sources.suffix(3)),
            confidence: .confirmed
        ),
        HistoricalEvent(
            id: francisStigmataID,
            date: Date().addingTimeInterval(-86400 * 30),
            title: "St. Francis Receives the Stigmata",
            shortNarrative: "On Mount La Verna in 1224, St. Francis of Assisi became the first recorded person to receive the stigmata — the five wounds of Christ — while in deep prayer. He bore them until his death two years later.",
            tradition: .catholic, liturgicalColor: "white",
            locationID: assisiID, sourceIDs: Array(sources.prefix(2)),
            confidence: .confirmed
        ),
        HistoricalEvent(
            id: lourdesApparitionID,
            date: Date().addingTimeInterval(-86400 * 60),
            title: "Our Lady Appears at Lourdes",
            shortNarrative: "On February 11, 1858, the Virgin Mary appeared to Bernadette Soubirous at the grotto of Massabielle. Over eighteen apparitions, Mary identified herself as 'the Immaculate Conception' and directed Bernadette to dig a spring.",
            tradition: .catholic, liturgicalColor: "white",
            locationID: lourdesID, sourceIDs: Array(sources.suffix(2)),
            confidence: .confirmed
        ),
        HistoricalEvent(
            id: fatimaApparitionID,
            date: Date().addingTimeInterval(-86400 * 45),
            title: "Our Lady of Fátima Appears to the Children",
            shortNarrative: "On May 13, 1917, the Virgin Mary appeared to Lucia, Francisco, and Jacinta near Fátima, Portugal, calling for prayer and penance. The Miracle of the Sun on October 13 was witnessed by over 70,000 people.",
            tradition: .catholic, liturgicalColor: "white",
            locationID: fatimaID, sourceIDs: Array(sources.suffix(3)),
            confidence: .confirmed
        ),
        HistoricalEvent(
            id: becketMartyrdomID,
            date: Date().addingTimeInterval(-86400 * 10),
            title: "St. Thomas Becket Murdered in Canterbury Cathedral",
            shortNarrative: "On December 29, 1170, four knights of King Henry II murdered Archbishop Thomas Becket in his own cathedral. 'I am ready to die for my Lord,' he said, 'that in my blood the Church may obtain liberty and peace.'",
            tradition: .catholic, liturgicalColor: "red",
            locationID: canterburyID, sourceIDs: Array(sources.prefix(3)),
            confidence: .confirmed
        ),
        HistoricalEvent(
            id: jamesDiscoveryID,
            date: Date().addingTimeInterval(-86400 * 90),
            title: "Relics of St. James Discovered at Compostela",
            shortNarrative: "In the 9th century, the remains of St. James the Greater were discovered in Galicia, leading to the founding of Santiago de Compostela and the establishment of one of Christendom's great pilgrimages.",
            tradition: .catholic, liturgicalColor: "white",
            locationID: santiagoID, sourceIDs: Array(sources.prefix(2)),
            confidence: .traditional
        ),
    ]

    // ─── Route Packs ──────────────────────────────────────

    static let routePacks: [RoutePack] = [
        RoutePack(
            id: sevenChurchesPackID,
            title: "Seven Churches of Rome",
            subtitle: "The ancient station churches of the Eternal City",
            region: "Rome, Italy",
            traditionTags: [.catholic],
            stopIDs: [sanGiovanniID, stPetersID, stPaulOutsideID, santaMariaMaggioreID, sanLorenzoID, santaCroceID, sanSebastianoID],
            estimatedDistance: "11.8 mi", estimatedTime: "5–7 hours",
            isPremium: true
        ),
        RoutePack(
            id: passionWalkPackID,
            title: "Jerusalem: Passion Walk",
            subtitle: "Follow Christ's final hours in the Holy City",
            region: "Jerusalem",
            traditionTags: [.catholic, .orthodox],
            stopIDs: [mountZionID, gethsemaneID, viaDolorosaID, holySepulchreID],
            estimatedDistance: "1.5 mi", estimatedTime: "2–3 hours",
            isPremium: true
        ),
        RoutePack(
            id: marianPackID,
            title: "Marian Apparitions of Europe",
            subtitle: "The sites where the Virgin Mary appeared",
            region: "France, Portugal",
            traditionTags: [.catholic],
            stopIDs: [lourdesID, fatimaID],
            estimatedDistance: "Multi-city", estimatedTime: "3–5 days",
            isPremium: true
        ),
        RoutePack(
            id: canterburyPackID,
            title: "Canterbury Pilgrim Walk",
            subtitle: "In the footsteps of medieval pilgrims and martyrs",
            region: "Kent, England",
            traditionTags: [.catholic, .orthodox],
            stopIDs: [canterburyID],
            estimatedDistance: "Varies by route", estimatedTime: "1–3 days",
            isPremium: true
        ),
        RoutePack(
            id: desertFathersPackID,
            title: "Desert Fathers of Egypt",
            subtitle: "Where monasticism was born in the wilderness",
            region: "Sinai, Egypt",
            traditionTags: [.catholic, .orthodox],
            stopIDs: [mountSinaiID],
            estimatedDistance: "Multi-site", estimatedTime: "2–4 days",
            isPremium: true
        ),
        RoutePack(
            id: constantinoplePackID,
            title: "Constantinople and the Councils",
            subtitle: "Where doctrine was forged and empires met",
            region: "Istanbul, Turkey",
            traditionTags: [.orthodox, .catholic],
            stopIDs: [hagiaSophiaID],
            estimatedDistance: "3.2 mi", estimatedTime: "4–6 hours",
            isPremium: true
        ),
        RoutePack(
            id: londonSaintsPackID,
            title: "Saints of London",
            subtitle: "Martyrs, monasteries, and hidden sacred history",
            region: "London, England",
            traditionTags: [.catholic],
            stopIDs: [],
            estimatedDistance: "6.5 mi", estimatedTime: "Full day",
            isPremium: true
        ),
        RoutePack(
            id: caminoPackID,
            title: "Camino Sacred Stops",
            subtitle: "Key devotional sites along the Way of St. James",
            region: "Galicia, Spain",
            traditionTags: [.catholic],
            stopIDs: [santiagoID],
            estimatedDistance: "Varies", estimatedTime: "4–6 weeks",
            isPremium: true
        ),
    ]

    // ─── Helpers ──────────────────────────────────────────

    static func location(by id: UUID) -> SacredLocation? {
        locations.first { $0.id == id }
    }

    static func events(for locationID: UUID) -> [HistoricalEvent] {
        events.filter { $0.locationID == locationID }
    }

    static func routePack(by id: UUID) -> RoutePack? {
        routePacks.first { $0.id == id }
    }

    static func stops(for pack: RoutePack) -> [SacredLocation] {
        pack.stopIDs.compactMap { location(by: $0) }
    }

    static func locations(near coordinate: CLLocationCoordinate2D, radius: Double = 50_000) -> [NearbySiteRow] {
        let userLoc = CLLocation(latitude: coordinate.latitude, longitude: coordinate.longitude)
        return locations.compactMap { loc in
            let siteLoc = CLLocation(latitude: loc.latitude, longitude: loc.longitude)
            let distance = userLoc.distance(from: siteLoc)
            guard distance <= radius else { return nil }
            return NearbySiteRow(id: loc.id, location: loc, distance: distance, isTodayConnected: loc.isTodayConnected)
        }
        .sorted { ($0.distance ?? .infinity) < ($1.distance ?? .infinity) }
    }
}
Swift

// MARK: - File: L10n.swift

import Foundation

/// Localization abstraction for Anno Sacred Atlas.
/// In production, replace static strings with String(localized:table:bundle:)
/// backed by Localizable.xcstrings. Vietnamese equivalents documented in comments.
enum L10n {
    // ─── Tab & Navigation ─────────────────────────────────
    static let map             = "Map"               // Bản đồ
    static let today           = "Today"             // Hôm nay
    static let saved           = "Saved"             // Đã lưu
    static let nearby          = "Nearby"            // Gần đây
    static let explore         = "Explore"           // Khám phá

    // ─── Actions ──────────────────────────────────────────
    static let startPilgrimage = "Start Pilgrimage"  // Bắt đầu hành hương
    static let continueJourney = "Continue Journey"  // Tiếp tục hành trình
    static let endJourney      = "End Journey"       // Kết thúc hành trình
    static let pauseJourney    = "Pause"             // Tạm dừng
    static let resumeJourney   = "Resume"            // Tiếp tục
    static let save            = "Save"              // Lưu
    static let share           = "Share"             // Chia sẻ
    static let directions      = "Directions"        // Chỉ đường
    static let readMore        = "Read More"         // Đọc thêm
    static let addNote         = "Add Note"          // Thêm ghi chú
    static let viewSources     = "View Sources"      // Xem nguồn
    static let unlock          = "Unlock"            // Mở khóa

    // ─── Content Labels ───────────────────────────────────
    static let sources         = "Sources"           // Nguồn
    static let confirmed       = "Confirmed"         // Đã xác nhận
    static let traditional     = "Traditional"       // Theo truyền thống
    static let disputed        = "Disputed"          // Tranh luận
    static let confidence      = "Confidence"        // Độ tin cậy
    static let tradition       = "Tradition"         // Truyền thống
    static let category        = "Category"          // Phân loại

    // ─── Filter Options ───────────────────────────────────
    static let all             = "All"               // Tất cả
    static let catholic        = "Catholic"          // Công giáo
    static let orthodox        = "Orthodox"          // Chính thống
    static let jewish          = "Jewish"            // Do Thái
    static let islamic         = "Islamic"           // Hồi giáo
    static let interfaith      = "Interfaith"        // Liên tôn

    // ─── Feature Names ────────────────────────────────────
    static let sacredAtlas     = "Sacred Atlas"      // Bản đồ Thánh
    static let pilgrimMode     = "Pilgrim Mode"      // Chế độ Hành hương
    static let onThisGround    = "On This Ground"    // Trên mảnh đất này
    static let routePacks      = "Route Packs"       // Lộ trình
    static let passport        = "Passport"          // Hộ chiếu
    static let fieldNotes      = "Field Notes"       // Ghi chú hành trình
    static let visited         = "Visited"           // Đã thăm
    static let stamps          = "Stamps"            // Con dấu

    // ─── Premium ──────────────────────────────────────────
    static let unlockAtlas     = "Unlock the Sacred Atlas"
    static let atlasDescription = "Explore 2,400+ sacred sites, source-backed place histories, curated pilgrimage routes, and your private pilgrimage passport."
    static let unlockRoute     = "Unlock Full Route"
    static let sitesAvailable  = "sites available in preview"

    // ─── Nearby ───────────────────────────────────────────
    static let nearYouTitle    = "Near You in Sacred History"
    static let connectedToday  = "Connected to today"
    static let noLocationTitle = "Explore Sacred History"
    static let noLocationMessage = "Allow location to discover sacred sites near you, or browse the atlas manually."

    // ─── Passport ─────────────────────────────────────────
    static let sitesVisitedCount = "sites visited"
    static let routesCompleted   = "routes completed"
    static let notesWritten      = "notes written"
    static let noVisitsYet       = "Your passport awaits"
    static let noVisitsSubtitle  = "Start a pilgrimage or visit sacred sites to collect stamps."

    // ─── Pilgrim Mode ────────────────────────────────────
    static let nextStop       = "Next Stop"
    static let journeyComplete = "Journey Complete"
    static let distanceToNext  = "Distance to next"
    static let stopsVisited    = "stops visited"

    // ─── Distance Formatting ──────────────────────────────
    static func distanceString(_ meters: Double) -> String {
        if meters < 1000 {
            return String(format: "%.0f m", meters)
        } else if meters < 1600 {
            return String(format: "%.1f km", meters / 1000)
        } else {
            return String(format: "%.1f mi", meters / 1609.34)
        }
    }
}
Swift

// MARK: - File: Theme.swift

import SwiftUI

// ─── Color System ────────────────────────────────────────

extension Color {
    static let annoGold         = Color(red: 0.788, green: 0.659, blue: 0.298)
    static let annoGoldLight    = Color(red: 0.918, green: 0.839, blue: 0.588)
    static let annoIvory        = Color(red: 1.000, green: 1.000, blue: 0.941)
    static let annoParchment    = Color(red: 0.961, green: 0.933, blue: 0.867)
    static let annoDeepNavy     = Color(red: 0.071, green: 0.078, blue: 0.137)
    static let annoDarkSurface  = Color(red: 0.098, green: 0.106, blue: 0.173)
    static let annoCardDark     = Color(red: 0.118, green: 0.125, blue: 0.200)
    static letannoSubtext       = Color(red: 0.596, green: 0.596, blue: 0.639)

    // Tradition accent colors
    static let catholicAccent   = Color(red: 0.831, green: 0.686, blue: 0.216)
    static let orthodoxAccent   = Color(red: 0.498, green: 0.271, blue: 0.525)
    static let jewishAccent     = Color(red: 0.180, green: 0.333, blue: 0.710)
    static let islamicAccent    = Color(red: 0.137, green: 0.510, blue: 0.263)
    static let interfaithAccent = Color(red: 0.576, green: 0.333, blue: 0.655)

    static func traditionColor(_ tradition: Tradition) -> Color {
        switch tradition {
        case .catholic:   return .catholicAccent
        case .orthodox:   return .orthodoxAccent
        case .jewish:     return .jewishAccent
        case .islamic:    return .islamicAccent
        case .interfaith: return .interfaithAccent
        }
    }

    static func confidenceColor(_ confidence: ConfidenceLabel) -> Color {
        switch confidence {
        case .confirmed:   return .green
        case .traditional: return .annoGold
        case .disputed:    return .orange
        }
    }
}

// ─── Typography ──────────────────────────────────────────

extension Font {
    static let annoSerifTitle = Font.system(size: 28, weight: .bold, design: .serif)
    static let annoSerifHeading = Font.system(size: 20, weight: .semibold, design: .serif)
    static let annoSerifSubheading = Font.system(size: 16, weight: .medium, design: .serif)
    static let annoSerifCaption = Font.system(size: 13, weight: .regular, design: .serif)
    static let annoBody = Font.system(.body, design: .default)
    static let annoCaption = Font.system(.caption, design: .default)
}

// ─── Spacing & Sizing ────────────────────────────────────

enum AnnoSpacing {
    static let xs: CGFloat = 4
    static let sm: CGFloat = 8
    static let md: CGFloat = 12
    static let lg: CGFloat = 16
    static let xl: CGFloat = 24
    static let xxl: CGFloat = 32
}

// ─── View Modifiers ──────────────────────────────────────

struct ParchmentCard: ViewModifier {
    @Environment(\.colorScheme) private var colorScheme
    func body(content: Content) -> some View {
        content
            .padding(AnnoSpacing.lg)
            .background(colorScheme == .dark ? Color.annoCardDark : Color.annoParchment)
            .clipShape(RoundedRectangle(cornerRadius: 14, style: .continuous))
            .shadow(color: .black.opacity(colorScheme == .dark ? 0.4 : 0.1),
                    radius: 8, y: 4)
    }
}

extension View {
    func parchmentCard() -> some View {
        modifier(ParchmentCard())
    }
}
Wait, I have a typo: static letannoSubtext should be static let annoSubtext. Let me fix that and continue.

Let me continue writing all the files. I'll be more careful with syntax.

Swift

// MARK: - File: Services.swift

import Foundation
import CoreLocation
import SwiftUI

// ─── Location Manager ────────────────────────────────────

@Observable
class AnnoLocationManager: NSObject, CLLocationManagerDelegate {
    private let manager = CLLocationManager()
    var currentLocation: CLLocation?
    var authorizationStatus: CLAuthorizationStatus = .notDetermined
    var isLocating: Bool = false

    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyHundredMeters
    }

    func requestWhenInUseAuthorization() {
        manager.requestWhenInUseAuthorization()
    }

    func startUpdating() {
        guard authorizationStatus == .authorizedWhenInUse || authorizationStatus == .authorizedAlways else { return }
        isLocating = true
        manager.startUpdatingLocation()
    }

    func stopUpdating() {
        isLocating = false
        manager.stopUpdatingLocation()
    }

    // CLLocationManagerDelegate
    nonisolated func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        Task { @MainActor in
            currentLocation = locations.last
        }
    }

    nonisolated func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        Task { @MainActor in
            authorizationStatus = manager.authorizationStatus
            if manager.authorizationStatus == .authorizedWhenInUse || manager.authorizationStatus == .authorizedAlways {
                startUpdating()
            }
        }
    }
}

// ─── Pilgrim Session Store ───────────────────────────────

@Observable
class PilgrimSessionStore {
    var activeJourney: JourneySession?
    var visitedSites: [VisitedSite] = []
    var fieldNotes: [FieldNote] = []
    var completedJourneys: [JourneySession] = []

    var hasActiveJourney: Bool { activeJourney?.isActive == true }

    var totalSitesVisited: Int { visitedSites.count }
    var totalRoutesCompleted: Int { completedJourneys.count }
    var totalNotesWritten: Int { fieldNotes.count }

    func startJourney(routePackID: UUID? = nil) {
        activeJourney = JourneySession.new(routePackID: routePackID)
    }

    func visitSite(_ locationID: UUID, name: String, tradition: Tradition) {
        guard let journey = activeJourney else { return }
        let site = VisitedSite(
            id: UUID(),
            locationID: locationID,
            locationName: name,
            tradition: tradition,
            visitedAt: Date()
        )
        visitedSites.append(site)
        activeJourney?.visitedLocationIDs.append(locationID)
    }

    func addFieldNote(locationID: UUID, text: String) {
        let note = FieldNote(id: UUID(), locationID: locationID, createdAt: Date(), text: text)
        fieldNotes.append(note)
    }

    func pauseJourney() {
        activeJourney?.isActive = false
    }

    func resumeJourney() {
        activeJourney?.isActive = true
    }

    func endJourney() {
        guard var journey = activeJourney else { return }
        journey.endedAt = Date()
        journey.isActive = false
        completedJourneys.append(journey)
        activeJourney = nil
    }

    func hasVisited(_ locationID: UUID) -> Bool {
        visitedSites.contains { $0.locationID == locationID }
    }
}
Swift

// MARK: - File: AtlasViewModel.swift

import SwiftUI
import MapKit
import CoreLocation

@Observable
class AtlasViewModel {
    // ─── Map State ────────────────────────────────────────
    var cameraPosition: MapCameraPosition = .region(
        MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: 41.9022, longitude: 12.4539),
            span: MKCoordinateSpan(latitudeDelta: 0.12, longitudeDelta: 0.12)
        )
    )
    var selectedLocationID: UUID?
    var isShowingLocationDetail = false

    // ─── Filters ──────────────────────────────────────────
    var filterTradition: Tradition?
    var filterCategory: SacredCategory?
    var filterConfidence: ConfidenceLabel?
    var showNearbyOnly = false
    var showTodayOnly = false

    // ─── Panels ───────────────────────────────────────────
    var isNearbyExpanded = false
    var isShowingRoutePacks = false
    var isShowingPassport = false
    var isShowingPilgrimMode = false
    var isShowingPremium = false

    // ─── Entitlement ──────────────────────────────────────
    var entitlement: EntitlementTier = .free

    // ─── Data ─────────────────────────────────────────────
    var allLocations: [SacredLocation] = MockData.locations
    var allRoutePacks: [RoutePack] = MockData.routePacks

    // ─── Services ─────────────────────────────────────────
    var locationManager = AnnoLocationManager()
    var pilgrimStore = PilgrimSessionStore()

    // ─── Computed ─────────────────────────────────────────

    var selectedLocation: SacredLocation? {
        guard let id = selectedLocationID else { return nil }
        return allLocations.first { $0.id == id }
    }

    var filteredLocations: [SacredLocation] {
        var result = allLocations

        if let tradition = filterTradition {
            result = result.filter { $0.traditions.contains(tradition) }
        }
        if let category = filterCategory {
            result = result.filter { $0.categories.contains(category) }
        }
        if let confidence = filterConfidence {
            result = result.filter { $0.confidence == confidence }
        }
        if showTodayOnly {
            result = result.filter { $0.isTodayConnected }
        }
        if showNearbyOnly, let userLoc = locationManager.currentLocation {
            let userCoord = userLoc.coordinate
            result = result.filter { loc in
                let siteLoc = CLLocation(latitude: loc.latitude, longitude: loc.longitude)
                return userLoc.distance(from: siteLoc) <= 50_000 // 50 km
            }
        }

        return result
    }

    var nearbySites: [NearbySiteRow] {
        guard let userLoc = locationManager.currentLocation else { return [] }
        return MockData.locations(near: userLoc.coordinate, radius: 100_000)
    }

    var freeNearbySites: [NearbySiteRow] {
        Array(nearbySites.prefix(3))
    }

    var todayConnectedNearby: [NearbySiteRow] {
        nearbySites.filter { $0.isTodayConnected }
    }

    // ─── Entitlement Logic ────────────────────────────────

    func isLocationLocked(_ location: SacredLocation) -> Bool {
        if entitlement == .premium { return false }
        // Free users can see: today-connected, and first 3 nearby
        if location.isTodayConnected { return false }
        if let userLoc = locationManager.currentLocation {
            let siteLoc = CLLocation(latitude: location.latitude, longitude: location.longitude)
            let distance = userLoc.distance(from: siteLoc)
            if distance <= 50_000 {
                let freeNearby = freeNearbySites.map(\.location.id)
                if freeNearby.contains(location.id) { return false }
            }
        }
        return true
    }

    func isRoutePackLocked(_ pack: RoutePack) -> Bool {
        if entitlement == .premium { return false }
        return pack.isPremium
    }

    func previewStops(for pack: RoutePack) -> [SacredLocation] {
        let stops = MockData.stops(for: pack)
        if entitlement == .premium { return stops }
        return Array(stops.prefix(2))
    }

    var lockedPinCount: Int {
        filteredLocations.filter { isLocationLocked($0) }.count
    }

    // ─── Actions ──────────────────────────────────────────

    func selectLocation(_ id: UUID?) {
        selectedLocationID = id
        if id != nil {
            isShowingLocationDetail = true
        }
    }

    func centerOnUser() {
        if let location = locationManager.currentLocation {
            withAnimation {
                cameraPosition = .region(
                    MKCoordinateRegion(
                        center: location.coordinate,
                        span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05)
                    )
                )
            }
        } else {
            locationManager.requestWhenInUseAuthorization()
        }
    }

    func centerOnRome() {
        withAnimation {
            cameraPosition = .region(
                MKCoordinateRegion(
                    center: CLLocationCoordinate2D(latitude: 41.9022, longitude: 12.4539),
                    span: MKCoordinateSpan(latitudeDelta: 0.12, longitudeDelta: 0.12)
                )
            )
        }
    }

    func centerOnJerusalem() {
        withAnimation {
            cameraPosition = .region(
                MKCoordinateRegion(
                    center: CLLocationCoordinate2D(latitude: 31.7787, longitude: 35.2297),
                    span: MKCoordinateSpan(latitudeDelta: 0.08, longitudeDelta: 0.08)
                )
            )
        }
    }

    func clearFilters() {
        filterTradition = nil
        filterCategory = nil
        filterConfidence = nil
        showNearbyOnly = false
        showTodayOnly = false
    }

    var hasActiveFilters: Bool {
        filterTradition != nil || filterCategory != nil || filterConfidence != nil || showNearbyOnly || showTodayOnly
    }
}
Swift

// MARK: - File: SharedComponents.swift

import SwiftUI

// ─── Tradition Badge ─────────────────────────────────────

struct TraditionBadge: View {
    let tradition: Tradition
    var compact: Bool = false

    var body: some View {
        Text(traditionLabel)
            .font(compact ? .annoCaption : .annoCaption)
            .fontWeight(.semibold)
            .foregroundStyle(.white)
            .padding(.horizontal, compact ? 6 : 8)
            .padding(.vertical, compact ? 2 : 3)
            .background(Color.traditionColor(tradition))
            .clipShape(Capsule())
    }

    private var traditionLabel: String {
        switch tradition {
        case .catholic:   L10n.catholic
        case .orthodox:   L10n.orthodox
        case .jewish:     L10n.jewish
        case .islamic:    L10n.islamic
        case .interfaith: L10n.interfaith
        }
    }
}

// ─── Confidence Badge ────────────────────────────────────

struct ConfidenceBadge: View {
    let confidence: ConfidenceLabel

    var body: some View {
        HStack(spacing: 4) {
            Circle()
                .fill(Color.confidenceColor(confidence))
                .frame(width: 6, height: 6)
            Text(label)
                .font(.annoCaption)
                .fontWeight(.medium)
                .foregroundStyle(Color.confidenceColor(confidence))
        }
    }

    private var label: String {
        switch confidence {
        case .confirmed:   L10n.confirmed
        case .traditional: L10n.traditional
        case .disputed:    L10n.disputed
        }
    }
}

// ─── Gold Divider ────────────────────────────────────────

struct GoldDivider: View {
    var body: some View {
        Rectangle()
            .fill(Color.annoGold.opacity(0.3))
            .frame(height: 0.5)
    }
}

// ─── Category Chip ───────────────────────────────────────

struct CategoryChip: View {
    let category: SacredCategory
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(categoryLabel)
                .font(.annoCaption)
                .fontWeight(isSelected ? .semibold : .regular)
                .foregroundStyle(isSelected ? Color.annoGold : .secondary)
                .padding(.horizontal, 10)
                .padding(.vertical, 5)
                .background(
                    RoundedRectangle(cornerRadius: 8, style: .continuous)
                        .fill(isSelected ? Color.annoGold.opacity(0.15) : Color.clear)
                )
                .overlay(
                    RoundedRectangle(cornerRadius: 8, style: .continuous)
                        .strokeBorder(isSelected ? Color.annoGold.opacity(0.4) : Color.secondary.opacity(0.3), lineWidth: 0.5)
                )
        }
        .buttonStyle(.plain)
    }

    private var categoryLabel: String {
        switch category {
        case .martyrdom: return "Martyrs"
        case .relic:     return "Relics"
        case .marian:    return "Marian"
        case .monastery: return "Monasteries"
        case .biblical:  return "Biblical"
        case .council:   return "Councils"
        case .shrine:    return "Shrines"
        case .church:    return "Churches"
        case .apparition: return "Apparitions"
        }
    }
}

// ─── Pilgrim Stamp View ─────────────────────────────────

struct StampView: View {
    let site: VisitedSite
    @Environment(\.colorScheme) private var colorScheme

    var body: some View {
        VStack(spacing: AnnoSpacing.sm) {
            ZStack {
                Circle()
                    .stroke(Color.traditionColor(site.tradition), lineWidth: 2)
                    .frame(width: 56, height: 56)
                Circle()
                    .fill(Color.traditionColor(site.tradition).opacity(0.12))
                    .frame(width: 50, height: 50)
                Image(systemName: "checkmark.seal.fill")
                    .foregroundStyle(Color.traditionColor(site.tradition))
                    .font(.title3)
            }
            Text(site.locationName)
                .font(.annoSerifCaption)
                .foregroundStyle(colorScheme == .dark ? .annoIvory : .primary)
                .lineLimit(2)
                .multilineTextAlignment(.center)
            Text(site.stampLabel)
                .font(.annoCaption)
                .foregroundStyle(.secondary)
        }
        .frame(width: 100)
    }
}

// ─── On This Ground Banner ───────────────────────────────

struct OnThisGroundBanner: View {
    let location: SacredLocation

    var body: some View {
        VStack(alignment: .leading, spacing: AnnoSpacing.sm) {
            HStack {
                Image(systemName: "location.fill")
                    .foregroundStyle(Color.annoGold)
                    .font(.caption)
                Text(L10n.onThisGround)
                    .font(.annoSerifSubheading)
                    .foregroundStyle(Color.annoGold)
            }
            Text(location.whyThisPlaceMatters)
                .font(.annoBody)
                .foregroundStyle(.primary)
                .lineLimit(4)
            HStack(spacing: AnnoSpacing.lg) {
                ConfidenceBadge(confidence: location.confidence)
                Text("\(location.sourceCount) \(L10n.sources.lowercased())")
                    .font(.annoCaption)
                    .foregroundStyle(.secondary)
            }
        }
        .padding()
        .background(.ultraThinMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 14, style: .continuous))
    }
}

// ─── Empty State View ────────────────────────────────────

struct EmptyStateView: View {
    let icon: String
    let title: String
    let subtitle: String

    var body: some View {
        VStack(spacing: AnnoSpacing.lg) {
            Image(systemName: icon)
                .font(.system(size: 40))
                .foregroundStyle(Color.annoGold.opacity(0.5))
            Text(title)
                .font(.annoSerifSubheading)
                .foregroundStyle(.secondary)
            Text(subtitle)
                .font(.annoCaption)
                .foregroundStyle(.tertiary)
                .multilineTextAlignment(.center)
        }
        .padding(AnnoSpacing.xl)
    }
}
Swift

// MARK: - File: SacredAtlasView.swift

import SwiftUI
import MapKit

struct SacredAtlasView: View {
    @State private var viewModel = AtlasViewModel()
    @Environment(\.colorScheme) private var colorScheme

    var body: some View {
        ZStack {
            // ─── Map Layer ────────────────────────────────
            mapLayer
                .ignoresSafeArea()

            // ─── Top Overlay: Filters ─────────────────────
            VStack {
                filterBar
                Spacer()
            }

            // ─── Bottom Overlay ───────────────────────────
            VStack {
                Spacer()
                if viewModel.selectedLocationID != nil {
                    locationCard
                } else {
                    nearbyPanel
                }
            }

            // ─── Floating Controls ────────────────────────
            floatingControls
        }
        .sheet(isPresented: $viewModel.isShowingLocationDetail) {
            if let location = viewModel.selectedLocation {
                LocationDetailView(
                    location: location,
                    viewModel: viewModel
                )
            }
        }
        .sheet(isPresented: $viewModel.isShowingRoutePacks) {
            RoutePackListView(viewModel: viewModel)
        }
        .sheet(isPresented: $viewModel.isShowingPassport) {
            PassportView(store: viewModel.pilgrimStore)
        }
        .fullScreenCover(isPresented: $viewModel.isShowingPilgrimMode) {
            PilgrimModeView(viewModel: viewModel)
        }
        .sheet(isPresented: $viewModel.isShowingPremium) {
            PremiumUnlockView()
        }
    }

    // ─── Map ──────────────────────────────────────────────

    private var mapLayer: some View {
        Map(position: $viewModel.cameraPosition, selection: $viewModel.selectedLocationID) {
            UserAnnotation()

            ForEach(viewModel.filteredLocations) { location in
                Annotation(location.placeName, coordinate: location.coordinate) {
                    SacredPinView(
                        tradition: location.traditions.first ?? .catholic,
                        isTodayConnected: location.isTodayConnected,
                        isLocked: viewModel.isLocationLocked(location),
                        isSelected: viewModel.selectedLocationID == location.id
                    )
                }
                .tag(location.id)
            }

            // Route polyline if pilgrim mode active
            if let journey = viewModel.pilgrimStore.activeJourney,
               let packID = journey.routePackID,
               let pack = viewModel.allRoutePacks.first(where: { $0.id == packID }) {
                let stops = MockData.stops(for: pack)
                if stops.count >= 2 {
                    MapPolyline(coordinates: stops.map(\.coordinate))
                        .stroke(Color.annoGold.opacity(0.6), style: StrokeStyle(lineWidth: 3, lineCap: .round, lineJoin: .round))
                }
            }
        }
        .mapStyle(.standard(emphasis: .muted))
        .mapControls {
            MapCompass()
            MapScaleView()
        }
    }

    // ─── Filter Bar ───────────────────────────────────────

    private var filterBar: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: AnnoSpacing.sm) {
                // Today filter
                FilterChip(
                    label: L10n.today,
                    icon: "sun.max",
                    isSelected: viewModel.showTodayOnly,
                    action: { viewModel.showTodayOnly.toggle() }
                )

                // Tradition filters
                ForEach(Tradition.allCases) { tradition in
                    FilterChip(
                        label: traditionLabel(tradition),
                        icon: nil,
                        isSelected: viewModel.filterTradition == tradition,
                        color: Color.traditionColor(tradition),
                        action: {
                            withAnimation(.easeInOut(duration: 0.2)) {
                                viewModel.filterTradition = viewModel.filterTradition == tradition ? nil : tradition
                            }
                        }
                    )
                }

                // Confidence filter
                Menu {
                    ForEach(ConfidenceLabel.allCases) { conf in
                        Button {
                            viewModel.filterConfidence = viewModel.filterConfidence == conf ? nil : conf
                        } label: {
                            Label(confLabel(conf), systemImage: viewModel.filterConfidence == conf ? "checkmark" : "")
                        }
                    }
                } label: {
                    FilterChip(
                        label: viewModel.filterConfidence.map(confLabel) ?? L10n.confidence,
                        icon: "shield.checkered",
                        isSelected: viewModel.filterConfidence != nil,
                        action: {} // handled by menu
                    )
                }

                // Clear
                if viewModel.hasActiveFilters {
                    Button {
                        withAnimation { viewModel.clearFilters() }
                    } label: {
                        Image(systemName: "xmark.circle.fill")
                            .foregroundStyle(.secondary)
                            .font(.caption)
                    }
                }
            }
            .padding(.horizontal, AnnoSpacing.lg)
            .padding(.top, 8)
        }
        .padding(.top, 4)
    }

    // ─── Nearby Panel ─────────────────────────────────────

    private var nearbyPanel: some View {
        VStack(spacing: 0) {
            // Drag handle
            Capsule()
                .fill(Color.secondary.opacity(0.3))
                .frame(width: 36, height: 4)
                .padding(.top, 8)
                .padding(.bottom, 4)

            // Header
            HStack {
                VStack(alignment: .leading, spacing: 2) {
                    Text(L10n.nearYouTitle)
                        .font(.annoSerifSubheading)
                        .foregroundStyle(colorScheme == .dark ? .annoIvory : .primary)
                    if !viewModel.nearbySites.isEmpty {
                        Text("\(viewModel.nearbySites.count) sacred sites within 100 km")
                            .font(.annoCaption)
                            .foregroundStyle(.secondary)
                    }
                }
                Spacer()
                Button { viewModel.isNearbyExpanded.toggle() } label: {
                    Image(systemName: viewModel.isNearbyExpanded ? "chevron.down" : "chevron.up")
                        .foregroundStyle(.secondary)
                }
            }
            .padding(.horizontal, AnnoSpacing.lg)
            .padding(.vertical, AnnoSpacing.sm)

            if viewModel.isNearbyExpanded || viewModel.nearbySites.isEmpty {
                expandedNearbyContent
            } else {
                collapsedNearbyContent
            }
        }
        .background(.ultraThinMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
        .padding(.horizontal, AnnoSpacing.sm)
        .padding(.bottom, 4)
    }

    private var collapsedNearbyContent: some View {
        VStack(spacing: 0) {
            // Today-connected highlight
            if !viewModel.todayConnectedNearby.isEmpty {
                ForEach(viewModel.todayConnectedNearby.prefix(2)) { row in
                    nearbyRow(row, highlightToday: true)
                }
            }

            // Top 3 nearby
            ForEach(viewModel.freeNearbySites.filter { !$0.isTodayConnected }.prefix(3)) { row in
                nearbyRow(row)
            }

            // Premium tease
            if viewModel.entitlement == .free && viewModel.nearbySites.count > 3 {
                premiumNearbyTease
            }

            // No location state
            if viewModel.nearbySites.isEmpty {
                noLocationState
            }
        }
        .padding(.bottom, AnnoSpacing.sm)
    }

    private var expandedNearbyContent: some View {
        ScrollView(.vertical, showsIndicators: false) {
            LazyVStack(spacing: AnnoSpacing.xs) {
                ForEach(viewModel.nearbySites.prefix(20)) { row in
                    nearbyRow(row, highlightToday: row.isTodayConnected)
                }

                if viewModel.entitlement == .free && viewModel.nearbySites.count > 3 {
                    premiumNearbyTease
                }

                if viewModel.nearbySites.isEmpty {
                    noLocationState
                }
            }
        }
        .frame(maxHeight: 300)
        .padding(.bottom, AnnoSpacing.sm)
    }

    private func nearbyRow(_ row: NearbySiteRow, highlightToday: Bool = false) -> some View {
        Button {
            viewModel.selectedLocationID = row.location.id
            viewModel.isShowingLocationDetail = true
        } label: {
            HStack(spacing: AnnoSpacing.md) {
                // Tradition dot
                Circle()
                    .fill(Color.traditionColor(row.location.traditions.first ?? .catholic))
                    .frame(width: 10, height: 10)

                VStack(alignment: .leading, spacing: 2) {
                    HStack(spacing: AnnoSpacing.xs) {
                        Text(row.location.placeName)
                            .font(.annoSerifCaption)
                            .foregroundStyle(.primary)
                            .lineLimit(1)
                        if highlightToday {
                            Text("● \(L10n.connectedToday)")
                                .font(.system(size: 10, weight: .semibold))
                                .foregroundStyle(Color.annoGold)
                        }
                    }
                    Text(row.location.country)
                        .font(.annoCaption)
                        .foregroundStyle(.secondary)
                }

                Spacer()

                if let distance = row.distance {
                    Text(L10n.distanceString(distance))
                        .font(.annoCaption)
                        .foregroundStyle(.secondary)
                }
            }
            .padding(.horizontal, AnnoSpacing.lg)
            .padding(.vertical, AnnoSpacing.sm)
        }
        .buttonStyle(.plain)
    }

    private var premiumNearbyTease: some View {
        Button {
            viewModel.isShowingPremium = true
        } label: {
            HStack {
                VStack(alignment: .leading, spacing: 2) {
                    Text("Unlock \(viewModel.nearbySites.count) nearby sites")
                        .font(.annoSerifCaption)
                        .foregroundStyle(Color.annoGold)
                    Text("Full Sacred Atlas access")
                        .font(.annoCaption)
                        .foregroundStyle(Color.annoGold.opacity(0.7))
                }
                Spacer()
                Image(systemName: "lock.fill")
                    .foregroundStyle(Color.annoGold)
                    .font(.caption)
            }
            .padding(.horizontal, AnnoSpacing.lg)
            .padding(.vertical, AnnoSpacing.md)
            .background(Color.annoGold.opacity(0.08))
        }
        .buttonStyle(.plain)
    }

    private var noLocationState: some View {
        VStack(spacing: AnnoSpacing.md) {
            Image(systemName: "location.slash")
                .font(.title2)
                .foregroundStyle(.secondary)
            Text(L10n.noLocationTitle)
                .font(.annoSerifSubheading)
            Text(L10n.noLocationMessage)
                .font(.annoCaption)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
            Button {
                viewModel.locationManager.requestWhenInUseAuthorization()
            } label: {
                Text("Enable Location")
                    .font(.annoCaption)
                    .fontWeight(.semibold)
                    .foregroundStyle(.white)
                    .padding(.horizontal, AnnoSpacing.lg)
                    .padding(.vertical, AnnoSpacing.sm)
                    .background(Color.annoGold)
                    .clipShape(Capsule())
            }
        }
        .padding(AnnoSpacing.xl)
    }

    // ─── Location Card (selected pin) ────────────────────

    private var locationCard: some View {
        Group {
            if let location = viewModel.selectedLocation {
                LocationCardView(
                    location: location,
                    isLocked: viewModel.isLocationLocked(location),
                    isVisited: viewModel.pilgrimStore.hasVisited(location.id),
                    onTap: { viewModel.isShowingLocationDetail = true },
                    onDirections: { openDirections(to: location) },
                    onSave: { /* save action */ },
                    onStartPilgrimage: {
                        viewModel.pilgrimStore.startJourney()
                        viewModel.pilgrimStore.visitSite(
                            location.id, name: location.placeName,
                            tradition: location.traditions.first ?? .catholic
                        )
                        viewModel.isShowingPilgrimMode = true
                    },
                    onUnlock: { viewModel.isShowingPremium = true }
                )
            }
        }
    }

    // ─── Floating Controls ────────────────────────────────

    private var floatingControls: some View {
        VStack {
            Spacer()
            HStack {
                VStack(spacing: AnnoSpacing.sm) {
                    // Route packs
                    FloatingButton(icon: "map") {
                        viewModel.isShowingRoutePacks = true
                    }
                    // Passport
                    FloatingButton(icon: "book.closed") {
                        viewModel.isShowingPassport = true
                    }
                    // Pilgrim mode (if active journey)
                    if viewModel.pilgrimStore.hasActiveJourney {
                        FloatingButton(icon: "figure.walk", badge: "•") {
                            viewModel.isShowingPilgrimMode = true
                        }
                    }
                }

                Spacer()

                VStack(spacing: AnnoSpacing.sm) {
                    // Quick nav
                    Menu {
                        Button("Rome") { viewModel.centerOnRome() }
                        Button("Jerusalem") { viewModel.centerOnJerusalem() }
                    } label: {
                        Image(systemName: "globe")
                            .frame(width: 40, height: 40)
                            .background(.ultraThinMaterial)
                            .clipShape(Circle())
                            .shadow(radius: 3)
                    }

                    // Locate me
                    FloatingButton(icon: "location.fill") {
                        viewModel.centerOnUser()
                    }
                }
            }
            .padding(.horizontal, AnnoSpacing.lg)
            .padding(.bottom, viewModel.selectedLocationID != nil ? 200 : 180)
        }
    }

    // ─── Helpers ──────────────────────────────────────────

    private func traditionLabel(_ t: Tradition) -> String {
        switch t {
        case .catholic:   L10n.catholic
        case .orthodox:   L10n.orthodox
        case .jewish:     L10n.jewish
        case .islamic:    L10n.islamic
        case .interfaith: L10n.interfaith
        }
    }

    private func confLabel(_ c: ConfidenceLabel) -> String {
        switch c {
        case .confirmed:   L10n.confirmed
        case .traditional: L10n.traditional
        case .disputed:    L10n.disputed
        }
    }

    private func openDirections(to location: SacredLocation) {
        let placemark = MKPlacemark(coordinate: location.coordinate)
        let mapItem = MKMapItem(placemark: placemark)
        mapItem.name = location.placeName
        mapItem.openInMaps(launchOptions: [MKLaunchOptionsDirectionsModeKey: MKLaunchOptionsDirectionsModeWalking])
    }
}

// ─── Sub-Components ──────────────────────────────────────

struct SacredPinView: View {
    let tradition: Tradition
    var isTodayConnected: Bool = false
    var isLocked: Bool = false
    var isSelected: Bool = false

    @Environment(\.colorScheme) private var colorScheme

    var body: some View {
        ZStack {
            // Glow for today-connected
            if isTodayConnected {
                Circle()
                    .fill(Color.annoGold.opacity(0.3))
                    .frame(width: 28, height: 28)
            }

            // Main pin
            Circle()
                .fill(isLocked ? Color.gray.opacity(0.5) : Color.traditionColor(tradition))
                .frame(width: isSelected ? 20 : 14, height: isSelected ? 20 : 14)
                .overlay(
                    Circle()
                        .strokeBorder(Color.white, lineWidth: isSelected ? 2 : 1.5)
                )
                .scaleEffect(isSelected ? 1.1 : 1.0)

            // Lock icon for premium
            if isLocked {
                Image(systemName: "lock.fill")
                    .font(.system(size: 7))
                    .foregroundStyle(.white)
            }
        }
        .animation(.easeInOut(duration: 0.2), value: isSelected)
    }
}

struct FilterChip: View {
    let label: String
    var icon: String? = nil
    let isSelected: Bool
    var color: Color = Color.annoGold
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 4) {
                if let icon {
                    Image(systemName: icon)
                        .font(.system(size: 10))
                }
                Text(label)
                    .font(.annoCaption)
                    .fontWeight(isSelected ? .semibold : .regular)
            }
            .foregroundStyle(isSelected ? color : .secondary)
            .padding(.horizontal, 10)
            .padding(.vertical, 6)
            .background(
                Capsule()
                    .fill(isSelected ? color.opacity(0.15) : Color(UIColor.tertiarySystemFill))
            )
        }
        .buttonStyle(.plain)
    }
}

struct FloatingButton: View {
    let icon: String
    var badge: String? = nil
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            ZStack(alignment: .topTrailing) {
                Image(systemName: icon)
                    .font(.body)
                    .foregroundStyle(.primary)
                    .frame(width: 40, height: 40)
                    .background(.ultraThinMaterial)
                    .clipShape(Circle())
                    .shadow(radius: 3)

                if let badge {
                    Text(badge)
                        .font(.system(size: 8, weight: .bold))
                        .foregroundStyle(.white)
                        .background(Color.annoGold)
                        .clipShape(Circle())
                        .frame(width: 10, height: 10)
                        .offset(x: 2, y: -2)
                }
            }
        }
    }
}
Swift

// MARK: - File: LocationCardView.swift

import SwiftUI

struct LocationCardView: View {
    let location: SacredLocation
    let isLocked: Bool
    let isVisited: Bool
    let onTap: () -> Void
    let onDirections: () -> Void
    let onSave: () -> Void
    let onStartPilgrimage: () -> Void
    let onUnlock: () -> Void

    @Environment(\.colorScheme) private var colorScheme

    var body: some View {
        VStack(spacing: 0) {
            // Handle
            Capsule()
                .fill(Color.secondary.opacity(0.3))
                .frame(width: 36, height: 4)
                .padding(.top, 8)

            VStack(alignment: .leading, spacing: AnnoSpacing.md) {
                // Title row
                HStack(alignment: .top) {
                    VStack(alignment: .leading, spacing: 4) {
                        Text(location.placeName)
                            .font(.annoSerifHeading)
                            .foregroundStyle(colorScheme == .dark ? .annoIvory : .primary)
                            .lineLimit(2)

                        HStack(spacing: AnnoSpacing.sm) {
                            ForEach(location.traditions, id: \.self) { t in
                                TraditionBadge(tradition: t, compact: true)
                            }
                            ConfidenceBadge(confidence: location.confidence)
                            if isVisited {
                                Image(systemName: "checkmark.seal.fill")
                                    .foregroundStyle(.green)
                                    .font(.caption)
                            }
                        }
                    }
                    Spacer()
                }

                // "On This Ground" summary
                if !isLocked {
                    Text(location.whyThisPlaceMatters)
                        .font(.annoBody)
                        .foregroundStyle(.secondary)
                        .lineLimit(3)
                } else {
                    Text(location.whyThisPlaceMatters)
                        .font(.annoBody)
                        .foregroundStyle(.secondary)
                        .lineLimit(1)
                        .blur(radius: 2)

                    Button {
                        onUnlock()
                    } label: {
                        HStack(spacing: AnnoSpacing.sm) {
                            Image(systemName: "lock.open")
                            Text(L10n.unlock)
                                .fontWeight(.semibold)
                        }
                        .font(.annoCaption)
                        .foregroundStyle(Color.annoGold)
                    }
                }

                // Metadata
                if !isLocked {
                    HStack(spacing: AnnoSpacing.lg) {
                        if let hours = location.visitingHours {
                            Label(hours, systemImage: "clock")
                                .font(.annoCaption)
                                .foregroundStyle(.secondary)
                                .lineLimit(1)
                        }
                        Label("\(location.sourceCount) \(L10n.sources.lowercased())", systemImage: "book")
                            .font(.annoCaption)
                            .foregroundStyle(.secondary)
                    }
                }

                GoldDivider()

                // Actions
                HStack(spacing: AnnoSpacing.lg) {
                    Button { onTap() } label: {
                        Label(L10n.readMore, systemImage: "doc.text")
                            .font(.annoCaption)
                            .fontWeight(.medium)
                    }
                    Button { onDirections() } label: {
                        Label(L10n.directions, systemImage: "arrow.triangle.turn.up.right.diamond")
                            .font(.annoCaption)
                            .fontWeight(.medium)
                    }
                    Button { onSave() } label: {
                        Label(L10n.save, systemImage: "bookmark")
                            .font(.annoCaption)
                            .fontWeight(.medium)
                    }
                    Spacer()
                    if !isLocked {
                        Button { onStartPilgrimage() } label: {
                            Label(L10n.startPilgrimage, systemImage: "figure.walk")
                                .font(.annoCaption)
                                .fontWeight(.semibold)
                                .foregroundStyle(Color.annoGold)
                        }
                    }
                }
                .foregroundStyle(.primary)
            }
            .padding(.horizontal, AnnoSpacing.lg)
            .padding(.vertical, AnnoSpacing.md)
        }
        .background(.ultraThinMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
        .padding(.horizontal, AnnoSpacing.sm)
        .padding(.bottom, 4)
    }
}
Swift

// MARK: - File: LocationDetailView.swift

import SwiftUI

struct LocationDetailView: View {
    let location: SacredLocation
    let viewModel: AtlasViewModel
    @Environment(\.colorScheme) private var colorScheme
    @Environment(\.dismiss) private var dismiss
    @State private var showingFullNarrative = false

    var body: some View {
        NavigationStack {
            ScrollView(.vertical, showsIndicators: false) {
                VStack(alignment: .leading, spacing: AnnoSpacing.lg) {
                    // Hero area — art placeholder
                    heroArea

                    // Title & badges
                    titleSection

                    // "On This Ground"
                    onThisGroundSection

                    // Associated events
                    if !associatedEvents.isEmpty {
                        eventsSection
                    }

                    // Sources
                    sourcesSection

                    // Actions
                    actionsSection

                    // Premium gate for free users
                    if viewModel.isLocationLocked(location) {
                        PremiumGateView(
                            title: L10n.unlockAtlas,
                            subtitle: "Full place history, sources, and pilgrimage tools for this site.",
                            action: { viewModel.isShowingPremium = true }
                        )
                    }
                }
                .padding(.horizontal, AnnoSpacing.lg)
                .padding(.bottom, AnnoSpacing.xxl)
            }
            .background(colorScheme == .dark ? Color.annoDeepNavy : Color.annoIvory)
            .navigationTitle("")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }
                }
            }
        }
    }

    // ─── Hero ─────────────────────────────────────────────

    private var heroArea: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 14, style: .continuous)
                .fill(
                    LinearGradient(
                        colors: [
                            Color.traditionColor(location.traditions.first ?? .catholic).opacity(0.6),
                            Color.annoDeepNavy.opacity(0.8)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
                .frame(height: 180)

            VStack(spacing: AnnoSpacing.sm) {
                Image(systemName: "building.columns")
                    .font(.system(size: 36))
                    .foregroundStyle(Color.annoGold)
                Text(location.region)
                    .font(.annoSerifCaption)
                    .foregroundStyle(Color.annoGold.opacity(0.8))
            }
        }
    }

    // ─── Title ────────────────────────────────────────────

    private var titleSection: some View {
        VStack(alignment: .leading, spacing: AnnoSpacing.sm) {
            Text(location.placeName)
                .font(.annoSerifTitle)
                .foregroundStyle(colorScheme == .dark ? .annoIvory : .primary)

            HStack(spacing: AnnoSpacing.sm) {
                ForEach(location.traditions, id: \.self) { t in
                    TraditionBadge(tradition: t)
                }
            }

            HStack(spacing: AnnoSpacing.lg) {
                ConfidenceBadge(confidence: location.confidence)
                if let address = location.modernAddress {
                    Label(address, systemImage: "mappin")
                        .font(.annoCaption)
                        .foregroundStyle(.secondary)
                        .lineLimit(1)
                }
            }

            if !location.categories.isEmpty {
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: AnnoSpacing.xs) {
                        ForEach(location.categories, id: \.self) { cat in
                            CategoryChip(category: cat, isSelected: false) { }
                        }
                    }
                }
            }
        }
    }

    // ─── On This Ground ──────────────────────────────────

    private var onThisGroundSection: some View {
        VStack(alignment: .leading, spacing: AnnoSpacing.md) {
            Text(L10n.onThisGround)
                .font(.annoSerifSubheading)
                .foregroundStyle(Color.annoGold)

            Text(location.whyThisPlaceMatters)
                .font(.annoBody)
                .foregroundStyle(.primary)
                .lineLimit(showingFullNarrative ? nil : 5)

            if location.whyThisPlaceMatters.count > 200 {
                Button(showingFullNarrative ? "Show less" : L10n.readMore) {
                    withAnimation { showingFullNarrative.toggle() }
                }
                .font(.annoCaption)
                .foregroundStyle(Color.annoGold)
            }
        }
        .parchmentCard()
    }

    // ─── Events ──────────────────────────────────────────

    private var associatedEvents: [HistoricalEvent] {
        MockData.events.filter { $0.locationID == location.id }
    }

    private var eventsSection: some View {
        VStack(alignment: .leading, spacing: AnnoSpacing.md) {
            Text("Connected Events")
                .font(.annoSerifSubheading)
                .foregroundStyle(colorScheme == .dark ? .annoIvory : .primary)

            ForEach(associatedEvents) { event in
                VStack(alignment: .leading, spacing: AnnoSpacing.xs) {
                    HStack {
                        Text(event.title)
                            .font(.annoSerifCaption)
                            .foregroundStyle(.primary)
                        Spacer()
                        TraditionBadge(tradition: event.tradition, compact: true)
                    }
                    Text(event.shortNarrative)
                        .font(.annoCaption)
                        .foregroundStyle(.secondary)
                        .lineLimit(3)
                    ConfidenceBadge(confidence: event.confidence)
                }
                .padding(AnnoSpacing.md)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(colorScheme == .dark ? Color.annoDarkSurface : Color.annoParchment.opacity(0.5))
                .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
            }
        }
    }

    // ─── Sources ─────────────────────────────────────────

    private var sourcesSection: some View {
        VStack(alignment: .leading, spacing: AnnoSpacing.sm) {
            Text(L10n.sources)
                .font(.annoSerifSubheading)
                .foregroundStyle(colorScheme == .dark ? .annoIvory : .primary)

            HStack {
                Text("\(location.sourceCount) sources cited")
                    .font(.annoCaption)
                    .foregroundStyle(.secondary)
                Spacer()
                ConfidenceBadge(confidence: location.confidence)
            }
        }
        .parchmentCard()
    }

    // ─── Actions ─────────────────────────────────────────

    private var actionsSection: some View {
        VStack(spacing: AnnoSpacing.md) {
            // Directions
            Button {
                let placemark = MKPlacemark(coordinate: location.coordinate)
                let item = MKMapItem(placemark: placemark)
                item.name = location.placeName
                item.openInMaps(launchOptions: [MKLaunchOptionsDirectionsModeKey: MKLaunchOptionsDirectionsModeWalking])
            } label: {
                Label(L10n.directions, systemImage: "arrow.triangle.turn.up.right.diamond")
                    .frame(maxWidth: .infinity)
                    .font(.annoBody.weight(.medium))
            }
            .buttonStyle(.bordered)

            // Start Pilgrimage
            if viewModel.entitlement == .premium {
                Button {
                    viewModel.pilgrimStore.startJourney()
                    viewModel.pilgrimStore.visitSite(
                        location.id, name: location.placeName,
                        tradition: location.traditions.first ?? .catholic
                    )
                    dismiss()
                    viewModel.isShowingPilgrimMode = true
                } label: {
                    Label(L10n.startPilgrimage, systemImage: "figure.walk")
                        .frame(maxWidth: .infinity)
                        .font(.annoBody.weight(.semibold))
                        .foregroundStyle(Color.annoDeepNavy)
                }
                .tint(Color.annoGold)
                .buttonStyle(.borderedProminent)
            }

            // Save
            Button {
                // Save action placeholder
            } label: {
                Label(L10n.save, systemImage: "bookmark")
                    .frame(maxWidth: .infinity)
                    .font(.annoBody.weight(.medium))
            }
            .buttonStyle(.bordered)
        }
    }
}
Swift

// MARK: - File: NearbyPanelView.swift
// (Integrated into SacredAtlasView — this file provides the standalone version for reuse)

import SwiftUI

struct NearbyPanelStandalone: View {
    let sites: [NearbySiteRow]
    let entitlement: EntitlementTier
    let onSelect: (SacredLocation) -> Void
    let onUnlock: () -> Void
    @State private var isExpanded = false
    @Environment(\.colorScheme) private var colorScheme

    var body: some View {
        VStack(spacing: 0) {
            Capsule()
                .fill(Color.secondary.opacity(0.3))
                .frame(width: 36, height: 4)
                .padding(.top, 8)
                .padding(.bottom, 4)

            HStack {
                Text(L10n.nearYouTitle)
                    .font(.annoSerifSubheading)
                    .foregroundStyle(colorScheme == .dark ? .annoIvory : .primary)
                Spacer()
                Text("\(sites.count) sites")
                    .font(.annoCaption)
                    .foregroundStyle(.secondary)
            }
            .padding(.horizontal, AnnoSpacing.lg)
            .padding(.vertical, AnnoSpacing.sm)

            ScrollView(.vertical, showsIndicators: false) {
                LazyVStack(spacing: AnnoSpacing.xs) {
                    ForEach(sites.prefix(entitlement == .premium ? 20 : 3)) { row in
                        Button {
                            onSelect(row.location)
                        } label: {
                            HStack(spacing: AnnoSpacing.md) {
                                Circle()
                                    .fill(Color.traditionColor(row.location.traditions.first ?? .catholic))
                                    .frame(width: 10, height: 10)
                                VStack(alignment: .leading, spacing: 2) {
                                    Text(row.location.placeName)
                                        .font(.annoSerifCaption)
                                        .foregroundStyle(.primary)
                                    if row.isTodayConnected {
                                        Text(L10n.connectedToday)
                                            .font(.system(size: 10, weight: .semibold))
                                            .foregroundStyle(Color.annoGold)
                                    }
                                }
                                Spacer()
                                if let d = row.distance {
                                    Text(L10n.distanceString(d))
                                        .font(.annoCaption)
                                        .foregroundStyle(.secondary)
                                }
                            }
                            .padding(.horizontal, AnnoSpacing.lg)
                            .padding(.vertical, AnnoSpacing.sm)
                        }
                        .buttonStyle(.plain)
                    }

                    if entitlement == .free && sites.count > 3 {
                        Button(onUnlock) {
                            HStack {
                                Text("Unlock \(sites.count) nearby sites")
                                    .font(.annoSerifCaption)
                                    .foregroundStyle(Color.annoGold)
                                Spacer()
                                Image(systemName: "lock.fill")
                                    .foregroundStyle(Color.annoGold)
                                    .font(.caption)
                            }
                            .padding(.horizontal, AnnoSpacing.lg)
                            .padding(.vertical, AnnoSpacing.md)
                            .background(Color.annoGold.opacity(0.08))
                        }
                        .buttonStyle(.plain)
                    }
                }
            }
            .frame(maxHeight: isExpanded ? 300 : 120)
        }
        .background(.ultraThinMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
    }
}
Swift

// MARK: - File: RoutePackViews.swift

import SwiftUI

struct RoutePackListView: View {
    let viewModel: AtlasViewModel
    @Environment(\.colorScheme) private var colorScheme
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            ScrollView(.vertical, showsIndicators: false) {
                LazyVStack(spacing: AnnoSpacing.md) {
                    ForEach(viewModel.allRoutePacks) { pack in
                        NavigationLink {
                            RoutePackDetailView(pack: pack, viewModel: viewModel)
                        } label: {
                            RoutePackRow(pack: pack, isLocked: viewModel.isRoutePackLocked(pack))
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(AnnoSpacing.lg)
            }
            .background(colorScheme == .dark ? Color.annoDeepNavy : Color.annoIvory)
            .navigationTitle(L10n.routePacks)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }
                }
            }
        }
    }
}

struct RoutePackRow: View {
    let pack: RoutePack
    let isLocked: Bool
    @Environment(\.colorScheme) private var colorScheme

    var body: some View {
        HStack(spacing: AnnoSpacing.md) {
            // Icon
            ZStack {
                RoundedRectangle(cornerRadius: 10, style: .continuous)
                    .fill(
                        LinearGradient(
                            colors: [
                                Color.traditionColor(pack.traditionTags.first ?? .catholic).opacity(0.6),
                                Color.annoDeepNavy.opacity(0.8)
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: 56, height: 56)
                Image(systemName: "map")
                    .foregroundStyle(Color.annoGold)
                    .font(.title3)
            }

            VStack(alignment: .leading, spacing: 4) {
                HStack {
                    Text(pack.title)
                        .font(.annoSerifSubheading)
                        .foregroundStyle(colorScheme == .dark ? .annoIvory : .primary)
                        .lineLimit(1)
                    if isLocked {
                        Image(systemName: "lock.fill")
                            .font(.caption2)
                            .foregroundStyle(Color.annoGold)
                    }
                }
                Text(pack.subtitle)
                    .font(.annoCaption)
                    .foregroundStyle(.secondary)
                    .lineLimit(1)
                HStack(spacing: AnnoSpacing.md) {
                    Label(pack.stopIDs.count == 1 ? "1 site" : "\(pack.stopIDs.count) sites", systemImage: "mappin")
                    Label(pack.estimatedDistance, systemImage: "point.topleft.down.to.point.bottomright.curvepath")
                    Label(pack.estimatedTime, systemImage: "clock")
                }
                .font(.system(size: 10))
                .foregroundStyle(.secondary)
            }

            Spacer()

            Image(systemName: "chevron.right")
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .padding(AnnoSpacing.md)
        .background(colorScheme == .dark ? Color.annoCardDark : Color.annoParchment.opacity(0.5))
        .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
    }
}

struct RoutePackDetailView: View {
    let pack: RoutePack
    let viewModel: AtlasViewModel
    @Environment(\.colorScheme) private var colorScheme
    @Environment(\.dismiss) private var dismiss

    private var stops: [SacredLocation] {
        MockData.stops(for: pack)
    }

    private var previewStops: [SacredLocation] {
        viewModel.previewStops(for: pack)
    }

    private var isLocked: Bool {
        viewModel.isRoutePackLocked(pack)
    }

    var body: some View {
        ScrollView(.vertical, showsIndicators: false) {
            VStack(alignment: .leading, spacing: AnnoSpacing.lg) {
                // Hero
                ZStack {
                    RoundedRectangle(cornerRadius: 14, style: .continuous)
                        .fill(
                            LinearGradient(
                                colors: [
                                    Color.traditionColor(pack.traditionTags.first ?? .catholic).opacity(0.7),
                                    Color.annoDeepNavy
                                ],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )
                        .frame(height: 160)

                    VStack(spacing: AnnoSpacing.sm) {
                        Image(systemName: "map")
                            .font(.system(size: 32))
                            .foregroundStyle(Color.annoGold)
                        Text(pack.region)
                            .font(.annoSerifCaption)
                            .foregroundStyle(Color.annoGold.opacity(0.8))
                    }
                }

                // Title
                VStack(alignment: .leading, spacing: AnnoSpacing.sm) {
                    Text(pack.title)
                        .font(.annoSerifTitle)
                        .foregroundStyle(colorScheme == .dark ? .annoIvory : .primary)
                    Text(pack.subtitle)
                        .font(.annoBody)
                        .foregroundStyle(.secondary)

                    HStack(spacing: AnnoSpacing.lg) {
                        Label("\(stops.count) sites", systemImage: "mappin")
                        Label(pack.estimatedDistance, systemImage: "point.topleft.down.to.point.bottomright.curvepath")
                        Label(pack.estimatedTime, systemImage: "clock")
                    }
                    .font(.annoCaption)
                    .foregroundStyle(.secondary)

                    HStack(spacing: AnnoSpacing.sm) {
                        ForEach(pack.traditionTags, id: \.self) { t in
                            TraditionBadge(tradition: t, compact: true)
                        }
                    }
                }

                GoldDivider()

                // Stops
                Text("Stops")
                    .font(.annoSerifSubheading)
                    .foregroundStyle(colorScheme == .dark ? .annoIvory : .primary)

                ForEach(Array(previewStops.enumerated()), id: \.element.id) { index, stop in
                    HStack(spacing: AnnoSpacing.md) {
                        // Stop number
                        ZStack {
                            Circle()
                                .fill(Color.annoGold.opacity(0.2))
                                .frame(width: 32, height: 32)
                            Text("\(index + 1)")
                                .font(.annoSerifCaption)
                                .foregroundStyle(Color.annoGold)
                        }

                        VStack(alignment: .leading, spacing: 2) {
                            Text(stop.placeName)
                                .font(.annoSerifCaption)
                                .foregroundStyle(.primary)
                            Text(stop.country)
                                .font(.annoCaption)
                                .foregroundStyle(.secondary)
                        }

                        Spacer()

                        ConfidenceBadge(confidence: stop.confidence)
                    }
                    .padding(AnnoSpacing.md)
                    .background(colorScheme == .dark ? Color.annoCardDark : Color.annoParchment.opacity(0.5))
                    .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
                }

                // Locked stops
                if isLocked && stops.count > previewStops.count {
                    let lockedCount = stops.count - previewStops.count
                    VStack(spacing: AnnoSpacing.sm) {
                        Text("\(lockedCount) more \(lockedCount == 1 ? "site" : "sites") \(L10n.sitesAvailable.lowercased())")
                            .font(.annoSerifCaption)
                            .foregroundStyle(Color.annoGold)
                        Text("Unlock the full route, offline prep, source-backed stops, and pilgrimage passport.")
                            .font(.annoCaption)
                            .foregroundStyle(.secondary)
                            .multilineTextAlignment(.center)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(AnnoSpacing.lg)
                    .background(Color.annoGold.opacity(0.06))
                    .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
                }

                // Start button
                if !isLocked {
                    Button {
                        viewModel.pilgrimStore.startJourney(routePackID: pack.id)
                        dismiss()
                        viewModel.isShowingPilgrimMode = true
                    } label: {
                        Label(L10n.startPilgrimage, systemImage: "figure.walk")
                            .frame(maxWidth: .infinity)
                            .font(.annoBody.weight(.semibold))
                            .foregroundStyle(Color.annoDeepNavy)
                    }
                    .tint(Color.annoGold)
                    .buttonStyle(.borderedProminent)
                    .controlSize(.large)
                } else {
                    Button {
                        viewModel.isShowingPremium = true
                    } label: {
                        Label(L10n.unlockRoute, systemImage: "lock.open")
                            .frame(maxWidth: .infinity)
                            .font(.annoBody.weight(.semibold))
                            .foregroundStyle(Color.annoDeepNavy)
                    }
                    .tint(Color.annoGold)
                    .buttonStyle(.borderedProminent)
                    .controlSize(.large)
                }
            }
            .padding(AnnoSpacing.lg)
        }
        .background(colorScheme == .dark ? Color.annoDeepNavy : Color.annoIvory)
        .navigationTitle(pack.title)
        .navigationBarTitleDisplayMode(.inline)
    }
}
Swift

// MARK: - File: PilgrimModeView.swift

import SwiftUI
import MapKit

struct PilgrimModeView: View {
    let viewModel: AtlasViewModel
    @Environment(\.colorScheme) private var colorScheme
    @Environment(\.dismiss) private var dismiss
    @State private var showingFieldNote = false
    @State private var fieldNoteText = ""
    @State private var fieldNoteLocationID: UUID?

    var body: some View {
        ZStack {
            Color.annoDeepNavy.ignoresSafeArea()

            VStack(spacing: 0) {
                // ─── Status Bar ────────────────────────────
                statusBar

                // ─── Map ───────────────────────────────────
                pilgrimMap

                // ─── Journey Panel ─────────────────────────
                journeyPanel
            }
        }
        .statusBarHidden(true)
    }

    // ─── Status Bar ──────────────────────────────────────

    private var statusBar: some View {
        HStack {
            VStack(alignment: .leading, spacing: 2) {
                Text(L10n.pilgrimMode)
                    .font(.annoSerifSubheading)
                    .foregroundStyle(Color.annoGold)
                if let journey = viewModel.pilgrimStore.activeJourney {
                    Text(journey.isActive ? "Active" : "Paused")
                        .font(.annoCaption)
                        .foregroundStyle(journey.isActive ? .green : .orange)
                }
            }
            Spacer()

            HStack(spacing: AnnoSpacing.md) {
                Button {
                    viewModel.pilgrimStore.pauseJourney()
                } label: {
                    Image(systemName: "pause.fill")
                        .foregroundStyle(.primary)
                        .frame(width: 36, height: 36)
                        .background(.ultraThinMaterial)
                        .clipShape(Circle())
                }

                Button {
                    viewModel.pilgrimStore.endJourney()
                    dismiss()
                } label: {
                    Image(systemName: "xmark")
                        .foregroundStyle(.white)
                        .frame(width: 36, height: 36)
                        .background(Color.red.opacity(0.8))
                        .clipShape(Circle())
                }
            }
        }
        .padding(.horizontal, AnnoSpacing.lg)
        .padding(.top, 50)
        .padding(.bottom, AnnoSpacing.md)
        .background(Color.annoDeepNavy.opacity(0.8))
    }

    // ─── Pilgrim Map ─────────────────────────────────────

    private var pilgrimMap: some View {
        Map(position: .constant(.userLocation(fallback: .automatic))) {
            UserAnnotation()

            if let journey = viewModel.pilgrimStore.activeJourney,
               let packID = journey.routePackID,
               let pack = viewModel.allRoutePacks.first(where: { $0.id == packID }) {
                let stops = MockData.stops(for: pack)
                ForEach(stops) { stop in
                    Annotation(stop.placeName, coordinate: stop.coordinate) {
                        ZStack {
                            Circle()
                                .fill(viewModel.pilgrimStore.hasVisited(stop.id) ? Color.green : Color.traditionColor(stop.traditions.first ?? .catholic))
                                .frame(width: 16, height: 16)
                            Circle()
                                .strokeBorder(.white, lineWidth: 1.5)
                                .frame(width: 16, height: 16)
                            if viewModel.pilgrimStore.hasVisited(stop.id) {
                                Image(systemName: "checkmark")
                                    .font(.system(size: 8, weight: .bold))
                                    .foregroundStyle(.white)
                            }
                        }
                    }
                }

                if stops.count >= 2 {
                    MapPolyline(coordinates: stops.map(\.coordinate))
                        .stroke(Color.annoGold.opacity(0.5), style: StrokeStyle(lineWidth: 3, lineCap: .round, lineJoin: .round))
                }
            }
        }
        .mapStyle(.standard(emphasis: .muted))
        .frame(maxHeight: .infinity)
    }

    // ─── Journey Panel ───────────────────────────────────

    private var journeyPanel: some View {
        VStack(spacing: AnnoSpacing.md) {
            // Progress
            if let journey = viewModel.pilgrimStore.activeJourney {
                progressSection(journey: journey)
            }

            // Next stop
            nextStopSection

            // Visited timeline
            visitedTimeline

            // Field note
            Button {
                if let currentID = viewModel.pilgrimStore.activeJourney?.visitedLocationIDs.last {
                    fieldNoteLocationID = currentID
                }
                showingFieldNote = true
            } label: {
                Label(L10n.addNote, systemImage: "square.and.pencil")
                    .font(.annoCaption)
                    .fontWeight(.medium)
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)
            .tint(Color.annoGold)
        }
        .padding(AnnoSpacing.lg)
        .background(Color.annoDeepNavy)
        .clipShape(RoundedRectangle(cornerRadius: 20, style: .continuous))
        .shadow(color: .black.opacity(0.5), radius: 10, y: -5)
        .alert("Field Note", isPresented: $showingFieldNote) {
            TextField("What did this place stir in you?", text: $fieldNoteText)
            Button("Save") {
                if let locID = fieldNoteLocationID {
                    viewModel.pilgrimStore.addFieldNote(locationID: locID, text: fieldNoteText)
                }
                fieldNoteText = ""
            }
            Button("Cancel", role: .cancel) { fieldNoteText = "" }
        } message: {
            Text("A private reflection for your pilgrimage record.")
        }
    }

    private func progressSection(journey: JourneySession) -> some View {
        VStack(spacing: AnnoSpacing.sm) {
            HStack {
                Text("\(journey.visitedLocationIDs.count) \(L10n.stopsVisited)")
                    .font(.annoSerifCaption)
                    .foregroundStyle(Color.annoGold)
                Spacer()
                if let packID = journey.routePackID,
                   let pack = viewModel.allRoutePacks.first(where: { $0.id == packID }) {
                    Text("\(journey.visitedLocationIDs.count) / \(pack.stopIDs.count)")
                        .font(.annoCaption)
                        .foregroundStyle(.secondary)
                }
            }

            ProgressView(value: progressValue)
                .tint(Color.annoGold)
        }
    }

    private var progressValue: Double {
        guard let journey = viewModel.pilgrimStore.activeJourney,
              let packID = journey.routePackID,
              let pack = viewModel.allRoutePacks.first(where: { $0.id == packID }),
              pack.stopIDs.count > 0 else { return 0 }
        return Double(journey.visitedLocationIDs.count) / Double(pack.stopIDs.count)
    }

    private var nextStopSection: some View {
        Group {
            if let next = nextUnvisitedStop {
                HStack(spacing: AnnoSpacing.md) {
                    Image(systemName: "arrow.triangle.turn.up.right.diamond")
                        .foregroundStyle(Color.annoGold)
                    VStack(alignment: .leading, spacing: 2) {
                        Text(L10n.nextStop)
                            .font(.annoCaption)
                            .foregroundStyle(.secondary)
                        Text(next.placeName)
                            .font(.annoSerifSubheading)
                            .foregroundStyle(.primary)
                    }
                    Spacer()
                    Button("Visit") {
                        viewModel.pilgrimStore.visitSite(
                            next.id, name: next.placeName,
                            tradition: next.traditions.first ?? .catholic
                        )
                    }
                    .font(.annoCaption)
                    .fontWeight(.semibold)
                    .foregroundStyle(Color.annoDeepNavy)
                    .padding(.horizontal, AnnoSpacing.md)
                    .padding(.vertical, AnnoSpacing.xs)
                    .background(Color.annoGold)
                    .clipShape(Capsule())
                }
            } else if viewModel.pilgrimStore.activeJourney?.visitedLocationIDs.isEmpty == false {
                HStack {
                    Image(systemName: "checkmark.seal.fill")
                        .foregroundStyle(.green)
                    Text(L10n.journeyComplete)
                        .font(.annoSerifSubheading)
                        .foregroundStyle(.green)
                }
            }
        }
    }

    private var nextUnvisitedStop: SacredLocation? {
        guard let journey = viewModel.pilgrimStore.activeJourney,
              let packID = journey.routePackID,
              let pack = viewModel.allRoutePacks.first(where: { $0.id == packID }) else { return nil }
        let stops = MockData.stops(for: pack)
        return stops.first { !journey.visitedLocationIDs.contains($0.id) }
    }

    private var visitedTimeline: some View {
        Group {
            if !viewModel.pilgrimStore.activeJourney!.visitedLocationIDs.isEmpty {
                VStack(alignment: .leading, spacing: AnnoSpacing.xs) {
                    ForEach(viewModel.pilgrimStore.activeJourney!.visitedLocationIDs, id: \.self) { locID in
                        if let loc = MockData.location(by: locID) {
                            HStack(spacing: AnnoSpacing.sm) {
                                Image(systemName: "checkmark.circle.fill")
                                    .foregroundStyle(.green)
                                    .font(.caption)
                                Text(loc.placeName)
                                    .font(.annoCaption)
                                    .foregroundStyle(.secondary)
                            }
                        }
                    }
                }
            }
        }
    }
}
Swift

// MARK: - File: PassportView.swift

import SwiftUI

struct PassportView: View {
    let store: PilgrimSessionStore
    @Environment(\.colorScheme) private var colorScheme
    @Environment(\.dismiss) private var dismiss
    @State private var selectedTab = 0

    var body: some View {
        NavigationStack {
            TabView(selection: $selectedTab) {
                stampsTab
                    .tabItem {
                        Label(L10n.stamps, systemImage: "checkmark.seal")
                    }
                    .tag(0)

                journeysTab
                    .tabItem {
                        Label("Journeys", systemImage: "map")
                    }
                    .tag(1)

                notesTab
                    .tabItem {
                        Label(L10n.fieldNotes, systemImage: "square.and.pencil")
                    }
                    .tag(2)
            }
            .tint(Color.annoGold)
            .navigationTitle(L10n.passport)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }
                }
            }
        }
    }

    // ─── Stamps Tab ──────────────────────────────────────

    private var stampsTab: some View {
        ScrollView(.vertical, showsIndicators: false) {
            // Stats
            HStack(spacing: AnnoSpacing.xxl) {
                statItem(value: "\(store.totalSitesVisited)", label: L10n.sitesVisitedCount)
                statItem(value: "\(store.totalRoutesCompleted)", label: L10n.routesCompleted)
                statItem(value: "\(store.totalNotesWritten)", label: L10n.notesWritten)
            }
            .padding(.vertical, AnnoSpacing.xl)

            GoldDivider()

            if store.visitedSites.isEmpty {
                EmptyStateView(
                    icon: "book.closed",
                    title: L10n.noVisitsYet,
                    subtitle: L10n.noVisitsSubtitle
                )
                .padding(.top, AnnoSpacing.xxl)
            } else {
                LazyVGrid(columns: [
                    GridItem(.flexible()),
                    GridItem(.flexible()),
                    GridItem(.flexible())
                ], spacing: AnnoSpacing.lg) {
                    ForEach(store.visitedSites) { site in
                        StampView(site: site)
                    }
                }
                .padding(AnnoSpacing.lg)
            }
        }
        .background(colorScheme == .dark ? Color.annoDeepNavy : Color.annoIvory)
    }

    // ─── Journeys Tab ────────────────────────────────────

    private var journeysTab: some View {
        ScrollView(.vertical, showsIndicators: false) {
            if store.completedJourneys.isEmpty && store.activeJourney == nil {
                EmptyStateView(
                    icon: "map",
                    title: "No Journeys Yet",
                    subtitle: "Start a pilgrimage to begin your sacred record."
                )
                .padding(.top, AnnoSpacing.xxl)
            } else {
                LazyVStack(spacing: AnnoSpacing.md) {
                    if let active = store.activeJourney {
                        journeyCard(journey: active, isActive: true)
                    }
                    ForEach(store.completedJourneys) { journey in
                        journeyCard(journey: journey, isActive: false)
                    }
                }
                .padding(AnnoSpacing.lg)
            }
        }
        .background(colorScheme == .dark ? Color.annoDeepNavy : Color.annoIvory)
    }

    private func journeyCard(journey: JourneySession, isActive: Bool) -> some View {
        VStack(alignment: .leading, spacing: AnnoSpacing.sm) {
            HStack {
                Circle()
                    .fill(isActive ? Color.green : Color.annoGold)
                    .frame(width: 8, height: 8)
                Text(isActive ? "Active Journey" : "Completed")
                    .font(.annoSerifCaption)
                    .foregroundStyle(isActive ? .green : Color.annoGold)
                Spacer()
                Text(journey.startedAt, style: .date)
                    .font(.annoCaption)
                    .foregroundStyle(.secondary)
            }

            if let packID = journey.routePackID,
               let pack = MockData.routePack(by: packID) {
                Text(pack.title)
                    .font(.annoSerifSubheading)
                    .foregroundStyle(.primary)
            }

            Text("\(journey.visitedLocationIDs.count) \(L10n.stopsVisited)")
                .font(.annoCaption)
                .foregroundStyle(.secondary)
        }
        .parchmentCard()
    }

    // ─── Notes Tab ───────────────────────────────────────

    private var notesTab: some View {




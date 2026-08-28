//  ContentImportService.swift
//  Anno
//
//  Background import service that loads all JSON resources into SwiftData models.

import Foundation
import SwiftData
import Observation

@Observable
@MainActor
final class ContentImportService {
    enum ImportPhase: Equatable {
        case idle
        case preparing
        case importingEntries
        case importingPlaces
        case importingArtworks
        case importingRoutes
        case completed
        case failed(Error)
        
        static func == (lhs: ImportPhase, rhs: ImportPhase) -> Bool {
            switch (lhs, rhs) {
            case (.idle, .idle), (.preparing, .preparing), (.importingEntries, .importingEntries),
                 (.importingPlaces, .importingPlaces), (.importingArtworks, .importingArtworks),
                 (.importingRoutes, .importingRoutes), (.completed, .completed):
                return true
            case (.failed(let lErr), .failed(let rErr)):
                return lErr.localizedDescription == rErr.localizedDescription
            default:
                return false
            }
        }
    }
    
    var phase: ImportPhase = .idle
    var progress: Double = 0.0
    var message: String = ""
    var entriesImported: Int = 0
    var placesImported: Int = 0
    var artworksImported: Int = 0
    var routesImported: Int = 0
    
    private let modelContext: ModelContext
    private var task: Task<Void, Never>?
    
    init(modelContext: ModelContext) {
        self.modelContext = modelContext
    }
    
    deinit {
        task?.cancel()
    }
    
    func startImport() {
        guard task == nil else { return }
        task = Task { await runImport() }
    }
    
    func cancelImport() {
        task?.cancel()
        task = nil
        phase = .idle
        progress = 0.0
        message = ""
    }
    
    private func runImport() async {
        phase = .preparing
        message = "Preparing import..."
        progress = 0.0
        
        do {
            // Phase 1: Anno Entries (anno_unified_2026.json)
            phase = .importingEntries
            message = "Importing daily entries..."
            try await importEntries()
            await updateProgress(0.25)
            
            // Phase 2: Sacred Places (sacred_geography_master.json)
            phase = .importingPlaces
            message = "Importing sacred places..."
            try await importPlaces()
            await updateProgress(0.5)
            
            // Phase 3: Artworks (art_dossiers_catalog.json)
            phase = .importingArtworks
            message = "Importing artworks..."
            try await importArtworks()
            await updateProgress(0.75)
            
            // Phase 4: Pilgrimage Routes (sacred_geography_master.json)
            phase = .importingRoutes
            message = "Importing pilgrimage routes..."
            try await importRoutes()
            await updateProgress(1.0)
            
            phase = .completed
            message = "Import complete: \(entriesImported) entries, \(placesImported) places, \(artworksImported) artworks, \(routesImported) routes"
        } catch {
            phase = .failed(error)
            message = "Import failed: \(error.localizedDescription)"
        }
    }
    
    @MainActor
    private func updateProgress(_ value: Double) {
        progress = value
    }
    
    private func importEntries() async throws {
        guard let url = Bundle.main.url(forResource: "anno_full_2026", withExtension: "json") else {
            throw ImportError.missingResource("anno_full_2026.json")
        }
        
        let data = try Data(contentsOf: url)
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        let wrapper = try decoder.decode(AnnoUnifiedWrapper.self, from: data)
        
        for entryData in wrapper.entries {
            // Check if already exists
            let existing = try modelContext.fetch(
                FetchDescriptor<AnnoEntry>(predicate: #Predicate { $0.id == entryData.id })
            )
            
            let entry: AnnoEntry
            if let existing = existing.first {
                entry = existing
            } else {
                entry = AnnoEntry(id: entryData.id)
                modelContext.insert(entry)
            }
            
            // Update from JSON
            entry.date = entryData.date
            entry.weekday = entryData.weekday
            entry.mockPriority = entryData.mockPriority
            entry.liturgical = LiturgicalInfo(from: entryData.liturgical)
            entry.calendars = CalendarConversions(from: entryData.calendars)
            entry.primary = PrimaryContent(from: entryData.primary)
            entry.place = entryData.place.map { SacredPlace(from: $0) }
            entry.artwork = ArtworkCandidate(from: entryData.artwork)
            entry.sources = entryData.sources.map { SourceRef(from: $0) }
            entry.appHooks = AppHooks(from: entryData.appHooks)
            
            entriesImported += 1
            
            // Yield periodically
            if entriesImported % 20 == 0 {
                await updateProgress(0.25 * Double(entriesImported) / Double(wrapper.entries.count))
                try Task.checkCancellation()
            }
        }
        
        try modelContext.save()
    }
    
    private func importPlaces() async throws {
        guard let url = Bundle.main.url(forResource: "sacred_geography_master", withExtension: "json") else {
            throw ImportError.missingResource("sacred_geography_master.json")
        }
        
        let data = try Data(contentsOf: url)
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        let wrapper = try decoder.decode(SacredGeographyMaster.self, from: data)
        
        for sanctuary in wrapper.sanctuaries {
            let existing = try modelContext.fetch(
                FetchDescriptor<SacredPlace>(predicate: #Predicate { $0.id == sanctuary.id })
            )

            let place: SacredPlace
            if let existing = existing.first {
                place = existing
            } else {
                place = SacredPlace(
                    id: sanctuary.id,
                    name: sanctuary.name,
                    latitude: sanctuary.latitude,
                    longitude: sanctuary.longitude,
                    confidence: ConfidenceLevel(rawValue: sanctuary.confidence) ?? .contextual,
                    sourceUrl: sanctuary.sourceUrl
                )
                modelContext.insert(place)
            }

            placesImported += 1
        }

        try modelContext.save()
    }
    
    private func importArtworks() async throws {
        guard let url = Bundle.main.url(forResource: "art_dossiers_catalog", withExtension: "json", subdirectory: "ArtDossiers") else {
            throw ImportError.missingResource("art_dossiers_catalog.json")
        }
        
        let data = try Data(contentsOf: url)
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        let wrapper = try decoder.decode(ArtDossiersCatalog.self, from: data)
        
        for artworkData in wrapper.artworks {
            let existing = try modelContext.fetch(
                FetchDescriptor<Artwork>(predicate: #Predicate { $0.id == artworkData.artworkId })
            )
            
            let artwork: Artwork
            if let existing = existing.first {
                artwork = existing
            } else {
                artwork = Artwork(
                    id: artworkData.artworkId,
                    title: artworkData.title,
                    artist: artworkData.artist,
                    yearCreated: artworkData.yearCreated,
                    medium: artworkData.medium,
                    dimensions: artworkData.dimensions,
                    currentLocation: artworkData.currentLocation,
                    imageUrlHighRes: artworkData.imageUrlHighres,
                    imageUrlThumb: artworkData.imageUrlThumb,
                    licenseType: artworkData.licenseType,
                    theologicalSignificanceEn: artworkData.theologicalSignificanceEn,
                    theologicalSignificanceVi: artworkData.theologicalSignificanceVi,
                    feastAssociation: artworkData.feastAssociation
                )
                modelContext.insert(artwork)
            }
            
            artworksImported += 1
        }
        
        try modelContext.save()
    }
    
    private func importRoutes() async throws {
        guard let url = Bundle.main.url(forResource: "sacred_geography_master", withExtension: "json") else {
            throw ImportError.missingResource("sacred_geography_master.json")
        }
        
        let data = try Data(contentsOf: url)
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        let wrapper = try decoder.decode(SacredGeographyMaster.self, from: data)
        
        for routeData in wrapper.pilgrimageRoutes {
            let existing = try modelContext.fetch(
                FetchDescriptor<PilgrimageRoute>(predicate: #Predicate { $0.id == routeData.routeId })
            )
            
            let route: PilgrimageRoute
            if let existing = existing.first {
                route = existing
            } else {
                route = PilgrimageRoute(routeId: routeData.routeId)
                modelContext.insert(route)
            }
            
            // Update from JSON
            route.titleEn = routeData.titleEn
            route.titleVi = routeData.titleVi
            route.region = routeData.region
            route.durationDays = routeData.durationDays
            route.distanceKm = routeData.distanceKm
            route.difficulty = routeData.difficulty
            route.spiritualThemeEn = routeData.spiritualThemeEn
            route.spiritualThemeVi = routeData.spiritualThemeVi
            route.overviewEn = routeData.overviewEn
            route.overviewVi = routeData.overviewVi
            route.waypoints = routeData.waypoints.map { PilgrimageWaypoint(from: $0) }
            
            routesImported += 1
        }
        
        try modelContext.save()
    }
}

enum ImportError: LocalizedError {
    case missingResource(String)
    case decodingFailed(String)
    
    var errorDescription: String? {
        switch self {
        case .missingResource(let name):
            return "Missing bundled resource: \(name)"
        case .decodingFailed(let msg):
            return "Failed to decode JSON: \(msg)"
        }
    }
}

// MARK: - Decoding Helpers (matching AnnoEntry.swift schema)

private struct AnnoUnifiedWrapper: Codable {
    let schemaVersion: String
    let generatedOn: String
    let totalEntries: Int
    let entries: [AnnoEntryData]
}

private struct AnnoEntryData: Codable {
    let id: String
    let date: String
    let weekday: String
    let mockPriority: String
    let liturgical: LiturgicalInfoData
    let calendars: CalendarConversionsData
    let primary: PrimaryContentData
    let place: SacredPlaceData?
    let artwork: ArtworkCandidateData
    let sources: [SourceRefData]
    let appHooks: AppHooksData
}

private struct LiturgicalInfoData: Codable {
    let rank: String
    let color: String
    let titleEn: String
    let titleVi: String
}

private struct CalendarConversionsData: Codable {
    let julian: String
    let hebrew: String
    let islamicUmmAlQura: String
    let coptic: String
    let ethiopian: String
}

private struct PrimaryContentData: Codable {
    let type: String
    let titleEn: String
    let titleVi: String
    let summaryEn: String
    let summaryVi: String
    let confidence: String
    let confidenceNoteEn: String
    let confidenceNoteVi: String
    let bodyEn: String
    let bodyVi: String
}

private struct SacredPlaceData: Codable {
    let name: String
    let latitude: Double
    let longitude: Double
    let confidence: String
    let sourceUrl: String
}

private struct ArtworkCandidateData: Codable {
    let title: String
    let maker: String
    let dateLabel: String
    let sourceUrl: String
    let status: String
}

private struct SourceRefData: Codable {
    let label: String
    let url: String
    let type: String
}

private struct AppHooksData: Codable {
    let heroLineEn: String
    let heroLineVi: String
    let prayerPromptEn: String
    let prayerPromptVi: String
}

// MARK: - Sacred Geography

private struct SacredGeographyMaster: Codable {
    let schemaVersion: String
    let compiledOn: String
    let descriptionEn: String
    let descriptionVi: String
    let countriesCovered: [String]
    let sanctuaries: [SanctuaryData]
    let pilgrimageRoutes: [PilgrimageRouteData]
}

private struct SanctuaryData: Codable {
    let id: String
    let name: String
    let latitude: Double
    let longitude: Double
    let confidence: String
    let sourceUrl: String
}

private struct PilgrimageRouteData: Codable {
    let routeId: String
    let titleEn: String
    let titleVi: String
    let region: String
    let durationDays: Int
    let distanceKm: Double
    let difficulty: String
    let spiritualThemeEn: String
    let spiritualThemeVi: String
    let overviewEn: String
    let overviewVi: String
    let waypoints: [PilgrimageWaypointData]
}

private struct PilgrimageWaypointData: Codable {
    let waypointId: String
    let nameEn: String
    let nameVi: String
    let latitude: Double
    let longitude: Double
    let order: Int
    let historicalSummaryEn: String
    let historicalSummaryVi: String
    let sacredRelicEn: String
    let sacredRelicVi: String
    let scriptureReading: String
    let suggestedPrayerEn: String
    let suggestedPrayerVi: String
}

// MARK: - Art Dossiers

private struct ArtDossiersCatalog: Codable {
    let schemaVersion: String
    let curatedOn: String
    let descriptionEn: String
    let descriptionVi: String
    let totalArtworks: Int
    let artworks: [ArtworkData]
}

private struct ArtworkData: Codable {
    let artworkId: String
    let feastAssociation: String
    let title: String
    let artist: String
    let yearCreated: String
    let medium: String
    let dimensions: String
    let currentLocation: String
    let imageUrlHighres: String
    let imageUrlThumb: String
    let licenseType: String
    let theologicalSignificanceEn: String
    let theologicalSignificanceVi: String
}

// MARK: - Model Initializers

extension AnnoEntry {
    convenience init(id: String) {
        self.init(
            id: id,
            date: "",
            weekday: "",
            mockPriority: "",
            liturgical: LiturgicalInfo(rank: "", color: "", titleEn: "", titleVi: ""),
            calendars: CalendarConversions(julian: "", hebrew: "", islamicUmmAlQura: "", coptic: "", ethiopian: ""),
            primary: PrimaryContent(type: "", titleEn: "", titleVi: "", summaryEn: "", summaryVi: "", confidence: .confirmed, confidenceNoteEn: "", confidenceNoteVi: "", bodyEn: "", bodyVi: ""),
            place: nil,
            artwork: ArtworkCandidate(title: "", maker: "", dateLabel: "", sourceUrl: "", status: ""),
            sources: [],
            appHooks: AppHooks(heroLineEn: "", heroLineVi: "", prayerPromptEn: "", prayerPromptVi: "")
        )
    }
}

extension LiturgicalInfo {
    init(from data: LiturgicalInfoData) {
        self.rank = data.rank
        self.color = data.color
        self.titleEn = data.titleEn
        self.titleVi = data.titleVi
    }
}

extension CalendarConversions {
    init(from data: CalendarConversionsData) {
        self.julian = data.julian
        self.hebrew = data.hebrew
        self.islamicUmmAlQura = data.islamicUmmAlQura
        self.coptic = data.coptic
        self.ethiopian = data.ethiopian
    }
}

extension PrimaryContent {
    init(from data: PrimaryContentData) {
        self.type = data.type
        self.titleEn = data.titleEn
        self.titleVi = data.titleVi
        self.summaryEn = data.summaryEn
        self.summaryVi = data.summaryVi
        self.confidence = ConfidenceLevel(rawValue: data.confidence) ?? .confirmed
        self.confidenceNoteEn = data.confidenceNoteEn
        self.confidenceNoteVi = data.confidenceNoteVi
        self.bodyEn = data.bodyEn
        self.bodyVi = data.bodyVi
    }
}

extension SacredPlace {
    convenience init(from data: SacredPlaceData) {
        self.init(
            id: UUID().uuidString,
            name: data.name,
            latitude: data.latitude,
            longitude: data.longitude,
            confidence: ConfidenceLevel(rawValue: data.confidence) ?? .contextual,
            sourceUrl: data.sourceUrl
        )
    }
}

extension ArtworkCandidate {
    init(from data: ArtworkCandidateData) {
        self.title = data.title
        self.maker = data.maker
        self.dateLabel = data.dateLabel
        self.sourceUrl = data.sourceUrl
        self.status = data.status
    }
}

extension SourceRef {
    init(from data: SourceRefData) {
        self.label = data.label
        self.url = data.url
        self.type = data.type
    }
}

extension AppHooks {
    init(from data: AppHooksData) {
        self.heroLineEn = data.heroLineEn
        self.heroLineVi = data.heroLineVi
        self.prayerPromptEn = data.prayerPromptEn
        self.prayerPromptVi = data.prayerPromptVi
    }
}

extension PilgrimageRoute {
    convenience init(routeId: String) {
        self.init(
            routeId: routeId,
            titleEn: "",
            titleVi: "",
            region: "",
            durationDays: 0,
            distanceKm: 0,
            difficulty: "",
            spiritualThemeEn: "",
            spiritualThemeVi: "",
            overviewEn: "",
            overviewVi: "",
            waypoints: []
        )
    }
}

extension PilgrimageWaypoint {
    convenience init(from data: PilgrimageWaypointData) {
        self.init(
            waypointId: data.waypointId,
            nameEn: data.nameEn,
            nameVi: data.nameVi,
            latitude: data.latitude,
            longitude: data.longitude,
            order: data.order,
            historicalSummaryEn: data.historicalSummaryEn,
            historicalSummaryVi: data.historicalSummaryVi,
            sacredRelicEn: data.sacredRelicEn,
            sacredRelicVi: data.sacredRelicVi,
            scriptureReading: data.scriptureReading,
            suggestedPrayerEn: data.suggestedPrayerEn,
            suggestedPrayerVi: data.suggestedPrayerVi
        )
    }
}
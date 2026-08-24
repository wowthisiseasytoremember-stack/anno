//  ArtDossier.swift
//  Anno
//
//  Model representing high-resolution sacred art dossiers with
//  bilingual theological commentary, iconography, and museum provenance.

import Foundation

struct ArtDossierCatalog: Codable {
    let schemaVersion: String
    let curatedOn: String
    let descriptionEn: String
    let descriptionVi: String
    let totalArtworks: Int
    let artworks: [ArtDossier]

    enum CodingKeys: String, CodingKey {
        case schemaVersion = "schema_version"
        case curatedOn = "curated_on"
        case descriptionEn = "description_en"
        case descriptionVi = "description_vi"
        case totalArtworks = "total_artworks"
        case artworks
    }
}

struct ArtDossier: Codable, Identifiable, Hashable {
    var id: String { artworkId }

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

    enum CodingKeys: String, CodingKey {
        case artworkId = "artwork_id"
        case feastAssociation = "feast_association"
        case title
        case artist
        case yearCreated = "year_created"
        case medium
        case dimensions
        case currentLocation = "current_location"
        case imageUrlHighres = "image_url_highres"
        case imageUrlThumb = "image_url_thumb"
        case licenseType = "license_type"
        case theologicalSignificanceEn = "theological_significance_en"
        case theologicalSignificanceVi = "theological_significance_vi"
    }

    /// Returns the localized theological significance according to the language mode.
    func localizedTheologicalSignificance(for language: LanguageMode) -> String {
        language == .vietnamese ? theologicalSignificanceVi : theologicalSignificanceEn
    }

    /// Convenience initializer to construct an ArtDossier from an AnnoEntry and ArtworkCandidate.
    init(
        artworkId: String,
        feastAssociation: String,
        title: String,
        artist: String,
        yearCreated: String,
        medium: String = "Sacred Masterwork",
        dimensions: String = "Historical Dimension",
        currentLocation: String = "Ecclesial Archive",
        imageUrlHighres: String,
        imageUrlThumb: String,
        licenseType: String = "Public Domain",
        theologicalSignificanceEn: String,
        theologicalSignificanceVi: String
    ) {
        self.artworkId = artworkId
        self.feastAssociation = feastAssociation
        self.title = title
        self.artist = artist
        self.yearCreated = yearCreated
        self.medium = medium
        self.dimensions = dimensions
        self.currentLocation = currentLocation
        self.imageUrlHighres = imageUrlHighres
        self.imageUrlThumb = imageUrlThumb
        self.licenseType = licenseType
        self.theologicalSignificanceEn = theologicalSignificanceEn
        self.theologicalSignificanceVi = theologicalSignificanceVi
    }

    /// Adapter initializer from AnnoEntry
    init(from entry: AnnoEntry) {
        self.artworkId = "art-\(entry.id)"
        self.feastAssociation = entry.liturgical.titleEn
        self.title = entry.artwork.title
        self.artist = entry.artwork.maker
        self.yearCreated = entry.artwork.dateLabel
        self.medium = "Sacred Masterwork"
        self.dimensions = "Historical Collection"
        self.currentLocation = entry.place?.name ?? "Sacred Collection"
        self.imageUrlHighres = entry.artwork.sourceUrl
        self.imageUrlThumb = entry.artwork.sourceUrl
        self.licenseType = entry.artwork.status
        self.theologicalSignificanceEn = entry.primary.summaryEn
        self.theologicalSignificanceVi = entry.primary.summaryVi
    }
}

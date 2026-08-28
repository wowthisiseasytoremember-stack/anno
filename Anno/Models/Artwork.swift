//  Artwork.swift
//  Anno
//
//  SwiftData model for sacred artwork dossiers.

import Foundation
import SwiftData

@Model
final class Artwork {
    @Attribute(.unique) var id: String
    var title: String
    var artist: String
    var yearCreated: String
    var medium: String
    var dimensions: String
    var currentLocation: String
    var imageUrlHighRes: String
    var imageUrlThumb: String
    var licenseType: String
    var theologicalSignificanceEn: String
    var theologicalSignificanceVi: String
    var feastAssociation: String

    init(
        id: String,
        title: String,
        artist: String,
        yearCreated: String,
        medium: String,
        dimensions: String,
        currentLocation: String,
        imageUrlHighRes: String,
        imageUrlThumb: String,
        licenseType: String,
        theologicalSignificanceEn: String,
        theologicalSignificanceVi: String,
        feastAssociation: String
    ) {
        self.id = id
        self.title = title
        self.artist = artist
        self.yearCreated = yearCreated
        self.medium = medium
        self.dimensions = dimensions
        self.currentLocation = currentLocation
        self.imageUrlHighRes = imageUrlHighRes
        self.imageUrlThumb = imageUrlThumb
        self.licenseType = licenseType
        self.theologicalSignificanceEn = theologicalSignificanceEn
        self.theologicalSignificanceVi = theologicalSignificanceVi
        self.feastAssociation = feastAssociation
    }
}
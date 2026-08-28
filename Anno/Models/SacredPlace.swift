//  SacredPlace.swift
//  Anno
//
//  SwiftData model for sacred places and sanctuaries.

import Foundation
import SwiftData

@Model
final class SacredPlace {
    @Attribute(.unique) var id: String
    var name: String
    var latitude: Double
    var longitude: Double
    var confidenceRaw: String
    var sourceUrl: String

    init(id: String, name: String, latitude: Double, longitude: Double, confidence: ConfidenceLevel, sourceUrl: String) {
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.confidenceRaw = confidence.rawValue
        self.sourceUrl = sourceUrl
    }

    var confidence: ConfidenceLevel {
        get { ConfidenceLevel(rawValue: confidenceRaw) ?? .contextual }
        set { confidenceRaw = newValue.rawValue }
    }
}
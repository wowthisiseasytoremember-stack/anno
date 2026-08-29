//  Visit.swift
//  Anno
//
//  SwiftData model for visited site records (pilgrim passport stamps).

import Foundation
import SwiftData

@Model
final class Visit {
    @Attribute(.unique) var id: UUID = UUID()
    var locationID: String = ""
    var placeName: String = ""
    var traditionRaw: String = ""
    var arrivalDate: Date = Date()
    var stampCode: String = ""
    var latitude: Double = 0.0
    var longitude: Double = 0.0

    init(locationID: String, placeName: String, tradition: String, latitude: Double, longitude: Double) {
        self.id = UUID()
        self.locationID = locationID
        self.placeName = placeName
        self.traditionRaw = tradition
        self.latitude = latitude
        self.longitude = longitude
        self.arrivalDate = Date()
        self.stampCode = "SIGIL-\(Int.random(in: 1000...9999))-\(String(placeName.prefix(3).uppercased()))"
    }
}
//  FieldNote.swift
//  Anno
//
//  SwiftData model for pilgrim reflections and field notes.

import Foundation
import SwiftData

@Model
final class FieldNote {
    @Attribute(.unique) var id: UUID = UUID()
    var journeyID: UUID
    var locationID: String
    var placeName: String
    var text: String
    var createdAt: Date = Date()

    init(journeyID: UUID, locationID: String, placeName: String, text: String) {
        self.id = UUID()
        self.journeyID = journeyID
        self.locationID = locationID
        self.placeName = placeName
        self.text = text
        self.createdAt = Date()
    }
}
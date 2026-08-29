//  Journey.swift
//  Anno
//
//  SwiftData model for pilgrim journey sessions.

import Foundation
import SwiftData

@Model
final class Journey {
    @Attribute(.unique) var id: UUID = UUID()
    var startDate: Date = Date()
    var endDate: Date?
    var routePackID: String?
    var routePackTitle: String?
    var statusRaw: String = JourneyStatus.active.rawValue
    var totalDistanceWalked: Double = 0.0

    @Relationship(deleteRule: .cascade) var visits: [Visit] = []
    @Relationship(deleteRule: .cascade) var notes: [FieldNote] = []

    init(routePackID: String? = nil, routePackTitle: String? = nil) {
        self.id = UUID()
        self.startDate = Date()
        self.routePackID = routePackID
        self.routePackTitle = routePackTitle
    }
}

enum JourneyStatus: String, Codable, CaseIterable {
    case active
    case completed
    case paused
}
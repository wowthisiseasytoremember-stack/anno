//  Devotional.swift
//  Anno
//
//  Data model representing a daily Catholic devotional meditation,
//  scripture verse, and prayer in English and Vietnamese.

import Foundation

struct DevotionalPoolFixture: Codable {
    let schemaVersion: String
    let totalDays: Int
    let descriptionEn: String
    let descriptionVi: String
    let devotionals: [Devotional]
}

struct Devotional: Codable, Identifiable, Hashable {
    var id: Int { dayOfYear }
    let dayOfYear: Int
    let themeEn: String
    let themeVi: String
    let scriptureReference: String
    let scriptureTextEn: String
    let scriptureTextVi: String
    let reflectionTitleEn: String
    let reflectionTitleVi: String
    let reflectionBodyEn: String
    let reflectionBodyVi: String
    let authorOrSource: String
    let dailyPrayerEn: String
    let dailyPrayerVi: String
}

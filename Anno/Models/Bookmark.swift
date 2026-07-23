//  Bookmark.swift
//  DailyDevotionKJVForWomen
//
//  SwiftData model persisting a bookmarked verse.
//

import Foundation
import SwiftData

/// A verse the user has saved. Persisted locally with SwiftData.
@Model
final class Bookmark {
    /// Stable reference id, e.g. "john.3.16". Unique per bookmark.
    @Attribute(.unique) var referenceID: String
    var bookID: String
    var bookName: String
    var chapter: Int
    var verse: Int
    var text: String
    var dateAdded: Date
    /// Optional colour tag index for sorting/organising later.
    var note: String

    init(reference: VerseReference, text: String, note: String = "") {
        self.referenceID = reference.id
        self.bookID = reference.bookID
        self.bookName = reference.bookName
        self.chapter = reference.chapter
        self.verse = reference.verse
        self.text = text
        self.dateAdded = .now
        self.note = note
    }

    var reference: VerseReference {
        VerseReference(bookID: bookID, bookName: bookName, chapter: chapter, verse: verse)
    }

    var displayReference: String { "\(bookName) \(chapter):\(verse)" }
}
//
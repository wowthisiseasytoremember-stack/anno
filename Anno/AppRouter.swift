//  AppRouter.swift
//  DailyDevotionKJVForWomen
//
//  Shared navigation state so App Intents / widgets and in-app actions can
//  drive navigation to specific destinations.
//

import SwiftUI
import Observation

/// The main tabs of the app.
enum AppTab: Hashable {
    case today, library, search, bookmarks, settings
}

/// Type-safe navigation destinations pushed onto reader stacks.
enum ReaderRoute: Hashable {
    case book(String)
    case chapter(bookID: String, chapter: Int, highlightVerse: Int?)
}

/// Observable router coordinating tab selection and deep links.
@Observable
@MainActor
final class AppRouter {
    var selectedTab: AppTab = .today
    var libraryPath = NavigationPath()

    /// Opens a specific verse in the reader tab.
    func openVerse(_ reference: VerseReference) {
        selectedTab = .library
        libraryPath = NavigationPath()
        libraryPath.append(ReaderRoute.book(reference.bookID))
        libraryPath.append(
            ReaderRoute.chapter(
                bookID: reference.bookID,
                chapter: reference.chapter,
                highlightVerse: reference.verse
            )
        )
    }

    func openChapter(bookID: String, chapter: Int) {
        selectedTab = .library
        libraryPath = NavigationPath()
        libraryPath.append(ReaderRoute.book(bookID))
        libraryPath.append(ReaderRoute.chapter(bookID: bookID, chapter: chapter, highlightVerse: nil))
    }
}
//
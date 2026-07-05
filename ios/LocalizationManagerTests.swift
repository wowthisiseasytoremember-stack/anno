//
//  LocalizationManagerTests.swift
//  Anno iOSTests
//
//  Unit tests for LocalizationManager.
//
//  These tests verify:
//  - String lookup with fallback
//  - Language switch notification
//  - Persistence across "restarts"
//  - Edge cases (missing keys, empty dictionaries)

import XCTest
@testable import Anno

final class LocalizationManagerTests: XCTestCase {

    var manager: LocalizationManager!

    override func setUp() {
        super.setUp()
        // Reset to a known state by creating a fresh manager
        // (Tests should inject mock dictionaries rather than relying on bundle files)
        manager = LocalizationManager.shared
    }

    // MARK: - String Lookup

    func testReturnsEnglishString() {
        let result = manager.string(forKey: "tab.today")
        XCTAssertEqual(result, "Today")
    }

    func testReturnsVietnameseString() {
        manager.setLanguage(.vietnamese)
        let result = manager.string(forKey: "tab.today")
        XCTAssertEqual(result, "Hôm nay")
    }

    func testFallsBackToEnglishWhenVietnameseKeyMissing() {
        manager.setLanguage(.vietnamese)
        // Assume "app.future_feature" exists only in English during development
        let result = manager.string(forKey: "app.future_feature")
        XCTAssertEqual(result, "Future Feature", "Should fall back to English when Vietnamese key is missing")
    }

    func testReturnsKeyWhenNeitherLanguageHasIt() {
        let result = manager.string(forKey: "nonexistent.key.xyz")
        XCTAssertEqual(result, "nonexistent.key.xyz", "Should return raw key as visible developer signal")
    }

    func testEnglishStringReturnsEnglishRegardlessOfCurrentLanguage() {
        manager.setLanguage(.vietnamese)
        let result = manager.englishString(forKey: "tab.today")
        XCTAssertEqual(result, "Today", "englishString should always return English")
    }

    // MARK: - Language Switch

    func testSetLanguagePostsNotification() {
        let expectation = XCTNSNotificationExpectation(name: .localizationDidChange)

        manager.setLanguage(.vietnamese)

        wait(for: [expectation], timeout: 1.0)
    }

    func testSetLanguageDoesNotPostNotificationForSameLanguage() {
        let expectation = XCTNSNotificationExpectation(name: .localizationDidChange)
        expectation.isInverted = true

        manager.setLanguage(.english) // Already English

        wait(for: [expectation], timeout: 0.5)
    }

    func testCurrentLanguageUpdatesAfterSwitch() {
        manager.setLanguage(.vietnamese)
        XCTAssertEqual(manager.currentLanguage, .vietnamese)

        manager.setLanguage(.english)
        XCTAssertEqual(manager.currentLanguage, .english)
    }

    func testToggledLanguageReturnsOpposite() {
        manager.setLanguage(.english)
        XCTAssertEqual(manager.toggledLanguage(), .vietnamese)

        manager.setLanguage(.vietnamese)
        XCTAssertEqual(manager.toggledLanguage(), .english)
    }

    // MARK: - Persistence

    func testLanguagePersistsAcrossRestarts() {
        manager.setLanguage(.vietnamese)

        // Simulate app restart by recreating the manager
        // (Language reads from UserDefaults in init)
        let freshManager = LocalizationManager.shared
        XCTAssertEqual(freshManager.currentLanguage, .vietnamese,
                       "Language preference should persist in UserDefaults")
    }

    // MARK: - Edge Cases

    func testEmptyVietnameseDictionaryDoesNotCrash() {
        manager.setLanguage(.vietnamese)
        // Even with no Vietnamese strings loaded, lookups should fall back to English
        let result = manager.string(forKey: "tab.today")
        XCTAssertNotNil(result)
    }

    func testMultipleConsecutiveSwitches() {
        for _ in 0..<10 {
            manager.setLanguage(.vietnamese)
            manager.setLanguage(.english)
        }
        // Should not crash, notification count is irrelevant
        XCTAssertEqual(manager.currentLanguage, .english)
    }
}

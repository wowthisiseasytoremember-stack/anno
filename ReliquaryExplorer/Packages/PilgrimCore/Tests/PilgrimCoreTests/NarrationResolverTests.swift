import PilgrimCore
import XCTest

@testable import PilgrimCore

final class NarrationResolverTests: XCTestCase {
    private let multilingual = SanctuarySite(
        id: "assisi",
        name: "Assisi",
        latitude: 43.07,
        longitude: 12.39,
        radiusMeters: 70,
        narrations: [
            "en": LocalizedNarration(audioFileName: "assisi_en", transcript: "English"),
            "it": LocalizedNarration(audioFileName: "assisi_it", transcript: "Italiano"),
            "es": LocalizedNarration(audioFileName: "assisi_es", transcript: "Español"),
        ]
    )

    private let italianOnly = SanctuarySite(
        id: "torino",
        name: "Torino",
        latitude: 45.07,
        longitude: 7.68,
        radiusMeters: 50,
        narrations: ["it": LocalizedNarration(audioFileName: "torino_it", transcript: "Italiano")]
    )

    func testExactLanguageMatch() {
        let resolver = NarrationResolver(preferredLanguages: ["it-IT"])
        XCTAssertEqual(resolver.narration(for: multilingual)?.language, "it")
    }

    func testRegionStrippedMatching() {
        // A Mexican-Spanish device should get the generic Spanish track.
        let resolver = NarrationResolver(preferredLanguages: ["es-MX", "en-US"])
        XCTAssertEqual(resolver.narration(for: multilingual)?.language, "es")
    }

    func testEnglishFallback() {
        let resolver = NarrationResolver(preferredLanguages: ["ja-JP"])
        XCTAssertEqual(resolver.narration(for: multilingual)?.language, "en")
    }

    func testOnlyAvailableTrackWhenNoEnglish() {
        let resolver = NarrationResolver(preferredLanguages: ["ja-JP"])
        XCTAssertEqual(resolver.narration(for: italianOnly)?.language, "it")
    }

    func testExplicitOverrideWins() {
        let resolver = NarrationResolver(preferredLanguages: ["en-US"], overrideLanguageCode: "it")
        XCTAssertEqual(resolver.narration(for: multilingual)?.language, "it")
    }

    func testOverrideFallsBackWhenUnavailable() {
        let resolver = NarrationResolver(preferredLanguages: ["it-IT"], overrideLanguageCode: "fr")
        XCTAssertEqual(resolver.narration(for: italianOnly)?.language, "it")
    }

    func testEmptyNarrationsReturnsNil() {
        let empty = SanctuarySite(
            id: "empty", name: "Empty", latitude: 0, longitude: 0, radiusMeters: 50, narrations: [:]
        )
        XCTAssertNil(NarrationResolver(preferredLanguages: ["en"]).narration(for: empty))
    }
}

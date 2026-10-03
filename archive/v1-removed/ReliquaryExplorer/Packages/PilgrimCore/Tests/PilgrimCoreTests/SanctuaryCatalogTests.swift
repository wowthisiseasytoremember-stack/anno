import PilgrimCore
import XCTest

@testable import PilgrimCore

final class SanctuaryCatalogTests: XCTestCase {
    private func temporaryFile(_ contents: String) throws -> URL {
        let url = FileManager.default.temporaryDirectory
            .appendingPathComponent("catalog_\(UUID().uuidString).json")
        try contents.write(to: url, atomically: true, encoding: .utf8)
        addTeardownBlock { try? FileManager.default.removeItem(at: url) }
        return url
    }

    func testDecodesPreferredNarrationsForm() throws {
        let json = """
        [{
          "id": "s1", "name": "Sanctuary One",
          "latitude": 42.88, "longitude": -8.54, "radiusMeters": 60,
          "narrations": {
            "en": {"audioFileName": "a_en", "transcript": "English"},
            "es": {"audioFileName": "a_es", "transcript": "Español"}
          }
        }]
        """
        let catalog = try SanctuaryCatalog.load(url: temporaryFile(json))
        XCTAssertEqual(catalog.sites.count, 1)
        XCTAssertEqual(catalog.sites[0].narrations["es"]?.audioFileName, "a_es")
    }

    func testDecodesLegacyFlatFormAsEnglish() throws {
        let json = """
        [{
          "id": "s2", "name": "Sanctuary Two",
          "latitude": 45.07, "longitude": 7.68, "radiusMeters": 40,
          "audioFileName": "hagiography_holy_shroud",
          "transcript": "Entering the perimeter."
        }]
        """
        let catalog = try SanctuaryCatalog.load(url: temporaryFile(json))
        XCTAssertEqual(catalog.sites[0].narrations["en"]?.audioFileName, "hagiography_holy_shroud")
        XCTAssertEqual(catalog.sites[0].narrations.count, 1)
    }

    func testLoadsBundledFixtureAndLegacyFixture() throws {
        // The packaged production config.
        let bundled = try SanctuaryCatalog.load(bundle: .module)
        XCTAssertFalse(bundled.sites.isEmpty, "Packaged SanctuariesConfig.json should decode")

        // The legacy-form test fixture demonstrates config compatibility.
        let fixtureURL = try XCTUnwrap(
            Bundle.module.url(forResource: "legacy_flat_sanctuaries", withExtension: "json")
            ?? Bundle(for: type(of: self)).url(forResource: "legacy_flat_sanctuaries", withExtension: "json")
        )
        let legacy = try SanctuaryCatalog.load(url: fixtureURL)
        XCTAssertEqual(legacy.sites.count, 2)
        XCTAssertEqual(legacy.sites[0].narrations["en"]?.transcript.prefix(15), "You are approac")
    }

    func testRejectsDuplicateIDs() throws {
        let json = """
        [
          {"id": "dup", "name": "A", "latitude": 0, "longitude": 0, "radiusMeters": 50, "audioFileName": "a", "transcript": "t"},
          {"id": "dup", "name": "B", "latitude": 1, "longitude": 1, "radiusMeters": 50, "audioFileName": "a", "transcript": "t"}
        ]
        """
        XCTAssertThrowsError(try SanctuaryCatalog.load(url: temporaryFile(json))) { error in
            guard case let SanctuaryCatalogError.duplicateSiteIDs(ids) = error else {
                return XCTFail("Expected duplicateSiteIDs, got \(error)")
            }
            XCTAssertEqual(ids, ["dup"])
        }
    }

    func testRejectsInvalidRadiusAndCoordinates() throws {
        let badRadius = """
        [{"id": "r", "name": "R", "latitude": 0, "longitude": 0, "radiusMeters": 5, "audioFileName": "a", "transcript": "t"}]
        """
        XCTAssertThrowsError(try SanctuaryCatalog.load(url: temporaryFile(badRadius)))

        let badCoordinate = """
        [{"id": "c", "name": "C", "latitude": 120, "longitude": 0, "radiusMeters": 50, "audioFileName": "a", "transcript": "t"}]
        """
        XCTAssertThrowsError(try SanctuaryCatalog.load(url: temporaryFile(badCoordinate)))
    }

    func testSiteLookup() throws {
        let json = """
        [{"id": "x", "name": "X", "latitude": 10, "longitude": 20, "radiusMeters": 80, "audioFileName": "a", "transcript": "t"}]
        """
        let catalog = try SanctuaryCatalog.load(url: temporaryFile(json))
        XCTAssertEqual(catalog.site(withID: "x")?.name, "X")
        XCTAssertNil(catalog.site(withID: "missing"))
    }
}

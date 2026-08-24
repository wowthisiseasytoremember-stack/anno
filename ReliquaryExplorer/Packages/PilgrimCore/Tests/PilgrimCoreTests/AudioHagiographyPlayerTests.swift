import Foundation
import PilgrimCore
import XCTest

@testable import PilgrimCore

// MARK: - Fakes

final class FakeAudioEngine: AudioPlaybackEngine {
    var loadError: Error?
    var shouldDeclinePlay = false
    private(set) var loadedURLs: [URL] = []
    private(set) var playCount = 0
    private(set) var stopCount = 0
    private(set) var pauseCount = 0
    var isPlaying = false
    var currentTime: TimeInterval = 0
    var duration: TimeInterval = 42
    var onFinished: (() -> Void)?

    func load(url: URL) throws {
        if let loadError { throw loadError }
        loadedURLs.append(url)
    }

    func play() -> Bool {
        playCount += 1
        isPlaying = !shouldDeclinePlay
        return isPlaying
    }

    func pause() { pauseCount += 1; isPlaying = false }
    func stop() { stopCount += 1; isPlaying = false }
}

final class StubAudioFileResolver: AudioFileResolving {
    var urlsByName: [String: URL] = [:]
    func audioURL(forResource name: String) -> URL? { urlsByName[name] }
}

// MARK: - Tests

@MainActor
final class AudioHagiographyPlayerTests: XCTestCase {
    private let bilingual = SanctuarySite(
        id: "assisi",
        name: "Assisi",
        latitude: 43.07,
        longitude: 12.39,
        radiusMeters: 70,
        narrations: [
            "en": LocalizedNarration(audioFileName: "assisi_en", transcript: "English"),
            "it": LocalizedNarration(audioFileName: "assisi_it", transcript: "Italiano"),
        ]
    )

    private func flushLoops() async {
        try? await Task.sleep(nanoseconds: 100_000_000)
    }

    func testPlayResolvesLanguageAndStartsEngine() async {
        let engine = FakeAudioEngine()
        let resolver = StubAudioFileResolver()
        let en = URL(fileURLWithPath: "/bundle/assisi_en.m4a")
        resolver.urlsByName["assisi_en"] = en

        let player = AudioHagiographyPlayer(
            audioFileResolver: resolver,
            narrationResolver: { NarrationResolver(preferredLanguages: ["en-US"]) },
            engine: engine
        )

        player.play(site: bilingual)
        await flushLoops()

        XCTAssertEqual(engine.loadedURLs, [en])
        XCTAssertEqual(engine.playCount, 1)
        XCTAssertEqual(player.snapshot?.siteID, "assisi")
        XCTAssertEqual(player.snapshot?.language, "en")
    }

    func testMissingAssetEmitsFailureEvent() async {
        let engine = FakeAudioEngine()
        let player = AudioHagiographyPlayer(
            audioFileResolver: StubAudioFileResolver(),
            narrationResolver: { NarrationResolver(preferredLanguages: ["en"]) },
            engine: engine
        )

        var received: [HagiographyPlaybackEvent] = []
        let task = Task {
            for await event in player.events {
                received.append(event)
                if case .failed = event.kind { break }
            }
        }

        player.play(site: bilingual)
        await flushLoops()
        task.cancel()

        XCTAssertEqual(received.count, 1)
        XCTAssertEqual(received[0].siteID, "assisi")
        guard case .failed = received[0].kind else {
            return XCTFail("Expected a .failed event for the missing asset")
        }
        XCTAssertEqual(engine.playCount, 0)
        XCTAssertNil(player.snapshot)
    }

    func testStopReplacesTrackAndEmits() async {
        let engine = FakeAudioEngine()
        let resolver = StubAudioFileResolver()
        resolver.urlsByName["assisi_en"] = URL(fileURLWithPath: "/a.m4a")
        resolver.urlsByName["assisi_it"] = URL(fileURLWithPath: "/b.m4a")

        let player = AudioHagiographyPlayer(
            audioFileResolver: resolver,
            narrationResolver: { NarrationResolver(preferredLanguages: ["it-IT"]) },
            engine: engine
        )

        player.play(site: bilingual)
        XCTAssertEqual(engine.loadedURLs.map(\.lastPathComponent), ["b.m4a"])

        player.play(site: bilingual) // second play stops and reloads
        XCTAssertEqual(engine.stopCount, 1)
        XCTAssertEqual(engine.loadedURLs.count, 2)
        XCTAssertEqual(player.snapshot?.language, "it")
    }

    func testNaturalFinishClearsSnapshot() async {
        let engine = FakeAudioEngine()
        let resolver = StubAudioFileResolver()
        resolver.urlsByName["assisi_en"] = URL(fileURLWithPath: "/a.m4a")

        let player = AudioHagiographyPlayer(
            audioFileResolver: resolver,
            narrationResolver: { NarrationResolver(preferredLanguages: ["en"]) },
            engine: engine
        )

        player.play(site: bilingual)
        XCTAssertNotNil(player.snapshot)

        engine.onFinished?()
        await flushLoops()
        XCTAssertNil(player.snapshot)
    }
}

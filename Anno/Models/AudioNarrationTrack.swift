//  AudioNarrationTrack.swift
//  Anno
//
//  Data model representing studio-recorded high-fidelity sacred audio narration,
//  bilingual liturgical spoken reflections, sacred chant accompaniment, and cue points.

import Foundation

// MARK: - Catalog Fixture Container

public struct AudioNarrationCatalog: Codable, Sendable {
    public let schemaVersion: String
    public let curatedOn: String
    public let descriptionEn: String
    public let descriptionVi: String
    public let totalTracks: Int
    public let tracks: [AudioNarrationTrack]

    enum CodingKeys: String, CodingKey {
        case schemaVersion = "schema_version"
        case curatedOn = "curated_on"
        case descriptionEn = "description_en"
        case descriptionVi = "description_vi"
        case totalTracks = "total_tracks"
        case tracks
    }

    public init(
        schemaVersion: String = "anno.audio_narration.v1",
        curatedOn: String = "2026-08-24",
        descriptionEn: String = "",
        descriptionVi: String = "",
        totalTracks: Int = 0,
        tracks: [AudioNarrationTrack] = []
    ) {
        self.schemaVersion = schemaVersion
        self.curatedOn = curatedOn
        self.descriptionEn = descriptionEn
        self.descriptionVi = descriptionVi
        self.totalTracks = totalTracks
        self.tracks = tracks
    }
}

// MARK: - Cue Point / Chapter Marker

public struct AudioCuePoint: Codable, Identifiable, Hashable, Sendable {
    public var id: Double { timeSeconds }
    public let timeSeconds: Double
    public let titleEn: String
    public let titleVi: String

    enum CodingKeys: String, CodingKey {
        case timeSeconds = "time_seconds"
        case titleEn = "title_en"
        case titleVi = "title_vi"
    }

    public init(timeSeconds: Double, titleEn: String, titleVi: String) {
        self.timeSeconds = timeSeconds
        self.titleEn = titleEn
        self.titleVi = titleVi
    }

    public func title(for language: LanguageMode) -> String {
        language == .vietnamese ? titleVi : titleEn
    }
}

// MARK: - Audio Narration Track

public struct AudioNarrationTrack: Codable, Identifiable, Hashable, Sendable {
    public var id: String { audioId }
    public let audioId: String
    public let date: String?
    public let liturgicalDay: String?
    public let feastRank: String?
    public let titleEn: String
    public let titleVi: String
    public let audioUrlEn: String
    public let audioUrlVi: String
    public let durationSeconds: Double
    public let narratorName: String
    public let narratorNameVi: String?
    public let sacredMusicBackground: String
    public let musicLicenseInfo: String?
    public let audioFormat: String?
    public let bitrateKbps: Int?
    public let fileSizeBytes: Int?
    public let artworkUrl: String?
    public let cuePoints: [AudioCuePoint]?
    public let transcriptEn: String
    public let transcriptVi: String

    enum CodingKeys: String, CodingKey {
        case audioId = "audio_id"
        case date
        case liturgicalDay = "liturgical_day"
        case feastRank = "feast_rank"
        case titleEn = "title_en"
        case titleVi = "title_vi"
        case audioUrlEn = "audio_url_en"
        case audioUrlVi = "audio_url_vi"
        case durationSeconds = "duration_seconds"
        case narratorName = "narrator_name"
        case narratorNameVi = "narrator_name_vi"
        case sacredMusicBackground = "sacred_music_background"
        case musicLicenseInfo = "music_license_info"
        case audioFormat = "audio_format"
        case bitrateKbps = "bitrate_kbps"
        case fileSizeBytes = "file_size_bytes"
        case artworkUrl = "artwork_url"
        case cuePoints = "cue_points"
        case transcriptEn = "transcript_en"
        case transcriptVi = "transcript_vi"
    }

    public init(
        audioId: String,
        date: String? = nil,
        liturgicalDay: String? = nil,
        feastRank: String? = nil,
        titleEn: String,
        titleVi: String,
        audioUrlEn: String,
        audioUrlVi: String,
        durationSeconds: Double,
        narratorName: String,
        narratorNameVi: String? = nil,
        sacredMusicBackground: String,
        musicLicenseInfo: String? = nil,
        audioFormat: String? = "audio/mp4; codecs=mp4a.40.2",
        bitrateKbps: Int? = 192,
        fileSizeBytes: Int? = nil,
        artworkUrl: String? = nil,
        cuePoints: [AudioCuePoint]? = nil,
        transcriptEn: String,
        transcriptVi: String
    ) {
        self.audioId = audioId
        self.date = date
        self.liturgicalDay = liturgicalDay
        self.feastRank = feastRank
        self.titleEn = titleEn
        self.titleVi = titleVi
        self.audioUrlEn = audioUrlEn
        self.audioUrlVi = audioUrlVi
        self.durationSeconds = durationSeconds
        self.narratorName = narratorName
        self.narratorNameVi = narratorNameVi
        self.sacredMusicBackground = sacredMusicBackground
        self.musicLicenseInfo = musicLicenseInfo
        self.audioFormat = audioFormat
        self.bitrateKbps = bitrateKbps
        self.fileSizeBytes = fileSizeBytes
        self.artworkUrl = artworkUrl
        self.cuePoints = cuePoints
        self.transcriptEn = transcriptEn
        self.transcriptVi = transcriptVi
    }

    public func title(for language: LanguageMode) -> String {
        language == .vietnamese ? titleVi : titleEn
    }

    public func audioURL(for language: LanguageMode) -> URL? {
        let raw = language == .vietnamese ? audioUrlVi : audioUrlEn
        // Remote CDN URL (http/https) takes precedence.
        if let url = URL(string: raw), let scheme = url.scheme, scheme == "http" || scheme == "https" {
            return url
        }
        // Otherwise resolve `raw` as a local bundled resource (with or without extension).
        let name = (raw as NSString).deletingPathExtension
        let ext = (raw as NSString).pathExtension.isEmpty ? "mp3" : (raw as NSString).pathExtension
        return Bundle.main.url(forResource: name, withExtension: ext)
    }

    public func narrator(for language: LanguageMode) -> String {
        if language == .vietnamese, let vi = narratorNameVi, !vi.isEmpty {
            return vi
        }
        return narratorName
    }

    public func transcript(for language: LanguageMode) -> String {
        language == .vietnamese ? transcriptVi : transcriptEn
    }
}

// MARK: - Playback Controls Options

public enum PlaybackSpeedOption: Float, CaseIterable, Identifiable, Sendable {
    case speed0_75x = 0.75
    case speed1_0x = 1.0
    case speed1_25x = 1.25
    case speed1_5x = 1.5
    case speed2_0x = 2.0

    public var id: Float { rawValue }

    public var label: String {
        switch self {
        case .speed0_75x: return "0.75×"
        case .speed1_0x:  return "1.0×"
        case .speed1_25x: return "1.25×"
        case .speed1_5x:  return "1.5×"
        case .speed2_0x:  return "2.0×"
        }
    }
}

public enum SleepTimerOption: Equatable, Hashable, Identifiable, Sendable {
    case off
    case minutes(Int)
    case endOfTrack

    public var id: String {
        switch self {
        case .off: return "off"
        case .minutes(let m): return "min_\(m)"
        case .endOfTrack: return "end_of_track"
        }
    }

    public func label(for language: LanguageMode) -> String {
        switch self {
        case .off:
            return language == .vietnamese ? "Tắt hẹn giờ" : "Off"
        case .minutes(let m):
            return language == .vietnamese ? "\(m) phút" : "\(m) min"
        case .endOfTrack:
            return language == .vietnamese ? "Hết bài đọc" : "End of Track"
        }
    }

    public var totalSeconds: TimeInterval? {
        switch self {
        case .off: return nil
        case .minutes(let m): return TimeInterval(m * 60)
        case .endOfTrack: return nil // handled dynamically by player
        }
    }

    public static let standardOptions: [SleepTimerOption] = [
        .off,
        .minutes(5),
        .minutes(10),
        .minutes(15),
        .minutes(30),
        .minutes(45),
        .minutes(60),
        .endOfTrack
    ]
}

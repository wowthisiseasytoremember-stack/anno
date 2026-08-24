# Anno Sacred Audio Narration & Devotional Audio Stream Schema

**Schema Version:** `anno.audio_narration.v1`  
**Status:** Canonical Production Specification  
**Initiative:** Monetization & Daily Devotional Craft  
**Domain:** Native SwiftUI (`AVFoundation`, `MediaPlayer`, `AVAudioSession`)  

---

## 1. Overview & Architectural Role

The **Sacred Audio Narration Stream** is a premium feature of Anno designed for contemplative listening, bedtime prayer, daily commuting, and accessibility. Every feast day, saint biography, and devotional reflection provides studio-quality spoken narration accompanied by authentic sacred liturgical music (Gregorian Chant, Renaissance Polyphony, Sacred Harp, Byzantine and Canto liturgies).

### Key Architectural Invariants:
1. **100% Bilingual Parity:** Every audio entry provides twin high-fidelity audio tracks (`audio_url_en` and `audio_url_vi`) and matching verbatim spoken transcripts (`transcript_en` and `transcript_vi`) with full Vietnamese ecclesiastical diacritics.
2. **Deterministic Liturgical Linking:** Audio tracks map directly to calendar dates (`date`), liturgical feast rankings, and entry IDs.
3. **Background Playback & Lock-Screen Integration:** Full support for `AVAudioSession` `.playback` mode, `MPNowPlayingInfoCenter`, and `MPRemoteCommandCenter` (play/pause, scrubbing, 15s skip, playback rate, dynamic lock-screen artwork).
4. **Offline First & Efficient Streaming:** Supports local bundled audio fallback, CDN streaming over progressive AAC-LC (128–256 kbps) / HLS, and local cache.
5. **Sacred Music Accompaniment:** Clear metadata attribution and public domain / licensed provenance for background sacred music styles.

---

## 2. JSON Catalog Schema Specification

A master audio narration catalog adheres to the `anno.audio_narration.v1` format:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AnnoAudioNarrationCatalog",
  "type": "object",
  "required": [
    "schema_version",
    "curated_on",
    "description_en",
    "description_vi",
    "total_tracks",
    "tracks"
  ],
  "properties": {
    "schema_version": { "type": "string", "const": "anno.audio_narration.v1" },
    "curated_on": { "type": "string", "format": "date" },
    "description_en": { "type": "string" },
    "description_vi": { "type": "string" },
    "total_tracks": { "type": "integer", "minimum": 1 },
    "tracks": {
      "type": "array",
      "items": { "$ref": "#/$defs/AudioNarrationTrack" }
    }
  },
  "$defs": {
    "AudioNarrationTrack": {
      "type": "object",
      "required": [
        "audio_id",
        "title_en",
        "title_vi",
        "audio_url_en",
        "audio_url_vi",
        "duration_seconds",
        "narrator_name",
        "sacred_music_background",
        "transcript_en",
        "transcript_vi"
      ],
      "properties": {
        "audio_id": {
          "type": "string",
          "pattern": "^audio-[a-z0-9-]+$"
        },
        "date": {
          "type": ["string", "null"],
          "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
        },
        "liturgical_day": { "type": "string" },
        "feast_rank": { "type": "string" },
        "title_en": { "type": "string", "minLength": 3 },
        "title_vi": { "type": "string", "minLength": 3 },
        "audio_url_en": { "type": "string", "format": "uri" },
        "audio_url_vi": { "type": "string", "format": "uri" },
        "duration_seconds": { "type": "number", "minimum": 1 },
        "narrator_name": { "type": "string", "minLength": 2 },
        "narrator_name_vi": { "type": "string" },
        "sacred_music_background": { "type": "string", "minLength": 3 },
        "music_license_info": { "type": "string" },
        "audio_format": { "type": "string", "default": "audio/mp4; codecs=mp4a.40.2" },
        "bitrate_kbps": { "type": "integer", "minimum": 64 },
        "file_size_bytes": { "type": "integer", "minimum": 1000 },
        "artwork_url": { "type": "string", "format": "uri" },
        "cue_points": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["time_seconds", "title_en", "title_vi"],
            "properties": {
              "time_seconds": { "type": "number", "minimum": 0 },
              "title_en": { "type": "string" },
              "title_vi": { "type": "string" }
            }
          }
        },
        "transcript_en": { "type": "string", "minLength": 20 },
        "transcript_vi": { "type": "string", "minLength": 20 }
      }
    }
  }
}
```

---

## 3. Swift Data Model Integration

The Swift data models bridge directly into `Anno`:

```swift
import Foundation

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
}

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
}

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

    public func title(for language: LanguageMode) -> String {
        language == .vietnamese ? titleVi : titleEn
    }

    public func audioURL(for language: LanguageMode) -> URL? {
        let raw = language == .vietnamese ? audioUrlVi : audioUrlEn
        return URL(string: raw)
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
```

---

## 4. Audio Player Service Architecture (`AudioDevotionalPlayer.swift`)

The player service manages the full AVFoundation and MediaPlayer lifecycle:

1. **Audio Session Configuration:**
   * Configures `AVAudioSession.sharedInstance().setCategory(.playback, mode: .spokenAudio, options: [.allowAirPlay, .allowBluetooth, .allowBluetoothA2DP])` to enable background playback when screen is locked.
   * Handles audio session interruptions (`AVAudioSession.interruptionNotification`) when incoming calls, alarms, or Siri activate.
   * Responds to route change events (e.g. unplugging headphones or disconnecting AirPods) by automatically pausing playback.

2. **Lock Screen Media Controls (`MPRemoteCommandCenter` & `MPNowPlayingInfoCenter`):**
   * Configures responsive remote commands for:
     - `playCommand`, `pauseCommand`, `togglePlayPauseCommand`
     - `changePlaybackPositionCommand` (scrubbing from lock screen slider)
     - `skipForwardCommand` (15 seconds forward)
     - `skipBackwardCommand` (15 seconds backward)
     - `changePlaybackRateCommand` (0.75x, 1.0x, 1.25x, 1.5x, 2.0x)
   * Publishes dynamic lock-screen metadata:
     - `MPMediaItemPropertyTitle`: Track title in active language
     - `MPMediaItemPropertyArtist`: Narrator name & Sacred Music title
     - `MPMediaItemPropertyAlbumTitle`: "Anno — Sacred History & Devotion"
     - `MPNowPlayingInfoPropertyElapsedPlaybackTime`: Current playback timestamp
     - `MPMediaItemPropertyPlaybackDuration`: Total track duration
     - `MPNowPlayingInfoPropertyPlaybackRate`: Current playback rate (or 0.0 when paused)
     - `MPMediaItemPropertyArtwork`: Liturgical art or icon

3. **Sleep Timer Control:**
   * Configurable timers: 5m, 10m, 15m, 30m, 45m, 60m, or "End of Track".
   * Automatically smoothly pauses when the timer expires.

4. **Playback Speed Controls:**
   * Discrete speeds: `0.75x`, `1.0x`, `1.25x`, `1.5x`, `2.0x`.

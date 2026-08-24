#!/usr/bin/env python3
"""
Validation gate for Anno Audio Narration catalog and data schema.
Enforces:
1. Valid JSON format & schema conformance (anno.audio_narration.v1).
2. Complete bilingual parity (EN & VI) for titles, narration transcripts, and cue points.
3. Non-empty required fields: audio_id, duration_seconds, sacred_music_background, URLs.
4. Vietnamese diacritic integrity on all Vietnamese fields.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "Anno/Resources/audio_narration_catalog.json"
SCHEMA_DOC_PATH = ROOT / "docs/AUDIO_NARRATION_SCHEMA.md"
SWIFT_MODEL_PATH = ROOT / "Anno/Models/AudioNarrationTrack.swift"
SWIFT_SERVICE_PATH = ROOT / "Anno/Services/AudioDevotionalPlayer.swift"

VIETNAMESE_DIACRITICS = re.compile(
    r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ]",
    re.IGNORECASE
)

AUDIO_ID_PATTERN = re.compile(r"^audio-[a-z0-9-]+$")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    print("=== Validating Anno Audio Narration Catalog & Services ===")

    # 1. Check file existence
    for path, desc in [
        (SCHEMA_DOC_PATH, "Audio Narration Schema Documentation"),
        (CATALOG_PATH, "Audio Narration JSON Catalog"),
        (SWIFT_MODEL_PATH, "Swift Audio Models"),
        (SWIFT_SERVICE_PATH, "Swift Audio Player Service"),
    ]:
        if not path.exists():
            fail(f"Missing required file: {desc} at {path}")
        print(f"✓ Found {desc} ({path.name})")

    # 2. Parse and validate JSON catalog
    try:
        catalog_data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"Failed to parse JSON in {CATALOG_PATH}: {e}")

    # Check top-level schema fields
    if catalog_data.get("schema_version") != "anno.audio_narration.v1":
        fail(f"Invalid schema_version: expected 'anno.audio_narration.v1', got {catalog_data.get('schema_version')}")

    tracks = catalog_data.get("tracks", [])
    total_tracks = catalog_data.get("total_tracks", 0)

    if len(tracks) != total_tracks:
        fail(f"Track count mismatch: total_tracks={total_tracks} but tracks array has {len(tracks)}")

    if len(tracks) == 0:
        fail("Audio narration catalog is empty; expected >= 1 tracks.")

    print(f"✓ Catalog header valid: {len(tracks)} tracks declared.")

    # 3. Validate each track
    seen_ids = set()
    for idx, track in enumerate(tracks, 1):
        audio_id = track.get("audio_id")
        if not audio_id or not AUDIO_ID_PATTERN.match(audio_id):
            fail(f"Track #{idx}: invalid or missing audio_id: '{audio_id}'")
        if audio_id in seen_ids:
            fail(f"Track #{idx}: duplicate audio_id '{audio_id}'")
        seen_ids.add(audio_id)

        # Check required string fields
        for field in [
            "title_en",
            "title_vi",
            "audio_url_en",
            "audio_url_vi",
            "narrator_name",
            "sacred_music_background",
            "transcript_en",
            "transcript_vi",
        ]:
            val = track.get(field)
            if not val or not isinstance(val, str) or len(val.strip()) == 0:
                fail(f"Track '{audio_id}': missing or empty field '{field}'")

        # Check duration
        duration = track.get("duration_seconds")
        if not isinstance(duration, (int, float)) or duration <= 0:
            fail(f"Track '{audio_id}': invalid duration_seconds: {duration}")

        # Check URLs
        for url_field in ["audio_url_en", "audio_url_vi"]:
            url_val = track.get(url_field, "")
            if not url_val.startswith("https://") and not url_val.startswith("http://"):
                fail(f"Track '{audio_id}': invalid URL in {url_field}: '{url_val}'")

        # Check Vietnamese diacritics
        title_vi = track.get("title_vi", "")
        transcript_vi = track.get("transcript_vi", "")
        if not VIETNAMESE_DIACRITICS.search(title_vi):
            fail(f"Track '{audio_id}': title_vi lacks authentic Vietnamese diacritics: '{title_vi}'")
        if not VIETNAMESE_DIACRITICS.search(transcript_vi):
            fail(f"Track '{audio_id}': transcript_vi lacks authentic Vietnamese diacritics.")

        # Check cue points if present
        cue_points = track.get("cue_points")
        if cue_points is not None:
            if not isinstance(cue_points, list):
                fail(f"Track '{audio_id}': cue_points must be a list")
            for cp_idx, cp in enumerate(cue_points):
                if "time_seconds" not in cp or not isinstance(cp["time_seconds"], (int, float)):
                    fail(f"Track '{audio_id}' cue_point #{cp_idx}: missing or invalid time_seconds")
                if not cp.get("title_en") or not cp.get("title_vi"):
                    fail(f"Track '{audio_id}' cue_point #{cp_idx}: missing title_en or title_vi")

    print(f"✓ All {len(tracks)} audio narration tracks verified against schema rules.")

    # 4. Check Swift code symbols
    swift_model_text = SWIFT_MODEL_PATH.read_text(encoding="utf-8")
    for symbol in ["AudioNarrationCatalog", "AudioNarrationTrack", "AudioCuePoint", "PlaybackSpeedOption", "SleepTimerOption"]:
        if symbol not in swift_model_text:
            fail(f"Missing symbol '{symbol}' in {SWIFT_MODEL_PATH.name}")

    swift_service_text = SWIFT_SERVICE_PATH.read_text(encoding="utf-8")
    for symbol in [
        "AudioDevotionalPlayer",
        "AVPlayer",
        "AVAudioSession",
        "MPNowPlayingInfoCenter",
        "MPRemoteCommandCenter",
        "togglePlayPause",
        "seek(to:",
        "setPlaybackSpeed",
        "setSleepTimer",
        "setLanguage",
    ]:
        if symbol not in swift_service_text:
            fail(f"Missing symbol/method '{symbol}' in {SWIFT_SERVICE_PATH.name}")

    print("✓ Swift models and AudioDevotionalPlayer service symbols verified.")
    print("=== All Audio Narration Validation Checks Passed Successfully! ===")


if __name__ == "__main__":
    main()

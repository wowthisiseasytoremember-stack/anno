#!/usr/bin/env python3
"""Regression tests for the Swift AnnoEntry fixture decode contract."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "validate_fixture_decode", PROJECT_ROOT / "tools" / "validate_fixture_decode.py"
)
validate_fixture_decode = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_fixture_decode)

validate_fixture = validate_fixture_decode.validate_fixture
DEFAULT_FIXTURE = validate_fixture_decode.DEFAULT_FIXTURE


def base_entry() -> dict:
    return {
        "id": "anno-2026-01-01",
        "date": "2026-01-01",
        "weekday": "Thursday",
        "mock_priority": "engine_b_v1",
        "liturgical": {
            "rank": "Feria",
            "color": "green",
            "title_en": "Thursday in Ordinary Time",
            "title_vi": "Thứ Năm Thường Niên",
        },
        "calendars": {
            "julian": "2025-12-19",
            "hebrew": "12 Tevet 5786",
            "islamic_umm_al_qura": "12 Rajab 1447 AH",
            "coptic": "23 Koiak 1742",
            "ethiopian": "23 Tahsas 2018",
        },
        "primary": {
            "type": "liturgical_day",
            "title_en": "Thursday in Ordinary Time",
            "title_vi": "Thứ Năm Thường Niên",
            "summary_en": "A sourced devotional summary.",
            "summary_vi": "Tóm tắt suy niệm có nguồn.",
            "confidence": "confirmed",
            "confidence_note_en": "Confirmed from official calendar.",
            "confidence_note_vi": "Xác nhận từ lịch chính thức.",
            "body_en": "A two-paragraph reflection.",
            "body_vi": "Một bài suy niệm hai đoạn.",
        },
        "place": None,
        "artwork": {
            "title": "Placeholder",
            "maker": "Unattributed",
            "date_label": "",
            "source_url": "",
            "status": "placeholder_only",
        },
        "sources": [
            {"label": "USCCB", "url": "https://bible.usccb.org/", "type": "liturgical_calendar"},
            {"label": "Vatican", "url": "https://www.vatican.va/", "type": "vatican"},
        ],
        "app_hooks": {
            "hero_line_en": "Open today.",
            "hero_line_vi": "Mở hôm nay.",
            "prayer_prompt_en": "Pray with me.",
            "prayer_prompt_vi": "Cầu nguyện cùng nhau.",
        },
    }


class TestSwiftFixtureDecodeContract(unittest.TestCase):
    def test_committed_fixture_matches_swift_contract(self) -> None:
        self.assertTrue(DEFAULT_FIXTURE.exists(), f"fixture missing: {DEFAULT_FIXTURE}")
        import json
        data = json.loads(DEFAULT_FIXTURE.read_text(encoding="utf-8"))
        issues = validate_fixture(data)
        self.assertEqual(issues, [], "\n".join(issues))

    def test_generated_on_is_required(self) -> None:
        data = {
            "schema_version": "1.0",
            "entries": [base_entry()],
        }
        issues = validate_fixture(data)
        self.assertIn("generated_on is not a string", issues)

    def test_null_artwork_field_is_rejected(self) -> None:
        entry = base_entry()
        entry["artwork"]["maker"] = None
        data = {
            "schema_version": "1.0",
            "generated_on": "2026-12-31",
            "entries": [entry],
        }
        issues = validate_fixture(data)
        self.assertIn("entry[0] anno-2026-01-01: artwork.maker is not a string", issues)

    def test_partial_place_object_is_rejected(self) -> None:
        entry = base_entry()
        entry["place"] = {"name": "Jerusalem, Israel"}
        data = {
            "schema_version": "1.0",
            "generated_on": "2026-12-31",
            "entries": [entry],
        }
        issues = validate_fixture(data)
        for expected in (
            "entry[0] anno-2026-01-01: place.latitude is not a number",
            "entry[0] anno-2026-01-01: place.longitude is not a number",
            "entry[0] anno-2026-01-01: place.source_url is not a string",
            "entry[0] anno-2026-01-01: place.confidence is not a supported enum",
        ):
            self.assertIn(expected, issues)

    def test_string_coordinate_is_rejected(self) -> None:
        entry = base_entry()
        entry["place"] = {
            "name": "Jerusalem, Israel",
            "latitude": "31.7784",
            "longitude": 35.2354,
            "confidence": "confirmed",
            "source_url": "https://www.vatican.va/",
        }
        data = {
            "schema_version": "1.0",
            "generated_on": "2026-12-31",
            "entries": [entry],
        }
        issues = validate_fixture(data)
        self.assertIn("entry[0] anno-2026-01-01: place.latitude is not a number", issues)


if __name__ == "__main__":
    unittest.main()

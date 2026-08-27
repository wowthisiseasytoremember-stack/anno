#!/usr/bin/env python3
"""
tools/test_calendar_engine.py
Comprehensive Quality & Liturgical Math Acceptance Test Runner for Engine A.

Validates:
1. Multi-Calendar Deterministic Math across 1,826 days (2026-01-01 to 2030-12-31) in data/calendar_2026_2030.jsonl
2. Western and Eastern Easter Computus (2026-2035)
3. Moveable Feasts mathematical integrity
4. Multi-Proper Liturgical Calendar Resolver (General Roman, USCCB, HDGMVN, 1962 EF)
5. Zero drift in day counts, Julian offsets, JDN sequence, and keviah types
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path

# Add project root and tools to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from calendar_engine import convert_date, compute_julian_offset
from computus_engine import (
    compute_gregorian_easter,
    compute_julian_easter,
    compute_liturgical_year_anchors,
)
from multi_proper_calendar_resolver import MultiProperCalendarResolver


class TestComputusAndMoveableFeasts(unittest.TestCase):
    """Verifies Meeus Computus algorithms and liturgical anchor relationships."""

    KNOWN_GREGORIAN_EASTER = {
        2026: date(2026, 4, 5),
        2027: date(2027, 3, 28),
        2028: date(2028, 4, 16),
        2029: date(2029, 4, 1),
        2030: date(2030, 4, 21),
        2031: date(2031, 4, 13),
        2032: date(2032, 3, 28),
        2033: date(2033, 4, 17),
        2034: date(2034, 4, 9),
        2035: date(2035, 3, 25),
    }

    KNOWN_ORTHODOX_EASTER_GREGORIAN = {
        2026: date(2026, 4, 12),
        2027: date(2027, 5, 2),
        2028: date(2028, 4, 16),
        2029: date(2029, 4, 8),
        2030: date(2030, 4, 28),
    }

    def test_gregorian_easter_dates(self) -> None:
        for year, expected_date in self.KNOWN_GREGORIAN_EASTER.items():
            calculated = compute_gregorian_easter(year)
            self.assertEqual(
                calculated,
                expected_date,
                f"Gregorian Easter mismatch for year {year}: got {calculated}, expected {expected_date}",
            )

    def test_julian_orthodox_easter_dates(self) -> None:
        for year, expected_date in self.KNOWN_ORTHODOX_EASTER_GREGORIAN.items():
            _, calculated = compute_julian_easter(year)
            self.assertEqual(
                calculated,
                expected_date,
                f"Julian/Orthodox Easter mismatch for year {year}: got {calculated}, expected {expected_date}",
            )

    def test_moveable_feast_offsets_integrity(self) -> None:
        for year in range(2026, 2036):
            anchors = compute_liturgical_year_anchors(year)
            easter = date.fromisoformat(anchors["easter_sunday"])
            ash_wed = date.fromisoformat(anchors["ash_wednesday"])
            palm_sun = date.fromisoformat(anchors["palm_sunday"])
            holy_thurs = date.fromisoformat(anchors["holy_thursday"])
            good_fri = date.fromisoformat(anchors["good_friday"])
            holy_sat = date.fromisoformat(anchors["holy_saturday"])
            asc_thurs = date.fromisoformat(anchors["ascension_thursday"])
            asc_sun = date.fromisoformat(anchors["ascension_sunday"])
            pentecost = date.fromisoformat(anchors["pentecost_sunday"])
            trinity = date.fromisoformat(anchors["trinity_sunday"])
            corpus_thurs = date.fromisoformat(anchors["corpus_christi_thursday"])
            corpus_sun = date.fromisoformat(anchors["corpus_christi_sunday"])
            sacred_heart = date.fromisoformat(anchors["most_sacred_heart_of_jesus"])
            advent_1 = date.fromisoformat(anchors["first_sunday_of_advent"])
            advent_4 = date.fromisoformat(anchors["fourth_sunday_of_advent"])
            christmas = date.fromisoformat(anchors["nativity_of_the_lord"])

            self.assertEqual(ash_wed, easter - timedelta(days=46))
            self.assertEqual(palm_sun, easter - timedelta(days=7))
            self.assertEqual(holy_thurs, easter - timedelta(days=3))
            self.assertEqual(good_fri, easter - timedelta(days=2))
            self.assertEqual(holy_sat, easter - timedelta(days=1))
            self.assertEqual(asc_thurs, easter + timedelta(days=39))
            self.assertEqual(asc_sun, easter + timedelta(days=42))
            self.assertEqual(pentecost, easter + timedelta(days=49))
            self.assertEqual(trinity, easter + timedelta(days=56))
            self.assertEqual(corpus_thurs, easter + timedelta(days=60))
            self.assertEqual(corpus_sun, easter + timedelta(days=63))
            self.assertEqual(sacred_heart, easter + timedelta(days=68))

            # Advent rules
            self.assertEqual(advent_1.weekday(), 6)  # Sunday
            self.assertEqual(advent_4.weekday(), 6)  # Sunday
            self.assertEqual(advent_1, advent_4 - timedelta(weeks=3))
            self.assertTrue(advent_4 <= date(year, 12, 24))
            self.assertEqual(christmas, date(year, 12, 25))


class TestMultiProperResolver(unittest.TestCase):
    """Verifies liturgical divergence rules across 4 calendar propers."""

    def setUp(self) -> None:
        self.resolver = MultiProperCalendarResolver()

    def test_vietnamese_martyrs_divergence(self) -> None:
        """Nov 24 must be Solemnity (Lễ Trọng, Red) in Vietnam vs Memorial in General Roman."""
        for yr in [2026, 2027, 2028, 2029]:
            d = date(yr, 11, 24)
            res = self.resolver.resolve_divergences(d)
            self.assertTrue(res["has_divergence"])
            self.assertEqual(res["propers"]["hdgmvn"]["rank"], "Solemnity")
            self.assertEqual(res["propers"]["hdgmvn"]["color"], "Red")
            self.assertIn("Đại Lễ Các Thánh Tử Đạo Việt Nam", res["propers"]["hdgmvn"]["title_vi"])
            self.assertEqual(res["propers"]["general_roman"]["rank"], "Memorial")

        # 2030 has Christ the King on Sunday Nov 24
        d_2030 = date(2030, 11, 24)
        res_2030 = self.resolver.resolve_divergences(d_2030)
        self.assertTrue(res_2030["has_divergence"])
        self.assertEqual(res_2030["propers"]["hdgmvn"]["rank"], "Solemnity")

    def test_usccb_proper_saints(self) -> None:
        """Verifies US-specific sanctoral memorials."""
        # St. Elizabeth Ann Seton (Jan 4)
        res_seton = self.resolver.resolve_date(date(2026, 1, 4), proper="usccb")
        self.assertEqual(res_seton["rank"], "Memorial")
        self.assertIn("Elizabeth Ann Seton", res_seton["title_en"])

        # St. Frances Xavier Cabrini (Nov 13)
        res_cabrini = self.resolver.resolve_date(date(2026, 11, 13), proper="usccb")
        self.assertEqual(res_cabrini["rank"], "Memorial")
        self.assertIn("Cabrini", res_cabrini["title_en"])

        # St. Kateri Tekakwitha (Jul 14)
        res_kateri = self.resolver.resolve_date(date(2026, 7, 14), proper="usccb")
        self.assertEqual(res_kateri["rank"], "Memorial")
        self.assertIn("Kateri", res_kateri["title_en"])

    def test_ascension_transference_divergence(self) -> None:
        """Ascension is Thursday in General Roman/1962 and Sunday in USCCB/HDGMVN."""
        # 2026 Ascension Thursday = 2026-05-14
        d_thurs = date(2026, 5, 14)
        res_thurs = self.resolver.resolve_divergences(d_thurs)
        self.assertTrue(res_thurs["has_divergence"])
        self.assertEqual(res_thurs["propers"]["general_roman"]["rank"], "Solemnity")
        self.assertEqual(res_thurs["propers"]["extraordinary_1962"]["rank"], "1st Class")
        self.assertEqual(res_thurs["propers"]["usccb"]["rank"], "Easter Weekday")

        # 2026 Ascension Sunday = 2026-05-17
        d_sun = date(2026, 5, 17)
        res_sun = self.resolver.resolve_divergences(d_sun)
        self.assertTrue(res_sun["has_divergence"])
        self.assertEqual(res_sun["propers"]["usccb"]["rank"], "Solemnity")
        self.assertEqual(res_sun["propers"]["hdgmvn"]["rank"], "Solemnity")

    def test_1962_septuagesima_and_passiontide(self) -> None:
        """1962 Extraordinary Form seasons compute correctly."""
        # 2026 Easter is April 5. Septuagesima is Feb 1 (Easter - 63d).
        res_sept = self.resolver.get_1962_season_for_date(date(2026, 2, 1))
        self.assertIn("Septuagesima", res_sept["season_en"])
        self.assertEqual(res_sept["default_color"], "Violet")

        # Passion Sunday is March 22 (Easter - 14d)
        res_pass = self.resolver.get_1962_season_for_date(date(2026, 3, 22))
        self.assertIn("Passiontide", res_pass["season_en"])

        # Pentecost Octave (May 24 to May 30)
        res_oct = self.resolver.get_1962_season_for_date(date(2026, 5, 27))
        self.assertEqual(res_oct["season_en"], "Octave of Pentecost")
        self.assertEqual(res_oct["default_color"], "Red")

    def test_rules_json_artifact_exists(self) -> None:
        rules_path = PROJECT_ROOT / "data/assets/liturgical_propers_rules.json"
        self.assertTrue(rules_path.exists(), "liturgical_propers_rules.json must exist")
        data = json.loads(rules_path.read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], "1.0.0")
        self.assertIn("supported_propers", data)
        self.assertIn("sample_benchmark_resolutions_2026_2030", data)
        self.assertGreaterEqual(len(data["sample_benchmark_resolutions_2026_2030"]), 20)


class TestFullFiveYearDataset(unittest.TestCase):
    """Verifies continuous 5-year dataset (2026–2030 = 1,826 days) without drift or missing keys."""

    DATASET_PATH = PROJECT_ROOT / "data/calendar_2026_2030.jsonl"

    def test_jsonl_existence_and_exact_day_count(self) -> None:
        self.assertTrue(self.DATASET_PATH.exists(), f"Missing dataset: {self.DATASET_PATH}")
        with open(self.DATASET_PATH, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        
        # 2026(365) + 2027(365) + 2028(366 leap) + 2029(365) + 2030(365) = 1,826
        self.assertEqual(len(lines), 1826, f"Expected 1826 lines, got {len(lines)}")

    def test_continuous_chronology_and_deterministic_fields(self) -> None:
        expected_date = date(2026, 1, 1)
        prev_jdn = None
        keviah_pattern = re.compile(r"^[1-7](?:g|s|sh)[KH]$")

        with open(self.DATASET_PATH, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f, start=1):
                entry = json.loads(line)

                # 1. Gregorian date continuity
                g_date_str = entry["gregorian_date"]
                g_date = date.fromisoformat(g_date_str)
                self.assertEqual(
                    g_date,
                    expected_date,
                    f"Line {line_idx}: Date sequence broken. Expected {expected_date}, got {g_date}",
                )

                # 2. Gregorian Day of Year
                expected_doy = g_date.timetuple().tm_yday
                self.assertEqual(entry["gregorian_doy"], expected_doy)

                # 3. JDN monotonicity (strictly +1.0 each day)
                current_jdn = entry["jdn_at_boundary"]
                if prev_jdn is not None:
                    self.assertAlmostEqual(
                        current_jdn - prev_jdn,
                        1.0,
                        places=5,
                        msg=f"Line {line_idx}: JDN non-linear step ({prev_jdn} -> {current_jdn})",
                    )
                prev_jdn = current_jdn

                # 4. Julian offset and drift
                julian_data = entry["julian"]
                self.assertEqual(julian_data["offset_days"], 13)
                expected_julian_date = (g_date - timedelta(days=13)).isoformat()
                self.assertEqual(julian_data["date"], expected_julian_date)

                # 5. Hebrew Keviah validity (No '?' characters)
                hebrew_data = entry["hebrew"]
                keviah = hebrew_data["year_type"]
                self.assertIsNotNone(
                    keviah_pattern.match(keviah),
                    f"Line {line_idx} ({g_date_str}): Invalid Hebrew keviah format '{keviah}'",
                )
                self.assertIn("PDT", hebrew_data["sundown_at_anchor"])

                # 6. Islamic Tabular vs Umm al-Qura divergence
                islamic_tab = entry["islamic_tabular"]
                div = islamic_tab["divergence_from_umm_al_qura"]
                self.assertIsInstance(div, int)
                self.assertGreaterEqual(div, 0)
                if div > 0:
                    self.assertIsNotNone(islamic_tab["divergence_note"])

                # 7. Coptic & Ethiopian alignment
                coptic_data = entry["coptic"]
                ethiopian_data = entry["ethiopian"]
                c_year = int(coptic_data["date"].split()[-1])
                e_year = int(ethiopian_data["date"].split()[-1])
                self.assertEqual(e_year, c_year + 276)

                # 8. Byzantine Anno Mundi year
                byz_data = entry["byzantine"]
                byz_year = int(byz_data["date"].split()[-1])
                expected_byz_year = g_date.year + (5508 if g_date.month < 9 else 5509)
                self.assertEqual(byz_year, expected_byz_year)

                # Advance expected date
                expected_date += timedelta(days=1)

        self.assertEqual(expected_date, date(2031, 1, 1))


class TestConvertDateFutureYears(unittest.TestCase):
    """Regression guard: convert_date must not crash on 2027+ (was broken: date - datetime)."""

    FUTURE_DATES = [
        date(2026, 7, 3), date(2027, 1, 1), date(2028, 2, 29),
        date(2029, 1, 1), date(2030, 12, 31),
    ]

    def test_convert_date_runs_for_all_future_years(self) -> None:
        for d in self.FUTURE_DATES:
            with self.subTest(d=d.isoformat()):
                r = convert_date(d)
                self.assertIn("islamic_tabular", r)
                self.assertIn("coptic", r)
                self.assertIn("hebrew", r)
                # Islamic tabular date must be a non-empty AH string
                self.assertTrue(r["islamic_tabular"]["date"].endswith("AH"))

    def test_islamic_tabular_matches_known_2027_01_01(self) -> None:
        r = convert_date(date(2027, 1, 1))
        self.assertEqual(r["islamic_tabular"]["date"], "25 Rajab 1448 AH")


def main() -> None:
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestComputusAndMoveableFeasts))
    suite.addTest(unittest.makeSuite(TestMultiProperResolver))
    suite.addTest(unittest.makeSuite(TestFullFiveYearDataset))
    suite.addTest(unittest.makeSuite(TestConvertDateFutureYears))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    main()

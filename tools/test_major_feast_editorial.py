#!/usr/bin/env python3
"""Fast stdlib-only tests for the four 2026 mandatory bilingual feast records."""
from __future__ import annotations
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from major_feast_editorial import (FIXTURE, RESEARCH, REQUIRED, new_entry,
                                  read_json, source_entries, validate_fixture)


class MajorFeastEditorialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = read_json(FIXTURE)
        cls.upstream = source_entries()
        cls.overlay = read_json(RESEARCH / "2026-11-22_result_vi.json")

    def check(self, edit=None):
        fixture = copy.deepcopy(self.fixture)
        upstream = copy.deepcopy(self.upstream)
        overlay = copy.deepcopy(self.overlay)
        if edit:
            edit(fixture, upstream, overlay)
        return validate_fixture(fixture, upstream, overlay)

    def record(self, fixture, day):
        return next(x for x in fixture["entries"] if x["date"] == day)

    def test_all_four_authoritative_dates_pass(self):
        self.assertEqual(self.check(), [])

    def test_expected_four_major_feasts_are_in_scope(self):
        self.assertEqual(set(REQUIRED),
                         {"2026-08-15", "2026-11-22", "2026-12-08", "2026-12-25"})

    def test_christ_king_rank_cannot_regress(self):
        errors = self.check(lambda f,u,v: self.record(f, "2026-11-22")
                            ["liturgical"].update(rank="Sunday", color="green"))
        self.assertTrue(any("expected Solemnity" in e for e in errors), errors)

    def test_wrong_festival_title_rejected(self):
        errors = self.check(lambda f,u,v: self.record(f, "2026-11-22")
                            ["liturgical"].update(title_en="33th Sunday in Ordinary Time"))
        self.assertTrue(any("title_en mismatch" in e for e in errors), errors)

    def test_missing_dated_liturgical_source_rejected(self):
        errors = self.check(lambda f,u,v: self.record(f, "2026-12-25")
                            ["sources"].pop(0))
        self.assertTrue(any("dated USCCB source missing" in e for e in errors), errors)

    def test_english_copy_pasted_as_vietnamese_rejected(self):
        def edit(f,u,v):
            obj = self.record(f, "2026-12-08")["primary"]
            obj["summary_vi"] = obj["summary_en"]
        errors = self.check(edit)
        self.assertTrue(any("English copied into primary.summary_vi" in e for e in errors), errors)

    def test_upstream_divergence_rejected(self):
        errors = self.check(lambda f,u,v: u["2026-08-15"]["primary"].update(
            body_en="Different version of the Assumption"))
        self.assertTrue(any("primary.body_en differs from upstream" in e for e in errors), errors)

    def test_november_vietnamese_overlay_divergence_rejected(self):
        errors = self.check(lambda f,u,v: v["primary"].update(
            summary_vi="Out-of-sync Vietnamese summary"))
        self.assertTrue(any("VI overlay" in e for e in errors), errors)

    def test_no_duplicate_dates(self):
        errors = self.check(lambda f,u,v: f["entries"].append(copy.deepcopy(f["entries"][-1])))
        self.assertTrue(any("Duplicate dates" in e for e in errors), errors)

    def test_starter_is_single_file_non_shipping_and_non_overwriting(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d) / "draft.json"
            new_entry("2027-01-06", output)
            obj = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(obj["id"], "anno-2027-01-06")
            self.assertEqual(obj["_editorial"]["status"], "draft_do_not_ship")
            self.assertEqual(len(obj["sources"]), 2)
            self.assertIn("alt_vi", obj["_editorial"]["assets"])
            with self.assertRaises(FileExistsError):
                new_entry("2027-01-06", output)


if __name__ == "__main__":
    unittest.main()

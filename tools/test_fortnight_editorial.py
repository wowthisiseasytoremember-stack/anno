#!/usr/bin/env python3
"""Stdlib-only regression coverage for all 14 July 3–16 2026 daily records."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fortnight_editorial import (AUTHORITY, CALENDAR_URL, FIXTURE, SOURCE,
                                 read, scaffold, validate)


class JulyFortnightIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = read(SOURCE)
        cls.fixture = read(FIXTURE)

    def entry(self, source, day):
        return next(e for e in source["entries"] if e["date"] == day)

    def errors(self, edit=None):
        source, fixture = copy.deepcopy(self.source), copy.deepcopy(self.fixture)
        if edit:
            edit(source, fixture)
        return validate(source, fixture)

    def test_every_item_is_checked_and_current_fixture_passes(self):
        self.assertEqual(self.errors(), [])

    def test_all_fourteen_dates_have_authority_contract(self):
        self.assertEqual(len(AUTHORITY), 14)
        self.assertEqual(list(AUTHORITY)[0], "2026-07-03")
        self.assertEqual(list(AUTHORITY)[-1], "2026-07-16")

    def test_thomas_is_feast_not_ordinary_feria(self):
        def corrupt(s,f):
            e = self.entry(s,"2026-07-03")
            e["liturgical"]["rank"] = "Feria"
        self.assertTrue(any("rank/color" in e for e in self.errors(corrupt)))

    def test_marian_days_is_not_july_national_feast(self):
        def corrupt(s,f):
            e = self.entry(s,"2026-07-09")
            e["liturgical"]["title_en"] = "Marian Days (Đại Hội Thánh Mẫu)"
        self.assertTrue(any("display title mismatch" in e for e in self.errors(corrupt)))

    def test_benedict_memorial_cannot_be_displaced(self):
        def corrupt(s,f):
            e=self.entry(s,"2026-07-11")
            e["liturgical"]["rank"] = "Feast"
        self.assertTrue(any("rank/color" in e for e in self.errors(corrupt)))

    def test_us_memorials_kateri_bonaventure_are_required(self):
        def corrupt(s,f):
            self.entry(s,"2026-07-14")["liturgical"]["rank"] = "Feria"
            self.entry(s,"2026-07-15")["liturgical"]["rank"] = "Feria"
        err=self.errors(corrupt)
        self.assertEqual(sum("rank/color" in x for x in err),2)

    def test_english_weekday_in_vietnamese_rejected(self):
        def corrupt(s,f):
            self.entry(s,"2026-07-04")["primary"]["body_vi"] += " Friday"
        self.assertTrue(any("untranslated English weekday" in x for x in self.errors(corrupt)))

    def test_english_fallback_cannot_masquerade_as_vietnamese(self):
        def corrupt(s,f):
            e=self.entry(s,"2026-07-04")["primary"]
            e["summary_vi"] = e["summary_en"]
        self.assertTrue(any("English copied into" in x for x in self.errors(corrupt)))

    def test_faked_artwork_clearance_rejected(self):
        def corrupt(s,f):
            e=self.entry(s,"2026-07-04")["artwork"]
            e["status"]="cleared"
            e["source_url"]="https://example.com/placeholder.jpg"
        self.assertTrue(any("unlicensed/placeholder artwork" in x for x in self.errors(corrupt)))

    def test_fake_place_provenance_rejected(self):
        def corrupt(s,f):
            self.entry(s,"2026-07-04")["place"] = {
                "name":"Universal Church","source_url":"https://example.com"
            }
        self.assertTrue(any("invented place" in x for x in self.errors(corrupt)))

    def test_official_calendar_source_cannot_disappear(self):
        def corrupt(s,f):
            e=self.entry(s,"2026-07-10")
            e["sources"]=[x for x in e["sources"] if x["url"]!=CALENDAR_URL]
        self.assertTrue(any("dated USCCB readings and 2026 national calendar" in x
                            for x in self.errors(corrupt)))

    def test_factual_gospel_reference_cannot_drift(self):
        def corrupt(s,f):
            self.entry(s,"2026-07-16")["primary"]["confidence_note_en"]="generic calendar"
        self.assertTrue(any("reading attribution lacks" in x for x in self.errors(corrupt)))

    def test_source_compiled_mismatch_rejected(self):
        def corrupt(s,f):
            self.entry(f,"2026-07-03")["primary"]["body_en"]="outdated generated copy"
        self.assertTrue(any("source content differs" in x for x in self.errors(corrupt)))

    def test_duplicate_daily_summary_rejected(self):
        def corrupt(s,f):
            self.entry(s,"2026-07-13")["primary"]["summary_en"]=self.entry(
                s,"2026-07-12")["primary"]["summary_en"]
        self.assertTrue(any("Duplicate EN daily summaries" in x for x in self.errors(corrupt)))

    def test_scaffold_single_file_draft_assets_audit_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/"draft.json"
            scaffold("2027-07-03",target)
            obj=json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(obj["id"],"anno-2027-07-03")
            self.assertEqual(obj["_editorial"]["status"],"draft_do_not_ship")
            self.assertIn("alt_vi",obj["_editorial"]["assets"])
            self.assertTrue(obj["_editorial"]["review_checklist"])
            self.assertEqual(len(obj["sources"]),2)
            with self.assertRaises(FileExistsError):
                scaffold("2027-07-03",target)


if __name__ == "__main__":
    unittest.main()

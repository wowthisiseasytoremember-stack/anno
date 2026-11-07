#!/usr/bin/env python3
"""Linux-only regression tests for the complete seven-plus-one station content contract."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
from socal_station import CONTENT, ROUTE, MARKERS, MOMENTS, SOURCE_NOTES, new_station, validate


class SoCalStationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = {
            "content": json.loads(CONTENT.read_text(encoding="utf-8")),
            "route": json.loads(ROUTE.read_text(encoding="utf-8")),
            "markers": json.loads(MARKERS.read_text(encoding="utf-8")),
            "moments": json.loads(MOMENTS.read_text(encoding="utf-8")),
        }
        cls.notes = SOURCE_NOTES.read_text(encoding="utf-8")

    def audit_fixture(self, *, change=None, source_notes=None):
        payload = copy.deepcopy(self.baseline)
        if change:
            change(payload)
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for name, obj in payload.items():
                (root / f"{name}.json").write_text(json.dumps(obj, ensure_ascii=False),
                                                    encoding="utf-8")
            (root / "sources.md").write_text(
                self.notes if source_notes is None else source_notes, encoding="utf-8"
            )
            return validate(
                root / "content.json", root / "route.json",
                markers_path=root / "markers.json",
                moments_path=root / "moments.json",
                notes_path=root / "sources.md"
            )

    def test_live_pack_is_complete_and_consistent(self):
        errors, core, optional = self.audit_fixture()
        self.assertEqual((core, optional), (7, 1))
        self.assertEqual(errors, [])

    def test_rejects_missing_vietnamese_step(self):
        def change(data):
            data["content"]["chapters"][0]["stations"][0]["look_vi"] = ""
        errors, _, _ = self.audit_fixture(change=change)
        self.assertTrue(any("look_vi" in e for e in errors), errors)

    def test_rejects_orphaned_official_citation(self):
        def change(data):
            data["content"]["chapters"][0]["stations"][0]["official_url"] = "https://other.example.com/unlisted"
        errors, _, _ = self.audit_fixture(change=change)
        self.assertTrue(any("absent from canonical source notes" in e for e in errors), errors)

    def test_rejects_route_content_divergence(self):
        def change(data):
            data["route"]["waypoints"][3]["historical_summary_en"] = "Different history in map"
        errors, _, _ = self.audit_fixture(change=change)
        self.assertTrue(any("route historical_summary_en differs" in e for e in errors), errors)

    def test_rejects_changed_marker_identity(self):
        def change(data):
            data["markers"]["markers"][0]["station_id"] = "wrong_id"
        errors, _, _ = self.audit_fixture(change=change)
        self.assertTrue(any("Marker station order" in e for e in errors), errors)

    def test_rejects_moment_level_divergence(self):
        def change(data):
            data["content"]["chapters"][0]["stations"][0]["moment_level"] = "highlight"
        errors, _, _ = self.audit_fixture(change=change)
        self.assertTrue(any("moment level differs" in e for e in errors), errors)

    def test_rejects_quick_variant_expansion(self):
        def change(data):
            data["content"]["variants"][0]["chapter_ids"].append("st_columban")
        errors, _, _ = self.audit_fixture(change=change)
        self.assertTrue(any("Quick/extended" in e for e in errors), errors)

    def test_rejects_fixed_clock_time_in_durable_copy(self):
        def change(data):
            data["content"]["chapters"][4]["stations"][0]["know_en"] = "Mass at 9:30 AM."
        errors, _, _ = self.audit_fixture(change=change)
        self.assertTrue(any("clock time in durable" in e for e in errors), errors)

    def test_rejects_accidental_mark_final_on_vi(self):
        def change(data):
            data["content"]["translation_status"] = "complete"
        errors, _, _ = self.audit_fixture(change=change)
        self.assertTrue(any("pending-human-review" in e for e in errors), errors)

    def test_starter_has_stubs_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "draft.json"
            args = SimpleNamespace(id="new_test_station", title_en="Test", role="reflection",
                                   level="reflection", output=str(path))
            new_station(args)
            obj = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(obj["station_id"], "new_test_station")
            self.assertEqual(obj["_editorial"]["status"], "draft_do_not_ship")
            self.assertTrue(all(f"{step}_en" in obj and f"{step}_vi" in obj
                                for step in ("arrive", "look", "know", "pray", "continue")))
            with self.assertRaises(FileExistsError):
                new_station(args)


if __name__ == "__main__":
    unittest.main()

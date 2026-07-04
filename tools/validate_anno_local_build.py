#!/usr/bin/env python3
"""Validate the source-only Anno local build scaffold."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "Anno/AnnoApp.swift",
    "Anno/RootView.swift",
    "Anno/Models/AnnoEntry.swift",
    "Anno/Services/FixtureStore.swift",
    "Anno/Localization/LanguageMode.swift",
    "Anno/Localization/LocalizedEntryText.swift",
    "Anno/Design/AnnoTheme.swift",
    "Anno/Today/TodayView.swift",
    "Anno/Today/ArtworkCandidateView.swift",
    "Anno/Today/ConfidenceBadge.swift",
    "Anno/Today/CalendarConversionGrid.swift",
    "Anno/Calendar/WeekCalendarView.swift",
    "Anno/Calendar/EntryListRow.swift",
    "Anno/Map/SacredSiteMapView.swift",
    "Anno/Map/SacredSiteListView.swift",
    "Anno/Saved/SavedView.swift",
    "Anno/Sources/SourceSheet.swift",
    "Anno/Sources/SourceRow.swift",
    "Anno/Paywall/ArchivePaywallView.swift",
    "Anno/Paywall/ProductCopy.swift",
    "Anno/Resources/anno_fortnight_2026-07-03_2026-07-16.json",
    "Anno/Resources/anno_week_2026-07-03_2026-07-09.json",
    "docs/blind-frontier/swift-module-packets.md",
    "docs/blind-frontier/content-asset-packets.md",
    "docs/mechanical-packets/july-17-30-date-fill-packets.md",
    "docs/mechanical-packets/artwork-clearance-packets.md",
    "docs/mechanical-packets/translation-review-packets.md",
    "docs/mechanical-packets/swift-qa-packets.md",
    "docs/mechanical-packets/generated-artwork-clearance-packet-list.md",
    "docs/mechanical-packets/generated-translation-review-packet-list.md",
    "docs/mechanical-packets/generated-swift-qa-packet-list.md",
    "docs/IOS_PREVIEW_CHECKLIST.md",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail(f"missing required scaffold files: {missing}")

    fixture = json.loads((ROOT / "Anno/Resources/anno_fortnight_2026-07-03_2026-07-16.json").read_text())
    week = json.loads((ROOT / "Anno/Resources/anno_week_2026-07-03_2026-07-09.json").read_text())
    entries = fixture.get("entries", [])
    ids = {entry.get("id") for entry in entries}

    if len(entries) != 14:
        fail(f"expected 14 bundled fortnight entries, found {len(entries)}")
    if len(week.get("entry_ids", [])) != 7:
        fail(f"expected 7 bundled week ids, found {len(week.get('entry_ids', []))}")
    if any(entry_id not in ids for entry_id in week.get("entry_ids", [])):
        fail("week resource references an id not present in the fortnight resource")

    swift_text = "\n".join((ROOT / path).read_text() for path in REQUIRED_FILES if path.endswith(".swift"))
    required_terms = ["LanguageMode", "ConfidenceLevel", "SourceSheet", "SacredSiteMapView", "ArchivePaywallView"]
    missing_terms = [term for term in required_terms if term not in swift_text]
    if missing_terms:
        fail(f"missing expected Swift symbols: {missing_terms}")

    print("OK: Anno source scaffold, bundled resources, blind packets, and mechanical packets are present.")


if __name__ == "__main__":
    main()

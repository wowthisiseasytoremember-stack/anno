#!/usr/bin/env python3
"""Generate an artwork/source clearance queue from the Anno mock fixture."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/mock/anno_fortnight_2026-07-03_2026-07-16.json"
OUTPUT = ROOT / "data/assets/artwork_clearance_queue_2026-07-03_2026-07-16.json"


STATUS_TO_ACTION = {
    "public_domain_candidate": "Verify public-domain status, download source image, capture attribution, and store license note.",
    "museum_candidate": "Check museum image policy, rights page, object ID, and permitted app/screenshot usage.",
    "provenance_candidate": "Find a rights-cleared image source or replace with a public-domain equivalent.",
    "art_history_candidate": "Verify image source reliability and reuse permission before bundling.",
    "reference_only_rights_unclear": "Do not bundle. Use only for editorial reference until rights are cleared or replacement is found.",
    "sidebar_candidate": "Keep out of primary Today art unless the sidebar is implemented.",
    "needs_asset_research": "Assign art researcher to find a better rights-clear candidate.",
    "representation_review_required": "Require cultural/editorial review before image selection or marketing use.",
}


def priority_for(status: str, mock_priority: str) -> str:
    if status in {"reference_only_rights_unclear", "representation_review_required"}:
        return "P0-risk"
    if mock_priority == "week_real_data":
        return "P0-week"
    if status in {"needs_asset_research", "provenance_candidate"}:
        return "P1-research"
    return "P2-clearance"


def main() -> None:
    fixture = json.loads(SOURCE.read_text())
    items = []
    status_counts: Counter[str] = Counter()

    for entry in fixture["entries"]:
        artwork = entry["artwork"]
        status = artwork["status"]
        status_counts[status] += 1
        items.append(
            {
                "entry_id": entry["id"],
                "date": entry["date"],
                "mock_priority": entry["mock_priority"],
                "entry_title_en": entry["primary"]["title_en"],
                "entry_title_vi": entry["primary"]["title_vi"],
                "artwork_title": artwork["title"],
                "maker": artwork["maker"],
                "date_label": artwork["date_label"],
                "source_url": artwork["source_url"],
                "current_status": status,
                "clearance_priority": priority_for(status, entry["mock_priority"]),
                "next_action": STATUS_TO_ACTION.get(status, "Review rights and provenance before bundling."),
                "ship_decision": "placeholder_only" if status in {"reference_only_rights_unclear", "needs_asset_research", "representation_review_required"} else "candidate_pending_clearance",
                "notes": entry["primary"]["confidence_note_en"],
            }
        )

    output = {
        "schema_version": "anno.artwork_clearance.v1",
        "generated_from": str(SOURCE.relative_to(ROOT)),
        "date_window": fixture["source_window"],
        "summary": {
            "total_items": len(items),
            "status_counts": dict(sorted(status_counts.items())),
            "p0_items": sum(1 for item in items if item["clearance_priority"].startswith("P0")),
            "placeholder_only_items": sum(1 for item in items if item["ship_decision"] == "placeholder_only"),
        },
        "policy": {
            "do_not_bundle_uncleared_modern_images": True,
            "preserve_attribution": True,
            "store_license_evidence_before_app_use": True,
        },
        "items": items,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

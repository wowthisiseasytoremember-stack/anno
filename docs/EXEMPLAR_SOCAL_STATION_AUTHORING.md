# SoCal station authoring — reusable template and acceptance gate

**Claimed area:** Orange County / Our Lady of La Vang pilgrimage. This is a **native iOS SwiftUI** experience, not a web article or social post. The live master is `Anno/Resources/socal_la_vang_exemplar_content_v1.json`. This template does not modify the master automatically.

## One-file starter

Create a new station JSON **draft** with one command:

```bash
python3 tools/socal_station.py new \
  --id proposed_station_id \
  --title-en "Proposed Station" \
  --role reflection \
  --level reflection \
  --output /tmp/proposed_station_id.json
```

The command creates **one file** containing the native `SoCalExemplarContent.Station` fields, paired EN/VI stubs, `official_url`, a claim/source ledger, image/caption/alt slots, and the standards checklist. It refuses to overwrite. Treat all `TODO` text, `_editorial.status=draft_do_not_ship`, and the example URL as hard stops.

Complete all five actions — ARRIVE, LOOK, KNOW, PRAY, CONTINUE — **before** copying reviewed fields into the appropriate existing chapter. Do not add to the seven core IDs or existing GPS route without explicitly expanding the core product and updating route, moments, progress and QR identities. An optional context station can use `station_id`; core stations must match route `waypoint_id`.

Run a conformance audit after any edit:

```bash
python3 tools/socal_station.py audit
python3 tools/validate_route_coordinates.py
```

## Reusable presentation component

`SoCalRitualStepRow` in `Anno/Map/SoCalExemplarViews.swift` accepts the bilingual step label, icon, text, tint and prayer emphasis. The existing five-step ritual is composed from five instances. It is a native SwiftUI view, not a scrollytelling/pinned-card web treatment. The station's `official_url` produces a native external-source link.

## Editorial acceptance checklist

- Clear opening and unique chapter contribution, not interchangeable “another parish” copy.
- Historical facts, dates, places and counts map to the official-source index in `docs/EXEMPLAR_SOCAL_SOURCE_NOTES.md`; tradition language is explicit.
- One observable LOOK, achievable without presuming the building is open or that the pilgrim can stand/see at a particular distance; no speculative access claims.
- A dignified prayer/reflection; no scoring, XP, special spiritual entitlement, or dependency on GPS.
- Accurate identifiers and geography; changes to existing IDs require migration.
- EN/VI authored independently; human Vietnamese Catholic edit signed off before final.
- Correct semantics/VoiceOver order, large text, contrast and reduced motion on a physical iPhone.
- If images are actually introduced: licensed rights, caption/attribution, meaningful EN/VI alt text, efficient asset delivery. Avoid decorative imagery merely to fill slots.
- Official links inspected for currency, schedules/parking explicitly rechecked before field release.
- Route time, distance and physical access tested; placeholders must not be presented as actual measurements.

**Review queue:** `docs/EXEMPLAR_SOCAL_EDITORIAL_AUDIT_2026-11-06.md`, Issue #28 for source/field/Vietnamese review, Issue #33 for iOS/device build. No GitHub merge equals App Store release.

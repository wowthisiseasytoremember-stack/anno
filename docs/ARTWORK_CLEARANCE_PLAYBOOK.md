# Artwork Clearance Playbook

Updated: 2026-07-03

## Purpose

Anno's art-first interface only works if the art is real, sourced, and legally usable. The fixture already records artwork candidates, but candidates are not app assets. Use the generated queue at `data/assets/artwork_clearance_queue_2026-07-03_2026-07-16.json` to turn candidates into production decisions.

## Clearance States

| State | Meaning | App Use |
|---|---|---|
| `public_domain_candidate` | Likely usable after source and attribution check | Can become bundled art after evidence is saved |
| `museum_candidate` | Museum record exists, but image policy must be checked | Use after rights page is reviewed |
| `provenance_candidate` | Good art-history candidate, unclear image source | Research before use |
| `art_history_candidate` | Useful scholarly candidate, source/rights need review | Research before use |
| `reference_only_rights_unclear` | Modern/editorial image with unclear rights | Do not bundle |
| `representation_review_required` | Image choice has cultural/editorial risk | Require review before use |
| `needs_asset_research` | Current candidate is weak | Replace |
| `sidebar_candidate` | Useful but not primary | Do not block Today screen |

## Evidence Required Before Bundling

For each bundled image, save:

- Source URL.
- Object page URL if different from image URL.
- Maker, title, date, institution/collection.
- Rights statement or license.
- Download timestamp.
- Local filename.
- Required credit line.
- Any modification restrictions.

## Week-One Priorities

Clear first:

1. July 3: Caravaggio, Saint Thomas.
2. July 4: Zurbaran, Saint Elizabeth of Portugal.
3. July 8: Jacques Callot, Aquila and Priscilla.

Do not bundle without replacement:

- July 6 Maria Goretti modern Vatican News/reference image.
- July 9 Chinese Martyrs modern Vatican News/reference image.
- July 14 Kateri image until representation review is complete.

## Asset Handoff Prompt

```text
You are clearing artwork for Anno, a premium Catholic daily-history iOS app.

Use the artwork clearance queue JSON as your source of truth. For each P0 item, find a legally usable image asset or mark it placeholder-only.

Return one row per item:
- entry_id
- chosen_image_url
- object_page_url
- title
- maker
- date
- institution
- license_or_rights_statement
- required_credit_line
- can_bundle_in_app: yes/no
- can_use_in_app_store_screenshots: yes/no
- unresolved_risk

Do not use modern editorial images unless the rights statement explicitly permits app and marketing usage. Prefer museum/public-domain sources with clear object pages.
```

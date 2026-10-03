# Anno Icon System

Status: canonical for v1 UI semantics.

## Brand mark

The current app-icon direction remains the illuminated capital **A**:

- warm near-black `#13110E` field
- gold leaf `#C9A84C`
- restrained gilt `#D9C06E`
- manuscript / Romanesque architectural character
- no collage of religious symbols
- no wordmark inside the app icon

Canonical source concept: `visuals/app-icon-anno.svg`.

The app icon should feel like an illuminated object; in-app controls should **not** imitate that amount of detail.

## In-app rule

Use SF Symbols first. All product meaning is routed through `Anno/Design/AnnoSymbols.swift`.

Do not hard-code a new symbol name into a view unless:
1. there is no existing semantic token, and
2. the new meaning is durable enough to deserve one.

This keeps future custom-symbol work reversible: a semantic token can switch from an SF Symbol to a custom symbol without rewriting every screen.

## Core meanings

| Meaning | Semantic token | Current system symbol |
|---|---|---|
| Today | `AnnoSymbol.today` | sun |
| Calendar | `AnnoSymbol.calendar` | calendar |
| Pilgrimage | `AnnoSymbol.pilgrimage` | walking figure |
| Route | `AnnoSymbol.route` | map |
| Waypoint | `AnnoSymbol.waypoint` | map pin |
| Prayer | `AnnoSymbol.prayer` | praying/sparkle hands |
| Sources | `AnnoSymbol.sources` | books |
| Confidence | `AnnoSymbol.confidence(...)` | seal / scroll / question / info |
| Sacred / Catholic identity | `AnnoSymbol.sacred` | cross |
| Language | `AnnoSymbol.language` | character book |
| Artwork expansion | `AnnoSymbol.artworkExpand` | expand arrows |

## Source categories

Source icons are semantic, not decorative:

- liturgical → closed book
- historical → clock
- church biography → classical building
- academic → document + magnifier
- unknown → generic text/book

Color remains secondary to the glyph so meaning is not color-only.

## Pilgrimage categories

- Marian → heart
- Apostolic → cross
- Martyrs → flame
- Eucharist / Passion → sun
- Monastic / desert → mountain

These are navigation shorthand, not theological logos.

## Custom-icon threshold

A custom symbol should exist only if the system symbol fails one of these tests:

- recognizable at 16–20 pt
- legible in monochrome
- understandable without a label after repeated use
- compatible with Dynamic Type layouts
- does not introduce a second illustration style

Likely future custom candidates:
- the illuminated Anno **A**
- a compact pilgrimage-station marker
- perhaps one Anno-specific liturgical-day glyph

Everything else should remain SF Symbols unless real screenshots prove otherwise.

## Motion

Symbol animation is state-driven and restrained:

- selection → short bounce/replace
- ongoing loading → subtle pulse
- reveal → appear/opacity
- never repeat decorative motion indefinitely unless it communicates activity
- honor Reduce Motion

Motion tokens live in `Anno/Design/AnnoMotion.swift`.

# Brand & Visual Direction Addendum
Updated: 2026-07-03

## Status

Mandatory visual-direction addendum for **Anno**.

This supersedes the earlier warm-light-first visual direction. Dark mode is now the default brand experience.

## 1. Name Lock

Working brand: **Anno**.

Why this wins:

- Short, premium, and app-icon friendly.
- Calendar-native: "Anno Domini" gives the name immediate date/year meaning.
- Latin and scholarly without becoming obscure.
- More commercially accessible than Sanctorale, Ordo, Kalendarium, or Chronicon Sacrum.
- Expandable beyond Catholic v1 into wider sacred-history context.

App Store metadata:

| Field | Copy |
|---|---|
| App Name | `Anno` |
| Subtitle | `This Day in Catholic History` |
| Keywords | `saint,feast,liturgical,calendar,catholic,history,pilgrimage,ordo,daily,martyrology` |

Bundle ID target:

```text
com.yourco.anno
```

Availability checks still required:

- App Store name.
- Bundle ID.
- Trademark conflicts in religion, calendar, education, wellness, and games.

Fallbacks only if the bare word cannot be used:

- `Anno: Catholic Calendar`
- `Anno Daily`
- `Anno — Sacred History`
- `Anno: Saints & Sacred Time`

## 2. Brand Metaphor

Because Anno means "year," time is the central metaphor.

Use:

- Illuminated Timeline.
- Walking through the centuries.
- Every date holds a memory.
- This day, for two thousand years.

Avoid:

- Generic archive-only framing.
- Reference-book dryness.
- Wellness-app routine language.

Core emotional promise:

> Every day since the Incarnation has been numbered. This is what happened on this date.

## 3. Dark Mode First

Dark mode is the default and brand-defining experience.

Rationale:

- Gold accents feel physically luminous on OLED screens.
- Bedside/morning use benefits from a quiet, dim interface.
- Dark sacred-timeline aesthetic differentiates from bright Catholic apps.
- It pairs naturally with illuminated manuscript, chapel, map, art, and pilgrimage references.

Light mode exists for accessibility and user preference, but the brand lives in the dark.

## 4. Color Palette

Primary dark palette:

| Role | Name | Hex | Usage |
|---|---|---|---|
| Background | Narthex | `#13110E` | Primary canvas; warm near-black. |
| Surface | Choir | `#1F1B16` | Cards, elevated containers, sheets. |
| Primary Accent | Gold Leaf | `#C9A84C` | Hero icons, active states, feast markers. |
| Gold Light | Gilt | `#D9C06E` | Highlights and selected states. |
| Secondary | Lapis | `#2B4A7C` | Marian feasts, links, selected map elements. |
| Tertiary | Crimson | `#8C2F3B` | Martyrs, alerts, liturgical red. |
| Primary Text | Vellum | `#EDE7DA` | Headlines and body text. |
| Secondary Text | Incense | `#9B9085` | Captions, metadata, dates. |
| Dividers | Ash | `#2E2A24` | Separators and card edges. |
| Liturgical Green | Verdigris | `#3B6B52` | Ordinary Time. |
| Liturgical Violet | Advent | `#5C3D6E` | Advent and Lent. |
| Liturgical White | Easter | `#F5F0E8` | Solemnities and light mode background. |

Light mode secondary palette:

| Role | Hex |
|---|---|
| Background | `#F5F0E8` |
| Surface | `#FFFFFF` |
| Gold | `#8B7030` |
| Primary Text | `#1F1B16` |

Non-negotiable:

> Never use more than one accent color on the same screen.

Most screens should use no accent color beyond Gold Leaf. Lapis, Crimson, Verdigris, and Advent are contextual states, not decoration.

## 5. Typography

Use Apple's native stack for v1.

| Purpose | Font | Notes |
|---|---|---|
| Display/headlines | New York Display | System serif, bookish, trusted. |
| Reading/body | New York Text | Use generous line height. |
| UI/nav/metadata | SF Pro | Native controls, metadata, navigation. |
| Pills/tags | SF Pro Rounded | Confidence badges and small controls. |
| Liturgical Latin | New York Italic | Scholarly and traditional. |
| Numerical dates | SF Pro Tabular | Calendar alignment. |

Do not ship Cormorant Garamond in v1. New York/SF reduces accessibility and Dynamic Type risk.

## 6. App Icon

Recommended concept:

> A premium iOS app icon, rounded rectangle. A single golden illuminated capital letter A centered on deep warm near-black `#13110E`. The letter is rendered in rich warm gold `#C9A84C` in the style of a Carolingian manuscript initial, elegant and restrained, with subtle vine-like flourishes extending from the crossbar and apex. Two or three fine golden tendrils maximum. Gold has slight tonal variation suggesting real gold leaf dimensionality, but remains flat and graphic. No other text, no crosses, no halos. Background is smooth and textureless. The overall impression is a single folio detail from a medieval manuscript. Aspect ratio 1:1, 1024x1024px.

Why A works:

- The crossbar of a Romanesque capital A reads like a small architectural arch.
- At small size it is a confident gold triangle.
- At large size the illumination rewards inspection.

## 7. App Store Copy

Subtitle:

```text
This Day in Catholic History
```

Screenshot captions:

| # | Caption | Supporting |
|---|---|---|
| 1 | This day, for two thousand years. | Every morning: saints, feasts, martyrdoms, art, and pilgrimage sites for this date across centuries. |
| 2 | Every saint. Every feast. Mapped. | Sacred sites, real routes, real history. |
| 3 | Pray where the Church has prayed. | One quiet, historically grounded prayer prompt tied to the day's events. |
| 4 | Sacred art, not stock photos. | Paintings, mosaics, and manuscripts with scholarly captions and provenance. |
| 5 | Two millennia. One calendar. | Browse any date and see the density of Catholic history. |
| 6 | Built for depth. Designed for devotion. | Source transparency, liturgical rhythm, premium native design. |

Tone rule:

> No generic verses. No inspirational quotes. Only actual history.

## 8. Design Discipline

Non-negotiable:

- One accent per screen.
- No pure black `#000000`.
- No pure white in dark-mode surfaces.
- Ornament is earned.
- Dark mode is default.
- The art is the ornament.
- Do not decorate around sacred art; let it breathe.
- Use fine-line dividers only for real section breaks.
- Use gilded initials only for major feasts or rare ceremonial moments.


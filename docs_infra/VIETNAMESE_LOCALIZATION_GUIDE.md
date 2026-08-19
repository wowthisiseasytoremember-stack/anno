# Vietnamese Localization Guide

Updated: 2026-07-03

## Product Stance

Vietnamese support should exist from the first SwiftUI data model, not as a later string pass. Treat `en` and `vi` as sibling content fields for historical copy, prayer prompts, confidence labels, and liturgical titles.

## Typography

- Use system fonts first: New York for reading surfaces, SF Pro for UI and metadata.
- Do not force custom serif fonts for Vietnamese diacritics in v1.
- Expect Vietnamese to run 30-50% longer than English.
- Avoid fixed-height cards for translated text.
- In SwiftUI, prefer `Text(...).fixedSize(horizontal: false, vertical: true)` for body copy and source notes.

## Date And Calendar Format

- Preferred app date: `16 tháng 7 • Thứ Năm`.
- Calendar week starts Monday.
- Weekday headers: `T2 T3 T4 T5 T6 T7 CN`.
- Keep liturgical season names translated in UI labels, but preserve proper names carefully.

## Tone

Vietnamese Catholic copy should be reverent, plain, and specific. Avoid generic inspirational language. The target voice is closer to a parish bulletin written by a careful editor than a wellness app.

## Translation Rules

- Translate "Saint" as `Thánh`.
- Translate "Blessed" as `Chân phước`.
- Translate "Doctor of the Church" as `tiến sĩ Hội Thánh`.
- Translate "Ordinary Time" as `Mùa Thường Niên`.
- Translate "Optional Memorial" as `Lễ nhớ tùy chọn`.
- Use `Đức Mẹ` for Marian titles where idiomatic.
- Keep place names in their common local/international form unless a Vietnamese Catholic form is widely established.

## Build Notes

Use `localization/vi/Localizable.strings` as the flat v1 bridge and `data/localization/vi_terms.json` as the design/content glossary. When the native project exists, migrate the flat strings into Xcode String Catalogs and keep the JSON glossary as editorial source material.

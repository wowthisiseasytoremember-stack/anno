# Anno Apple Surfaces

This directory contains source that is intentionally **not yet wired into the shipping Xcode target** while Mac access is unavailable.

## Ready now

- `Widgets/AnnoDailyWidget.swift`: source-complete iPhone Home Screen + Lock Screen widget prototype.
- Accessory widget layouts are deliberately shared with the future Watch complication presentation.
- Uses the same `AnnoGlance` payload as the app-side Apple integrations.

## Activation when Xcode validation is available

1. Add an iOS Widget Extension target.
2. Include `anno_unified_2026.json` in the extension bundle.
3. Move/share `AnnoGlance.swift` and fixture model files through a small shared target or shared source group.
4. Add the widget extension to the Anno app target.
5. Validate systemSmall, systemMedium, accessoryCircular, accessoryRectangular, and accessoryInline.
6. Reuse the accessory layouts in a watchOS Widget Extension when the companion Watch target exists.

Do not add a Watch app merely for marketing surface area. The first Watch version should be glance-first: today's entry, liturgical color/rank, and tap-through.

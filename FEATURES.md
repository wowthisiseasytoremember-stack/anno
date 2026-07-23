# Interfaith Devotional — Feature Upgrades
Ingested: 2026-07-03, from product discussion
Priority: P0 (must) → P1 (strong) → P2 (polish)

## P0 — Must-haves

### 1. Sundown anchor from user location
- Get GPS → SunCalc sunset → swap Garden Grove hardcode
- Fallback to timezone approximation
- Banner when near boundary

### 2. Expandable calendars
- Collapse extras by default, animate open
- CSS transition on max-height, toggle button

### 3. Skeleton loaders
- Shimmer animation on card load
- respects prefers-reduced-motion

### 4. Colorblind-safe pins
- Icon overlays (+/✡/☪/∞) on tradition dots, not just color
- :focus-visible outlines on all interactive

### 5. Reduced motion guard
- Global prefers-reduced-motion: kill animations, transitions, scroll-behavior

## P1 — Strong upgrades

### 6. Better map — 7-day window
- Default to week view, cluster pins, bottom sheet
- "Directions" CTA opens Apple/Google Maps

### 7. Audio narration
- Play button per card, Web Speech API free tier
- Speed control, resume, premium ElevenLabs

### 8. Shareable cards
- html2canvas → native share API
- download fallback

### 9. Confidence badges
- confirmed/traditional/disputed pills with tooltip

### 10. Swipe between days
- Touchstart→touchend delta, haptic feedback

## P2 — Polish

### 11. Subtle grain texture
- radial-gradient noise on cards

### 12. Gold shimmer on hero badge
- animated gradient sweep

### 13. Glass tab bar
- backdrop-filter blur, active indicator dot

### 14. Art lightbox
- Full-screen, zoom, caption overlay

### 15. Save with micro-feedback
- Scale animation, color shift, toast

## Layout fixes
- 8pt grid, 68ch line length, DM Serif only titles
- 44x44px tap targets, inner glow on cards
- loading="lazy", --radius/--radius-lg consistency

## Top 5 (80% gain)
1. Expandable calendars (P0)
2. Skeleton loaders (P0)
3. Colorblind-safe pins (P0)
4. This week's map (P1)
5. Audio narration (P1)

## Implementation note
Base mockup needs building first — current project is spec-only (PRD.md). Features to be applied after base.

# Anno — Apple-Native Sacred Polish Roadmap

**Status:** Active  
**Product target:** narrow Catholic-first Anno v1  
**Execution mode:** source-first/cloud-first while Mac access is limited  
**Quality bar:** slop + 20% — shippable, coherent, delightful, not over-engineered

## North star

Anno should feel like opening a small illuminated devotional object every day.

The visual target is **quiet baseline + earned spectacle**.

Ordinary days should feel contemplative, tactile, and still. Important days should visibly become more ceremonial. Catholicism has a real tradition of pageantry, procession, gold, incense, relics, mosaics, bells, vestments, basilicas, and Baroque theatricality. Anno can use that tradition without turning every tap into a theme-park effect.

### Sacred intensity model

Anno uses three expressive levels:

1. **Feria / Ordinary** — quiet, sparse, low-motion.
2. **Feast / Memorial** — richer color, stronger iconography, more visible transitions.
3. **Solemnity / Major moment** — earned spectacle: aureoles, gold bloom, procession-like reveals, more dramatic art treatment.

The current 2026 fixture is naturally compatible with this:
- 110 Feria
- 24 Sundays
- 44 Memorial / Optional Memorial / Feast days
- 4 Solemnities

That means spectacle remains rare enough to feel special.

---

# 1. Visual grammar

## 1.1 Surface hierarchy

Canonical semantic surfaces:

- **Narthex** — deepest background / app shell
- **Choir** — ordinary card surface
- **Raised** — primary interactive or artwork surface
- **Devotional** — prayer / pilgrimage / liturgical emphasis
- **Research** — sources / confidence / provenance
- **Solemn** — major-feast / ceremonial moment

Rules:

- gold = focus, sacred emphasis, current selection
- vellum = primary reading text
- incense = secondary text
- liturgical colors = contextual atmosphere and metadata
- shadows remain warm and intentional
- decorative glow is reserved for liturgical importance or sacred art

## 1.2 Shape language

- compact controls: 10 pt continuous radius
- normal cards: 16 pt continuous radius
- hero / artwork surfaces: 22 pt continuous radius
- metadata: capsules/pills
- minimum tap target: 44 pt

## 1.3 Typography

- semantic Dynamic Type throughout
- serif for devotional/editorial content
- system sans allowed for compact metadata/control text
- EN/VI both survive accessibility sizes
- major feast titles may get more editorial spacing and ornament, but not tiny decorative text

---

# 2. Sacred motion language

## 2.1 Motion vocabulary

Motion should communicate meaning:

- **reveal** — content enters like a page or folio opening
- **procession** — sequential appearance of important content
- **selection** — short tactile/system response
- **consecration / emphasis** — one-time gold bloom or aureole on major sacred state
- **pilgrimage** — directional movement, route progression, station selection
- **art immersion** — slower transition into artwork viewing
- **research folio** — sources/provenance open with measured, editorial motion

## 2.2 Spectacle rules

Allowed on solemnities / major moments:

- radial gold bloom
- subtle aureole / halo geometry
- gilded divider draw-on
- staged content procession
- richer liturgical-color atmosphere
- SF Symbol draw/bounce/replace effects
- slightly stronger haptic confirmation
- artwork hero expansion

Avoid:

- constant looping ornament
- confetti
- cartoon bounce everywhere
- audio surprises
- spinning crosses
- excessive particle systems
- anything that competes with reading or prayer

## 2.3 Accessibility

Every motion effect:
- honors Reduce Motion
- never conveys required information only through animation
- remains legible at large Dynamic Type
- never blocks interaction while playing

---

# 3. Calendar visual cleanup

## Goal

The calendar should feel less like a generic date picker and more like a compact liturgical calendar.

## Work

- semantic month navigation controls
- liturgical color marks on day cells
- Sundays get stronger visual hierarchy
- Feasts receive a small aureole/ring
- Solemnities receive a rarer gilded halo treatment
- selected day transitions use sacred intensity rather than generic ease-in/out
- conversion dates use shared metadata pills
- empty days have an intentional quiet state
- detail panel uses canonical surfaces
- wheel/grid switch uses semantic icons + sensory feedback
- EN/VI layout audit

---

# 4. Today screen

## Goal

Today is the devotional heart of Anno.

## Work

- staged page/procession reveal
- liturgical atmosphere varies by sacred intensity
- artwork card becomes the visual altar/centerpiece
- prayer surface becomes visually distinct from research/source surface
- sacred place and pilgrimage cards use pilgrimage semantics
- no fake actions
- major solemnities can trigger a one-time aureole/gold-bloom treatment
- confidence/source information remains visually quieter than devotional content

---

# 5. Sacred Art viewer

## Goal

Feel like entering a viewing chapel or gallery, not opening a generic full-screen image.

## Work

- slow immersive transition
- dark narthex background
- art remains the brightest object
- commentary behaves like opening a folio
- provenance remains quieter than theological text
- error/loading states are intentional
- optional major-feast aureole/ambient treatment around art
- no looping motion after the artwork is loaded

---

# 6. Pilgrimage / Map

## Goal

Make route progression feel like pilgrimage, not GPS.

## Work

- route selection uses procession/waypoint language
- current station visibly receives focus
- station-to-station transitions feel directional
- connected-to-today routes get a liturgical cue
- empty filter state is explicit
- selected waypoint may get a restrained halo/ripple once
- Apple Maps remains the handoff for actual navigation
- avoid pretending Anno is a turn-by-turn mapping product

---

# 7. Icon system

## Brand

Keep the illuminated gold **A** as the primary mark.

Canonical concept:
- near-black field
- gold-leaf illuminated capital A
- Romanesque / manuscript character
- no collage of religious symbols
- strong enough to survive small sizes

## In-app

SF Symbols first through `AnnoSymbols.swift`.

Custom symbols only when they add distinct Anno meaning:
- illuminated A
- pilgrimage station
- possible liturgical-day glyph
- possible aureole/solemnity ornament

## Future variants

- standard app icon
- dark/tinted treatment
- monochrome/system-friendly mark
- widget/Watch mark
- App Store screenshot lockup

---

# 8. Apple ecosystem

## Active now

### Spotlight
- index daily entries
- index flagship pilgrimage routes
- route Spotlight taps back into Today / Map

## Staged

### WidgetKit
- small daily widget
- medium devotional widget
- Lock Screen accessory circular
- Lock Screen accessory rectangular
- inline widget

### Apple Watch
Glance-first only:
- today’s feast/title
- liturgical color/rank
- complication
- tap-through to companion content

Do not build a miniature full app on the Watch.

### App Intents / Siri / Shortcuts
Small useful set:
- “Show today in Anno”
- “Show today’s feast”
- “Open pilgrimage routes”
- “Open [route]”
- possibly “Read today’s prayer prompt” if the content model is reliable enough

### Spotlight / Siri language
Prefer plain user vocabulary over internal theological schema names.

---

# 9. Boring states

Every major screen needs designed states for:

- loading
- offline/image failure
- no content
- no sources
- no matching routes
- malformed bundled content
- missing artwork
- long Vietnamese text
- very large Dynamic Type
- Reduce Motion
- first run
- returning run

These should feel like Anno, not debug fallbacks.

---

# 10. Widgets / Watch activation plan

While Mac access is unavailable:
- keep source complete
- keep extension code outside active target
- share a small stable `AnnoGlance` model
- avoid signing/embedding speculation

When Xcode is available:
1. create Widget Extension target
2. share canonical data model/resources
3. validate Home Screen + Lock Screen families
4. validate timeline refresh behavior
5. create Watch widget/complication only if the glance experience is useful
6. test tinted/monochrome rendering

---

# 11. Cloud QA without burning macOS minutes

Default:
- source review
- Linux/data validation
- static consistency checks

Manual-only:
- macOS native build
- simulator screenshots
- visual smoke matrix

When deliberately invoked, capture:
- Welcome
- Today
- Calendar
- Map
- EN
- VI
- large Dynamic Type
- Reduce Motion
- at least one solemnity and one ordinary day

---

# 12. Physical-device pass later

When a Mac/iPhone workflow is available, verify:

- real haptics
- scroll feel
- gesture conflicts
- art zoom
- image/network behavior
- VoiceOver
- Dynamic Type extremes
- Reduce Motion
- widget rendering
- lock-screen rendering
- Watch complication if activated
- battery/performance sanity

---

# 13. Definition of polished v1

Anno v1 is visually ready when:

- no screen looks like a different app
- ordinary days feel calm
- major days visibly earn more ceremony
- motion has semantic purpose
- EN/VI both look intentional
- all major failure/empty states are designed
- no fake controls are reachable
- Apple system surfaces use the same core visual language
- the app still reads clearly with Reduce Motion and large text
- sacred spectacle supports the content instead of obscuring it


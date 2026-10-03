# Anno — Apple Pilgrimage Magic Roadmap

**Status:** active  
**Primary exemplar:** Our Lady of La Vang — Orange County Pilgrimage  
**Platform philosophy:** Anno should feel unmistakably built for Apple hardware, not merely rendered on it.

## Product rule

Every platform feature must improve at least one of:

**ARRIVE → SEE → PRAY → REMEMBER → SHARE**

If an API is impressive but does not deepen one of those moments, defer it.

The target is not minimalism. The target is **sacred spectacle with native Apple fluency**.

---

# 1. iPhone core — ship first

## 1.1 Core Haptics

**Status: implemented foundation**

Use tactile language as part of sacred hierarchy:

- ordinary station: one soft transient
- pilgrimage highlight: two-stage arrival
- major pilgrimage moment: three-stage ceremonial arrival
- pilgrimage completion: richer four-note tactile peal

Rules:
- never vibrate continuously for decoration
- no haptic spam while scrolling
- Reduce Motion does not imply disabling useful haptics
- always degrade gracefully on unsupported hardware

Primary files:
- `Anno/Utilities/Haptics.swift`
- `Anno/Map/SacredSiteMapView.swift`

## 1.2 MapKit pilgrimage state

Use native MapKit as the spatial spine:

- featured Orange County route
- route polyline
- sacred waypoint pins
- visited-state seals
- chapter-aware grouping
- Apple Maps handoff for actual navigation
- map camera transitions tied to station selection
- no custom turn-by-turn engine

Future delight:
- camera fly-to between chapters
- visited segments change from incense/ash to gilt
- route completion resolves the full path in gold

## 1.3 Live Activities + Dynamic Island

**Use only while a pilgrimage is actively underway.**

Dynamic Island should answer:

- where am I in the pilgrimage?
- what is next?
- how many core stations have I visited?
- is there an active prayer/reflection moment?

Compact examples:
- cross / Marian glyph
- `3 / 7`
- next: St. Columban

Expanded:
- current chapter
- next station
- progress line
- one App Intent action such as **Open Next Station**

Lock Screen Live Activity:
- pilgrimage title
- current station
- next station
- progress
- optional "Open in Maps"

Do not turn a pilgrimage into a stopwatch.

## 1.4 Location awareness

Use location to enhance presence, never gate prayer.

Desired behavior:
- user opts into pilgrimage location awareness
- coarse approach: "You're near the La Vang campus"
- station arrival: suggest opening the relevant station
- dwell awareness: if stationary near a station for a few minutes, offer the prayer/reflection quietly
- departing: offer next station rather than nagging

Use modern Core Location APIs and capability checks.

Privacy:
- foreground / when-in-use first
- background monitoring only if the user deliberately enables an active pilgrimage
- no location history product
- no remote storage requirement for v1
- manual **I'm Here** remains available

## 1.5 Time awareness

Anno should know *when* sacred activity is happening.

Examples:
- dawn: softer candle / blue-gold treatment
- evening: deeper narthex, candlelight emphasis
- feast/solemnity: rank-aware spectacle
- Friday / Lent / Triduum: penitential visual register where liturgically appropriate
- anniversary of a completed pilgrimage: optional remembrance card

Never claim liturgical significance from clock time alone.

## 1.6 Core Motion / sensors

Useful signals:
- stationary vs moving
- walking activity
- heading/orientation for AR/map affordances
- optional step/distance summary for an active walking segment
- barometer only where elevation meaningfully helps a future route

Do not turn Anno into a fitness tracker.

Good use:
"You've slowed down at the Martyrs Wall. Take a moment."

Bad use:
"Only 432 steps until holiness."

Motion access is optional and must explain why it helps.

---

# 2. Camera + Vision

## 2.1 Sacred-camera mode

A camera surface can become an interpretive layer for physical pilgrimage.

Potential modes:

### Read
Use Vision text recognition for:
- martyr names
- plaques
- church inscriptions
- bilingual text
- historical markers

Then offer:
- station context
- pronunciation
- translation
- source-backed explanation

### Recognize
Use Vision / image matching where reliable to identify:
- shrine
- martyr wall
- known artwork
- route-specific visual markers

Never pretend confidence is higher than it is.

### Scan
Support:
- QR markers
- barcodes if useful
- NFC handoff
- printed Anno markers for field-test prototypes

### Capture
Create a pilgrimage memory:
- photo
- station label
- date
- route
- prayer/invocation
- optional generated keepsake

Privacy:
- on-device Vision first
- explicit user capture
- no face recognition product
- no background camera behavior

---

# 3. ARKit

AR should deepen physical encounter, not replace the site.

## 3.1 Christ Cathedral exemplar concepts

### Martyrs Wall
Point camera at the wall:
- names receive restrained highlights
- tap a recognized name for sourced historical context
- avoid game mechanics

### La Vang Shrine
Possible overlay:
- historical timeline around the physical shrine
- Quảng Trị ↔ Garden Grove connection
- restrained Marian aureole / canopy interpretation
- "look here" annotations for design symbolism

### Route threshold
At arrival:
- an illuminated Anno A or route sigil appears spatially
- one-time ceremonial reveal
- then gets out of the way

## 3.2 Anchor strategy

Preferred order:
1. image/reference anchor where a known physical feature is stable
2. local/manual placement
3. geographic AR anchor only when ARKit geotracking availability is confirmed at that site

ARKit geotracking is not guaranteed everywhere and can be weaker on pedestrian-only/gated areas, so never make it the only route mechanism.

## 3.3 AR guardrail

No floating cartoon saints.
No Pokémon-Go relic collection.
No sacred-content loot mechanic.

Spectacle is welcome. Trivialization is not.

---

# 4. Beacons, NFC, and physical pilgrimage markers

## 4.1 iBeacon

Optional site-deployment feature.

Best use:
- a parish/shrine intentionally installs low-cost beacons
- Anno recognizes proximity to a specific chapel/station
- user receives an in-app arrival affordance during an active pilgrimage

Do not assume churches will install hardware for v1.

Prototype first with developer-owned beacon hardware.

## 4.2 NFC

High-potential physical layer.

A small NFC tag can:
- deep-link directly to a station
- open a prayer
- mark a specific physical station as discovered
- launch an AR/camera experience

Core NFC requires device/capability handling and explicit entitlement/configuration.

NFC is probably cheaper and easier to deploy at a cooperating site than beacons.

## 4.3 QR

The boring-but-excellent fallback.

Advantages:
- zero battery
- zero entitlement
- printable
- easy field testing
- works for parish flyers, plaques, bulletin boards, temporary events

Every NFC/beacon concept should have a QR fallback during prototyping.

---

# 5. Apple Watch

Watch should be a pilgrimage companion, not a miniature iPhone app.

## Complication / widget

Show:
- today's feast
- liturgical color
- active pilgrimage progress
- next station

## During an active pilgrimage

Watch can:
- tap when approaching/arriving at a station
- show one sentence of arrival context
- show prayer prompt
- advance to next station
- mark **I'm Here**
- surface Live Activity in Smart Stack

Potential sacred interaction:
- gentle haptic prayer cadence for a short guided prayer or decade of the Rosary

Do not fake rosary completion.
Do not track heart rate for spiritual scoring.

---

# 6. Live Activities / Dynamic Island across devices

ActivityKit can surface active pilgrimage state on:
- iPhone Lock Screen
- Dynamic Island
- Apple Watch Smart Stack
- supported iPad/Mac/CarPlay contexts

This makes one implementation disproportionately valuable.

State model should be tiny:
- route ID
- station ID
- chapter number
- visited / total
- short status
- next station

No location coordinates in the public Live Activity state.

---

# 7. App Intents / Siri / Shortcuts

Existing staged intents:
- Today in Anno
- Today's Feast
- Pilgrimage Routes

Next useful intents:
- **Start La Vang Pilgrimage**
- **Open My Next Station**
- **Where am I in my pilgrimage?**
- **Show my pilgrimage progress**
- **Open today's prayer**
- **Open the Martyrs Wall station**

Later foreground navigation can route directly into a route/station.

Siri language should be ordinary:
"What's next on my La Vang pilgrimage?"

Not:
"Resolve current PilgrimageWaypoint entity."

---

# 8. Spotlight + Visual Intelligence

Spotlight:
- route
- chapters
- stations
- La Vang
- Vietnamese Catholic
- Garden Grove
- Santa Ana
- Little Saigon

Visual Intelligence future:
- define Anno entities for known churches, stations, sacred art, and pilgrimage content
- let system-level visual workflows hand recognized sacred places/content into Anno intents

Keep entity IDs stable.

---

# 9. Image Playground + Genmoji

## 9.1 Image Playground

Best fit: **pilgrimage keepsakes**, not historical illustration.

After completion, optionally let the user create:
- Marian devotional postcard
- illuminated route card
- family pilgrimage remembrance
- stylized Orange County pilgrimage poster
- portrait/landscape share art

Seed generation from:
- route title
- date
- selected station
- Marian blue / gold
- user's own captured pilgrimage image if they deliberately choose it

Availability-gate this. Apple Intelligence/image generation is not universal.

## 9.2 Genmoji / adaptive image glyph

Do not invent a core Genmoji feature just to check a box.

Good uses:
- user-generated expressive pilgrimage glyph for a share message
- custom inline "La Vang pilgrimage" glyph in a personal note/share flow
- completion keepsake embellishment

Support standard Genmoji rendering in editable/rich-text surfaces if those surfaces exist.

Do not replace canonical liturgical/sacred symbols with generated Genmoji.

---

# 10. Native sharing + Messages

Immediate:
- ShareLink for text/URL/keepsake
- proper deep links to route/station
- rich LinkPresentation metadata later

Potential Messages extension:
- Anno pilgrimage stickers
- Marian / feast share cards
- route invitation
- "meet me at La Vang" deep link

Do this only if sharing behavior proves real in user testing.

A normal iOS share sheet gets us most of the value first.

---

# 11. visionOS

Do not port the entire iPhone UI.

Use visionOS where spatial presence earns it.

High-value concepts:

### Sacred Art Chapel
- artwork at architectural scale
- source/provenance beside it
- guided devotional reflection
- no faux museum clutter

### Spatial Pilgrimage Table
- Orange County route on a 3D tabletop
- chapters rise from the map
- tap a church to open context/art/prayer

### La Vang Memory Space
- spatial reconstruction / interpretive installation
- careful distinction between documented history, devotional tradition, and artistic reconstruction

### Remote pilgrimage review
Useful for:
- elderly users
- accessibility
- family members preparing to visit

visionOS is an expansion lane, not a v1 blocker.

---

# 12. Device-awareness matrix

| Signal | Use | Permission / limitation |
| --- | --- | --- |
| Location | approach/arrival/next station | explicit location permission |
| Time | atmosphere/remembrance | none |
| Motion activity | walking/stationary context | motion permission |
| Pedometer | optional walking summary | motion permission |
| Heading | map/AR orientation | location/sensor availability |
| Barometer | future elevation-heavy routes | hardware dependent |
| Camera | Vision/AR/capture | camera permission |
| NFC | physical station markers | hardware + entitlement |
| Beacon | optional site proximity | Bluetooth/location behavior |
| Watch | haptic/glance companion | paired device |
| Apple Intelligence | generated keepsakes/Genmoji | capability, language, region, settings |

---

# 13. Privacy promise

Anno should be unusually clear:

- physical presence enhances content but never unlocks prayer as DRM
- no hidden always-on pilgrimage tracking
- no selling location data
- no requirement to upload camera frames for Vision features
- motion data is contextual, not a spiritual score
- family photos used for generated keepsakes only when explicitly selected

---

# 14. Build order

## Wave A — highest ROI Apple magic
1. Core Haptics sacred language
2. real persisted pilgrimage progress
3. completion keepsake + ShareLink
4. Live Activity state model / Dynamic Island source
5. Watch complication + active pilgrimage glance
6. App Intent progress/next-station actions

## Wave B — physical awareness
7. location-aware approach/arrival
8. time-aware atmosphere
9. motion/stationary awareness
10. QR deep links
11. NFC prototype
12. beacon prototype

## Wave C — camera + spatial
13. Vision text recognition for martyrs/plaques
14. route camera mode
15. AR image-anchor prototype at La Vang
16. geographic AR where site availability proves viable

## Wave D — generative + platform expansion
17. Image Playground keepsake
18. Genmoji/adaptive glyph share embellishment
19. Messages-specific assets if sharing proves strong
20. visionOS Sacred Art Chapel / spatial pilgrimage table

---

# 15. Definition of magical

A tester should notice Apple hardware helping without needing to know any framework names.

Examples:
- the phone *feels* different when a major pilgrimage moment arrives
- the Lock Screen quietly knows which station is next
- the Watch taps when they reach a meaningful place
- pointing the camera at the Martyrs Wall reveals context
- a physical NFC/QR marker opens exactly the right prayer
- the completion card feels personal enough to send to family
- the experience gets out of the way once prayer begins

That is the bar.

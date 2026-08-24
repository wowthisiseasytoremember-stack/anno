# Anno (Interfaith Devotional & Sacred History Engine)

<p align="center">
  <b>A luxury native SwiftUI application pairing deterministic multi-calendar calculation with peer-reviewed historical research, Catholic-first liturgical devotion, immersive AR reliquary veneration, and ambient sacred audio geofencing.</b>
</p>

---

## 🌟 Core Pillars & Capabilities

1. **Deterministic Multi-Calendar Conversion (Engine A):**
   - Pure Python / Swift mathematical engines without LLM hallucination risk.
   - Computes astronomical Easter computus (Gregorian, Julian Orthodox), Catholic 1962 / 1969 Proper divergence, Hebrew Lunisolar (`pyluach`), and Islamic Hijri (`hijri-converter`).

2. **Master Global Sacred Geography & Pilgrimages (Phase B):**
   - **72 Singular Sanctuaries & Shrines:** Verified WGS84 coordinates, historical hagiographies, relic classifications, and primary citations across 31 countries.
   - **18 Pilgrimage Corridors & 106 Waypoints:** Golden polyline routes across SoCal Vietnamese Catholic circuits (Christ Cathedral La Vang), Camino de Santiago, Rome 7 Churches, Asian Martyr trails, and Desert Monasteries.
   - **Spiritual Inquiry Header:** *"Whose path will you walk today?"* / *"Hôm nay bạn muốn bước theo con đường của ai?"* with liturgical date temporal proximity matching.

3. **Spatial AR Reliquary Viewer (`ReliquaryExplorer`):**
   - Multiplatform iOS / visionOS RealityKit viewer placing 1:1 true-scale 3D sacred reliquaries (*Cruciform Passion Reliquary, Holy Textile Casket of the Turin Shroud, Apostolic Silver Casket of Santiago*) on real surfaces.
   - Realistic PBR materials reflecting ambient room light with gold leaf, oxidized silver, and samite silk shaders.

4. **Ambient Audio Geofencing & Spatial Acoustics:**
   - Three concentric acoustic proximity tiers ($500\text{m} \rightarrow 100\text{m} \rightarrow 20\text{m}$) blooming from distant monastic choir loops to spoken bilingual hagiography with cathedral impulse response reverb.
   - Low-power CoreLocation circular region monitoring consuming $< 1.5\%$ battery over full walking days.

5. **Structural Bilingual Localization (100% EN / VI):**
   - Native support for Vietnamese diacritics, liturgical feasts (*HĐGMVN* specific solemnities), and prayers.

---

## 🏛️ Repository Layout

```
Anno/
├── Anno/                                   # Native SwiftUI Client Application
│   ├── RootView.swift                      # Main TabView (Today, Calendar, Map, Saved)
│   ├── Design/AnnoTheme.swift              # Ecclesial design tokens (Narthex, Gold Leaf, Vellum)
│   ├── Components/                         # GlassCard, TactileDateWheel, SacredArtCanvas
│   ├── Models/                             # AnnoEntry, PilgrimageRoute, Sanctuary
│   ├── Services/                           # SacredGeographyLoader, SacredSpatialAudioEngine, AudioDevotionalPlayer
│   ├── Today/TodayView.swift               # Liturgical Daily Devotional & "Walk This Path Today" card
│   ├── Map/SacredSiteMapView.swift         # MapKit interactive routes, filters & reliquary sheets
│   └── Resources/                          # Unified 182-day calendar, 365 devotional pool, MP3 audio, PNG icons
│
├── ReliquaryExplorer/                      # Multiplatform AR & Geofence Package
│   ├── Apps/iOS/                           # iOS ARKit reliquary application
│   ├── Apps/visionOS/                      # visionOS ImmersiveSpace spatial application
│   ├── Packages/PilgrimCore/               # Shared Swift package (AR, Audio, Geofence, Catalog)
│   └── Demo/SimulatorRoutes/               # GPX walking simulation trails
│
├── calendar_engine.py                      # Deterministic Python calendar engine
├── tools/                                  # Automated validation, red-team, and decodable test gates
└── docs/                                   # Architectural bibles and engineering specifications
```

---

## 🧪 Verification & Test Commands

```bash
# Run master decodable, coordinate, and content test suites
python3 tools/test_swift_geography_decodable.py
python3 tools/validate_sanctuaries.py
python3 tools/validate_route_coordinates.py
python3 tools/validate_mock_content.py
python3 tools/test_calendar_engine.py
python3 tools/red_team_stress_test.py
```

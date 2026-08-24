# Phase B: Monetization Data Schemas & Route Assets — Granular Sprint Plan

**Parent Plan:** [`docs/plans/CONSOLIDATED_AUDIT_AND_EXPANSION_PLAN.md`](file:///home/ichabod/Projects/Anno/docs/plans/CONSOLIDATED_AUDIT_AND_EXPANSION_PLAN.md)  
**Execution Environment:** Linux Server (`ichabod`) (Asset/JSON Preparation) $\rightarrow$ macOS (Client Validation)  
**Target Output:** Complete pilgrimage route JSON packs, public-domain artwork dossiers, StoreKit 2 configuration files, and localized paywall copy specifications.  
**Concurrency Profile:** Very High (Sprints B.1, B.2, and B.3 can execute 100% in parallel on Linux independently of Phase A and Phase C).

---

## Sprint B.1: Sacred Geography Pilgrimage Route Packs (Data & GeoJSON) `[PARALLELIZABLE — IMMEDIATE]`
**Target:** [`Anno/Resources/PilgrimageRoutes/`](file:///home/ichabod/Projects/Anno/Anno/Resources/) containing structured multi-stop pilgrimage JSONs.  
**Dependencies:** None. Can run immediately in parallel with Sprints B.2, B.3, and all Phase A sprints. All 4 routes can be authored concurrently.

### Context & Goal
The Pilgrim Tier ($9.99/mo or $79.99/yr) monetizes physical and spiritual religious travel. It requires curated, high-fidelity pilgrimage routes containing GPS coordinates, stop order, saint/relic descriptions, liturgical readings, and offline maps.

### Tasks
- [x] **B.1.1 — Define Route Schema (`docs/PILGRIMAGE_ROUTE_SCHEMA.md`):**
  Specify JSON schema for routes: `route_id`, `title_en`, `title_vi`, `region`, `duration_days`, `difficulty`, `waypoints` (array of `waypoint_id`, `name_en`, `name_vi`, `lat`, `lng`, `order`, `historical_summary_en/vi`, `sacred_relic_en/vi`, `scripture_reading`, `suggested_prayer_en/vi`).
- [x] **B.1.2 — Author Route 1: Rome in 3 Days (Seven Pilgrim Churches of Rome):**
  * *Stop 1:* St. Peter's Basilica (Vatican) `[41.9022, 12.4539]`
  * *Stop 2:* St. Paul Outside the Walls `[41.8587, 12.4797]`
  * *Stop 3:* Basilica of St. John Lateran `[41.8859, 12.5057]`
  * *Stop 4:* Basilica of St. Mary Major `[41.8976, 12.4984]`
  * *Stop 5:* Basilica of St. Lawrence Outside the Walls `[41.9028, 12.5208]`
  * *Stop 6:* Basilica of the Holy Cross in Jerusalem `[41.8883, 12.5161]`
  * *Stop 7:* Sanctuary of Our Lady of Divine Love `[41.7778, 12.5447]`
  * Save to `Anno/Resources/PilgrimageRoutes/rome_seven_churches.json` (bilingual EN + VI).
- [x] **B.1.3 — Author Route 2: The Holy Land — The Passion & Resurrection:**
  * *Stops:* Mount of Olives $\rightarrow$ Garden of Gethsemane $\rightarrow$ Church of All Nations $\rightarrow$ Via Dolorosa (Stations I–XIV) $\rightarrow$ Basilica of the Holy Sepulchre.
  * Save to `Anno/Resources/PilgrimageRoutes/holy_land_passion.json` (bilingual EN + VI).
- [x] **B.1.4 — Author Route 3: European Marian Shrines:**
  * *Stops:* Sanctuary of Our Lady of Lourdes (France), Sanctuary of Fátima (Portugal), Basilica of the Holy House of Loreto (Italy), Jasna Góra Monastery (Częstochowa, Poland).
  * Save to `Anno/Resources/PilgrimageRoutes/marian_shrines_europe.json` (bilingual EN + VI).
- [x] **B.1.5 — Author Route 4: Vietnam Sacred Catholic Shrines:**
  * *Stops:* Our Lady of La Vang (Quảng Trị), Notre-Dame Cathedral of Saigon, Phat Diem Cathedral (Ninh Bình), Basilica of Our Lady of the Immaculate Conception (Phú Nhai, Nam Định), Shrine of the Vietnamese Martyrs (Ba Giồng).
  * Save to `Anno/Resources/PilgrimageRoutes/vietnam_shrines.json` (bilingual EN + VI).
- [x] **B.1.6 — Geo-Coordinate Verification Script (`tools/validate_route_coordinates.py`):**
  Write validator verifying that all latitude/longitude bounds are strictly within valid earthly bounds and accurately mapped to real historical sites.

---

## Sprint B.2: High-Resolution Sacred Art Dossiers & License Clearance `[PARALLELIZABLE — IMMEDIATE]`
**Target:** [`Anno/Resources/ArtDossiers/`](file:///home/ichabod/Projects/Anno/Anno/Resources/) linking feast days to verified public-domain artworks.  
**Dependencies:** None. Can execute concurrently with Sprints B.1, B.3, and all Phase A sprints.

### Context & Goal
Sacred iconography is a primary habit-building and conversion feature. Users can zoom into high-resolution historical art (Fra Angelico, Caravaggio, Giotto, Raphael, El Greco) and view art history notes.

### Tasks
- [x] **B.2.1 — Curate 60+ High-Resolution Masterpieces:**
  Map each major feast in the 182-day calendar to verified Wikimedia Commons / Met Museum Open Access public domain images (PD-1923 / CC0).
- [x] **B.2.2 — Artwork Metadata Schema:**
  Include `artwork_id`, `title`, `artist`, `year_created`, `medium`, `current_location`, `image_url_highres`, `image_url_thumb`, `license_type` ("Public Domain - US / CC0 / Life+70"), `theological_significance_en`, `theological_significance_vi`.
- [x] **B.2.3 — Artwork Clearance & HTTP Link Check (`tools/verify_artwork_links.py`):**
  Automate an HTTP `HEAD` / `GET` request pool to ensure all image URLs return `200 OK` and non-corrupted image payloads.

---

## Sprint B.3: StoreKit 2 Configuration & Pricing Ladder Setup `[PARALLELIZABLE — IMMEDIATE]`
**Target:** [`Anno/Configuration/AnnoProducts.storekit`](file:///home/ichabod/Projects/Anno/Anno/) and pricing ladder models.  
**Dependencies:** None. Defines the canonical product catalog for both client and sandbox testing.

### Context & Pricing Strategy
From the pricing psychology audit, we implement a 4-tier funnel:
1. **Free ($0):** Current day view & conversion.
2. **Buyer Micro-Unlock ($1.99 non-consumable):** Friction-clearing purchase ("Unlock Yesterday" or single feast dossier).
3. **Annual Premium ($49.99/yr default) or Monthly ($4.99/mo):** Full calendar archive, future previews, high-res art gallery, audio.
4. **Pilgrim Pass ($9.99/mo or $79.99/yr):** GPS pilgrimage route packs & offline navigation.

### Tasks
- [x] **B.3.1 — StoreKit Configuration File (`AnnoProducts.storekit`):**
  Create an Xcode StoreKit 2 testing file defining:
  ```json
  {
    "products": [
      {
        "id": "com.anno.unlock.day_pass",
        "type": "NonConsumable",
        "price": 1.99,
        "family": "AnnoOneTime"
      }
    ],
    "subscriptions": [
      {
        "group": "AnnoSubscriptions",
        "levels": [
          {
            "id": "com.anno.subscription.premium.annual",
            "price": 49.99,
            "period": "P1Y"
          },
          {
            "id": "com.anno.subscription.premium.monthly",
            "price": 4.99,
            "period": "P1M"
          },
          {
            "id": "com.anno.subscription.pilgrim.annual",
            "price": 79.99,
            "period": "P1Y"
          },
          {
            "id": "com.anno.subscription.pilgrim.monthly",
            "price": 9.99,
            "period": "P1M"
          }
        ]
      }
    ]
  }
  ```
- [x] **B.3.2 — Localized Product Metadata (EN + VI):**
  Write bilingual marketing copy for App Store Connect submission and local display in [`Anno/Resources/product_metadata.json`](file:///home/ichabod/Projects/Anno/Anno/Resources/).

---

## Sprint B.4: Paywall Trigger Rules & Entitlement State Payloads `[DEPENDS ON B.3]`
**Target:** [`Anno/Paywall/`](file:///home/ichabod/Projects/Anno/Anno/Paywall/) paywall models and copy matrices.  
**Dependencies:** Consumes product IDs and tier definitions established in Sprint B.3.


### Tasks
- [x] **B.4.1 — Paywall Rules Matrix (`Anno/Resources/paywall_triggers.json`):**
  Formalize client gating logic:
  * *Archive Trigger:* `user_taps_date != today` $\rightarrow$ if free user, display `ArchivePaywallView` with "Yesterday's Saint" teaser.
  * *Map Trigger:* `user_pans_beyond_radius` or `user_taps_route` $\rightarrow$ display `PilgrimPaywallView`.
  * *Audio Trigger:* `play_count >= 3` in current week $\rightarrow$ display `AudioPremiumPaywallView`.
  * *Bookmark Trigger:* `saved_count >= 5` $\rightarrow$ display `SpiritualBouquetPaywallView`.
- [x] **B.4.2 — Localized Paywall Copy Matrix (EN + VI):**
  Implement high-taste, ethical Catholic copy in `Localizable.strings` (e.g. *"Never lose a day of Catholic history"* / *"Mở khóa kho tàng lịch sử và các vị Thánh"*).
- [x] **B.4.3 — Mock Purchase & Entitlement Service (`Services/EntitlementService.swift`):**
  Write an offline-safe entitlement manager that observes StoreKit `Transaction.currentEntitlements` and provides preview overrides for development.

---

## Phase B Acceptance Criteria & Done Definition
1. Four pilgrimage route files exist in `Anno/Resources/PilgrimageRoutes/` in valid bilingual JSON format.
2. All route coordinates pass `tools/validate_route_coordinates.py` with 0 invalid points.
3. Over 60 sacred art image URLs verified active (`HTTP 200`) with public domain attributions.
4. `AnnoProducts.storekit` is structured and ready for direct import into Xcode.
5. Paywall trigger rules and localized copy matrices exist and pass string validation.

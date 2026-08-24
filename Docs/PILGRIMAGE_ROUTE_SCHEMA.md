# Pilgrimage Route JSON Schema Specification

**Version:** 1.0.0  
**Target Directory:** `Anno/Resources/PilgrimageRoutes/`  
**Purpose:** Defines the data contract for sacred geography route packs supporting physical and spiritual pilgrimage navigation, offline map integration, and devotional contemplation in the Anno iOS app.

---

## 1. Top-Level Route Object Schema

Each pilgrimage route is serialized as an individual JSON file (`<route_id>.json`).

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `route_id` | String | Yes | Unique snake_case identifier (e.g. `rome_seven_churches`). |
| `title_en` | String | Yes | Human-readable English title of the pilgrimage route. |
| `title_vi` | String | Yes | Accurate, localized Vietnamese title with diacritics. |
| `region` | String | Yes | Geographic region or country (e.g., `Rome, Italy`, `Holy Land`, `Western Europe`, `Vietnam`). |
| `duration_days` | Integer / Float | Yes | Recommended duration in days (e.g., `1`, `3`, `7`). |
| `distance_km` | Number | Yes | Approximate total travel / walking distance in kilometers. |
| `difficulty` | String | Yes | Enum: `"easy"`, `"moderate"`, `"challenging"`. |
| `overview_en` | String | Yes | Detailed English overview of the spiritual journey, history, and practice. |
| `overview_vi` | String | Yes | Detailed Vietnamese overview of the spiritual journey, history, and practice. |
| `spiritual_theme_en` | String | Yes | Core spiritual theme / theological intention in English (e.g., *Metanoia and Martyrdom*). |
| `spiritual_theme_vi` | String | Yes | Core spiritual theme / theological intention in Vietnamese. |
| `waypoints` | Array[Waypoint] | Yes | Ordered list of stops along the pilgrimage route. |

---

## 2. Waypoint Object Schema

Each element in `waypoints` represents a geographic stop / sanctuary with sacred history, relic details, scripture reading, and a guided prayer.

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `waypoint_id` | String | Yes | Unique snake_case identifier within the route (e.g. `st_peters_basilica`). |
| `name_en` | String | Yes | Sacred site name in English. |
| `name_vi` | String | Yes | Sacred site name in Vietnamese with full diacritics. |
| `latitude` | Float | Yes | WGS84 Latitude between `-90.0` and `90.0`. |
| `longitude` | Float | Yes | WGS84 Longitude between `-180.0` and `180.0`. |
| `order` | Integer | Yes | 1-based sequential stop number (`1, 2, 3, ...`). |
| `historical_summary_en` | String | Yes | Historical and architectural context in English. |
| `historical_summary_vi` | String | Yes | Historical and architectural context in Vietnamese. |
| `sacred_relic_en` | String | Yes | Description of principal relics, tombs, or miraculous icons preserved at the site (English). |
| `sacred_relic_vi` | String | Yes | Description of principal relics, tombs, or miraculous icons (Vietnamese). |
| `scripture_reading` | String | Yes | Liturgical scripture citation (e.g., `Matthew 16:13-19`). |
| `suggested_prayer_en` | String | Yes | Contemplative pilgrimage prayer in English. |
| `suggested_prayer_vi` | String | Yes | Contemplative pilgrimage prayer in Vietnamese. |

---

## 3. Example JSON Structure

```json
{
  "route_id": "rome_seven_churches",
  "title_en": "The Seven Pilgrim Churches of Rome",
  "title_vi": "Hành trình Bảy Nhà thờ Hành hương Rôma",
  "region": "Rome, Italy",
  "duration_days": 2,
  "distance_km": 25.0,
  "difficulty": "moderate",
  "overview_en": "Instituted in its modern form by St. Philip Neri in the 16th century...",
  "overview_vi": "Được Thánh Philípphê Nêri khởi xướng vào thế kỷ 16...",
  "spiritual_theme_en": "Apostolic Witness and Jubilee Renewal",
  "spiritual_theme_vi": "Chứng tá Tông đồ và Canh tân Năm Thánh",
  "waypoints": [
    {
      "waypoint_id": "st_peters_basilica",
      "name_en": "St. Peter's Basilica",
      "name_vi": "Vương cung Thánh đường Thánh Phêrô",
      "latitude": 41.9022,
      "longitude": 12.4539,
      "order": 1,
      "historical_summary_en": "Erected over the tomb of St. Peter the Apostle...",
      "historical_summary_vi": "Được xây dựng trên mộ của Thánh Phêrô Tông đồ...",
      "sacred_relic_en": "Tomb of Saint Peter the Apostle under the Baldachin",
      "sacred_relic_vi": "Mộ Thánh Phêrô Tông đồ bên dưới Tán bàn thờ Bernini",
      "scripture_reading": "Matthew 16:13-19",
      "suggested_prayer_en": "Lord Jesus Christ, Rock of our Salvation...",
      "suggested_prayer_vi": "Lạy Chúa Giêsu Kitô, Đá tảng của ơn cứu độ..."
    }
  ]
}
```

---

## 4. Validation Invariants
1. `latitude` must be within `[-90.0, 90.0]`.
2. `longitude` must be within `[-180.0, 180.0]`.
3. `order` must start at `1` and increment contiguously without gaps (`1, 2, ..., N`).
4. Bilingual fields must never be empty or placeholder strings. Vietnamese text must use standard Vietnamese unicode diacritics.
5. JSON files must parse cleanly with `json.load()` and conform strictly to the key set.

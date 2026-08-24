# Anno — Liturgical Solar Compass & Multi-Calendar Sundown Ring

**Feature Codename:** `HorariumSolarCompass` / `LiturgicalDial`  
**Domain:** Native SwiftUI (`Canvas`, `TimelineView`, `CoreLocation`, `UIImpactFeedbackGenerator`)  
**Status:** Feature Specification & Implementation Plan  
**Target Delivery:** High-Craft Luxury Interface (Post-Scaffold Milestone)  

---

## 1. Product Vision & Spiritual Rationale

In the Catholic and broader Abrahamic tradition, **time is not a linear digital counter—it is cyclical, liturgical, and solar**:
1. **The Divine Office (Liturgy of the Hours / *Kinh Phụng Vụ*):** Catholic monasticism and the universal Church partition the 24-hour day into 7 canonical prayer gates (*Matins, Lauds, Terce, Sext, None, Vespers, Compline*).
2. **The Sundown Divergence:** In the Hebrew and Islamic calendars, the date transitions at **astronomical sunset** (*Tzeit HaKochavim* / *Maghrib*), whereas the civil Gregorian day changes at midnight (12:00 AM).
3. **The UX Breakthrough:** The **Liturgical Solar Compass** transforms this complex theological and mathematical reality into a fluid, tactile 24-hour astronomical dial (resembling a luxury Swiss mechanical astrolabe) right in the `TodayView` of Anno.

```
                                 12:00 PM (Sext)
                                       ▲
                            ┌──────────┴──────────┐
               09:00 AM     │      DAY ARC        │     03:00 PM
               (Terce) ◄────┤    (Golden Glow)    ├────► (None / Mercy Hour)
                            └──────────┬──────────┘
                                       │
  06:00 AM (Lauds) ────────────────────┼────────────────────► 06:00 PM (Vespers)
  [Sunrise Boundary]                   │                      [Sunset Boundary]
                            ┌──────────┴──────────┐           ★ HEBREW & HIJRI
               03:00 AM     │     NIGHT ARC       │           DATE ADVANCES HERE!
               (Matins) ◄───┤   (Deep Narthex)    ├───► 09:00 PM (Compline)
                            └──────────┬──────────┘
                                       ▼
                               12:00 AM (Midnight)
                           [Gregorian Date Advances]
```

---

## 2. Interactive Component Architecture

### 2.1 The 24-Hour Circular Dial (`LiturgicalCompassView.swift`)
* **Outer Ring — The 7 Canonical Liturgical Hours:**
  * **Matins / Office of Readings (*Kinh Đêm*):** 00:00 – 05:00 (Dark indigo glow).
  * **Lauds / Morning Prayer (*Kinh Sáng*):** 05:00 – 08:00 (Dawn rose-gold glow).
  * **Terce / Mid-Morning (*Kinh Giờ Ba*):** 08:00 – 11:30 (Daylight gold).
  * **Sext / Midday Prayer (*Kinh Giờ Sáu*):** 11:30 – 14:00 (High noon golden zenith).
  * **None / Divine Mercy Hour (*Kinh Giờ Chín*):** 14:00 – 17:00 (Passion hour amber).
  * **Vespers / Evening Prayer (*Kinh Chiều*):** 17:00 – 20:00 (Sunset twilight crimson).
  * **Compline / Night Prayer (*Kinh Tối*):** 20:00 – 24:00 (Deep sanctuary sapphire).
* **Inner Ring — The Multi-Calendar Sundown Transition Marker:**
  * Displays the exact computed local sunset time (e.g. `19:42`).
  * Features a prominent golden flare at the sunset notch: when the rotating solar indicator passes this notch, the Hebrew date (e.g. *11 Elul 5786*) and Islamic date (e.g. *11 Rabi' al-Awwal 1448*) visually increment with a smooth rolling counter and haptic tap, 4 hours before the Gregorian date changes at midnight.
* **Center Hub — Real-Time Astronomical Sun & Moon Indicator:**
  * Shows exact solar elevation, twilight phases (Civil, Nautical, Astronomical), and moon illumination percentage.
  * Tapping the center hub opens the **Hour Prayer Drawer**, presenting the Psalms, Canticle, and antiphons for the active liturgical hour in English and Vietnamese.

---

## 3. Data & Mathematical Engine (`HorariumEngine.swift`)

The dial is driven by pure mathematical models already built into Anno:
1. **Solar Ephemeris:** Computes local solar noon, sunrise, and sunset based on user GPS or default sanctuary coordinates using NOAA solar calculations (available in `calendar_engine.py`).
2. **Canonical Interval Mapping:** Calculates current active hour, elapsed percentage of the current hour, and exact countdown timer to the next liturgical prayer gate.
3. **Multi-Calendar Epoch Alignment:** Seamlessly links Gregorian $Y/M/D$, Julian (O.S.), Hebrew Molad / Parashah, and Saudi Umm al-Qura dates.

```swift
public struct LiturgicalHourState {
    public let currentHour: CanonicalHour
    public let nextHour: CanonicalHour
    public let timeUntilNextHour: TimeInterval
    public let solarElevationDegrees: Double
    public let isDaylight: Bool
    public let sunsetDate: Date
    public let activeHebrewDateString: String
    public let activeGregorianDateString: String
    
    public enum CanonicalHour: String, CaseIterable, Identifiable {
        case matins = "Matins"
        case lauds = "Lauds"
        case terce = "Terce"
        case sext = "Sext"
        case none = "None"
        case vespers = "Vespers"
        case compline = "Compline"
        
        public var nameVi: String {
            switch self {
            case .matins: return "Kinh Đêm"
            case .lauds: return "Kinh Sáng"
            case .terce: return "Kinh Giờ Ba"
            case .sext: return "Kinh Giờ Sáu"
            case .none: return "Kinh Giờ Chín"
            case .vespers: return "Kinh Chiều"
            case .compline: return "Kinh Tối"
            }
        }
    }
}
```

---

## 4. Tactile & Haptic Interactions

* **Live Mode:** The compass tracks real-time system clock using SwiftUI `TimelineView(.periodic(from: .now, by: 60.0))`.
* **Time-Travel Scrubbing Mode:** The user can touch and rotate the dial 360 degrees:
  * Every canonical hour boundary crossed fires a distinct haptic pulse (`UIImpactFeedbackGenerator(style: .medium)`).
  * Crossing the **Sunset Boundary** triggers a double-tap haptic (`.rigid` followed by `.light`) as the Hebrew/Hijri date indicators roll forward.
  * Crossing the **Midnight Boundary** triggers a solemn church-bell haptic sequence as the Gregorian date advances.
* **"Snap to Now" Floating Button:** Seamless spring animation returning the dial to the present liturgical moment.

---

## 5. Granular Implementation Tasks & Roadmap

- [ ] **Task H.1 — Solar Mathematics & Horarium Engine (`Anno/Services/HorariumEngine.swift`):**
  - Implement NOAA solar zenith & twilight calculations.
  - Implement active canonical hour interval resolver with day/night arc geometry.
- [ ] **Task H.2 — Circular Astrolabe Canvas (`Anno/Components/LiturgicalCompassDial.swift`):**
  - Custom SwiftUI `Canvas` rendering 24-hour Roman numeral ticks, liturgical hour sectors, and sunset flare notches.
  - Smooth gesture rotation with boundary snap and haptic feedback.
- [ ] **Task H.3 — Real-Time Date Rollover Animation (`Anno/Components/SundownRolloverView.swift`):**
  - Dual rolling number transition displaying Gregorian date vs. Hebrew/Islamic sundown transition.
- [ ] **Task H.4 — Canonical Prayer Drawer Integration (`Anno/Views/CanonicalHourPrayerView.swift`):**
  - Bilingual (EN/VI) Psalmody, Scripture reading, and closing collect for the active hour.
- [ ] **Task H.5 — `TodayView` Top-Fold Embed:**
  - Integrate the dial directly above the hero saint card in `TodayView.swift` with dynamic `.liturgicalAtmosphere()` background response.

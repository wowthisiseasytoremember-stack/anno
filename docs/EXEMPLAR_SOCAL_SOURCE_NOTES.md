# SoCal La Vang Exemplar — Source & Volatility Notes

**Verified:** 2026-10-03  
**Scope:** official-source facts used by the Orange County exemplar.  
**Rule:** devotional narrative may be durable; schedules/hours/parking/tours are volatile and must be rechecked.

## Recheck of official pages — 2026-11-06 (remote, not on-site)

**Scope:** Desktop-readable official-page claims and public links; this is not a certificate of accessibility, legal permission to enter, translation accuracy, or field conditions. The original 2026-10-03 audit remains the baseline for other claims. These pages can change; do not copy live hours into durable JSON.

| Live station ID | Checked claim or verification outcome | Source | Status / remaining review |
| --- | --- | --- | --- |
| `our_lady_la_vang_shrine_christ_cathedral` | Christ Cathedral identifies the shrine, its 2021 opening, Vietnamese Marian clothing/canopy, and the **Catholic tradition** of La Vang in 1798. | https://www.christcathedralcalifornia.org/ollvshrine/about-the-shrine/ | Official page present; outdoor visibility and devotional wording still require field/cultural review. |
| `martyrs_wall_117_vietnamese_christian` | Christ Cathedral describes the names of 117 martyrs and inscriptions recording dates/manner of death. | https://www.christcathedralcalifornia.org/ollvshrine/pictures/ | Official page present; do not claim inscriptions are readable to every visitor. |
| `rosary_gardens_christ_cathedral_pilgrimage` | Christ Cathedral presents Marian Gardens behind the shrine as a place for the Rosary. | https://www.christcathedralcalifornia.org/event_slides/marian-gardens/ | Official page present; entrances, seating, accessibility and open status still require visit-day check. |
| `christ_cathedral_context` (optional) | Christ Cathedral publishes visitor/tour information and offers requested languages subject to availability. | https://www.christcathedralcalifornia.org/visit/ | Live tour offerings are volatile: app copy now links out rather than freezing the offerings. |
| `st_columban_church_garden_grove` | Diocese confirms Saint Columban at 10801 Stanford Ave, Garden Grove, and describes its multicultural identity. | https://www.rcbo.org/directories/parishes/saint-columban-catholic-church/ | Actual programs, Vietnamese schedule and physical access still need live/local verification. |
| `vietnamese_catholic_center_santa_ana` | Diocese confirms 1538 Century Blvd, Santa Ana, Vietnamese architectural features, and a three-generation religious/cultural/educational/social mission. | https://www.rcbo.org/directories/parishes/vietnamese-catholic-center/ | Official page present; cannot infer public entry or current programs. |
| `our_lady_of_la_vang_church_santa_ana` | Diocese confirms the active parish at 288 S Harbor Blvd, Santa Ana. | https://www.rcbo.org/directories/parishes/our-lady-of-la-vang-catholic-church/ | Official page present; current parish/language schedules and site access need review. |
| `st_barbara_parish_westminster` | Diocese confirms **Saint Barbara is in Santa Ana**, at 730 S Euclid St. The legacy ID is not the visitor label. | https://www.rcbo.org/directories/parishes/saint-barbara-catholic-church/ | Keep stable ID for progress/markers; current parish programming/access require review. |

**Editorial handling:** A canonical link's presence is not a full fact-check of every clause; link reachability changes and could not be proven by an offline validator. The Linux gate checks that each of the eight station links is indexed here and matches content data, while historical-source judgment remains editorial. The normalized route's `distance_km=0` currently suppresses distance UI; treat this as **unknown pending field measurement**, not literal zero distance.

## Christ Cathedral / Our Lady of La Vang Shrine

Official:
- https://www.christcathedralcalifornia.org/ollvshrine/
- https://www.christcathedralcalifornia.org/ollvshrine/about-the-shrine/
- https://www.christcathedralcalifornia.org/ollvshrine/pictures/
- https://www.christcathedralcalifornia.org/event_slides/marian-gardens/
- https://www.christcathedralcalifornia.org/visit/

Verified durable facts:
- shrine is on Christ Cathedral campus in Garden Grove
- shrine was blessed/opened in July 2021
- shrine visually references the La Vang rainforest tradition
- central Marian statue is depicted in Vietnamese áo dài and khăn đống
- shrine includes the names of 117 Vietnamese Catholic martyrs; panels identify name/date/manner of death
- Marian Gardens are open behind the shrine and are presented as a place to pray the Rosary
- Christ Cathedral offers tours and lists Vietnamese as an available reservation language, subject to guide availability

Volatile:
- campus hours
- tour schedule
- parking lot assignment
- construction/event closures
- guide availability

## Saint Columban Catholic Church

Official:
- https://www.saintcolumbanchurch.org/
- https://www.rcbo.org/directories/parishes/saint-columban-catholic-church/

Verified durable facts:
- 10801 Stanford Ave, Garden Grove, CA 92840
- Diocese of Orange parish
- describes itself as a sacramental, multicultural community
- Vietnamese-language liturgical and formation life is currently substantial

Volatile:
- Mass times
- confession/adoration schedules
- parish staffing
- office hours

## Vietnamese Catholic Center

Official:
- https://www.rcbo.org/directories/parishes/vietnamese-catholic-center/
- official site linked by Diocese: https://sites.google.com/vietcatholiccenter.org/web/

Verified durable facts:
- 1538 Century Blvd, Santa Ana, CA 92703
- Diocese describes the Center as important to Vietnamese-American Catholic life
- its architecture intentionally reflects Vietnamese design
- Diocese says it supports religious, cultural, educational, and social activities
- Diocese explicitly describes service to three generations: elders, adults, children

Volatile:
- office hours
- program/event schedule
- current staff/contact details

## Our Lady of La Vang Catholic Church

Official:
- https://www.rcbo.org/directories/parishes/our-lady-of-la-vang-catholic-church
- https://ourladyoflavang.org/

Verified durable facts:
- active Diocese of Orange parish
- 288 S Harbor Blvd, Santa Ana, CA 92704
- La Vang identity exists here as parish life, not only at the Christ Cathedral shrine

Volatile:
- Mass/liturgy language schedule
- office hours
- current clergy/staff
- parish events

## Saint Barbara Catholic Church

Official:
- https://www.saintbarbarachurch.org/
- https://www.rcbo.org/directories/parishes/saint-barbara-catholic-church/

Verified durable facts:
- 730 S Euclid St, Santa Ana, CA 92704
- active Diocese of Orange parish
- current official parish materials show extensive Vietnamese-language liturgical life
- parish also has school/formation/sacramental structures that make it useful for the "faith handed forward" chapter

Important correction:
- **Santa Ana, not Westminster**

Volatile:
- Mass times
- confession times
- clergy/staff
- school/program details

## Historical-language rule

For the 1798 La Vang tradition:
- use "Catholic tradition holds..." / "the shrine commemorates..." / "Vietnamese Catholics venerate..."
- avoid presenting the apparition as an independently verified empirical event

For local contemporary facts:
- direct factual language is appropriate when supported by official parish/diocesan sources.

## Vietnamese review rule

The current exemplar Vietnamese copy is a product draft.

Before final:
- review with fluent Vietnamese Catholic readers
- preserve devotional terminology familiar to Vietnamese Catholics
- allow Vietnamese line breaks and phrasing to differ from English
- do not label strings "verified" merely because they are grammatically correct

## Field-test checklist

When the user can physically run the route, verify:
- actual drive order and friction
- parking/arrival clarity at each geographic stop
- whether Christ Cathedral substations feel like one chapter
- whether Vietnamese Catholic Center and St. Barbara feel distinct rather than redundant
- whether Our Lady of La Vang parish earns a major-moment treatment
- realistic Quick/Core route duration
- whether opening and completion language feels moving or overproduced

# SoCal La Vang exemplar — full station editorial audit

**Claimed area:** Orange County / Our Lady of La Vang pilgrimage, all **8** existing stations: seven core waypoints plus optional Christ Cathedral context.  
**Date:** 2026-11-06. **State:** baseline audit completed **before** implementation. Findings are not claims of field verification.  
**Environment:** SwiftUI iOS/MapKit devotional experience; JSON content in `Anno/Resources/socal_la_vang_exemplar_content_v1.json` and seven live waypoints in `Anno/Resources/PilgrimageRoutes/socal_vietnamese_catholic_pilgrimage_la_vang.json`. Source references are in `docs/EXEMPLAR_SOCAL_SOURCE_NOTES.md`; native bundle has no web article publishing stage. Live shipping = built, device-tested, submitted/released through App Store/TestFlight as appropriate; GitHub merge alone is **not** release.

**Boundaries:** Preserve 5 geographic chapters, 7 core IDs, the optional cathedral station, manual “I'm Here,” bilingual drafts, app's ARRIVE / LOOK / KNOW / PRAY / CONTINUE grammar, and existing moment levels. Do not insert schedule, parking, or accessibility claims without fresh on-site or official corroboration. The source-note verification date is 2026-10-03; links and mutable claims need pre-release rechecking. The historic apparition remains **Catholic tradition**, not empirical certainty. Drive's located East Asian route research is archival/other-route material, not authority for Orange County.

## Full per-item findings (three-column audit)

### 1. Our Lady of La Vang Shrine — `our_lady_la_vang_shrine_christ_cathedral`
| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Strong visual first LOOK and clear refuge thesis; route-facing source is only a link, not a claim-by-claim ledger. | medium | Cross-reference exact shrine/about source in the existing source notes; include claim-to-source audit checklist in the reusable template. |
| Visual instruction presumes the statue/canopy is visible on arrival; accessible arrival, QR/NFC, and image alt text not field-tested. | medium | Add conditional public-viewing wording; retain manual check-in and verify wayfinding/accessibility on-site; no speculative hero image. |
| Vietnamese phrasing has no human Catholic sign-off. | high | Keep `translation_status` as review-needed; send EN/VI paired text and theological terminology for reader review before release. |

### 2. 117 Vietnamese Martyrs wall — `martyrs_wall_117_vietnamese_christian`
| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Precise number 117 and panel details rely on Christ Cathedral shrine source, not a recorded per-claim check. | medium | Cite shrine/about and pictures in editorial notes; flag any altered count, dates, or translations for source confirmation. |
| LOOK asks visitors to read a death detail that may be small or inaccessible. | medium | Make observation conditional; give an alternative personal reflection without requiring close access to the wall. |
| Martyr imagery and captions require respectful treatment and alt text if artwork is later added. | low | Use the existing restrained highlight; record captions, rights, and accessible text in asset checklist, not unlicensed visual production. |

### 3. Marian Gardens — `rosary_gardens_christ_cathedral_pilgrimage`
| Issue | Severity | Proposed fix |
| --- | --- | --- |
| “Find a place to sit” assumes seating/access is available; on-site conditions unverified. | medium | Allow standing or pausing in permitted space; avoid promises of seating, hours, or quiet. |
| Historic fact is short and sourced in existing notes; source affordance is not part of ritual UI. | medium | Make official visit/source link discoverable in station UI; preserve calm reflection presentation. |
| No image or transcript is attached; assess Dynamic Type/VoiceOver in device pass. | low | Keep text-only card; verify semantic reading order and contrast on iPhone. |

### 4. Optional Christ Cathedral context — `christ_cathedral_context`
| Issue | Severity | Proposed fix |
| --- | --- | --- |
| KNOW embeds potentially volatile Vietnamese-language tour availability. | high | Replace with durable campus context and direct readers to official visitor page for current tour/language arrangements. |
| Optional item has `station_id` rather than `waypoint_id` by design; it is **not** a live route waypoint. | low | Retain ID and optional state; do not manufacture an eighth GPS station or require it for completion. |
| Context route is not surfaced as a core waypoint; optional presentation may need a device check. | medium | Verify extended variant and keyboard/VoiceOver access during native QA; do not claim it is currently reachable. |

### 5. Saint Columban — `st_columban_church_garden_grove`
| Issue | Severity | Proposed fix |
| --- | --- | --- |
| LOOK assumes multilingual/formation activities are visible during a random visit. | medium | Use a conditional public-facing observation, avoiding promises of events or building access. |
| “Currently maintains” refers to changeable programming; exact calendar not fixed. | medium | Phrase as official parish identity, link the parish for present details; verify before release. |
| Vietnamese Catholic voice and access routes require a parish/family reader and field test. | high | Keep human sign-off and access checks open; do not assert current language schedule. |

### 6. Vietnamese Catholic Center — `vietnamese_catholic_center_santa_ana`
| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Diocese's description of three generations is appropriately attributed, but visit instructions do not differentiate public exterior viewing from access to programs. | medium | Keep diocesan attribution, make the LOOK doable from a permitted space; avoid promising entry. |
| Accessibility/parking/grounds access has not been field-tested. | high | Add explicit access-check flag; no invented visitor instructions. |
| VI cultural/institutional terms have not been human-reviewed. | high | Flag human Vietnamese Catholic editorial review. |

### 7. Our Lady of La Vang parish — `our_lady_of_la_vang_church_santa_ana`
| Issue | Severity | Proposed fix |
| --- | --- | --- |
| LOOK is conceptual (“difference between”) rather than a concrete on-site prompt; opening lacks the immediate observation. | medium | Direct attention to the parish name/setting, conditionally from a public area, then connect it to everyday worship. |
| Claim that this is an active Santa Ana parish is in diocesan source notes but not citation-visible in ritual card. | medium | Preserve diocesan URL and surface an official-source link in app. |
| Language-community nuance and visit logistics need local review. | high | Flag parish-family review and site access check; do not invent Mass languages or hours. |

### 8. Saint Barbara — `st_barbara_parish_westminster` (stable ID; physical site Santa Ana)
| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Stable legacy identifier says Westminster, while verified address and displayed name say Santa Ana. | medium | **Do not rename** identifier without migration for persisted progress, links, markers, and tests; keep visible Santa Ana geography correct. |
| LOOK lists Mass, confession, school, people arriving as if immediately visible. | medium | Give a conditional public-facing prompt instead of implying activity at arrival. |
| The connection from institution-building to family continuity works; VI translation and visitor access lack human/device verification. | high | Keep family/Catholic language and field-test flags open; keep reflection-level dignity rather than achievement language. |

## Shared findings / release gates

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| All 8 stations contain EN/VI ARRIVE/LOOK/KNOW/PRAY/CONTINUE and official URLs, but no automated editorial conformance gate. | high | Add a lightweight validator that inspects all 8 stations, core-to-route consistency, official links, voluntary access language, and translation-status flag. |
| No reusable one-item scaffold documenting the schema and editorial checks. | medium | Add parameterized native JSON starter with one command that creates a single station-file draft; retain strict non-shipping status. |
| No visible official-source action in `SoCalStationRitualView`; link is stored but not rendered there. | high | Add a native SwiftUI `Link` with accessible bilingual label and validity guard; keep external navigation optional. |
| Content lacks field-confirmed hours, parking, physical approach radii, estimated travel distance, and accessibility. | high | Do **not** fabricate. Issue #28 remains the owner for field verification; keep route `distance_km=0` as hidden/unknown sentinel until measured, not as a zero-distance claim. |
| Image/thumbnail/cover references and final App Store screenshots not present in these station records; copyrights and alt text need real app/assets. | medium | Skip decorative image generation; use existing semantic native banners. Do device-level accessibility, performance, link, preview and asset rights passes before publishing. |
| No direct rendering measurement or Xcode build available in this connector session. | high | Validate JSON and source-level invariants; require macOS device/Xcode pass (#33) before calling this shipped. |

## Source & status index

- Christ Cathedral shrine and martyrs: https://www.christcathedralcalifornia.org/ollvshrine/about-the-shrine/ ; https://www.christcathedralcalifornia.org/ollvshrine/pictures/
- Marian Gardens: https://www.christcathedralcalifornia.org/event_slides/marian-gardens/
- Cathedral visitor information: https://www.christcathedralcalifornia.org/visit/
- Saint Columban: https://www.saintcolumbanchurch.org/ ; https://www.rcbo.org/directories/parishes/saint-columban-catholic-church/
- Vietnamese Catholic Center: https://www.rcbo.org/directories/parishes/vietnamese-catholic-center/
- Our Lady of La Vang parish: https://www.rcbo.org/directories/parishes/our-lady-of-la-vang-catholic-church
- Saint Barbara: https://www.rcbo.org/directories/parishes/saint-barbara-catholic-church/

**Open human checks:** native Vietnamese Catholic edit; local parish/cultural authenticity; site access/parking/routes/physical accessibility and distance; current official schedules/tours; links and rights; color contrast, dynamic type, VoiceOver on device. Until checked, this is **edited draft**, not field-verified or released.

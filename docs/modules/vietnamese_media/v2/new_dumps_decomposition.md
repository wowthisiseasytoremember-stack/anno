# New Vietnamese Media Dumps — Decomposition Against Existing Module

**Source:** 4 zip-extracted files (August 2026 research)  
**Against:** `vietnamese_media/` module (v1: source dump + module index, v2: citation templates, v3: full landscape with sprints)

---

## File Inventory

| New File | Focus | Unique Value |
|----------|-------|--------------|
| `directory_westminster_oc.md` | Westminster/OC-specific directory + **ideological/political landscape** (Conciliar vs Traditionalist) | Demographic context, outreach strategy per segment, 34 sources with orientation flags |
| `master_directory_technical.md` | **Technical ingestion architecture** + legal flags + code snippets | HTML/JS ingestion templates, Vatican copyright rules, RSS/API patterns, daily schedule |
| `hub_source_list_verified.md` | **Verification-tiered source list** (Group 1/2/3) with category tags [A]/[B1]/[B2]/[C] | Verified live vs unconfirmed vs rejected; contact info; corrections from prior doc |
| `directory_outreach.md` | Outreach/marketing directory + **political orientation analysis** + top 10 priorities | Verification tiers, exclusion list, verification log, next steps |

---

## What's NEW vs Existing v1 Module Index (`module_index.md`)

| Existing M1-M10 | New Docs Add |
|-----------------|--------------|
| **M1 Streaming** | 34 YouTube channels with **verified channel IDs/handles**, ideological orientation per channel, daily schedule matrix |
| **M2 Radio/Audio** | **13 radio/podcast sources** with stream URLs (HLS/MP3/RSS), mobile apps, Radio Garden alternatives |
| **M3 Parish Livestreams** | **8 OC parishes** with verified livestream URLs, archive depth (back to Dec 2023), weekly schedules |
| **M4 Official** | Vatican News VI podcast RSS URL, RVA 24/7 digital stream (not shortwave), HDGM Vietnam YouTube |
| **M5 Diaspora** | VietCatholic News full platform map (web, YouTube 724K, TV, radio archive, document archive) |
| **M6 General VI** | KVNR 1480 **rejection** (no verified Catholic hour), SBTN/VCAL/VNA-TV placement context |
| **M7 Vietnam-Produced** | **TGPSG corrected handle** (@tgpsgthanhletructuyen), Redemptorists migrated to @dcctsaigon, HDGM verified |
| **M8 Films** | **Phim Công Giáo Archive** (phimconggiao.net), **Thánh Ca Việt Nam** (70+ years hymnody, PDF+MP3) |
| **M9 Aggregators** | **nguoiviet.tv** (embeds KVNR, VNCR, VietCatholic), VietCatholic TV streaming |
| **M10 Orientation** | **Explicit Conciliar vs Traditionalist taxonomy** with outreach guidance per segment |

---

## New Actionable Intelligence

### 1. Legal/Technical Compliance (from master_directory_technical.md)
- **Vatican Copyright:** Only iframe embeds + RSS allowed — no rehosting MP4 without written consent from `tiengviet@vaticannews.va`
- **RVA Status:** Shortwave dead; digital HLS/MP3 stream **live** at `vietnamese.rvasia.org` + Radio Garden + mobile app
- **Redemptorist Migration:** `trungtammucvudcct.com` lapsed → all content at YouTube `@dcctsaigon` + `dongchuacuuthe.us`
- **Parish Cadence:** COVID daily streams → Weekend/Vigil focus (verify current schedules)

### 2. Verified Ingestion Code Snippets (master_directory_technical.md §4)
- **YouTube iframe embed** template for parish livestreams
- **HTML5 audio player** for RVA + Radio MHCG streams
- **RSS → JSON parser** for Vatican News daily podcast (Node.js fetch example)
- **Daily liturgical broadcast schedule** (Pacific Time) — 6:30am Saigon → 10pm Radio MHCG

### 3. Verification Corrections (hub_source_list_verified.md §C)
| Prior Claim | Correction |
|-------------|------------|
| KVNR 1480 "Sống Đức Tin" Thurs 8-9pm | ❌ **Unverified** — likely Protestant "Đài Nguồn Sống" confusion |
| Our Lady of the Pillar, Riverside daily 5pm | ❌ **Wrong parish** — that parish is in St. Louis, MO |
| TGPSG channel ID UCc7qu2cB... | ❌ **Unconfirmed** — use `@tgpsgthanhletructuyen` |
| youtube.com/c/rvaviet for RVA | ❌ **Unconfirmed** — verified `@daichanlyachau` (UCfEEKI87bNDZkqWPSh5OkLQ) |
| rveritas-asia.org podcast RSS | 🔴 **Fetch failed** — Wayback only |
| "Don't embed Vatican YouTube" | ⚠️ **Overcautious** — embedding official player IS permitted |
| St. Cecilia/St. John/Holy Spirit "✅ Verified" | 🟡 **Inflated** — based on 2020 listings; 2025-26 schedules differ |

### 4. Political Orientation Taxonomy (directory_westminster_oc.md + directory_outreach.md)
| Category | Outlets | Outreach Guidance |
|----------|---------|-------------------|
| **Conciliar/Progressive/Vatican II** | Vatican News VI, RVA, Jesuit Media (Dòng Tên), Diocesan media, Youth ministry | Second-gen, young families, educators, students |
| **Traditionalist/Conservative/Anti-Communist** | VietCatholic Network, Radio MHCG, CRM, SBTN, Charismatic channels | First-gen elders, parish councils, senior groups, conservative donors |
| **Devotional/Scriptural/Neutral** | Daily Gospel apps, Lời Chúa Cho Mọi Người | Universal — safe for any campaign |
| **State-Affiliated (Vietnam)** | Báo Người Công giáo Việt Nam (UBĐKCGVN) | **Flag prominently** — state-sponsored, not Church-run |
| **Self-identified "Left/Liberal" VI Catholic** | **None found** | Orientation runs anti-communist ↔ neutral ↔ state-affiliated |

### 5. Top 10 Outreach Priorities (directory_outreach.md §1)
1. Vietnamese Catholic Center (Santa Ana) — daily Mass, diocesan anchor
2. Christ Cathedral (Garden Grove) — multiple weekly Vietnamese Masses, La Vang Shrine
3. Radio Mẹ Hằng Cứu Giúp (KALI-FM 106.3) — daily radio hour receivable in Westminster
4. Công Giáo TV (VietCatholic TV) — 24/7 online TV stream
5. Vatican News Tiếng Việt — official Holy See VI content
6. Radio Veritas Asia — 24/7 web radio + 116K YouTube
7. VietCatholic News — oldest/largest diaspora (1996, 724K subs)
8. Holy Spirit Parish Fountain Valley — largest VI parish in OC
9. Đức Mẹ La Vang Santa Ana — parish + shrine events
10. TGPSG (Saigon Archdiocese) — source with state context flag

### 6. Enrichments from Reviewed Doc (hub_source_list_verified.md §B)
- VCC OC: phone (714) 554-4211, capacity ~200, ~83K served, legacy domain vncatholic.net
- St. Barbara Santa Ana: large VI community, links to VietCatholic resources
- St. Bonaventure Huntington Beach: livestream hub with archived Masses
- Diocese of Orange Vimeo (vimeo.com/rcbo): VI synod/formation videos
- Radio Veritas alternatives: Radio Garden, myTuner
- TNTT/VEYM: 14 chapters in Diocese of Orange (tnttldns.org)
- **Localization candidate:** "Magnifica Humanitas" (Pope Leo XIV encyclical, May 2026) — check vaticannews.va/vi for VI translation first

---

## Mapping to Existing vietnamese_media Module Structure

### v1 (Raw Dumps) — ADD THESE 4 FILES
| New File | Module Slot |
|----------|-------------|
| `directory_westminster_oc.md` | M1-M3 + M10 (orientation) |
| `master_directory_technical.md` | M1-M2 + M4-M5 + ingestion code |
| `hub_source_list_verified.md` | All M1-M10 with verification tiers |
| `directory_outreach.md` | M1-M9 + M10 orientation + top 10 |

### v2 (Synthesized) — NEEDS UPDATE
| File | Update Needed |
|------|---------------|
| `citation_templates.md` | Add 34 YouTube channel IDs, 13 radio stream URLs, 8 parish livestream URLs, corrected handles |
| **New needed** | `ingestion_code_snippets.md` — HTML/JS templates from master_directory_technical.md §4 |
| **New needed** | `legal_compliance_rules.md` — Vatican copyright, RVA status, Redemptorist migration, parish cadence |
| **New needed** | `verification_corrections.md` — 9 corrected/rejected claims from hub_source_list_verified.md |

### v3 (Full Landscape with Sprints) — NEEDS UPDATE
| Section | Update |
|---------|--------|
| Partnership tracker | Add VCC OC, Christ Cathedral, Radio MHCG, VietCatholic News, Holy Spirit FV as Tier 1 |
| Source allowlist for Engine B | Update with verified handles/IDs, add category tags [A]/[B1]/[B2]/[C], verification status |
| Sprint planning | Add "Technical ingestion build" sprint (code snippets), "Legal compliance audit" sprint |

---

## Recommended Next Steps

| Priority | Action | Owner |
|----------|--------|-------|
| **1** | Extract ingestion code snippets → `ingestion_code_snippets.md` (v2) | `deepseek-worker` |
| **2** | Extract legal compliance rules → `legal_compliance_rules.md` (v2) | `deepseek-worker` |
| **3** | Extract verification corrections → `verification_corrections.md` (v2) | `yolo-worker` |
| **4** | Update `citation_templates.md` (v2) with 34 channel IDs + 13 stream URLs + 8 parish URLs | `deepseek-worker` |
| **5** | Update v3 `full_landscape_with_sprints.md` partnership tracker + source allowlist | `deepseek-worker` |
| **6** | Build Engine B source allowlist JSON from updated allowlist | `deepseek-worker` |

---

## Module Completeness After This Ingestion

| Module | v1 (Raw) | v2 (Synthesized) | v3 (Implementation) |
|--------|----------|------------------|---------------------|
| **M1 Streaming** | 🟢 34 channels | 🟡 needs channel IDs | 🟡 needs allowlist JSON |
| **M2 Radio/Audio** | 🟢 13 sources | 🟡 needs stream URLs | 🟡 needs RSS parser |
| **M3 Parish Livestreams** | 🟢 8 parishes | 🟡 needs verified URLs | 🟡 needs archive depth |
| **M4 Official** | 🟢 Vatican/RVA/HDGM | 🟢 citation templates | 🟢 |
| **M5 Diaspora** | 🟢 VietCatholic full map | 🟢 | 🟢 |
| **M6 General VI** | 🟢 KVNR rejection noted | 🟢 | 🟢 |
| **M7 Vietnam-Produced** | 🟢 corrected handles | 🟢 state context flags | 🟢 |
| **M8 Films/Archive** | 🟢 Phim Công Giáo, Thánh Ca | 🟢 | 🟢 |
| **M9 Aggregators** | 🟢 nguoiviet.tv, VietCatholic TV | 🟢 | 🟢 |
| **M10 Orientation** | 🟢 Conciliar vs Traditionalist taxonomy | 🟢 | 🟢 |
| **Legal/Technical** | 🟢 in master_directory | 🟡 **needs extraction** | 🟡 |
| **Verification Data** | 🟢 in hub_source_list | 🟡 **needs extraction** | 🟡 |
| **Ingestion Code** | 🟢 in master_directory | 🟡 **needs extraction** | 🟡 |

---

## Ready for Worker Dispatch

When you're ready, I can create focused briefs for:
1. `deepseek-worker`: Build ingestion code snippets + legal compliance + update citation templates
2. `yolo-worker`: Extract verification corrections
3. `deepseek-worker`: Update v3 landscape + build Engine B allowlist JSON
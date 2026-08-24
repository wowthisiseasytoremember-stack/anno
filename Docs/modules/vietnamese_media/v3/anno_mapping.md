# Vietnamese Media Module → Anno Features Mapping

**Source:** `vietnamese_media` module (v1-v3: hub_source_list_verified.md, ingestion_code_snippets.md, legal_compliance_rules.md, full_landscape_with_sprints.md)  
**Target:** Anno MVP (`MVP_PLAN_FINAL.md`, `AnnoEntry.swift`, `AGENTS.md`, `CLAUDE.md`)  
**Date:** 2026-08-19

---

## Executive Summary

The vietnamese_media module provides **34 YouTube channels, 13 radio sources, 8 parish livestreams, and institutional sources** — organized into 10 media categories (M1-M10) with verification tiers, legal compliance rules, and ingestion code. This is the **data backbone** for Anno's:
- **Layer 5 (Connections)**: Mass stream links, audio streams
- **Engine B**: Source allowlist for historical research
- **Localization**: Vietnamese Catholic terminology corpus
- **M7 Analytics**: Browser event tracking
- **M9 Directory**: Parish contact data
- **M15 Diocese Partnership**: VCC OC anchor relationship

---

## AnnoEntry.swift Fields → Vietnamese Media Sources

| AnnoEntry Field | Vietnamese Media Source | Integration Point |
|-----------------|------------------------|-------------------|
| `artwork.sourceUrl` | YouTube channel thumbnails, Vatican artwork | Daily artwork showcase (M3) |
| `sources` ([SourceRef]) | All 34 YouTube + 13 radio + 8 parish + institutional | Engine B citation templates |
| `place` (SacredPlace) | Parish locations from M3 (8 OC parishes) | Layer 6 parish spotlights, M9 Directory |
| `connections.massStreams` | VCC OC (8:30am), Christ Cathedral (multiple), Holy Spirit, St. Cecilia, St. John Baptist, St. Polycarp, Blessed Sacrament, St. Bonaventure | Layer 5 "Thánh Lễ trực tuyến hôm nay" |
| `connections.readingsUrl` | Vatican News VI podcast RSS, USCCB VI readings | Layer 5 "Bài Đọc" links |
| `connections.hymnSuggestions` | Thánh Ca Việt Nam (70+ years PDF+MP3), VietCatholic Archive | Layer 5 "Thánh Ca" |
| `connections.pilgrimageLinks` | La Vang Shrine (Christ Cathedral events), Saigon archdiocese streams | Layer 5 + M2 Pilgrimage |

---

## Module M1-M10 → Anno Feature Mapping

### M1: Streaming Video (34 YouTube channels)
| Anno Use | Source | Tier | Notes |
|----------|--------|------|-------|
| **Daily Mass streams (Layer 5)** | VCC OC (@VietCatholicCenter), Christ Cathedral (@DioceseOrange), Holy Spirit, St. Bonaventure, Blessed Sacrament | 1 (verified live) | Embed via iframe; schedule JSON per source |
| **Saint bios / feast content (Engine B)** | Vatican News VI (@VaticanNewsVI), VietCatholicNews (@VietCatholicTV), TGPSG (@tgpsgthanhletructuyen) | 1-4 | Tier 4 = state context badge |
| **Homiletic corpus (Localization)** | All parish channels + VCC OC + Vatican | 1-2 | Extract captions/transcripts for VI terminology |
| **Artwork thumbnails (M3)** | All channels' video thumbnails | 1-2 | YouTube oEmbed API for legal thumbnails |

### M2: Radio/Audio (13 sources)
| Anno Use | Source | Tier | Notes |
|----------|--------|------|-------|
| **Live audio stream (Layer 5)** | RVA (`stream.zeno.fm/edDe0t8E`), Radio MHCG (KALI 106.3) | 1-2 | HTML5 `<audio>` player; test weekly |
| **Daily podcast (Layer 5)** | Vatican News VI podcast RSS (`vietnamese-program.podcast.xml`) | 1 | 25-min daily; fetch via rss2json |
| **Pronunciation reference (Engine B)** | Radio Vatican VI, RVA | 1 | Audio for Vietnamese name pronunciation |
| **Devotional audio (Layer 4/6)** | Divine Mercy (@GiaoDiemTinMungOfficial), Redemptorists | 2-4 | Healing prayers, chaplets |

### M3: Parish Livestreams (8 OC parishes)
| Anno Use | Source | Tier | Notes |
|----------|--------|-------|-------|
| **Local Mass times (Layer 1/5)** | VCC OC (daily 8:30am), Christ Cathedral (multiple), Holy Spirit, St. Cecilia, St. John Baptist, St. Polycarp, Blessed Sacrament, St. Bonaventure | 1-2 | Schedule JSON per parish; verify monthly |
| **Parish directory (M9)** | All 8 + contact info from `directory_westminster_oc.md` | 1-2 | Name, address, phone, email, Mass schedule |
| **Homiletic samples (Engine B)** | Sunday Mass recordings | 1-2 | Vietnamese preaching style for Layer C |

### M4: Official/Institutional (Vatican, RVA, HDGM, Diocese, VCC)
| Anno Use | Source | Tier | Notes |
|----------|--------|-------|-------|
| **Calendar authority (Engine A/B)** | Vatican liturgical calendar, Diocese of Orange calendar, HDGM Vietnam | 1 | Primary source for feast dates, rankings |
| **Papal documents (Layer 6/7)** | Vatican News VI, Vatican podcast | 1 | Encyclicals, audiences, canonizations |
| **Vietnamese liturgical terminology** | All official sources | 1 | Glossary for structural VI localization |

### M5: Diaspora Independent (VietCatholicNews, VietCatholic TV, nguoiviet.tv)
| Anno Use | Source | Tier | Notes |
|----------|--------|-------|-------|
| **Cultural context (Layer 6)** | VietCatholicNews articles, commentary | 2 | Diaspora perspective, La Vang coverage, refugee experience |
| **News aggregation (Layer 5/10)** | VietCatholic TV streaming, nguoiviet.tv embeds | 2 | Event promotion, community announcements |

### M6: General VI Media (KVNR 1480, SBTN, VNA-TV, Saigon TV, VCAL)
| Anno Use | Source | Tier | Notes |
|----------|--------|-------|-------|
| **Broadcast placement (M12/M13)** | KVNR 1480 media kit (no verified Catholic hour) | 3 | Sponsor/underwriter outreach only |
| **Community reach (M9/M10)** | SBTN, VNA-TV, Saigon TV | 3 | Event promotion, directory cross-promo |

### M7: Vietnam-Produced (TGPSG, HDGM Vietnam, Redemptorists VN, Báo Người Công giáo VN)
| Anno Use | Source | Tier | Notes |
|----------|--------|-------|-------|
| **Liturgical reference (Engine B)** | TGPSG daily Mass, HDGM documents | 4 | **State context badge REQUIRED** |
| **Vietnamese practice (Layer 6)** | Redemptorists VN healing prayers, TGPSG devotions | 4 | Cultural reference with disclaimer |

### M8: Films/Archive (Phim Công Giáo, Thánh Ca Việt Nam, VietCatholic Archive, Chan Ly Viet, Dân Chúa USA)
| Anno Use | Source | Tier | Notes |
|----------|--------|-------|-------|
| **Hymn database (Layer 5)** | Thánh Ca Việt Nam (70+ yrs PDF+MP3) | 2 | Sheet music + choral recordings for Layer 5 |
| **Film clips (v2/M3)** | Phim Công Giáo (dubbed Catholic films) | 2 | Licensed clips for premium content |
| **Archival research (Engine B)** | VietCatholic Archive, Chan Ly Viet | 2 | Historical Vietnamese Catholic content |

### M9: Aggregators (nguoiviet.tv, VietCatholic TV streaming)
| Anno Use | Source | Tier | Notes |
|----------|--------|-------|-------|
| **Discovery layer** | nguoiviet.tv embeds KVNR, VNCR, VietCatholic | 2 | Not primary source; mine for channel discovery |

### M10: Orientation (Conciliar vs Traditionalist vs State-affiliated)
| Anno Use | Application |
|----------|-------------|
| **Source badge UI** | Every source in app shows orientation badge (Layer 5, Sources sheet) |
| **Outreach strategy** | Align with conciliar/diaspora (VCC, Vatican, Diocese); cautious with state-affiliated |
| **Partnership prioritization** | VCC OC (anchor), Christ Cathedral (bishop), parishes (Tier 1) → VietCatholicNews → Vatican |

---

## Legal Compliance → Anno Implementation Rules

| Rule | Anno Implementation |
|------|---------------------|
| **Vatican: embed only, no download/rehost** | YouTube iframe embed only; never store MP4; use oEmbed for thumbnails |
| **RVA: stream.zeno.fm/edDe0t8E is live** | Primary audio source; test weekly; Radio Garden backup |
| **Redemptorists: use @dcctsaigon + dongchuacuuthe.us** | Update any legacy `trungtammucvudcct.com` references |
| **Parish schedules: COVID daily → weekend/vigil** | Store schedule as JSON; "Verify Schedule" button; default "Check source" |
| **YouTube embeds: permitted for all verified channels** | Use official iframe embed; YouTube ToS + Vatican sharing tools allow |
| **KVNR 1480: no Catholic hour** | Do not list as Catholic source; keep as broadcast placement only |
| **State-affiliated sources: mandatory badge** | ⚠️ "Produced in Vietnam; state context applies" on TGPSG, HDGM, Redemptorists VN |
| **Exclusion list: no non-Catholic, no secular news** | Filter at ingestion; Catholic-only scope |

---

## Ingestion Code Snippets → Anno Implementation

| Snippet | Anno Integration |
|---------|------------------|
| **4.1 YouTube Embed** | `TodayView` + `Calendar` detail: iframe embed for Mass streams (Layer 5) |
| **4.2 HTML5 Audio Player** | `TodayView`: RVA/Radio MHCG live audio player (Layer 5) |
| **4.3 RSS Feed Ingestion** | `tools/fetch_vatican_podcast.py` → daily podcast MP3 URL for Layer 5 |
| **4.4 Daily Schedule JSON** | `data/liturgical_schedule.json` → routing engine for "Thánh Lễ hôm nay" |
| **4.5 SQLite Schema** | `data/vi_catholic_sources.db` → M9 Directory + Engine B source allowlist |
| **4.6 Seed Data** | Pre-populate database with 34+ verified sources |

---

## Engine B Source Allowlist (from vietnamese_media + research_infrastructure)

| Tier | Publishers | Validation Rule | Anno Integration |
|------|------------|-----------------|------------------|
| **1** | Vatican News VI, Radio Vatican VI, VCC OC | No additional validation | Primary source for universal feasts, papal docs |
| **2** | VietCatholicNews/TV, Parish livestreams (3 confirmed) | `accessed` date within 90 days | Secondary cultural context, local feasts |
| **3** | KVNR 1480, VNCR 106.3 | Explicit `notes` with program + broadcast date | Broadcast placement only |
| **4** | TGPSG, HDGM Vietnam, Redemptorists Vietnam | **Require** "Produced in Vietnam; state context applies" in notes | Reference only with badge |

---

## Vietnamese Localization Corpus (for Layer C / calendar_content Layer 6)

| Corpus Source | Extraction Method | Output |
|---------------|-------------------|--------|
| Vatican News VI podcast transcripts | Download last 90 episodes → Whisper/transcript | `data/corpus/vatican_news_vi/` |
| VietCatholicNews articles | Scrape last 180 days → metadata | `data/corpus/vietcatholic_news/` |
| VCC OC Mass captions | YouTube captions last 30 Masses | `data/corpus/vcc_mass_captions/` |
| **Terminology extraction** | spaCy + custom Catholic lexicon | `tools/extract_vi_terminology.py` |
| **Feast day EN↔VI mapping** | From corpus + official calendar | `data/localization/feast_mapping_vi.json` |

---

## M9 Directory Data (from vietnamese_media M3 + directory_westminster_oc.md)

| Parish | City | Vietnamese Mass | Contact | Tier |
|--------|------|-----------------|---------|------|
| Vietnamese Catholic Center | Santa Ana | Daily 8:30am | (714) 554-4211 | 1 |
| Christ Cathedral | Garden Grove | Sun 6:30/14:00/16:00, Sat 6:30/09:00/18:30, Weekday 17:30 | Diocese Orange | 1 |
| Holy Spirit | Fountain Valley | Weekend/Vigil | `@blessedsacramentcatholicch9746` | 2 |
| St. Cecilia | Tustin | Weekend/Vigil | Parish site | 2 |
| St. John the Baptist | Costa Mesa | Sun 8am (TLM) | Parish site | 2 |
| St. Polycarp | Stanton | Weekend/Vigil | Parish site | 2 |
| Blessed Sacrament | Westminster | Daily 6pm? | `@blessedsacramentcatholicch9746` | 2 |
| St. Bonaventure | Huntington Beach | Archived VODs | `stbonaventure.org/livestream` | 2 |

---

## Sprint Dependencies (from full_landscape_with_sprints.md)

| Sprint | Vietnamese Media Tasks | Anno Dependency |
|--------|------------------------|-----------------|
| **Corpus Build (parallel, no macOS)** | Download Vatican podcast transcripts, scrape VietCatholicNews, extract VCC captions, build terminology pipeline, generate feast mapping | Feeds Engine B, Layer C localization, calendar_content Layer 6 |
| **Outreach Validation (human)** | Contact VCC OC, KVNR media kit, VietCatholicNews media kit, Diocese calendar, survey 3 parish streams | Feeds M15 (diocese), M12/M13 (sponsors), M9 (directory) |
| **Sprint 1-2 (macOS)** | Build `BrowserAnalytics` with source schema, implement YouTube embed + audio player in WKWebView | M7 Analytics, M1/M5 Layer 5 |
| **Sprint 3-4 (phone content)** | Use feast mapping for Jul 3-16 content generation; cite sources per citation templates | calendar_content Layer 3, Engine B |
| **Sprint 5-6** | Wire source database to app; parish directory UI; sponsor outreach with traffic data | M8, M9, M12, M13 |

---

## Summary: What's Ready vs. What Needs App

| **Ready (data/code scaffolding)** | **Needs Anno App Running** |
|-----------------------------------|----------------------------|
| • 34 YouTube channels verified + embed codes | • WKWebView aggregator with iframe embeds |
| • 13 radio sources + stream URLs + HTML5 player | • HTML5 audio player in TodayView |
| • 8 parish livestreams + schedules + contacts | • Parish directory UI (M9) |
| • SQLite schema + seed data for source DB | • Source database query in app |
| • RSS fetch scripts (Vatican podcast) | • Daily podcast link in Layer 5 |
| • Daily schedule JSON for routing | • "Thánh Lễ hôm nay" live routing |
| • Legal compliance rules (hard stops) | • UI badges (state context, orientation) |
| • Engine B source allowlist (4 tiers) | • Citation display in Sources sheet |
| • Localization corpus plan | • Terminology in Layer C generation |
| • Outreach contact list | • Partnership conversations |

---

## Cross-Module Dependencies

| Vietnamese Media Provides | Consumed By Module |
|---------------------------|-------------------|
| Mass stream URLs (Layer 5) | `calendar_content` M1 (Connections layer) |
| Parish data (M9 Directory) | `monetization` M9, M15 (Diocese partnership) |
| Artwork thumbnails | `monetization` M3 (Artwork Multi-Stream) |
| Source citations | `research_infrastructure` (Engine B validation) |
| Vietnamese terminology | `calendar_content` Layer 6 (Culture notes) |
| Audio streams | `calendar_content` Layer 5 (Connections) |
| Hymn database (Thánh Ca) | `calendar_content` Layer 5 (Connections) |
| VCC OC anchor relationship | `monetization` M14 (Grants), M15 (Diocese) |
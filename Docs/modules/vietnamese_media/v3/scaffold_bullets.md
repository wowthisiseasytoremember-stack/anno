# Vietnamese Media Module — Scaffold Bullets for Worker Agent

**Source:** `docs/modules/vietnamese_media/v3/anno_mapping.md`  
**For:** Worker agent reference — what to build, minimal structure

---

## Build-Ready Items (scaffold only, not full implementation)

### 1. Source Database (SQLite) — `data/vi_catholic_sources.db`
- Schema from `ingestion_code_snippets.md` §4.5
- Seed data from §4.6 (34+ verified sources)
- Indexes: category, tier, verification_status, orientation
- Columns: id, name, name_vi, category, tier, platform, platform_handle, stream_url, embed_url, schedule_json, timezone, orientation, state_context_flag, verification_status, last_verified, contact_info, notes

### 2. YouTube Embed Components
- Responsive iframe embed (from §4.1)
- Channel IDs for 8+ verified parishes + Vatican + VietCatholic + TGPSG + Redemptorists
- oEmbed API call for legal thumbnails (no scraping)
- Schedule JSON per source (daily/weekly times)

### 3. HTML5 Audio Player Components
- RVA stream: `https://stream.zeno.fm/edDe0t8E` (primary)
- Radio Garden backup: `radio.garden/listen/radio-veritas-asia/edDe0t8E`
- Radio MHCG: check `dongchuacuuthe.us/radio-mhcg` for current URL
- Vatican News VI podcast: fetch via RSS → MP3 URL (via rss2json API)

### 4. Daily Liturgical Schedule Router
- JSON from §4.4: times → source/platform/handle/location/verified
- Pacific Time schedule: 06:30 (Saigon replay), 08:30 (VCC OC), 12:00 (Vatican), 15:00 (Divine Mercy), 18:00 (Blessed Sacrament), 22:00 (Radio MHCG)
- Vietnam = UTC+7 = +14h from Pacific; use replays for US viewers

### 5. Engine B Source Allowlist (4 Tiers)
- Tier 1: Vatican News VI, Radio Vatican VI, VCC OC (no extra validation)
- Tier 2: VietCatholicNews/TV, 3 confirmed parish livestreams (accessed within 90 days)
- Tier 3: KVNR 1480, VNCR 106.3 (explicit notes with program + broadcast date)
- Tier 4: TGPSG, HDGM Vietnam, Redemptorists Vietnam (MANDATORY "Produced in Vietnam; state context applies" in notes)

### 6. Legal Compliance Enforcement
- Vatican: iframe embed ONLY; no MP4 download/rehost; oEmbed for thumbnails
- RVA: test stream weekly; zeno.fm primary
- Redemptorists: use @dcctsaigon + dongchuacuuthe.us (not lapsed trungtammucvudcct.com)
- Parish schedules: store as JSON; "Verify Schedule" button; default "Check source"
- State-affiliated (tier 4): mandatory badge in UI
- KVNR 1480: do NOT list as Catholic source
- Exclusion list: filter non-Catholic, secular news at ingestion

### 7. Localization Corpus Pipeline
- Download Vatican News VI podcast transcripts (last 90 days) → `data/corpus/vatican_news_vi/`
- Scrape VietCatholicNews articles (last 180 days) → `data/corpus/vietcatholic_news/`
- Extract VCC OC Mass YouTube captions (last 30) → `data/corpus/vcc_mass_captions/`
- Terminology extraction: spaCy + custom Catholic lexicon → `tools/extract_vi_terminology.py`
- Feast day EN↔VI mapping table → `data/localization/feast_mapping_vi.json`
- Source citation templates per outlet type → `docs/research/source_citation_templates.md`

### 8. Parish Directory Data (M9 Foundation)
- 8 OC parishes with: name, city, Vietnamese Mass schedule, contact, tier
- Tier 1: VCC OC, Christ Cathedral
- Tier 2: Holy Spirit, St. Cecilia, St. John Baptist, St. Polycarp, Blessed Sacrament, St. Bonaventure
- Contact info from `directory_westminster_oc.md`

### 9. Orientation Badge System
- Conciliar: "Vatican II / Synodal / Pastoral" (Vatican, RVA, Jesuit, Diocesan)
- Traditionalist: "Diaspora Traditional / Anti-Communist" (VietCatholic, Radio MHCG, CRM, SBTN)
- Neutral: "Devotional / Scriptural" (Daily Gospel apps, Lời Chúa Cho Mọi Người)
- State-affiliated: ⚠️ **"Produced in Vietnam; state context applies"** (TGPSG, HDGM, Redemptorists VN, Báo Người Công giáo VN)

### 10. Verification Maintenance Scripts
- Weekly: test VCC OC livestream page, RVA stream endpoint
- Daily: fetch Vatican News VI podcast RSS
- Monthly: check parish YouTube channels for new uploads
- Monthly: verify TGPSG/HDGM/Redemptorists VN channels active
- Quarterly: check domain expirations (trungtammucvudcct.com lapsed, others)

---

## Dependency Order

```
Source Database (1) ← pure data, no app needed
    ↓
YouTube Embed (2) + Audio Player (3) + Schedule Router (4) ← frontend components
    ↓
Engine B Allowlist (5) + Legal Rules (6) ← validation logic
    ↓
Localization Corpus (7) ← parallel, feeds Engine B + calendar_content
    ↓
Parish Directory (8) + Orientation Badges (9) ← UI components
    ↓
Verification Scripts (10) ← ongoing maintenance
```

**Zero-code prep (do this week):** 
- Test all 34 YouTube embeds manually
- Test RVA audio stream in browser
- Verify 8 parish schedules on their sites
- Contact VCC OC for partnership (human)
- Download Vatican podcast episodes for corpus

---

## Cross-Module Inputs Needed

| Need | From Module |
|------|-------------|
| Calendar dataset (feast dates) | `calendar_content` module |
| Artwork assets for daily showcase | `monetization` M3 |
| Engine B research prompts | `research_infrastructure` v1/engine_b_prompt.md |
| Grant application (CCC) | `monetization` M14 / `calendar_content` v1/calendar_spec_full.md |
| Diocese partnership protocol | `monetization` M15 |
| Sponsor prospectus | `monetization` M12/M13 |
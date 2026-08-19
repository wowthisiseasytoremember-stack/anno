# Source Citation Templates — Vietnamese Catholic Media

**Purpose:** Standardized citation formats for Engine B research output when sourcing from Vietnamese Catholic media outlets.

---

## Citation Schema (Engine B Output)

All Engine B entries must include `sources` array with objects matching:

```json
{
  "type": "primary|secondary|tertiary",
  "title": "Human-readable title",
  "url": "Canonical URL",
  "accessed": "YYYY-MM-DD",
  "publisher": "Outlet name",
  "language": "vi|en",
  "medium": "video|audio|text|livestream",
  "notes": "Optional context (e.g., 'homily at 12:34', 'daily podcast ep 2026-08-15')"
}
```

---

## Per-Outlet Templates

### 1. Vatican News Tiếng Việt (Official Holy See)

| Medium | Template | Example |
|--------|----------|---------|
| **Website Article** | `"publisher": "Vatican News – Tiếng Việt", "medium": "text", "url": "https://www.vaticannews.va/vi/..."` | Pope Francis Angelus address, feast explanation |
| **YouTube Video** | `"publisher": "Vatican News – Tiếng Việt", "medium": "video", "url": "https://youtube.com/watch?v=..."` | Papal audience, catechesis, prayer |
| **Daily Podcast** | `"publisher": "Radio Vatican – Tiếng Việt", "medium": "audio", "url": "https://vaticannews.va/vi/podcast/...", "notes": "Episode YYYY-MM-DD, segment at MM:SS"` | 25-min daily: news, meditation, prayer |
| **Facebook Post** | `"publisher": "Vatican News – Tiếng Việt (Facebook)", "medium": "text", "url": "https://facebook.com/VaticanNewsVI/posts/..."` | Short-form papal quote, graphic |

**Authority:** Primary for universal Church teaching, papal acts, canonizations, liturgical norms.

---

### 2. VietCatholicNews / VietCatholic TV (Diaspora Independent, est. 1996)

| Medium | Template | Example |
|--------|----------|---------|
| **Website Article** | `"publisher": "VietCatholicNews", "medium": "text", "url": "https://vietcatholic.net/..."` | News, "World Seen from Vatican", commentary |
| **YouTube Video** | `"publisher": "VietCatholicNews", "medium": "video", "url": "https://youtube.com/watch?v=..."` | Weekly audience, Sunday Angelus, meditations, sacred music |
| **Streaming TV (VietCatholic TV)** | `"publisher": "VietCatholic TV", "medium": "video", "url": "https://nguoiviet.tv/vietcatholic-news/..."` | Live Mass, special programs |
| **Radio (KVNR "Sống Đức Tin")** | `"publisher": "KVNR 1480 AM – Sống Đức Tin", "medium": "audio", "url": "https://vietcatholiccenter.org/radio-archive/...", "notes": "Broadcast YYYY-MM-DD"` | Weekly faith formation hour |

**Authority:** Secondary — diaspora Church perspective, Vietnamese cultural context, local feast coverage (La Vang, Vietnamese martyrs). Not Magisterial.

---

### 3. Vietnamese Catholic Center – Diocese of Orange (Official Diocesan)

| Medium | Template | Example |
|--------|----------|---------|
| **YouTube Livestream/Recording** | `"publisher": "Vietnamese Catholic Center – Diocese of Orange", "medium": "video", "url": "https://youtube.com/@VietCatholicCenter/...", "notes": "Daily Mass YYYY-MM-DD, homily at HH:MM"` | Daily Mass (8:30 AM PT), Liturgy of Hours |
| **Website Livestream Page** | `"publisher": "Vietnamese Catholic Center – Diocese of Orange", "medium": "video", "url": "https://vietcatholiccenter.org/livestream/"` | Embedded player, prayer intentions |
| **Radio Archive** | `"publisher": "Vietnamese Catholic Center – Diocese of Orange", "medium": "audio", "url": "https://vietcatholiccenter.org/radio-archive/..."` | "Sống Đức Tin" weekly episodes |

**Authority:** Primary for diocesan calendar, local feast observances, Bishop's directives, official Vietnamese liturgical terminology in OC.

---

### 4. Parish Livestreams (Diocese of Orange Parishes)

| Parish | Platform | Template |
|--------|----------|----------|
| **Holy Spirit – Fountain Valley** | Facebook Live | `"publisher": "Holy Spirit Catholic Church – Fountain Valley", "medium": "video", "url": "https://facebook.com/holyspiritfv/videos/...", "notes": "Vietnamese Mass YYYY-MM-DD HH:MM"` |
| **St. Cecilia – Tustin** | Facebook Live | `"publisher": "St. Cecilia Catholic Church – Tustin", "medium": "video", "url": "https://facebook.com/StCeciliaCatholicChurch/videos/...", "notes": "Vietnamese Mass YYYY-MM-DD HH:MM"` |
| **St. John the Baptist – Costa Mesa** | Facebook | `"publisher": "St. John the Baptist Catholic Church – Costa Mesa", "medium": "video", "url": "https://facebook.com/.../videos/...", "notes": "Vietnamese Mass YYYY-MM-DD HH:MM (also TLM)"` |

**Authority:** Tertiary — local pastoral application, homiletic style, congregational Vietnamese usage. Verify each parish's current streaming status.

---

### 5. Radio Vatican Vietnamese (Official Vatican Radio)

| Medium | Template | Example |
|--------|----------|---------|
| **Podcast (Spotify/Apple)** | `"publisher": "Radio Vatican – Tiếng Việt", "medium": "audio", "url": "https://open.spotify.com/episode/...", "notes": "Daily program YYYY-MM-DD, segment: Scripture meditation at MM:SS"` | 25-min daily program |
| **Website** | `"publisher": "Radio Vatican – Tiếng Việt", "medium": "text", "url": "https://vaticannews.va/vi/podcast/vietnamese-program.html"` | Program description, schedule |

**Authority:** Primary — same as Vatican News, audio format.

---

### 6. General Vietnamese Radio (KVNR, VNCR, etc.) — Catholic Blocks Only

| Station | Program | Template |
|---------|---------|----------|
| **KVNR 1480 AM** | "Sống Đức Tin" (Thurs 8-9pm) | `"publisher": "KVNR 1480 AM – Little Saigon Radio", "medium": "audio", "url": "https://littlesaigonradio.com/...", "notes": "Sống Đức Tin YYYY-MM-DD"` |
| **VNCR FM 106.3** | Catholic programming (verify schedule) | `"publisher": "VNCR FM 106.3 – Vietnam California Radio", "medium": "audio", "url": "https://radiovncr.com/...", "notes": "Program name, YYYY-MM-DD"` |

**Authority:** Tertiary — commercial radio carrying Catholic content. Verify Catholic block exists before citing.

---

### 7. Vietnam-Produced Media (Use with Context Caveat)

| Outlet | Context Flag | Template |
|--------|--------------|----------|
| **TGPSG (Archdiocese of Saigon)** | ⚠️ State context — Vietnamese Fatherland Front | `"publisher": "TGPSG – Tổng Giáo phận Sài Gòn", "medium": "video", "url": "https://youtube.com/...", "notes": "Produced in Vietnam; state context applies"` |
| **hdgmvietnam.com (Catholic Bishops' Conference of Vietnam)** | ⚠️ State context | `"publisher": "Hội Đồng Giám Mục Việt Nam", "medium": "text", "url": "https://hdgmvietnam.com/...", "notes": "Official VN bishops' conference; state context applies"` |
| **Redemptorists Vietnam (dcctvn.org)** | ⚠️ State context; progressive voice | `"publisher": "Tỉnh Dòng Chúa Cứu Thế Việt Nam", "medium": "text|video", "url": "https://dcctvn.org/...", "notes": "Produced in Vietnam; state context applies"` |

**Rule:** Always include `"notes": "Produced in Vietnam; state context applies"` when citing these sources. Do not present as independent diaspora voice.

---

## Engine B Prompt Integration

Add to `docs/research/anno-research-prompt-main.md` source allowlist:

```markdown
## Vietnamese Catholic Source Allowlist (Tiered)

### Tier 1 — Primary (Magisterial / Official Diocesan)
- Vatican News – Tiếng Việt (website, YouTube, podcast, Facebook)
- Radio Vatican – Tiếng Việt (podcast, website)
- Vietnamese Catholic Center – Diocese of Orange (YouTube, website, radio archive)

### Tier 2 — Secondary (Diaspora Independent, Established)
- VietCatholicNews / VietCatholic TV (website, YouTube, streaming TV, radio archive)
- Parish livestreams: Holy Spirit FV, St. Cecilia Tustin, St. John the Baptist CM (Facebook)

### Tier 3 — Tertiary (Local Pastoral / Commercial Radio Catholic Blocks)
- KVNR 1480 AM "Sống Đức Tin" (radio archive via VCC)
- VNCR FM 106.3 (verify Catholic programming schedule per episode)

### Tier 4 — Context-Required (Vietnam-Produced)
- TGPSG (Saigon Archdiocese) — FLAG: state context
- HDGM Vietnam (Bishops' Conference) — FLAG: state context
- Redemptorists Vietnam — FLAG: state context
- **NEVER cite:** Unaffiliated "THÁNH LỄ TRỰC TUYẾN" channel (ownership unclear)
```

---

## Validation Gate Updates

Update `tools/validate_engine_b_output.py` to recognize these publishers and enforce:

1. **Tier 1 sources:** No additional validation needed
2. **Tier 2 sources:** Require `accessed` date within 90 days for time-sensitive content
3. **Tier 3 sources:** Require explicit `notes` field with program name + broadcast date
4. **Tier 4 sources:** Require `notes` field containing "Produced in Vietnam; state context applies" — **reject if missing**

---

## Quick Reference Card

| Publisher Short Name | Full Name for Citation | Tier | Language | Medium |
|---------------------|------------------------|------|----------|--------|
| `vatican_news_vi` | Vatican News – Tiếng Việt | 1 | vi | text, video, audio |
| `radio_vatican_vi` | Radio Vatican – Tiếng Việt | 1 | vi | audio, text |
| `vcc_oc` | Vietnamese Catholic Center – Diocese of Orange | 1 | vi | video, audio |
| `vietcatholic` | VietCatholicNews / VietCatholic TV | 2 | vi, en | text, video, audio |
| `holy_spirit_fv` | Holy Spirit Catholic Church – Fountain Valley | 3 | vi, en | video |
| `st_cecilia_tustin` | St. Cecilia Catholic Church – Tustin | 3 | vi, en, es | video |
| `st_john_baptist_cm` | St. John the Baptist – Costa Mesa | 3 | vi, en, es, la | video |
| `kvnr_1480` | KVNR 1480 AM – Little Saigon Radio | 3 | vi | audio |
| `vncr_1063` | VNCR FM 106.3 – Vietnam California Radio | 3 | vi | audio |
| `tgpsg_saigon` | TGPSG – Tổng Giáo phận Sài Gòn | 4* | vi | video |
| `hdgm_vietnam` | Hội Đồng Giám Mục Việt Nam | 4* | vi | text |
| `redemptorists_vn` | Tỉnh Dòng Chúa Cứu Thế Việt Nam | 4* | vi | text, video |

*Tier 4 = requires state context flag in notes
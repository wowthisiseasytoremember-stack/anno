# Legal & Technical Compliance Rules — Vietnamese Catholic Media Hub

**Extracted from:** `master_directory_technical.md` §2 + `hub_source_list_verified.md` §C  
**Purpose:** Hard constraints for hub development — violation risks legal action or platform bans

---

## 1. Vatican Media Copyright (CRITICAL)

**Official Policy (Dicastery for Communication):**
> *"Những hình ảnh được đăng trên kênh này là sản phẩm của Bộ Truyền Thông hoặc thuộc quyền sở hữu của Bộ này; mọi hình thức sử dụng bởi bên thứ ba đều bị nghiêm cấm, trừ khi được cấp phép rõ ràng bằng văn bản."*

**Translation:** "Images/videos posted on this channel are products of the Dicastery for Communication or owned by it; any form of use by third parties is strictly prohibited, unless explicitly permitted in writing."

**Hub Rules:**
| Action | Permitted? | Notes |
|--------|------------|-------|
| Embed official YouTube player via iframe | ✅ **YES** | YouTube ToS permits embeds; Vatican sharing tools allow it |
| Link to `vaticannews.va/vi` articles | ✅ **YES** | Standard web linking |
| Use RSS podcast feed (`vietnamese-program.podcast.xml`) | ✅ **YES** | Public RSS feed for podcast apps |
| Download MP4 video files | ❌ **NO** | Requires written consent from `tiengviet@vaticannews.va` |
| Rehost MP4 on your CDN/server | ❌ **NO** | Strictly prohibited |
| Scrape/rip video content | ❌ **NO** | Violates copyright + YouTube ToS |
| Use video thumbnails without permission | ⚠️ **CAUTION** | Better to use YouTube's oEmbed API for thumbnails |

**Contact for Permission:** `tiengviet@vaticannews.va` (Vietnamese desk, Dicastery for Communication)

---

## 2. Radio Veritas Asia (RVA) Status Clarification

**Common Misconception:** "RVA is offline"  
**Reality:** Shortwave radio towers decommissioned. **Digital stream is 100% active.**

**Active Endpoints (Verified 2026-08-19):**
| Endpoint | Type | Status |
|----------|------|--------|
| `https://vietnamese.rvasia.org` | Website + HLS stream | ✅ Live |
| `https://stream.zeno.fm/edDe0t8E` | Direct MP3/HLS stream | ✅ Live |
| `radio.garden/listen/radio-veritas-asia/edDe0t8E` | Radio Garden embed | ✅ Live |
| Mobile app `org.rvasia.app` | iOS/Android | ✅ Live |
| `rveritas-asia.org` podcast RSS | Historical feed | 🔴 **Fetch failed** — Wayback only |

**Hub Rule:** Use `https://stream.zeno.fm/edDe0t8E` as primary audio source. Test weekly.

---

## 3. Redemptorist Domain Migration

**Legacy Domain:** `trungtammucvudcct.com` — **LAPSED/EXPIRED**

**Active Channels (Verified 2026-08-19):**
| Platform | Handle/URL | Content |
|----------|------------|---------|
| YouTube | `@dcctsaigon` (Đền Đức Mẹ Hằng Cứu Giúp Sài Gòn) | Daily Mass, devotions, healing prayers |
| Website | `dongchuacuuthe.us` | Radio MHCG stream, overseas base |
| YouTube (Overseas) | `@GiaoDiemTinMungOfficial` | Nightly broadcast, Divine Mercy |

**Hub Rule:** Update any hardcoded references to `trungtammucvudcct.com` → `@dcctsaigon` + `dongchuacuuthe.us`

---

## 4. Parish Livestream Cadence Shift

**Pattern Observed:** COVID-era daily livestreams → **Weekend/Vigil focus**

**Verification Required Before Hardcoding:**
| Parish | Prior (COVID) | Current (2025-26) | Verify Before Use |
|--------|---------------|-------------------|-------------------|
| Holy Spirit FV | Daily | Weekend/Vigil | Check `@blessedsacramentcatholicch9746` |
| St. Cecilia Tustin | Daily | Weekend/Vigil | Check parish site |
| St. John Baptist CM | Daily | Weekend/Vigil (+ TLM) | Check parish site |
| St. Polycarp Stanton | Daily | Weekend/Vigil | Check parish site |
| Blessed Sacrament Westminster | Daily | Daily 6pm? | Check `@blessedsacramentcatholicch9746` |
| Christ Cathedral | Multiple daily | Multiple weekly | ✅ Verified 2026 schedule |
| VCC OC | Daily 8:30am | Daily 8:30am | ✅ Verified 2026-08-18 |

**Hub Rule:** Store schedule as JSON per source; provide "Verify Schedule" button in admin; default to "Check source for current times" in UI.

---

## 5. YouTube Embed Permissions (Clarification)

**From `hub_source_list_verified.md` §C.6:**
> **"Do not embed Vatican YouTube videos" — ⚠️ overcautious/wrong: embedding the official YouTube player is permitted (Vatican terms allow sharing via provided tools; YouTube ToS allows embeds). The restriction applies to downloading, re-hosting, or re-publishing content without DPC written permission.**

**Hub Rule:** Embedding official YouTube channels via iframe is **permitted and recommended**. This applies to ALL verified channels (Vatican, VCC OC, Christ Cathedral, parishes, VietCatholic, RVA, TGPSG, Redemptorists).

---

## 6. KVNR 1480 — No Verified Catholic Hour

**From `hub_source_list_verified.md` §C.1:**
> **"KVNR 1480 'carries Catholic program Sống Đức Tin Thursdays 8–9 PM' — ❌ unverified; searching it surfaces Protestant programming (e.g., 'Đài Nguồn Sống,' evangelical) — likely category confusion, and Tin Lành content is out of scope anyway."**

**Hub Rule:** KVNR 1480 = **General Vietnamese station, no verified Catholic block**. Do not list as Catholic source. Keep as "placement candidate" for future broadcast buy only.

---

## 7. Rejected/Corrected Claims (Do Not Import)

| Claim | Correction | Source |
|-------|------------|--------|
| Our Lady of the Pillar, Riverside — daily 5pm VI Mass | ❌ Parish is in St. Louis, MO | `hub_source_list_verified.md` §C.2 |
| TGPSG channel ID `UCc7qu2cB-CzTt8CpWqLba-g` | ❌ Unconfirmed; use `@tgpsgthanhletructuyen` | §C.3 |
| `youtube.com/c/rvaviet` for RVA | ❌ Unconfirmed; verified `@daichanlyachau` (UCfEEKI87bNDZkqWPSh5OkLQ) | §C.4 |
| `rveritas-asia.org` podcast RSS (481 episodes) | 🔴 Feed fetch failed; Wayback only | §C.5 |
| St. Cecilia/St. John/Holy Spirit "✅ VERIFIED" | 🟡 Inflated — based on 2020 listings | §C.7 |
| "[Live] Vietnamese Masses" playlist `PLOwY8rPOM7mXim3EUZJgdNCdG48NXG7cu` | ⚪ Not verified this pass; mine for channels if loads | §C.8 |
| "THÁNH LỄ TRỰC TUYẾN" unaffiliated channel | ⚠️ Ownership unclear; exclude until identified | §C.9 |

---

## 8. Political Orientation Disclosure (UI Requirement)

**From `directory_outreach.md` §9 + `directory_westminster_oc.md`:**

| Orientation | Badge Text | When to Show |
|-------------|------------|--------------|
| `conciliar` | "Vatican II / Synodal / Pastoral" | Vatican News, RVA, Jesuit Media, Diocesan |
| `traditionalist` | "Diaspora Traditional / Anti-Communist" | VietCatholic, Radio MHCG, CRM, SBTN |
| `neutral` | "Devotional / Scriptural" | Daily Gospel apps, Lời Chúa Cho Mọi Người |
| `state_affiliated` | ⚠️ **"Produced in Vietnam; state context applies"** | TGPSG, HDGM Vietnam, Redemptorists VN, Báo Người Công giáo VN |

**UI Rule:** Any source with `state_context_flag = 1` MUST display the warning badge prominently. Never present as independent diaspora voice.

---

## 9. Exclusion List (Scope Boundaries)

**From `directory_outreach.md` §10 — Do Not Include in Hub:**

| Category | Examples | Reason |
|----------|----------|--------|
| Non-Catholic Christian | Tin Lành TV, "Giảng Luận Kinh Thánh", evangelical YouTube | Catholic-only scope |
| Other Religions | Phật Giáo TV, Cao Đài TV | Out of scope |
| General Secular VI Media | Người Việt Daily News, SBTN, Saigon TV, VNA-TV | Only as broadcast-placement context |
| EWTN | No VI programming (EN/ES only) | Verified 2026-08-18 |
| Secular News | Radio Free Asia, BBC Vietnamese | Journalism, not Catholic outlet |

---

## 10. Verification Log Standard (For Ongoing Maintenance)

**From `directory_outreach.md` §11:**

| Check | Frequency | Method |
|-------|-----------|--------|
| VCC OC livestream page | Weekly | Fetch `vietcatholiccenter.org/home/livestream` |
| RVA stream endpoint | Weekly | Test `https://stream.zeno.fm/edDe0t8E` |
| Vatican News VI podcast | Daily | Fetch RSS `vietnamese-program.podcast.xml` |
| Parish YouTube channels | Monthly | Check for new uploads |
| TGPSG/HDGM/Redemptorists VN | Monthly | Verify channels active; note state context |
| Domain expirations | Quarterly | Check `trungtammucvudcct.com` (lapsed), others |

---

## Summary: Hard Stops for Hub Development

| Rule | Violation Consequence |
|------|----------------------|
| No Vatican MP4 download/rehost | Legal action from Holy See Dicastery |
| No KVNR Catholic hour listing | Misinformation; loss of credibility |
| No state-affiliated content without badge | Misleading diaspora audience; trust violation |
| No unverified parish schedules | Users show up to empty church; trust loss |
| No `trungtammucvudcct.com` references | Broken links; outdated info |
| No RVA "offline" claims | Factually wrong; misses live stream |

---

**Last Verified:** 2026-08-19  
**Next Audit Due:** 2026-09-19 (monthly for streams, quarterly for domains)
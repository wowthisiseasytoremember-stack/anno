# Verification Corrections — Rejected & Corrected Claims

**Extracted from:** `hub_source_list_verified.md` §C (Corrections to reviewed document)  
**Purpose:** Single source of truth for what NOT to import and what to correct

---

## A. REJECTED — Do Not Import These Claims

| # | Prior Claim | Correction | Evidence | Action |
|---|-------------|------------|----------|--------|
| **1** | KVNR 1480 AM carries Catholic program "Sống Đức Tin" Thursdays 8–9 PM | ❌ **UNVERIFIED / LIKELY FALSE** — Search surfaces Protestant "Đài Nguồn Sống" (evangelical). Category confusion. Tin Lành content is out of scope. | `hub_source_list_verified.md` §C.1 | **Remove KVNR from Catholic sources.** Keep as "general station, placement candidate only." |
| **2** | Our Lady of the Pillar, Riverside — daily 5 PM Vietnamese Mass | ❌ **WRONG PARISH** — Resolvable parish of that name is in **St. Louis, MO**. No such parish in Riverside with daily VI Mass. | §C.2 | **Drop entirely.** |
| **3** | TGPSG channel ID `UCc7qu2cB-CzTt8CpWqLba-g` | ❌ **UNCONFIRMED** — Use verified handle **`@tgpsgthanhletructuyen`** (from bishops' conference directory). | §C.3 | **Update TGPSG handle.** |
| **4** | `youtube.com/c/rvaviet` for Đài Chân Lý Á Châu (RVA) | ❌ **UNCONFIRMED** — Verified channel is **`@daichanlyachau`** (UCfEEKI87bNDZkqWPSh5OkLQ). | §C.4 | **Update RVA handle.** |
| **5** | `rveritas-asia.org` podcast RSS (481 episodes) | 🔴 **FETCH FAILED** 2026-08-19 — Wayback Machine only historical asset. Feed dead. | §C.5 | **Mark RSS as dead.** Use `vietnamese.rvasia.org` website stream instead. |
| **6** | "Do not embed Vatican YouTube videos" | ⚠️ **OVERCAUTIOUS / WRONG** — Embedding official YouTube player IS permitted (Vatican terms allow sharing via provided tools; YouTube ToS allows embeds). Restriction is on **downloading/rehosting/republishing** without DPC written permission. | §C.6 | **Allow Vatican YouTube embeds.** Update any "no embed" rules. |
| **7** | St. Cecilia, St. John the Baptist, Holy Spirit — "✅ VERIFIED" | 🟡 **VERIFICATION INFLATION** — Based on 2020-era diocesan listings. Current 2025-26 schedules differ. This file's 🟡 flags and updated times supersede. | §C.7 | **Downgrade to 🟡 LISTED/UNCONFIRMED.** Re-verify before citing air times. |
| **8** | "[Live] Vietnamese Masses" YouTube playlist `PLOwY8rPOM7mXim3EUZJgdNCdG48NXG7cu` | ⚪ **NOT VERIFIED THIS PASS** — If it loads, mine for additional channels rather than linking playlist directly. | §C.8 | **Don't link playlist.** Extract channel IDs if accessible. |
| **9** | "THÁNH LỄ TRỰC TUYẾN" unaffiliated channel | ⚠️ **OWNERSHIP UNCLEAR** — Correctly self-flagged by reviewed doc. Exclude until ownership identified. | §C.9 | **Exclude from hub.** |

---

## B. ENRICHMENTS — Adopt These Updates (with Flags)

| # | Source | Enrichment | Flag | Source |
|---|--------|------------|------|--------|
| **1** | Vietnamese Catholic Center (VCC OC) | Phone: **(714) 554-4211**<br>Chapel capacity: ~200<br>Served: ~83,000 VI Catholics in diocese<br>Legacy domain: `vncatholic.net` (unverified) | ⚠️ **Confirm before publishing** | §B.1 |
| **2** | St. Barbara, Santa Ana | Large VI community<br>Email: `info@st-barbarachurch.org`<br>Phone: (714) 775-7733<br>Links to VietCatholic resources (no own streams) | 🟡 **Confirm contact details** | §B.2 |
| **3** | St. Bonaventure, Huntington Beach | Livestream hub: `stbonaventure.org/livestream` → parish YouTube with **archived Masses** | ✅ High value — archive depth | §B.3 |
| **4** | Diocese of Orange Vimeo | `vimeo.com/rcbo` — reportedly includes VI synod/formation videos | 🔍 **Manual sweep needed** for VI content | §B.4 |
| **5** | Radio Veritas Asia Access Paths | Radio Garden: `radio.garden/listen/radio-veritas-asia/edDe0t8E`<br>myTuner Radio app also carries stream | ✅ **Test before publishing** | §B.5 |
| **6** | TNTT/VEYM Nodes (Outreach Partners) | Liên Đoàn Nguồn Sống: `tnttldns.org` (14 chapters in Diocese of Orange)<br>National VEYM Facebook | 📢 **Promotion channels** for hub | §B.6 |
| **7** | Localization Candidate: "Magnifica Humanitas" | Pope Leo XIV's first encyclical (signed May 15, 2026; released May 25, 2026) — safeguarding human person in AI age.<br>**Check `vaticannews.va/vi` for VI translation first** (VI desk typically translates major docs).<br>`vatican.va` text is DPC-copyright — **link, don't rehost**. | 🎯 **High-value localization target** | §B.7 |

---

## C. VERIFICATION TIER DEFINITIONS (From Source List)

| Tier | Label | Criteria | Examples |
|------|-------|----------|----------|
| **Group 1** | ✅ **VERIFIED LIVE** | Content page/stream/channel fetched or confirmed posting current content on 2026-08-18/19 | VCC OC, Christ Cathedral, Radio MHCG, RVA, Vatican News VI, VietCatholic News, Holy Spirit FV, Đức Mẹ La Vang |
| **Group 2** | 🟡 **LISTED / UNCONFIRMED TODAY** | Exists and confirmed via official/recent (2025–mid-2026) listings; stream not re-fetched today; links presumed good | St. Cecilia, St. John Baptist, St. Polycarp, St. Barbara, Blessed Sacrament (some), TGPSG, HDGM, Redemptorists VN |
| **Group 3** | 🔴 **OFFLINE / BROKEN** | Found but failing now | `conggiao24h.com` (404), `rveritas-asia.org` RSS, `trungtammucvudcct.com` (lapsed) |
| **Group 3** | ⚪ **HISTORICAL / ARCHIVE** | No longer airing but accessible | `chanlyviet.org` (1996-2019), `danchuausa.net` (1980s-2010s) |

---

## D. CATEGORY TAGS (For Engine B Source Allowlist)

| Tag | Meaning | Examples |
|-----|---------|----------|
| **[A]** | Mainstream Catholic content **dubbed/subtitled in Vietnamese** (papal/Vatican with VI dubbing) | Vatican News VI, RVA (some) |
| **[B1]** | **Vietnamese-produced** Catholic content (VI parishes, clergy, orgs) | VCC OC, Christ Cathedral, Holy Spirit, VietCatholic, parishes |
| **[B2]** | VI-language Catholic content by **international Catholic orgs' VI services** | RVA, Vatican News VI (original VI production) |
| **[C]** | **Localization candidate** — significant free/openly-licensed Catholic content *not* in VI that hub could link/host/subtitle/dub | "Magnifica Humanitas" encyclical, EWTN content (if VI added), English Catholic films |

---

## E. STATUS CHANGES LOG

| Date | Source | Old Status | New Status | Reason |
|------|--------|------------|------------|--------|
| 2026-08-19 | KVNR 1480 Catholic hour | Assumed ✅ | ❌ Rejected | Protestant confusion |
| 2026-08-19 | Our Lady of Pillar Riverside | Assumed ✅ | ❌ Rejected | Wrong parish (St. Louis) |
| 2026-08-19 | TGPSG channel ID | `UCc7qu2cB...` | `@tgpsgthanhletructuyen` | Bishops' conference directory |
| 2026-08-19 | RVA YouTube | `youtube.com/c/rvaviet` | `@daichanlyachau` | Verified handle |
| 2026-08-19 | RVA podcast RSS | Assumed live | 🔴 Dead | Fetch failed; Wayback only |
| 2026-08-19 | Vatican YouTube embed | "Don't embed" | ✅ Embed permitted | YouTube ToS + Vatican sharing tools |
| 2026-08-19 | St. Cecilia/St. John/Holy Spirit | ✅ Verified | 🟡 Listed/Unconfirmed | 2020-era listings; schedules shifted |
| 2026-08-19 | Redemptorist domain | `trungtammucvudcct.com` | `@dcctsaigon` + `dongchuacuuthe.us` | Domain lapsed; migration complete |

---

## F. QUICK REFERENCE: CORRECTED HANDLES/IDs

| Source | **Corrected** Handle/ID | Platform |
|--------|------------------------|----------|
| Vatican News VI | `@VaticanNewsVI` / `@VaticanNewsTiengViet` | YouTube |
| Radio Veritas Asia | `@daichanlyachau` (UCfEEKI87bNDZkqWPSh5OkLQ) | YouTube |
| TGPSG (Saigon Archdiocese) | `@tgpsgthanhletructuyen` | YouTube |
| Redemptorists Vietnam | `@dcctsaigon` (Đền Đức Mẹ Hằng Cứu Giúp Sài Gòn) | YouTube |
| Redemptorists Overseas | `@GiaoDiemTinMungOfficial` | YouTube |
| VCC OC | `@VietCatholicCenter` (UC1HuzI97H8M5bI3Wl6wKdvA) | YouTube |
| Christ Cathedral / Diocese | `@DioceseOrange` | YouTube |
| Holy Spirit FV | `@blessedsacramentcatholicch9746` | YouTube |
| VietCatholic News/TV | `@VietCatholicTV` | YouTube / `vietcatholic.net` |

---

## G. IMPLEMENTATION CHECKLIST

- [ ] Remove KVNR 1480 from Catholic source list
- [ ] Remove Our Lady of the Pillar Riverside
- [ ] Update TGPSG handle to `@tgpsgthanhletructuyen`
- [ ] Update RVA handle to `@daichanlyachau`
- [ ] Mark RVA podcast RSS as dead; use website stream
- [ ] Allow Vatican YouTube embeds in hub
- [ ] Downgrade St. Cecilia, St. John Baptist, Holy Spirit to 🟡
- [ ] Exclude "THÁNH LỄ TRỰC TUYẾN" channel
- [ ] Update Redemptorist references to `@dcctsaigon` / `dongchuacuuthe.us`
- [ ] Add VCC OC phone/capacity/served numbers (with confirm flag)
- [ ] Add St. Barbara contact info (with confirm flag)
- [ ] Add St. Bonaventure archive note
- [ ] Add Diocese of Orange Vimeo sweep task
- [ ] Add Radio Garden/myTuner as RVA backups
- [ ] Add TNTT/VEYM as outreach partners
- [ ] Add "Magnifica Humanitas" localization candidate task
- [ ] Update Engine B source allowlist with corrected handles + tags [A]/[B1]/[B2]/[C]
- [ ] Update citation templates with corrected channel IDs
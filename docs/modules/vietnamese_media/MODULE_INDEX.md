# Vietnamese Media Module — Versioned Index

**Purpose:** Source classification for Engine B research — 10 media categories (M1-M10).

---

## Versioned Files

| Version | File | Description |
|---------|------|-------------|
| **v1** | `source_research_dump.md` | Raw operator research dump (paste-2026-08-19-072712) — original M1-M10 |
| **v1** | `module_index.md` | First decomposition: 10 modules (streaming, radio, parish, official, diaspora, general, Vietnam-flagged, films, aggregators, orientation) |
| **v1** | `directory_westminster_oc.md` | **NEW** Full Westminster/OC directory + ideological landscape (Conciliar vs Traditionalist) |
| **v1** | `master_directory_technical.md` | **NEW** Technical ingestion architecture + legal flags + code snippets |
| **v1** | `hub_source_list_verified.md` | **NEW** Verification-tiered source list (Group 1/2/3) with category tags [A]/[B1]/[B2]/[C] |
| **v1** | `directory_outreach.md` | **NEW** Outreach/marketing directory + political orientation + top 10 priorities |
| **v2** | `citation_templates.md` | Per-outlet Engine B citation formats (12 publishers, 4 tiers) — **NEEDS UPDATE** with new handles/URLs |
| **v2** | `ingestion_code_snippets.md` | **NEW** HTML/JS/Node.js templates for YouTube embed, audio streams, RSS parsing, schedule routing |
| **v2** | `legal_compliance_rules.md` | **NEW** Vatican copyright, RVA status, Redemptorist migration, parish cadence, embed permissions |
| **v2** | `verification_corrections.md` | **NEW** 9 rejected claims, 7 enrichments, corrected handles, status change log |
| **v3** | `full_landscape_with_sprints.md` | Full decomposition with sprints, partnership tracker, source allowlist — **NEEDS UPDATE** |

---

## Module Quick Reference (M1-M10)

| Code | Module | Key Sources | Verification | Anno Use |
|------|--------|-------------|--------------|----------|
| **M1** | Streaming Video | 34 YouTube channels (Vatican, VCC OC, Christ Cathedral, Holy Spirit, VietCatholic, TGPSG, Redemptorists, parishes) | 15 ✅ Live, 10 🟡 Listed | Engine B allowlist; content calendar |
| **M2** | Radio/Audio | 13 sources (RVA, Radio MHCG, Vatican podcast, KVNR rejected, Radio Garden, myTuner) | 8 ✅ Live, 2 🟡 Listed | Audio pipeline (v2); pronunciation ref |
| **M3** | Parish Livestreams | 8 OC parishes (VCC OC, Christ Cathedral, Holy Spirit, St. Cecilia, St. John Baptist, St. Polycarp, Blessed Sacrament, St. Bonaventure) | 3 ✅ Live, 5 🟡 Listed | Local calendar verification; homiletic corpus |
| **M4** | Official/Institutional | Vatican News VI, RVA, HDGM Vietnam, Diocese of Orange, VCC OC | ✅ Verified | Primary source tier; calendar authority |
| **M5** | Diaspora Independent | VietCatholic News (1996, 724K subs), VietCatholic TV, nguoiviet.tv | ✅ Verified | Secondary tier; cultural context |
| **M6** | General VI Media | KVNR 1480 (❌ no Catholic hour), SBTN, VNA-TV, Saigon TV, VCAL | ⚠️ Placement only | Tertiary outreach; verify Catholic blocks |
| **M7** | Vietnam-Produced | TGPSG (@tgpsgthanhletructuyen), HDGM Vietnam, Redemptorists VN (@dcctsaigon), Báo Người Công giáo VN | ✅ Verified **+ State context flag** | **Flag required**; not for outreach |
| **M8** | Films/Archive | Phim Công Giáo (phimconggiao.net), Thánh Ca Việt Nam (70+ yrs, PDF+MP3), VietCatholic Archive, Chan Ly Viet, Dân Chúa USA | ✅ Verified | Cultural ref; licensed clips (v2) |
| **M9** | Aggregators | nguoiviet.tv (embeds KVNR, VNCR, VietCatholic), VietCatholic TV streaming | ✅ Verified | Discovery layer; not primary |
| **M10** | Orientation | **Conciliar/Progressive** (Vatican, RVA, Jesuits, Diocesan) vs **Traditionalist** (VietCatholic, Radio MHCG, CRM, SBTN) vs **State-affiliated** (TGPSG, HDGM, Redemptorists VN) | Analysis complete | Outreach strategy; partnership alignment |

---

## Entry Points for Workers

| Task | Worker Type | Input Files |
|------|-------------|-------------|
| Build Engine B source allowlist JSON | `deepseek-worker` | v1/hub_source_list_verified.md (Group 1), v2/citation_templates.md, v2/verification_corrections.md |
| Generate citation validator rules | `deepseek-worker` | v2/citation_templates.md (needs update with new handles) |
| Create partnership outreach tracker | `yolo-worker` | v1/directory_outreach.md (top 10), v3/full_landscape_with_sprints.md |
| Build ingestion frontend components | `deepseek-worker` | v2/ingestion_code_snippets.md (YouTube embed, audio player, RSS parser, schedule) |
| Legal compliance audit | `deepseek-worker` | v2/legal_compliance_rules.md (Vatican copyright, RVA, Redemptorist, parish cadence) |
| Apply verification corrections | `yolo-worker` | v2/verification_corrections.md (9 rejections, 7 enrichments, handle updates) |
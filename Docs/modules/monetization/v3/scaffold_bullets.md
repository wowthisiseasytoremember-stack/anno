# Monetization Module — Scaffold Bullets for Worker Agent

**Source:** `docs/modules/monetization/v3/anno_mapping.md`  
**For:** Worker agent reference — what to build, minimal structure

---

## Build-Ready Items (scaffold only, not full implementation)

### 1. BrowserAnalytics Service (M7) — ONLY ichabod-doable prototype
- Python/Node service: ingest anonymized browser events → aggregate → quarterly reports
- Schema: `event_type` (page_view, link_click, mass_stream_start, artwork_download), `content_id`, `timestamp`, `device_class`, `geo_diocese` (no PII)
- Aggregation: daily/weekly/monthly totals; top content; peak hours; source popularity; feast engagement
- Output: quarterly JSON report + markdown summary for diocese/publishers/tour operators
- CLI: `python browser_analytics.py --input events.jsonl --quarter Q3-2026 --output reports/`
- Test with mock data from `vietnamese_media` source list

### 2. AnnoEntry.swift Extensions for Monetization (M1, M3, M8)
- Add `downloadUrl`, `purchaseUrl`, `price` to `ArtworkCandidate` (M3 commerce)
- Add `affiliateLinks: [AffiliateLink]?` to `PrimaryContent` or `Connections` (M5)
- Add `sponsorAcknowledgment: String?` to `AnnoEntry` (M12/M13 static placement)
- Add `isPremiumContent: Bool` flag (M8 gate) — true for Layers 3-7
- Define `AffiliateLink` struct: `label`, `url`, `program` (amazon/ignatius/tan/catholic_company)
- Define `SponsorPlacement` struct: `season`, `underwriterName`, `acknowledgmentText`, `placement` (header/footer/inline)

### 3. StoreKit 2 Subscription Infrastructure (M8)
- `RevenueCat` or native StoreKit 2: `SubscriptionManager` class
- Products: `anno_premium_monthly` ($2.99), `anno_premium_yearly` ($19.99) — "$1/mo" framing
- Entitlements: `premium_calendar`, `unlimited_bookmarks`, `push_notifications`, `offline_reading`, `custom_alerts`, `ad_free`
- Feature gating: `PremiumGate` environment value / view modifier
- Restore purchases, subscription status sync, server receipt validation (optional)

### 4. Parish CRM (M1, M15) — Data Only
- CSV/JSON: 16 Diocese of Orange parishes + 40-60 national targets
- Fields: `name`, `city`, `state`, `vietnamese_mass_schedule`, `contact_pastor`, `contact_council`, `warm_intro_source`, `tier` (1/2/3), `status` (cold/contacted/demo_sent/negotiating/closed), `units_ordered`, `notes`
- Tier 1: VCC OC, Our Lady of La Vang, Blessed Sacrament, St. Barbara
- Filter views: by tier, by status, by diocese

### 5. Content Production Tracker (M1) — Shared with calendar_content
- 460-row Kanban (see calendar_content scaffold)
- Add monetization columns: `parish_license_potential`, `artwork_asset_id`, `affiliate_opportunities`, `sponsor_season`

### 6. Grant Application Boilerplate (M14)
- Template from `calendar_content/v1/calendar_spec_full.md` CCC draft
- Sections: Executive Summary, Statement of Need, Project Description, Target Audience, Budget, Sustainability, Evaluation, Organizational Capacity, Timeline
- Variable brackets: `[PROJECT_NAME]`, `[YOUR_NAME]`, `[DIOCESE]`, `[VCC_LETTER]`, `[BUDGET_FIGURES]`
- Multi-grant reuse: same narrative → CCC, KofC, CCFOC, OCCF, CA Humanities

### 7. Sponsor/Underwriter Prospectus (M12/M13)
- 1-page bilingual (VI/EN): Hub description, audience demographics, season calendar, sponsorship tiers
- Seasons: Advent, Christmas, Lent, Triduum, Easter, Pentecost, Ordinary Time (5-6/yr)
- Tiers: Season sponsor $200-500 (static acknowledgment), Underwriter $100-250/mo (rotating quarterly)
- Deliverable: PDF + editable markdown

### 8. Tour Referral Outreach (M6)
- Email template + 1-pager PDF for 206 Tours, Tekton Ministries, Unitours, VI-specific operators
- Value prop: "Your tours listed in our Vietnamese Catholic pilgrimage routes → qualified referrals"
- Commission: 3-5% of $3-8K tours; track via UTM parameters

### 9. Affiliate Link Injection (M5)
- Content render hook: after saint bio / feast context, inject relevant affiliate links
- Categories: pilgrimage → travel; saints → books; rosary → items; seasons → devotional items
- Programs: Amazon Associates, Ignatius Press, TAN Books, Catholic Company, Aquinas & More
- Disclosure: "We may earn a commission" — culturally appropriate phrasing

### 10. Prayer Intention Board Foundation (M11)
- Extend `Bookmark.swift` → `Intention` model: `text`, `isPublic`, `donationAmount`, `createdAt`
- Consumable IAP: `intention_donation_1`, `intention_donation_5` ($1, $5)
- Cultural framing: "Đóng góp cho sứ vụ" (support the ministry) — never "pay for prayer"
- Community view: anonymized public intentions (opt-in) + personal saved

---

## Dependency Order

```
BrowserAnalytics (1) ← pure Python, no app needed
    ↓
AnnoEntry Extensions (2) ← Swift, needs Xcode (Sprint 1)
    ↓
StoreKit 2 Setup (3) ← needs AnnoEntry + Sprint 1
    ↓
Parish CRM (4) ← data only, can start anytime
    ↓
Content Tracker (5) ← needs moveable feast dates
    ↓
Grant Template (6) ← writing, customize brackets
    ↓
Sponsor Prospectus (7) ← fill specifics from content calendar
    ↓
Tour Referral Outreach (8) ← send when ready
    ↓
Affiliate Injection (9) ← needs content volume (Sprint 3+)
    ↓
Prayer Board (10) ← needs SwiftData + StoreKit 2 (Sprint 5+)
```

**Zero-code prep (do this week):** Ko-fi, Affiliate apps, Grant LOI, Diocese email, Artwork creation, Prayer guide writing

---

## Cross-Module Inputs Needed

| Need | From Module |
|------|-------------|
| Vietnamese Mass stream URLs | `vietnamese_media` M1 (34 YouTube) + M3 (8 parish livestreams) |
| Parish directory data | `vietnamese_media` M3 + this module M9 |
| Artwork assets | this module M3 (creation) + `calendar_content` Layer 2 |
| Pilgrimage routes | `monetization` M2 (v2) |
| Source citations for bios | `research_infrastructure` (Engine B output) |
| Calendar dataset (460 entries) | `calendar_content` module |
| VCC endorsement letter | `monetization` M15 (you secure) |
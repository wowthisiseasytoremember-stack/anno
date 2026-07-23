# ARTWORK ACQUISITION PLAN — Anno Engine B, full 365-day run

Goal: every one of the 365 entries ships with a real, license-clean artwork candidate (`status: "placeholder_only"` until human visual review), plus a small flagship set of museum-grade images for the highest-traffic dates.

---

## (a) Core pipeline — Wikimedia Commons first

Per date, per primary subject (saint / feast / place):

1. **Search**: Commons API `action=query&list=search` (or `generator=search`) with queries in priority order:
   - `"{Saint name}" painting`, `"{Saint name}" martyr`, `"{feast}" manuscript illumination`
   - category fallback: `Category:{Saint name}` → `categorymembers` file list
2. **Filter** (via `imageinfo&iiprop=extmetadata`):
   - License ∈ {Public domain, CC0, CC-BY (any version)}. CC-BY-SA accepted only if nothing better exists (share-alike is fine for app display but complicates merchandise later).
   - Resolution ≥ 1200 px on the long edge preferred; ≥ 800 px minimum.
   - Prefer paintings/frescoes/manuscripts > photographs of statues > modern devotional cards (last resort).
3. **Record** into `artwork_clearance_queue` format (existing schema), one row per candidate:
   `date, subject, commons_file, artist, date_of_work, source_institution, license, license_url, attribution_string, width, height, qa_status`
   - `attribution_string` is generated mechanically: `"{Title}, {artist}, {date}. {Institution}, via Wikimedia Commons. {License}."`
4. **QA gate (Agent C)**: curl the file page (200 + title sanity), then batch-eyeball thumbnails once per batch — machines check licenses, humans check that the picture is actually of the right saint.
5. **Attribution page**: the app needs one "Image credits" screen fed from the clearance queue; CC-BY legally requires this, PD/CC0 gets it anyway as good practice.

## (b) Museum open-access sources — flagship dates

For ~40 flagship dates (major solemnities, the Viet feast days, Advent/Christmas/Easter anchors, Thanksgiving, La Vang-adjacent Marian days), upgrade from Commons to direct museum open-access:

| Source | Access | License | Notes |
|---|---|---|---|
| **Metropolitan Museum Open Access** | API (`collectionapi.metmuseum.org`) | CC0 | Best first stop: strong medieval/Baroque saint holdings (the pilot's Clement I is Met CC0). |
| **Rijksmuseum** | API (free key) | CC0/PD | Dutch masters; good for Nativity, Adoration, Marian feasts. |
| **National Gallery of Art (Washington)** | Open data / images.nga.gov | CC0 | Excellent Italian Renaissance saints. |
| **Art Institute of Chicago** | Public API | CC0 | Good supplementary pool. |
| **Walters Art Museum** | Open access | CC0/PD | **Illuminated manuscripts** — key for generic fallback (see c). |
| **Getty** | Open content | PD/CC0 | Manuscripts + Baroque. |

Flagship rule: museum image → Commons only as fallback. Record museum object URL in `sources` as `type: "artwork_reference"`.

## (c) Dates with no good PD art

Roughly 15–25% of dates will have no usable subject-specific PD image. Fallback ladder:

1. **Generic illuminated-manuscript imagery** by theme, not by saint: initial letters, marginalia, calendar pages from Books of Hours (Walters, Getty, BnF Gallica PD). Theme map: martyr → palm/crown miniature; Marian → Annunciation/virgin initial; Advent → Isaiah/Annunciation to the shepherds leaves; Ordinary weekdays → calendar/kalends pages.
2. **Architecture**: a PD photo of the church/place named in the entry's `place` block (already geolocated — the image and the Atlas pin reinforce each other).
3. **Diocesan/shrine photo permissions** for Viet-specific subjects with thin PD coverage (La Vang shrine, Cha Diệp Tắc Sậy, Phát Diệm): one-time permission email template to the diocese/shrine office requesting CC-BY-equivalent app-display rights; log correspondence in the clearance queue with `qa_status: permission_pending`. Budget 2–4 weeks lead; never block a batch on it — use fallback (1) meanwhile.
4. **Explicit null**: honest fallback — entry ships with `artwork: null` rather than a hallucinated or wrong-subject image. Target: ≤ 3% of dates.

## (d) Pilot batch artwork candidates after URL check

All 7 pilot URLs re-verified live (200) in this QA pass:

| Date | Work | License | Status |
|---|---|---|---|
| 11/23 | Ciampelli, *Martyrdom of St Clement I* (Met, via Commons) | CC0 | ✓ keep |
| 11/24 | *Martyrdom of St Pierre Borie*, 1838 (MEP Paris, via Commons) | PD painting | ✓ keep (filename has a source-side typo "Matyrdom"; resolves correctly) |
| 11/25 | Caravaggio, *St Catherine of Alexandria* (Thyssen, via Commons) | PD | ✓ keep |
| 11/26 | Ferris, *The First Thanksgiving* (LOC, via Commons) | PD — romanticized, caption honestly (already done) | ✓ keep |
| 11/27 | Miraculous Medal photo (Xhienne, via Commons) | CC BY-SA 3.0 — attribution required | ✓ keep, generate attribution string |
| 11/28 | Crivelli, *St James of the Marches* 1477 (Louvre, via Commons) | PD | ✓ keep |
| 11/29 | Advent wreath (Clemens Pfeiffer, via Commons) | CC BY — attribution required | ✓ keep, generate attribution string; consider upgrading to a Walters Advent miniature for flagship polish |

Remaining human step: eyeball all 7 files once (URL check proves existence, not subject).

## (e) Effort estimate & swarm integration

- **Per batch (7 days)**: Commons search+filter ≈ 15–25 min agent time scripted, ≈ 60–90 min unscripted; license recording ≈ 10 min; Agent C URL+thumbnail QA ≈ 20 min. **Total ≈ 1.5–2 agent-hours per batch** once the search scripts exist; 53 batches ≈ **80–105 agent-hours** for the year.
- **Flagship museum upgrades**: ~40 dates × 15 min ≈ 10 agent-hours, run as a single dedicated job after wave 2.
- **Permission emails** (diocesan/shrine photos): one wave-3 job, ~3 agent-hours total including tracking.
- **Placement in the 3-wave plan**:
  - **Wave 1 (A+B)**: Agent A already proposes artwork candidates per date (as in this pilot) — keep that; A's dossier must include license + file URL, not just a museum page.
  - **Wave 2 (Agent C)**: add artwork URL fetch + license spot-check to the existing C checklist (adds ~5 min/batch).
  - **Wave 3 (revision/Atlas agents)**: the flagship museum-upgrade job, the permission-correspondence job, and one final full-corpus thumbnail eyeball pass (2–3 humans × 2 days, or ~15 agent-hours if agent-vision is trusted with a human audit sample).
- **Hard rule** (consistent with the swarm anti-hallucination rule): no artwork URL enters an entry without a live fetch in that batch's QA run. A date with no verified image gets the fallback ladder, never an invented file.

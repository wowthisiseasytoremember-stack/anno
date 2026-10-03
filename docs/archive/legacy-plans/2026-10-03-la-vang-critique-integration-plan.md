> ARCHIVED / SUPERSEDED 2026-10-03
>
> This integration plan predates the user's later decisions and the canonical `docs/EXEMPLAR_SOCAL_LA_VANG_RED_TEAM_SPEC.md`. In particular, St. Barbara is now core. Preserve this file as research history only.

# La Vang — Orange County critique integration plan

**Status:** Proposed integration plan. Not canonical product truth until reviewed/merged.  
**Source:** Exact external critique preserved in `docs/research/2026-10-03_la-vang-critique-verbatim.md`.  
**Tracking:** Issue #28 — Make the Orange County La Vang pilgrimage the v1 exemplar.

## Decision

Fold the critique into Anno as a **route-specific exemplar upgrade**, not a rewrite of the whole app.

The highest-leverage change is to make the Orange County route exercise the pilgrimage primitives Anno actually needs:

- chapters containing multiple on-site substations;
- manual arrival that never locks prayer behind GPS;
- remote/non-driven stations;
- a fixed station grammar: ARRIVE → SEE → KNOW → PRAY → CONTINUE;
- explicit sacred-intensity metadata;
- authored EN + VI route content even though daily-calendar VI remains intentionally reduced;
- source/provenance and field-verification state per KNOW claim;
- route variants without duplicating route content;
- accessible/audio-first prayer surfaces;
- completion that remembers a meaningful companion/name, not merely a station count.

Do **not** resurrect the old 18-route / 106-waypoint geofence architecture as the product model. The existing geofence documents are useful implementation research, but Issue #28's newer rules govern the exemplar: geofencing may suggest arrival; it must not unlock, authenticate, or complete prayer.

## 1. Route story

Use this as the working narrative arc:

**Mary → persecution and witness → crossing → the first generation → parish life → handed forward**

That fixes the current missing migration hinge without turning the route into a history lecture.

### Working chapter structure

1. **Christ Cathedral / La Vang campus — refuge + witness**
   - The Shrine / Linh Đài Đức Mẹ La Vang
   - Vietnamese Martyrs memorial
   - Marian Garden
   - Cathedral context: short, non-optional
   - campus is one drive stop with multiple substations, not multiple fake route legs

2. **Threshold — crossing**
   - preferred research candidate: narrated, non-driven Camp Pendleton station
   - alternatives if research or tone argues against it: cemetery/Boat People memorial or another physically visitable migration witness
   - this is the primitive that proves a station can matter without GPS presence

3. **St. Columban — scale / ordinary weekly life**
   - KEEP only if field research produces a specific SEE prompt and verified community context

4. **Vietnamese Catholic Center — first generation / institution-building**
   - retain from Issue #28 core route unless research disproves the role
   - make this chapter about how the community organized itself, not "another church"

5. **The Parish / Giáo Xứ Đức Mẹ La Vang — devotion becomes local parish life**
   - rename in-app to avoid colliding with route and shrine names
   - founding story becomes the KNOW spine after verification

6. **Handed forward — generational close**
   - St. Barbara remains provisional
   - include only if field research shows a physically and narratively distinct school/youth/sacramental generational role
   - otherwise the generational close can happen through the chosen martyr, family prayer, and completion experience without another redundant parish

## 2. Naming contract

Avoid three UI objects called "Our Lady of La Vang."

- Route display title: **La Vang — Orange County**
- Christ Cathedral substation: **The Shrine** / **Linh Đài Đức Mẹ La Vang**
- Santa Ana parish station: **The Parish** / **Giáo Xứ Đức Mẹ La Vang**
- marketing/search metadata may retain full formal names

## 3. Schema changes required

The current `docs/PILGRIMAGE_ROUTE_SCHEMA.md` assumes a route is a flat ordered array of physical waypoints. The exemplar now requires a v2 shape.

### Route-level additions

- `chapters[]` instead of only flat `waypoints[]`
- `variants[]` with IDs:
  - `quick`
  - `half_day`
  - `full`
- `modes[]`, with `group_parish_day` as a mode/toggle on Full rather than a fourth route
- `narrative_arc_en`, `narrative_arc_vi`
- `reopen_dates[]` for pilgrimage-linked calendar moments
- `field_test_status`
- `review_status`

### Chapter/station additions

- `chapter_id`
- `drive_stop_id` so several substations can share one physical campus arrival
- `presence_requirement`: `physical | optional | remote`
- `arrival_mode`: manual is always allowed; geofence is optional suggestion
- `presentation_intensity`: `quiet | medium | major`
- `etiquette`
- `quiet_mode_supported`
- `arrive`
- `see`
- `know`
- `pray`
- `continue`
- `go_deeper` optional
- `audio` optional
- `accessibility` / large-type behavior
- `claims[]` with source, confidence, and last_verified
- `permissions[]` for image/audio/text rights when relevant

### Claim/provenance contract

Each factual statement used in a KNOW card should be representable as:

- claim text;
- source URL/title;
- confidence;
- `verification_method`: source | field | partner;
- `last_verified`;
- `status`: verified | verify | disputed.

This should reuse Anno's existing source/confidence philosophy rather than invent a second provenance system.

## 4. Presentation grammar

Every station uses the same user-facing sequence:

**ARRIVE → SEE → KNOW → PRAY → CONTINUE**

Rules:

- ARRIVE: orientation, not spectacle by default.
- SEE: one concrete physical observation or, for remote stations, one concrete image/object/story anchor.
- KNOW: short sourced historical/context paragraph.
- PRAY: devotional action; for Vietnamese canonical prayers, use established Vietnamese prayer text rather than translating the English surface.
- CONTINUE: one sentence connecting this station to the next chapter in the arc.
- GO DEEPER: optional; long history, oral testimony, documents, extended audio.

The Christ Cathedral chapter should explicitly hinge Shrine → Martyrs: refuge and persecution are the same history seen from two sides.

## 5. Geofencing reconciliation

Existing `PILGRIM_COMPANION_GEOFENCING_SPEC.md` contains a stronger automatic/unlock model than the newer exemplar decisions allow.

For the La Vang exemplar:

- location may suggest "you may have arrived";
- user can always open/mark a station manually;
- prayer/audio is never GPS-gated;
- no "authenticated" spiritual seal;
- no required auto-completion;
- remote stations must function completely without physical presence;
- Quiet Mode suppresses haptics and visual bloom;
- location remains on-device if/when used.

Treat the older geofence spec as optional implementation reference, not product authority where it conflicts with Issue #28 or this exemplar.

## 6. Vietnamese scope exception

Anno's global v1 decision remains: daily-calendar content is EN-primary with VI limited to selected major feasts.

The **La Vang exemplar is a deliberate exception** because Vietnamese Catholic users are the primary test community for this route. Route/station strings should be authored as sibling EN and VI content and human reviewed.

Specific review gates from the critique:

- settle the second-person register once; do not casually use `bạn` for elders;
- review `truyền lại` versus `trao lại`;
- review the emotional weight of `Đức tin đã vượt biển`;
- use canonical Vietnamese prayers where applicable;
- allow `chúng con` in prayer voice;
- test Vietnamese typography first, especially uppercase/hero display;
- preserve culturally appropriate Marian address (`Mẹ`, `Đức Mẹ`) by context.

Require two Vietnamese Catholic reviewers from different generations before labeling route VI as final.

## 7. Audio/accessibility

For this exemplar, audio is not decoration.

Ship the station model so it can support:

- real recorded Vietnamese PRAY audio;
- large-type simplified interaction ("Bà/Ông mode" as a working concept, final label TBD);
- autoplay as an accessibility/user preference, never surprise playback by default;
- no synthetic TTS fallback for canonical prayer audio; show text when a reviewed recording is unavailable;
- future first-generation oral-history clips in GO DEEPER.

Do not block the route on oral-history collection. The schema should allow it; v1 can ship without it.

## 8. Visual intensity

Use the existing "quiet baseline + earned spectacle" direction.

- Shrine: major intensity.
- Shrine → Martyrs transition: deliberate, slower hinge.
- Martyrs: distinct deep liturgical red + muted gilt; community review required.
- ordinary parish stations: quiet/medium.
- completion: major intensity.
- Quiet Mode: suppress decorative bloom/haptics regardless of station intensity.

Do not hard-code saturated red + bright yellow for the Martyrs surface until community review.

## 9. "Find Mother" throughline

Prototype one repeated SEE motif:

**Find Mother.**

At each post-shrine parish/community stop, field research should identify whether there is a specific La Vang image, grotto, statue, or other Marian presence worth directing attention toward.

Only keep this device if it is physically true at the selected stops. Do not fabricate a motif to preserve copy.

If validated, this becomes the visual proof that La Vang moved from monumental shrine to ordinary community life.

## 10. Etiquette, not volatile schedules

Keep schedules out of narrative data.

Each station may include stable etiquette:

- Mass or prayer may be in progress;
- silence device;
- avoid photography during liturgy;
- chapel-specific reverence where applicable;
- accessibility/parking notes only when field-verified.

Current Mass times, office hours, and event times should remain external/linked practical data with a last-verified timestamp if surfaced.

## 11. Calendar retention hook

Connect the completed route to Anno's calendar engine before building social features.

Candidate reopen moments to verify/configure:

- Assumption / La Vang observance around August 15;
- Vietnamese Martyrs, November 24;
- Tết;
- All Souls.

The product behavior is a respectful pilgrimage-day reminder or route resurfacing, not a streak mechanic.

## 12. Completion object

Completion should store/share meaning, not only count.

Add a route-session field for a chosen saint/martyr/companion where the route supports it.

Example output pattern:

"Completed Oct 3, 2026 · I prayed with Agnes Lê Thị Thành."

Use "traced" / "followed" rather than "walked" for a primarily driven route.

## 13. Research + permissions gate

Before KNOW copy is marked final:

- visit every physical stop;
- photograph/record the exact SEE target for internal verification;
- verify parking/accessibility;
- verify Martyrs inscription layout and Shrine physical details;
- verify parish founding histories;
- verify the role/address/history of the Vietnamese Catholic Center;
- research the Camp Pendleton migration station and decide whether it is remote-only;
- contact parish/diocesan/Vietnamese Catholic Center partners where practical;
- clear image/likeness rights;
- identify licensing status for prayer/hymn/audio text;
- maintain the claims register.

Do not silently upgrade any **[verify]** statement from the verbatim critique to confirmed app copy.

## 14. Testable milestone

The first physically testable exemplar is done when:

- ≥80% of testers understand/open the Christ Cathedral substations as distinct moments without being told how the hierarchy works;
- ≥70% can explain why the parish/community stops belong in the same story;
- Layer-2/KNOW engagement is measurable; initial target from critique is median ≥15 seconds where the paragraph length makes that meaningful;
- Vietnamese-primary testers rate VI copy at least as "written for me" as the English face;
- community review yields zero unresolved factual corrections in final KNOW cards;
- the whole route remains usable with location permission denied.

## 15. Implementation order

### Phase A — data model and spec
1. Create `PILGRIMAGE_ROUTE_SCHEMA_V2.md` rather than silently mutating the old contract.
2. Add chapters/substations, variants, remote presence, station grammar, claims, etiquette, presentation intensity.
3. Add a migration note from v1 flat waypoints.

### Phase B — exemplar fixture
4. Create an Orange County La Vang route fixture using placeholders for unverified facts.
5. Encode the Christ Cathedral campus as one chapter/drive stop with substations.
6. Add the remote Threshold slot without committing to factual copy until researched.
7. Keep St. Barbara explicitly provisional.

### Phase C — current non-Mac work
8. Add JSON validation for the v2 fixture.
9. Add claims-register validation: no `verify` claim may ship as `verified`.
10. Add EN/VI completeness validation for this route only.
11. Draft the research/field worksheet and reviewer signoff sheet.

### Phase D — Mac/native implementation
12. Render chapter → station hierarchy in Map/Pilgrimage UI.
13. Implement ARRIVE/SEE/KNOW/PRAY/CONTINUE surfaces.
14. Add manual arrival first; geofence suggestion second.
15. Add Quiet Mode and large-type/audio accessibility.
16. Add variant picker: Quick / Half Day / Full; Group/Parish Day as Full-mode behavior.

### Phase E — field test
17. Drive/test the route.
18. Replace placeholders with verified SEE targets and sourced KNOW cards.
19. Conduct two-generation Vietnamese review.
20. Measure the milestone; cut redundant parish stops if the arc still collapses into "another Vietnamese church."

## 16. What this changes in current Anno docs

After approval, reconcile these files in one focused pass:

- `docs/PILGRIMAGE_ROUTE_SCHEMA.md` → retain as v1 or point to v2.
- `docs/PILGRIM_COMPANION_GEOFENCING_SPEC.md` → mark GPS as enhancement, not spiritual gate.
- `docs/PILGRIM_AUDIO_GEOFENCE_BEAUTY_SPEC.md` → preserve intensity ideas, remove any mandatory arrival/unlock assumptions.
- `docs/VIETNAMESE_LOCALIZATION_GUIDE.md` → add route-specific authored bilingual exception and elder/register note.
- `docs/VIETNAMESE_CATHOLIC_RESEARCH_PROMPT.md` → add SoCal field-verification/claims register workstream rather than relying on generated cultural research.
- `ROADMAP.md` / `AGENTS.md` → identify the OC La Vang route as the v1 pilgrimage exemplar without changing the 5-flagship product scope.
- Issue #28 → update checklist against the merged exemplar spec.

## 17. Explicitly not now

Do not let this integration reopen removed v1 scope:

- no AR Reliquary;
- no spatial audio requirement;
- no restoration of 18-route breadth;
- no turn-by-turn navigation;
- no social feed;
- no leaderboard/XP/streak;
- no GPS requirement;
- no generalized "elder mode" architecture beyond the minimum route accessibility behavior until tested;
- no mass-time ingestion system;
- no oral-history platform before the route itself works.

## Immediate next artifact after review

Promote the approved decisions from this plan into the missing Issue #28 target:

`docs/EXEMPLAR_SOCAL_LA_VANG_RED_TEAM_SPEC.md`

That file should become the concise canonical route spec. The verbatim critique remains immutable source material beside it.

## 18. Evidence weighting across critique sources

There are now two preserved critique sources:

1. `docs/research/2026-10-03_la-vang-critique-verbatim.md` — **primary/trusted critique source**.
2. `docs/research/2026-10-03_la-vang-critique-secondary-verbatim.md` — **secondary/lower-confidence critique source**.

Use them differently.

### Adoption rule

A recommendation is stronger when it is supported by one or more of:

- both critique sources independently converge on it;
- current Anno product decisions already point the same way;
- official diocesan/parish/site sources verify the factual premise;
- field testing verifies the physical premise;
- Vietnamese Catholic community reviewers confirm the cultural/language premise.

A recommendation is weaker when it depends on:

- a unique factual claim present only in the secondary critique;
- precise attendance numbers, dimensions, materials, addresses, affiliations, histories, or personnel relationships not independently verified;
- emotional/cultural interpretation not confirmed by the primary audience;
- a specific site role inferred from reputation rather than field observation.

Never promote those weaker claims directly into KNOW copy or canonical route structure merely because they are specific.

### High-confidence convergence between both critiques

These are strengthened because both sources independently argue for them and they already fit Issue #28 / current Anno direction:

- Christ Cathedral should be **one geographic chapter with substations**.
- Our Lady of La Vang Church belongs in the candidate/core route, but should be differentiated from the Shrine in naming and function.
- St. Barbara is **provisional**, with narrative function more important than keeping that exact parish.
- ARRIVE → SEE → KNOW → PRAY → CONTINUE should be a reusable pilgrimage grammar.
- manual arrival must remain first-class; GPS cannot be spiritual DRM.
- Shrine and completion can carry the strongest ceremonial treatment; Martyrs should be solemn; Gardens should be quieter.
- the experience should be explicitly Vietnamese Catholic while welcoming others.
- Vietnamese copy requires authored/community-reviewed treatment rather than literal machine translation.
- exact timing, parking, dwell, accessibility, and wayfinding must come from physical testing.
- no turn-by-turn navigation, leaderboard, XP, AR requirement, UGC route builder, or mandatory GPS in v1.
- route success should be measured with real users, not assumed from a polished spec.

### Primary-source ideas retained over secondary-source tension

Where the two critiques diverge, default toward the trusted critique unless field evidence overturns it:

- **Migration hinge:** keep an explicit crossing/Threshold chapter in the working architecture. The secondary critique's four-chapter route omits this as a discrete station even while praising the migration arc. Do not drop the hinge without testing whether the story still lands.
- **Vietnamese Catholic Center:** retain as a core research candidate from Issue #28 / primary critique. The secondary critique treats it mainly as an alternative; do not demote it on that basis alone.
- **Route variants:** keep the underlying Quick / Half Day / Full data model from the primary plan, while borrowing the secondary critique's better user-facing naming if testing prefers it. Product labels can change without changing the route model.
- **Cathedral context:** primary critique argues the Cathedral itself should be short but non-optional; secondary calls it optional. Treat this as a testable editorial question, with the default currently **short + included** because it contributes the local-Church/diaspora story.

### Secondary-source ideas worth incorporating as hypotheses

These are useful, but should enter the research/test backlog rather than canon:

- intent-based variant labels such as “Visit La Vang” and “La Vang + One Parish”;
- optional respectful meal/cultural pauses outside the sacred station sequence;
- family prompts for elders/children;
- a final “What will you hand forward?” reflection;
- explicit campus wayfinding notes for substations;
- sensory SEE prompts tied to precise physical details;
- possible healing metaphor around La Vang medicinal leaves;
- attributed community quotes/testimony;
- testing with elders, families, young adults, non-Vietnamese Catholics, and parish groups;
- community_verified_date as a useful content metadata field;
- post-completion keepsake/holy-card treatment and related prayer resurfacing.

### Secondary factual claims that remain untrusted until verified

Examples include, but are not limited to:

- exact shrine statue height/material/design details;
- exact Martyrs Wall construction/details and Alpha-ribbon relationship;
- exact Marian Gardens layout/art provenance;
- exact parish street addresses when not independently checked;
- exact Vietnamese Mass counts or school/community statistics;
- personnel/design relationships such as who helped design the shrine statue;
- claims about a parish's 1975 refugee history;
- exact 1–4 mile spacing between stops;
- Marian Days attendance figures;
- “largest Vietnamese population outside Vietnam” and specific clergy/community-share claims;
- precise local feast-day practices/dates beyond universal liturgical dates.

These belong in the claims register with `status: verify` until sourced.

## 19. Net change from the secondary critique

The second critique does **not** change the fundamental architecture already proposed in this plan. It mainly improves the research/testing brief.

Adopt now at the planning level:

- treat sensory specificity as a quality requirement for SEE prompts;
- add multi-generational test cases;
- add real campus wayfinding/accessibility observations to field research;
- add qualitative “would I hand this to my grandparents/family?” testing;
- consider intent-based labels over product-y duration labels in UI;
- add `community_verified_date` as a candidate provenance field;
- test “What will you hand forward?” as the completion reflection.

Do **not** adopt yet:

- any unique physical/site fact from the secondary critique;
- the claim that St. Barbara definitively fulfills the generational chapter;
- exact attendance/population/community statistics;
- a route structure that removes the migration Threshold solely because the secondary critique did not include it;
- any sensory prompt whose physical referent has not been seen/verified.

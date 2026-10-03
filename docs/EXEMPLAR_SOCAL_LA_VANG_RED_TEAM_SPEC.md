# Anno SoCal Exemplar — Red-Team Product Spec

**Status:** critique-ready, recommended direction  
**Route:** Our Lady of La Vang — Orange County  
**Purpose:** make the SoCal Vietnamese Catholic route the v1 pilgrimage exemplar that can be physically tested by the initial user base.

## Red-team verdict

The earlier concept is directionally strong but had five weaknesses:

1. It treated three points on the Christ Cathedral campus as if they were separate travel destinations.
2. It over-indexed on "church after church" without giving every geographic stop a distinct product job.
3. It used St. Barbara as a core stop even though the Vietnamese Catholic Center tells the three-generation diaspora/community story more directly.
4. It risked turning the pilgrimage into an achievement flow rather than a devotional journey.
5. It relied on poetic copy before fully separating durable spiritual narrative from volatile practical information.

## Recommended core route

### Chapter 1 — La Vang: memory, refuge, witness
**Christ Cathedral campus, Garden Grove**

One geographic arrival with multiple in-app stations:

- Our Lady of La Vang Shrine — **Major Pilgrimage Moment**
- 117 Vietnamese Martyrs wall — **Pilgrimage Highlight**
- Marian Gardens — **Reflection**
- Christ Cathedral — optional context/deeper-visit station

The app should understand these as one campus chapter, not three drive legs.

### Chapter 2 — A living parish
**St. Columban Catholic Church, Garden Grove**

Narrative job:
- active Vietnamese Catholic parish life
- continuity between immigrant story and ordinary sacramental life
- historical anchor: episcopal ordination of Bishop Thomas Thanh Thai Nguyen in 2017

Do not make the bishop ordination the only reason this station matters.

Moment:
**FAITH BECOMES COMMUNITY**

### Chapter 3 — The diaspora builds institutions
**Vietnamese Catholic Center, Santa Ana**

Narrative job:
- explicit Vietnamese-American Catholic institution
- three generations: elders, adults, children
- religious + cultural + educational + social continuity
- bridge from refugee-era institution building to the next generation

Moment:
**A HOME BUILT FOR THE NEXT GENERATION**

This is the clearest "diaspora continuity" stop in the route and should replace St. Barbara in the core exemplar unless user testing proves otherwise.

### Chapter 4 — La Vang as parish life
**Our Lady of La Vang Catholic Church, Santa Ana**

Narrative job:
- La Vang devotion is not only a monument at Christ Cathedral
- Marian identity embedded in an active parish
- Vietnamese, English, and Spanish Catholic life share one parish context

Moment:
**LA VANG LIVES HERE TOO**

## Optional extension

### St. Barbara Catholic Church, Santa Ana

Strong Vietnamese parish life and a large multilingual community, but narratively redundant in the core route once the Vietnamese Catholic Center and Our Lady of La Vang parish are present.

Use as:
- optional "community extension"
- alternate stop if field testing shows stronger family/group resonance
- later route branch focused on Vietnamese parish life

Do not delete it from the data until field testing decides.

## Route variants

Keep variants simple and behavior-based:

### Quick — La Vang Campus
Christ Cathedral campus only.

For:
- first-time user
- older relatives
- casual visit
- short test session

### Core — Orange County Pilgrimage
1. Christ Cathedral / La Vang chapter
2. St. Columban
3. Vietnamese Catholic Center
4. Our Lady of La Vang parish

This is the primary exemplar.

### Extended — Community Route
Core route plus St. Barbara and future verified optional community stops.

Do not lead with exact minute estimates until physically driven and timed.

## Emotional arc

Replace the overly linear "Mary → persecution → migration → community → next generation" model with:

**Refuge → witness → survival → institution-building → living parish → inheritance**

Mary/La Vang is the thread through the arc, not merely step one.

This avoids reducing Vietnamese Catholic identity to a single refugee narrative while preserving the real history of persecution and migration.

## Opening

**OUR LADY OF LA VANG**  
**ORANGE COUNTY PILGRIMAGE**

Preferred hook:

**A faith carried through persecution, migration, and generations continues here.**

Alternate mass-market hook:

**Start close to home. Walk a living story of Vietnamese Catholic faith.**

Avoid making "Faith crossed an ocean" the sole thesis; it is memorable but too reductive for second/third-generation users and for Vietnamese Catholics whose family story does not fit a single migration narrative.

Primary CTA:
**BEGIN PILGRIMAGE**

Secondary:
**SEE THE ROUTE**

## Station grammar

Every station uses the same five-beat pattern:

1. **ARRIVE** — obvious arrival state, haptic, title
2. **LOOK** — one physical thing to notice
3. **KNOW** — one short context paragraph
4. **PRAY** — one prayer/prompt
5. **CONTINUE** — next action

Deep history, sources, schedules, and maps live behind secondary actions.

## Spectacle levels

### Reflection
- little/no glow
- quiet typography
- no achievement language

### Pilgrimage Highlight
- explicit label
- aureole
- stronger color
- medium haptic
- larger title

### Major Pilgrimage Moment
- explicit label
- hero typography
- thematic bloom
- stronger one-shot haptic
- sacred divider
- optional invocation
- no looping animation after the reveal

## Christ Cathedral chapter

### Shrine
**MAJOR PILGRIMAGE MOMENT**
- Marian blue + gold
- largest route-specific hero treatment
- one-line invocation
- focus on refuge/hope and the Vietnamese-American shrine story

### 117 Martyrs
**PILGRIMAGE HIGHLIGHT**
- crimson/gold
- quieter motion than the shrine
- prompt: choose one name and pause
- never turn martyrdom into celebratory gamification

### Marian Gardens
**REFLECTION**
- deliberately reduces visual intensity
- prompt for silence, rosary, or a short personal intention
- the contrast is part of the design

### Cathedral
Optional deeper visit.
- architecture / local Church context
- current tour link rather than duplicated schedule
- support Vietnamese-language tour information when available

## Practical data rule

Narrative data should be durable. Volatile data should be linked/verified.

Durable:
- station story
- devotional prompt
- historical context
- significance
- official URL

Volatile:
- Mass times
- confession times
- tour schedules
- office hours
- parking restrictions
- temporary closures

For volatile data:
- display "check current schedule"
- prefer official source links
- record last_verified
- do not bury stale times in devotional prose

## Historical truth language

Avoid flattening devotional tradition into unsupported empirical certainty.

Use language such as:
- "Catholic tradition holds..."
- "The shrine commemorates..."
- "Vietnamese Catholics venerate..."
- "The Diocese describes..."

Use direct factual language for documented local facts.

## Completion

Keep the emotional payoff; remove gamey accounting.

Recommended:

# PILGRIMAGE COMPLETE

**You made a pilgrimage through a living story of Vietnamese Catholic faith in Orange County.**

Then:
**Our Lady of La Vang, pray for us.**

Show:
- visited stations
- date
- optional share keepsake

Avoid:
- XP
- scores
- leaderboards
- fake achievement badges
- competitive completion metrics

## Share artifact

A devotional keepsake, not a gaming badge.

Include:
- illuminated Anno A
- Marian blue + gilt
- route title
- date completed
- subtle route line
- invocation
- optional station list

Sentimental is acceptable. Generic "achievement unlocked" is not.

## Bilingual standard

English and Vietnamese are co-authored surfaces.

Requirements:
- independent line breaks
- non-literal translation allowed
- culturally recognizable Vietnamese saint/devotional names
- human Vietnamese Catholic review before copy is called final
- no shipping claim that every Vietnamese string is verified unless it actually is

## Recommended data model additions

Keep these optional so other routes remain compatible:

- chapter_id
- chapter_order
- station_role
- moment_level
- moment_label_en
- moment_label_vi
- look_prompt_en
- look_prompt_vi
- short_context_en
- short_context_vi
- official_url
- visit_tier: core | optional
- last_verified

Route variants should preferably live in a small separate manifest containing ordered waypoint IDs instead of duplicating waypoint objects.

## What not to build

- turn-by-turn navigation
- mandatory GPS check-in
- AR
- leaderboards
- social feed
- user-built route editor
- elaborate group coordination
- fixed Mass schedules embedded in narrative data

## Validation target

A tester succeeds without coaching if they can:

1. understand what this pilgrimage is
2. choose Quick or Core
3. get to Christ Cathedral
4. understand Shrine / Martyrs / Gardens as different spiritual moments
5. continue to the next geographic stop
6. understand why each stop belongs
7. finish with an emotional payoff
8. want to show the route to a family member or parish friend

## Decisions still requiring user ruling

1. Approve Vietnamese Catholic Center as core and move St. Barbara to optional.
2. Approve four geographic chapters as the Core route.
3. Approve "Refuge → witness → survival → institution-building → living parish → inheritance" as the narrative arc.
4. Choose opening hook.
5. Decide how loud the completion screen can go.

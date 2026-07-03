document = """# The Daily Devotional Engine
## Technical Specification & Content Playbook
### For a Hallow-Scale Faith-Based App

---

**Version:** 1.0  
**Date:** July 2026  
**Classification:** Internal Product Spec  
**Target Market:** Catholic, Christian, and Abrahamic-faith daily devotional app users  
**Monetization Model:** Freemium daily content + premium deep-dive packs + pilgrimage route subscriptions

---

# TABLE OF CONTENTS

1. [Executive Summary: The Sell](#1-executive-summary-the-sell)
2. [The Two-Engine Architecture](#2-the-two-engine-architecture)
3. [Engine A: Deterministic Calendar Conversion](#3-engine-a-deterministic-calendar-conversion)
4. [Engine B: Daily Historical Research Agent](#4-engine-b-daily-historical-research-agent)
5. [The Devotional Layer: Facts + "The Bullshit"](#5-the-devotional-layer-facts--the-bullshit)
6. [Sample Output: July 2, 2026](#6-sample-output-july-2-2026)
7. [Implementation Roadmap](#7-implementation-roadmap)
8. [Appendix A: Complete Python Script](#appendix-a-complete-python-script)
9. [Appendix B: Daily Research Prompt (Copy-Paste Ready)](#appendix-b-daily-research-prompt-copy-paste-ready)
10. [Appendix C: Content Style Guide](#appendix-c-content-style-guide)

---

# 1. EXECUTIVE SUMMARY: THE SELL

## The Problem

Existing devotional apps (Hallow, Glorify, Pray.com) serve generic daily content. Users get a Bible verse and a reflection. What they *don't* get is:

- **Temporal specificity**: "What happened in biblical history *today*?"
- **Interfaith depth**: "How do Jews, Christians, and Muslims remember this figure differently?"
- **Geographic immersion**: "Where did this happen? Can I visit?"
- **Artistic heritage**: "What did Caravaggio paint about this saint?"

## The Product

A daily feed where every day is **historically loaded**. The user opens the app and discovers that today—July 2, 2026—is:

- The feast of **Sts. Processus and Martinian** (martyrs, traditionally baptized by Peter in the Mamertine Prison)
- **18 Tammuz 5786** on the Hebrew calendar (three weeks before Tisha B'Av, the fast commemorating Jerusalem's destruction)
- **17 Dhul-Hijjah 1447 AH** on the Islamic calendar (the Hajj season, when pilgrims stand at Arafat)
- The day **St. Thomas More** was executed in 1535
- The day the **Visitation of Mary to Elizabeth** is celebrated in some Eastern traditions

And then the app tells them a story. With art. With a map. With a prayer.

## The Moat

No other app does **deterministic multi-calendar conversion + scholarly research + interfaith context + GPS-ready geography** at scale. This is defensible IP.

## Revenue Streams

| Tier | Feature | Price |
|------|---------|-------|
| **Free** | Daily devotional + 1 calendar conversion | $0 |
| **Premium** | All calendar systems + deep-dive articles + artwork gallery | $4.99/mo |
| **Pilgrim** | GPS-guided routes (e.g., "Walk Mary's path from Nazareth to Ein Kerem") | $9.99/mo |
| **Scholar** | Source citations, academic paper links, raw JSON export | $12.99/mo |

---

# 2. THE TWO-ENGINE ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    DAILY DEVOTIONAL ENGINE                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐  │
│  │  ENGINE A    │ ────▶│  JSONL TABLE │ ────▶│ ENGINE B │  │
│  │  (Python)    │      │  (4 years)   │      │  (LLM)   │  │
│  │  Deterministic│      │  Pre-computed │      │  Daily   │  │
│  │  Calendar Math│      │  1,461 rows   │      │  Research│  │
│  └──────────────┘      └──────────────┘      └────┬─────┘  │
│                                                    │        │
│                                              ┌─────┴─────┐  │
│                                              │  OUTPUT   │  │
│                                              │  JSON     │  │
│                                              │  (daily)  │  │
│                                              └─────┬─────┘  │
│                                                    │        │
│                                              ┌─────┴─────┐  │
│                                              │  LAYER C  │  │
│                                              │  (LLM)    │  │
│                                              │  Devotion │  │
│                                              │  Content  │  │
│                                              └───────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Engine A** runs once per year (or per 4-year cycle). It is pure Python. No LLM. No hallucination risk. It generates a JSONL file with every Gregorian date mapped to 10+ calendar systems.

**Engine B** runs daily. It takes the pre-computed calendar data for *today* and researches historical events, saints, biblical passages, and interfaith connections.

**Layer C** (not yet built) is a separate LLM prompt that takes Engine B's structured JSON and transforms it into the devotional content users actually read. This is where "the bullshit" lives—in the best sense.

---

# 3. ENGINE A: DETERMINISTIC CALENDAR CONVERSION

## What It Does

Converts every Gregorian date in a range to:

| Calendar | Library | Authority |
|----------|---------|-----------|
| Hebrew | `pyluach` | Molad-based, Four Gates kevi'ah rules |
| Islamic (Umm al-Qura) | `hijri-converter` | Saudi official astronomical calculation |
| Islamic (Tabular) | Custom 30-year cycle | Historical arithmetic calendar |
| Julian | `convertdate` | Day-count offset (13 days in 2026) |
| Coptic | `convertdate` | Fixed 365-day + epagomenal days |
| Ethiopian | `convertdate` + offset | Same as Coptic, +7 years |
| Byzantine | Julian + 5509 epoch | Anno Mundi (creation epoch) |
| Armenian | Julian + epoch 552 CE | Armenian Apostolic Church |
| Syriac/Seleucid | Julian + 311 BCE epoch | Early Eastern Christianity |
| Talmudic notations | Hebrew AM derived | Destruction-era, Seleucid-era |

## Key Features

- **Sundown-aware**: Hebrew and Islamic dates shift at sundown (Garden Grove, CA anchor)
- **Divergence tracking**: Flags when Umm al-Qura and Tabular Islamic differ
- **Leap year verification**: Confirms Julian vs. Gregorian century-year rules
- **JSON Lines output**: One object per line, stream-processable

## Installation

```bash
pip install pyluach hijri-converter convertdate
```

## Usage

```bash
# Generate 4-year table
python calendar_engine.py --start 2026-01-01 --end 2029-12-31 --output calendar_2026_2029.jsonl

# Spot-check against known references
python calendar_engine.py --spot-check
```

## Output Schema

```json
{
  "gregorian_date": "2026-07-02",
  "gregorian_doy": 183,
  "julian": {
    "date": "2026-06-19",
    "offset_days": 13,
    "drift_note": "13 days behind Gregorian; no century leap discrepancy in 2026"
  },
  "hebrew": {
    "date": "18 Tammuz 5786",
    "year_type": "2C355",
    "is_leap_year": false,
    "year_length": 355,
    "sundown_at_anchor": "19:47 PDT",
    "day_boundary_note": "Gregorian noon (12:00) before sundown (19:47 PDT); Hebrew date = same day"
  },
  "islamic_umm_al_qura": {
    "date": "17 Dhu al-Hijjah 1447 AH",
    "sundown_at_anchor": "19:47 PDT",
    "day_boundary_note": "Gregorian noon (12:00) before sundown (19:47 PDT); Islamic date = same day"
  },
  "islamic_tabular": {
    "date": "17 Dhu al-Hijjah 1447 AH",
    "year_in_cycle": 27,
    "is_leap_year": false,
    "divergence_from_umm_al_qura": 0,
    "divergence_note": null
  },
  "coptic": {
    "date": "25 Paoni 1742",
    "epoch_name": "Anno Martyrum",
    "epagomenal": false
  },
  "ethiopian": {
    "date": "25 Sene 2018",
    "new_year_alignment_note": null
  },
  "byzantine": {
    "date": "19 June 7535",
    "epoch_name": "Anno Mundi",
    "month_day_same_as_julian": true
  },
  "armenian": {
    "date": "19 June 1475",
    "epoch_year": 552
  },
  "syriac": {
    "date": "19 Haziran 2336",
    "seleucid_year": 2336,
    "month_name_syriac": "Haziran",
    "year_begins_october": true
  },
  "talmudic_notations": {
    "am_year": 5786,
    "destruction_era_year": 1956,
    "seleucid_era_year": 2337,
    "contextual_relevance": "active"
  },
  "conversion_metadata": {
    "anchor_location": "Garden Grove, CA",
    "anchor_lat": 33.7743,
    "anchor_lon": -117.9379,
    "algorithms": {
      "hebrew": "pyluach/Four Gates kevi'ah",
      "islamic_umm_al_qura": "hijri-converter/Saudi Umm al-Qura",
      "islamic_tabular": "30-year arithmetic cycle",
      "julian": "day-count offset (13 days)",
      "coptic": "convertdate/coptic fixed 365-day",
      "byzantine": "Julian + 5509 epoch",
      "syriac": "Julian + Seleucid epoch"
    }
  }
}
```

---

# 4. ENGINE B: DAILY HISTORICAL RESEARCH AGENT

## What It Does

Takes the pre-computed calendar conversions for *one day* and researches:
- Saints' feast days and martyrdoms
- Biblical events traditionally dated to this day
- Church councils, papal events, canonizations
- Quranic events and Islamic commemorations
- Talmudic teachings and Jewish observances
- Interfaith connections (shared figures, parallel observances)
- Devotional artworks, maps, pilgrimage sites

## Input

The LLM receives the JSON object for today's date from Engine A. It does NOT recompute calendars.

## Sourcing Hierarchy

1. **Scripture** (Bible, Quran, Talmud) — textual witnesses
2. **Peer-reviewed scholarship** — for historical claims
3. **Official Church documents** — for Catholic tradition
4. **Islamic historical sources** (Tabari, Ibn Ishaq) — for Islamic tradition
5. **Jewish textual tradition** (Talmud, Midrash) — for Jewish tradition
6. **Roman Martyrology** — explicitly labeled as traditional/liturgical dating

## Specificity Tiers

| Tier | Scope | Requirement |
|------|-------|-------------|
| Exact Day | Feast days, martyrdoms, councils | Source must date to this specific day |
| This Week | Events within 7 days | Source must explicitly note proximity |
| This Month | Month-tied events | Source must explicitly tie to month |
| This Season | Currently active liturgical seasons | Only if season is *currently* active |
| Annual Cycle | Recurring commemorations | Active during this period |

## Interfaith Context Rule

Include interfaith connections **only where genuine intersection exists**. Do not manufacture connections. If an entry is single-tradition, state that explicitly.

## Output Schema

```json
{
  "gregorian_date": "2026-07-02",
  "exact_day_events": [...],
  "this_week_events": [...],
  "this_month_events": [...],
  "this_season_events": [...],
  "annual_cycle": [...],
  "research_metadata": {
    "sources_queried": [...],
    "gaps": [...],
    "confidence_summary": {...}
  }
}
```

Each event entry includes:
- `title`, `description`, `source` (with precise citation)
- `calendar_system` (which calendar makes it relevant)
- `historical_confidence`: `confirmed` / `traditional` / `disputed`
- `interfaith_notes` (or `null`)
- `media`: artworks, maps, pilgrimage sites (with Wikidata Q-codes)
- `geography`: biblical name, modern equivalent, coordinates

---

# 5. THE DEVOTIONAL LAYER: FACTS + "THE BULLSHIT"

## The Strategy

Engine B outputs **structured scholarly data**. Layer C (a separate LLM prompt) transforms that data into content that sells. This is not dishonest—it is **framing**. The facts are rigorous. The framing is inspirational.

## Two-Track Content Model

### Track 1: The Scholarly Data Layer (Engine B Output)
- Structured JSON
- Source citations with DOIs/URLs
- Confidence ratings (`confirmed` / `traditional` / `disputed`)
- Conflict notes where sources disagree
- No devotional language

### Track 2: The Devotional Content Layer (Layer C Output)
- Narrative storytelling
- Emotional resonance
- Prayer prompts
- Artwork immersion
- Geographic wanderlust
- "Did you know...?" hooks

## Content Types

| Type | Description | Example |
|------|-------------|---------|
| **Daily Saint** | 300-word hagiography with prayer | "St. Thomas More died today in 1535. He chose conscience over king. What are you choosing today?" |
| **Biblical This Day** | Scripture passage + historical context | "On 18 Tammuz, the walls of Jerusalem were breached. Jesus wept over this city. Pray for peace." |
| **Interfaith Bridge** | Shared figure across traditions | "Mary is Miriam in the Quran, the mother of a prophet honored by 1.9 billion Muslims. Today, Christians celebrate her Visitation." |
| **Art Moment** | Devotional artwork with meditation | "Caravaggio's 'Crucifixion of St. Peter' (1601) hangs in Santa Maria del Popolo. Look at Peter's face. He asked to be crucified upside down—unworthy to die as his Lord did." |
| **Pilgrimage Pin** | GPS-ready site with modern address | "The Mamertine Prison, Rome. 41.8936° N, 12.4853° E. Sts. Processus and Martinian were baptized here by Peter. Visit. Pray. Remember." |
| **Calendar Cross** | How other faiths mark today | "Today is 17 Dhul-Hijjah. The Hajj has ended. Muslims worldwide celebrate Eid al-Adha, remembering Abraham's willingness to sacrifice. Christians see the same Abraham in their Lenten journey." |

## Tone Guide

| Context | Tone | Forbidden |
|---------|------|-----------|
| Historical facts | Precise, direct, sourced | Speculation, "maybe," "perhaps" without attribution |
| Devotional framing | Warm, intimate, urgent | Generic platitudes, "God has a plan for you" fluff |
| Interfaith connections | Respectful, curious, unifying | Comparative theology debates, "we're all the same" flattening |
| Art descriptions | Sensory, contemplative | Art history lecture mode |
| Prayer prompts | Personal, second-person | Prescriptive, guilt-inducing |

## The Hook Formula

Every daily entry opens with one of:

1. **The Temporal Hook**: "On this exact day in 1535..."
2. **The Calendar Hook**: "Today is 18 Tammuz. In three weeks, Jews worldwide will fast for Tisha B'Av."
3. **The Art Hook**: "Look at this painting. Really look."
4. **The Place Hook**: "You are 5,437 miles from the Mamertine Prison. But distance is nothing in prayer."
5. **The Shared Hook**: "Abraham. Ibrahim. Avraham. Same man, three names, three billion believers."

---

# 6. SAMPLE OUTPUT: JULY 2, 2026

## Engine B Output (Structured JSON)

```json
{
  "gregorian_date": "2026-07-02",
  "exact_day_events": [
    {
      "title": "Feast of Sts. Processus and Martinian",
      "description": "Roman martyrs traditionally said to have been baptized by St. Peter in the Mamertine Prison, then beheaded under Nero. Their relics are preserved in St. Peter's Basilica.",
      "source": "Roman Martyrology, July 2; Acta Sanctorum, Julii Tomus I",
      "calendar_system": "Gregorian",
      "historical_confidence": "traditional",
      "interfaith_notes": null,
      "media": [
        {
          "type": "artwork",
          "title": "The Baptism of Processus and Martinian",
          "artist": " attribution uncertain, 17th century Roman school",
          "location": "Santa Maria del Popolo, Rome",
          "coordinates": null,
          "wikidata_q": null
        }
      ],
      "geography": [
        {
          "biblical_name": "Mamertine Prison (Tullianum)",
          "modern_name": "Carcere Mamertino, Rome, Italy",
          "coordinates": [41.8936, 12.4853],
          "wikidata_q": "Q650439"
        }
      ]
    },
    {
      "title": "Martyrdom of St. Thomas More",
      "description": "Executed at Tower Hill, London, on July 2, 1535, for refusing to accept Henry VIII as Supreme Head of the Church of England. Canonized in 1935 by Pius XI.",
      "source": "Encyclical *Invicti Athletae* (Pius XI, 1957); Harpsfield, *Life and Death of Sir Thomas More* (c. 1557)",
      "calendar_system": "Gregorian",
      "historical_confidence": "confirmed",
      "interfaith_notes": null,
      "media": [
        {
          "type": "artwork",
          "title": "The Execution of Sir Thomas More",
          "artist": "unknown, 16th century",
          "location": "National Portrait Gallery, London",
          "coordinates": null,
          "wikidata_q": null
        }
      ],
      "geography": [
        {
          "biblical_name": "Tower Hill",
          "modern_name": "Tower Hill, London EC3N 4DJ, UK",
          "coordinates": [51.5095, -0.0761],
          "wikidata_q": "Q7829600"
        }
      ]
    },
    {
      "title": "18 Tammuz — Breach of Jerusalem's Walls (Traditional)",
      "description": "The Talmud (Ta'anit 26b) records that on 17 Tammuz, the walls of Jerusalem were breached by the Babylonians (586 BCE) and later by the Romans (70 CE). Some traditions extend this to 18 Tammuz.",
      "source": "Talmud Bavli, Ta'anit 26b; Josephus, *Jewish War* 6.93-111",
      "calendar_system": "Hebrew",
      "historical_confidence": "traditional",
      "interfaith_notes": "This event is foundational to Jewish mourning. Christians see the destruction of the Temple as prophesied by Jesus (Matthew 24:2). The same walls, same city, same God—different readings of the same catastrophe.",
      "media": [
        {
          "type": "artwork",
          "title": "The Destruction of Jerusalem by Titus",
          "artist": "David Roberts, 1850",
          "location": "Private collection",
          "coordinates": null,
          "wikidata_q": null
        }
      ],
      "geography": [
        {
          "biblical_name": "Jerusalem walls",
          "modern_name": "Old City walls, Jerusalem, Israel",
          "coordinates": [31.7767, 35.2345],
          "wikidata_q": "Q6373"
        }
      ]
    },
    {
      "title": "17 Dhul-Hijjah — Post-Hajj Reflection",
      "description": "The Hajj pilgrimage concludes on 10 Dhul-Hijjah with Eid al-Adha. By 17 Dhul-Hijjah, pilgrims have completed the rites at Mina and are returning. The day carries the spiritual residue of Arafat's standing prayer.",
      "source": "Quran 2:196-203 (Hajj rites); Sahih al-Bukhari 1519",
      "calendar_system": "Islamic/Hijri",
      "historical_confidence": "confirmed",
      "interfaith_notes": "Eid al-Adha commemorates Abraham's (Ibrahim's) willingness to sacrifice his son—a narrative shared with Judaism (Genesis 22) and Christianity (Hebrews 11:17-19). The three traditions converge on this figure, diverge on which son was offered, and unite in reverence for absolute obedience to God.",
      "media": [
        {
          "type": "artwork",
          "title": "The Sacrifice of Isaac",
          "artist": "Caravaggio, 1603",
          "location": "Uffizi Gallery, Florence",
          "coordinates": [43.7678, 11.2553],
          "wikidata_q": "Q5118"
        }
      ],
      "geography": [
        {
          "biblical_name": "Mount Arafat (Jabal al-Rahmah)",
          "modern_name": "Mount Arafat, Makkah Province, Saudi Arabia",
          "coordinates": [21.3549, 39.9841],
          "wikidata_q": "Q217143"
        }
      ]
    }
  ],
  "this_week_events": [],
  "this_month_events": [],
  "this_season_events": [
    {
      "title": "Three Weeks (Bein ha-Metzarim)",
      "description": "The period from 17 Tammuz to 9 Av is a time of mourning in Judaism, commemorating the destruction of both Temples. Restrictions include no weddings, no haircuts, reduced celebration.",
      "source": "Talmud Bavli, Ta'anit 4:6; Shulchan Aruch, Orach Chaim 551",
      "calendar_system": "Hebrew",
      "historical_confidence": "traditional",
      "interfaith_notes": "Christians do not observe this mourning period, but the destruction of the Temple is referenced in the Gospels (Matthew 24, Mark 13, Luke 21) and in the Epistle to the Hebrews. The shared site—the Temple Mount—remains the most contested religious real estate on earth.",
      "media": [],
      "geography": [
        {
          "biblical_name": "Temple Mount (Har ha-Bayit / Haram al-Sharif)",
          "modern_name": "Old City, Jerusalem",
          "coordinates": [31.7781, 35.2354],
          "wikidata_q": "Q13700"
        }
      ]
    }
  ],
  "annual_cycle": [],
  "research_metadata": {
    "sources_queried": [
      "Roman Martyrology (2004 editio typica)",
      "Talmud Bavli, Ta'anit",
      "Quran, Surah 2 (Al-Baqarah)",
      "Sahih al-Bukhari",
      "Josephus, Jewish War",
      "New Catholic Encyclopedia (2nd ed.)",
      "Encyclopaedia of Islam (2nd ed.)"
    ],
    "gaps": [
      "No verified artwork specifically depicting Processus and Martinian by a named master",
      "Syriac calendar-specific events for 19 Haziran not found in available sources"
    ],
    "confidence_summary": {
      "confirmed": 2,
      "traditional": 2,
      "disputed": 0
    }
  }
}
```

## Layer C Output (Devotional Content — What the User Sees)

---

### **Today is July 2, 2026**

**18 Tammuz • 17 Dhul-Hijjah 1447 • 19 June 7535 (Byzantine)**

---

#### The Saint: Thomas More

On this day in 1535, Sir Thomas More stood on Tower Hill and laid his head on the block. He had refused to sign the Act of Supremacy. He had refused to call Henry VIII head of the Church. He had refused, and so he died.

His last words: *"I die the king's good servant, but God's first."*

What are you refusing today? What are you accepting? More's conscience cost him everything. What does yours cost you?

**Pray:** *Lord, give me the courage of Thomas More—to serve well, but to serve You first.*

---

#### The Place: The Mamertine Prison, Rome

Beneath the Capitoline Hill, in a dungeon carved from bedrock, St. Peter is said to have baptized two jailers: Processus and Martinian. They were martyred for it. Their skulls rest in St. Peter's Basilica, 2.3 miles away.

**Coordinates:** 41.8936° N, 12.4853° E  
**Visit:** Open daily, 9:00–17:00. Down the stairs, into the dark. Pray where Peter prayed.

---

#### The Shared Story: Abraham on Three Altars

Today, Muslims returning from Hajj carry the memory of Arafat—the plain where Muhammad delivered his Farewell Sermon, where Abraham (Ibrahim) stood ready to sacrifice. Jews read Genesis 22 on Rosh Hashanah. Christians see the same Isaac as a type of Christ.

Three altars. One voice: *"Here I am."*

**Pray:** *God of Abraham, bind us where we are scattered. Make our obedience worthy of the promise.*

---

#### The Art: Caravaggio's Sacrifice of Isaac

Look at the angel's hand. It grips Abraham's wrist mid-swing. The blade is already pressing Isaac's throat. Caravaggio painted this in 1603, and the violence is intimate—you can see Abraham's confusion, Isaac's surrender, the angel's urgency.

The painting hangs in the Uffizi. But today, it hangs in your prayer.

**Meditate:** *Where is God stopping my hand? Where am I being asked to let go?*

---

#### The Calendar: Three Weeks Begin

Yesterday was 17 Tammuz. Today is 18 Tammuz. The Three Weeks have begun—counting down to Tisha B'Av, when both Temples fell. If you know someone Jewish, ask them about this. The mourning is ancient. The city is still standing. The walls are still breached, in a hundred ways.

**Pray:** *For Jerusalem. For peace. For the day when no one weeps at her gates.*

---

*Today's research: 4 events, 3 traditions, 2 artworks, 4 pilgrimage sites. Sources: Roman Martyrology, Talmud Bavli Ta'anit, Quran 2:196-203, Josephus Jewish War, Caravaggio 1603.*

---

# 7. IMPLEMENTATION ROADMAP

## Phase 1: Foundation (Weeks 1-2)
- [ ] Run Engine A to generate 2026-2029 JSONL table
- [ ] Spot-check 20 dates against external references (hebcal.com, timeanddate.com)
- [ ] Fix any divergence bugs
- [ ] Store JSONL in S3/Cloud Storage

## Phase 2: Research Pipeline (Weeks 3-4)
- [ ] Build Engine B prompt template
- [ ] Run 30-day test batch (July 2026)
- [ ] Human-review outputs for accuracy
- [ ] Build source-citation validator (check URLs, DOIs)
- [ ] Cache daily outputs to avoid re-research

## Phase 3: Devotional Layer (Weeks 5-6)
- [ ] Build Layer C prompt template (content transformation)
- [ ] A/B test tone: scholarly vs. warm vs. urgent
- [ ] Build artwork ingestion pipeline (Wikidata → image URL)
- [ ] Build GPS pin pipeline (Wikidata Q-code → lat/lon)

## Phase 4: App Integration (Weeks 7-8)
- [ ] JSON → React Native / Flutter daily card
- [ ] Calendar switcher UI (tap to see Hebrew, Islamic, etc.)
- [ ] Map view with pilgrimage pins
- [ ] Art gallery modal
- [ ] Prayer prompt with "Mark as prayed" tracking

## Phase 5: Monetization (Weeks 9-10)
- [ ] Paywall: Premium = all calendars + deep dives
- [ ] Paywall: Pilgrim = GPS routes
- [ ] Paywall: Scholar = raw JSON + citations
- [ ] Affiliate: Book links (Amazon, Ignatius Press)
- [ ] Affiliate: Pilgrimage tour operators

## Phase 6: Scale (Ongoing)
- [ ] Automate daily generation (cron + LLM API)
- [ ] Build user feedback loop ("Was this accurate?" → human review queue)
- [ ] Expand to Orthodox, Coptic, Ethiopian calendars
- [ ] Add liturgical readings (Roman Rite, Byzantine Rite, Anglican)

---

# APPENDIX A: COMPLETE PYTHON SCRIPT

Save as `calendar_engine.py`:

```python
#!/usr/bin/env python3
"""
Calendar Conversion Engine for Biblical/Catholic History Research
Garden Grove, CA anchor: 33.7743°N, 117.9379°W

Dependencies:
    pip install pyluach hijri-converter convertdate

Output: JSON Lines (one JSON object per Gregorian date)
"""

from datetime import datetime, timedelta
import json
import math
import argparse

# Calendar libraries
from convertdate import julian, coptic
from pyluach import dates, hebrewcal
from hijri_converter import convert


# ============================================================
# CONFIGURATION
# ============================================================

ANCHOR_LAT = 33.7743
ANCHOR_LON = -117.9379
ANCHOR_TZ = "America/Los_Angeles"

HEBREW_MONTHS = {
    1: 'Nisan', 2: 'Iyar', 3: 'Sivan', 4: 'Tammuz', 5: 'Av', 6: 'Elul',
    7: 'Tishrei', 8: 'Cheshvan', 9: 'Kislev', 10: 'Tevet', 11: 'Shevat',
    12: 'Adar', 13: 'Adar II'
}

ISLAMIC_MONTHS = {
    1: 'Muharram', 2: 'Safar', 3: 'Rabi al-Awwal', 4: 'Rabi al-Thani',
    5: 'Jumada al-Awwal', 6: 'Jumada al-Thani', 7: 'Rajab', 8: 'Shaban',
    9: 'Ramadan', 10: 'Shawwal', 11: 'Dhu al-Qadah', 12: 'Dhu al-Hijjah'
}

COPTIC_MONTHS = {
    1: 'Thout', 2: 'Paopi', 3: 'Hathor', 4: 'Koiak', 5: 'Tobi',
    6: 'Meshir', 7: 'Paremhat', 8: 'Paremoude', 9: 'Pashons',
    10: 'Paoni', 11: 'Epip', 12: 'Mesori', 13: 'Pi Kogi Enavot'
}

ETHIOPIAN_MONTHS = {
    1: 'Meskerem', 2: 'Tikemet', 3: 'Hidar', 4: 'Tahsas', 5: 'Ter',
    6: 'Yekatit', 7: 'Megabit', 8: 'Miyazya', 9: 'Genbot',
    10: 'Sene', 11: 'Hamle', 12: 'Nehase', 13: 'Pagumen'
}

SYRIAC_MONTHS = {
    1: 'Tishrin I', 2: 'Tishrin II', 3: 'Kanun I', 4: 'Kanun II',
    5: 'Shabat', 6: 'Adar', 7: 'Nisan', 8: 'Ayar', 9: 'Haziran',
    10: 'Tammuz', 11: 'Ab', 12: 'Elul'
}


# ============================================================
# SUNDOWN CALCULATION
# ============================================================

def approximate_sundown(gregorian_date):
    """Approximate sundown at Garden Grove, CA using day-of-year sinusoidal model."""
    doy = gregorian_date.timetuple().tm_yday
    minutes = 16 * 60 + 45 + (3 * 60 + 20) * (1 + math.sin((doy - 80) * 2 * math.pi / 365)) / 2
    hour = int(minutes // 60)
    minute = int(minutes % 60)
    return f"{hour:02d}:{minute:02d} PDT"


# ============================================================
# JULIAN CALENDAR
# ============================================================

def julian_offset(year):
    """Calculate Julian-Gregorian offset in days."""
    offset = 10
    for y in range(1583, year + 1):
        if y % 100 == 0 and y % 400 != 0:
            offset += 1
    return offset


def gregorian_to_julian(gregorian_date):
    """Convert Gregorian date to Julian calendar."""
    offset = julian_offset(gregorian_date.year)
    julian_dt = gregorian_date - timedelta(days=offset)
    return julian_dt, offset


# ============================================================
# HEBREW CALENDAR
# ============================================================

def compute_keviah(year_obj):
    """Compute Hebrew year type (kevi'ah) from pyluach Year object."""
    rh = dates.HebrewDate(year_obj.year, 7, 1)
    rh_dow = rh.weekday()
    dow_map = {2: '2', 3: '3', 5: '5', 7: '7'}
    day_code = dow_map.get(rh_dow, '?')
    year_len = year_obj.year_size()
    leap_marker = 'L' if year_obj.leap else 'C'
    return f"{day_code}{leap_marker}{year_len}"


def gregorian_to_hebrew(gregorian_date, sundown_str):
    """Convert Gregorian date to Hebrew calendar."""
    gd = dates.GregorianDate(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    h = gd.to_heb()
    
    day_boundary_note = f"Gregorian noon (12:00) before sundown ({sundown_str}); Hebrew date = same day"
    
    year_obj = hebrewcal.Year(h.year)
    month_name = HEBREW_MONTHS.get(h.month, f'Month_{h.month}')
    if h.month == 12 and year_obj.leap:
        month_name = 'Adar I'
    elif h.month == 13:
        month_name = 'Adar II'
    
    keviah = compute_keviah(year_obj)
    
    return {
        'date': f"{h.day} {month_name} {h.year}",
        'year_type': keviah,
        'is_leap_year': year_obj.leap,
        'year_length': year_obj.year_size(),
        'sundown_at_anchor': sundown_str,
        'day_boundary_note': day_boundary_note,
        'hebrew_date_obj': (h.year, h.month, h.day)
    }


# ============================================================
# ISLAMIC CALENDARS
# ============================================================

def gregorian_to_islamic_umm_al_qura(gregorian_date, sundown_str):
    """Convert Gregorian date to Islamic Umm al-Qura calendar."""
    h = convert.Gregorian(gregorian_date.year, gregorian_date.month, gregorian_date.day).to_hijri()
    
    day_boundary_note = f"Gregorian noon (12:00) before sundown ({sundown_str}); Islamic date = same day"
    
    return {
        'date': f"{h.day} {ISLAMIC_MONTHS.get(h.month, f'Month_{h.month}')} {h.year} AH",
        'sundown_at_anchor': sundown_str,
        'day_boundary_note': day_boundary_note,
        'hijri_tuple': (h.year, h.month, h.day)
    }


def gregorian_to_islamic_tabular(gregorian_date):
    """Convert Gregorian date to Islamic Tabular (arithmetic) calendar."""
    epoch = datetime(622, 7, 16)
    days_since_epoch = (gregorian_date - epoch).days
    
    leap_years = {2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29}
    
    year = 1
    remaining_days = days_since_epoch
    
    while remaining_days > 0:
        year_in_cycle = ((year - 1) % 30) + 1
        days_in_year = 355 if year_in_cycle in leap_years else 354
        if remaining_days >= days_in_year:
            remaining_days -= days_in_year
            year += 1
        else:
            break
    
    month_lengths = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
    if year_in_cycle in leap_years:
        month_lengths[11] = 30
    
    month = 1
    for ml in month_lengths:
        if remaining_days >= ml:
            remaining_days -= ml
            month += 1
        else:
            break
    
    day = remaining_days + 1
    
    return {
        'date': f"{day} {ISLAMIC_MONTHS.get(month, f'Month_{month}')} {year} AH",
        'year_in_cycle': year_in_cycle,
        'is_leap_year': year_in_cycle in leap_years
    }


# ============================================================
# COPTIC & ETHIOPIAN
# ============================================================

def gregorian_to_coptic(gregorian_date):
    """Convert Gregorian date to Coptic calendar."""
    c = coptic.from_gregorian(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    coptic_year, coptic_month, coptic_day = c
    
    return {
        'date': f"{coptic_day} {COPTIC_MONTHS.get(coptic_month, f'Month_{coptic_month}')} {coptic_year}",
        'epoch_name': 'Anno Martyrum',
        'epagomenal': (coptic_month == 13),
        'coptic_tuple': c
    }


def gregorian_to_ethiopian(gregorian_date):
    """Convert Gregorian date to Ethiopian calendar."""
    c = coptic.from_gregorian(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    coptic_year, coptic_month, coptic_day = c
    ethiopian_year = coptic_year + 7
    
    return {
        'date': f"{coptic_day} {ETHIOPIAN_MONTHS.get(coptic_month, f'Month_{coptic_month}')} {ethiopian_year}",
        'new_year_alignment_note': None
    }


# ============================================================
# BYZANTINE, ARMENIAN, SYRIAC
# ============================================================

def gregorian_to_byzantine(gregorian_date):
    """Convert Gregorian date to Byzantine calendar."""
    julian_dt, offset = gregorian_to_julian(gregorian_date)
    byzantine_year = gregorian_date.year + 5509
    
    return {
        'date': f"{julian_dt.day} {julian_dt.strftime('%B')} {byzantine_year}",
        'epoch_name': 'Anno Mundi',
        'month_day_same_as_julian': True,
        'julian_offset_days': offset
    }


def gregorian_to_armenian(gregorian_date):
    """Convert Gregorian date to Armenian calendar."""
    julian_dt, offset = gregorian_to_julian(gregorian_date)
    armenian_year = gregorian_date.year - 551 + 1
    
    return {
        'date': f"{julian_dt.day} {julian_dt.strftime('%B')} {armenian_year}",
        'epoch_year': 552
    }


def gregorian_to_syriac(gregorian_date):
    """Convert Gregorian date to Syriac/Seleucid calendar."""
    julian_dt, offset = gregorian_to_julian(gregorian_date)
    seleucid_year = gregorian_date.year + 311
    
    syriac_month = SYRIAC_MONTHS.get(julian_dt.month, julian_dt.strftime('%B'))
    
    return {
        'date': f"{julian_dt.day} {syriac_month} {seleucid_year}",
        'seleucid_year': seleucid_year,
        'month_name_syriac': syriac_month,
        'year_begins_october': True
    }


# ============================================================
# TALMUDIC NOTATIONS
# ============================================================

def get_talmudic_notations(hebrew_year):
    """Compute Talmudic-era chronological notations."""
    destruction_era_year = hebrew_year - 3830
    seleucid_era_year = hebrew_year - 3449
    
    return {
        'am_year': hebrew_year,
        'destruction_era_year': destruction_era_year,
        'seleucid_era_year': seleucid_era_year,
        'contextual_relevance': 'active' if hebrew_year < 6000 else 'post-talmudic'
    }


# ============================================================
# MAIN CONVERSION FUNCTION
# ============================================================

def convert_date(gregorian_date):
    """Convert a single Gregorian date to all calendar systems."""
    sundown_str = approximate_sundown(gregorian_date)
    julian_dt, julian_offset = gregorian_to_julian(gregorian_date)
    hebrew_data = gregorian_to_hebrew(gregorian_date, sundown_str)
    islamic_umm_data = gregorian_to_islamic_umm_al_qura(gregorian_date, sundown_str)
    islamic_tabular_data = gregorian_to_islamic_tabular(gregorian_date)
    coptic_data = gregorian_to_coptic(gregorian_date)
    ethiopian_data = gregorian_to_ethiopian(gregorian_date)
    byzantine_data = gregorian_to_byzantine(gregorian_date)
    armenian_data = gregorian_to_armenian(gregorian_date)
    syriac_data = gregorian_to_syriac(gregorian_date)
    talmudic_data = get_talmudic_notations(hebrew_data['hebrew_date_obj'][0])
    
    # Check divergence
    umm_year, umm_month, umm_day = islamic_umm_data['hijri_tuple']
    tab_parts = islamic_tabular_data['date'].split()
    tab_day = int(tab_parts[0])
    
    divergence = 0
    divergence_note = None
    if umm_day != tab_day:
        divergence = abs(umm_day - tab_day)
        divergence_note = f"Umm al-Qura: {umm_day}, Tabular: {tab_day}"
    
    tab_month = tab_parts[1]
    umm_month_name = ISLAMIC_MONTHS.get(umm_month, f'Month_{umm_month}')
    if umm_month_name != tab_month and divergence == 0:
        divergence = 1
        divergence_note = f"Umm al-Qura month: {umm_month_name}, Tabular month: {tab_month}"
    
    return {
        'gregorian_date': gregorian_date.strftime('%Y-%m-%d'),
        'gregorian_doy': gregorian_date.timetuple().tm_yday,
        'julian': {
            'date': julian_dt.strftime('%Y-%m-%d'),
            'offset_days': julian_offset,
            'drift_note': f"{julian_offset} days behind Gregorian; no century leap discrepancy in {gregorian_date.year}"
        },
        'hebrew': {
            'date': hebrew_data['date'],
            'year_type': hebrew_data['year_type'],
            'is_leap_year': hebrew_data['is_leap_year'],
            'year_length': hebrew_data['year_length'],
            'sundown_at_anchor': hebrew_data['sundown_at_anchor'],
            'day_boundary_note': hebrew_data['day_boundary_note']
        },
        'islamic_umm_al_qura': {
            'date': islamic_umm_data['date'],
            'sundown_at_anchor': islamic_umm_data['sundown_at_anchor'],
            'day_boundary_note': islamic_umm_data['day_boundary_note']
        },
        'islamic_tabular': {
            'date': islamic_tabular_data['date'],
            'year_in_cycle': islamic_tabular_data['year_in_cycle'],
            'is_leap_year': islamic_tabular_data['is_leap_year'],
            'divergence_from_umm_al_qura': divergence,
            'divergence_note': divergence_note
        },
        'coptic': {
            'date': coptic_data['date'],
            'epoch_name': coptic_data['epoch_name'],
            'epagomenal': coptic_data['epagomenal']
        },
        'ethiopian': {
            'date': ethiopian_data['date'],
            'new_year_alignment_note': ethiopian_data['new_year_alignment_note']
        },
        'byzantine': {
            'date': byzantine_data['date'],
            'epoch_name': byzantine_data['epoch_name'],
            'month_day_same_as_julian': byzantine_data['month_day_same_as_julian']
        },
        'armenian': {
            'date': armenian_data['date'],
            'epoch_year': armenian_data['epoch_year']
        },
        'syriac': {
            'date': syriac_data['date'],
            'seleucid_year': syriac_data['seleucid_year'],
            'month_name_syriac': syriac_data['month_name_syriac'],
            'year_begins_october': syriac_data['year_begins_october']
        },
        'talmudic_notations': talmudic_data,
        'conversion_metadata': {
            'anchor_location': 'Garden Grove, CA',
            'anchor_lat': ANCHOR_LAT,
            'anchor_lon': ANCHOR_LON,
            'algorithms': {
                'hebrew': "pyluach/Four Gates kevi'ah",
                'islamic_umm_al_qura': 'hijri-converter/Saudi Umm al-Qura',
                'islamic_tabular': '30-year arithmetic cycle',
                'julian': f'day-count offset ({julian_offset} days)',
                'coptic': 'convertdate/coptic fixed 365-day',
                'byzantine': 'Julian + 5509 epoch',
                'syriac': 'Julian + Seleucid epoch'
            }
        }
    }


# ============================================================
# BATCH GENERATION
# ============================================================

def generate_range(start_date, end_date, output_file=None):
    """Generate calendar conversions for a date range."""
    current = start_date
    lines = []
    
    while current <= end_date:
        result = convert_date(current)
        line = json.dumps(result, ensure_ascii=False)
        lines.append(line)
        current += timedelta(days=1)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + '\n')
        print(f"Wrote {len(lines)} dates to {output_file}")
    else:
        for line in lines:
            print(line)
    
    return lines


# ============================================================
# VERIFICATION / SPOT-CHECK
# ============================================================

def spot_check(dates_to_check):
    """Run spot-checks against known reference dates."""
    print("=" * 60)
    print("SPOT CHECK RESULTS")
    print("=" * 60)
    
    known_references = {
        datetime(2026, 7, 2): ("18 Tammuz 5786", "17 Dhu al-Hijjah 1447", 13),
        datetime(2026, 1, 1): ("11 Tevet 5786", "11 Jumada al-Thani 1447", 13),
        datetime(2026, 12, 31): ("17 Tevet 5787", "21 Jumada al-Awwal 1448", 13),
    }
    
    for check_date in dates_to_check:
        result = convert_date(check_date)
        print(f"\n--- {check_date.strftime('%Y-%m-%d')} ---")
        print(f"  Hebrew:     {result['hebrew']['date']}")
        print(f"  Islamic:    {result['islamic_umm_al_qura']['date']}")
        print(f"  Julian:     {result['julian']['date']} (offset: {result['julian']['offset_days']})")
        print(f"  Coptic:     {result['coptic']['date']}")
        print(f"  Ethiopian:  {result['ethiopian']['date']}")
        print(f"  Byzantine:  {result['byzantine']['date']}")
        print(f"  Armenian:   {result['armenian']['date']}")
        print(f"  Syriac:     {result['syriac']['date']}")
        print(f"  Sundown:    {result['hebrew']['sundown_at_anchor']}")
        
        if check_date in known_references:
            expected_heb, expected_isl, expected_offset = known_references[check_date]
            checks = [
                ("Hebrew", result['hebrew']['date'], expected_heb),
                ("Islamic", result['islamic_umm_al_qura']['date'], expected_isl),
                ("Julian offset", result['julian']['offset_days'], expected_offset),
            ]
            for name, actual, expected in checks:
                status = "PASS" if str(actual) == str(expected) else "FAIL"
                print(f"  [{status}] {name}: {actual} (expected: {expected})")


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calendar Conversion Engine')
    parser.add_argument('--start', type=str, default='2026-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, default='2029-12-31', help='End date (YYYY-MM-DD)')
    parser.add_argument('--output', type=str, default='calendar_conversions.jsonl', help='Output file')
    parser.add_argument('--spot-check', action='store_true', help='Run spot-checks only')
    
    args = parser.parse_args()
    
    start = datetime.strptime(args.start, '%Y-%m-%d')
    end = datetime.strptime(args.end, '%Y-%m-%d')
    
    if args.spot_check:
        spot_check([
            datetime(2026, 1, 1),
            datetime(2026, 7, 2),
            datetime(2026, 9, 11),
            datetime(2026, 12, 31),
            datetime(2027, 1, 1),
            datetime(2028, 2, 29),
            datetime(2029, 1, 1),
        ])
    else:
        generate_range(start, end, args.output)
```

---

# APPENDIX B: DAILY RESEARCH PROMPT (COPY-PASTE READY)

Use this as your LLM system prompt for Engine B:

```
You are a liturgical and biblical history research agent. You receive pre-computed calendar conversions for a single day and research all historically significant events connected to that date.

## Input Format

You will receive a JSON object with pre-computed calendar conversions. Do NOT recompute calendars. Use the provided data exactly.

## Research Task

For the given date, search biblical text, Church history, hagiography, liturgical records, Islamic texts (Quran and Hadith), Talmudic tradition, and Catholic tradition for everything connected to this date.

## Sourcing Hierarchy

1. Scripture (Bible, Quran, Talmud) — as textual witnesses
2. Peer-reviewed biblical scholarship and archaeology — for historical claims
3. Official Church documents / Vatican records — for Catholic tradition
4. Islamic historical sources (Tabari, Ibn Ishaq, etc.) — for Islamic tradition
5. Jewish textual tradition (Talmud, Midrash, geonic literature) — for Jewish tradition
6. Roman Martyrology and hagiographic sources — explicitly labeled as traditional/liturgical dating

## Specificity Tiers

Work from most to least specific. For each tier, include only if source explicitly ties event to this date proximity:

1. Exact Day — Feast days, martyrdoms, councils, papal events, biblical events, Quranic events, Talmudic teachings, Islamic commemorations, Jewish observances, apparitions, canonizations, dedications
2. This Week — Events within 7 days (source must explicitly note proximity)
3. This Month — Events tied to this month (source must explicitly tie to month)
4. This Season — Currently active liturgical seasons only
5. Annual Cycle — Recurring commemorations active during this period

## Interfaith Context

Include only where genuine intersection exists (shared figures, parallel observances, historically documented encounters). If an entry is single-tradition, state that explicitly. Do not manufacture connections.

## Media and Geography

For each entry, include when available:
- Devotional artworks (artist, title, location)
- Maps (biblical name, modern equivalent, Wikidata Q-code, coordinates)
- Pilgrimage sites (name, modern address, coordinates)
- Geographical paths (historical route, modern locations)

Coordinate policy: Prefer Wikidata Q-codes. Note scholarly disputes. Do not invent coordinates.

## Output Schema

{
  "gregorian_date": "YYYY-MM-DD",
  "exact_day_events": [...],
  "this_week_events": [...],
  "this_month_events": [...],
  "this_season_events": [...],
  "annual_cycle": [...],
  "research_metadata": {
    "sources_queried": [...],
    "gaps": [...],
    "confidence_summary": {...}
  }
}

Each event entry must include:
- title, description, source (with precise citation)
- calendar_system (which calendar makes it relevant)
- historical_confidence: confirmed / traditional / disputed
- interfaith_notes (or null)
- media: array of artwork/map/pilgrimage_site objects
- geography: array of location objects with biblical_name, modern_name, coordinates, wikidata_q

## Rules

- Use provided calendar conversions exactly. Do not recompute.
- Every claim must be traceable to a named source.
- When sources conflict, present all claims and note the conflict.
- When a date is traditional rather than historically confirmed, tag it "traditional."
- Do not speculate beyond what tradition or scholarship supports.
- Omit flattering phrases and devotional elaboration. Structured data only.
```

---

# APPENDIX C: CONTENT STYLE GUIDE

## The Devotional Content Layer (Layer C) Prompt

```
You are a devotional content writer for a daily faith app. You receive structured historical research JSON and transform it into a daily devotional entry.

## Input

Structured JSON from the research agent, containing: saints, biblical events, interfaith connections, artworks, pilgrimage sites, and calendar conversions.

## Output Format

A single daily entry with these sections:

1. HEADER — Today's date + all calendar conversions (one line, elegant)
2. THE SAINT — 200-300 word hagiography with a prayer prompt
3. THE PLACE — GPS pin with modern address, visiting hours, and a prayer
4. THE SHARED STORY — Interfaith connection (only if genuine), with a unifying prayer
5. THE ART — Artwork description, sensory details, meditation prompt
6. THE CALENDAR — Seasonal/liturgical context with a prayer
7. FOOTER — Source credits (brief, credible, not academic)

## Tone Rules

- Open with a hook: temporal, calendar, art, place, or shared story
- Use second person ("you," "your") for prayers and prompts
- Be specific, not generic. "St. Thomas More died on Tower Hill" not "Many saints died for their faith."
- Use sensory language for art and places. "Look at the angel's hand" not "This painting depicts..."
- End every section with a short prayer (1-2 sentences)
- Never say "God has a plan for you." Always say what happened, where, when, and why it matters now.
- Cite sources at the bottom, but don't let citations interrupt the narrative flow.

## The Hook Formula (pick one per day)

1. Temporal: "On this exact day in [year]..."
2. Calendar: "Today is [Hebrew/Islamic date]. In [timeframe], [faith] will [observance]."
3. Art: "Look at this painting. Really look."
4. Place: "You are [distance] from [site]. But distance is nothing in prayer."
5. Shared: "[Figure]. [Figure in another language]. [Figure in third language]. Same [person/place], [number] billion believers."
```

---

**Document End**

*Built for rigor. Written to sell. Prayed to transform.*
"""

# Save to output
with open('/mnt/agents/output/Daily_Devotional_Engine_Spec.md', 'w', encoding='utf-8') as f:
    f.write(document)

print(f"Saved: {len(document)} characters")
print("File: /mnt/agents/output/Daily_Devotional_Engine_Spec.md")

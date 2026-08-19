# Flagship Content Slate
Updated: 2026-07-03

## Purpose

The first content batch should prove the product, not merely fill dates. Use this slate to create screenshots, TestFlight demos, landing pages, audio tests, Vietnamese translation samples, and premium route teasers.

Pick entries that show:

- Catholic recognition.
- Strong story hook.
- Sacred art potential.
- Real map pin.
- Source/confidence clarity.
- Optional Sacred Context when genuine.
- Vietnamese translation viability.

## Selection Rules

Each flagship entry should have:

- A memorable headline.
- A Catholic event or saint tied to the date.
- At least one credible source.
- A location with modern coordinates where possible.
- One visual/art object or architecture image.
- A short prayer/reflection.
- A confidence badge.
- A premium upsell angle: archive, art, audio, or route.

Do not pick entries only because they are famous. Pick entries that make the app feel inevitable.

## Core 30-Day Slate

This is a proposed flagship slate. Dates should be verified before production.

| Date | Entry | Why it matters | Asset angle | Premium hook |
|---|---|---|---|---|
| Jan 1 | Mary, Mother of God | Major Catholic solemnity, Marian identity | Marian art, Rome churches | Marian route |
| Jan 25 | Conversion of St. Paul | Dramatic story and strong art history | Caravaggio, Damascus/Rome | Art gallery |
| Feb 2 | Presentation of the Lord | Temple, Mary, Simeon, candle imagery | Temple/Jerusalem art | Sacred Context |
| Feb 11 | Our Lady of Lourdes | Pilgrimage utility is obvious | Lourdes grotto/map | Pilgrim tier |
| Mar 19 | St. Joseph | Broad Catholic recognition | Joseph iconography | Family/home angle |
| Mar 25 | Annunciation | Art-rich, Marian, major feast | Fra Angelico, Nazareth | Marian route |
| Apr 25 | St. Mark | Venice/Alexandria geography | Basilica/map | Travel hook |
| Apr 29 | St. Catherine of Siena | Strong female saint, Rome/Siena | Siena/Rome | Archive/art |
| May 1 | St. Joseph the Worker | Labor, modern relevance | Workshop/Joseph art | Daily habit |
| May 13 | Our Lady of Fatima | Pilgrimage and modern devotion | Fatima map | Pilgrim tier |
| May 31 | Visitation | Marian, biblical geography | Ein Kerem | Marian route |
| Jun 13 | St. Anthony of Padua | Famous, folk devotion, strong search | Padua/Lisbon | Archive search |
| Jun 24 | Nativity of John the Baptist | Calendar-specific, biblical | Ein Kerem/Jordan | Sacred Context |
| Jun 29 | Sts. Peter and Paul | Rome anchor, major solemnity | St. Peter's/St. Paul's | Rome route |
| Jul 3 | St. Thomas the Apostle | India route, doubt/faith hook | Chennai/Mylapore | Global map |
| Jul 11 | St. Benedict | Europe, monasticism, patronage | Monte Cassino | Pilgrim route |
| Jul 22 | St. Mary Magdalene | Strong story, art, contested history | Sainte-Baume/art | Confidence labels |
| Jul 25 | St. James | Camino/Santiago | Santiago route | Pilgrim tier |
| Jul 31 | St. Ignatius of Loyola | Founder story, Spain/Rome | Loyola/Rome | Route pack |
| Aug 6 | Transfiguration | Art and theology, mountain geography | Raphael/Tabor | Art gallery |
| Aug 15 | Assumption of Mary | Major Marian solemnity | Marian art | Annual upgrade |
| Aug 28 | St. Augustine | Conversion, North Africa, writing | Hippo/Milan/Rome | Source depth |
| Sep 14 | Exaltation of the Holy Cross | Relic/geography/history | Jerusalem/Rome | Sacred places |
| Sep 29 | Archangels | Famous feast, art-rich | Michael/Gabriel/Raphael art | Audio/art |
| Oct 4 | St. Francis of Assisi | High recognition, pilgrimage | Assisi | Pilgrim route |
| Oct 7 | Our Lady of the Rosary | Catholic devotional connection | Lepanto/Mary/rosary art | Archive/audio |
| Oct 15 | St. Teresa of Avila | Mystic, Spain route | Avila | Route pack |
| Oct 22 | St. John Paul II | Modern pope, pilgrimage | Krakow/Rome | Modern Catholic hook |
| Nov 1 | All Saints | Universal Catholic entry point | Pantheon/saints art | App identity |
| Dec 12 | Our Lady of Guadalupe | Huge Americas/Vietnamese Catholic resonance | Tepeyac | Pilgrim/art |

## Screenshot-Grade Entries

Use these for visual demos:

### Sts. Peter and Paul

Why:

- Rome map route is obvious.
- Catholic identity is unmistakable.
- Art/architecture is abundant.
- Premium route hook is strong.

Today screen:

- "Today Rome remembers its two great apostles."

Map hook:

- St. Peter's Basilica, Basilica of St. Paul Outside the Walls, Mamertine Prison.

### Our Lady of Lourdes

Why:

- Pilgrimage monetization is concrete.
- Strong Catholic recognition.
- Map/travel utility is immediate.

Paywall hook:

- "Plan Lourdes with readings, art, and offline pins."

### Conversion of St. Paul

Why:

- Dramatic story.
- Caravaggio art.
- Conversion narrative without generic self-help.

Art hook:

- Caravaggio's "Conversion on the Way to Damascus."

### St. James

Why:

- Camino route makes Pilgrim tier obvious.
- Searchable and travel-adjacent.

Premium hook:

- "Open the Santiago route pack."

### Our Lady of Guadalupe

Why:

- Massive Catholic resonance.
- Strong visual identity.
- Good test for localization and global Catholic audience.

Vietnamese note:

- Needs careful Catholic terminology review.

## Content Template

Use this template for every flagship entry:

```json
{
  "date": "YYYY-MM-DD",
  "liturgical_context": "",
  "primary_title_en": "",
  "primary_title_vi": "",
  "hook_en": "",
  "hook_vi": "",
  "body_en": "",
  "body_vi": "",
  "prayer_en": "",
  "prayer_vi": "",
  "confidence": "confirmed | traditional | disputed",
  "sources": [
    {
      "title": "",
      "url": "",
      "source_type": "scripture | martyrology | church_document | scholarship | museum | other"
    }
  ],
  "art": [
    {
      "title": "",
      "artist": "",
      "year": "",
      "image_source": "",
      "license": "",
      "caption_en": "",
      "caption_vi": ""
    }
  ],
  "places": [
    {
      "name": "",
      "modern_address": "",
      "coordinates": [0, 0],
      "apple_maps_query": "",
      "route_pack_candidate": true
    }
  ],
  "sacred_context": {
    "include": false,
    "reason": "",
    "body_en": "",
    "body_vi": ""
  },
  "premium_hooks": ["archive", "map", "art", "audio", "pilgrim"]
}
```

## First Production Batch

Batch 1 should include:

- 10 flagship English entries.
- 10 Vietnamese translations reviewed by a Vietnamese Catholic.
- 10 map pins.
- 10 source sheets.
- 5 art lightbox candidates.
- 3 audio samples.
- 2 route teasers: Rome and Marian.

Do not generate all 365 days until the first 10 feel excellent.

## QA Gates

Reject an entry if:

- The date is wrong.
- The liturgical context is wrong.
- The saint/event is source-free.
- The art attribution is uncertain but labeled as confirmed.
- The map pin is approximate but presented as exact.
- The prayer sounds manipulative.
- Vietnamese translation uses generic Christian phrasing where Catholic terms are needed.
- Sacred Context is manufactured.


# Content Sprint 1 — July 3-9, 2026
**Goal:** 7 days of Catholic saint feast day content
**Output:** 7 `AnnoEntry` JSON objects
**How to use:** Copy the prompt below into Claude/ChatGPT on your iPhone. Collect the JSON output. Drop it in `data/content_batch_1/` on the project.

---

## LLM Prompt (copy this entire block)

```
You are a Catholic liturgical content writer for a daily devotional app called Anno. Generate AnnoEntry JSON for July 3-9, 2026.

CONTEXT:
- This is a Catholic-first daily devotional app
- Each day gets ONE entry (the primary feast or commemoration)
- Content must be historically accurate, sourced, and bilingual (English + Vietnamese)
- The app shows saints, feast days, and historical figures — no interfaith content

OUTPUT FORMAT (one JSON object per day, as a JSON array):

[
  {
    "id": "anno-2026-07-03",
    "date": "2026-07-03",
    "weekday": "Friday",
    "mock_priority": "real_data",
    "liturgical": {
      "rank": "Feast|Memorial|Feria|Solemnity",
      "color": "red|white|green|violet|gold",
      "title_en": "Liturgical title in English",
      "title_vi": "Tiêu đề phụng vụ bằng tiếng Việt"
    },
    "calendars": {
      "julian": "Julian date (June 20, 2026 for Jul 3)",
      "hebrew": "Hebrew date (18 Tammuz 5786 for Jul 3)",
      "islamic_umm_al_qura": "Islamic date (18 Muharram 1448 AH for Jul 3)",
      "coptic": "Coptic date (26 Paoni 1742 for Jul 3)",
      "ethiopian": "Ethiopian date (26 Sene 2018 for Jul 3)"
    },
    "primary": {
      "type": "saint_feast|memorial|feria|marian_day",
      "title_en": "English title of the saint/day",
      "title_vi": "Tiêu đề tiếng Việt",
      "summary_en": "3-5 sentence hagiography or description. Include: who the saint was, what they did, why they matter, how they died (if martyr). Be specific — names, dates, places.",
      "summary_vi": "3-5 câu tiếng Việt. Bao gồm: thánh đó là ai, làm gì, tại sao quan trọng, cách chết (nếu tử đạo). Cụ thể — tên, ngày, nơi.",
      "confidence": "confirmed|traditional",
      "confidence_note_en": "One sentence on source quality.",
      "confidence_note_vi": "Một câu về chất lượng nguồn."
    },
    "place": {
      "name": "Name of sacred site (null if no specific location)",
      "latitude": 0.0,
      "longitude": 0.0,
      "confidence": "confirmed|traditional",
      "source_url": "Real, verifiable URL (Wikipedia, Vatican, etc.)"
    },
    "artwork": {
      "title": "Title of a real artwork depicting this saint/day",
      "maker": "Artist name",
      "date_label": "Date or period",
      "source_url": "Real Wikimedia Commons or museum URL",
      "status": "Public Domain"
    },
    "sources": [
      {
        "label": "Source name",
        "url": "Real, working URL",
        "type": "liturgical|historical|biographical"
      }
    ],
    "appHooks": {
      "hero_line_en": "One compelling hook line in English",
      "hero_line_vi": "Một câu hấp dẫn bằng tiếng Việt",
      "prayer_prompt_en": "Short prayer (1-2 sentences)",
      "prayer_prompt_vi": "Lời nguyện ngắn (1-2 câu)"
    }
  }
]

CALENDAR CONVERSIONS (use these exactly):
- Jul 3: Julian=Jun 20, Hebrew=18 Tammuz 5786, Islamic=18 Muharram 1448, Coptic=26 Paoni 1742, Ethiopian=26 Sene 2018
- Jul 4: Julian=Jun 21, Hebrew=19 Tammuz 5786, Islamic=19 Muharram 1448, Coptic=27 Paoni 1742, Ethiopian=27 Sene 2018
- Jul 5: Julian=Jun 22, Hebrew=20 Tammuz 5786, Islamic=20 Muharram 1448, Coptic=28 Paoni 1742, Ethiopian=28 Sene 2018
- Jul 6: Julian=Jun 23, Hebrew=21 Tammuz 5786, Islamic=21 Muharram 1448, Coptic=29 Paoni 1742, Ethiopian=29 Sene 2018
- Jul 7: Julian=Jun 24, Hebrew=22 Tammuz 5786, Islamic=22 Muharram 1448, Coptic=30 Paoni 1742, Ethiopian=30 Sene 2018
- Jul 8: Julian=Jun 25, Hebrew=23 Tammuz 5786, Islamic=23 Muharram 1448, Coptic=1 Epip 1742, Ethiopian=1 Hamle 2018
- Jul 9: Julian=Jun 26, Hebrew=24 Tammuz 5786, Islamic=24 Muharram 1448, Coptic=2 Epip 1742, Ethiopian=2 Hamle 2018

SAINTS TO COVER:
- Jul 3: St. Thomas, Apostle (Feast, red) — "Doubting Thomas", martyred in India
- Jul 4: St. Elizabeth of Portugal (Memorial, white) — queen, peacemaker, Third Order Franciscan
- Jul 5: St. Anthony Zaccaria (Memorial, white) — founder of the Barnabites, doctor
- Jul 6: St. Maria Goretti (Memorial, white) — virgin martyr, 11 years old, purity
- Jul 7: Bl. Pier Giorgio Frassati (Memorial, white) — young Italian, outdoorsman, servant of the poor
- Jul 8: St. Kilian (Memorial, red) — Irish missionary bishop, martyred in Germany
- Jul 9: St. Augustine Zhao Rong and Companions (Memorial, red) — Chinese martyrs

RULES:
1. Every URL must be real and verifiable. Use Wikipedia, USCCB, Vatican News, Catholic Encyclopedia.
2. Vietnamese must be grammatically correct Catholic Vietnamese. Use: "Thánh" (Saint), "Lễ kính" (Feast), "Lễ nhớ" (Memorial), "Tông đồ" (Apostle), "tử đạo" (martyr), "Đức Kitô" (Christ).
3. Artwork URLs must be real Wikimedia Commons links or museum pages.
4. Place coordinates must be real (use Google Maps or Wikipedia infobox).
5. Confidence: "confirmed" for historically documented saints, "traditional" for early hagiography.
6. Do NOT include interfaith content.
7. Output ONLY the JSON array. No commentary, no markdown, no explanation.

VALIDATE YOUR OUTPUT:
- All 7 entries present
- All fields populated (no nulls except place where no location exists)
- All URLs start with http:// or https://
- Vietnamese text contains no non-Vietnamese characters (except proper nouns)
- Summary is 3-5 sentences, not one-liner
```

---

## Checklist (after generating)

- [ ] All 7 entries present (Jul 3-9)
- [ ] Each entry has: id, date, weekday, liturgical, calendars, primary, place, artwork, sources, appHooks
- [ ] All sources are real URLs (click-test 2-3)
- [ ] All artwork URLs are real (click-test)
- [ ] Vietnamese summaries are grammatically correct
- [ ] No interfaith content
- [ ] Confidence levels are appropriate
- [ ] Place coordinates are real locations
- [ ] Save output as `data/content_batch_1/jul_03-09.json`
- [ ] Run `python tools/validate_mock_content.py data/content_batch_1/jul_03-09.json`
- [ ] Fix any validation errors

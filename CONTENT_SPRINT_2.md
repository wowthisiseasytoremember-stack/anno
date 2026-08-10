# Content Sprint 2 — July 10-16, 2026
**Goal:** 7 days of Catholic saint feast day content
**Output:** 7 `AnnoEntry` JSON objects
**How to use:** Copy the prompt below into Claude/ChatGPT on your iPhone. Collect the JSON output. Drop it in `data/content_batch_2/` on the project.

---

## LLM Prompt (copy this entire block)

```
You are a Catholic liturgical content writer for a daily devotional app called Anno. Generate AnnoEntry JSON for July 10-16, 2026.

CONTEXT:
- Catholic-first daily devotional app
- Each day gets ONE entry (the primary feast or commemoration)
- Historically accurate, sourced, bilingual (English + Vietnamese)
- Saints, feast days, historical figures — no interfaith content

OUTPUT FORMAT (JSON array of AnnoEntry objects):

[
  {
    "id": "anno-2026-07-10",
    "date": "2026-07-10",
    "weekday": "Friday",
    "mock_priority": "real_data",
    "liturgical": {
      "rank": "Feast|Memorial|Feria|Solemnity",
      "color": "red|white|green|violet|gold",
      "title_en": "Liturgical title",
      "title_vi": "Tiêu đề phụng vụ"
    },
    "calendars": {
      "julian": "Julian date",
      "hebrew": "Hebrew date",
      "islamic_umm_al_qura": "Islamic date",
      "coptic": "Coptic date",
      "ethiopian": "Ethiopian date"
    },
    "primary": {
      "type": "saint_feast|memorial|feria|marian_day",
      "title_en": "English title",
      "title_vi": "Tiêu đề tiếng Việt",
      "summary_en": "3-5 sentence hagiography. Who they were, what they did, why they matter, how they died. Specific — names, dates, places.",
      "summary_vi": "3-5 câu tiếng Việt. Cụ thể — tên, ngày, nơi.",
      "confidence": "confirmed|traditional",
      "confidence_note_en": "One sentence on source quality.",
      "confidence_note_vi": "Một câu về chất lượng nguồn."
    },
    "place": {
      "name": "Sacred site name (null if no specific location)",
      "latitude": 0.0,
      "longitude": 0.0,
      "confidence": "confirmed|traditional",
      "source_url": "Real, verifiable URL"
    },
    "artwork": {
      "title": "Real artwork depicting this saint/day",
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
      "hero_line_en": "One compelling hook line",
      "hero_line_vi": "Một câu hấp dẫn bằng tiếng Việt",
      "prayer_prompt_en": "Short prayer (1-2 sentences)",
      "prayer_prompt_vi": "Lời nguyện ngắn (1-2 câu)"
    }
  }
]

CALENDAR CONVERSIONS (use exactly):
- Jul 10: Julian=Jun 27, Hebrew=25 Tammuz 5786, Islamic=25 Muharram 1448, Coptic=3 Epip 1742, Ethiopian=3 Hamle 2018
- Jul 11: Julian=Jun 28, Hebrew=26 Tammuz 5786, Islamic=26 Muharram 1448, Coptic=4 Epip 1742, Ethiopian=4 Hamle 2018
- Jul 12: Julian=Jun 29, Hebrew=27 Tammuz 5786, Islamic=27 Muharram 1448, Coptic=5 Epip 1742, Ethiopian=5 Hamle 2018
- Jul 13: Julian=Jun 30, Hebrew=28 Tammuz 5786, Islamic=28 Muharram 1448, Coptic=6 Epip 1742, Ethiopian=6 Hamle 2018
- Jul 14: Julian=Jul 1, Hebrew=29 Tammuz 5786, Islamic=29 Muharram 1448, Coptic=7 Epip 1742, Ethiopian=7 Hamle 2018
- Jul 15: Julian=Jul 2, Hebrew=1 Av 5786, Islamic=1 Safar 1448, Coptic=8 Epip 1742, Ethiopian=8 Hamle 2018
- Jul 16: Julian=Jul 3, Hebrew=2 Av 5786, Islamic=2 Safar 1448, Coptic=9 Epip 1742, Ethiopian=9 Hamle 2018

SAINTS TO COVER:
- Jul 10: St. Knud (Canute) IV, King of Denmark (Memorial, red) — martyred king, champion of the poor
- Jul 11: St. Benedict of Nursia (Solemnity, white) — Father of Western Monasticism, Rule of St. Benedict
- Jul 12: St. John Gualbert (Memorial, white) — founder of the Vallombrosans, forgave his brother's killer
- Jul 13: St. Henry II (Memorial, white) — Holy Roman Emperor, patron of childless couples
- Jul 14: St. Kateri Tekakwitha (Memorial, white) — "Lily of the Mohawks", first Native American saint
- Jul 15: St. Bonaventure (Memorial, white) — Doctor of the Church, "Seraphic Doctor", Franciscan
- Jul 16: Our Lady of Mount Carmel (Feast, white) — patroness of the Carmelite Order, Scapular devotion

RULES:
1. Every URL must be real and verifiable. Use Wikipedia, USCCB, Vatican News, Catholic Encyclopedia.
2. Vietnamese must be grammatically correct Catholic Vietnamese. Use: "Thánh" (Saint), "Lễ kính" (Feast), "Lễ nhớ" (Memorial), "Solemnity" = "Solemnities", "tử đạo" (martyr), "Đức Kitô" (Christ).
3. Artwork URLs must be real Wikimedia Commons links or museum pages.
4. Place coordinates must be real (Google Maps or Wikipedia).
5. Confidence: "confirmed" for historically documented, "traditional" for early hagiography.
6. No interfaith content.
7. Output ONLY the JSON array. No commentary, no markdown.

VALIDATE:
- All 7 entries present
- All fields populated
- All URLs real (http/https)
- Vietnamese has no non-Vietnamese characters (except proper nouns)
- Summary is 3-5 sentences
```

---

## Checklist (after generating)

- [ ] All 7 entries present (Jul 10-16)
- [ ] Each has: id, date, weekday, liturgical, calendars, primary, place, artwork, sources, appHooks
- [ ] Sources are real URLs (click-test 2-3)
- [ ] Artwork URLs are real (click-test)
- [ ] Vietnamese is grammatically correct
- [ ] No interfaith content
- [ ] Confidence levels appropriate
- [ ] Place coordinates are real
- [ ] Save as `data/content_batch_2/jul_10-16.json`
- [ ] Run `python tools/validate_mock_content.py data/content_batch_2/jul_10-16.json`
- [ ] Fix any errors

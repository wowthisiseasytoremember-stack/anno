# Anno — External Agent Research & Structuring Prompt Pack

**Target Use Case:** Copy-pasteable prompts to hand to any external LLM or research agent (Claude, ChatGPT, DeepSeek, etc.) **without filesystem access**.  
**Ingestion Compatibility:** Outputs strict, ready-to-ingest JSON that passes Anno's automated validation gates (`tools/validate_engine_b_output.py`, `tools/validate_route_coordinates.py`, `tools/validate_devotional_pool.py`).

---

## 📋 Table of Prompts

1. [Prompt 1: Daily Sacred History Research & Bilingual Dossier (Engine B)](#prompt-1-daily-sacred-history-research--bilingual-dossier)
2. [Prompt 2: Pilgrimage Route & GPS Waypoints Pack (Pilgrim Tier)](#prompt-2-pilgrimage-route--gps-waypoints-pack)
3. [Prompt 3: Sacred Art Masterpiece Dossier & Provenance](#prompt-3-sacred-art-masterpiece-dossier--provenance)
4. [Prompt 4: 30-Day Bilingual Catholic Devotional Pool Slice](#prompt-4-30-day-bilingual-catholic-devotional-pool-slice)

---

## Prompt 1: Daily Sacred History Research & Bilingual Dossier

```markdown
You are an expert Catholic historian, hagiographer, and liturgical scholar working for Anno (a high-craft sacred history and multi-calendar app).

Your task is to conduct deep, rigorous historical research for the specified Gregorian date and return a single, strictly valid JSON object.

### Input Date:
- Gregorian Date: [INSERT_DATE: e.g. 2027-03-25]
- Day of Week: [INSERT_DAY: e.g. Thursday]

### Epistemic Rules (Strict):
1. ZERO hallucination: Every historical claim must be factual and documented.
2. Minimum 2, preferably 3+ verified primary/academic sources (USCCB, Vatican, New Advent/Catholic Encyclopedia, Alban Butler's Lives of the Saints, Acta Sanctorum, Patrologia Latina/Graeca). Do NOT use example.com.
3. Epistemic Confidence Tag: Use strictly "confirmed", "traditional", "disputed", or "contextual".
4. Liturgical Rank: Must be one of ["Solemnity", "Feast", "Memorial", "Optional Memorial", "Feria", "Sunday"].
5. Liturgical Color: Must be lowercase: ["white", "red", "green", "purple", "rose", "gold", "verdigris"].
6. Paragraph & Sentence Constraints:
   - summary_en & summary_vi: Exactly 2 to 4 sentences.
   - body_en & body_vi: At least 3 full paragraphs (separated by \n\n) detailing: (1) identity/feast origin, (2) historical biography/context, (3) theological & spiritual significance.
7. Bilingual Vietnamese Quality: Must use accurate, canonical Catholic Vietnamese ecclesiastical terminology (e.g. Lễ Trọng, Lễ Kính, Lễ Nhớ, Thánh Tử Đạo, Mầu Nhiệm, Bổn Mạng) with 100% correct Vietnamese tone marks/diacritics.

### Output JSON Format (Return ONLY raw JSON, no markdown fences, no preamble):
{
  "id": "anno-[YYYY-MM-DD]",
  "date": "[YYYY-MM-DD]",
  "weekday": "[Weekday]",
  "mock_priority": "engine_b_v1",
  "liturgical": {
    "rank": "[Rank]",
    "color": "[color]",
    "title_en": "[English Liturgical Title]",
    "title_vi": "[Vietnamese Liturgical Title]"
  },
  "calendars": {
    "julian": "[Julian Date String]",
    "hebrew": "[Hebrew Date String]",
    "islamic_umm_al_qura": "[Hijri Date String]",
    "coptic": "[Coptic Date String]",
    "ethiopian": "[Ethiopian Date String]"
  },
  "primary": {
    "type": "saint | liturgical_day | historical_event | feast | solemnity",
    "title_en": "[Title in English]",
    "title_vi": "[Title in Vietnamese]",
    "summary_en": "[2-4 sentences in English]",
    "summary_vi": "[2-4 sentences in Vietnamese with diacritics]",
    "body_en": "[Paragraph 1]\n\n[Paragraph 2]\n\n[Paragraph 3]",
    "body_vi": "[Đoạn 1]\n\n[Đoạn 2]\n\n[Đoạn 3]",
    "confidence": "confirmed | traditional | disputed | contextual",
    "confidence_note_en": "[Brief justification for confidence level]",
    "confidence_note_vi": "[Giải thích ngắn về mức độ tin cậy]"
  },
  "place": {
    "name": "[Sanctuary / Relic Basilica / Birthplace or null]",
    "latitude": [Float latitude or null],
    "longitude": [Float longitude or null],
    "confidence": "confirmed | traditional | disputed | contextual",
    "source_url": "[Valid HTTP URL to basilica or diocese]"
  },
  "artwork": {
    "title": "[Title of Masterpiece Artwork]",
    "maker": "[Artist Name / Unknown]",
    "date_label": "[Creation Year / Era, e.g. c. 1440]",
    "source_url": "[Valid Wikimedia Commons or Met Museum URL]",
    "status": "placeholder_only"
  },
  "sources": [
    {
      "label": "[Source 1 Title & Edition]",
      "url": "[Valid HTTPS URL]",
      "type": "liturgical_calendar | vatican | encyclopedia | academic"
    },
    {
      "label": "[Source 2 Title & Author]",
      "url": "[Valid HTTPS URL]",
      "type": "liturgical_calendar | vatican | encyclopedia | academic"
    }
  ],
  "app_hooks": {
    "hero_line_en": "[Inspiring 1-sentence hero line]",
    "hero_line_vi": "[Câu tiêu đề truyền cảm hứng bằng tiếng Việt]",
    "prayer_prompt_en": "[Daily contemplative prayer in English]",
    "prayer_prompt_vi": "[Lời kinh nguyện suy niệm hàng ngày bằng tiếng Việt]"
  }
}
```

---

## Prompt 2: Pilgrimage Route & GPS Waypoints Pack

```markdown
You are a sacred geography curator for Anno.

Create a curated, multi-day bilingual Catholic pilgrimage route pack in raw JSON format.

### Target Route:
- Route Name: [INSERT_NAME: e.g. "Camino Ignaciano — From Loyola to Manresa"]
- Region: [INSERT_REGION: e.g. "Basque Country and Catalonia, Spain"]
- Duration (Days): [e.g. 21]
- Distance (km): [e.g. 650.0]
- Difficulty: ["easy" | "moderate" | "challenging"]

### Quality & Coordinate Rules:
1. Real WGS84 GPS coordinates (Latitude in [-90, 90], Longitude in [-180, 180]) for every sanctuary.
2. Sequential waypoint ordering starting strictly at order 1, 2, 3, ... N without gaps.
3. Every waypoint must describe genuine historical relics/shrines, relevant scripture citations, and guided prayers in both English and Vietnamese.
4. Vietnamese text must be natural, spiritually profound, and contain accurate tone marks.

### Output JSON Format (Return ONLY raw JSON):
{
  "route_id": "[snake_case_route_id]",
  "title_en": "[English Title]",
  "title_vi": "[Vietnamese Title]",
  "region": "[Region / Country]",
  "duration_days": [Integer or Float],
  "distance_km": [Float],
  "difficulty": "easy | moderate | challenging",
  "overview_en": "[Detailed historical overview of the pilgrimage route]",
  "overview_vi": "[Tổng quan lịch sử chi tiết bằng tiếng Việt]",
  "spiritual_theme_en": "[Core theological theme in English]",
  "spiritual_theme_vi": "[Chủ đề thiêng liêng cốt lõi bằng tiếng Việt]",
  "waypoints": [
    {
      "waypoint_id": "[unique_waypoint_id]",
      "name_en": "[Sanctuary Name in English]",
      "name_vi": "[Tên Thánh đường / Đền thánh bằng tiếng Việt]",
      "latitude": [Float],
      "longitude": [Float],
      "order": 1,
      "historical_summary_en": "[Historical context in English]",
      "historical_summary_vi": "[Bối cảnh lịch sử bằng tiếng Việt]",
      "sacred_relic_en": "[Relic / Miraculous icon details in English]",
      "sacred_relic_vi": "[Chi tiết Thánh tích / Linh ảnh bằng tiếng Việt]",
      "scripture_reading": "[Scripture reference, e.g. Luke 9:1-6]",
      "suggested_prayer_en": "[Contemplative pilgrimage prayer in English]",
      "suggested_prayer_vi": "[Lời nguyện hành hương chiêm niệm bằng tiếng Việt]"
    }
  ]
}
```

---

## Prompt 3: Sacred Art Masterpiece Dossier & Provenance

```markdown
You are a sacred iconography and art history curator for Anno.

Curate a dossier of verified Public Domain sacred artworks (Fra Angelico, Giotto, Caravaggio, Raphael, Michelangelo, Titian, El Greco, Rembrandt, Dürer, etc.) associated with Catholic feasts.

### Quality Rules:
1. Public Domain Clearance: Artwork must be PD-US / CC0 / Life+70.
2. Verified Image URLs: Must provide active, valid URLs from Wikimedia Commons, Met Museum Open Access, or National Gallery of Art.
3. Theological Significance: Explain the iconographic symbolism, theological depth, and spiritual meaning in both English and Vietnamese.

### Output JSON Format (Return ONLY raw JSON array):
[
  {
    "artwork_id": "art-[kebab-case-title-artist]",
    "feast_association": "[Associated Feast / Saint / Mystery]",
    "title": "[Title of Painting / Fresco / Sculpture]",
    "artist": "[Artist Full Name]",
    "year_created": "[e.g. c. 1440–1445]",
    "medium": "[e.g. Oil on canvas / Fresco / Tempera on panel]",
    "dimensions": "[e.g. 230 cm × 321 cm]",
    "current_location": "[Museum / Basilica, City, Country]",
    "image_url_highres": "[Direct HTTPS URL to high-resolution image]",
    "image_url_thumb": "[Direct HTTPS URL to thumbnail image]",
    "license_type": "Public Domain - US / CC0 / Life+70",
    "theological_significance_en": "[2-3 sentences explaining the iconographic symbolism and spiritual depth]",
    "theological_significance_vi": "[Bản dịch tiếng Việt giải thích ý nghĩa biểu tượng thánh kinh và linh đạo]"
  }
]
```

---

## Prompt 4: 30-Day Bilingual Catholic Devotional Pool Slice

```markdown
You are a Catholic spiritual writer and theologian for Anno.

Generate a 30-day slice of authentic, traditional Catholic daily meditations based on the masters of Catholic spirituality:
- *The Imitation of Christ* (Thomas à Kempis)
- *Introduction to the Devout Life* (St. Francis de Sales)
- *Confessions* (St. Augustine)
- *Practice of the Presence of God* (Brother Lawrence)
- *True Devotion to the Blessed Virgin* (St. Louis-Marie de Montfort)
- Sacred Scripture (Douay-Rheims / CPDV & Vietnamese Catholic Bible)

### Quality Rules:
1. Every day must have a distinct theological theme, scripture reference, 2-3 paragraph reflection, and daily prayer.
2. Both English and Vietnamese versions must be provided with complete, flawless diacritics and traditional prayer language.

### Output JSON Format (Return ONLY raw JSON array):
[
  {
    "day_of_year": [Integer 1..365],
    "theme_en": "[Theme in English, e.g. Humility of Heart]",
    "theme_vi": "[Chủ đề tiếng Việt, e.g. Sự Khiêm Nhường trong Tâm Hồn]",
    "scripture_reference": "[e.g. Matthew 11:29]",
    "scripture_text_en": "[Scripture verse in English]",
    "scripture_text_vi": "[Câu Lời Chúa bằng tiếng Việt]",
    "reflection_title_en": "Day [N]: [Title in English]",
    "reflection_title_vi": "Ngày [N]: [Tiêu đề tiếng Việt]",
    "reflection_body_en": "[Paragraph 1]\n\n[Paragraph 2]\n\n[Paragraph 3]",
    "reflection_body_vi": "[Đoạn 1]\n\n[Đoạn 2]\n\n[Đoạn 3]",
    "author_or_source": "[e.g. Thomas à Kempis, The Imitation of Christ]",
    "daily_prayer_en": "[Contemplative daily prayer in English]",
    "daily_prayer_vi": "[Lời kinh nguyện hàng ngày bằng tiếng Việt]"
  }
]
```

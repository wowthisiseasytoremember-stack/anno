# Engine B — Catholic Daily Research Prompt

**Version:** 1.0
**Purpose:** Produce a single `anno.mock.v1` entry JSON for one Gregorian date.
**Output format:** Single JSON object with required fields per ANNO_CONTENT_SCHEMA.md.

## Rules

1. **Do NOT change the schema.** Every field below must be present. Use null for optional fields you can't fill.
2. **Do NOT make up sources.** Every factual claim must link to a verifiable, authoritative Catholic source.
3. **Confidence must be honest.**
   - `confirmed`: liturgical rank, canonization record, museum document, shrine identity, well-sourced historical fact
   - `traditional`: devotional tradition, apparition narrative, traditional tomb site, approximate geography
   - `disputed`: conflicting claims or insufficient evidence
   - `contextual`: useful map anchor but not the exact place of the event
4. **Vietnamese fields:** Provide Vietnamese translations for title_vi, summary_vi, hero_line_vi, prayer_prompt_vi, confidence_note_vi. Use standard Vietnamese Catholic terminology. For proper names of saints not commonly known in Vietnamese, keep the English name and add a parenthetical Vietnamese approximation.
5. **Sources:** Minimum 2, prefer 3+. Each source must have a real URL (USCCB, Vatican.va, CatholicCulture.org, New Advent/Catholic Encyclopedia, Britannica, academic journals). Do not use example.com.
6. **Sunday entries** are liturgical anchors — the primary content is the Sunday's liturgical theme, not a saint memorial. Saint of the day should appear as secondary content, not primary.
7. **No commemoration on major solemnities.** If the date is a major feast (e.g., Christmas, Easter, Assumption, All Saints), the solemnity IS the primary content. Don't foreground a minor saint.

## Input

```
Date: {{ DATE }} (YYYY-MM-DD format)
Weekday: {{ WEEKDAY }}
Year: {{ YEAR }} (used for Computus/Movable feasts)
```

## Output Schema

```json
{
  "id": "anno-{{ DATE }}",
  "date": "{{ DATE }}",
  "weekday": "{{ WEEKDAY }}",
  "mock_priority": "engine_b_v1",
  "liturgical": {
    "rank": "Solemnity | Feast | Memorial | Optional Memorial | Feria | Sunday",
    "color": "white | red | green | purple | rose | gold | verdigris",
    "title_en": "Liturgical title in English",
    "title_vi": "Tên phụng vụ bằng tiếng Việt"
  },
  "calendars": {
    "julian": "Compute: {{ DATE }} minus 13 days (1900-2099) or minus 14 days (2100+)",
    "hebrew": "Convert date to Hebrew calendar",
    "islamic_umm_al_qura": "Convert date to Islamic/Umm al-Qura calendar",
    "coptic": "Convert date to Coptic calendar",
    "ethiopian": "Convert date to Ethiopian calendar"
  },
  "primary": {
    "type": "saint | liturgical_day | historical_event | feast | solemnity",
    "title_en": "Primary title in English",
    "title_vi": "Tiêu đề chính bằng tiếng Việt",
    "summary_en": "2-4 sentence summary of the day's significance",
    "summary_vi": "Tóm tắt 2-4 câu về ý nghĩa của ngày này",
    "body_en": "A 3-5 paragraph researched article covering: (1) who/what the day commemorates, (2) historical context, (3) significance to Catholic tradition. Include specific dates, locations, and key figures.",
    "body_vi": "Same content as body_en, translated into Vietnamese Catholic terminology",
    "confidence": "confirmed | traditional | disputed | contextual",
    "confidence_note_en": "Brief explanation of confidence level",
    "confidence_note_vi": "Giải thích ngắn về mức độ tin cậy"
  },
  "place": {
    "name": "Specific location name, or null if none verified",
    "latitude": float or null,
    "longitude": float or null,
    "confidence": "confirmed | traditional | disputed | contextual",
    "source_url": "URL for location claim"
  },
  "artwork": {
    "title": "Title of a public domain artwork depicting this saint/event",
    "maker": "Artist name if known",
    "date_label": "Century or year",
    "source_url": "Wikimedia Commons or museum URL",
    "status": "placeholder_only"
  },
  "sources": [
    {
      "label": "Short source label",
      "url": "https://actual-verifiable-url",
      "type": "liturgical_calendar | vatican | encyclopedia | academic | news | devotional"
    }
  ],
  "app_hooks": {
    "hero_line_en": "One compelling line for the card header",
    "hero_line_vi": "Một dòng hấp dẫn cho tiêu đề thẻ",
    "prayer_prompt_en": "A short prayer or reflection prompt",
    "prayer_prompt_vi": "Một lời cầu nguyện ngắn hoặc gợi ý suy niệm"
  }
}
```

## Authoritative Source Reference

For source URLs, prefer (in order):

| Source | URL Pattern | Best For |
|--------|-------------|----------|
| USCCB Daily Readings | https://bible.usccb.org/bible/readings/MMDD.cfm | Daily liturgical assignments |
| Vatican.va | https://www.vatican.va/... | Papal documents, saint canonizations |
| CatholicCulture.org | https://www.catholicculture.org/culture/liturgicalyear/calendar/day.cfm?date=YYYY-MM-DD | Daily liturgical calendar with saint info |
| New Advent Catholic Encyclopedia | https://www.newadvent.org/cathen/ | Historical saint biographies |
| Britannica | https://www.britannica.com/biography/ | General historical context |
| Catholic News Agency | https://www.catholicnewsagency.com/saints | Saint of the Day |
| Basilica/Shrine official sites | Individual URLs | Patron saint details |
| Wikimedia Commons | https://commons.wikimedia.org/ | Public domain artwork |

## Known Dates of High Sensitivity

These dates require extra care:
- Easter/Pascha (movable — confirm the actual date for the given year)
- Christmas (Dec 25) and Marian solemnities (Jan 1, Aug 15, Dec 8)
- Ash Wednesday, Palm Sunday, Holy Week (movable — compute for the given year)
- Pentecost, Trinity Sunday, Corpus Christi (movable)
- Local patronal feasts (name-specific, use confirmed sources)
- Any date where Gregorian/Julian divergence changes the observance

## Example Entry (July 3 — Feast of St. Thomas the Apostle)

```
Date: 2026-07-03
Weekday: Friday
```

```json
{
  "id": "anno-2026-07-03",
  "date": "2026-07-03",
  "weekday": "Friday",
  "mock_priority": "engine_b_v1",
  "liturgical": {
    "rank": "Feast",
    "color": "red",
    "title_en": "Feast of Saint Thomas, Apostle",
    "title_vi": "Lễ Kính Thánh Tôma, Tông đồ"
  },
  "calendars": {
    "julian": "2026-06-20",
    "hebrew": "18 Tamuz 5786",
    "islamic_umm_al_qura": "18 Muharram 1448 AH",
    "coptic": "26 Paoni 1742",
    "ethiopian": "26 Sene 2018"
  },
  "primary": {
    "type": "saint",
    "title_en": "Saint Thomas the Apostle",
    "title_vi": "Thánh Tôma Tông đồ",
    "summary_en": "Saint Thomas, one of the Twelve Apostles, is best known for doubting the Resurrection until he saw Christ's wounds. His journey from doubt to faith — and his missionary work bringing Christianity to India — make him a powerful witness for believers across cultures.",
    "summary_vi": "Thánh Tôma, một trong Mười Hai Tông Đồ, nổi tiếng vì đã hoài nghi sự Phục Sinh cho đến khi thấy các vết thương của Chúa Kitô. Hành trình từ nghi ngờ đến đức tin — và công cuộc truyền giáo đưa Kitô giáo đến Ấn Độ — làm cho ngài trở thành chứng nhân mạnh mẽ cho các tín hữu trên khắp các nền văn hóa.",
    "body_en": "Thomas the Apostle, also called Didymus (\"the twin\"), was one of the original Twelve Apostles chosen by Jesus. The Gospel of John uniquely highlights Thomas's character in three episodes...",
    "body_vi": "Thánh Tôma Tông đồ, còn gọi là Didymus (\"sinh đôi\"), là một trong Mười Hai Tông Đồ nguyên thủy được Chúa Giêsu chọn...",
    "confidence": "confirmed",
    "confidence_note_en": "Thomas is named in all four Gospels and the Acts of the Apostles. His feast has been celebrated on July 3 since at least the 8th century. The Syro-Malabar tradition of his mission to India is well-documented.",
    "confidence_note_vi": "Thánh Tôma được nhắc đến trong cả bốn sách Tin Mừng và Sách Công vụ. Lễ của ngài được cử hành vào ngày 3 tháng 7 từ ít nhất thế kỷ thứ 8. Truyền thống Syro-Malabar về sứ vụ của ngài tại Ấn Độ đã được ghi chép đầy đủ."
  },
  "place": {
    "name": "Mylapore, Chennai, India",
    "latitude": 13.0330,
    "longitude": 80.2707,
    "confidence": "traditional",
    "source_url": "https://www.newadvent.org/cathen/14663b.htm"
  },
  "artwork": {
    "title": "The Incredulity of Saint Thomas",
    "maker": "Caravaggio",
    "date_label": "1601-1602",
    "source_url": "https://commons.wikimedia.org/wiki/Category:The_Incredulity_of_Saint_Thomas_by_Caravaggio",
    "status": "placeholder_only"
  },
  "sources": [
    {"label": "Catholic Encyclopedia — St. Thomas", "url": "https://www.newadvent.org/cathen/14663b.htm", "type": "encyclopedia"},
    {"label": "USCCB — July 3", "url": "https://bible.usccb.org/bible/readings/0703.cfm", "type": "liturgical_calendar"},
    {"label": "Britannica — Saint Thomas", "url": "https://www.britannica.com/biography/Saint-Thomas-Apostle", "type": "academic"}
  ],
  "app_hooks": {
    "hero_line_en": "From doubt to faith — the apostle who touched the wounds of Christ.",
    "hero_line_vi": "Từ nghi ngờ đến đức tin — vị tông đồ đã chạm vào các vết thương của Chúa Kitô.",
    "prayer_prompt_en": "Lord, help me to believe even when I cannot see. Like Thomas, may my doubt lead me to a deeper faith.",
    "prayer_prompt_vi": "Lạy Chúa, xin giúp con tin tưởng ngay cả khi con không thể thấy. Như Thánh Tôma, ước gì sự nghi ngờ của con dẫn con đến một đức tin sâu sắc hơn."
  }
}
```

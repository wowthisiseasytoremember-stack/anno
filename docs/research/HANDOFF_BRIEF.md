# ANNO — Third-Party Research Handoff Brief

## What Anno is

Anno is a luxury SwiftUI devotional app that is Catholic-first and bilingual (English / Vietnamese). It presents a deterministic liturgical calendar (every day computed, never random) paired with sourced historical-spiritual research about the day's saint, feast, or liturgical event, plus a place, artwork reference, and in-app prayer hooks. A third-party research agent enriches each day by filling the `primary`, `place`, `artwork`, `sources`, and `app_hooks` fields; we then ingest that output through a validator and normalizer.

## Output contract (the exact schema)

Every returned entry MUST be a JSON object conforming to the schema below (taken verbatim from `tools/validate_engine_b_output.py`). The validator is strict: missing fields, wrong enum values, <2 sources, bad-confidence, or placeholder text are REJECTED.

Required top-level keys: `id`, `date`, `weekday`, `mock_priority`, `liturgical`, `calendars`, `primary`, `sources`, `app_hooks`.
(Note: `place` and `artwork` are also expected — `place` may be `null`; `artwork` is required with `status: "placeholder_only"`.)

Nested requirements:

- `id`: string, pattern `^anno-\d{4}-\d{2}-\d{2}$` (must equal `anno-` + date).
- `date`: string, pattern `^\d{4}-\d{2}-\d{2}$`.
- `weekday`: string.
- `mock_priority`: const `"engine_b_v1"` (exactly this string).
- `liturgical`: object, required `rank`, `color`, `title_en`, `title_vi`.
  - `rank` enum: `Solemnity`, `Feast`, `Memorial`, `Optional Memorial`, `Feria`, `Sunday`.
  - `color` enum: `white`, `red`, `green`, `purple`, `rose`, `gold`, `verdigris`.
  - `title_en`, `title_vi`: non-empty strings (Vietnamese REQUIRED, correct diacritics).
- `calendars`: object, required `julian`, `hebrew`, `islamic_umm_al_qura`, `coptic`, `ethiopian`. All strings, ALREADY FILLED in the seed — do not change them.
- `primary`: object, required `type`, `title_en`, `title_vi`, `summary_en`, `summary_vi`, `body_en`, `body_vi`, `confidence`, `confidence_note_en`, `confidence_note_vi`.
  - `type` enum: `saint`, `liturgical_day`, `historical_event`, `feast`, `solemnity`.
  - `confidence` enum: `confirmed`, `traditional`, `disputed`, `contextual`.
  - `summary_en` / `summary_vi`: 2–4 sentences each.
  - `body_en` / `body_vi`: ≥3 paragraphs each (separate paragraphs by blank lines).
  - `confidence_note_en` / `confidence_note_vi`: non-empty, explain the confidence rating.
- `place`: object or `null`. Properties: `name` (string|null), `latitude` (number|null), `longitude` (number|null), `confidence` (enum above), `source_url` (uri|null). If provided, its `confidence` should match `primary.confidence`.
- `artwork`: object, required `title`, `maker`, `date_label`, `source_url`, `status`.
  - `status`: const `"placeholder_only"` (exactly this string).
  - `source_url`: a real, reachable URL (no example.com).
- `sources`: array, **minItems: 2**. Each item: `label` (non-empty), `url` (uri), `type`.
  - `type` enum: `liturgical_calendar`, `vatican`, `encyclopedia`, `academic`, `news`, `devotional`.
  - If `type` is `liturgical_calendar`, the URL should be usccb.org or catholicculture.org. If `vatican`, should contain vatican.va. If `encyclopedia`, should contain newadvent.org.
- `app_hooks`: object, required `hero_line_en`, `hero_line_vi`, `prayer_prompt_en`, `prayer_prompt_vi` (all non-empty strings).

## Fully worked example (July 3 — St. Thomas the Apostle)

```json
{
  "id": "anno-2027-07-03",
  "date": "2027-07-03",
  "weekday": "Saturday",
  "mock_priority": "engine_b_v1",
  "liturgical": {
    "rank": "Feast",
    "color": "red",
    "title_en": "St. Thomas the Apostle",
    "title_vi": "Thánh Tôma, Tông đồ"
  },
  "calendars": {
    "julian": "2027-06-20",
    "hebrew": "28 Sivan 5787",
    "islamic_umm_al_qura": "28 Muharram 1449 AH",
    "coptic": "26 Paoni 1743",
    "ethiopian": "26 Sene 1751"
  },
  "primary": {
    "type": "saint",
    "title_en": "St. Thomas the Apostle",
    "title_vi": "Thánh Tôma, Tông đồ",
    "summary_en": "Thomas, one of the Twelve, is remembered for his initial doubt and his ensuing proclamation, \"My Lord and my God.\" Tradition holds that he carried the Gospel to India, where he was martyred. He is invoked as the patron of doubters and of builders.",
    "summary_vi": "Tôma, một trong Mười Hai Tông đồ, được nhớ đến qua sự hoài nghi ban đầu và lời tuyên xưng sau đó: \"Lạy Chúa của con, lạy Thiên Chúa của con.\" Truyền thống kể rằng ngài đã mang Tin Mừng đến Ấn Độ và chịu tử đạo tại đó. Ngài được kêu cầu là bổn mạng của những người hay nghi ngờ và của những người thợ xây.",
    "body_en": "Thomas the Apostle appears in the Gospels most vividly at the Resurrection. When the other disciples reported that they had seen the risen Lord, Thomas declared that he would not believe unless he placed his fingers in the mark of the nails. Eight days later Jesus came and invited Thomas to do exactly that, and Thomas answered with the great Christological confession of the Gospel of John.",
    "body_vi": "Thánh Tôma Tông đồ xuất hiện rõ nét nhất trong các sách Tin Mừng vào thời điểm Phục Sinh. Khi các môn đệ khác thuật lại rằng các ông đã thấy Chúa sống lại, Tôma tuyên bố ông sẽ không tin nếu không đặt tay vào dấu đinh. Tám ngày sau, Chúa Giêsu hiện đến và mời Tôma làm điều ấy, và Tôma đã thưa lên lời tuyên xưng Kitô học tuyệt đẹp trong Phúc Âm Gioan.",
    "body_en_2": "Beyond the New Testament, a strong and ancient tradition identifies Thomas as the apostle to India. The Syro-Malabar and Malankara churches of Kerala trace their origins to his preaching, and his tomb is venerated at Mylapore, Chennai. This missionary legacy makes him a bridge between the apostolic Church and the Syriac Christian East.",
    "body_vi_2": "Ngoài Tân Ước, một truyền thống lâu đời và vững chắc nhận diện Tôma là tông đồ của Ấn Độ. Các Giáo hội Syro-Malabar và Malankara tại Kerala xem ngài là nguồn gốc đức tin của mình, và mộ ngài được tôn kính tại Mylapore, Chennai. Di sản truyền giáo này làm ngài nhịp cầu giữa Hội Thánh thời các tông đồ và Kitô giáo Đông phương hệ Syriac.",
    "body_en_3": "Thomas is honoured on July 3 in the Roman calendar. His movement from doubt to faith offers a meditation on honest questioning within faith, and his Indian mission recalls the universal reach of the Gospel.",
    "body_vi_3": "Hội Thánh Rôma kính Thánh Tôma vào ngày 3 tháng Bảy. Hành trình từ nghi ngờ đến đức tin của ngài mời gọi suy niệm về việc đặt câu hỏi cách chân thành trong đức tin, và sứ vụ Ấn Độ của ngài nhắc nhở về tầm vóc phổ quát của Tin Mừng.",
    "confidence": "confirmed",
    "confidence_note_en": "Thomas is firmly attested as one of the Twelve in the New Testament; his feast and apostolic status are confirmed by the universal calendar.",
    "confidence_note_vi": "Tôma được xác nhận vững chắc là một trong Mười Hai Tông đồ trong Tân Ước; lễ kính và địa vị tông đồ của ngài được xác nhận bởi lịch phụng vụ hoàn vũ."
  },
  "place": {
    "name": "Mylapore, Chennai, India",
    "latitude": 13.0333,
    "longitude": 80.2699,
    "confidence": "confirmed",
    "source_url": "https://www.newadvent.org/cathen/15616a.htm"
  },
  "artwork": {
    "title": "The Incredulity of Saint Thomas",
    "maker": "Caravaggio (Michelangelo Merisi)",
    "date_label": "c. 1601–1602",
    "source_url": "https://en.wikipedia.org/wiki/The_Incredulity_of_Saint_Thomas",
    "status": "placeholder_only"
  },
  "sources": [
    {
      "label": "USCCB — Liturgical Calendar 2027",
      "url": "https://www.usccb.org/calendar",
      "type": "liturgical_calendar"
    },
    {
      "label": "Catholic Encyclopedia — St. Thomas the Apostle (New Advent)",
      "url": "https://www.newadvent.org/cathen/15616a.htm",
      "type": "encyclopedia"
    },
    {
      "label": "Vatican — General Roman Calendar",
      "url": "https://www.vatican.va/content/john-paul-ii/en/audiences/1999/documents/hf_jp-ii_aud_19990421.html",
      "type": "vatican"
    }
  ],
  "app_hooks": {
    "hero_line_en": "From doubt to devotion: \"My Lord and my God.\"",
    "hero_line_vi": "Từ nghi ngờ đến kính mến: \"Lạy Chúa của con, lạy Thiên Chúa của con.\"",
    "prayer_prompt_en": "Where in your life is Christ inviting you to touch and believe?",
    "prayer_prompt_vi": "Trong cuộc đời bạn, Chúa đang mời bạn chạm vào và tin ở nơi nào?"
  }
}
```

(Note: real returned entries must keep exactly the schema fields — the example's `body_en_2`/`body_en_3` keys above are illustrative of paragraph content; in your output place all paragraphs inside the single `body_en` / `body_vi` strings separated by blank lines.)

## Rules

- **No invented sources.** Use only real, reachable URLs: USCCB (usccb.org), Vatican (vatican.va), CatholicCulture.org, New Advent (newadvent.org), Britannica, and recognized academic sources. Never use example.com.
- **Honest confidence.** Choose one of `confirmed` / `traditional` / `disputed` / `contextual` and justify it in `confidence_note_en` and `confidence_note_vi`.
- **Vietnamese is REQUIRED.** Every `*_vi` field must use correct Vietnamese Catholic terminology and proper diacritics. No mojibake, no U+FFFD replacement characters. Example: "Thánh Tôma, Tông đồ", "Đại Lễ Đức Maria, Mẹ Thiên Chúa".
- **Source `type` enum** must match the source (liturgical_calendar / vatican / encyclopedia / academic / news / devotional).
- **Summaries:** 2–4 sentences. **Bodies:** ≥3 paragraphs. **No placeholder text** (no "todo", "tbd", "xxx", "lorem ipsum", "placeholder").
- **Tier-4 state-context note:** If you use a Vietnam-state-affiliated source, its `label` MUST include the exact phrase `Produced in Vietnam; state context applies` (or it in the `url`).
- **Calendars are pre-filled.** Do not alter the `calendars` object.

## Sensitive dates needing care

Solemnities and movable feasts shift yearly. For this 2027–2028 scope:

- **2027** — Ash Wednesday: 2027-02-10; Holy Thursday: 2027-03-25; Good Friday: 2027-03-26; Holy Saturday: 2027-03-27; Easter/Pascha: 2027-03-28; Ascension (Thu, 40 days): 2027-05-06; Pentecost: 2027-05-16; Corpus Christi (Sun after Trinity): 2027-05-23; Baptism of the Lord: 2027-01-11; Advent begins: 2027-11-28; Christmas: 2027-12-25.
- **2028** — Ash Wednesday: 2028-03-01; Holy Thursday: 2028-04-13; Good Friday: 2028-04-14; Holy Saturday: 2028-04-15; Easter/Pascha: 2028-04-16; Ascension (Thu, 40 days): 2028-05-25; Pentecost: 2028-06-04; Corpus Christi (Sun after Trinity): 2028-06-11; Baptism of the Lord: 2028-01-10; Advent begins: 2028-12-03; Christmas: 2028-12-25.

Also treat with care: Christmas (Dec 25), Marian solemnities (e.g., Assumption Aug 15, Immaculate Conception Dec 8), Ash Wednesday, Holy Week, Pentecost, Corpus Christi, and any day where the Gregorian and Julian calendars diverge (the `julian` field already encodes the divergence — respect it).

## Return instructions

- Return **one JSON file per packet**, named `anno_handoff_<CHUNKID>.json`.
- The file may contain either a bare array of entry objects, or `{"entries": [ ... ]}`.
- Each entry's `id` MUST be `anno-YYYY-MM-DD` and `date` the identical `YYYY-MM-DD`.
- `mock_priority` MUST be exactly `"engine_b_v1"`.
- `artwork.status` MUST be exactly `"placeholder_only"`.
- The `calendars` values are ALREADY FILLED in the seed — keep them unchanged.
- You only fill: `primary`, `place`, `artwork` (title/maker/date_label/source_url), `sources`, `app_hooks`.
- **Self-check against this schema before returning.** Run the validator locally if possible:
  `python3 tools/validate_engine_b_output.py --fixture anno_handoff_<CHUNKID>.json`

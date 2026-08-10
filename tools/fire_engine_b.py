#!/usr/bin/env python3
"""Fire Engine B — Catholic Research Pipeline for July 17-30."""
import json, os, subprocess, sys, time

ANNO_DIR = "/home/ichabod/Projects/Anno"
OUT_DIR = os.path.join(ANNO_DIR, "data", "research_results")
os.makedirs(OUT_DIR, exist_ok=True)

# Get API key
env_path = "/home/ichabod/.hermes/.env"
api_key = None
with open(env_path) as f:
    for line in f:
        if line.startswith("OPENROUTER_API_KEY="):
            api_key = line.strip().split("=", 1)[1]
            break

if not api_key:
    print("❌ Could not find OPENROUTER_API_KEY in .env")
    sys.exit(1)

print(f"🔑 API key found: {api_key[:8]}...{api_key[-4:]}")

# Calendar data from Engine A
CALENDAR = {
    "2026-07-17": {"weekday": "Friday",    "julian": "2026-07-04",  "hebrew": "3 Av 5786",             "islamic": "3 Safar 1448 AH",   "coptic": "10 Epip 1742",  "ethiopian": "10 Hamle 2018"},
    "2026-07-18": {"weekday": "Saturday",  "julian": "2026-07-05",  "hebrew": "4 Av 5786",             "islamic": "4 Safar 1448 AH",   "coptic": "11 Epip 1742",  "ethiopian": "11 Hamle 2018"},
    "2026-07-19": {"weekday": "Sunday",    "julian": "2026-07-06",  "hebrew": "5 Av 5786",             "islamic": "5 Safar 1448 AH",   "coptic": "12 Epip 1742",  "ethiopian": "12 Hamle 2018"},
    "2026-07-20": {"weekday": "Monday",    "julian": "2026-07-07",  "hebrew": "6 Av 5786",             "islamic": "6 Safar 1448 AH",   "coptic": "13 Epip 1742",  "ethiopian": "13 Hamle 2018"},
    "2026-07-21": {"weekday": "Tuesday",   "julian": "2026-07-08",  "hebrew": "7 Av 5786",             "islamic": "7 Safar 1448 AH",   "coptic": "14 Epip 1742",  "ethiopian": "14 Hamle 2018"},
    "2026-07-22": {"weekday": "Wednesday", "julian": "2026-07-09",  "hebrew": "8 Av 5786",             "islamic": "8 Safar 1448 AH",   "coptic": "15 Epip 1742",  "ethiopian": "15 Hamle 2018"},
    "2026-07-23": {"weekday": "Thursday",  "julian": "2026-07-10",  "hebrew": "9 Av 5786",             "islamic": "9 Safar 1448 AH",   "coptic": "16 Epip 1742",  "ethiopian": "16 Hamle 2018"},
    "2026-07-24": {"weekday": "Friday",    "julian": "2026-07-11",  "hebrew": "10 Av 5786",            "islamic": "10 Safar 1448 AH",  "coptic": "17 Epip 1742",  "ethiopian": "17 Hamle 2018"},
    "2026-07-25": {"weekday": "Saturday",  "julian": "2026-07-12",  "hebrew": "11 Av 5786",            "islamic": "11 Safar 1448 AH",  "coptic": "18 Epip 1742",  "ethiopian": "18 Hamle 2018"},
    "2026-07-26": {"weekday": "Sunday",    "julian": "2026-07-13",  "hebrew": "12 Av 5786",            "islamic": "12 Safar 1448 AH",  "coptic": "19 Epip 1742",  "ethiopian": "19 Hamle 2018"},
    "2026-07-27": {"weekday": "Monday",    "julian": "2026-07-14",  "hebrew": "13 Av 5786",            "islamic": "13 Safar 1448 AH",  "coptic": "20 Epip 1742",  "ethiopian": "20 Hamle 2018"},
    "2026-07-28": {"weekday": "Tuesday",   "julian": "2026-07-15",  "hebrew": "14 Av 5786",            "islamic": "14 Safar 1448 AH",  "coptic": "21 Epip 1742",  "ethiopian": "21 Hamle 2018"},
    "2026-07-29": {"weekday": "Wednesday", "julian": "2026-07-16",  "hebrew": "15 Av 5786",            "islamic": "15 Safar 1448 AH",  "coptic": "22 Epip 1742",  "ethiopian": "22 Hamle 2018"},
    "2026-07-30": {"weekday": "Thursday",  "julian": "2026-07-17",  "hebrew": "16 Av 5786",            "islamic": "16 Safar 1448 AH",  "coptic": "23 Epip 1742",  "ethiopian": "23 Hamle 2018"},
}

# Context notes about known feasts
FEAST_NOTES = {
    "2026-07-19": "Sixteenth Sunday in Ordinary Time — liturgical anchor. Primary: Sunday theme, not saint.",
    "2026-07-22": "Feast of St. Mary Magdalene — Apostle to the Apostles, first witness of the Resurrection.",
    "2026-07-25": "Feast of St. James the Apostle — brother of John, patron of Spain, Santiago de Compostela.",
    "2026-07-26": "Seventeenth Sunday in Ordinary Time — liturgical anchor.",
    "2026-07-29": "Memorial of Sts. Martha, Mary, and Lazarus — friends of Jesus in Bethany.",
    "2026-07-30": "Optional Memorial of St. Peter Chrysologus — Bishop of Ravenna, Doctor of the Church.",
}

SYSTEM_PROMPT = """You are Engine B of the Anno project — a Catholic liturgical research engine. You produce structured JSON entries for liturgical dates.

You MUST:
1. Output ONLY valid JSON, no other text before or after.
2. Use EXACT snake_case key names as shown in the schema.
3. Provide REAL Vietnamese Catholic terminology for all Vietnamese fields.
4. Include minimum 2 verifiable sources per entry with real URLs (newadvent.org, catholicculture.org, vatican.va, USCCB, etc.)
5. Use honest confidence levels: confirmed/traditional/disputed/contextual

For Sunday entries: the Sunday's liturgical theme IS the primary content, not any saint memorial."""


def build_prompt(date, cal):
    feast_note = FEAST_NOTES.get(date, "Weekday of Ordinary Time")
    if "Sunday" in feast_note:
        feast_note += "\nIMPORTANT: Sunday is a liturgical anchor — the primary content is the Sunday theme, not the saint of the day."
    
    prompt = f"""Research the following Catholic liturgical date and produce a JSON entry.

Date: {date}
Weekday: {cal['weekday']}

Calendar conversions (verified, include these exactly):
- Julian: {cal['julian']}
- Hebrew: {cal['hebrew']}
- Islamic (Umm al-Qura): {cal['islamic']}
- Coptic: {cal['coptic']}
- Ethiopian: {cal['ethiopian']}

Context: {feast_note}

Schema (output ONLY this JSON, no other text):

{{
  "id": "anno-{date}",
  "date": "{date}",
  "weekday": "{cal['weekday']}",
  "mock_priority": "engine_b_v1",
  "liturgical": {{
    "rank": "Solemnity | Feast | Memorial | Optional Memorial | Feria | Sunday",
    "color": "white | red | green | purple | rose | gold | verdigris",
    "title_en": "Liturgical title in English",
    "title_vi": "Tên phụng vụ bằng tiếng Việt"
  }},
  "calendars": {{
    "julian": "{cal['julian']}",
    "hebrew": "{cal['hebrew']}",
    "islamic_umm_al_qura": "{cal['islamic']}",
    "coptic": "{cal['coptic']}",
    "ethiopian": "{cal['ethiopian']}"
  }},
  "primary": {{
    "type": "saint | liturgical_day | feast | solemnity",
    "title_en": "Primary title",
    "title_vi": "Tiêu đề chính",
    "summary_en": "2-4 sentence summary of the day's significance",
    "summary_vi": "Tóm tắt 2-4 câu về ý nghĩa của ngày này",
    "body_en": "3-5 paragraph researched article with historical context",
    "body_vi": "Same content in Vietnamese Catholic terminology",
    "confidence": "confirmed | traditional | disputed | contextual",
    "confidence_note_en": "Brief confidence explanation",
    "confidence_note_vi": "Giải thích ngắn về mức độ tin cậy"
  }},
  "place": {{
    "name": "Specific location or null",
    "latitude": null,
    "longitude": null,
    "confidence": "confirmed | traditional | disputed | contextual",
    "source_url": "URL for location claim"
  }},
  "artwork": {{
    "title": "Title of public domain artwork",
    "maker": "Artist name or null",
    "date_label": "Century or year",
    "source_url": "Wikimedia Commons or museum URL",
    "status": "placeholder_only"
  }},
  "sources": [
    {{"label": "Short label", "url": "https://actual-verifiable-url", "type": "liturgical_calendar | vatican | encyclopedia | academic | devotional"}}
  ],
  "app_hooks": {{
    "hero_line_en": "One compelling card header line",
    "hero_line_vi": "Một dòng hấp dẫn cho tiêu đề thẻ",
    "prayer_prompt_en": "Short prayer or reflection prompt",
    "prayer_prompt_vi": "Một lời cầu nguyện ngắn hoặc gợi ý suy niệm"
  }}
}}"""

    return prompt


def call_openrouter(prompt, retries=2):
    payload = {
        "model": "nvidia/nemotron-3-super-120b-a12b:free",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 4000
    }
    
    for attempt in range(retries + 1):
        try:
            result = subprocess.run(
                ["curl", "-s", "-w", "\n%{http_code}",
                 "https://openrouter.ai/api/v1/chat/completions",
                 "-H", f"Authorization: Bearer {api_key}",
                 "-H", "Content-Type: application/json",
                 "-H", "HTTP-Referer: https://anno.app",
                 "-d", json.dumps(payload)],
                capture_output=True, text=True, timeout=90
            )
            *body_parts, http_code = result.stdout.strip().rsplit('\n', 1)
            body = '\n'.join(body_parts)
            
            if http_code != "200":
                print(f"    HTTP {http_code}: {body[:200]}")
                time.sleep(3)
                continue
            
            response_data = json.loads(body)
            content = response_data['choices'][0]['message']['content']
            
            # Extract and parse JSON
            start = content.find('{')
            end = content.rfind('}')
            if start >= 0 and end > start:
                parsed = json.loads(content[start:end+1])
                return parsed
            else:
                print(f"    No JSON found in response, raw: {content[:300]}")
                time.sleep(3)
        except Exception as e:
            print(f"    Error: {e}")
            time.sleep(3)
    
    return None


success = 0
fail = 0

dates = [f"2026-07-{d:02d}" for d in range(17, 31)]

for date in dates:
    outfile = os.path.join(OUT_DIR, f"{date}_result.json")
    
    # Skip if already exists and valid
    if os.path.exists(outfile) and os.path.getsize(outfile) > 100:
        print(f"⏭️  {date} — already done")
        success += 1
        continue
    
    cal = CALENDAR[date]
    print(f"📡 {date} ({cal['weekday']}) — researching...", end=" ", flush=True)
    
    prompt = build_prompt(date, cal)
    
    # Save prompt for reference
    with open(os.path.join(OUT_DIR, f"{date}_prompt.txt"), "w") as f:
        f.write(prompt)
    
    result = call_openrouter(prompt)
    
    if result:
        title = result.get("liturgical", {}).get("title_en", "N/A")
        primary_type = result.get("primary", {}).get("type", "N/A")
        confidence = result.get("primary", {}).get("confidence", "N/A")
        sources = len(result.get("sources", []))
        has_body = len(result.get("primary", {}).get("body_en", "")) > 50
        
        with open(outfile, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {title} | {primary_type} | confidence:{confidence} | sources:{sources} | body:{'✓' if has_body else '✗'}")
        success += 1
    else:
        print(f"❌ Failed after retries")
        fail += 1

print(f"\n{'='*50}")
print(f"Engine B Results: ✅ {success} succeeded, ❌ {fail} failed")
print(f"Results: {OUT_DIR}")

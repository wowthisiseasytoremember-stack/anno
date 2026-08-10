#!/usr/bin/env python3
"""Fire Engine B — English-only research via opencode-zen zen/v1 with nemotron-3-ultra-free."""
import json, os, subprocess, sys, time

OUT_DIR = "/home/ichabod/Projects/Anno/data/research_results"
os.makedirs(OUT_DIR, exist_ok=True)

with open("/home/ichabod/.hermes/.env") as f:
    env = f.read()
    
zen_key = None
for line in env.split("\n"):
    if line.startswith("OPENCODE_ZEN_API_KEY="):
        zen_key = line.split("=", 1)[1].strip()
        break

print(f"🔑 Key found: {zen_key[:10]}...{zen_key[-4:]} ({len(zen_key)} chars)")

CAL = {
    "2026-07-18": ("Saturday", "2026-07-05", "4 Av 5786", "4 Safar 1448 AH", "11 Epip 1742", "11 Hamle 2018"),
    "2026-07-19": ("Sunday", "2026-07-06", "5 Av 5786", "5 Safar 1448 AH", "12 Epip 1742", "12 Hamle 2018"),
    "2026-07-20": ("Monday", "2026-07-07", "6 Av 5786", "6 Safar 1448 AH", "13 Epip 1742", "13 Hamle 2018"),
    "2026-07-21": ("Tuesday", "2026-07-08", "7 Av 5786", "7 Safar 1448 AH", "14 Epip 1742", "14 Hamle 2018"),
    "2026-07-22": ("Wednesday", "2026-07-09", "8 Av 5786", "8 Safar 1448 AH", "15 Epip 1742", "15 Hamle 2018"),
    "2026-07-23": ("Thursday", "2026-07-10", "9 Av 5786", "9 Safar 1448 AH", "16 Epip 1742", "16 Hamle 2018"),
    "2026-07-24": ("Friday", "2026-07-11", "10 Av 5786", "10 Safar 1448 AH", "17 Epip 1742", "17 Hamle 2018"),
    "2026-07-25": ("Saturday", "2026-07-12", "11 Av 5786", "11 Safar 1448 AH", "18 Epip 1742", "18 Hamle 2018"),
    "2026-07-26": ("Sunday", "2026-07-13", "12 Av 5786", "12 Safar 1448 AH", "19 Epip 1742", "19 Hamle 2018"),
    "2026-07-27": ("Monday", "2026-07-14", "13 Av 5786", "13 Safar 1448 AH", "20 Epip 1742", "20 Hamle 2018"),
    "2026-07-28": ("Tuesday", "2026-07-15", "14 Av 5786", "14 Safar 1448 AH", "21 Epip 1742", "21 Hamle 2018"),
    "2026-07-29": ("Wednesday", "2026-07-16", "15 Av 5786", "15 Safar 1448 AH", "22 Epip 1742", "22 Hamle 2018"),
    "2026-07-30": ("Thursday", "2026-07-17", "16 Av 5786", "16 Safar 1448 AH", "23 Epip 1742", "23 Hamle 2018"),
}

FEAST = {
    "2026-07-18": "Optional Memorial of the Blessed Virgin Mary on Saturday",
    "2026-07-19": "Sixteenth Sunday in Ordinary Time. PRIMARY content is the Sunday theme (Good Shepherd/Psalm 23), NOT a saint.",
    "2026-07-20": "Optional Memorial of St. Apollinaris, Bishop and Martyr",
    "2026-07-21": "Optional Memorial of St. Lawrence of Brindisi, Doctor of the Church",
    "2026-07-22": "Feast of St. Mary Magdalene, Apostle to the Apostles",
    "2026-07-23": "Optional Memorial of St. Bridget of Sweden, Religious",
    "2026-07-24": "Friday of the Sixteenth Week in Ordinary Time",
    "2026-07-25": "Feast of St. James the Apostle, patron of Spain",
    "2026-07-26": "Seventeenth Sunday in Ordinary Time. PRIMARY content is the Sunday theme.",
    "2026-07-27": "Monday of the Seventeenth Week in Ordinary Time",
    "2026-07-28": "Tuesday of the Seventeenth Week in Ordinary Time",
    "2026-07-29": "Memorial of Sts. Martha, Mary, and Lazarus",
    "2026-07-30": "Optional Memorial of St. Peter Chrysologus, Doctor of the Church",
}

SYSTEM = "You produce structured JSON for Catholic liturgical dates. Output ONLY valid JSON."

def call_api(model, prompt, retries=2):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 3000,
    }
    for attempt in range(retries + 1):
        try:
            if attempt > 0:
                time.sleep(5 * attempt)
            result = subprocess.run(
                ["curl", "-s", "-w", "\n%{http_code}",
                 "https://opencode.ai/zen/v1/chat/completions",
                 "-H", f"Authorization: Bearer {zen_key}",
                 "-H", "Content-Type: application/json",
                 "-d", json.dumps(payload)],
                capture_output=True, text=True, timeout=90,
            )
            *body_parts, http_code = result.stdout.strip().rsplit("\n", 1)
            body = "\n".join(body_parts)
            if http_code == "429":
                continue
            if http_code != "200":
                continue
            resp = json.loads(body)
            content = resp["choices"][0]["message"]["content"]
            start = content.find("{")
            end = content.rfind("}")
            if start >= 0 and end > start:
                return json.loads(content[start : end + 1])
        except Exception:
            time.sleep(2)
    return None

done, fail = 0, 0
dates = [f"2026-07-{d:02d}" for d in range(18, 31)]

# Use nemotron-3-ultra-free as primary, kept as fallback list
models = ["nemotron-3-ultra-free", "deepseek-v4-flash-free"]

for date in dates:
    outfile = os.path.join(OUT_DIR, f"{date}_result_en.json")
    if os.path.exists(outfile) and os.path.getsize(outfile) > 200:
        print(f"⏭️  {date} — exists")
        done += 1
        continue

    wd, jul, heb, isl, cop, eth = CAL[date]
    ctx = FEAST.get(date, "Weekday")
    
    prompt = f"""Create a JSON entry for {date} ({wd}).
Calendar: Julian={jul} Hebrew={heb} Islamic={isl} Coptic={cop} Ethiopian={eth}
Context: {ctx}

JSON with these exact keys: id, date, weekday, mock_priority, liturgical(rank,color,title_en), calendars(julian,hebrew,islamic_umm_al_qura,coptic,ethiopian), primary(type,title_en,summary_en,body_en,confidence,confidence_note_en), place(name,latitude,longitude,confidence,source_url), artwork(title,maker,date_label,source_url,status), sources([label,url,type]), app_hooks(hero_line_en,prayer_prompt_en).

English only. No Vietnamese. Output ONLY the JSON object, nothing before or after."""

    result = None
    for model in models:
        print(f"📡 {date} via {model}...", end=" ", flush=True)
        result = call_api(model, prompt)
        if result:
            break
        print(f"no", end=" ")

    if result:
        title = result.get("liturgical", {}).get("title_en", "N/A")
        ptype = result.get("primary", {}).get("type", "N/A")
        src = len(result.get("sources", []))
        conf = result.get("primary", {}).get("confidence", "N/A")
        body_len = len(result.get("primary", {}).get("body_en", ""))
        with open(outfile, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"✅ {title} | {ptype} | conf:{conf} | src:{src} | body:{body_len}c")
        done += 1
    else:
        print(f"❌ All failed")
        fail += 1

print(f"\n{'='*40}\nDone: ✅ {done} | Failed: ❌ {fail}")

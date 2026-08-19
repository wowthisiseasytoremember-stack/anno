#!/usr/bin/env python3
"""Robust Engine B firer for dates 2026-07-27 .. 2026-07-30.

Reuses the SYSTEM_PROMPT + build_prompt from fire_engine_b.py but with:
  - json5-tolerant parsing (handles trailing commas, unquoted keys)
  - markdown code-fence stripping
  - up to 5 retries per date
Outputs data/research_results/2026-07-DD_result.json (same shape as 24-26).
"""
from __future__ import annotations
import json, os, sys, time, subprocess
import json5
sys.path.insert(0, os.path.dirname(__file__))
from fire_engine_b import SYSTEM_PROMPT, build_prompt, CALENDAR, ANNO_DIR  # type: ignore

OUT_DIR = os.path.join(ANNO_DIR, "data", "research_results")
os.makedirs(OUT_DIR, exist_ok=True)

# Read API key
api_key = None
with open("/home/ichabod/.hermes/.env") as f:
    for line in f:
        if line.startswith("OPENROUTER_API_KEY="):
            api_key = line.strip().split("=", 1)[1]
            break
assert api_key, "OPENROUTER_API_KEY not found"


def call_openrouter(prompt, retries=5):
    payload = {
        "model": "nvidia/nemotron-3-super-120b-a12b:free",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 4096,
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
                capture_output=True, text=True, timeout=120,
            )
            *body_parts, http_code = result.stdout.strip().rsplit("\n", 1)
            body = "\n".join(body_parts)
            if http_code != "200":
                print(f"    HTTP {http_code}: {body[:160]}")
                time.sleep(3)
                continue
            response_data = json.loads(body)
            content = response_data["choices"][0]["message"]["content"]
            # strip code fences
            c = content.strip()
            if c.startswith("```"):
                c = c.split("\n", 1)[1] if "\n" in c else c[3:]
            if c.endswith("```"):
                c = c[:-3]
            c = c.strip()
            start, end = c.find("{"), c.rfind("}")
            if start >= 0 and end > start:
                parsed = json5.loads(c[start:end + 1])
                return parsed
            print(f"    No JSON parsed (attempt {attempt+1})")
        except Exception as e:
            print(f"    Error: {e} (attempt {attempt+1})")
            time.sleep(3)
    return None


success = fail = 0
for d in range(27, 31):
    date = f"2026-07-{d:02d}"
    outfile = os.path.join(OUT_DIR, f"{date}_result.json")
    if os.path.exists(outfile) and os.path.getsize(outfile) > 100:
        print(f"⏭️  {date} — already done")
        success += 1
        continue
    cal = CALENDAR[date]
    print(f"📡 {date} ({cal['weekday']}) — researching...", end=" ", flush=True)
    prompt = build_prompt(date, cal)
    with open(os.path.join(OUT_DIR, f"{date}_prompt.txt"), "w") as f:
        f.write(prompt)
    result = call_openrouter(prompt)
    if result:
        with open(outfile, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"✅ {result.get('liturgical',{}).get('title_en','?')} | {result.get('primary',{}).get('type','?')} | src={len(result.get('sources',[]))}")
        success += 1
    else:
        print("❌ Failed")
        fail += 1

print(f"\nEngine B 27-30: ✅ {success} succeeded, ❌ {fail} failed")

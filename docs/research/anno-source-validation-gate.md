# Engine B — Source Validation Gate

**Purpose:** Verify each generated Engine B entry before merging into the app fixture.
**Runs after:** Each batch of research outputs is returned.

## Checks

For each entry, verify:

### 1. Schema Compliance
- All required fields present per ANNO_CONTENT_SCHEMA.md
- `id` matches pattern `anno-YYYY-MM-DD`
- `date` matches the requested date
- `liturgical.rank` is one of: Solemnity, Feast, Memorial, Optional Memorial, Feria, Sunday
- `liturgical.color` is one of: white, red, green, purple, rose, gold, verdigris
- `primary.confidence` is one of: confirmed, traditional, disputed, contextual
- `mock_priority` is `engine_b_v1`

### 2. Source Validation
- Each source URL must resolve (HTTP 200 or known redirect)
- At least 2 sources per entry, 3 preferred
- No `example.com` URLs
- Source URLs should match their `type`:
  - `liturgical_calendar` → usccb.org, catholicculture.org
  - `vatican` → vatican.va
  - `encyclopedia` → newadvent.org, britannica.com
  - `academic` → .edu, jstor.org, academia.edu
  - `news` → catholicnewsagency.com, cruxnow.com
  - `devotional` → ewtn.com, relevant radio, etc.

### 3. Content Quality
- `summary_en` is 2-4 sentences (not a single line)
- `body_en` has substantive paragraphs (3+), not placeholder text like "A day of ordinary time..."
- `hero_line_en` is a compelling single line (not a repetition of summary)
- No placeholder content from the old dataset
- Sources are referenced by the content (claims in body should map to a cited source)

### 4. Confidence Consistency
- If rank is "Solemnity" or "Feast", confidence should be "confirmed"
- If place is a traditional (uncertain) site, place.confidence should match
- `confidence_note` explains the label — not just "verified" but specific reasoning

### 5. Bilingual Fields
- Both `*_en` and `*_vi` fields present for: title, summary, body, hero_line, prayer_prompt, confidence_note
- VI fields are genuine Vietnamese, not machine transliteration of English
- Proper names (saints, places) that have standard Vietnamese Catholic forms should use them

## Scoring

| Score | Meaning | Action |
|-------|---------|--------|
| Pass | All checks pass | Merge into fixture |
| Pass with notes | Minor issues (typo, missing VI accent) | Fix inline, merge |
| Revise | Missing fields, wrong confidence, bad sources | Return to agent with specific instructions |
| Reject | Schema violation, hallucinated saint, placeholder content | Return to agent with error details |

## Script

```bash
# Run this after each batch
python3 tools/validate_mock_content.py --fixture path/to/generated.json

# Additional checks
python3 tools/validate_mock_content.py --fixture path/to/generated.json --strict --check-sources --check-content-quality
```

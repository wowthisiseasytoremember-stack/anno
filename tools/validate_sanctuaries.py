#!/usr/bin/env python3
"""
validate_sanctuaries.py
Validates individual sanctuary JSON files in Anno/Resources/SacredSanctuaries/
against the anno.sanctuary.v1 schema contract, WGS84 GPS bounds, Vietnamese
ecclesiastical terminology / diacritics, and minimum source citations.
"""

import os
import sys
import json
import glob
import re

VALID_CATEGORIES = {
    "marian_apparition",
    "apostolic_tomb",
    "eucharistic_miracle",
    "doctor_of_church",
    "martyr_shrine",
    "passion_relic",
    "monastic_sanctuary"
}

VALID_CONFIDENCES = {"confirmed", "traditional", "disputed", "contextual"}
VALID_PRECISIONS = {"exact_altar", "crypt", "apparition_ground", "monastery_complex", "chapel_altar", "holy_stairs"}

REQUIRED_FIELDS = [
    "sanctuary_id",
    "category",
    "name_en",
    "name_vi",
    "feast_day_association",
    "location",
    "canonical_status",
    "primary_relics",
    "historical_summary_en",
    "historical_summary_vi",
    "scripture_reading",
    "suggested_prayer_en",
    "suggested_prayer_vi",
    "primary_sources"
]

REQUIRED_LOCATION_FIELDS = [
    "shrine_or_basilica",
    "city",
    "region_or_state",
    "country",
    "latitude",
    "longitude",
    "precision"
]

REQUIRED_CANONICAL_FIELDS = [
    "approval_or_consecration_date",
    "approving_authority",
    "confidence",
    "confidence_note_en",
    "confidence_note_vi"
]

REQUIRED_RELIC_FIELDS = [
    "relic_name_en",
    "relic_name_vi",
    "relic_type",
    "reliquary_location"
]

VI_DIACRITICS_REGEX = re.compile(r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ]", re.IGNORECASE)

def validate_sanctuary_file(filepath: str) -> list:
    errors = []
    basename = os.path.basename(filepath)
    expected_id = os.path.splitext(basename)[0]

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [f"[{basename}] Invalid JSON format: {e}"]

    # 1. Top level fields
    for f in REQUIRED_FIELDS:
        if f not in data:
            errors.append(f"[{basename}] Missing required field '{f}'")
        elif isinstance(data[f], str) and not data[f].strip():
            errors.append(f"[{basename}] Field '{f}' must not be empty")

    sanctuary_id = data.get("sanctuary_id")
    if sanctuary_id != expected_id:
        errors.append(f"[{basename}] sanctuary_id '{sanctuary_id}' does not match filename '{expected_id}'")

    category = data.get("category")
    if category not in VALID_CATEGORIES:
        errors.append(f"[{basename}] Invalid category '{category}'. Must be one of {sorted(VALID_CATEGORIES)}")

    # 2. Location validation
    loc = data.get("location", {})
    if not isinstance(loc, dict):
        errors.append(f"[{basename}] 'location' must be an object")
    else:
        for lf in REQUIRED_LOCATION_FIELDS:
            if lf not in loc:
                errors.append(f"[{basename}] Missing location field '{lf}'")
            elif isinstance(loc[lf], str) and not loc[lf].strip():
                errors.append(f"[{basename}] Location field '{lf}' must not be empty")

        lat = loc.get("latitude")
        lng = loc.get("longitude")
        if not isinstance(lat, (int, float)) or not (-90.0 <= lat <= 90.0):
            errors.append(f"[{basename}] Invalid latitude '{lat}'. Must be in [-90.0, 90.0]")
        if not isinstance(lng, (int, float)) or not (-180.0 <= lng <= 180.0):
            errors.append(f"[{basename}] Invalid longitude '{lng}'. Must be in [-180.0, 180.0]")

    # 3. Canonical status validation
    canon = data.get("canonical_status", {})
    if not isinstance(canon, dict):
        errors.append(f"[{basename}] 'canonical_status' must be an object")
    else:
        for cf in REQUIRED_CANONICAL_FIELDS:
            if cf not in canon:
                errors.append(f"[{basename}] Missing canonical_status field '{cf}'")
            elif isinstance(canon[cf], str) and not canon[cf].strip():
                errors.append(f"[{basename}] Canonical field '{cf}' must not be empty")
        
        conf = canon.get("confidence")
        if conf not in VALID_CONFIDENCES:
            errors.append(f"[{basename}] Invalid confidence '{conf}'. Must be one of {sorted(VALID_CONFIDENCES)}")

    # 4. Primary relics validation
    relics = data.get("primary_relics", [])
    if not isinstance(relics, list) or len(relics) == 0:
        errors.append(f"[{basename}] 'primary_relics' must be a non-empty array")
    else:
        for r_idx, r in enumerate(relics):
            if not isinstance(r, dict):
                errors.append(f"[{basename} -> relic #{r_idx}] Must be an object")
                continue
            for rf in REQUIRED_RELIC_FIELDS:
                if rf not in r or (isinstance(r[rf], str) and not r[rf].strip()):
                    errors.append(f"[{basename} -> relic #{r_idx}] Missing/empty field '{rf}'")

    # 5. Vietnamese diacritics validation
    vi_fields = [
        ("name_vi", data.get("name_vi", "")),
        ("canonical_status.confidence_note_vi", canon.get("confidence_note_vi", "") if isinstance(canon, dict) else ""),
        ("historical_summary_vi", data.get("historical_summary_vi", "")),
        ("suggested_prayer_vi", data.get("suggested_prayer_vi", ""))
    ]
    for field_name, val in vi_fields:
        if val and not VI_DIACRITICS_REGEX.search(val):
            errors.append(f"[{basename}] Field '{field_name}' lacks Vietnamese diacritics: '{val[:40]}...'")

    # 6. Primary sources validation (at least 2 valid sources)
    sources = data.get("primary_sources", [])
    if not isinstance(sources, list) or len(sources) < 2:
        errors.append(f"[{basename}] Must have at least 2 primary sources (got {len(sources) if isinstance(sources, list) else 0})")
    else:
        for s_idx, src in enumerate(sources):
            if not isinstance(src, dict):
                errors.append(f"[{basename} -> source #{s_idx}] Must be an object")
                continue
            if not src.get("label") or not src.get("url"):
                errors.append(f"[{basename} -> source #{s_idx}] Missing 'label' or 'url'")
            elif not src["url"].startswith("http"):
                errors.append(f"[{basename} -> source #{s_idx}] URL must start with http/https: '{src['url']}'")

    return errors

def main():
    sanctuaries_dir = sys.argv[1] if len(sys.argv) > 1 else "Anno/Resources/SacredSanctuaries"
    json_files = sorted(glob.glob(os.path.join(sanctuaries_dir, "*.json")))

    if not json_files:
        print(f"ERROR: No JSON sanctuary files found in '{sanctuaries_dir}'")
        sys.exit(1)

    print(f"Validating {len(json_files)} sanctuary files in '{sanctuaries_dir}'...\n")
    all_errors = {}

    for fpath in json_files:
        basename = os.path.basename(fpath)
        errs = validate_sanctuary_file(fpath)
        if errs:
            all_errors[basename] = errs
            print(f"❌ {basename} (FAIL - {len(errs)} issues)")
            for e in errs:
                print(f"   • {e}")
        else:
            print(f"✅ {basename} (PASS)")

    print("-" * 60)
    if all_errors:
        print(f"FAILED: {len(all_errors)} / {len(json_files)} sanctuary files contain errors.")
        sys.exit(1)
    else:
        print(f"ALL PASS: {len(json_files)} sanctuary files validated successfully.")
        sys.exit(0)

if __name__ == "__main__":
    main()

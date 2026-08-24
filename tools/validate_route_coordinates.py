#!/usr/bin/env python3
"""
validate_route_coordinates.py
Validates pilgrimage route JSON files in Anno/Resources/PilgrimageRoutes/
Ensures structural schema adherence, geographic coordinate validity,
sequential waypoint ordering, and non-empty bilingual fields with Vietnamese diacritics.
"""

import os
import sys
import json
import glob
import re

REQUIRED_ROUTE_FIELDS = [
    "route_id", "title_en", "title_vi", "region", "duration_days",
    "distance_km", "difficulty", "overview_en", "overview_vi",
    "spiritual_theme_en", "spiritual_theme_vi", "waypoints"
]

REQUIRED_WAYPOINT_FIELDS = [
    "waypoint_id", "name_en", "name_vi", "latitude", "longitude",
    "order", "historical_summary_en", "historical_summary_vi",
    "sacred_relic_en", "sacred_relic_vi", "scripture_reading",
    "suggested_prayer_en", "suggested_prayer_vi"
]

VALID_DIFFICULTIES = {"easy", "moderate", "challenging"}

# Regex matching common Vietnamese diacritics
VI_DIACRITICS_REGEX = re.compile(r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ]", re.IGNORECASE)

def validate_route_file(filepath: str) -> list:
    errors = []
    basename = os.path.basename(filepath)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [f"[{basename}] Invalid JSON format: {e}"]

    # 1. Top-level fields check
    for field in REQUIRED_ROUTE_FIELDS:
        if field not in data:
            errors.append(f"[{basename}] Missing required top-level field: '{field}'")
        elif isinstance(data[field], str) and not data[field].strip():
            errors.append(f"[{basename}] Field '{field}' must not be empty")

    if data.get("difficulty") not in VALID_DIFFICULTIES:
        errors.append(f"[{basename}] Invalid difficulty '{data.get('difficulty')}'. Must be one of {VALID_DIFFICULTIES}")

    # Check route_id matching filename
    expected_id = os.path.splitext(basename)[0]
    if data.get("route_id") != expected_id:
        errors.append(f"[{basename}] route_id '{data.get('route_id')}' does not match filename '{expected_id}'")

    # Check Vietnamese content in route title/overview
    for vi_field in ["title_vi", "overview_vi", "spiritual_theme_vi"]:
        val = data.get(vi_field, "")
        if val and not VI_DIACRITICS_REGEX.search(val):
            errors.append(f"[{basename}] Field '{vi_field}' lacks expected Vietnamese diacritics: '{val[:40]}...'")

    # 2. Waypoints validation
    waypoints = data.get("waypoints", [])
    if not isinstance(waypoints, list) or len(waypoints) == 0:
        errors.append(f"[{basename}] 'waypoints' must be a non-empty list")
        return errors

    orders_seen = []
    waypoint_ids_seen = set()

    for idx, wp in enumerate(waypoints, start=1):
        wp_prefix = f"[{basename} -> Waypoint #{idx}]"

        # Check waypoint fields
        for wp_field in REQUIRED_WAYPOINT_FIELDS:
            if wp_field not in wp:
                errors.append(f"{wp_prefix} Missing field '{wp_field}'")
            elif isinstance(wp[wp_field], str) and not wp[wp_field].strip():
                errors.append(f"{wp_prefix} String field '{wp_field}' is empty")

        # Unique waypoint_id
        wp_id = wp.get("waypoint_id")
        if wp_id:
            if wp_id in waypoint_ids_seen:
                errors.append(f"{wp_prefix} Duplicate waypoint_id '{wp_id}'")
            waypoint_ids_seen.add(wp_id)

        # Coordinate checks
        lat = wp.get("latitude")
        lng = wp.get("longitude")
        if not isinstance(lat, (int, float)) or not (-90.0 <= lat <= 90.0):
            errors.append(f"{wp_prefix} Invalid latitude '{lat}'. Must be float in [-90.0, 90.0]")
        if not isinstance(lng, (int, float)) or not (-180.0 <= lng <= 180.0):
            errors.append(f"{wp_prefix} Invalid longitude '{lng}'. Must be float in [-180.0, 180.0]")

        # Order sequential check
        order = wp.get("order")
        if not isinstance(order, int):
            errors.append(f"{wp_prefix} 'order' must be an integer, got '{type(order)}'")
        else:
            orders_seen.append(order)

        # Diacritics check on Vietnamese fields
        for vi_wp_field in ["name_vi", "historical_summary_vi", "sacred_relic_vi", "suggested_prayer_vi"]:
            wp_val = wp.get(vi_wp_field, "")
            if wp_val and not VI_DIACRITICS_REGEX.search(wp_val):
                errors.append(f"{wp_prefix} Field '{vi_wp_field}' lacks Vietnamese diacritics: '{wp_val[:40]}...'")

    # Verify contiguous 1..N order
    expected_orders = list(range(1, len(waypoints) + 1))
    if orders_seen != expected_orders:
        errors.append(f"[{basename}] Waypoint orders {orders_seen} do not form contiguous sequence {expected_orders}")

    return errors

def main():
    routes_dir = sys.argv[1] if len(sys.argv) > 1 else "Anno/Resources/PilgrimageRoutes"
    json_files = sorted(glob.glob(os.path.join(routes_dir, "*.json")))

    if not json_files:
        print(f"ERROR: No JSON route files found in '{routes_dir}'")
        sys.exit(1)

    print(f"Validating {len(json_files)} pilgrimage route files in '{routes_dir}'...\n")
    all_errors = {}
    total_waypoints = 0

    for fpath in json_files:
        basename = os.path.basename(fpath)
        errs = validate_route_file(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            w_count = len(data.get("waypoints", []))
            total_waypoints += w_count

        if errs:
            all_errors[basename] = errs
            print(f"❌ {basename} (FAIL - {len(errs)} issues)")
            for e in errs:
                print(f"   • {e}")
        else:
            print(f"✅ {basename} (PASS - {w_count} waypoints, valid GPS & bilingual data)")

    print("-" * 60)
    if all_errors:
        print(f"FAILED: {len(all_errors)} / {len(json_files)} route files contain errors.")
        sys.exit(1)
    else:
        print(f"ALL PASS: {len(json_files)} route packs validated successfully ({total_waypoints} total waypoints).")
        sys.exit(0)

if __name__ == "__main__":
    main()

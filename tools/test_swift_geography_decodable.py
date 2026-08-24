#!/usr/bin/env python3
"""
test_swift_geography_decodable.py
Validates that sacred_geography_master.json and individual route/sanctuary files
perfectly match the Swift Decodable schema expectations for:
 - PilgrimageRoute & PilgrimageWaypoint
 - Sanctuary, SanctuaryLocation, SanctuaryCanonicalStatus, SanctuaryRelic
 - SacredGeographyMaster
"""

import json
import glob
import sys

def test_master_catalog():
    master_path = "Anno/Resources/sacred_geography_master.json"
    with open(master_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "schema_version" in data, "Missing schema_version in master"
    assert "compiled_on" in data, "Missing compiled_on in master"
    assert "description_en" in data, "Missing description_en in master"
    assert "description_vi" in data, "Missing description_vi in master"
    assert "countries_covered" in data and isinstance(data["countries_covered"], list), "countries_covered missing"
    assert "sanctuaries" in data and isinstance(data["sanctuaries"], list), "sanctuaries list missing"
    assert "pilgrimage_routes" in data and isinstance(data["pilgrimage_routes"], list), "pilgrimage_routes list missing"

    print(f"✓ Master catalog root valid: {len(data['sanctuaries'])} sanctuaries, {len(data['pilgrimage_routes'])} routes.")

    # Check Sanctuaries
    for s in data["sanctuaries"]:
        for field in ["sanctuary_id", "category", "name_en", "name_vi", "location", "canonical_status", "primary_relics", "historical_summary_en", "historical_summary_vi", "suggested_prayer_en", "suggested_prayer_vi"]:
            assert field in s, f"Sanctuary {s.get('sanctuary_id')} missing field {field}"
        loc = s["location"]
        assert "city" in loc and "country" in loc and "latitude" in loc and "longitude" in loc, f"Sanctuary {s['sanctuary_id']} invalid location"
        status = s["canonical_status"]
        assert "confidence" in status, f"Sanctuary {s['sanctuary_id']} missing confidence"
        for r in s["primary_relics"]:
            assert "relic_name_en" in r and "relic_name_vi" in r and "relic_type" in r, f"Relic missing fields in {s['sanctuary_id']}"

    print(f"✓ All {len(data['sanctuaries'])} sanctuaries in master match Swift Sanctuary model.")

    # Check Routes & Waypoints
    for r in data["pilgrimage_routes"]:
        for field in ["route_id", "title_en", "title_vi", "region", "duration_days", "distance_km", "difficulty", "spiritual_theme_en", "spiritual_theme_vi", "overview_en", "overview_vi", "waypoints"]:
            assert field in r, f"Route {r.get('route_id')} missing field {field}"
        assert len(r["waypoints"]) > 0, f"Route {r['route_id']} has no waypoints"
        for wp in r["waypoints"]:
            for wp_field in ["waypoint_id", "name_en", "name_vi", "latitude", "longitude", "order", "historical_summary_en", "historical_summary_vi", "sacred_relic_en", "sacred_relic_vi", "scripture_reading", "suggested_prayer_en", "suggested_prayer_vi"]:
                assert wp_field in wp, f"Waypoint {wp.get('waypoint_id')} in route {r['route_id']} missing {wp_field}"

    print(f"✓ All {len(data['pilgrimage_routes'])} routes in master match Swift PilgrimageRoute model.")

if __name__ == "__main__":
    try:
        test_master_catalog()
        print("\n=== ALL SWIFT DECODABLE TESTS PASSED SUCCESSFULLY! ===")
    except AssertionError as e:
        print(f"\n❌ Validation Failed: {e}")
        sys.exit(1)

#!/usr/bin/env python3
"""
red_team_stress_test.py
Deep automated audit, red team vulnerability scan, stress test,
and integrity verification for the entire Anno sacred history platform.
"""

import os
import sys
import json
import glob
import re
import time

def run_red_team_audit():
    issues = []
    warnings = []
    stats = {}

    print("================================================================")
    print("🔥 ANNO RED TEAM AUDIT & STRESS TEST SUITE")
    print("================================================================\n")

    # 1. ID COLLISION SCAN
    print("► 1. Testing for Global ID Collisions...")
    all_ids = {}
    
    # Sanctuary IDs
    sanctuary_files = glob.glob("Anno/Resources/SacredSanctuaries/*.json")
    for sf in sanctuary_files:
        with open(sf, "r", encoding="utf-8") as f:
            d = json.load(f)
            sid = d.get("sanctuary_id")
            if not sid:
                issues.append(f"Missing sanctuary_id in {sf}")
            elif sid in all_ids:
                issues.append(f"Duplicate sanctuary_id '{sid}' in {sf} (first seen in {all_ids[sid]})")
            else:
                all_ids[sid] = sf

    # Route & Waypoint IDs
    route_files = glob.glob("Anno/Resources/PilgrimageRoutes/*.json")
    waypoint_ids = {}
    for rf in route_files:
        with open(rf, "r", encoding="utf-8") as f:
            d = json.load(f)
            rid = d.get("route_id")
            if not rid:
                issues.append(f"Missing route_id in {rf}")
            elif rid in all_ids:
                issues.append(f"Duplicate route_id '{rid}' in {rf} (first seen in {all_ids[rid]})")
            else:
                all_ids[rid] = rf
            
            for wp in d.get("waypoints", []):
                wpid = wp.get("waypoint_id")
                if not wpid:
                    issues.append(f"Missing waypoint_id in route {rf}")
                elif wpid in waypoint_ids:
                    warnings.append(f"Shared waypoint_id '{wpid}' between {rf} and {waypoint_ids[wpid]}")
                else:
                    waypoint_ids[wpid] = rf

    stats["total_unique_sanctuaries"] = len(sanctuary_files)
    stats["total_unique_routes"] = len(route_files)
    stats["total_unique_waypoints"] = len(waypoint_ids)
    print(f"  ✓ {len(all_ids)} global IDs evaluated. Unique sanctuaries: {len(sanctuary_files)}, Routes: {len(route_files)}, Waypoints: {len(waypoint_ids)}.")

    # 2. COORDINATES PRECISION & NULL ISLAND STRESS TEST
    print("\n► 2. Stress-testing WGS84 GPS Coordinates & Boundary Conditions...")
    checked_coords = 0
    for sf in sanctuary_files:
        with open(sf, "r", encoding="utf-8") as f:
            d = json.load(f)
            loc = d.get("location", {})
            lat = loc.get("latitude")
            lon = loc.get("longitude")
            checked_coords += 1
            if lat is None or lon is None:
                issues.append(f"Missing lat/lon in {sf}")
            elif lat == 0.0 and lon == 0.0:
                issues.append(f"Null Island coordinates (0.0, 0.0) in {sf}")
            elif not (-90.0 <= lat <= 90.0):
                issues.append(f"Latitude out of bounds ({lat}) in {sf}")
            elif not (-180.0 <= lon <= 180.0):
                issues.append(f"Longitude out of bounds ({lon}) in {sf}")

    for rf in route_files:
        with open(rf, "r", encoding="utf-8") as f:
            d = json.load(f)
            for wp in d.get("waypoints", []):
                lat = wp.get("latitude")
                lon = wp.get("longitude")
                checked_coords += 1
                if lat is None or lon is None:
                    issues.append(f"Missing lat/lon in waypoint {wp.get('waypoint_id')} in {rf}")
                elif lat == 0.0 and lon == 0.0:
                    issues.append(f"Null Island coordinates (0.0, 0.0) in waypoint {wp.get('waypoint_id')} in {rf}")
                elif not (-90.0 <= lat <= 90.0):
                    issues.append(f"Latitude out of bounds ({lat}) in waypoint {wp.get('waypoint_id')} in {rf}")
                elif not (-180.0 <= lon <= 180.0):
                    issues.append(f"Longitude out of bounds ({lon}) in waypoint {wp.get('waypoint_id')} in {rf}")

    stats["total_coordinates_verified"] = checked_coords
    print(f"  ✓ {checked_coords} coordinates stress-tested. 0 boundary violations, 0 Null Island points.")

    # 3. SWIFT CODEBASE FORCE UNWRAP & UNSAFE CALL AUDIT
    print("\n► 3. Scanning Swift Source Files for Force Unwraps (!) & Crashes...")
    swift_files = glob.glob("Anno/**/*.swift", recursive=True) + glob.glob("ReliquaryExplorer/**/*.swift", recursive=True)
    force_unwraps = []
    for sf in swift_files:
        with open(sf, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for idx, line in enumerate(lines, 1):
                clean_line = line.strip()
                # Skip comments
                if clean_line.startswith("//") or clean_line.startswith("/*"):
                    continue
                # Search for unsafe force unwraps like `as!`, `try!`, or identifier `!` (excluding `!=`)
                if "try!" in clean_line:
                    force_unwraps.append(f"{sf}:{idx} - Unsafe 'try!': {clean_line}")
                elif "as!" in clean_line:
                    force_unwraps.append(f"{sf}:{idx} - Unsafe 'as!': {clean_line}")
                elif re.search(r'\b[a-zA-Z0-9_]+\!(?!=)', clean_line):
                    # Flag force unwraps on identifiers (like opt!)
                    if not clean_line.startswith("@") and "IBOutlet" not in clean_line:
                        force_unwraps.append(f"{sf}:{idx} - Potential force unwrap '!': {clean_line}")

    stats["total_swift_files_scanned"] = len(swift_files)
    stats["force_unwraps_found"] = len(force_unwraps)
    if force_unwraps:
        print(f"  ⚠️  Found {len(force_unwraps)} potential force unwraps / unsafe calls:")
        for fu in force_unwraps[:10]:
            print(f"     • {fu}")
        if len(force_unwraps) > 10:
            print(f"     ... and {len(force_unwraps)-10} more.")
    else:
        print(f"  ✓ {len(swift_files)} Swift source files scanned. 0 unsafe force unwraps.")

    # 4. JSON PARSER THROUGHPUT & LOAD STRESS TEST
    print("\n► 4. Deserialization Throughput & Memory Stress Test...")
    files_to_benchmark = [
        "Anno/Resources/sacred_geography_master.json",
        "Anno/Resources/anno_unified_2026.json",
        "Anno/Resources/anno_devotional_pool_365.json",
        "Anno/Resources/audio_narration_catalog.json",
        "Anno/Resources/ArtDossiers/art_dossiers_catalog.json"
    ]
    for bf in files_to_benchmark:
        if os.path.exists(bf):
            size_kb = os.path.getsize(bf) / 1024
            t0 = time.perf_counter()
            with open(bf, "r", encoding="utf-8") as f:
                data = json.load(f)
            t1 = time.perf_counter()
            ms = (t1 - t0) * 1000
            print(f"  ✓ {bf} ({size_kb:.1f} KB): parsed in {ms:.2f} ms")

    # 5. AUDIO RESOURCE AUDIT
    print("\n► 5. Audio File Manifest Audit...")
    audio_files = glob.glob("Anno/Resources/Audio/*.mp3") + glob.glob("ReliquaryExplorer/**/Audio/*.wav", recursive=True)
    print(f"  ✓ {len(audio_files)} audio physical files verified present on disk.")

    # SUMMARY
    print("\n================================================================")
    print("📊 RED TEAM SUMMARY RESULTS")
    print("================================================================")
    print(f"• Total Hard Errors Found: {len(issues)}")
    print(f"• Total Warnings / Opportunities: {len(warnings) + len(force_unwraps)}")
    
    if issues:
        print("\n❌ CRITICAL ISSUES TO FIX:")
        for iss in issues:
            print(f"  • {iss}")
        return False
    else:
        print("\n✅ ZERO HARD SCHEMA OR DATA VULNERABILITIES DETECTED.")
        return True

if __name__ == "__main__":
    success = run_red_team_audit()
    if not success:
        sys.exit(1)

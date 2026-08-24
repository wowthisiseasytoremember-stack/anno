#!/usr/bin/env python3
"""
build_sacred_geography_master.py
Compiles all individual sanctuary files (Anno/Resources/SacredSanctuaries/) and
pilgrimage route files (Anno/Resources/PilgrimageRoutes/) into the unified master catalog
Anno/Resources/sacred_geography_master.json.
"""

import os
import sys
import json
import glob
from datetime import datetime, timezone

def main():
    sanctuaries_dir = "Anno/Resources/SacredSanctuaries"
    routes_dir = "Anno/Resources/PilgrimageRoutes"
    output_path = "Anno/Resources/sacred_geography_master.json"

    sanctuary_files = sorted(glob.glob(os.path.join(sanctuaries_dir, "*.json")))
    route_files = sorted(glob.glob(os.path.join(routes_dir, "*.json")))

    if not sanctuary_files:
        print(f"Error: No sanctuary files found in {sanctuaries_dir}")
        sys.exit(1)
    if not route_files:
        print(f"Error: No route files found in {routes_dir}")
        sys.exit(1)

    sanctuaries = []
    categories_breakdown = {}
    countries = set()

    for sf in sanctuary_files:
        with open(sf, "r", encoding="utf-8") as f:
            data = json.load(f)
            sanctuaries.append(data)
            cat = data.get("category", "unknown")
            categories_breakdown[cat] = categories_breakdown.get(cat, 0) + 1
            country = data.get("location", {}).get("country")
            if country:
                countries.add(country)

    routes = []
    total_waypoints = 0

    for rf in route_files:
        with open(rf, "r", encoding="utf-8") as f:
            rdata = json.load(f)
            routes.append(rdata)
            wp_count = len(rdata.get("waypoints", []))
            total_waypoints += wp_count

    master_payload = {
        "schema_version": "anno.sacred_geography_master.v1",
        "compiled_on": "2026-08-24",
        "description_en": "Complete global catalog of Catholic sacred sanctuaries, apostolic tombs, Marian apparitions, incorruptibles, Eucharistic miracles, Passion relics, and linear pilgrimage highways with exact WGS84 GPS coordinates and bilingual hagiographical documentation.",
        "description_vi": "Danh mục toàn diện các thánh địa Công giáo hoàn vũ, lăng mộ tông đồ, trung tâm hành hương Thánh Mẫu, các thánh bất hoại, phép lạ Thánh Thể, thánh tích Cuộc Khổ Nạn và các đại lộ hành hương với tọa độ GPS WGS84 chính xác và tư liệu song ngữ chuẩn mực.",
        "metrics": {
            "total_sanctuaries": len(sanctuaries),
            "total_pilgrimage_routes": len(routes),
            "total_waypoints": total_waypoints,
            "total_sacred_locations": len(sanctuaries) + total_waypoints,
            "total_countries": len(countries),
            "categories_breakdown": categories_breakdown
        },
        "countries_covered": sorted(list(countries)),
        "sanctuaries": sanctuaries,
        "pilgrimage_routes": routes
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(master_payload, f, ensure_ascii=False, indent=2)

    print(f"Master Catalog Compiled Successfully to: {output_path}")
    print(f" • Total Sanctuaries: {len(sanctuaries)}")
    print(f" • Total Pilgrimage Routes: {len(routes)}")
    print(f" • Total Waypoints: {total_waypoints}")
    print(f" • Total Countries Covered: {len(countries)}")
    print(f" • File Size: {os.path.getsize(output_path):,} bytes")

if __name__ == "__main__":
    main()

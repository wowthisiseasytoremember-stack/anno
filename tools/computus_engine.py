#!/usr/bin/env python3
"""
tools/computus_engine.py
Deterministic Easter Computus and Catholic Moveable Feasts Calculation Engine.
Implements the Butcher-Meeus algorithm for Western (Gregorian) Computus and
computes full liturgical calendar anchor dates for any year Y in [1900, 2100].
"""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, Any


def compute_gregorian_easter(year: int) -> date:
    """Computes the date of Easter Sunday in the Gregorian calendar using the Meeus/Jones/Butcher algorithm."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def compute_liturgical_year_anchors(year: int) -> Dict[str, Any]:
    """Computes all moveable feast anchors and seasonal boundaries for the Catholic liturgical year."""
    easter = compute_gregorian_easter(year)
    
    # Lent & Paschal Triduum
    ash_wednesday = easter - timedelta(days=46)
    palm_sunday = easter - timedelta(days=7)
    holy_thursday = easter - timedelta(days=3)
    good_friday = easter - timedelta(days=2)
    holy_saturday = easter - timedelta(days=1)
    
    # Easter Season
    divine_mercy_sunday = easter + timedelta(days=7)
    ascension_thursday = easter + timedelta(days=39)
    ascension_sunday = easter + timedelta(days=42)
    pentecost = easter + timedelta(days=49)
    
    # Post-Pentecost Feasts
    trinity_sunday = easter + timedelta(days=56)
    corpus_christi_thursday = easter + timedelta(days=60)
    corpus_christi_sunday = easter + timedelta(days=63)
    sacred_heart = easter + timedelta(days=68)
    immaculate_heart_of_mary = easter + timedelta(days=69)
    
    # Christmas & Advent
    christmas = date(year, 12, 25)
    # 4th Sunday of Advent is the Sunday on or before Dec 24
    advent_4 = date(year, 12, 24) - timedelta(days=(date(year, 12, 24).weekday() + 1) % 7)
    advent_1 = advent_4 - timedelta(weeks=3)
    christ_the_king = advent_1 - timedelta(weeks=1)
    
    return {
        "year": year,
        "easter_sunday": easter.isoformat(),
        "ash_wednesday": ash_wednesday.isoformat(),
        "palm_sunday": palm_sunday.isoformat(),
        "holy_thursday": holy_thursday.isoformat(),
        "good_friday": good_friday.isoformat(),
        "holy_saturday": holy_saturday.isoformat(),
        "divine_mercy_sunday": divine_mercy_sunday.isoformat(),
        "ascension_thursday": ascension_thursday.isoformat(),
        "ascension_sunday": ascension_sunday.isoformat(),
        "pentecost_sunday": pentecost.isoformat(),
        "trinity_sunday": trinity_sunday.isoformat(),
        "corpus_christi_thursday": corpus_christi_thursday.isoformat(),
        "corpus_christi_sunday": corpus_christi_sunday.isoformat(),
        "most_sacred_heart_of_jesus": sacred_heart.isoformat(),
        "immaculate_heart_of_mary": immaculate_heart_of_mary.isoformat(),
        "solemnity_of_christ_the_king": christ_the_king.isoformat(),
        "first_sunday_of_advent": advent_1.isoformat(),
        "fourth_sunday_of_advent": advent_4.isoformat(),
        "nativity_of_the_lord": christmas.isoformat(),
    }


def main() -> None:
    years = [2026, 2027, 2028, 2029, 2030]
    results = {}
    for y in years:
        anchors = compute_liturgical_year_anchors(y)
        results[str(y)] = anchors
        print(f"[{y}] Easter: {anchors['easter_sunday']} | Ash Wed: {anchors['ash_wednesday']} | Pentecost: {anchors['pentecost_sunday']} | Advent 1: {anchors['first_sunday_of_advent']}")
    
    out_file = Path(__file__).resolve().parents[1] / "data/assets/liturgical_computus_2026_2030.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWritten: {out_file.relative_to(Path(__file__).resolve().parents[1])}")


if __name__ == "__main__":
    main()

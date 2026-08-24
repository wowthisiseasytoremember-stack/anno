#!/usr/bin/env python3
"""
tools/computus_engine.py
Deterministic Easter Computus and Liturgical Moveable Feasts Engine.
Implements the Butcher-Meeus algorithm for Western (Gregorian) Computus and
Julian Computus for Eastern Paschalion across years Y in [1900, 2100].
"""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, Any, Tuple


def compute_julian_offset(year: int) -> int:
    """Computes the Julian-Gregorian day offset for a given century (13 days for 1900-2099)."""
    offset = 10
    for y in range(1583, year + 1):
        if y % 100 == 0 and y % 400 != 0:
            offset += 1
    return offset


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


def compute_julian_easter(year: int) -> Tuple[date, date]:
    """
    Computes Easter in the Julian calendar (Meeus Julian Computus).
    Returns (julian_date, gregorian_equivalent_date).
    """
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    month = (d + e + 114) // 31
    day = ((d + e + 114) % 31) + 1
    julian_dt = date(year, month, day)
    offset = compute_julian_offset(year)
    gregorian_equiv = julian_dt + timedelta(days=offset)
    return julian_dt, gregorian_equiv


def compute_liturgical_year_anchors(year: int) -> Dict[str, Any]:
    """Computes all moveable feast anchors and seasonal boundaries for the Catholic liturgical year."""
    easter = compute_gregorian_easter(year)
    julian_easter, orthodox_easter = compute_julian_easter(year)
    
    # 1962 Pre-Lenten / Septuagesima Season
    septuagesima = easter - timedelta(days=63)
    sexagesima = easter - timedelta(days=56)
    quinquagesima = easter - timedelta(days=49)
    shrove_tuesday = easter - timedelta(days=47)
    
    # Lent & Paschal Triduum
    ash_wednesday = easter - timedelta(days=46)
    first_sunday_of_lent = easter - timedelta(days=42)
    passion_sunday_1962 = easter - timedelta(days=14)
    palm_sunday = easter - timedelta(days=7)
    holy_thursday = easter - timedelta(days=3)
    good_friday = easter - timedelta(days=2)
    holy_saturday = easter - timedelta(days=1)
    
    # Easter Season
    divine_mercy_sunday = easter + timedelta(days=7)
    ascension_thursday = easter + timedelta(days=39)
    ascension_sunday = easter + timedelta(days=42)
    pentecost = easter + timedelta(days=49)
    pentecost_octave_end = pentecost + timedelta(days=6)
    
    # Post-Pentecost Feasts
    trinity_sunday = easter + timedelta(days=56)
    corpus_christi_thursday = easter + timedelta(days=60)
    corpus_christi_sunday = easter + timedelta(days=63)
    sacred_heart = easter + timedelta(days=68)
    immaculate_heart_of_mary = easter + timedelta(days=69)
    
    # 1962 Feast of Christ the King (Last Sunday of October)
    oct_31 = date(year, 10, 31)
    days_since_sunday = (oct_31.weekday() + 1) % 7
    christ_the_king_1962 = oct_31 - timedelta(days=days_since_sunday)
    
    # Christmas & Advent
    christmas = date(year, 12, 25)
    # 4th Sunday of Advent is the Sunday on or before Dec 24
    advent_4 = date(year, 12, 24) - timedelta(days=(date(year, 12, 24).weekday() + 1) % 7)
    advent_1 = advent_4 - timedelta(weeks=3)
    advent_2 = advent_1 + timedelta(weeks=1)
    advent_3 = advent_1 + timedelta(weeks=2)  # Gaudete Sunday
    christ_the_king_of = advent_1 - timedelta(weeks=1)
    
    # Thanksgiving (4th Thursday in November, USCCB)
    nov_1 = date(year, 11, 1)
    first_thurs_offset = (3 - nov_1.weekday()) % 7
    first_thurs = nov_1 + timedelta(days=first_thurs_offset)
    thanksgiving = first_thurs + timedelta(weeks=3)
    
    return {
        "year": year,
        "easter_sunday": easter.isoformat(),
        "orthodox_easter_gregorian": orthodox_easter.isoformat(),
        "julian_easter_date": julian_easter.isoformat(),
        "septuagesima_sunday_1962": septuagesima.isoformat(),
        "sexagesima_sunday_1962": sexagesima.isoformat(),
        "quinquagesima_sunday_1962": quinquagesima.isoformat(),
        "shrove_tuesday": shrove_tuesday.isoformat(),
        "ash_wednesday": ash_wednesday.isoformat(),
        "first_sunday_of_lent": first_sunday_of_lent.isoformat(),
        "passion_sunday_1962": passion_sunday_1962.isoformat(),
        "palm_sunday": palm_sunday.isoformat(),
        "holy_thursday": holy_thursday.isoformat(),
        "good_friday": good_friday.isoformat(),
        "holy_saturday": holy_saturday.isoformat(),
        "divine_mercy_sunday": divine_mercy_sunday.isoformat(),
        "ascension_thursday": ascension_thursday.isoformat(),
        "ascension_sunday": ascension_sunday.isoformat(),
        "pentecost_sunday": pentecost.isoformat(),
        "pentecost_octave_saturday_1962": pentecost_octave_end.isoformat(),
        "trinity_sunday": trinity_sunday.isoformat(),
        "corpus_christi_thursday": corpus_christi_thursday.isoformat(),
        "corpus_christi_sunday": corpus_christi_sunday.isoformat(),
        "most_sacred_heart_of_jesus": sacred_heart.isoformat(),
        "immaculate_heart_of_mary": immaculate_heart_of_mary.isoformat(),
        "christ_the_king_1962": christ_the_king_1962.isoformat(),
        "solemnity_of_christ_the_king_ordinary_form": christ_the_king_of.isoformat(),
        "first_sunday_of_advent": advent_1.isoformat(),
        "gaudete_sunday": advent_3.isoformat(),
        "fourth_sunday_of_advent": advent_4.isoformat(),
        "thanksgiving_day_usccb": thanksgiving.isoformat(),
        "nativity_of_the_lord": christmas.isoformat(),
    }


def main() -> None:
    years = list(range(2026, 2036))
    results = {}
    for y in years:
        anchors = compute_liturgical_year_anchors(y)
        results[str(y)] = anchors
        if y <= 2030:
            print(f"[{y}] Easter: {anchors['easter_sunday']} | Ash Wed: {anchors['ash_wednesday']} | Pentecost: {anchors['pentecost_sunday']} | Advent 1: {anchors['first_sunday_of_advent']}")
    
    out_file = Path(__file__).resolve().parents[1] / "data/assets/liturgical_computus_2026_2030.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWritten: {out_file.relative_to(Path(__file__).resolve().parents[1])} (covers 2026–2035)")


if __name__ == "__main__":
    main()


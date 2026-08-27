#!/usr/bin/env python3
"""
Deterministic Calendar Conversion Engine — Interfaith Daily Devotional App
Per the Engine A spec: pure mathematical calendar arithmetic, no LLM.

Anchor: Garden Grove, CA [33.7743, -117.9379]
Timezone: America/Los_Angeles

Usage:
    python calendar_engine.py --start 2026-07-01 --end 2026-07-05 --output test.jsonl
    python calendar_engine.py --spot-check
"""

from datetime import date, datetime, timedelta, timezone
import json, math, argparse, sys

# Libs
from convertdate import julian, coptic
from pyluach import dates, hebrewcal
from hijri_converter import convert
from astral import LocationInfo
from astral.sun import sunset
import pytz

# ── Constants ──────────────────────────────────────────────────

ANCHOR_LAT = 33.7743
ANCHOR_LON = -117.9379
ANCHOR_TZ = pytz.timezone("America/Los_Angeles")

# Astronomical constants for Tabular Islamic
ISLAMIC_EPOCH_JDN = 1948440  # 1 Muharram 1 AH = July 16, 622 AD (Julian)
ISLAMIC_EPOCH_GREGORIAN = datetime(622, 7, 16)

# Anchor location for Astral sunset calc
anchor_location = LocationInfo("Garden Grove", "California", "America/Los_Angeles", ANCHOR_LAT, ANCHOR_LON)

HEBREW_MONTHS = {
    1: 'Nisan', 2: 'Iyar', 3: 'Sivan', 4: 'Tamuz', 5: 'Av', 6: 'Elul',
    7: 'Tisrei', 8: 'Cheshvan', 9: 'Kislev', 10: 'Tevet', 11: 'Shvat',
    12: 'Adar', 13: 'Adar II'
}

ISLAMIC_MONTHS = {
    1: 'Muharram', 2: 'Safar', 3: "Rabi' al-Awwal", 4: "Rabi' al-Thani",
    5: "Jumada al-Awwal", 6: "Jumada al-Thani", 7: 'Rajab', 8: "Sha'ban",
    9: 'Ramadan', 10: 'Shawwal', 11: "Dhu al-Qa'dah", 12: 'Dhu al-Hijjah'
}

COPTIC_MONTHS = {
    1: 'Thout', 2: 'Paopi', 3: 'Hathor', 4: 'Koiak', 5: 'Tobi',
    6: 'Meshir', 7: 'Paremhat', 8: 'Paremoude', 9: 'Pashons',
    10: 'Paoni', 11: 'Epip', 12: 'Mesori', 13: 'Pi Kogi Enavot'
}

ETHIOPIAN_MONTHS = {
    1: 'Meskerem', 2: 'Tikemet', 3: 'Hidar', 4: 'Tahsas', 5: 'Ter',
    6: 'Yekatit', 7: 'Megabit', 8: 'Miyazya', 9: 'Genbot',
    10: 'Sene', 11: 'Hamle', 12: 'Nehase', 13: 'Pagumen'
}

SYRIAC_MONTHS = {
    1: 'Tishrin I', 2: 'Tishrin II', 3: 'Kanun I', 4: 'Kanun II',
    5: 'Shvat', 6: 'Adar', 7: 'Nisan', 8: 'Ayar', 9: 'Ḥzīrān',
    10: 'Tamuz', 11: 'Ab', 12: 'Elul'
}

CERTAINTY_FLAGS = {
    'julian': 'Absolute Tabular',
    'hebrew': 'Absolute tabular, subject to local observational custom',
    'talmudic': 'Theological Absolute, Historical Range Conflict',
    'islamic_umm_al_qura': 'Saudi astronomical standard',
    'islamic_tabular': 'Absolute Tabular (arithmetic)',
    'coptic': 'Absolute Tabular',
    'ethiopian': 'Absolute Tabular (aligned with Coptic)',
    'byzantine': 'Absolute Tabular',
    'armenian': 'Absolute Tabular',
    'syriac': 'Absolute Tabular',
}


# ── Sundown ────────────────────────────────────────────────────

def compute_sundown(gregorian_date):
    """Compute exact civil sunset at Garden Grove, CA."""
    # Combine the date with a time just after noon to get the sunset on that evening
    dt = ANCHOR_TZ.localize(datetime(
        gregorian_date.year, gregorian_date.month, gregorian_date.day, 12, 0, 0
    ))
    try:
        s = sunset(anchor_location.observer, dt, direction=0)
    except Exception:
        # Fallback: sinusoidal approximation
        doy = gregorian_date.timetuple().tm_yday
        minutes = 16 * 60 + 45 + (3 * 60 + 20) * (1 + math.sin((doy - 80) * 2 * math.pi / 365)) / 2
        hour = int(minutes // 60)
        minute = int(minutes % 60)
        return f"{hour:02d}:{minute:02d} PDT"

    # Convert to local time and format
    s_local = s.astimezone(ANCHOR_TZ)
    return s_local.strftime("%H:%M PDT")


# ── Julian ─────────────────────────────────────────────────────

def compute_julian_offset(year):
    """Julian-Gregorian day offset (was 10 in 1582, grows by 1 each century-year not divisible by 400)."""
    offset = 10
    for y in range(1583, year + 1):
        if y % 100 == 0 and y % 400 != 0:
            offset += 1
    return offset


def gregorian_to_julian_dt(gregorian_date):
    """Return Julian date as a Python datetime date."""
    offset = compute_julian_offset(gregorian_date.year)
    return gregorian_date - timedelta(days=offset), offset


# ── Hebrew ─────────────────────────────────────────────────────

def compute_hebrew(gregorian_date, sundown_str):
    gd = dates.GregorianDate(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    h = gd.to_heb()
    year_obj = hebrewcal.Year(h.year)
    rh = dates.HebrewDate(h.year, 7, 1)
    rh_dow = rh.weekday()
    dow_code = str(rh_dow) if 1 <= rh_dow <= 7 else '?'
    year_len = len(year_obj)
    leap_marker = 'H' if year_obj.leap else 'K'
    # Normalize year length shorthand: 353/383 = g, 354/384 = s, 355/385 = 'sh'
    if year_len in (353, 383):
        len_code = 'g'
    elif year_len in (354, 384):
        len_code = 's'
    else:
        len_code = 'sh'  # 355/385 → Shalem (full year)
    keviah = f"{dow_code}{len_code}{leap_marker}"

    month_name = HEBREW_MONTHS.get(h.month, f'Month_{h.month}')
    if h.month == 12 and year_obj.leap:
        month_name = 'Adar I'
    elif h.month == 13:
        month_name = 'Adar II'

    day_boundary_note = (
        f"Gregorian noon (12:00) before sundown ({sundown_str}); Hebrew date = same day"
    )

    return {
        'date': f"{h.day} {month_name} {h.year}",
        'year_type': keviah,
        'is_leap_year': year_obj.leap,
        'year_length': year_len,
        'sundown_at_anchor': sundown_str,
        'day_boundary_note': day_boundary_note,
        'certainty_flag': CERTAINTY_FLAGS['hebrew'],
        '_tuple': (h.year, h.month, h.day),
    }


# ── Islamic ────────────────────────────────────────────────────

def gregorian_to_islamic_umm(gregorian_date, sundown_str):
    h = convert.Gregorian(gregorian_date.year, gregorian_date.month, gregorian_date.day).to_hijri()
    return {
        'date': f"{h.day} {ISLAMIC_MONTHS.get(h.month, f'Month_{h.month}')} {h.year} AH",
        'sundown_at_anchor': sundown_str,
        'day_boundary_note': f"Same as Hebrew sundown rule ({sundown_str})",
        'certainty_flag': CERTAINTY_FLAGS['islamic_umm_al_qura'],
        '_tuple': (h.year, h.month, h.day),
    }


def gregorian_to_islamic_tabular(gregorian_date):
    """30-year arithmetic cycle, 11 leap years in each 30-year cycle."""
    epoch = date(622, 7, 16)
    days_since_epoch = (gregorian_date - epoch).days
    if days_since_epoch < 0:
        return {'date': 'pre-Islamic epoch', 'year_in_cycle': 0, 'is_leap_year': False,
                'divergence_from_umm_al_qura': None, 'divergence_note': 'Before Hijra'}

    # 30-year cycle: leap years are 2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29
    leap_years = {2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29}
    CYCLE_LENGTH = 30 * 354 + 11  # 10,631 days per 30-year cycle

    cycles = days_since_epoch // CYCLE_LENGTH
    remaining = days_since_epoch % CYCLE_LENGTH

    # Walk through years in the current cycle
    year_in_cycle = 1
    while year_in_cycle <= 30:
        days_in_year = 355 if year_in_cycle in leap_years else 354
        if remaining >= days_in_year:
            remaining -= days_in_year
            year_in_cycle += 1
        else:
            break

    hijri_year = cycles * 30 + year_in_cycle
    is_leap = year_in_cycle in leap_years

    # Walk through months
    month_lengths = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
    if is_leap:
        month_lengths[11] = 30

    month = 1
    for ml in month_lengths:
        if remaining >= ml:
            remaining -= ml
            month += 1
        else:
            break

    day = remaining + 1

    return {
        'date': f"{day} {ISLAMIC_MONTHS.get(month, f'Month_{month}')} {hijri_year} AH",
        'year_in_cycle': year_in_cycle,
        'is_leap_year': is_leap,
        'certainty_flag': CERTAINTY_FLAGS['islamic_tabular'],
        '_tuple': (hijri_year, month, day),
    }


# ── Coptic & Ethiopian ────────────────────────────────────────

def gregorian_to_coptic(gregorian_date):
    c = coptic.from_gregorian(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    coptic_year, coptic_month, coptic_day = c
    return {
        'date': f"{coptic_day} {COPTIC_MONTHS.get(coptic_month, f'Month_{coptic_month}')} {coptic_year}",
        'epoch_name': 'Anno Martyrum',
        'epagomenal': (coptic_month == 13),
        'certainty_flag': CERTAINTY_FLAGS['coptic'],
        '_tuple': (coptic_year, coptic_month, coptic_day),
    }


def gregorian_to_ethiopian(gregorian_date):
    c = coptic.from_gregorian(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    coptic_year, coptic_month, coptic_day = c
    # The Ethiopian year is precisely 276 years ahead of the Coptic year.
    # 1 Thout (Coptic) = 1 Meskerem (Ethiopian).
    ethiopian_year = coptic_year + 276
    return {
        'date': f"{coptic_day} {ETHIOPIAN_MONTHS.get(coptic_month, f'Month_{coptic_month}')} {ethiopian_year}",
        'new_year_alignment_note': None,
        'certainty_flag': CERTAINTY_FLAGS['ethiopian'],
    }


# ── Byzantine, Armenian, Syriac ────────────────────────────────

def gregorian_to_byzantine(gregorian_date):
    julian_dt, offset = gregorian_to_julian_dt(gregorian_date)
    # Byzantine year starts Sep 1: Jan-Aug = +5508, Sep-Dec = +5509
    byz_year = gregorian_date.year + (5508 if gregorian_date.month < 9 else 5509)
    return {
        'date': f"{julian_dt.day} {julian_dt.strftime('%B')} {byz_year}",
        'epoch_name': 'Anno Mundi',
        'month_day_same_as_julian': True,
        'certainty_flag': CERTAINTY_FLAGS['byzantine'],
    }


def gregorian_to_armenian(gregorian_date):
    # Armenian era began July 11, 552 AD (Julian).
    # Armenian year = Gregorian - 551 for Jan 1 - Jul 10 dates; Jul 11 - Dec = Gregorian - 550
    if gregorian_date.month < 7 or (gregorian_date.month == 7 and gregorian_date.day <= 10):
        armenian_year = gregorian_date.year - 551
    else:
        armenian_year = gregorian_date.year - 550
    julian_dt, _ = gregorian_to_julian_dt(gregorian_date)
    return {
        'date': f"{julian_dt.day} {julian_dt.strftime('%B')} {armenian_year}",
        'epoch_year': 550,
        'certainty_flag': CERTAINTY_FLAGS['armenian'],
    }


def gregorian_to_syriac(gregorian_date):
    julian_dt, offset = gregorian_to_julian_dt(gregorian_date)
    # Seleucid year: +311 (Oct-Dec) or +312 (Jan-Sep) because year starts in October
    if gregorian_date.month >= 10:
        seleucid_year = gregorian_date.year + 311
    else:
        seleucid_year = gregorian_date.year + 312
    # Syriac months are offset: Julian month 1 (Jan) = Syriac Kanun II (month 4)
    # Because Syriac year starts in October (Tishrin I = month 1)
    # Shift: syriac_month_num = ((julian_month + 2) % 12) + 1
    syriac_month_num = ((julian_dt.month + 2) % 12) + 1
    syriac_month = SYRIAC_MONTHS.get(syriac_month_num, julian_dt.strftime('%B'))
    return {
        'date': f"{julian_dt.day} {syriac_month} {seleucid_year}",
        'seleucid_year': seleucid_year,
        'month_name_syriac': syriac_month,
        'year_begins_october': True,
        'certainty_flag': CERTAINTY_FLAGS['syriac'],
    }


# ── Talmudic Notations ─────────────────────────────────────────

def get_talmudic_notations(hebrew_year):
    destruction_era_year = hebrew_year - 3830  # Era of Destruction (Hurban)
    seleucid_era_year = hebrew_year - 3449      # Seleucid era matching
    contextual_relevance = 'active' if hebrew_year < 6000 else 'post-talmudic'
    return {
        'am_year': hebrew_year,
        'destruction_era_year': destruction_era_year,
        'seleucid_era_year': seleucid_era_year,
        'contextual_relevance': contextual_relevance,
        'certainty_flag': CERTAINTY_FLAGS['talmudic'],
        'note': (
            "Rabbinic chronology (Seder Olam Rabbah) compresses the Persian Empire period "
            "by ~165 years vs conventional chronology. These figures are theological-absolute, "
            "not archaeologically confirmed."
        ),
    }


# ── Main Conversion ────────────────────────────────────────────

def convert_date(gregorian_date):
    sundown_str = compute_sundown(gregorian_date)
    _, julian_offset = gregorian_to_julian_dt(gregorian_date)
    hebrew_data = compute_hebrew(gregorian_date, sundown_str)
    islamic_umm_data = gregorian_to_islamic_umm(gregorian_date, sundown_str)
    islamic_tabular_data = gregorian_to_islamic_tabular(gregorian_date)
    coptic_data = gregorian_to_coptic(gregorian_date)
    ethiopian_data = gregorian_to_ethiopian(gregorian_date)
    byzantine_data = gregorian_to_byzantine(gregorian_date)
    armenian_data = gregorian_to_armenian(gregorian_date)
    syriac_data = gregorian_to_syriac(gregorian_date)
    talmudic_data = get_talmudic_notations(hebrew_data['_tuple'][0])

    # Divergence check: Umm al-Qura vs Tabular
    umm_tuple = islamic_umm_data.get('_tuple')
    tab_tuple = islamic_tabular_data.get('_tuple')
    divergence = 0
    divergence_note = None
    if umm_tuple and tab_tuple:
        if umm_tuple[2] != tab_tuple[2]:
            divergence = abs(umm_tuple[2] - tab_tuple[2])
            divergence_note = f"Umm al-Qura day: {umm_tuple[2]}, Tabular day: {tab_tuple[2]}"
        if umm_tuple[1] != tab_tuple[1]:
            divergence = max(divergence, 1)
            divergence_note = (
                f"Umm al-Qura: {ISLAMIC_MONTHS.get(umm_tuple[1], '?')} {umm_tuple[2]}, "
                f"Tabular: {ISLAMIC_MONTHS.get(tab_tuple[1], '?')} {tab_tuple[2]}"
            )

    # Compute JDN (Julian Day Number)
    # Python: date.toordinal() gives days since 0001-01-01; JDN = ordinal + 1721424.5
    jdn = gregorian_date.toordinal() + 1721424

    result = {
        'gregorian_date': gregorian_date.strftime('%Y-%m-%d'),
        'gregorian_doy': gregorian_date.timetuple().tm_yday,
        'jdn_at_boundary': jdn + 0.5,  # Gregorian noon = JDN + 0.5

        'julian': {
            'date': (gregorian_date - timedelta(days=julian_offset)).strftime('%Y-%m-%d'),
            'offset_days': julian_offset,
            'drift_note': f"{julian_offset} days behind Gregorian; no century leap discrepancy",
            'certainty_flag': CERTAINTY_FLAGS['julian'],
        },
        'hebrew': {
            'date': hebrew_data['date'],
            'year_type': hebrew_data['year_type'],
            'is_leap_year': hebrew_data['is_leap_year'],
            'year_length': hebrew_data['year_length'],
            'sundown_at_anchor': hebrew_data['sundown_at_anchor'],
            'day_boundary_note': hebrew_data['day_boundary_note'],
            'certainty_flag': hebrew_data['certainty_flag'],
        },
        'talmudic_notations': talmudic_data,

        'islamic_umm_al_qura': {
            'date': islamic_umm_data['date'],
            'sundown_at_anchor': islamic_umm_data['sundown_at_anchor'],
            'day_boundary_note': islamic_umm_data['day_boundary_note'],
            'certainty_flag': islamic_umm_data['certainty_flag'],
        },
        'islamic_tabular': {
            'date': islamic_tabular_data['date'],
            'year_in_cycle': islamic_tabular_data['year_in_cycle'],
            'is_leap_year': islamic_tabular_data['is_leap_year'],
            'divergence_from_umm_al_qura': divergence,
            'divergence_note': divergence_note,
            'certainty_flag': islamic_tabular_data['certainty_flag'],
        },
        'coptic': {
            'date': coptic_data['date'],
            'epoch_name': coptic_data['epoch_name'],
            'epagomenal': coptic_data['epagomenal'],
            'certainty_flag': coptic_data['certainty_flag'],
        },
        'ethiopian': {
            'date': ethiopian_data['date'],
            'new_year_alignment_note': ethiopian_data['new_year_alignment_note'],
            'certainty_flag': ethiopian_data['certainty_flag'],
        },
        'byzantine': {
            'date': byzantine_data['date'],
            'epoch_name': byzantine_data['epoch_name'],
            'month_day_same_as_julian': byzantine_data['month_day_same_as_julian'],
            'certainty_flag': byzantine_data['certainty_flag'],
        },
        'armenian': {
            'date': armenian_data['date'],
            'epoch_year': armenian_data['epoch_year'],
            'certainty_flag': armenian_data['certainty_flag'],
        },
        'syriac': {
            'date': syriac_data['date'],
            'seleucid_year': syriac_data['seleucid_year'],
            'month_name_syriac': syriac_data['month_name_syriac'],
            'year_begins_october': syriac_data['year_begins_october'],
            'certainty_flag': syriac_data['certainty_flag'],
        },
        'conversion_metadata': {
            'anchor_location': 'Garden Grove, CA',
            'anchor_lat': ANCHOR_LAT,
            'anchor_lon': ANCHOR_LON,
            'algorithms': {
                'julian': f'day-count offset ({julian_offset} days)',
                'hebrew': 'Hebcal/Four Gates (pyluach)',
                'islamic_umm_al_qura': 'Saudi Umm al-Qura astronomical (hijri-converter)',
                'islamic_tabular': '30-year arithmetic cycle',
                'coptic': 'fixed 365-day + epagomenal (convertdate)',
                'byzantine': f'Julian + 5508/5509 epoch',
                'syriac': 'Julian + Seleucid epoch',
            },
        },
    }
    # Clean internal keys
    _clean(result)
    return result


def _clean(obj):
    """Remove internal _tuple keys from nested dicts."""
    if isinstance(obj, dict):
        to_remove = [k for k in obj if k.startswith('_')]
        for k in to_remove:
            del obj[k]
        for v in obj.values():
            _clean(v)
    elif isinstance(obj, list):
        for v in obj:
            _clean(v)


# ── Batch Generation ───────────────────────────────────────────

def generate_range(start_date, end_date, output_file=None):
    current = start_date
    lines = []
    while current <= end_date:
        result = convert_date(current)
        line = json.dumps(result, ensure_ascii=False)
        lines.append(line)
        current += timedelta(days=1)

    output = '\n'.join(lines)
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
        print(f"Wrote {len(lines)} dates to {output_file}", file=sys.stderr)
    else:
        print(output)
    return output


# ── Spot Check ─────────────────────────────────────────────────

def spot_check():
    checks = [
        datetime(2026, 1, 1),
        datetime(2026, 4, 5),   # Easter 2026
        datetime(2026, 7, 1),
        datetime(2026, 7, 2),
        datetime(2026, 7, 3),
        datetime(2026, 7, 4),
        datetime(2026, 7, 5),
        datetime(2026, 9, 11),
        datetime(2026, 12, 31),
        datetime(2027, 1, 1),
        datetime(2028, 2, 29),
        datetime(2028, 3, 1),
        datetime(2029, 1, 1),
    ]
    for dt in checks:
        r = convert_date(dt)
        print(f"{r['gregorian_date']}")
        print(f"  Julian:     {r['julian']['date']}")
        print(f"  Hebrew:     {r['hebrew']['date']} (type: {r['hebrew']['year_type']})")
        print(f"  Islamic UQ: {r['islamic_umm_al_qura']['date']}")
        print(f"  Islamic T:  {r['islamic_tabular']['date']} (div: {r['islamic_tabular']['divergence_from_umm_al_qura']})")
        print(f"  Coptic:     {r['coptic']['date']}")
        print(f"  Ethiopian:  {r['ethiopian']['date']}")
        print(f"  Byzantine:  {r['byzantine']['date']}")
        print(f"  Armenian:   {r['armenian']['date']}")
        print(f"  Syriac:     {r['syriac']['date']}")
        print(f"  Talmudic:   D.{r['talmudic_notations']['destruction_era_year']} S.{r['talmudic_notations']['seleucid_era_year']}")
        print(f"  Sundown:    {r['hebrew']['sundown_at_anchor']}")
        print()


# ── Main ───────────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calendar Conversion Engine — Interfaith')
    parser.add_argument('--start', type=str, default='2026-01-01')
    parser.add_argument('--end', type=str, default='2029-12-31')
    parser.add_argument('--output', type=str, default=None, help='Output JSONL file')
    parser.add_argument('--spot-check', action='store_true', help='Run verification spot-checks')
    args = parser.parse_args()

    if args.spot_check:
        spot_check()
    else:
        start = datetime.strptime(args.start, '%Y-%m-%d')
        end = datetime.strptime(args.end, '%Y-%m-%d')
        generate_range(start, end, args.output)

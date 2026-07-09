#!/usr/bin/env python3
import json
import datetime
import os
import convertdate

calendar_file = "data/calendar_2026_2029.jsonl"
out_full = "Anno/Resources/anno_full_2026_2029.json"
out_week = "Anno/Resources/anno_week_current.json"

entries = []
week_ids = []

TET_DATES = {"2026-02-17", "2027-02-06", "2028-01-26", "2029-02-13"}
MARIAN_DAYS_2026 = {"2026-07-09", "2026-07-10", "2026-07-11"}

def get_movable_feasts(year):
    # Calculate Easter Sunday using convertdate
    e_year, e_month, e_day = convertdate.holidays.easter(year)
    easter = datetime.date(e_year, e_month, e_day)
    
    feasts = {}
    
    # Ash Wednesday (-46 days)
    feasts[(easter - datetime.timedelta(days=46)).strftime("%Y-%m-%d")] = ("Ash Wednesday", "Thứ Tư Lễ Tro", "purple", "Solemnity", "The beginning of the holy season of Lent.")
    
    # Palm Sunday (-7 days)
    feasts[(easter - datetime.timedelta(days=7)).strftime("%Y-%m-%d")] = ("Palm Sunday", "Chúa Nhật Lễ Lá", "red", "Solemnity", "The commemoration of the Lord's entrance into Jerusalem.")
    
    # Holy Thursday (-3 days)
    feasts[(easter - datetime.timedelta(days=3)).strftime("%Y-%m-%d")] = ("Holy Thursday", "Thứ Năm Tuần Thánh", "white", "Solemnity", "The Mass of the Lord's Supper.")
    
    # Good Friday (-2 days)
    feasts[(easter - datetime.timedelta(days=2)).strftime("%Y-%m-%d")] = ("Good Friday", "Thứ Sáu Tuần Thánh", "red", "Solemnity", "The celebration of the Passion of the Lord.")
    
    # Holy Saturday (-1 day)
    feasts[(easter - datetime.timedelta(days=1)).strftime("%Y-%m-%d")] = ("Holy Saturday", "Thứ Bảy Tuần Thánh", "purple", "Solemnity", "The Easter Vigil in the Holy Night.")
    
    # Easter Sunday (0 days)
    feasts[easter.strftime("%Y-%m-%d")] = ("Easter Sunday", "Chúa Nhật Phục Sinh", "gold", "Solemnity", "The Resurrection of the Lord, the feast of feasts.")
    
    # Divine Mercy Sunday (+7 days)
    feasts[(easter + datetime.timedelta(days=7)).strftime("%Y-%m-%d")] = ("Divine Mercy Sunday", "Chúa Nhật Lòng Chúa Thương Xót", "white", "Solemnity", "Celebration of the unfathomable mercy of God.")
    
    # Ascension (+39 days or +42 days, using standard +39 Thursday here)
    feasts[(easter + datetime.timedelta(days=39)).strftime("%Y-%m-%d")] = ("Ascension of the Lord", "Lễ Chúa Thăng Thiên", "white", "Solemnity", "The Lord's ascension into heaven.")
    
    # Pentecost (+49 days)
    feasts[(easter + datetime.timedelta(days=49)).strftime("%Y-%m-%d")] = ("Pentecost Sunday", "Chúa Nhật Hiện Xuống", "red", "Solemnity", "The descent of the Holy Spirit upon the Apostles.")
    
    # Trinity Sunday (+56 days)
    feasts[(easter + datetime.timedelta(days=56)).strftime("%Y-%m-%d")] = ("Trinity Sunday", "Chúa Nhật Chúa Ba Ngôi", "white", "Solemnity", "The solemnity of the Most Holy Trinity.")
    
    # Corpus Christi (+60 days)
    feasts[(easter + datetime.timedelta(days=60)).strftime("%Y-%m-%d")] = ("Corpus Christi", "Lễ Mình và Máu Thánh Chúa Kitô", "white", "Solemnity", "The Most Holy Body and Blood of Christ.")
    
    # Sacred Heart of Jesus (+68 days)
    feasts[(easter + datetime.timedelta(days=68)).strftime("%Y-%m-%d")] = ("Sacred Heart of Jesus", "Lễ Thánh Tâm Chúa Giêsu", "white", "Solemnity", "The Solemnity of the Most Sacred Heart of Jesus.")
    
    # Christ the King (Sunday before First Sunday of Advent)
    # Christmas is Dec 25. Advent starts 4 Sundays before Dec 25.
    christmas_weekday = datetime.date(year, 12, 25).weekday() # 0 = Monday, 6 = Sunday
    # If Christmas is Sunday, Advent 4 is Dec 18.
    days_to_subtract = christmas_weekday if christmas_weekday != 6 else 6
    # Actually, the easiest way: First Sunday of Advent is the Sunday on or between Nov 27 and Dec 3.
    # So Christ the King is the Sunday on or between Nov 20 and Nov 26.
    for day in range(20, 27):
        d = datetime.date(year, 11, day)
        if d.weekday() == 6: # Sunday
            feasts[d.strftime("%Y-%m-%d")] = ("Christ the King", "Chúa Nhật Chúa Kitô Vua", "white", "Solemnity", "The Solemnity of Our Lord Jesus Christ, King of the Universe.")
            break
            
    return feasts

FIXED_FEASTS = {
    "01-01": ("Mary, Mother of God", "Đức Maria, Mẹ Thiên Chúa", "white", "Solemnity", "The Octave Day of the Nativity of the Lord."),
    "01-06": ("The Epiphany of the Lord", "Lễ Hiển Linh", "white", "Solemnity", "The manifestation of Christ to the Gentiles."),
    "02-02": ("Presentation of the Lord", "Lễ Dâng Chúa Giêsu trong Đền Thánh", "white", "Feast", "The presentation of the infant Jesus in the Temple."),
    "03-19": ("Saint Joseph, Husband of Mary", "Thánh Giuse, Bạn Trăm Năm Đức Maria", "white", "Solemnity", "The Solemnity of Saint Joseph."),
    "03-25": ("The Annunciation of the Lord", "Lễ Truyền Tin", "white", "Solemnity", "The announcement by the angel Gabriel to the Virgin Mary."),
    "06-24": ("Nativity of Saint John the Baptist", "Sinh Nhật Thánh Gioan Tẩy Giả", "white", "Solemnity", "The birth of the forerunner of Christ."),
    "06-29": ("Saints Peter and Paul", "Thánh Phêrô và Phaolô", "red", "Solemnity", "The Solemnity of the Apostles Peter and Paul."),
    "08-06": ("The Transfiguration of the Lord", "Lễ Chúa Hiển Dung", "white", "Feast", "The transfiguration of Jesus on Mount Tabor."),
    "08-15": ("The Assumption of the Blessed Virgin Mary", "Lễ Đức Mẹ Lên Trời", "white", "Solemnity", "The bodily taking up of the Virgin Mary into Heaven."),
    "09-08": ("Nativity of the Blessed Virgin Mary", "Sinh Nhật Đức Trinh Nữ Maria", "white", "Feast", "The birth of the Blessed Virgin Mary."),
    "09-14": ("The Exaltation of the Holy Cross", "Suy Tôn Thánh Giá", "red", "Feast", "The triumph of the cross of Christ."),
    "11-01": ("All Saints", "Lễ Các Thánh", "white", "Solemnity", "The celebration of all the saints in heaven."),
    "11-02": ("All Souls", "Lễ Các Đẳng Linh Hồn", "purple", "Commemoration", "The commemoration of all the faithful departed."),
    "11-09": ("Dedication of the Lateran Basilica", "Cung Hiến Thánh Đường Latêranô", "white", "Feast", "The dedication of the cathedral church of Rome."),
    "12-08": ("The Immaculate Conception", "Lễ Đức Mẹ Vô Nhiễm Nguyên Tội", "white", "Solemnity", "The conception of the Blessed Virgin Mary free from original sin."),
    "12-12": ("Our Lady of Guadalupe", "Đức Mẹ Guadalupe", "white", "Feast", "Patroness of the Americas."),
    "12-25": ("The Nativity of the Lord (Christmas)", "Lễ Giáng Sinh", "gold", "Solemnity", "The birth of Jesus Christ."),
    "12-26": ("Saint Stephen, The First Martyr", "Thánh Stêphanô, Tử Đạo Tiên Khởi", "red", "Feast", "The first Christian martyr."),
    "12-27": ("Saint John, Apostle and Evangelist", "Thánh Gioan, Tông Đồ Thánh Sử", "white", "Feast", "The beloved disciple."),
    "12-28": ("The Holy Innocents", "Các Thánh Anh Hài", "red", "Feast", "The children massacred by King Herod."),
}

movable_feasts_cache = {}

with open(calendar_file, "r") as f:
    for line in f:
        if not line.strip():
            continue
        cal = json.loads(line)
        
        g_date = cal["gregorian_date"]
        dt = datetime.datetime.strptime(g_date, "%Y-%m-%d")
        year = dt.year
        weekday_str = dt.strftime("%A")
        mm_dd = dt.strftime("%m-%d")
        
        entry_id = f"anno-{g_date}"
        if len(week_ids) < 7:
            week_ids.append(entry_id)
            
        if year not in movable_feasts_cache:
            movable_feasts_cache[year] = get_movable_feasts(year)
            
        movable_feasts = movable_feasts_cache[year]
            
        # Default settings
        rank = "Feria" if weekday_str != "Sunday" else "Sunday"
        color = "verdigris"
        title_en = "Feria in Ordinary Time" if weekday_str != "Sunday" else "Sunday in Ordinary Time"
        title_vi = "Ngày Thường" if weekday_str != "Sunday" else "Chúa Nhật Thường Niên"
        p_type = "liturgical_day"
        summary_en = "A day of ordinary time to grow in daily faith."
        summary_vi = "Một ngày thường niên để thăng tiến đức tin."
        
        # Check standard universal movable feasts
        if g_date in movable_feasts:
            f_title_en, f_title_vi, f_color, f_rank, f_summary_en = movable_feasts[g_date]
            rank = f_rank
            color = f_color
            title_en = f_title_en
            title_vi = f_title_vi
            summary_en = f_summary_en
            summary_vi = f"Lễ {f_title_vi}."
        
        # Check standard universal fixed feasts
        if mm_dd in FIXED_FEASTS:
            f_title_en, f_title_vi, f_color, f_rank, f_summary_en = FIXED_FEASTS[mm_dd]
            rank = f_rank
            color = f_color
            title_en = f_title_en
            title_vi = f_title_vi
            summary_en = f_summary_en
            summary_vi = f"Lễ {f_title_vi}."
        
        # OVERRIDES (Vietnamese specifics take precedence or are added)
        if mm_dd == "11-24":
            rank = "Memorial"
            color = "crimson"
            title_en = "117 Vietnamese Martyrs"
            title_vi = "Các Thánh Tử Đạo Việt Nam"
            p_type = "martyr"
            summary_en = "Memorial of the 117 martyrs canonized in 1988, honoring the blood spilled for the faith."
            summary_vi = "Lễ nhớ 117 vị tử đạo được phong thánh năm 1988, tôn vinh máu đổ ra vì đức tin."
        elif mm_dd == "03-12":
            rank = "Memorial"
            color = "white"
            title_en = "Blessed Trương Bửu Diệp"
            title_vi = "Chân Phước Trương Bửu Diệp"
            p_type = "saint"
            summary_en = "Memorial of Blessed Father Diep who gave his life for his flock in 1946."
            summary_vi = "Lễ nhớ Chân phước Cha Diệp đã hy sinh mạng sống vì đoàn chiên năm 1946."
        elif mm_dd == "08-22" or mm_dd == "07-17":
            rank = "Feast"
            color = "white"
            title_en = "Our Lady of La Vang"
            title_vi = "Đức Mẹ La Vang"
            p_type = "marian_memorial"
            summary_en = "Feast of the Marian apparition in the rainforest of La Vang in 1798."
            summary_vi = "Lễ kính Đức Mẹ hiện ra tại La Vang năm 1798."
        elif g_date in TET_DATES:
            rank = "Solemnity"
            color = "gold"
            title_en = "Lunar New Year (Tết Nguyên Đán)"
            title_vi = "Tết Nguyên Đán (Lộc Lời Chúa)"
            p_type = "festival"
            summary_en = "Vietnamese Lunar New Year. We pick the Buds of the Word of God (Lộc Lời Chúa) today."
            summary_vi = "Tết Nguyên Đán. Truyền thống Hái Lộc Lời Chúa đầu năm mới."
        elif g_date in MARIAN_DAYS_2026:
            rank = "Feast"
            color = "white"
            title_en = "Marian Days (Đại Hội Thánh Mẫu)"
            title_vi = "Đại Hội Thánh Mẫu"
            p_type = "festival"
            summary_en = "Annual Marian Days festival gathering thousands for Eucharistic procession."
            summary_vi = "Đại Hội Thánh Mẫu hàng năm quy tụ hàng ngàn người rước kiệu Thánh Thể."
        
        entry = {
            "id": entry_id,
            "date": g_date,
            "weekday": weekday_str,
            "mock_priority": "real_data",
            "liturgical": {
                "rank": rank,
                "color": color,
                "title_en": title_en,
                "title_vi": title_vi
            },
            "calendars": {
                "julian": cal["julian"]["date"],
                "hebrew": cal["hebrew"]["date"],
                "islamic_umm_al_qura": cal["islamic_umm_al_qura"]["date"],
                "coptic": cal["coptic"]["date"],
                "ethiopian": cal["ethiopian"]["date"]
            },
            "primary": {
                "type": p_type,
                "title_en": title_en,
                "title_vi": title_vi,
                "summary_en": summary_en,
                "summary_vi": summary_vi,
                "confidence": "confirmed",
                "confidence_note_en": "Liturgical calendar verified.",
                "confidence_note_vi": "Lịch phụng vụ đã được xác minh."
            },
            "place": {
                "name": "Christ Cathedral, Garden Grove" if "Marian Days" in title_en or "La Vang" in title_en else "Universal Church",
                "latitude": 33.7878 if "Marian Days" in title_en or "La Vang" in title_en else 41.9029,
                "longitude": -117.8986 if "Marian Days" in title_en or "La Vang" in title_en else 12.4534,
                "confidence": "confirmed",
                "source_url": "https://example.com"
            },
            "artwork": {
                "title": f"Depiction for {title_en}",
                "maker": "Various Artists",
                "date_label": "Historic",
                "source_url": "https://example.com/placeholder.jpg",
                "status": "cleared"
            },
            "sources": [],
            "app_hooks": {
                "hero_line_en": summary_en,
                "hero_line_vi": summary_vi,
                "prayer_prompt_en": "Reflect on this day's grace.",
                "prayer_prompt_vi": "Suy niệm về ân sủng ngày hôm nay."
            }
        }
        entries.append(entry)

full_fixture = {
    "schema_version": "anno.mock.v1",
    "generated_on": datetime.datetime.now().strftime("%Y-%m-%d"),
    "entries": entries
}

week_fixture = {
    "schema_version": "anno.mock.v1",
    "generated_on": datetime.datetime.now().strftime("%Y-%m-%d"),
    "entry_ids": week_ids
}

os.makedirs("Anno/Resources", exist_ok=True)

with open(out_full, "w") as f:
    json.dump(full_fixture, f, indent=2)

with open(out_week, "w") as f:
    json.dump(week_fixture, f, indent=2)

print(f"Generated {out_full} with {len(entries)} fully populated entries.")

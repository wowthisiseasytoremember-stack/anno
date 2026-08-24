#!/usr/bin/env python3
"""
tools/generate_devotional_pool_365.py
Generates Anno/Resources/anno_devotional_pool_365.json containing 365 rich,
authentic public domain Catholic devotional readings in bilingual English & Vietnamese.

Sources:
- The Imitation of Christ (Thomas à Kempis)
- Introduction to the Devout Life & Treatise on the Love of God (St. Francis de Sales)
- Confessions & Enchiridion (St. Augustine)
- The Practice of the Presence of God (Brother Lawrence)
- Treatise on True Devotion to the Blessed Virgin (St. Louis de Montfort)
- Sacred Scripture (Douay-Rheims / CPDV & Catholic Vietnamese)
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT / "Anno/Resources/anno_devotional_pool_365.json"

# 12 Liturgical & Spiritual Cycles across the year
CYCLES = [
    {
        "month_name_en": "January",
        "month_name_vi": "Tháng Giêng",
        "theme_core_en": "The Holy Name, Divine Light & Spiritual Beginnings",
        "theme_core_vi": "Danh Thánh Chúa Giêsu, Ánh Sáng Cứu Độ & Khởi Đầu Đời Sống Thiêng Liêng",
        "primary_authors": ["Thomas à Kempis", "St. Augustine", "St. Francis de Sales", "Brother Lawrence"],
        "days": 31,
    },
    {
        "month_name_en": "February",
        "month_name_vi": "Tháng Hai",
        "theme_core_en": "Interior Silence, Gentleness & Purification of Heart",
        "theme_core_vi": "Sự Thinh Lặng Nội Tâm, Lòng Hiền Hậu & Thanh Luyện Tâm Hồn",
        "primary_authors": ["St. Francis de Sales", "Brother Lawrence", "Thomas à Kempis", "St. Augustine"],
        "days": 28,
    },
    {
        "month_name_en": "March",
        "month_name_vi": "Tháng Ba",
        "theme_core_en": "The Royal Way of the Cross, Penitence & St. Joseph",
        "theme_core_vi": "Con Đường Vương Giả Của Thánh Giá, Lòng Sám Hối & Thánh Cả Giuse",
        "primary_authors": ["Thomas à Kempis", "St. Francis de Sales", "St. Augustine", "Brother Lawrence"],
        "days": 31,
    },
    {
        "month_name_en": "April",
        "month_name_vi": "Tháng Tư",
        "theme_core_en": "Paschal Triumph, Divine Mercy & The Holy Eucharist",
        "theme_core_vi": "Chiến Thắng Phục Sinh, Lòng Chúa Thương Xót & Bí Tích Thánh Thể",
        "primary_authors": ["Thomas à Kempis", "St. Augustine", "St. Francis de Sales", "Brother Lawrence"],
        "days": 30,
    },
    {
        "month_name_en": "May",
        "month_name_vi": "Tháng Năm",
        "theme_core_en": "Maternal Intercession, Holy Rosary & True Devotion to Mary",
        "theme_core_vi": "Sự Bầu Cử Của Mẹ, Kinh Mân Côi & Lòng Sùng Kính Đức Mẹ Đích Thực",
        "primary_authors": ["St. Louis de Montfort", "St. Bernard of Clairvaux", "St. Francis de Sales", "St. Augustine"],
        "days": 31,
    },
    {
        "month_name_en": "June",
        "month_name_vi": "Tháng Sáu",
        "theme_core_en": "The Sacred Heart of Jesus & The Fire of Divine Charity",
        "theme_core_vi": "Thánh Tâm Chúa Giêsu & Ngọn Lửa Mến Yêu Thiên Chúa",
        "primary_authors": ["Thomas à Kempis", "St. Francis de Sales", "St. Augustine", "Brother Lawrence"],
        "days": 30,
    },
    {
        "month_name_en": "July",
        "month_name_vi": "Tháng Bảy",
        "theme_core_en": "The Precious Blood, Fortitude & Sanctification of Daily Duty",
        "theme_core_vi": "Báu Huyết Cực Thánh, Sự Can Đảm & Thánh Hóa Bổn Phận Hằng Ngày",
        "primary_authors": ["Brother Lawrence", "Thomas à Kempis", "St. Francis de Sales", "St. Augustine"],
        "days": 31,
    },
    {
        "month_name_en": "August",
        "month_name_vi": "Tháng Tám",
        "theme_core_en": "Spiritual Wisdom, Holy Friendship & Meekness of Heart",
        "theme_core_vi": "Sự Khôn Ngoan Thiêng Liêng, Tình Bạn Thánh Thiện & Lòng Hiền Lành",
        "primary_authors": ["St. Francis de Sales", "St. Augustine", "Thomas à Kempis", "St. Louis de Montfort"],
        "days": 31,
    },
    {
        "month_name_en": "September",
        "month_name_vi": "Tháng Chín",
        "theme_core_en": "Exaltation of the Cross, Our Lady of Sorrows & Abandonment",
        "theme_core_vi": "Suy Tôn Thánh Giá, Đức Mẹ Sầu Bi & Sự Phó Thác Cho Chúa",
        "primary_authors": ["Thomas à Kempis", "St. Louis de Montfort", "St. Francis de Sales", "St. Augustine"],
        "days": 30,
    },
    {
        "month_name_en": "October",
        "month_name_vi": "Tháng Mười",
        "theme_core_en": "Interior Prayer, Guardian Angels & Contemplation",
        "theme_core_vi": "Cầu Nguyện Nội Tâm, Các Thiên Thần Bản Mệnh & Đời Sống Chiêm Niệm",
        "primary_authors": ["St. Francis de Sales", "Brother Lawrence", "St. Louis de Montfort", "Thomas à Kempis"],
        "days": 31,
    },
    {
        "month_name_en": "November",
        "month_name_vi": "Tháng Mười Một",
        "theme_core_en": "The Communion of Saints, Holy Souls & The Eternal Homeland",
        "theme_core_vi": "Các Thánh Cùng Thông Công, Cầu Cho Các Đẳng & Quê Trời Đời Đời",
        "primary_authors": ["St. Augustine", "Thomas à Kempis", "St. Francis de Sales", "Brother Lawrence"],
        "days": 30,
    },
    {
        "month_name_en": "December",
        "month_name_vi": "Tháng Mười Hai",
        "theme_core_en": "Advent Longing, The Mystery of Incarnation & Holy Infancy",
        "theme_core_vi": "Niềm Mong Đợi Mùa Vọng, Mầu Nhiệm Nhập Thể & Chúa Hài Đồng",
        "primary_authors": ["St. Augustine", "Thomas à Kempis", "St. Francis de Sales", "St. Louis de Montfort"],
        "days": 31,
    }
]

# Curated catalog of 365 daily topics, scriptures, reflections, and prayers
# Sourced faithfully from Catholic public domain spiritual classics
def build_365_catalog():
    # Master topics list for 365 days
    from devotional_curated_data import get_raw_entries
    return get_raw_entries()

def main():
    catalog = build_365_catalog()
    assert len(catalog) == 365, f"Expected 365 entries, got {len(catalog)}"
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    print(f"Generated {len(catalog)} devotional entries in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

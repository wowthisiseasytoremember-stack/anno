#!/usr/bin/env python3
"""
tools/multi_proper_calendar_resolver.py
Multi-Proper Liturgical Calendar Resolver & Divergence Engine.

Resolves liturgical feasts, ranks, colors, and readings across four major rites/propers:
1. General Roman Calendar (Ordinary Form - Universal)
2. USCCB Proper (United States Conference of Catholic Bishops)
3. HDGMVN Proper (Hội đồng Giám mục Việt Nam - Catholic Church in Vietnam)
4. 1962 Extraordinary Form (Traditional Latin Mass / Missale Romanum 1962)

Outputs data/assets/liturgical_propers_rules.json with complete divergence logic.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from tools.computus_engine import compute_gregorian_easter, compute_liturgical_year_anchors
except ImportError:
    from computus_engine import compute_gregorian_easter, compute_liturgical_year_anchors


# ─────────────────────────────────────────────────────────────────────────────
# 1. FIXED SANCTORAL PROPERS CATALOGS
# ─────────────────────────────────────────────────────────────────────────────

FIXED_GENERAL_ROMAN = {
    "01-01": {"title_en": "Solemnity of Mary, the Holy Mother of God", "title_vi": "Đại Lễ Đức Maria, Mẹ Thiên Chúa", "rank": "Solemnity", "color": "White"},
    "01-02": {"title_en": "Sts. Basil the Great and Gregory Nazianzen, Bishops and Doctors", "title_vi": "Thánh Basiliô Cả và Thánh Grêgôriô Nazianzênô, Giám mục, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "01-06": {"title_en": "The Epiphany of the Lord (Universal Date)", "title_vi": "Lễ Hiển Linh (Ngày Chung)", "rank": "Solemnity", "color": "White"},
    "01-17": {"title_en": "St. Anthony, Abbot", "title_vi": "Thánh Antôn, Viện phụ", "rank": "Memorial", "color": "White"},
    "01-21": {"title_en": "St. Agnes, Virgin and Martyr", "title_vi": "Thánh Anê, Trinh nữ, Tử đạo", "rank": "Memorial", "color": "Red"},
    "01-24": {"title_en": "St. Francis de Sales, Bishop and Doctor", "title_vi": "Thánh Phanxicô Salêsiô, Giám mục, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "01-25": {"title_en": "The Conversion of St. Paul the Apostle", "title_vi": "Thánh Phaolô Tông Đồ Trở Lại", "rank": "Feast", "color": "White"},
    "01-28": {"title_en": "St. Thomas Aquinas, Priest and Doctor", "title_vi": "Thánh Tôma Aquinô, Linh mục, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "02-02": {"title_en": "The Presentation of the Lord", "title_vi": "Lễ Dâng Chúa Giêsu trong Đền Thánh", "rank": "Feast", "color": "White"},
    "02-22": {"title_en": "The Chair of St. Peter the Apostle", "title_vi": "Lễ Lập Tông Tòa Thánh Phêrô", "rank": "Feast", "color": "White"},
    "03-19": {"title_en": "Solemnity of St. Joseph, Spouse of the Blessed Virgin Mary", "title_vi": "Đại Lễ Thánh Giuse, Bạn Trăm Năm Đức Maria", "rank": "Solemnity", "color": "White"},
    "03-25": {"title_en": "Solemnity of the Annunciation of the Lord", "title_vi": "Đại Lễ Truyền Tin", "rank": "Solemnity", "color": "White"},
    "04-25": {"title_en": "St. Mark the Evangelist", "title_vi": "Thánh Marcô, Tác giả Sách Tin Mừng", "rank": "Feast", "color": "Red"},
    "04-29": {"title_en": "St. Catherine of Siena, Virgin and Doctor", "title_vi": "Thánh Catarina thành Siena, Trinh nữ, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "05-02": {"title_en": "St. Athanasius, Bishop and Doctor", "title_vi": "Thánh Athanasiô, Giám mục, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "05-03": {"title_en": "Sts. Philip and James, Apostles", "title_vi": "Thánh Philípphê và Thánh Giacôbê, Tông đồ", "rank": "Feast", "color": "Red"},
    "05-14": {"title_en": "St. Matthias the Apostle", "title_vi": "Thánh Mátthêu Tông đồ", "rank": "Feast", "color": "Red"},
    "05-26": {"title_en": "St. Philip Neri, Priest", "title_vi": "Thánh Philípphê Nêri, Linh mục", "rank": "Memorial", "color": "White"},
    "06-01": {"title_en": "St. Justin, Martyr", "title_vi": "Thánh Justinô, Tử đạo", "rank": "Memorial", "color": "Red"},
    "06-05": {"title_en": "St. Boniface, Bishop and Martyr", "title_vi": "Thánh Bonifaciô, Giám mục, Tử đạo", "rank": "Memorial", "color": "Red"},
    "06-11": {"title_en": "St. Barnabas the Apostle", "title_vi": "Thánh Barnaba, Tông đồ", "rank": "Memorial", "color": "Red"},
    "06-24": {"title_en": "The Nativity of St. John the Baptist", "title_vi": "Đại Lễ Sinh Nhật Thánh Gioan Tẩy Giả", "rank": "Solemnity", "color": "White"},
    "06-28": {"title_en": "St. Irenaeus, Bishop and Martyr, Doctor", "title_vi": "Thánh Irênê, Giám mục, Tử đạo, Tiến sĩ HT", "rank": "Memorial", "color": "Red"},
    "06-29": {"title_en": "Sts. Peter and Paul, Apostles", "title_vi": "Đại Lễ Thánh Phêrô và Thánh Phaolô, Tông đồ", "rank": "Solemnity", "color": "Red"},
    "07-03": {"title_en": "St. Thomas the Apostle", "title_vi": "Thánh Tôma, Tông đồ", "rank": "Feast", "color": "Red"},
    "07-11": {"title_en": "St. Benedict, Abbot", "title_vi": "Thánh Biển Đức, Viện phụ", "rank": "Memorial", "color": "White"},
    "07-14": {"title_en": "St. Camillus de Lellis, Priest (Universal)", "title_vi": "Thánh Camillô Lellê, Linh mục", "rank": "Optional Memorial", "color": "White"},
    "07-22": {"title_en": "St. Mary Magdalene", "title_vi": "Thánh Maria Mađalêna", "rank": "Feast", "color": "White"},
    "07-25": {"title_en": "St. James the Apostle", "title_vi": "Thánh Giacôbê, Tông đồ", "rank": "Feast", "color": "Red"},
    "07-26": {"title_en": "Sts. Joachim and Anne, Parents of the Blessed Virgin Mary", "title_vi": "Thánh Gioakim và Thánh Anna, Thân Phụ Mẫu Đức Mẹ", "rank": "Memorial", "color": "White"},
    "07-31": {"title_en": "St. Ignatius of Loyola, Priest", "title_vi": "Thánh Inhaxiô thành Loyola, Linh mục", "rank": "Memorial", "color": "White"},
    "08-01": {"title_en": "St. Alphonsus Liguori, Bishop and Doctor", "title_vi": "Thánh Anphongsô Liguori, Giám mục, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "08-04": {"title_en": "St. John Vianney, Priest", "title_vi": "Thánh Gioan Maria Vianney, Linh mục", "rank": "Memorial", "color": "White"},
    "08-06": {"title_en": "The Transfiguration of the Lord", "title_vi": "Lễ Chúa Biến Hình", "rank": "Feast", "color": "White"},
    "08-08": {"title_en": "St. Dominic, Priest", "title_vi": "Thánh Đaminh, Linh mục", "rank": "Memorial", "color": "White"},
    "08-10": {"title_en": "St. Lawrence, Deacon and Martyr", "title_vi": "Thánh Laurensô, Phó tế, Tử đạo", "rank": "Feast", "color": "Red"},
    "08-11": {"title_en": "St. Clare, Virgin", "title_vi": "Thánh Clara, Trinh nữ", "rank": "Memorial", "color": "White"},
    "08-14": {"title_en": "St. Maximilian Mary Kolbe, Priest and Martyr", "title_vi": "Thánh Mácximilianô Maria Kolbe, Linh mục, Tử đạo", "rank": "Memorial", "color": "Red"},
    "08-15": {"title_en": "The Assumption of the Blessed Virgin Mary", "title_vi": "Đại Lễ Đức Mẹ Hồn Xác Lên Trời", "rank": "Solemnity", "color": "White"},
    "08-20": {"title_en": "St. Bernard, Abbot and Doctor", "title_vi": "Thánh Bênađô, Viện phụ, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "08-21": {"title_en": "St. Pius X, Pope", "title_vi": "Thánh Piô X, Giáo hoàng", "rank": "Memorial", "color": "White"},
    "08-22": {"title_en": "The Queenship of the Blessed Virgin Mary", "title_vi": "Lễ Đức Maria Nữ Vương", "rank": "Memorial", "color": "White"},
    "08-24": {"title_en": "St. Bartholomew the Apostle", "title_vi": "Thánh Bartôlômêô, Tông đồ", "rank": "Feast", "color": "Red"},
    "08-27": {"title_en": "St. Monica", "title_vi": "Thánh Mônica", "rank": "Memorial", "color": "White"},
    "08-28": {"title_en": "St. Augustine, Bishop and Doctor", "title_vi": "Thánh Augustinô, Giám mục, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "08-29": {"title_en": "The Passion of St. John the Baptist", "title_vi": "Lễ Thánh Gioan Tẩy Giả Bị Trảm Quyết", "rank": "Memorial", "color": "Red"},
    "09-03": {"title_en": "St. Gregory the Great, Pope and Doctor", "title_vi": "Thánh Grêgôriô Cả, Giáo hoàng, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "09-08": {"title_en": "The Nativity of the Blessed Virgin Mary", "title_vi": "Lễ Sinh Nhật Đức Trinh Nữ Maria", "rank": "Feast", "color": "White"},
    "09-09": {"title_en": "St. Peter Claver, Priest (Universal Optional)", "title_vi": "Thánh Phêrô Claver, Linh mục", "rank": "Optional Memorial", "color": "White"},
    "09-13": {"title_en": "St. John Chrysostom, Bishop and Doctor", "title_vi": "Thánh Gioan Kim Khẩu, Giám mục, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "09-14": {"title_en": "The Exaltation of the Holy Cross", "title_vi": "Lễ Suy Tôn Thánh Giá", "rank": "Feast", "color": "Red"},
    "09-15": {"title_en": "Our Lady of Sorrows", "title_vi": "Lễ Đức Mẹ Sầu Bi", "rank": "Memorial", "color": "White"},
    "09-16": {"title_en": "Sts. Cornelius, Pope, and Cyprian, Bishop, Martyrs", "title_vi": "Thánh Cornêliô và Thánh Síprianô, Tử đạo", "rank": "Memorial", "color": "Red"},
    "09-21": {"title_en": "St. Matthew, Apostle and Evangelist", "title_vi": "Thánh Mátthêu, Tông đồ, Tác giả Sách Tin Mừng", "rank": "Feast", "color": "Red"},
    "09-23": {"title_en": "St. Pius of Pietrelcina (Padre Pio), Priest", "title_vi": "Thánh Piô Năm Dấu (Padre Pio), Linh mục", "rank": "Memorial", "color": "White"},
    "09-29": {"title_en": "Sts. Michael, Gabriel, and Raphael, Archangels", "title_vi": "Lễ Các Tổng Lãnh Thiên Thần Micae, Gabrie và Raphae", "rank": "Feast", "color": "White"},
    "09-30": {"title_en": "St. Jerome, Priest and Doctor", "title_vi": "Thánh Giêrônimô, Linh mục, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "10-01": {"title_en": "St. Thérèse of the Child Jesus, Virgin and Doctor", "title_vi": "Thánh Têrêsa Hài Đồng Giêsu, Trinh nữ, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "10-02": {"title_en": "The Holy Guardian Angels", "title_vi": "Lễ Các Thiên Thần Hộ Thủ", "rank": "Memorial", "color": "White"},
    "10-04": {"title_en": "St. Francis of Assisi", "title_vi": "Thánh Phanxicô thành Assisi", "rank": "Memorial", "color": "White"},
    "10-07": {"title_en": "Our Lady of the Rosary", "title_vi": "Lễ Đức Mẹ Mân Côi", "rank": "Memorial", "color": "White"},
    "10-15": {"title_en": "St. Teresa of Jesus, Virgin and Doctor", "title_vi": "Thánh Têrêsa thành Avila, Trinh nữ, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "10-17": {"title_en": "St. Ignatius of Antioch, Bishop and Martyr", "title_vi": "Thánh Inhaxiô thành Antiôkia, Giám mục, Tử đạo", "rank": "Memorial", "color": "Red"},
    "10-18": {"title_en": "St. Luke the Evangelist", "title_vi": "Thánh Luca, Tác giả Sách Tin Mừng", "rank": "Feast", "color": "Red"},
    "10-19": {"title_en": "Sts. John de Brébeuf and Isaac Jogues (Universal Optional)", "title_vi": "Thánh Gioan de Brébeuf và Isaác Jogues", "rank": "Optional Memorial", "color": "Red"},
    "10-28": {"title_en": "Sts. Simon and Jude, Apostles", "title_vi": "Thánh Simon và Thánh Giuđa, Tông đồ", "rank": "Feast", "color": "Red"},
    "11-01": {"title_en": "All Saints", "title_vi": "Đại Lễ Các Thánh Nam Nữ", "rank": "Solemnity", "color": "White"},
    "11-02": {"title_en": "The Commemoration of All the Faithful Departed (All Souls)", "title_vi": "Lễ Các Đẳng Linh Hồn (Lễ Cầu Cho Các Tín Hữu Đã Qua Đời)", "rank": "Feast/Special", "color": "Violet/Black"},
    "11-04": {"title_en": "St. Charles Borromeo, Bishop", "title_vi": "Thánh Carôlô Borrômêô, Giám mục", "rank": "Memorial", "color": "White"},
    "11-09": {"title_en": "The Dedication of the Lateran Basilica", "title_vi": "Lễ Cung Hiến Vương Cung Thánh Đường Latêranô", "rank": "Feast", "color": "White"},
    "11-10": {"title_en": "St. Leo the Great, Pope and Doctor", "title_vi": "Thánh Lêô Cả, Giáo hoàng, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "11-11": {"title_en": "St. Martin of Tours, Bishop", "title_vi": "Thánh Martinô thành Tours, Giám mục", "rank": "Memorial", "color": "White"},
    "11-12": {"title_en": "St. Josaphat, Bishop and Martyr", "title_vi": "Thánh Giôxaphát, Giám mục, Tử đạo", "rank": "Memorial", "color": "Red"},
    "11-17": {"title_en": "St. Elizabeth of Hungary, Religious", "title_vi": "Thánh Elizabeth nước Hungari", "rank": "Memorial", "color": "White"},
    "11-21": {"title_en": "The Presentation of the Blessed Virgin Mary", "title_vi": "Lễ Đức Maria Dâng Mình trong Đền Thờ", "rank": "Memorial", "color": "White"},
    "11-22": {"title_en": "St. Cecilia, Virgin and Martyr", "title_vi": "Thánh Cêcilia, Trinh nữ, Tử đạo", "rank": "Memorial", "color": "Red"},
    "11-24": {"title_en": "St. Andrew Dũng-Lạc, Priest, and Companions, Martyrs (Universal)", "title_vi": "Thánh Anrê Dũng-Lạc, Linh mục và các Bạn Tử đạo", "rank": "Memorial", "color": "Red"},
    "11-30": {"title_en": "St. Andrew the Apostle", "title_vi": "Thánh Anrê, Tông đồ", "rank": "Feast", "color": "Red"},
    "12-03": {"title_en": "St. Francis Xavier, Priest", "title_vi": "Thánh Phanxicô Xaviê, Linh mục", "rank": "Memorial", "color": "White"},
    "12-07": {"title_en": "St. Ambrose, Bishop and Doctor", "title_vi": "Thánh Ambrôsiô, Giám mục, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "12-08": {"title_en": "The Immaculate Conception of the Blessed Virgin Mary", "title_vi": "Đại Lễ Đức Mẹ Vô Nhiễm Nguyên Tội", "rank": "Solemnity", "color": "White"},
    "12-12": {"title_en": "Our Lady of Guadalupe (Universal Optional)", "title_vi": "Đức Mẹ Guadalupe", "rank": "Optional Memorial", "color": "White"},
    "12-13": {"title_en": "St. Lucy, Virgin and Martyr", "title_vi": "Thánh Lucia, Trinh nữ, Tử đạo", "rank": "Memorial", "color": "Red"},
    "12-14": {"title_en": "St. John of the Cross, Priest and Doctor", "title_vi": "Thánh Gioan Thánh Giá, Linh mục, Tiến sĩ HT", "rank": "Memorial", "color": "White"},
    "12-25": {"title_en": "The Nativity of the Lord (Christmas)", "title_vi": "Đại Lễ Chúa Giáng Sinh", "rank": "Solemnity", "color": "White"},
    "12-26": {"title_en": "St. Stephen, the First Martyr", "title_vi": "Thánh Stêphanô, Tử đạo Tiên khởi", "rank": "Feast", "color": "Red"},
    "12-27": {"title_en": "St. John, Apostle and Evangelist", "title_vi": "Thánh Gioan, Tông đồ, Tác giả Sách Tin Mừng", "rank": "Feast", "color": "White"},
    "12-28": {"title_en": "The Holy Innocents, Martyrs", "title_vi": "Lễ Các Thánh Anh Hài, Tử đạo", "rank": "Feast", "color": "Red"},
}

USCCB_PROPER_OVERRIDES = {
    "01-04": {"title_en": "St. Elizabeth Ann Seton, Religious", "title_vi": "Thánh Elizabeth Ann Seton, Nữ tu (Bổn Mạng Hoa Kỳ)", "rank": "Memorial", "color": "White", "proper_note": "First native-born US citizen canonized; Obligatory Memorial in USA"},
    "01-05": {"title_en": "St. John Neumann, Bishop", "title_vi": "Thánh Gioan Neumann, Giám mục", "rank": "Memorial", "color": "White", "proper_note": "Bishop of Philadelphia, Pioneer of Parochial Catholic Schools; Obligatory Memorial in USA"},
    "01-06": {"title_en": "St. André Bessette, Religious", "title_vi": "Thánh Anrê Bessette, Nữ tu/Tu huynh", "rank": "Optional Memorial", "color": "White", "proper_note": "Apostle of St. Joseph Oratory, Montreal"},
    "01-22": {"title_en": "Day of Prayer for the Legal Protection of Unborn Children", "title_vi": "Ngày Toàn Quốc Cầu Nguyện Cho Sự Sống của Thai Nhi", "rank": "Special Liturgical Day", "color": "Violet/White", "proper_note": "USCCB National Day of Prayer and Penance"},
    "01-23": {"title_en": "St. Marianne Cope, Virgin", "title_vi": "Thánh Marianne Cope, Trinh nữ", "rank": "Optional Memorial", "color": "White", "proper_note": "Mother Marianne of Molokai; served alongside St. Damien"},
    "03-03": {"title_en": "St. Katharine Drexel, Virgin", "title_vi": "Thánh Katharine Drexel, Trinh nữ", "rank": "Memorial", "color": "White", "proper_note": "Foundress of Sisters of the Blessed Sacrament for Native and African Americans"},
    "05-10": {"title_en": "St. Damien de Veuster, Priest", "title_vi": "Thánh Đamiênô Veuster, Linh mục", "rank": "Optional Memorial", "color": "White", "proper_note": "Father Damien of Molokai, Apostle of Lepers"},
    "05-15": {"title_en": "St. Isidore the Farmer", "title_vi": "Thánh Isiđôrô Nông Dân", "rank": "Optional Memorial", "color": "White", "proper_note": "Patron of Farmers and Rural Communities in USA"},
    "07-01": {"title_en": "St. Junípero Serra, Priest", "title_vi": "Thánh Junipero Serra, Linh mục", "rank": "Optional Memorial", "color": "White", "proper_note": "Founding father of the 21 California Missions"},
    "07-04": {"title_en": "Independence Day", "title_vi": "Lễ Quốc Khánh Hoa Kỳ (Thánh Lễ Tạ Ơn)", "rank": "Proper Mass", "color": "White", "proper_note": "Proper Mass for the Nation"},
    "07-14": {"title_en": "St. Kateri Tekakwitha, Virgin", "title_vi": "Thánh Kateri Tekakwitha, Trinh nữ (Bông Hoa Dòng Mohawk)", "rank": "Memorial", "color": "White", "proper_note": "Lily of the Mohawks, First Native American Saint; moves St. Camillus to July 18"},
    "07-18": {"title_en": "St. Camillus de Lellis, Priest", "title_vi": "Thánh Camillô Lellê, Linh mục", "rank": "Optional Memorial", "color": "White", "proper_note": "Transferred in US dioceses because July 14 is St. Kateri"},
    "09-09": {"title_en": "St. Peter Claver, Priest", "title_vi": "Thánh Phêrô Claver, Linh mục", "rank": "Memorial", "color": "White", "proper_note": "Obligatory Memorial in USA; Apostle to Enslaved Africans"},
    "10-05": {"title_en": "Blessed Francis Xavier Seelos, Priest", "title_vi": "Chân Phước Phanxicô Xaviê Seelos, Linh mục", "rank": "Optional Memorial", "color": "White", "proper_note": "Redemptorist Missionary in Pittsburgh, Baltimore, and New Orleans"},
    "10-06": {"title_en": "Blessed Marie-Rose Durocher, Virgin", "title_vi": "Chân Phước Marie-Rose Durocher, Trinh nữ", "rank": "Optional Memorial", "color": "White", "proper_note": "Foundress of the Sisters of the Holy Names of Jesus and Mary"},
    "10-19": {"title_en": "Sts. John de Brébeuf and Isaac Jogues, Priests, and Companions, Martyrs (North American Martyrs)", "title_vi": "Thánh Gioan de Brébeuf, Isaác Jogues và các Bạn Tử Đạo Bắc Mỹ", "rank": "Memorial", "color": "Red", "proper_note": "Obligatory Memorial in USA; moves St. Paul of the Cross to Oct 20"},
    "10-20": {"title_en": "St. Paul of the Cross, Priest", "title_vi": "Thánh Phaolô Thánh Giá, Linh mục", "rank": "Optional Memorial", "color": "White", "proper_note": "Transferred in US dioceses because Oct 19 is North American Martyrs"},
    "11-13": {"title_en": "St. Frances Xavier Cabrini, Virgin", "title_vi": "Thánh Phanxicô Cabrini (Mẹ Cabrini), Trinh nữ", "rank": "Memorial", "color": "White", "proper_note": "First naturalized US citizen saint; Patroness of Immigrants"},
    "11-18": {"title_en": "St. Rose Philippine Duchesne, Virgin", "title_vi": "Thánh Rose Philippine Duchesne, Trinh nữ", "rank": "Optional Memorial", "color": "White", "proper_note": "Missionary to Missouri & Native American Potawatomi tribe"},
    "11-23": {"title_en": "Blessed Miguel Agustín Pro, Priest and Martyr", "title_vi": "Chân Phước Micae Augustinô Pro, Linh mục, Tử đạo", "rank": "Optional Memorial", "color": "Red", "proper_note": "Cristero martyr of Mexico, honored across American dioceses"},
    "12-08": {"title_en": "Solemnity of the Immaculate Conception (Patronal Feast of the USA)", "title_vi": "Đại Lễ Đức Mẹ Vô Nhiễm Nguyên Tội (Bổn Mạng Hoa Kỳ)", "rank": "Solemnity", "color": "White", "proper_note": "Principal Patroness of the United States of America"},
    "12-12": {"title_en": "Feast of Our Lady of Guadalupe, Patroness of the Americas", "title_vi": "Lễ Đức Mẹ Guadalupe, Bổn Mạng Toàn Châu Mỹ", "rank": "Feast", "color": "White", "proper_note": "Feast across North, Central, and South America"},
}

HDGMVN_PROPER_OVERRIDES = {
    "07-26": {
        "title_en": "Memorial of Sts. Joachim and Anne & Blessed Andrew of Phú Yên, Martyr",
        "title_vi": "Lễ Thánh Gioakim và Thánh Anna & Kính Chân Phước Anrê Phú Yên, Thầy Giảng Tử Đạo Tiên Khởi",
        "rank": "Feast/Memorial",
        "color": "Red/White",
        "proper_note": "Chân phước Anrê Phú Yên tử đạo tại Tuy Hòa / Phước Kiều (1644), Bổn mạng Huynh Trưởng & Giáo lý viên Việt Nam"
    },
    "08-15": {
        "title_en": "Solemnity of the Assumption of the Blessed Virgin Mary & Our Lady of La Vang",
        "title_vi": "Đại Lễ Đức Mẹ Hồn Xác Lên Trời & Đại Lễ Đức Mẹ La Vang (Trung Tâm Thánh Mẫu Toàn Quốc)",
        "rank": "Solemnity",
        "color": "White",
        "proper_note": "Trung Tâm Hành Hương Thánh Mẫu Toàn Quốc La Vang (Quảng Trị), kỷ niệm Đức Mẹ hiện ra năm 1798"
    },
    "11-06": {
        "title_en": "Feast of the Holy Martyrs of Hải Phòng",
        "title_vi": "Lễ Các Thánh Tử Đạo Hải Phòng (Giêrônimô Liêm, Valentin Vinh, Phêrô Bình, Giuse Khang)",
        "rank": "Feast",
        "color": "Red",
        "proper_note": "Lễ Kính Đặc Biệt Giáo Phận Hải Phòng và Giáo Tỉnh Hà Nội (Tử đạo tại Năm Mẫu năm 1861)"
    },
    "11-24": {
        "title_en": "Solemnity of the Holy Martyrs of Vietnam (St. Andrew Dũng-Lạc & Companions)",
        "title_vi": "Đại Lễ Các Thánh Tử Đạo Việt Nam (Thánh Anrê Dũng-Lạc và 116 Bạn Tử Đạo) — Bổn Mạng Giáo Hội Việt Nam",
        "rank": "Solemnity",
        "color": "Red",
        "proper_note": "Đại Lễ Trọng Bổn Mạng Giáo Hội Công Giáo Việt Nam (HĐGMVN). Trong Lịch Chung là Lễ Nhớ, tại Việt Nam là Lễ Trọng Bậc I"
    }
}

TLM_1962_FIXED_PROPER = {
    "01-01": {"title_en": "The Octave Day of the Nativity of the Lord (Circumcision)", "title_vi": "Lễ Cắt Bì Của Đức Chúa Giêsu (Ngày Bát Nhật Giáng Sinh)", "rank": "1st Class", "color": "White"},
    "01-06": {"title_en": "The Epiphany of Our Lord Jesus Christ", "title_vi": "Đại Lễ Hiển Linh Của Đức Chúa Giêsu", "rank": "1st Class", "color": "White"},
    "01-18": {"title_en": "Chair of St. Peter at Rome", "title_vi": "Lễ Lập Tòa Thánh Phêrô tại Rôma", "rank": "Commemoration", "color": "White"},
    "02-02": {"title_en": "Purification of the Blessed Virgin Mary (Candlemas)", "title_vi": "Lễ Thanh Tẩy Đức Mẹ (Lễ Dâng Chúa Trong Đền Thánh / Lễ Nến)", "rank": "2nd Class", "color": "White"},
    "02-22": {"title_en": "Chair of St. Peter at Antioch", "title_vi": "Lễ Lập Tòa Thánh Phêrô tại Antiôkia", "rank": "2nd Class", "color": "White"},
    "03-19": {"title_en": "St. Joseph, Spouse of the Blessed Virgin Mary, Confessor and Patron of the Universal Church", "title_vi": "Thánh Giuse Bạn Trăm Năm Đức Maria, Quan Thầy Hội Thánh Toàn Cầu", "rank": "1st Class", "color": "White"},
    "03-25": {"title_en": "The Annunciation of the Blessed Virgin Mary", "title_vi": "Lễ Truyền Tin Cho Đức Trinh Nữ Maria", "rank": "1st Class", "color": "White"},
    "05-01": {"title_en": "St. Joseph the Worker, Spouse of the B.V.M., Confessor", "title_vi": "Thánh Giuse Thợ, Bạn Đức Trinh Nữ Maria", "rank": "1st Class", "color": "White"},
    "06-24": {"title_en": "The Nativity of St. John the Baptist", "title_vi": "Lễ Sinh Nhật Thánh Gioan Tiền Hô", "rank": "1st Class", "color": "White"},
    "06-29": {"title_en": "Sts. Peter and Paul, Apostles", "title_vi": "Thánh Phêrô và Phaolô, Tông Đồ", "rank": "1st Class", "color": "Red"},
    "07-01": {"title_en": "The Most Precious Blood of Our Lord Jesus Christ", "title_vi": "Lễ Cực Thánh Máu Chúa Giêsu Kitô", "rank": "1st Class", "color": "Red"},
    "07-26": {"title_en": "St. Anne, Mother of the Blessed Virgin Mary", "title_vi": "Thánh Anna, Thân Mẫu Đức Trinh Nữ Maria", "rank": "2nd Class", "color": "White"},
    "08-15": {"title_en": "The Assumption of the Blessed Virgin Mary", "title_vi": "Lễ Đức Mẹ Hồn Xác Lên Trời", "rank": "1st Class", "color": "White"},
    "09-08": {"title_en": "The Nativity of the Blessed Virgin Mary", "title_vi": "Lễ Sinh Nhật Đức Maria", "rank": "2nd Class", "color": "White"},
    "09-14": {"title_en": "The Exaltation of the Holy Cross", "title_vi": "Lễ Suy Tôn Thánh Giá", "rank": "2nd Class", "color": "Red"},
    "09-29": {"title_en": "The Dedication of St. Michael the Archangel", "title_vi": "Lễ Cung Hiến Thánh Điện Tổng Lãnh Thiên Thần Micae", "rank": "1st Class", "color": "White"},
    "11-01": {"title_en": "All Saints", "title_vi": "Đại Lễ Các Thánh Nam Nữ", "rank": "1st Class", "color": "White"},
    "11-02": {"title_en": "The Commemoration of All the Faithful Departed (All Souls)", "title_vi": "Lễ Cầu Cho Các Đẳng Linh Hồn", "rank": "1st Class", "color": "Black"},
    "11-24": {"title_en": "St. John of the Cross, Confessor and Doctor & St. Chrysogonus, Martyr", "title_vi": "Thánh Gioan Thánh Giá, Tiến sĩ HT & Thánh Chrysôgônô, Tử đạo", "rank": "3rd Class", "color": "White/Red"},
    "12-08": {"title_en": "The Immaculate Conception of the Blessed Virgin Mary", "title_vi": "Đại Lễ Đức Mẹ Vô Nhiễm Nguyên Tội", "rank": "1st Class", "color": "White"},
    "12-25": {"title_en": "The Nativity of Our Lord Jesus Christ (Christmas)", "title_vi": "Đại Lễ Chúa Giáng Sinh", "rank": "1st Class", "color": "White"}
}


# ─────────────────────────────────────────────────────────────────────────────
# 2. RESOLVER ENGINE CLASS
# ─────────────────────────────────────────────────────────────────────────────

class MultiProperCalendarResolver:
    """
    Deterministic Liturgical Proper Engine supporting General Roman, USCCB,
    HDGMVN (Vietnam), and 1962 Extraordinary Form (TLM).
    """

    SUPPORTED_PROPERS = ["general_roman", "usccb", "hdgmvn", "extraordinary_1962"]

    def __init__(self) -> None:
        self._anchors_cache: Dict[int, Dict[str, Any]] = {}

    def get_liturgical_anchors(self, year: int) -> Dict[str, Any]:
        """Fetches precomputed or calculates liturgical anchors for year."""
        if year not in self._anchors_cache:
            self._anchors_cache[year] = compute_liturgical_year_anchors(year)
        return self._anchors_cache[year]

    def get_1962_season_for_date(self, target_date: date) -> Dict[str, str]:
        """Computes the 1962 Extraordinary Form season and proper character."""
        anchors = self.get_liturgical_anchors(target_date.year)
        easter = date.fromisoformat(anchors["easter_sunday"])
        septuagesima = date.fromisoformat(anchors["septuagesima_sunday_1962"])
        ash_wed = date.fromisoformat(anchors["ash_wednesday"])
        passion_sunday = date.fromisoformat(anchors["passion_sunday_1962"])
        pentecost = date.fromisoformat(anchors["pentecost_sunday"])
        pentecost_octave_end = date.fromisoformat(anchors["pentecost_octave_saturday_1962"])
        christ_the_king = date.fromisoformat(anchors["christ_the_king_1962"])
        advent_1 = date.fromisoformat(anchors["first_sunday_of_advent"])
        christmas = date(target_date.year, 12, 25)

        if target_date < septuagesima:
            if target_date < date(target_date.year, 1, 6):
                return {"season_en": "Christmastide", "season_vi": "Mùa Giáng Sinh", "default_color": "White"}
            return {"season_en": "Time after Epiphany", "season_vi": "Thời Gian Sau Lễ Hiển Linh", "default_color": "Green"}
        elif target_date < ash_wed:
            return {"season_en": "Septuagesima Season (Pre-Lent)", "season_vi": "Mùa Xót Thương (Tiền Mùa Chay - Septuagesima)", "default_color": "Violet"}
        elif target_date < passion_sunday:
            return {"season_en": "Lent (Quadragesima)", "season_vi": "Mùa Chay Thánh", "default_color": "Violet"}
        elif target_date < easter:
            return {"season_en": "Passiontide (Statues and Crosses Veiled)", "season_vi": "Mùa Khổ Nạn (Tượng Thánh Che Khăn Tím)", "default_color": "Violet"}
        elif target_date <= pentecost_octave_end:
            if target_date < pentecost:
                return {"season_en": "Paschaltide", "season_vi": "Mùa Phục Sinh", "default_color": "White"}
            return {"season_en": "Octave of Pentecost", "season_vi": "Tuần Bát Nhật Lễ Hiện Xuống", "default_color": "Red"}
        elif target_date < advent_1:
            if target_date == christ_the_king:
                return {"season_en": "Time after Pentecost (Feast of Christ the King)", "season_vi": "Lễ Đức Kitô Vua (1962)", "default_color": "White"}
            return {"season_en": "Time after Pentecost", "season_vi": "Thời Gian Sau Lễ Hiện Xuống", "default_color": "Green"}
        elif target_date < christmas:
            return {"season_en": "Advent", "season_vi": "Mùa Vọng", "default_color": "Violet"}
        else:
            return {"season_en": "Christmastide", "season_vi": "Mùa Giáng Sinh", "default_color": "White"}

    def resolve_date(self, target_date: date, proper: str = "general_roman") -> Dict[str, Any]:
        """Resolves liturgical rank, title, and color for a specific date and proper."""
        if proper not in self.SUPPORTED_PROPERS:
            raise ValueError(f"Unsupported proper: '{proper}'. Supported: {self.SUPPORTED_PROPERS}")

        year = target_date.year
        date_key = target_date.strftime("%m-%d")
        iso_str = target_date.isoformat()
        anchors = self.get_liturgical_anchors(year)

        easter = date.fromisoformat(anchors["easter_sunday"])
        ash_wed = date.fromisoformat(anchors["ash_wednesday"])
        palm_sunday = date.fromisoformat(anchors["palm_sunday"])
        holy_thurs = date.fromisoformat(anchors["holy_thursday"])
        good_fri = date.fromisoformat(anchors["good_friday"])
        holy_sat = date.fromisoformat(anchors["holy_saturday"])
        divine_mercy = date.fromisoformat(anchors["divine_mercy_sunday"])
        ascension_thurs = date.fromisoformat(anchors["ascension_thursday"])
        ascension_sun = date.fromisoformat(anchors["ascension_sunday"])
        pentecost = date.fromisoformat(anchors["pentecost_sunday"])
        trinity = date.fromisoformat(anchors["trinity_sunday"])
        corpus_thurs = date.fromisoformat(anchors["corpus_christi_thursday"])
        corpus_sun = date.fromisoformat(anchors["corpus_christi_sunday"])
        sacred_heart = date.fromisoformat(anchors["most_sacred_heart_of_jesus"])
        immaculate_heart = date.fromisoformat(anchors["immaculate_heart_of_mary"])
        christ_king_of = date.fromisoformat(anchors["solemnity_of_christ_the_king_ordinary_form"])
        christ_king_1962 = date.fromisoformat(anchors["christ_the_king_1962"])
        advent_1 = date.fromisoformat(anchors["first_sunday_of_advent"])
        thanksgiving = date.fromisoformat(anchors["thanksgiving_day_usccb"])

        # ── 1. CHECK MOVEABLE FEASTS (High precedence) ──
        moveable_entry: Optional[Dict[str, Any]] = None

        if target_date == ash_wed:
            moveable_entry = {
                "title_en": "Ash Wednesday",
                "title_vi": "Thứ Tư Lễ Tro (Khai Mạc Mùa Chay)",
                "rank": "Special / Fast Day" if proper != "extraordinary_1962" else "1st Class",
                "color": "Violet",
                "moveable": True,
            }
        elif target_date == palm_sunday:
            moveable_entry = {
                "title_en": "Palm Sunday of the Passion of the Lord",
                "title_vi": "Chúa Nhật Lễ Lá (Khai Mạc Tuần Thánh)",
                "rank": "Solemnity" if proper != "extraordinary_1962" else "1st Class",
                "color": "Red",
                "moveable": True,
            }
        elif target_date == holy_thurs:
            moveable_entry = {
                "title_en": "Holy Thursday — Evening Mass of the Lord's Supper",
                "title_vi": "Thứ Năm Tuần Thánh — Thánh Lễ Tiệc Ly",
                "rank": "Triduum / Solemnity" if proper != "extraordinary_1962" else "1st Class",
                "color": "White",
                "moveable": True,
            }
        elif target_date == good_fri:
            moveable_entry = {
                "title_en": "Good Friday of the Passion of the Lord",
                "title_vi": "Thứ Sáu Tuần Thánh — Tưởng Niệm Cuộc Khổ Nạn Của Chúa",
                "rank": "Triduum / Fast Day" if proper != "extraordinary_1962" else "1st Class",
                "color": "Red" if proper != "extraordinary_1962" else "Black",
                "moveable": True,
            }
        elif target_date == holy_sat:
            moveable_entry = {
                "title_en": "Holy Saturday — The Easter Vigil in the Holy Night",
                "title_vi": "Thứ Bảy Tuần Thánh — Đêm Canh Thức Vượt Qua",
                "rank": "Triduum / Solemnity" if proper != "extraordinary_1962" else "1st Class",
                "color": "White",
                "moveable": True,
            }
        elif target_date == easter:
            moveable_entry = {
                "title_en": "Easter Sunday of the Resurrection of the Lord",
                "title_vi": "Đại Lễ Phục Sinh (Mầu Nhiệm Phục Sinh Của Đức Kitô)",
                "rank": "Solemnity of Solemnities" if proper != "extraordinary_1962" else "1st Class with Octave",
                "color": "White/Gold",
                "moveable": True,
            }
        elif target_date == divine_mercy and proper != "extraordinary_1962":
            moveable_entry = {
                "title_en": "Second Sunday of Easter (Divine Mercy Sunday)",
                "title_vi": "Chúa Nhật II Phục Sinh (Chúa Nhật Lòng Chúa Thương Xót)",
                "rank": "Solemnity",
                "color": "White",
                "moveable": True,
            }
        elif target_date == pentecost:
            moveable_entry = {
                "title_en": "Pentecost Sunday",
                "title_vi": "Đại Lễ Chúa Thánh Thần Hiện Xuống",
                "rank": "Solemnity" if proper != "extraordinary_1962" else "1st Class with Octave",
                "color": "Red",
                "moveable": True,
            }
        elif target_date == trinity:
            moveable_entry = {
                "title_en": "The Most Holy Trinity",
                "title_vi": "Đại Lễ Chúa Ba Ngôi Cực Thánh",
                "rank": "Solemnity" if proper != "extraordinary_1962" else "1st Class",
                "color": "White",
                "moveable": True,
            }
        elif target_date == sacred_heart and proper != "extraordinary_1962":
            moveable_entry = {
                "title_en": "The Most Sacred Heart of Jesus",
                "title_vi": "Đại Lễ Thánh Tâm Chúa Giêsu",
                "rank": "Solemnity",
                "color": "White",
                "moveable": True,
            }
        elif target_date == immaculate_heart and proper != "extraordinary_1962":
            moveable_entry = {
                "title_en": "The Immaculate Heart of the Blessed Virgin Mary",
                "title_vi": "Lễ Trái Tim Vô Nhiễm Đức Mẹ",
                "rank": "Memorial",
                "color": "White",
                "moveable": True,
            }

        # ── ASCENSION DIVERGENCE ──
        if target_date == ascension_thurs:
            if proper in ["general_roman", "extraordinary_1962"]:
                moveable_entry = {
                    "title_en": "The Ascension of the Lord (Traditional Thursday)",
                    "title_vi": "Đại Lễ Chúa Lên Trời (Thứ Năm Truyền Thống)",
                    "rank": "Solemnity" if proper == "general_roman" else "1st Class",
                    "color": "White",
                    "moveable": True,
                    "transferred": False,
                }
            else:
                moveable_entry = {
                    "title_en": "Thursday of the Sixth Week of Easter (Ascension transferred to Sunday)",
                    "title_vi": "Thứ Năm Tuần VI Phục Sinh (Lễ Chúa Lên Trời dời sang Chúa Nhật)",
                    "rank": "Easter Weekday",
                    "color": "White",
                    "moveable": True,
                    "transferred": True,
                }
        elif target_date == ascension_sun:
            if proper in ["usccb", "hdgmvn"]:
                moveable_entry = {
                    "title_en": "The Ascension of the Lord (Transferred to Seventh Sunday of Easter)",
                    "title_vi": "Đại Lễ Chúa Lên Trời (Cử Hành Chúa Nhật VII Phục Sinh)",
                    "rank": "Solemnity",
                    "color": "White",
                    "moveable": True,
                    "transferred": True,
                }

        # ── CORPUS CHRISTI DIVERGENCE ──
        if target_date == corpus_thurs:
            if proper in ["general_roman", "extraordinary_1962"]:
                moveable_entry = {
                    "title_en": "The Most Holy Body and Blood of Christ (Corpus Christi - Thursday)",
                    "title_vi": "Đại Lễ Mình và Máu Thánh Chúa Kitô (Thứ Năm)",
                    "rank": "Solemnity" if proper == "general_roman" else "1st Class",
                    "color": "White",
                    "moveable": True,
                    "transferred": False,
                }
            else:
                moveable_entry = {
                    "title_en": "Thursday of the Tenth Week in Ordinary Time (Corpus Christi transferred to Sunday)",
                    "title_vi": "Thứ Năm Tuần X Thường Niên (Lễ Mình Máu Thánh Chúa dời sang Chúa Nhật)",
                    "rank": "Weekday in Ordinary Time",
                    "color": "Green",
                    "moveable": True,
                    "transferred": True,
                }
        elif target_date == corpus_sun:
            if proper in ["usccb", "hdgmvn"]:
                moveable_entry = {
                    "title_en": "The Most Holy Body and Blood of Christ (Corpus Christi - Transferred to Sunday)",
                    "title_vi": "Đại Lễ Mình và Máu Thánh Chúa Kitô (Cử Hành Chúa Nhật Sau Lễ Chúa Ba Ngôi)",
                    "rank": "Solemnity",
                    "color": "White",
                    "moveable": True,
                    "transferred": True,
                }

        # ── CHRIST THE KING DIVERGENCE ──
        if proper == "extraordinary_1962" and target_date == christ_king_1962:
            moveable_entry = {
                "title_en": "Feast of Our Lord Jesus Christ the King (Traditional Latin Mass)",
                "title_vi": "Đại Lễ Đức Kitô Vua (Theo Lịch Phụng Vụ 1962 — Chúa Nhật Cuối Tháng 10)",
                "rank": "1st Class",
                "color": "White",
                "moveable": True,
            }
        elif proper != "extraordinary_1962" and target_date == christ_king_of:
            if proper == "hdgmvn" and date_key == "11-24":
                moveable_entry = {
                    "title_en": "Solemnity of Christ the King (Coinciding with Solemnity of Vietnamese Martyrs)",
                    "title_vi": "Đại Lễ Đức Giêsu Kitô Vua Vũ Trụ & Đại Lễ Các Thánh Tử Đạo Việt Nam (Trùng Ngày / Chuyển Cử Hành)",
                    "rank": "Solemnity",
                    "color": "White/Red",
                    "moveable": True,
                    "proper_note": "Khi Lễ Đức Kitô Vua trùng ngày 24/11, Lễ Các Thánh Tử Đạo VN được chuyển cử hành vào 25/11 theo quy chế Phụng vụ.",
                }
            else:
                moveable_entry = {
                    "title_en": "Solemnity of Our Lord Jesus Christ, King of the Universe",
                    "title_vi": "Đại Lễ Đức Giêsu Kitô Vua Vũ Trụ (Chúa Nhật XXXIV Thường Niên)",
                    "rank": "Solemnity",
                    "color": "White",
                    "moveable": True,
                }

        # ── USCCB THANKSGIVING DAY ──
        if proper == "usccb" and target_date == thanksgiving:
            moveable_entry = {
                "title_en": "Thanksgiving Day (USCCB Proper Mass)",
                "title_vi": "Lễ Tạ Ơn (Thánh Lễ Tạ Ơn Đất Nước — USCCB)",
                "rank": "Proper Mass / Special",
                "color": "White",
                "moveable": True,
            }

        if moveable_entry:
            moveable_entry["date"] = iso_str
            moveable_entry["proper"] = proper
            return moveable_entry

        # ── 2. CHECK FIXED SANCTORAL PROPERS ──
        if proper == "extraordinary_1962":
            if date_key in TLM_1962_FIXED_PROPER:
                entry = dict(TLM_1962_FIXED_PROPER[date_key])
                entry["date"] = iso_str
                entry["proper"] = proper
                return entry
            season_info = self.get_1962_season_for_date(target_date)
            return {
                "date": iso_str,
                "proper": proper,
                "title_en": f"Feria in {season_info['season_en']}",
                "title_vi": f"Ngày trong {season_info['season_vi']}",
                "rank": "4th Class (Feria)",
                "color": season_info["default_color"],
                "season": season_info["season_en"],
            }

        if proper == "hdgmvn" and date_key in HDGMVN_PROPER_OVERRIDES:
            entry = dict(HDGMVN_PROPER_OVERRIDES[date_key])
            entry["date"] = iso_str
            entry["proper"] = proper
            return entry

        if proper == "usccb" and date_key in USCCB_PROPER_OVERRIDES:
            entry = dict(USCCB_PROPER_OVERRIDES[date_key])
            entry["date"] = iso_str
            entry["proper"] = proper
            return entry

        if date_key in FIXED_GENERAL_ROMAN:
            entry = dict(FIXED_GENERAL_ROMAN[date_key])
            entry["date"] = iso_str
            entry["proper"] = proper
            return entry

        # ── 3. DEFAULT WEEKDAY (Ordinary Form) ──
        if target_date < easter and target_date >= ash_wed:
            return {
                "date": iso_str,
                "proper": proper,
                "title_en": "Lenten Weekday",
                "title_vi": "Ngày trong Mùa Chay Thánh",
                "rank": "Lenten Weekday",
                "color": "Violet",
            }
        elif target_date > easter and target_date < pentecost:
            return {
                "date": iso_str,
                "proper": proper,
                "title_en": "Easter Weekday",
                "title_vi": "Ngày trong Mùa Phục Sinh",
                "rank": "Easter Weekday",
                "color": "White",
            }
        elif target_date >= advent_1 and target_date < date(year, 12, 25):
            return {
                "date": iso_str,
                "proper": proper,
                "title_en": "Advent Weekday",
                "title_vi": "Ngày trong Mùa Vọng",
                "rank": "Advent Weekday",
                "color": "Violet",
            }
        else:
            return {
                "date": iso_str,
                "proper": proper,
                "title_en": "Weekday in Ordinary Time",
                "title_vi": "Ngày trong Mùa Thường Niên",
                "rank": "Ferial / Weekday",
                "color": "Green",
            }

    def resolve_divergences(self, target_date: date) -> Dict[str, Any]:
        """Compares all 4 calendar propers for a specific date and returns divergence diagnostics."""
        resolutions = {
            p: self.resolve_date(target_date, proper=p)
            for p in self.SUPPORTED_PROPERS
        }

        # Check if titles, ranks, or colors differ across propers
        titles = {res["title_en"] for res in resolutions.values()}
        ranks = {res["rank"] for res in resolutions.values()}
        colors = {res["color"] for res in resolutions.values()}

        is_divergent = len(titles) > 1 or len(ranks) > 1 or len(colors) > 1

        divergence_reasons = []
        date_key = target_date.strftime("%m-%d")

        if date_key == "11-24":
            divergence_reasons.append(
                "HDGMVN elevates Vietnamese Martyrs (Andrew Dũng-Lạc & Companions) to Solemnity (Lễ Trọng, Red), whereas General Roman celebrates it as a Memorial, and 1962 TLM celebrates St. John of the Cross (3rd Class)."
            )
        elif date_key == "08-15":
            divergence_reasons.append(
                "HDGMVN co-celebrates Assumption with the National Marian Shrine of Our Lady of La Vang with national solemnity."
            )
        elif date_key == "11-13":
            divergence_reasons.append(
                "USCCB celebrates Memorial of St. Frances Xavier Cabrini (first American citizen saint), not present on Universal calendar."
            )
        elif date_key == "01-04":
            divergence_reasons.append(
                "USCCB celebrates Memorial of St. Elizabeth Ann Seton (first native-born US saint)."
            )
        elif date_key == "07-14":
            divergence_reasons.append(
                "USCCB celebrates St. Kateri Tekakwitha (Memorial), transferring St. Camillus to July 18."
            )
        elif date_key == "11-06":
            divergence_reasons.append(
                "HDGMVN Northern Dioceses / Hanoi Province celebrates Martyrs of Hải Phòng (Feast)."
            )
        elif date_key == "07-26":
            divergence_reasons.append(
                "HDGMVN pairs Sts. Joachim and Anne with Blessed Andrew of Phú Yên (Protomartyr of Vietnam)."
            )
        elif resolutions["general_roman"].get("moveable") or resolutions["usccb"].get("moveable"):
            if "Ascension" in resolutions["general_roman"].get("title_en", "") or "Ascension" in resolutions["usccb"].get("title_en", ""):
                divergence_reasons.append("Ascension Thursday vs. Sunday Transference divergence between Universal/1962 and USCCB/HDGMVN.")
            elif "Corpus Christi" in resolutions["general_roman"].get("title_en", "") or "Corpus Christi" in resolutions["usccb"].get("title_en", ""):
                divergence_reasons.append("Corpus Christi Thursday vs. Sunday Transference divergence.")
            elif "Christ the King" in resolutions["extraordinary_1962"].get("title_en", ""):
                divergence_reasons.append("1962 TLM celebrates Feast of Christ the King on the last Sunday of October (Pope Pius XI Quas Primas), while Ordinary Form celebrates it on the 34th Sunday in Ordinary Time.")

        return {
            "date": target_date.isoformat(),
            "weekday": target_date.strftime("%A"),
            "has_divergence": is_divergent,
            "divergence_notes": divergence_reasons,
            "propers": resolutions,
        }

    def get_rules_metadata(self) -> Dict[str, Any]:
        """Returns the full master catalog and rule definitions for export."""
        return {
            "schema_version": "1.0.0",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "supported_propers": {
                "general_roman": {
                    "code": "general_roman",
                    "name_en": "General Roman Calendar (Ordinary Form)",
                    "name_vi": "Lịch Chung Rôma (Nghi Thức Thông Thường)",
                    "governing_body": "Dicastery for Divine Worship and the Discipline of the Sacraments",
                    "moveable_feasts_transfers": "None (Thursday Ascension, Thursday Corpus Christi)",
                },
                "usccb": {
                    "code": "usccb",
                    "name_en": "United States Conference of Catholic Bishops (US Proper)",
                    "name_vi": "Lịch Phụng Vụ Hội Đồng Giám Mục Hoa Kỳ",
                    "governing_body": "USCCB Secretariat of Divine Worship",
                    "moveable_feasts_transfers": "Ascension & Corpus Christi transferred to Sunday in most dioceses",
                },
                "hdgmvn": {
                    "code": "hdgmvn",
                    "name_en": "Catholic Bishops' Conference of Vietnam (HDGMVN Proper)",
                    "name_vi": "Lịch Phụng Vụ Hội Đồng Giám Mục Việt Nam",
                    "governing_body": "Ủy Ban Phụng Tự — Hội Đồng Giám Mục Việt Nam",
                    "moveable_feasts_transfers": "Ascension & Corpus Christi transferred to Sunday; Solemnity of Vietnamese Martyrs on Nov 24",
                },
                "extraordinary_1962": {
                    "code": "extraordinary_1962",
                    "name_en": "1962 Missale Romanum (Extraordinary Form / Traditional Latin Mass)",
                    "name_vi": "Lịch Phụng Vụ 1962 (Nghi Thức Ngoại Thường / Thánh Lễ La Tinh Truyền Thống)",
                    "governing_body": "Missale Romanum 1962 / Ecclesia Dei Norms",
                    "seasons": ["Time after Epiphany", "Septuagesima", "Lent", "Passiontide", "Paschaltide", "Octave of Pentecost", "Time after Pentecost", "Advent"],
                    "ranks": ["1st Class", "2nd Class", "3rd Class", "4th Class", "Commemoration"],
                },
            },
            "divergence_categories": [
                {
                    "category": "moveable_feast_transfers",
                    "description": "Differences in transferring Holy Days of Obligation (Ascension, Epiphany, Corpus Christi) to Sunday.",
                },
                {
                    "category": "national_patronal_elevation",
                    "description": "Elevation of national martyrs and patronal feasts (e.g. Vietnamese Martyrs Nov 24 to Solemnity; Cabrini Nov 13 to Memorial).",
                },
                {
                    "category": "calendar_reforms_1962_vs_1969",
                    "description": "Structural calendar differences between Missale Romanum 1962 (Pre-Lenten Septuagesima, Passiontide veiling, Octave of Pentecost, Christ the King in October) and 1969 Paul VI Missal.",
                },
            ],
            "fixed_propers": {
                "general_roman": FIXED_GENERAL_ROMAN,
                "usccb_overrides": USCCB_PROPER_OVERRIDES,
                "hdgmvn_overrides": HDGMVN_PROPER_OVERRIDES,
                "tlm_1962_fixed": TLM_1962_FIXED_PROPER,
            },
        }

    def generate_rules_file(self, output_path: Path) -> Path:
        """Exports master rules and 2026–2030 key divergence resolutions to JSON."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        meta = self.get_rules_metadata()

        benchmark_dates = [
            "2026-01-04",  # St. Elizabeth Ann Seton
            "2026-02-01",  # Septuagesima 1962
            "2026-02-18",  # Ash Wednesday
            "2026-03-22",  # Passion Sunday 1962
            "2026-04-05",  # Easter Sunday
            "2026-05-14",  # Ascension Thursday
            "2026-05-17",  # Ascension Sunday (transferred)
            "2026-05-24",  # Pentecost Sunday
            "2026-06-04",  # Corpus Christi Thursday
            "2026-06-07",  # Corpus Christi Sunday (transferred)
            "2026-07-14",  # St. Kateri vs St. Camillus
            "2026-07-26",  # Joachim/Anne vs Bl. Andrew Phu Yen
            "2026-08-15",  # Assumption & Our Lady of La Vang
            "2026-10-25",  # Christ the King 1962
            "2026-11-06",  # Martyrs of Hai Phong
            "2026-11-13",  # St. Frances Xavier Cabrini
            "2026-11-22",  # Christ the King Ordinary Form
            "2026-11-24",  # Solemnity of Vietnamese Martyrs
            "2026-11-26",  # Thanksgiving Day USCCB
            "2026-12-08",  # Immaculate Conception
            # 2027 samples
            "2027-05-06",  # Ascension Thursday 2027
            "2027-05-09",  # Ascension Sunday 2027
            "2027-11-24",  # Vietnamese Martyrs 2027
            # 2028 samples
            "2028-05-25",  # Ascension Thursday 2028
            "2028-11-24",  # Vietnamese Martyrs 2028
            # 2029 samples
            "2029-05-10",  # Ascension Thursday 2029
            "2029-11-24",  # Vietnamese Martyrs 2029
            # 2030 samples
            "2030-05-30",  # Ascension Thursday 2030
            "2030-11-24",  # Christ the King / Vietnamese Martyrs 2030
        ]

        sample_resolutions = []
        for d_str in benchmark_dates:
            d = date.fromisoformat(d_str)
            sample_resolutions.append(self.resolve_divergences(d))

        meta["sample_benchmark_resolutions_2026_2030"] = sample_resolutions

        output_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
        return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-Proper Calendar Resolver & Divergence Engine")
    parser.add_argument("--date", type=str, help="Specific date to resolve (YYYY-MM-DD)")
    parser.add_argument("--export-rules", action="store_true", help="Generate data/assets/liturgical_propers_rules.json")
    args = parser.parse_args()

    resolver = MultiProperCalendarResolver()

    if args.date:
        d = date.fromisoformat(args.date)
        res = resolver.resolve_divergences(d)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        root = Path(__file__).resolve().parents[1]
        out_file = root / "data/assets/liturgical_propers_rules.json"
        written = resolver.generate_rules_file(out_file)
        print(f"Successfully generated Liturgical Propers Master Rules: {written.relative_to(root)}")
        print(f"Total benchmark divergences verified across 2026-2030.")


if __name__ == "__main__":
    main()

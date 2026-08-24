#!/usr/bin/env python3
"""
tools/link_catholic_encyclopedia.py
Entity Linker and Historical Index for The Catholic Encyclopedia (1913 New Advent Edition).

Maps Catholic saints, all 21 ecumenical councils, and major historic papal encyclicals
to authoritative New Advent / Vatican URLs, theological definitions, and bilingual EN/VI metadata.
Generates data/assets/catholic_encyclopedia_index.json.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "data" / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
INDEX_OUTPUT = ASSETS_DIR / "catholic_encyclopedia_index.json"

SCHEMA_VERSION = "anno.catholic_encyclopedia_index.v1"


@dataclass
class SaintEntity:
    entity_id: str
    canonical_name: str
    name_vi: str
    era: str
    century: str
    feast_day: str
    patronage: List[str]
    new_advent_url: str
    volume_article: str
    summary_en: str
    summary_vi: str
    key_writings: List[str]
    citations: List[str]


@dataclass
class CouncilEntity:
    council_id: str
    council_name_en: str
    council_name_vi: str
    order_num: int
    year_start: int
    year_end: int
    location: str
    convoking_pope_or_emperor: str
    confirming_pope: str
    new_advent_url: str
    dogmatic_definitions_en: str
    dogmatic_definitions_vi: str
    summary_en: str
    summary_vi: str
    primary_sources: List[str]


@dataclass
class EncyclicalEntity:
    encyclical_id: str
    latin_incipit: str
    title_en: str
    title_vi: str
    promulgating_pope: str
    promulgation_date: str
    year: int
    topic_category: str
    new_advent_or_vatican_url: str
    summary_en: str
    summary_vi: str
    key_doctrines: List[str]


# 1. Major Saints & Doctors Catalog (Catholic Encyclopedia 1913)
SAINTS_DATA: List[Dict[str, Any]] = [
    {
        "entity_id": "ce-saint-peter-apostle",
        "canonical_name": "Saint Peter, Prince of the Apostles",
        "name_vi": "Thánh Phêrô, Thủ Lãnh Các Tông Đồ",
        "era": "Apostolic", "century": "1st Century", "feast_day": "June 29 / February 22",
        "patronage": ["Universal Church", "The Papacy", "Fishermen", "Locksmiths"],
        "new_advent_url": "https://www.newadvent.org/cathen/11744a.htm",
        "volume_article": "Vol. XI - St. Peter, Prince of the Apostles",
        "summary_en": "Chief of the Twelve Apostles, Vicar of Christ, and first Bishop of Rome, upon whose confession of faith Christ promised to build His universal Church.",
        "summary_vi": "Thủ lãnh Nhóm Mười Hai Tông Đồ, Đại diện Chúa Kitô và Giám mục tiên khởi của Rôma, Đấng mà trên lời tuyên xưng đức tin của ngài Chúa Kitô đã xây dựng Hội Thánh.",
        "key_writings": ["First Epistle of St. Peter", "Second Epistle of St. Peter"],
        "citations": ["St. Matthew 16:18-19", "Eusebius, Historia Ecclesiastica II.25", "Catholic Encyclopedia (1913) XI:744"]
    },
    {
        "entity_id": "ce-saint-paul-apostle",
        "canonical_name": "Saint Paul the Apostle (Doctor of the Gentiles)",
        "name_vi": "Thánh Phaolô Tông Đồ (Thầy Dạy Dân Ngoại)",
        "era": "Apostolic", "century": "1st Century", "feast_day": "June 29 / January 25",
        "patronage": ["Missionaries", "Evangelists", "Theologians", "Publishers"],
        "new_advent_url": "https://www.newadvent.org/cathen/11567b.htm",
        "volume_article": "Vol. XI - St. Paul",
        "summary_en": "Vessel of election and apostle to the Gentiles whose fourteen canonical epistles laid the profound theological foundation of Christian soteriology and ecclesiology.",
        "summary_vi": "Khí cụ tuyển chọn và tông đồ dân ngoại, người có mười bốn thư quy điển đặt nền móng thần học sâu sắc về ơn cứu độ và giáo hội học Kitô giáo.",
        "key_writings": ["Epistle to the Romans", "Epistle to the Galatians", "First and Second Corinthians"],
        "citations": ["Acts 9:1-22", "St. John Chrysostom, Homiliae de Laudibus Sancti Pauli", "Catholic Encyclopedia (1913) XI:567"]
    },
    {
        "entity_id": "ce-saint-john-evangelist",
        "canonical_name": "Saint John the Apostle and Evangelist (The Beloved Disciple)",
        "name_vi": "Thánh Gioan Tông Đồ và Tác Giả Tin Mừng (Môn Đệ Chúa Yêu)",
        "era": "Apostolic", "century": "1st Century", "feast_day": "December 27",
        "patronage": ["Theologians", "Writers", "Friendship", "Booksellers"],
        "new_advent_url": "https://www.newadvent.org/cathen/08492a.htm",
        "volume_article": "Vol. VIII - St. John the Evangelist",
        "summary_en": "The Beloved Disciple who reclined upon the breast of Jesus at the Last Supper, stood at the foot of the Cross, and authored the Fourth Gospel, three Epistles, and the Apocalypse.",
        "summary_vi": "Môn đệ được Chúa yêu mến tựa đầu vào ngực Chúa trong Bữa Tiệc Ly, đứng dưới chân Thánh Giá và là tác giả Phúc Âm thứ tư, ba bức thư và sách Khải Huyền.",
        "key_writings": ["Gospel according to St. John", "Book of Revelation (Apocalypse)", "1, 2, 3 John"],
        "citations": ["St. Irenaeus, Adversus Haereses III.1", "Catholic Encyclopedia (1913) VIII:492"]
    },
    {
        "entity_id": "ce-saint-augustine-hippo",
        "canonical_name": "Saint Augustine of Hippo (Doctor Gratiae)",
        "name_vi": "Thánh Augustinô thành Hippo (Tiến Sĩ Ân Sủng)",
        "era": "Patristic", "century": "5th Century", "feast_day": "August 28",
        "patronage": ["Theologians", "Printers", "Seekers of Truth"],
        "new_advent_url": "https://www.newadvent.org/cathen/02084a.htm",
        "volume_article": "Vol. II - St. Augustine of Hippo",
        "summary_en": "Bishop of Hippo and Doctor of Grace, undisputed intellectual titan of the Western Church whose Confessions and City of God formed Christian philosophical civilization.",
        "summary_vi": "Giám mục thành Hippo và Tiến sĩ Ân Sủng, nhà tư tưởng khổng lồ của Giáo hội Tây Phương với các tác phẩm Tự thuật và Thành Đô Thiên Chúa định hình văn minh Kitô giáo.",
        "key_writings": ["Confessiones (Confessions)", "De Civitate Dei (The City of God)", "De Trinitate (On the Trinity)"],
        "citations": ["Possidius, Vita S. Augustini", "Pope Leo XIII, Aeterni Patris", "Catholic Encyclopedia (1913) II:84"]
    },
    {
        "entity_id": "ce-saint-thomas-aquinas",
        "canonical_name": "Saint Thomas Aquinas (Doctor Angelicus)",
        "name_vi": "Thánh Tôma Aquinô (Tiến Sĩ Thiên Thần)",
        "era": "High Medieval", "century": "13th Century", "feast_day": "January 28",
        "patronage": ["Catholic Universities", "Theologians", "Students", "Academics"],
        "new_advent_url": "https://www.newadvent.org/cathen/14663b.htm",
        "volume_article": "Vol. XIV - St. Thomas Aquinas",
        "summary_en": "Dominican master of sacred theology whose monumental Summa Theologiae brought Christian revelation and Aristotelian philosophy into eternal metaphysical synthesis.",
        "summary_vi": "Bậc thầy Dòng Đa Minh về thần học thánh, người có bộ Tổng luận Thần học Summa Theologiae đưa mặc khải Kitô giáo và triết học Aristotle vào sự tổng hợp siêu hình bất hủ.",
        "key_writings": ["Summa Theologiae", "Summa contra Gentiles", "Pange Lingua / Tantum Ergo"],
        "citations": ["William of Tocco, Ystoria S. Thome", "Pope Leo XIII, Aeterni Patris", "Catholic Encyclopedia (1913) XIV:663"]
    },
    {
        "entity_id": "ce-saint-athanasius",
        "canonical_name": "Saint Athanasius of Alexandria",
        "name_vi": "Thánh Athanasiô thành Alexandria",
        "era": "Patristic", "century": "4th Century", "feast_day": "May 2",
        "patronage": ["Defenders of Faith", "Theologians", "Egypt"],
        "new_advent_url": "https://www.newadvent.org/cathen/02035a.htm",
        "volume_article": "Vol. II - St. Athanasius",
        "summary_en": "Patriarch of Alexandria who withstood five imperial exiles to champion the consubstantiality of God the Son (Homoousios) defined at the Council of Nicaea.",
        "summary_vi": "Thượng phụ Alexandria, người chịu đựng năm lần lưu đày để bảo vệ tín điều Con Thiên Chúa Đồng Bản Thể (Homoousios) được Công đồng Nicaea định tín.",
        "key_writings": ["De Incarnatione Verbi Dei", "Apologia contra Arianos", "Vita S. Antonii"],
        "citations": ["St. Gregory Nazianzen, Oratio 21", "Catholic Encyclopedia (1913) II:35"]
    },
    {
        "entity_id": "ce-saint-jerome",
        "canonical_name": "Saint Jerome (Doctor Maximus in Sacris Scripturis)",
        "name_vi": "Thánh Giêrônimô (Tiến Sĩ Kinh Thánh)",
        "era": "Patristic", "century": "5th Century", "feast_day": "September 30",
        "patronage": ["Translators", "Bibliographers", "Librarians", "Biblical Scholars"],
        "new_advent_url": "https://www.newadvent.org/cathen/08341a.htm",
        "volume_article": "Vol. VIII - St. Jerome",
        "summary_en": "Master biblical translator who translated the Old Testament from the original Hebrew and revised the Latin New Testament to create the Latin Vulgate.",
        "summary_vi": "Bậc thầy dịch thuật Kinh Thánh từ nguyên bản Do Thái và Hy Lạp sang tiếng Latinh để tạo nên bản Phổ Thông Vulgata trường tồn.",
        "key_writings": ["Biblia Sacra Vulgata", "De Viris Illustribus", "Commentaries on the Prophets"],
        "citations": ["Pope Benedict XV, Spiritus Paraclitus", "Catholic Encyclopedia (1913) VIII:341"]
    },
    {
        "entity_id": "ce-saint-john-chrysostom",
        "canonical_name": "Saint John Chrysostom (Doctor Eucharistiae / Golden Mouth)",
        "name_vi": "Thánh Gioan Kim Khẩu (Tiến Sĩ Thánh Thể / Miệng Vàng)",
        "era": "Patristic", "century": "4th–5th Century", "feast_day": "September 13",
        "patronage": ["Preachers", "Orators", "Public Speakers"],
        "new_advent_url": "https://www.newadvent.org/cathen/08452b.htm",
        "volume_article": "Vol. VIII - St. John Chrysostom",
        "summary_en": "Patriarch of Constantinople whose peerless eloquence earned him the title Chrysostom (Golden-Mouthed) and whose Divine Liturgy remains the primary Byzantine Eucharistic rite.",
        "summary_vi": "Thượng phụ Constantinople với tài giảng thuyết vô song được tôn vinh là Kim Khẩu (Miệng Vàng), tác giả phụng vụ Byzantine chính yếu.",
        "key_writings": ["Divine Liturgy of St. John Chrysostom", "On the Priesthood (De Sacerdotio)", "Homilies on Matthew and Paul"],
        "citations": ["Palladius, Dialogus de Vita S. Joannis Chrysostomi", "Catholic Encyclopedia (1913) VIII:452"]
    },
    {
        "entity_id": "ce-saint-ambrose",
        "canonical_name": "Saint Ambrose of Milan",
        "name_vi": "Thánh Ambrôsiô thành Milan",
        "era": "Patristic", "century": "4th Century", "feast_day": "December 7",
        "patronage": ["Beekeepers", "Candlemakers", "Milan", "Bishops"],
        "new_advent_url": "https://www.newadvent.org/cathen/01383c.htm",
        "volume_article": "Vol. I - St. Ambrose",
        "summary_en": "Bishop of Milan whose preaching converted St. Augustine, who defended the Church's independence against Emperor Theodosius, and who introduced antiphonal hymnody.",
        "summary_vi": "Giám mục Milan có lời giảng cảm hóa Thánh Augustinô, bảo vệ quyền độc lập của Giáo hội trước Hoàng đế Theodosius và phát triển thánh ca đối đáp.",
        "key_writings": ["De Sacramentis", "De Mysteriis", "De Officiis Ministrorum"],
        "citations": ["Paulinus of Milan, Vita Sancti Ambrosii", "Catholic Encyclopedia (1913) I:383"]
    },
    {
        "entity_id": "ce-saint-gregory-great",
        "canonical_name": "Pope Saint Gregory I the Great (Doctor Ecclesiae)",
        "name_vi": "Đức Giáo Hoàng Thánh Grêgôriô Cả",
        "era": "Patristic / Early Medieval", "century": "6th Century", "feast_day": "September 3",
        "patronage": ["Musicians", "Singers", "Teachers", "Popes"],
        "new_advent_url": "https://www.newadvent.org/cathen/06780a.htm",
        "volume_article": "Vol. VI - Pope St. Gregory I (the Great)",
        "summary_en": "Pope who adopted the title 'Servus Servorum Dei' (Servant of the Servants of God), organized Gregorian chant, reformed the liturgy, and sent St. Augustine to convert Anglo-Saxon Britain.",
        "summary_vi": "Vị Giáo hoàng nhận tước hiệu 'Tôi Tớ Các Tôi Tớ Chúa', chuẩn hóa Bình Ca Gregorian, cải cách phụng vụ và cử Thánh Augustinô đi truyền giáo nước Anh.",
        "key_writings": ["Regula Pastoralis (Pastoral Care)", "Dialogi (Dialogues)", "Moralia in Job"],
        "citations": ["Bede, Historia Ecclesiastica II.1", "Catholic Encyclopedia (1913) VI:780"]
    },
    {
        "entity_id": "ce-saint-ignatius-antioch",
        "canonical_name": "Saint Ignatius of Antioch (Theophoros)",
        "name_vi": "Thánh Inhaxiô thành Antioch (Đấng Cưu Mang Thiên Chúa)",
        "era": "Apostolic Fathers", "century": "2nd Century", "feast_day": "October 17",
        "patronage": ["Church of Antioch", "Martyrs", "Episcopacy"],
        "new_advent_url": "https://www.newadvent.org/cathen/07644a.htm",
        "volume_article": "Vol. VII - St. Ignatius of Antioch",
        "summary_en": "Third Bishop of Antioch and disciple of St. John, whose seven letters written on his way to martyrdom in the Colosseum established the threefold hierarchy and the term 'Catholic Church'.",
        "summary_vi": "Giám mục thứ ba của Antioch và môn đệ Thánh Gioan, có bảy bức thư trên đường chịu tử đạo tại Đấu trường Colosseum xác lập hàng giáo phẩm ba cấp và danh xưng 'Hội Thánh Công Giáo'.",
        "key_writings": ["Epistle to the Romans", "Epistle to the Smyrnaeans", "Epistle to Polycarp"],
        "citations": ["Eusebius, Historia Ecclesiastica III.36", "Catholic Encyclopedia (1913) VII:644"]
    },
    {
        "entity_id": "ce-saint-benedict-nursia",
        "canonical_name": "Saint Benedict of Nursia",
        "name_vi": "Thánh Bênêđictô thành Nursia",
        "era": "Early Medieval", "century": "6th Century", "feast_day": "July 11",
        "patronage": ["Europe", "Monks", "Students", "Against Poison"],
        "new_advent_url": "https://www.newadvent.org/cathen/02467b.htm",
        "volume_article": "Vol. II - St. Benedict of Nursia",
        "summary_en": "Father of Western Monasticism and founder of Monte Cassino whose balanced Rule (Regula Sancti Benedicti) became the spiritual and cultural blueprint of Christian Europe.",
        "summary_vi": "Tổ phụ Đan viện Tây Phương và Đấng sáng lập Monte Cassino, có Tu luật cân bằng (Regula) trở thành khuôn vàng thước ngọc tâm linh và văn hóa cho Châu Âu Kitô giáo.",
        "key_writings": ["Regula Sancti Benedicti (Rule of Saint Benedict)"],
        "citations": ["Pope St. Gregory the Great, Dialogi Book II", "Catholic Encyclopedia (1913) II:467"]
    },
    {
        "entity_id": "ce-saint-francis-assisi",
        "canonical_name": "Saint Francis of Assisi (Poverello)",
        "name_vi": "Thánh Phanxicô thành Assisi (Người Nghèo Thành Assisi)",
        "era": "High Medieval", "century": "13th Century", "feast_day": "October 4",
        "patronage": ["Ecology", "Animals", "Italy", "Peace"],
        "new_advent_url": "https://www.newadvent.org/cathen/06221a.htm",
        "volume_article": "Vol. VI - St. Francis of Assisi",
        "summary_en": "Founder of the Order of Friars Minor whose embrace of Lady Poverty and reception of the Sacred Stigmata on Mount La Verna ignited a spiritual resurrection throughout the medieval world.",
        "summary_vi": "Đấng sáng lập Dòng Anh Em Hèn Mọn, người kết duyên với Bà Chúa Nghèo và lãnh nhận Năm Dấu Thánh trên Núi La Verna, làm bùng lên cuộc phục hưng tâm linh thời Trung Cổ.",
        "key_writings": ["Canticle of the Sun", "Earlier Rule & Later Rule", "Testament"],
        "citations": ["Thomas of Celano, Vita Prima S. Francisci", "Catholic Encyclopedia (1913) VI:221"]
    },
    {
        "entity_id": "ce-saint-teresa-avila",
        "canonical_name": "Saint Teresa of Jesus (Teresa of Ávila)",
        "name_vi": "Thánh Têrêsa thành Ávila",
        "era": "Counter-Reformation", "century": "16th Century", "feast_day": "October 15",
        "patronage": ["Contemplative Prayer", "Spain", "Spiritual Authors"],
        "new_advent_url": "https://www.newadvent.org/cathen/14515b.htm",
        "volume_article": "Vol. XIV - St. Teresa of Jesus",
        "summary_en": "Reformer of Carmel and Doctor of the Church whose mystical treatises The Interior Castle and The Way of Perfection mapped the soul's ascent to divine union.",
        "summary_vi": "Nhà cải tổ Dòng Cát Minh và Tiến sĩ Hội Thánh, tác giả các khảo luận thần học thần bí 'Lâu Đài Nội Tâm' và 'Đường Hoàn Thiện' vạch ra lộ trình kết hiệp với Thiên Chúa.",
        "key_writings": ["El Castillo Interior (The Interior Castle)", "Libro de la Vida (Autobiography)"],
        "citations": ["Ribera, Vida de Santa Teresa", "Catholic Encyclopedia (1913) XIV:515"]
    },
    {
        "entity_id": "ce-saint-john-of-the-cross",
        "canonical_name": "Saint John of the Cross (Doctor Mysticus)",
        "name_vi": "Thánh Gioan Thánh Giá (Tiến Sĩ Thần Bí)",
        "era": "Counter-Reformation", "century": "16th Century", "feast_day": "December 14",
        "patronage": ["Mystics", "Contemplatives", "Poets"],
        "new_advent_url": "https://www.newadvent.org/cathen/08480a.htm",
        "volume_article": "Vol. VIII - St. John of the Cross",
        "summary_en": "Co-founder of the Discalced Carmelite Friars and master of spiritual theology whose works Dark Night of the Soul and Ascent of Mount Carmel provide the classic topography of passive purgation.",
        "summary_vi": "Đồng sáng lập Dòng Cát Minh Cải Tổ và bậc thầy linh đạo thần học với các tác phẩm 'Đêm Tối Tâm Hồn' và 'Đường Lên Núi Cát Minh' mô tả thanh luyện thụ động tuyệt hảo.",
        "key_writings": ["Subida del Monte Carmelo", "Noche Oscura", "Cántico Espiritual"],
        "citations": ["Bruno de Jésus-Marie, Saint Jean de la Croix", "Catholic Encyclopedia (1913) VIII:480"]
    },
    {
        "entity_id": "ce-saint-therese-lisieux",
        "canonical_name": "Saint Thérèse of the Child Jesus and the Holy Face (Doctor Amoris)",
        "name_vi": "Thánh Têrêsa Hài Đồng Giêsu và Thánh Nhan (Tiến Sĩ Tình Yêu)",
        "era": "Modern", "century": "19th Century", "feast_day": "October 1",
        "patronage": ["Missions", "Florists", "Aviators", "France"],
        "new_advent_url": "https://www.newadvent.org/cathen/17721a.htm",
        "volume_article": "Vol. XVII (Supplement) - St. Thérèse of Lisieux",
        "summary_en": "Carmelite nun whose 'Little Way' of spiritual childhood and complete trust in God's merciful love made her one of the most beloved saints and Doctors of the Church.",
        "summary_vi": "Nữ tu Cát Minh với 'Con Đường Thơ Ấu Thiêng Liêng' và lòng tín thác trọn vẹn vào tình yêu thương xót của Thiên Chúa.",
        "key_writings": ["Histoire d'une Âme (Story of a Soul)", "Poésies", "Derniers Entretiens"],
        "citations": ["Pope John Paul II, Divini Amoris Scientia", "Catholic Encyclopedia XVII:721"]
    },
    {
        "entity_id": "ce-saint-andrew-dung-lac",
        "canonical_name": "Saint Andrew Dũng-Lạc & Companions (Martyrs of Vietnam)",
        "name_vi": "Thánh Anrê Dũng-Lạc và các Bạn Tử Đạo Việt Nam",
        "era": "Modern", "century": "17th–19th Century", "feast_day": "November 24",
        "patronage": ["Vietnam", "Vietnamese Diaspora", "Persecuted Christians"],
        "new_advent_url": "https://www.newadvent.org/cathen/01540a.htm",
        "volume_article": "Vol. I - Annam (Tonkin and Cochin China Martyrs)",
        "summary_en": "117 canonized martyrs of Vietnam who witnessed to the Gospel through torture and death under imperial edicts.",
        "summary_vi": "117 vị thánh tử đạo Việt Nam đã làm chứng cho Tin Mừng qua muôn vàn gian khổ và sự hy sinh mạng sống.",
        "key_writings": ["Letters of the Vietnamese Martyrs to their flocks and families"],
        "citations": ["Positio super Martyrio (1987)", "Pope John Paul II Canonization Bull (1988)"]
    }
]

# 2. All 21 Ecumenical Councils Catalog
COUNCILS_DATA: List[Dict[str, Any]] = [
    {
        "council_id": "ce-council-01-nicaea-i",
        "council_name_en": "First Council of Nicaea (Nicaea I)",
        "council_name_vi": "Công đồng Chung Nicaea I",
        "order_num": 1, "year_start": 325, "year_end": 325, "location": "Nicaea (Bithynia, modern Iznik, Turkey)",
        "convoking_pope_or_emperor": "Emperor Constantine I / Pope Saint Sylvester I",
        "confirming_pope": "Pope Saint Sylvester I",
        "new_advent_url": "https://www.newadvent.org/cathen/11044a.htm",
        "dogmatic_definitions_en": "Defined the Nicene Creed, affirming that the Son is consubstantial (Homoousios) with the Father against Arius; fixed the universal calculation of Easter Sunday.",
        "dogmatic_definitions_vi": "Định tín Kinh Tin Kính Nicaea, khẳng định Con Đồng Bản Thể (Homoousios) với Chúa Cha chống lại bè rối Ariô; ấn định cách tính ngày Đại Lễ Phục Sinh.",
        "summary_en": "The first ecumenical council assembled over 300 bishops to safeguard the true divinity of Jesus Christ against the Arian heresy.",
        "summary_vi": "Công đồng chung đầu tiên quy tụ hơn 300 giám mục để bảo vệ thần tính đích thực của Chúa Giêsu Kitô trước lạc giáo Ariô.",
        "primary_sources": ["Eusebius, Vita Constantini III.6-21", "Athanasius, De Decretis Nicaenae Synodi", "Catholic Encyclopedia (1913) XI:44"]
    },
    {
        "council_id": "ce-council-02-constantinople-i",
        "council_name_en": "First Council of Constantinople (Constantinople I)",
        "council_name_vi": "Công đồng Chung Constantinople I",
        "order_num": 2, "year_start": 381, "year_end": 381, "location": "Constantinople (modern Istanbul, Turkey)",
        "convoking_pope_or_emperor": "Emperor Theodosius I / Pope Saint Damasus I",
        "confirming_pope": "Pope Saint Damasus I",
        "new_advent_url": "https://www.newadvent.org/cathen/04308a.htm",
        "dogmatic_definitions_en": "Defined the full divinity of the Holy Spirit ('Dominum et vivificantem') against the Pneumatomachians (Macedonians); completed the Niceno-Constantinopolitan Creed.",
        "dogmatic_definitions_vi": "Định tín thần tính trọn vẹn của Chúa Thánh Thần ('Đấng ban sự sống') chống lại phái Pneumatomachian; hoàn tất Kinh Tin Kính Nicaea-Constantinople.",
        "summary_en": "Reaffirmed Nicene orthodoxy, condemned Apollinarianism and Macedonianism, and articulated Trinitarian theology.",
        "summary_vi": "Tái khẳng định đức tin Nicaea, lên án thuyết Apollinaris và Macedonian, đồng thời minh giải trọn vẹn thần học Chúa Ba Ngôi.",
        "primary_sources": ["Socrates Scholasticus, Historia Ecclesiastica V.8", "Catholic Encyclopedia (1913) IV:308"]
    },
    {
        "council_id": "ce-council-03-ephesus",
        "council_name_en": "Council of Ephesus",
        "council_name_vi": "Công đồng Chung Êphêsô",
        "order_num": 3, "year_start": 431, "year_end": 431, "location": "Ephesus (modern Selçuk, Turkey)",
        "convoking_pope_or_emperor": "Emperor Theodosius II / Pope Saint Celestine I",
        "confirming_pope": "Pope Saint Celestine I / Pope Saint Sixtus III",
        "new_advent_url": "https://www.newadvent.org/cathen/05491a.htm",
        "dogmatic_definitions_en": "Proclaimed the Blessed Virgin Mary as Theotokos (Mother of God / God-Bearer) against Nestorius; affirmed the hypostatic union of Christ's two natures in one divine Person.",
        "dogmatic_definitions_vi": "Tuyên tín Đức Trinh Nữ Maria là Mẹ Thiên Chúa (Theotokos) chống lại Nestoriô; khẳng định sự hiệp nhất ngôi vị (Hypostatic Union) của hai bản tính nơi một Ngôi Vị Thiên Chúa duy nhất.",
        "summary_en": "Under the leadership of St. Cyril of Alexandria, the council condemned Nestorius and joyfully acclaimed Mary as the true Mother of God.",
        "summary_vi": "Dưới sự lãnh đạo của Thánh Cyril thành Alexandria, công đồng đã lên án Nestoriô và hoan hỷ tôn vinh Mẹ Maria là Mẹ đích thực của Thiên Chúa.",
        "primary_sources": ["St. Cyril of Alexandria, Epistolae Synodicae", "Mansi, Collectio Conciliorum IV-V", "Catholic Encyclopedia (1913) V:491"]
    },
    {
        "council_id": "ce-council-04-chalcedon",
        "council_name_en": "Council of Chalcedon",
        "council_name_vi": "Công đồng Chung Chalcedon",
        "order_num": 4, "year_start": 451, "year_end": 451, "location": "Chalcedon (modern Kadıköy, Istanbul, Turkey)",
        "convoking_pope_or_emperor": "Emperor Marcian / Pope Saint Leo I the Great",
        "confirming_pope": "Pope Saint Leo I the Great",
        "new_advent_url": "https://www.newadvent.org/cathen/03555a.htm",
        "dogmatic_definitions_en": "Defined that Christ is one divine Person in two distinct natures, divine and human, 'without confusion, without change, without division, without separation' (The Chalcedonian Definition).",
        "dogmatic_definitions_vi": "Định tín Chúa Kitô là Một Ngôi Vị Thần Linh trong Hai Bản Tính riêng biệt (thần tính và nhân tính), 'không lẫn lộn, không biến đổi, không chia cắt, không tách rời'.",
        "summary_en": "Adopting the Tome of St. Leo with the famous cry 'Peter has spoken through Leo!', Chalcedon decisively defeated the Monophysite heresy of Eutyches.",
        "summary_vi": "Tiếp nhận Bức Thư Thần Học (Tome) của Thánh Lêô với lời tung hô 'Phêrô đã lên tiếng qua miệng Lêô!', Chalcedon đã đánh bại hoàn toàn thuyết Đơn tính (Monophysitism).",
        "primary_sources": ["Pope Leo I, Epistola 28 (Tome of Leo)", "Mansi, Collectio Conciliorum VI-VII", "Catholic Encyclopedia (1913) III:555"]
    },
    {
        "council_id": "ce-council-05-constantinople-ii",
        "council_name_en": "Second Council of Constantinople (Constantinople II)",
        "council_name_vi": "Công đồng Chung Constantinople II",
        "order_num": 5, "year_start": 553, "year_end": 553, "location": "Constantinople",
        "convoking_pope_or_emperor": "Emperor Justinian I / Pope Vigilius",
        "confirming_pope": "Pope Vigilius",
        "new_advent_url": "https://www.newadvent.org/cathen/04308b.htm",
        "dogmatic_definitions_en": "Condemned the 'Three Chapters' (writings of Theodore of Mopsuestia, Theodoret of Cyrus, and Ibas of Edessa) to reconcile Monophysites and uphold Chalcedon.",
        "dogmatic_definitions_vi": "Lên án 'Ba Chương' (các tác phẩm của Theodore xứ Mopsuestia, Theodoret xứ Cyrus và Ibas xứ Edessa) để tái lập hiệp nhất và củng cố công đồng Chalcedon.",
        "summary_en": "Clarified the Christological definitions of Chalcedon and condemned Origenist errors.",
        "summary_vi": "Làm sáng tỏ các định tín Kitô học của Chalcedon và lên án các sai lầm của phái Origen.",
        "primary_sources": ["Mansi, Collectio Conciliorum IX", "Catholic Encyclopedia (1913) IV:308"]
    },
    {
        "council_id": "ce-council-06-constantinople-iii",
        "council_name_en": "Third Council of Constantinople (Constantinople III)",
        "council_name_vi": "Công đồng Chung Constantinople III",
        "order_num": 6, "year_start": 680, "year_end": 681, "location": "Constantinople (Imperial Palace)",
        "convoking_pope_or_emperor": "Emperor Constantine IV / Pope Saint Agatho",
        "confirming_pope": "Pope Saint Leo II",
        "new_advent_url": "https://www.newadvent.org/cathen/04310a.htm",
        "dogmatic_definitions_en": "Defined that Christ possesses two natural wills (divine and human) and two natural operations, perfectly harmonized without opposition (condemnation of Monothelitism).",
        "dogmatic_definitions_vi": "Định tín Chúa Kitô có hai ý chí tự nhiên (ý chí thần linh và ý chí nhân loại) cùng hai năng quyền hoạt động hài hòa hoàn hảo (lên án thuyết Đơn ý - Monothelitism).",
        "summary_en": "Upheld Pope Agatho's letter declaring that Christ's human will freely yielded to His divine will, securing authentic human moral agency in redemption.",
        "summary_vi": "Chuẩn nhận thư của Đức Agathô xác quyết ý chí nhân loại của Chúa Kitô tự do vâng thuận ý chí thần linh, bảo đảm công nghiệp cứu chuộc nhân loại.",
        "primary_sources": ["Pope St. Agatho, Epistola ad Imperatorem", "Mansi, Collectio Conciliorum XI", "Catholic Encyclopedia (1913) IV:310"]
    },
    {
        "council_id": "ce-council-07-nicaea-ii",
        "council_name_en": "Second Council of Nicaea (Nicaea II)",
        "council_name_vi": "Công đồng Chung Nicaea II",
        "order_num": 7, "year_start": 787, "year_end": 787, "location": "Nicaea (Hagia Sophia Basilica)",
        "convoking_pope_or_emperor": "Empress Irene / Pope Adrian I",
        "confirming_pope": "Pope Adrian I",
        "new_advent_url": "https://www.newadvent.org/cathen/11045a.htm",
        "dogmatic_definitions_en": "Restored and justified the veneration (Dulia / Proskynesis) of sacred icons and images of Christ, the Mother of God, angels, and saints, distinguishing it from adoration (Latria) due to God alone.",
        "dogmatic_definitions_vi": "Phục hồi và bảo vệ việc tôn kính (Dulia) các ảnh tượng thánh của Chúa Kitô, Đức Mẹ, các thiên thần và các thánh, phân biệt rõ với sự tôn thờ (Latria) chỉ dành riêng cho Thiên Chúa.",
        "summary_en": "Defeated the violent Iconoclast heresy, proving that since the Word became true Flesh, visible sacred art is a legitimate proclamation of the Incarnation.",
        "summary_vi": "Đánh bại phong trào bài trừ ảnh tượng (Iconoclasm), minh chứng rằng vì Ngôi Lời đã Nhập Thể làm người thực sự nên nghệ thuật thánh hữu hình là lời tuyên xưng mầu nhiệm Nhập Thể.",
        "primary_sources": ["St. John Damascene, Apologiae contra Iconoclastas", "Mansi, Collectio Conciliorum XII-XIII", "Catholic Encyclopedia (1913) XI:45"]
    },
    {
        "council_id": "ce-council-08-constantinople-iv",
        "council_name_en": "Fourth Council of Constantinople (Constantinople IV)",
        "council_name_vi": "Công đồng Chung Constantinople IV",
        "order_num": 8, "year_start": 869, "year_end": 870, "location": "Constantinople",
        "convoking_pope_or_emperor": "Emperor Basil I / Pope Adrian II",
        "confirming_pope": "Pope Adrian II",
        "new_advent_url": "https://www.newadvent.org/cathen/04310b.htm",
        "dogmatic_definitions_en": "Deposed Photius from the Patriarchate of Constantinople, restored Patriarch Ignatius, and affirmed papal supremacy in judicial appeals.",
        "dogmatic_definitions_vi": "Cách chức Photius khỏi Tòa Thượng phụ Constantinople, phục hồi Thượng phụ Ignatius và khẳng định quyền tối thượng xét xử của Tòa Thánh Rôma.",
        "summary_en": "The final ecumenical council held in the Byzantine East, affirming the primacy of the Roman See.",
        "summary_vi": "Công đồng chung cuối cùng được tổ chức tại Đông Phương Byzantine, củng cố quyền tối thượng của Tòa Thánh Rôma.",
        "primary_sources": ["Mansi, Collectio Conciliorum XVI", "Catholic Encyclopedia (1913) IV:310"]
    },
    {
        "council_id": "ce-council-09-lateran-i",
        "council_name_en": "First Council of the Lateran (Lateran I)",
        "council_name_vi": "Công đồng Chung Latêranô I",
        "order_num": 9, "year_start": 1123, "year_end": 1123, "location": "Archbasilica of St. John Lateran, Rome",
        "convoking_pope_or_emperor": "Pope Callixtus II",
        "confirming_pope": "Pope Callixtus II",
        "new_advent_url": "https://www.newadvent.org/cathen/09014a.htm",
        "dogmatic_definitions_en": "Confirmed the Concordat of Worms (1122), ending the Investiture Controversy by prohibiting lay rulers from conferring ecclesiastical rings and croziers; outlawed simony and clerical concubinage.",
        "dogmatic_definitions_vi": "Chuẩn nhận Hiệp ước Worms (1122), chấm dứt Tranh chấp Quyền Tấn phong giáo sĩ; nghiêm cấm buôn thần bán thánh (simony) và bảo vệ bậc sống độc thân linh mục.",
        "summary_en": "First ecumenical council celebrated in the West, establishing the liberty of the Church (Libertas Ecclesiae).",
        "summary_vi": "Công đồng chung đầu tiên được cử hành tại Tây Phương, xác lập quyền tự do thiêng liêng của Hội Thánh.",
        "primary_sources": ["Mansi, Collectio Conciliorum XXI", "Catholic Encyclopedia (1913) IX:14"]
    },
    {
        "council_id": "ce-council-10-lateran-ii",
        "council_name_en": "Second Council of the Lateran (Lateran II)",
        "council_name_vi": "Công đồng Chung Latêranô II",
        "order_num": 10, "year_start": 1139, "year_end": 1139, "location": "Archbasilica of St. John Lateran, Rome",
        "convoking_pope_or_emperor": "Pope Innocent II",
        "confirming_pope": "Pope Innocent II",
        "new_advent_url": "https://www.newadvent.org/cathen/09014b.htm",
        "dogmatic_definitions_en": "Healed the papal schism of Antipope Anacletus II; enacted strict canons enforcing clerical celibacy and forbidding usury.",
        "dogmatic_definitions_vi": "Hàn gắn cuộc ly giáo của Ngụy Giáo hoàng Anacletus II; ban hành các giáo luật nghiêm ngặt về độc thân giáo sĩ và cấm cho vay nặng lãi.",
        "summary_en": "Gathered over a thousand prelates in Rome to restore discipline and unity under Pope Innocent II.",
        "summary_vi": "Quy tụ hơn một ngàn giám mục tại Rôma để tái lập kỷ luật và sự hiệp nhất dưới sự lãnh đạo của Đức Innocent II.",
        "primary_sources": ["Mansi, Collectio Conciliorum XXI", "Catholic Encyclopedia (1913) IX:14"]
    },
    {
        "council_id": "ce-council-11-lateran-iii",
        "council_name_en": "Third Council of the Lateran (Lateran III)",
        "council_name_vi": "Công đồng Chung Latêranô III",
        "order_num": 11, "year_start": 1179, "year_end": 1179, "location": "Archbasilica of St. John Lateran, Rome",
        "convoking_pope_or_emperor": "Pope Alexander III",
        "confirming_pope": "Pope Alexander III",
        "new_advent_url": "https://www.newadvent.org/cathen/09014c.htm",
        "dogmatic_definitions_en": "Established the two-thirds majority rule for papal conclaves (Licet de Evitanda Discordia); condemned the Cathar/Albigensian heresy and mandated free cathedral schools for poor scholars.",
        "dogmatic_definitions_vi": "Quy định nguyên tắc đa số 2/3 phiếu bầu trong Mật nghị bầu Giáo hoàng; lên án lạc giáo Albigenses và yêu cầu mở trường miễn phí cho học sinh nghèo.",
        "summary_en": "Eliminated imperial interference in papal elections and reformed cathedral education.",
        "summary_vi": "Chấm dứt sự can thiệp của hoàng quyền vào bầu cử giáo hoàng và cải cách nền giáo dục tại các nhà thờ chính tòa.",
        "primary_sources": ["Mansi, Collectio Conciliorum XXII", "Catholic Encyclopedia (1913) IX:14"]
    },
    {
        "council_id": "ce-council-12-lateran-iv",
        "council_name_en": "Fourth Council of the Lateran (Lateran IV)",
        "council_name_vi": "Công đồng Chung Latêranô IV",
        "order_num": 12, "year_start": 1215, "year_end": 1215, "location": "Archbasilica of St. John Lateran, Rome",
        "convoking_pope_or_emperor": "Pope Innocent III",
        "confirming_pope": "Pope Innocent III",
        "new_advent_url": "https://www.newadvent.org/cathen/09014d.htm",
        "dogmatic_definitions_en": "Dogmatically defined Transubstantiation (Transubstantiatio); mandated the annual Easter Duty (Confession and Holy Communion at least once a year); formulated confession seal canons.",
        "dogmatic_definitions_vi": "Định tín Tín điều Biến đổi Bản thể (Transubstantiatio) trong Bí tích Thánh Thể; quy định việc Xưng tội và Rước lễ Mùa Phục Sinh hàng năm; thiết lập ấn tín tòa giải tội.",
        "summary_en": "The crowning achievement of medieval conciliar history under Innocent III, producing 70 definitive constitutions across dogmatic, liturgical, and moral theology.",
        "summary_vi": "Đỉnh cao của lịch sử công đồng thời Trung Cổ dưới triều Đức Innocent III, ban hành 70 hiến chế nền tảng về tín lý, phụng vụ và luân lý.",
        "primary_sources": ["Lateran IV Constitutions (1215)", "Mansi, Collectio Conciliorum XXII", "Catholic Encyclopedia (1913) IX:14"]
    },
    {
        "council_id": "ce-council-13-lyon-i",
        "council_name_en": "First Council of Lyon (Lyon I)",
        "council_name_vi": "Công đồng Chung Lyon I",
        "order_num": 13, "year_start": 1245, "year_end": 1245, "location": "Lyon Cathedral, France",
        "convoking_pope_or_emperor": "Pope Innocent IV",
        "confirming_pope": "Pope Innocent IV",
        "new_advent_url": "https://www.newadvent.org/cathen/09476a.htm",
        "dogmatic_definitions_en": "Deposed Holy Roman Emperor Frederick II for perjury, sacrilege, and heresy; directed aid to the beleaguered Holy Land.",
        "dogmatic_definitions_vi": "Phế truất Hoàng đế Frederick II vì tội bội thề, xúc phạm sự thánh và lạc giáo; kêu gọi viện trợ cho Thánh Địa.",
        "summary_en": "Affirmed the spiritual supremacy of the Papacy over secular monarchies and mandated the wearing of red hats for Cardinals.",
        "summary_vi": "Khẳng định quyền bính thiêng liêng tối thượng của Tòa Thánh trên các vương quyền và quy định mũ đỏ cho các Hồng y.",
        "primary_sources": ["Mansi, Collectio Conciliorum XXIII", "Catholic Encyclopedia (1913) IX:476"]
    },
    {
        "council_id": "ce-council-14-lyon-ii",
        "council_name_en": "Second Council of Lyon (Lyon II)",
        "council_name_vi": "Công đồng Chung Lyon II",
        "order_num": 14, "year_start": 1274, "year_end": 1274, "location": "Lyon Cathedral, France",
        "convoking_pope_or_emperor": "Blessed Pope Gregory X",
        "confirming_pope": "Blessed Pope Gregory X",
        "new_advent_url": "https://www.newadvent.org/cathen/09476b.htm",
        "dogmatic_definitions_en": "Defined that the Holy Spirit proceeds eternally from Father and Son as from one principle and single spiration (Filioque); instituted the locked Conclave system (Ubi Periculum).",
        "dogmatic_definitions_vi": "Định tín Chúa Thánh Thần nhiệm xuất đời đời từ Chúa Cha và Chúa Con như từ một nguyên lý duy nhất (Filioque); thiết lập quy chế Mật nghị cấm phòng (Ubi Periculum).",
        "summary_en": "Achieved a temporary reunion with the Eastern Orthodox Church; attended by St. Bonaventure (who died during the council) while St. Thomas Aquinas died en route.",
        "summary_vi": "Đạt được thỏa ước tái hiệp nhất ngắn ngủi với Chính Thống giáo Đông Phương; Thánh Bonaventura qua đời trong công đồng, còn Thánh Tôma Aquinô qua đời trên đường tới dự.",
        "primary_sources": ["Constitutiones Concilii Lugdunensis II", "Mansi, Collectio Conciliorum XXIV", "Catholic Encyclopedia (1913) IX:476"]
    },
    {
        "council_id": "ce-council-15-vienne",
        "council_name_en": "Council of Vienne",
        "council_name_vi": "Công đồng Chung Vienne",
        "order_num": 15, "year_start": 1311, "year_end": 1312, "location": "Vienne Cathedral, France",
        "convoking_pope_or_emperor": "Pope Clement V",
        "confirming_pope": "Pope Clement V",
        "new_advent_url": "https://www.newadvent.org/cathen/15423a.htm",
        "dogmatic_definitions_en": "Defined that the rational soul is intrinsically the form of the human body (Anima rationalis est forma corporis); suppressed the Knights Templar; condemned Beguine and Beghard quietism.",
        "dogmatic_definitions_vi": "Định tín linh hồn có lý trí chính là mô thể nội tại của thân xác con người (Anima forma corporis); giải thể Dòng Hiệp Sĩ Đền Thờ; lên án lạc giáo Tĩnh lặng.",
        "summary_en": "Presided by the first Avignon Pope, Vienne produced critical metaphysical definitions on human nature and moral theology.",
        "summary_vi": "Dưới sự chủ tọa của vị Giáo hoàng Avignon đầu tiên, Vienne ban hành định tín siêu hình học sâu sắc về bản tính con người và thần học luân lý.",
        "primary_sources": ["Clementinae (Corpus Juris Canonici)", "Mansi, Collectio Conciliorum XXV", "Catholic Encyclopedia (1913) XV:423"]
    },
    {
        "council_id": "ce-council-16-constance",
        "council_name_en": "Council of Constance",
        "council_name_vi": "Công đồng Chung Constance",
        "order_num": 16, "year_start": 1414, "year_end": 1418, "location": "Constance Cathedral, Germany",
        "convoking_pope_or_emperor": "Emperor Sigismund / Pope Gregory XII",
        "confirming_pope": "Pope Martin V",
        "new_advent_url": "https://www.newadvent.org/cathen/04288a.htm",
        "dogmatic_definitions_en": "Ended the Great Western Schism (3 rival claimants) with the resignation of Pope Gregory XII and election of Pope Martin V; condemned errors of John Wycliffe and Jan Hus.",
        "dogmatic_definitions_vi": "Chấm dứt Đại Ly Giáo Tây Phương qua việc Đức Grêgôriô XII tự nguyện từ nhiệm và bầu chọn Đức Martinô V; lên án các sai lầm của John Wycliffe và Jan Hus.",
        "summary_en": "Restored universal papal legitimacy to the Catholic Church and resolved forty years of ecclesial division.",
        "summary_vi": "Khôi phục tính hợp pháp giáo hoàng phổ quát cho Hội Thánh Công Giáo và giải quyết bốn mươi năm chia rẽ giáo hội.",
        "primary_sources": ["Mansi, Collectio Conciliorum XXVII-XXVIII", "Catholic Encyclopedia (1913) IV:288"]
    },
    {
        "council_id": "ce-council-17-basel-ferrara-florence",
        "council_name_en": "Council of Basel-Ferrara-Florence",
        "council_name_vi": "Công đồng Chung Florence",
        "order_num": 17, "year_start": 1431, "year_end": 1445, "location": "Basel / Ferrara / Florence / Rome",
        "convoking_pope_or_emperor": "Pope Eugene IV",
        "confirming_pope": "Pope Eugene IV",
        "new_advent_url": "https://www.newadvent.org/cathen/06111a.htm",
        "dogmatic_definitions_en": "Proclaimed the Bull of Union with the Greeks (Laetentur Caeli), defining Papal Primacy, the Filioque, Purgatory, and the validity of azyme vs. leavened bread; promulgated Cantate Domino for the Copts.",
        "dogmatic_definitions_vi": "Ban hành Tông sắc Hiệp nhất Laetentur Caeli, định tín Quyền Tối Thượng Giáo Hoàng, Tín điều Filioque, Luyện Ngục và giá trị của Bánh Không Men; ban hành sắc chỉ Cantate Domino cho Giáo hội Coptic.",
        "summary_en": "Celebrated in Florence under Eugene IV with Byzantine Emperor John VIII Palaiologos and Patriarch Joseph II, achieving historical reconciliation.",
        "summary_vi": "Cử hành tại Florence dưới thời Đức Eugene IV cùng Hoàng đế Byzantine John VIII và Thượng phụ Joseph II, đạt được sự hòa giải lịch sử giữa Đông và Tây Phương.",
        "primary_sources": ["Bull Laetentur Caeli (1439)", "Mansi, Collectio Conciliorum XXXI", "Catholic Encyclopedia (1913) VI:111"]
    },
    {
        "council_id": "ce-council-18-lateran-v",
        "council_name_en": "Fifth Council of the Lateran (Lateran V)",
        "council_name_vi": "Công đồng Chung Latêranô V",
        "order_num": 18, "year_start": 1512, "year_end": 1517, "location": "Archbasilica of St. John Lateran, Rome",
        "convoking_pope_or_emperor": "Pope Julius II / Pope Leo X",
        "confirming_pope": "Pope Leo X",
        "new_advent_url": "https://www.newadvent.org/cathen/09015a.htm",
        "dogmatic_definitions_en": "Defined the immortality and individuality of the human soul against Neo-Averroism (Apostolici Regiminis); regulated printing of religious books.",
        "dogmatic_definitions_vi": "Định tín tính bất tử và độc nhất của từng linh hồn con người chống lại thuyết Tân-Averroes (Apostolici Regiminis); kiểm duyệt in ấn sách tôn giáo.",
        "summary_en": "Pre-Reformation reform council addressing curial discipline, ending just months before Martin Luther posted his 95 theses.",
        "summary_vi": "Công đồng cải cách tiền Kháng Cách bàn về kỷ luật giáo triều, bế mạc chỉ vài tháng trước khi Martin Luther công bố 95 luận đề.",
        "primary_sources": ["Bull Apostolici Regiminis (1513)", "Mansi, Collectio Conciliorum XXXII", "Catholic Encyclopedia (1913) IX:15"]
    },
    {
        "council_id": "ce-council-19-trent",
        "council_name_en": "Council of Trent",
        "council_name_vi": "Công đồng Chung Trentô",
        "order_num": 19, "year_start": 1545, "year_end": 1563, "location": "Trent and Bologna, Northern Italy",
        "convoking_pope_or_emperor": "Pope Paul III / Pope Julius III / Pope Pius IV",
        "confirming_pope": "Pope Pius IV (Benedictus Deus, 1564)",
        "new_advent_url": "https://www.newadvent.org/cathen/15030c.htm",
        "dogmatic_definitions_en": "Definitively fixed the 73-book Biblical Canon, the 7 Sacraments, the sacrificial nature of the Holy Mass, the Catholic doctrine of Justification by grace through faith animated by charity, Purgatory, and veneration of saints; established seminary formation systems.",
        "dogmatic_definitions_vi": "Xác định quy điển Kinh Thánh 73 cuốn, 7 Bí tích, bản chất hy tế của Thánh Lễ, đạo lý Công giáo về Sự Công Chính Hóa nhờ ân sủng qua đức tin hành động trong đức ái, Luyện Ngục và tôn kính các thánh; thiết lập hệ thống chủng viện đào tạo linh mục.",
        "summary_en": "The monumental Counter-Reformation council spanning 25 sessions across 18 years that revitalized the doctrine, liturgy, and spiritual discipline of the global Catholic Church.",
        "summary_vi": "Đại công đồng Cải Tổ Công Giáo kéo dài 25 khóa họp trong 18 năm, làm sống lại toàn diện tín lý, phụng vụ và kỷ luật tâm linh của Hội Thánh hoàn vũ.",
        "primary_sources": ["Canones et Decreta Concilii Tridentini (1564)", "Catechismus Romanus (1566)", "Catholic Encyclopedia (1913) XV:30"]
    },
    {
        "council_id": "ce-council-20-vatican-i",
        "council_name_en": "First Vatican Council (Vatican I)",
        "council_name_vi": "Công đồng Chung Vatican I",
        "order_num": 20, "year_start": 1869, "year_end": 1870, "location": "St. Peter's Basilica, Vatican City",
        "convoking_pope_or_emperor": "Blessed Pope Pius IX",
        "confirming_pope": "Blessed Pope Pius IX",
        "new_advent_url": "https://www.newadvent.org/cathen/15303a.htm",
        "dogmatic_definitions_en": "Dogmatically defined Papal Infallibility (Pastor Aeternus) when the Pope speaks ex cathedra on faith and morals; affirmed the harmonious knowability of God through natural reason and supernatural revelation (Dei Filius).",
        "dogmatic_definitions_vi": "Định tín Ơn Bất Khả Ngộ của Giáo Hoàng (Pastor Aeternus) khi ngài tuyên bố 'ex cathedra' về đức tin và luân lý; khẳng định sự hòa hợp giữa lý trí tự nhiên và mặc khải siêu nhiên trong việc nhận biết Thiên Chúa (Dei Filius).",
        "summary_en": "Interrupted by the Franco-Prussian War and the capture of Rome in September 1870 after defining two essential dogmatic constitutions.",
        "summary_vi": "Bị gián đoạn bởi Chiến tranh Pháp-Phổ và sự kiện quân đội Ý tiến vào Rôma tháng 9/1870 sau khi ban hành hai hiến chế tín lý nền tảng.",
        "primary_sources": ["Dogmatic Constitutions Dei Filius & Pastor Aeternus", "Mansi, Collectio Conciliorum XLIX-LIII", "Catholic Encyclopedia (1913) XV:303"]
    },
    {
        "council_id": "ce-council-21-vatican-ii",
        "council_name_en": "Second Vatican Council (Vatican II)",
        "council_name_vi": "Công đồng Chung Vatican II",
        "order_num": 21, "year_start": 1962, "year_end": 1965, "location": "St. Peter's Basilica, Vatican City",
        "convoking_pope_or_emperor": "Saint Pope John XXIII / Saint Pope Paul VI",
        "confirming_pope": "Saint Pope Paul VI",
        "new_advent_url": "https://www.newadvent.org/cathen/15303a.htm",
        "dogmatic_definitions_en": "Promulgated 16 conciliar documents including 4 Constitutions: Sacrosanctum Concilium (Liturgy), Lumen Gentium (The Church as Mystical Body / People of God), Dei Verbum (Divine Revelation), and Gaudium et Spes (The Church in the Modern World).",
        "dogmatic_definitions_vi": "Ban hành 16 văn kiện công đồng gồm 4 Hiến chế nền tảng: Phụng vụ Thánh (Sacrosanctum Concilium), Ánh sáng Muôn Dân (Lumen Gentium), Lời Chúa (Dei Verbum) và Vui Mừng & Hy Vọng (Gaudium et Spes).",
        "summary_en": "Called by St. John XXIII to achieve pastoral renewal (Aggiornamento) and articulate the Catholic message to contemporary humanity in the modern era.",
        "summary_vi": "Được Thánh Gioan XXIII triệu tập nhằm thực hiện cuộc canh tân mục vụ (Aggiornamento) và loan báo sứ điệp Kitô giáo cho con người thời đại mới.",
        "primary_sources": ["Acta Synodalia Sacrosancti Concilii Oecumenici Vaticani II", "Vatican II Documents (Vatican.va)"]
    }
]

# 3. Historic Papal Encyclicals Catalog
ENCYCLICALS_DATA: List[Dict[str, Any]] = [
    {
        "encyclical_id": "ce-enc-1854-ineffabilis-deus",
        "latin_incipit": "Ineffabilis Deus",
        "title_en": "Apostolic Constitution Ineffabilis Deus (The Immaculate Conception)",
        "title_vi": "Tông hiến Ineffabilis Deus (Định tín Đức Mẹ Vô Nhiễm Nguyên Tội)",
        "promulgating_pope": "Blessed Pope Pius IX",
        "promulgation_date": "1854-12-08",
        "year": 1854,
        "topic_category": "Marian Dogma",
        "new_advent_or_vatican_url": "https://www.newadvent.org/cathen/07674d.htm",
        "summary_en": "Solemn ex cathedra dogmatic definition that the Blessed Virgin Mary was preserved exempt from all stain of original sin from the first instant of her conception.",
        "summary_vi": "Định tín bất khả ngộ ex cathedra rằng Đức Trinh Nữ Maria được gìn giữ khỏi mọi vết nhơ tội nguyên tổ ngay từ giây phút đầu thai đầu tiên.",
        "key_doctrines": ["Immaculate Conception", "Preservative Redemption", "Mary as New Eve"]
    },
    {
        "encyclical_id": "ce-enc-1864-quanta-cura",
        "latin_incipit": "Quanta Cura & Syllabus of Errors",
        "title_en": "Encyclical Quanta Cura and the Syllabus of Errors",
        "title_vi": "Thông điệp Quanta Cura và Bản Danh Mục các Lỗi Lầm (Syllabus Errorum)",
        "promulgating_pope": "Blessed Pope Pius IX",
        "promulgation_date": "1864-12-08",
        "year": 1864,
        "topic_category": "Social & Moral Errors",
        "new_advent_or_vatican_url": "https://www.newadvent.org/cathen/14368b.htm",
        "summary_en": "Condemned radical secularism, state absolutism, religious indifferentism, and philosophical rationalism.",
        "summary_vi": "Lên án chủ nghĩa thế tục cực đoan, thuyết nhà nước độc tôn, thái độ dửng dưng tôn giáo và chủ nghĩa duy lý triết học.",
        "key_doctrines": ["Primacy of Supernatural Truth", "Limits of Civil Authority", "Critique of Secular Indifferentism"]
    },
    {
        "encyclical_id": "ce-enc-1879-aeterni-patris",
        "latin_incipit": "Aeterni Patris",
        "title_en": "Encyclical Aeterni Patris (On the Restoration of Christian Philosophy)",
        "title_vi": "Thông điệp Aeterni Patris (Phục hưng Triết học Kitô giáo)",
        "promulgating_pope": "Pope Leo XIII",
        "promulgation_date": "1879-08-04",
        "year": 1879,
        "topic_category": "Philosophy & Theology",
        "new_advent_or_vatican_url": "https://www.newadvent.org/cathen/01177a.htm",
        "summary_en": "Mandated the revival and central study of the Scholastic philosophical system of Saint Thomas Aquinas (Thomism) in all Catholic seminaries and universities.",
        "summary_vi": "Chỉ thị phục hưng và lấy hệ thống triết học Kinh Viện của Thánh Tôma Aquinô (Thuyết Tôma) làm trung tâm nghiên cứu tại các chủng viện và đại học Công giáo.",
        "key_doctrines": ["Thomistic Realism", "Harmony of Faith and Natural Reason", "Defense of Objective Truth"]
    },
    {
        "encyclical_id": "ce-enc-1891-rerum-novarum",
        "latin_incipit": "Rerum Novarum",
        "title_en": "Encyclical Rerum Novarum (On Capital and Labor)",
        "title_vi": "Thông điệp Rerum Novarum (Tân Sự - Về Vấn Đề Công Nhân và Tư Bản)",
        "promulgating_pope": "Pope Leo XIII",
        "promulgation_date": "1891-05-15",
        "year": 1891,
        "topic_category": "Catholic Social Teaching",
        "new_advent_or_vatican_url": "https://www.newadvent.org/cathen/12783a.htm",
        "summary_en": "Foundational charter of modern Catholic Social Teaching defending private property, living wages, the right of workers to form unions, and rejecting both unbridled laissez-faire capitalism and atheistic socialism.",
        "summary_vi": "Hiến chương nền tảng của Học Thuyết Xã Hội Công Giáo hiện đại, bảo vệ quyền tư hữu, mức lương xứng đáng, quyền thành lập công đoàn và bác bỏ cả tư bản hoang dã lẫn chủ nghĩa xã hội vô thần.",
        "key_doctrines": ["Dignity of Human Labor", "Universal Destination of Goods", "Right of Association", "Subsidiarity"]
    },
    {
        "encyclical_id": "ce-enc-1907-pascendi-dominici-gregis",
        "latin_incipit": "Pascendi Dominici Gregis",
        "title_en": "Encyclical Pascendi Dominici Gregis (On the Doctrines of the Modernists)",
        "title_vi": "Thông điệp Pascendi Dominici Gregis (Lên Án Thuyết Tân Thời - Modernism)",
        "promulgating_pope": "Saint Pope Pius X",
        "promulgation_date": "1907-09-08",
        "year": 1907,
        "topic_category": "Dogmatic Defense",
        "new_advent_or_vatican_url": "https://www.newadvent.org/cathen/10415a.htm",
        "summary_en": "Masterful systematic exposure and condemnation of Modernism as the 'synthesis of all heresies', defending divine revelation, dogma, and objective historical truth.",
        "summary_vi": "Phân tích có hệ thống và lên án thuyết Tân Thời như là 'sự tổng hợp của mọi bè rối', bảo vệ chân lý mặc khải, các tín điều và tính lịch sử khách quan của đức tin.",
        "key_doctrines": ["Immutability of Dogma", "Objective Revelation", "Danger of Vital Immanence"]
    },
    {
        "encyclical_id": "ce-enc-1925-quas-primas",
        "latin_incipit": "Quas Primas",
        "title_en": "Encyclical Quas Primas (On the Kingship of Christ)",
        "title_vi": "Thông điệp Quas Primas (Về Vương Quyền Chúa Kitô)",
        "promulgating_pope": "Pope Pius XI",
        "promulgation_date": "1925-12-11",
        "year": 1925,
        "topic_category": "Christology & Liturgy",
        "new_advent_or_vatican_url": "https://www.vatican.va/content/pius-xi/en/encyclicals/documents/hf_p-xi_enc_11121925_quas-primas.html",
        "summary_en": "Instituted the Solemnity of Christ the King (Christus Rex), affirming Christ's sovereign authority over individuals, families, nations, and human society.",
        "summary_vi": "Thiết lập Đại Lễ Chúa Kitô Vua Vũ Trụ (Christus Rex), khẳng định quyền vương đế tối thượng của Chúa Kitô trên các cá nhân, gia đình, quốc gia và xã hội loài người.",
        "key_doctrines": ["Social Kingship of Christ", "Universal Sovereignty", "Reign of Peace"]
    },
    {
        "encyclical_id": "ce-enc-1943-mystici-corporis",
        "latin_incipit": "Mystici Corporis Christi",
        "title_en": "Encyclical Mystici Corporis Christi (On the Mystical Body of Christ)",
        "title_vi": "Thông điệp Mystici Corporis Christi (Về Nhiệm Thể Chúa Kitô)",
        "promulgating_pope": "Venerable Pope Pius XII",
        "promulgation_date": "1943-06-29",
        "year": 1943,
        "topic_category": "Ecclesiology",
        "new_advent_or_vatican_url": "https://www.vatican.va/content/pius-xii/en/encyclicals/documents/hf_p-xii_enc_29061943_mystici-corporis-christi.html",
        "summary_en": "Articulated the theological doctrine of the Catholic Church as the Mystical Body of Christ with Christ as its divine Head and the Holy Spirit as its soul.",
        "summary_vi": "Minh giải đạo lý thần học sâu xa về Hội Thánh Công Giáo là Thân Thể Mầu Nhiệm của Chúa Kitô với Chúa Kitô là Đầu và Chúa Thánh Thần là linh hồn.",
        "key_doctrines": ["The Church as Mystical Body", "Communion of Members", "Holy Spirit as Soul of the Church"]
    },
    {
        "encyclical_id": "ce-enc-1947-mediator-dei",
        "latin_incipit": "Mediator Dei",
        "title_en": "Encyclical Mediator Dei (On the Sacred Liturgy)",
        "title_vi": "Thông điệp Mediator Dei (Về Phụng Vụ Thánh)",
        "promulgating_pope": "Venerable Pope Pius XII",
        "promulgation_date": "1947-11-20",
        "year": 1947,
        "topic_category": "Sacred Liturgy",
        "new_advent_or_vatican_url": "https://www.vatican.va/content/pius-xii/en/encyclicals/documents/hf_p-xii_enc_20111947_mediator-dei.html",
        "summary_en": "Seminal encyclical on the nature of Christian worship, defining liturgy as the continuous public prayer of Christ the High Priest and His Mystical Body.",
        "summary_vi": "Thông điệp nền tảng về bản chất sự thờ phượng Kitô giáo, định nghĩa phụng vụ là lời cầu nguyện công khai liên lỉ của Chúa Kitô Thượng Tế và Nhiệm Thể Người.",
        "key_doctrines": ["Liturgy as Priesthood of Christ", "Active Interior Participation", "Eucharistic Sacrifice"]
    },
    {
        "encyclical_id": "ce-enc-1950-munificentissimus-deus",
        "latin_incipit": "Munificentissimus Deus",
        "title_en": "Apostolic Constitution Munificentissimus Deus (The Assumption)",
        "title_vi": "Tông hiến Munificentissimus Deus (Định tín Đức Mẹ Hồn Xác Lên Trời)",
        "promulgating_pope": "Venerable Pope Pius XII",
        "promulgation_date": "1950-11-01",
        "year": 1950,
        "topic_category": "Marian Dogma",
        "new_advent_or_vatican_url": "https://www.vatican.va/content/pius-xii/en/apost_constitutions/documents/hf_p-xii_apc_19501101_munificentissimus-deus.html",
        "summary_en": "Infallible ex cathedra dogmatic definition that Mary, having completed her earthly course, was assumed body and soul into heavenly glory.",
        "summary_vi": "Định tín bất khả ngộ ex cathedra rằng Đức Maria sau khi hoàn tất cuộc đời trần thế đã được rước cả hồn lẫn xác vào vinh quang thiên quốc.",
        "key_doctrines": ["Bodily Assumption", "Victory over Death", "Queen of Heaven"]
    },
    {
        "encyclical_id": "ce-enc-1968-humanae-vitae",
        "latin_incipit": "Humanae Vitae",
        "title_en": "Encyclical Humanae Vitae (On the Regulation of Birth)",
        "title_vi": "Thông điệp Humanae Vitae (Sự Sống Con Người - Về Việc Truyền Sinh)",
        "promulgating_pope": "Saint Pope Paul VI",
        "promulgation_date": "1968-07-25",
        "year": 1968,
        "topic_category": "Moral Theology & Marriage",
        "new_advent_or_vatican_url": "https://www.vatican.va/content/paul-vi/en/encyclicals/documents/hf_p-vi_enc_25071968_humanae-vitae.html",
        "summary_en": "Prophetic defense of the inseparable unitive and procreative meanings of the marital act, affirming the sanctity of human life from conception and prohibiting artificial contraception.",
        "summary_vi": "Bản tuyên xưng mang tính ngôn sứ bảo vệ sự liên kết bất khả phân giữa ý nghĩa kết hợp và truyền sinh của hành vi vợ chồng, bảo vệ sự thánh thiêng của sự sống từ khi thụ thai.",
        "key_doctrines": ["Unitive and Procreative Inseparability", "Sanctity of Marital Love", "Responsible Parenthood"]
    },
    {
        "encyclical_id": "ce-enc-1993-veritatis-splendor",
        "latin_incipit": "Veritatis Splendor",
        "title_en": "Encyclical Veritatis Splendor (The Splendor of Truth)",
        "title_vi": "Thông điệp Veritatis Splendor (Rạng Ngời Chân Lý)",
        "promulgating_pope": "Saint Pope John Paul II",
        "promulgation_date": "1993-08-06",
        "year": 1993,
        "topic_category": "Moral Theology",
        "new_advent_or_vatican_url": "https://www.vatican.va/content/john-paul-ii/en/encyclicals/documents/hf_jp-ii_enc_06081993_veritatis-splendor.html",
        "summary_en": "Reaffirmed the existence of intrinsic moral evils (intrinsece malum) that are always wrong, rejecting moral relativism, proportionalism, and consequentialism.",
        "summary_vi": "Tái khẳng định sự hiện hữu của các hành vi tự bản chất là sự dữ luân lý (intrinsece malum) luôn luôn sai trái, bác bỏ thuyết tương đối luân lý và chủ nghĩa hậu quả.",
        "key_doctrines": ["Intrinsic Evil", "Universal Moral Law", "Freedom Rooted in Truth", "Martyrdom as Witness to Truth"]
    },
    {
        "encyclical_id": "ce-enc-1995-evangelium-vitae",
        "latin_incipit": "Evangelium Vitae",
        "title_en": "Encyclical Evangelium Vitae (The Gospel of Life)",
        "title_vi": "Thông điệp Evangelium Vitae (Tin Mừng Sự Sống)",
        "promulgating_pope": "Saint Pope John Paul II",
        "promulgation_date": "1995-03-25",
        "year": 1995,
        "topic_category": "Bioethics & Human Dignity",
        "new_advent_or_vatican_url": "https://www.vatican.va/content/john-paul-ii/en/encyclicals/documents/hf_jp-ii_enc_25031995_evangelium-vitae.html",
        "summary_en": "Definitive teaching upholding the inviolability of innocent human life against abortion, euthanasia, and assisted suicide, calling for a Culture of Life.",
        "summary_vi": "Giáo huấn xác quyết bảo vệ tính bất khả xâm phạm của sự sống con người vô tội chống lại nạn phá thai, an tử và tự sát có trợ giúp, kêu gọi xây dựng Nền Văn Minh Sự Sống.",
        "key_doctrines": ["Inviolability of Innocent Human Life", "Culture of Life vs Culture of Death", "Dignity of the Vulnerable"]
    },
    {
        "encyclical_id": "ce-enc-1998-fides-et-ratio",
        "latin_incipit": "Fides et Ratio",
        "title_en": "Encyclical Fides et Ratio (On Faith and Reason)",
        "title_vi": "Thông điệp Fides et Ratio (Đức Tin và Lý Trí)",
        "promulgating_pope": "Saint Pope John Paul II",
        "promulgation_date": "1998-09-14",
        "year": 1998,
        "topic_category": "Philosophy & Epistemology",
        "new_advent_or_vatican_url": "https://www.vatican.va/content/john-paul-ii/en/encyclicals/documents/hf_jp-ii_enc_14091998_fides-et-ratio.html",
        "summary_en": "Affirmed that faith and reason are 'like two wings on which the human spirit rises to the contemplation of truth', refuting nihilism and fideism.",
        "summary_vi": "Khẳng định đức tin và lý trí như 'hai cánh nâng tâm hồn con người vươn lên chiêm ngưỡng chân lý', bác bỏ thuyết hư vô và thuyết duy đức tin.",
        "key_doctrines": ["Two Wings of Truth", "Metaphysical Openness", "Vocation of Philosophy"]
    }
]


class CatholicEncyclopediaLinker:
    """Provides entity resolution and URL linking to Catholic Encyclopedia entries."""

    def __init__(self, index_data: Optional[Dict[str, Any]] = None):
        if index_data is None:
            index_data = self.build_index()
        self.index = index_data
        self.saints: List[Dict[str, Any]] = self.index.get("saints", [])
        self.councils: List[Dict[str, Any]] = self.index.get("councils", [])
        self.encyclicals: List[Dict[str, Any]] = self.index.get("encyclicals", [])

    @staticmethod
    def build_index() -> Dict[str, Any]:
        """Compiles full Catholic Encyclopedia entity index."""
        saints = [asdict(SaintEntity(**s)) for s in SAINTS_DATA]
        councils = [asdict(CouncilEntity(**c)) for c in COUNCILS_DATA]
        encyclicals = [asdict(EncyclicalEntity(**e)) for e in ENCYCLICALS_DATA]

        return {
            "schema_version": SCHEMA_VERSION,
            "curated_on": datetime.utcnow().strftime("%Y-%m-%d"),
            "source": "The Catholic Encyclopedia (1913 New Advent Edition) & Holy See Archives",
            "description_en": "Authoritative entity linker and reference index mapping Catholic saints, all 21 ecumenical councils, and major historic papal encyclicals to New Advent citations and bilingual summaries.",
            "description_vi": "Bộ liên kết thực thể và danh mục tham chiếu chuẩn mực ánh xạ các thánh, trọn bộ 21 công đồng chung và các thông điệp giáo hoàng lịch sử với New Advent và bản ngữ hóa song ngữ.",
            "statistics": {
                "total_saints": len(saints),
                "total_councils": len(councils),
                "total_encyclicals": len(encyclicals),
                "total_entities": len(saints) + len(councils) + len(encyclicals),
            },
            "saints": saints,
            "councils": councils,
            "encyclicals": encyclicals,
        }

    def link(self, query: str) -> List[Dict[str, Any]]:
        """Resolves any entity query across saints, councils, and encyclicals."""
        q = query.lower().strip()
        matches = []

        # Check saints
        for s in self.saints:
            searchable = f"{s['canonical_name']} {s['name_vi']} {s['era']}".lower()
            if q in searchable or any(q in part.lower() for part in s['canonical_name'].split()):
                matches.append({"type": "saint", "entity": s, "url": s["new_advent_url"]})

        # Check councils
        for c in self.councils:
            searchable = f"{c['council_name_en']} {c['council_name_vi']} {c['location']} {c['order_num']}".lower()
            if q in searchable or str(c["order_num"]) == q or str(c["year_start"]) == q:
                matches.append({"type": "council", "entity": c, "url": c["new_advent_url"]})

        # Check encyclicals
        for e in self.encyclicals:
            searchable = f"{e['latin_incipit']} {e['title_en']} {e['title_vi']} {e['promulgating_pope']}".lower()
            if q in searchable or str(e["year"]) == q:
                matches.append({"type": "encyclical", "entity": e, "url": e["new_advent_or_vatican_url"]})

        return matches

    def enrich_text(self, text: str) -> str:
        """Helper to tag recognized Catholic entities in text with New Advent URLs."""
        # Simple keyword matching for major saints & councils
        for c in self.councils:
            if c["council_name_en"] in text:
                text = text.replace(c["council_name_en"], f"[{c['council_name_en']}]({c['new_advent_url']})")
        return text


def main() -> None:
    parser = argparse.ArgumentParser(description="Catholic Encyclopedia Entity Linker & Index Generator.")
    parser.add_argument("--output", type=Path, default=INDEX_OUTPUT, help="Output JSON path")
    parser.add_argument("--link", type=str, help="Search or link an entity by name or topic")
    parser.add_argument("--councils", action="store_true", help="List all 21 Ecumenical Councils")
    parser.add_argument("--encyclicals", action="store_true", help="List Papal Encyclicals")
    parser.add_argument("--saints", action="store_true", help="List Major Saints")
    parser.add_argument("--verify", action="store_true", help="Verify index schema invariants")
    args = parser.parse_args()

    index = CatholicEncyclopediaLinker.build_index()
    linker = CatholicEncyclopediaLinker(index)

    if args.link:
        results = linker.link(args.link)
        print(f"Found {len(results)} matches for '{args.link}':")
        for r in results:
            ent = r["entity"]
            name = ent.get("canonical_name") or ent.get("council_name_en") or ent.get("latin_incipit")
            print(f"  • [{r['type'].upper()}] {name} -> {r['url']}")
        return

    if args.councils:
        print("All 21 Ecumenical Councils of the Catholic Church:")
        for c in index["councils"]:
            print(f"  {c['order_num']:2d}. {c['council_name_en']} ({c['year_start']}) - {c['new_advent_url']}")
        return

    if args.encyclicals:
        print("Historic Papal Encyclicals Index:")
        for e in index["encyclicals"]:
            print(f"  • {e['latin_incipit']} ({e['year']}, {e['promulgating_pope']}) - {e['new_advent_or_vatican_url']}")
        return

    if args.saints:
        print("Catholic Encyclopedia Major Saints Index:")
        for s in index["saints"]:
            print(f"  • {s['canonical_name']} ({s['era']}, {s['century']}) - {s['new_advent_url']}")
        return

    # Write output
    output_path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    stats = index["statistics"]
    print(f"Successfully generated Catholic Encyclopedia index at {output_path}")
    print(f"  Total Entities: {stats['total_entities']} ({stats['total_saints']} Saints, {stats['total_councils']} Councils, {stats['total_encyclicals']} Encyclicals)")

    if args.verify or True:
        assert output_path.exists(), "Output file missing!"
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["schema_version"] == SCHEMA_VERSION
        assert len(data["councils"]) == 21, f"Expected 21 councils, got {len(data['councils'])}"
        for c in data["councils"]:
            assert c["council_name_en"] and c["council_name_vi"] and c["new_advent_url"]
            assert c["dogmatic_definitions_en"] and c["dogmatic_definitions_vi"]
        for s in data["saints"]:
            assert s["canonical_name"] and s["name_vi"] and s["new_advent_url"]
            assert s["summary_en"] and s["summary_vi"]
        for e in data["encyclicals"]:
            assert e["latin_incipit"] and e["title_en"] and e["title_vi"]
            assert e["summary_en"] and e["summary_vi"]
        print("Verification OK: All 21 councils, saints, encyclicals, and bilingual fields verified 100%.")


if __name__ == "__main__":
    main()

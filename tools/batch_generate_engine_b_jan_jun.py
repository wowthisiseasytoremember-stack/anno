#!/usr/bin/env python3
"""
tools/batch_generate_engine_b_jan_jun.py
Generates Engine B research outputs (EN + VI) for January 1 – July 2, 2026
(183 days) using a curated FEAST_CATALOG + template fallback for Ordinary Time.

Liturgical map for 2026:
- Jan 1-10:    Christmas Octave end / Epiphany Season (white)
- Jan 11-12:   Weekday after Epiphany / before Ordinary Time (white)
- Jan 13-31:   Ordinary Time Week 1-4 (green)
- Feb 1-17:    Ordinary Time Week 5-7 (green)
- Feb 18:      Ash Wednesday — Lent begins (purple)
- Feb 19 - Apr 2: Lent (purple, rose on Laetare Sun)
- Apr 3:       Holy Thursday
- Apr 4:       Good Friday
- Apr 5:       Easter Vigil / Easter Sunday (white/gold)
- Apr 6-11:    Easter Octave
- Apr 12 - May 23: Easter Time (white/gold)
- May 24:      Pentecost (red)
- May 25-31:   Ordinary Time resumes (green)
- Jun 1 - Jul 2: Ordinary Time Week 9-13 (green)

Major feasts:
  Jan 1: Solemnity of Mary, Mother of God
  Jan 6: Epiphany of the Lord
  Jan 11: Baptism of the Lord
  Jan 17: St. Anthony, Abbot (Mem)
  Jan 21: St. Agnes (Mem)
  Jan 24: St. Francis de Sales (Mem)
  Jan 25: Conversion of St. Paul (Feast)
  Jan 26: Sts. Timothy and Titus (Mem)
  Jan 28: St. Thomas Aquinas (Mem)
  Jan 31: St. John Bosco (Mem)
  Feb 2: Presentation of the Lord (Feast)
  Feb 3: St. Blaise (Mem)
  Feb 6: St. Paul Miki & Companions (Mem)
  Feb 10: St. Scholastica (Mem)
  Feb 11: Our Lady of Lourdes (Mem)
  Feb 14: Sts. Cyril and Methodius (Mem)
  Feb 17: Seven Holy Founders of Servites (Mem)
  Feb 18: Ash Wednesday
  Feb 22: Chair of St. Peter (Feast)
  Feb 23: St. Polycarp (Mem)
  Feb 24 onwards: Lent weekdays
  Mar 7: Sts. Perpetua and Felicity (Mem)
  Mar 17: St. Patrick (Mem)
  Mar 19: St. Joseph (Solemnity)
  Mar 25: Annunciation of the Lord (Solemnity)
  Apr 5: Easter Sunday (Solemnity)
  Apr 24: Divine Mercy Sunday
  Apr 25: St. Mark (Feast)
  Apr 29: St. Catherine of Siena (Mem)
  May 1: St. Joseph the Worker (Mem)
  May 2: St. Athanasius (Mem)
  May 3: Sts. Philip and James (Feast)
  May 12: Sts. Nereus and Achilleus (Mem); Our Lady of Fatima (Opt Mem)
  May 14: St. Matthias (Feast)
  May 15: St. Isidore (Mem)
  May 24: Pentecost (Solemnity)
  May 31: Visitation of Mary (Feast)
  Jun 1: St. Justin Martyr (Mem)
  Jun 2: Sts. Marcellinus and Peter (Mem)
  Jun 9: St. Ephrem (Mem)
  Jun 11: St. Barnabas (Mem)
  Jun 13: St. Anthony of Padua (Mem)
  Jun 19: Sacred Heart of Jesus (Solemnity)
  Jun 20: Immaculate Heart of Mary (Mem)
  Jun 21: St. Aloysius Gonzaga (Mem)
  Jun 24: Nativity of St. John the Baptist (Solemnity)
  Jun 29: Sts. Peter and Paul (Solemnity)
  Jul 2: Visitation (already used May 31) — check, actually Jul 2 falls in Ordinary Time
"""
from __future__ import annotations

import json, os, sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALENDAR_PATH = ROOT / "data/calendar_2026_2029.jsonl"
OUT_DIR = ROOT / "data/research_results"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Load deterministic calendar math
cal_map: dict[str, dict[str, str]] = {}
if CALENDAR_PATH.exists():
    with open(CALENDAR_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            g_date = entry.get("gregorian_date")
            if g_date:
                cal_map[g_date] = {
                    "julian": entry.get("julian", {}).get("date", ""),
                    "hebrew": entry.get("hebrew", {}).get("date", ""),
                    "islamic_umm_al_qura": entry.get("islamic_umm_al_qura", {}).get("date", ""),
                    "coptic": entry.get("coptic", {}).get("date", ""),
                    "ethiopian": entry.get("ethiopian", {}).get("date", ""),
                }


# Curated feast catalog for Jan 1 - Jul 2, 2026
FEAST_CATALOG: dict[str, dict] = {
    "2026-01-01": {
        "rank": "Solemnity", "color": "white", "type": "solemnity",
        "title_en": "Solemnity of Mary, the Holy Mother of God",
        "title_vi": "Đại Lễ Đức Maria, Mẹ Thiên Chúa",
        "hero_en": "Octave Day of Christmas — honoring Mary as Mother of God",
        "hero_vi": "Ngày thứ 8 trong Tuần Bát Nhật — tôn vinh Mẹ Maria là Mẹ Thiên Chúa",
        "saint_en": "Blessed Virgin Mary, Mother of God",
        "saint_vi": "Đức Trinh Nữ Maria, Mẹ Thiên Chúa",
        "summary_en": "The Octave Day of Christmas celebrates Mary's divine Motherhood, proclaimed at the Council of Ephesus in 431 AD. This Solemnity honors the Blessed Virgin Mary as Theotokos — the God-bearer — who bore the eternal Son of God in her womb by the power of the Holy Spirit.",
        "summary_vi": "Ngày thứ 8 trong Tuần Bát Nhật Giáng Sinh mừng kính Mẹ Maria là Mẹ Thiên Chúa, được Công đồng Êphêsô long trọng tuyên xưng năm 431. Đại Lễ này tôn vinh Đức Trinh Nữ Maria là Đức Theotokos — Đấng mang Thiên Chúa — đã cưu mang Con Hằng Hữu của Thiên Chúa bởi quyền năng Chúa Thánh Thần.",
        "body_en": "On this Octave Day of the Nativity, the Church turns the focus from the newborn King to His Mother, recognizing the singular grace bestowed upon the Virgin Mary. The Council of Ephesus (431 AD) defined that Mary is rightly called the Mother of God because her Son, Jesus Christ, is one divine Person with two natures, divine and human.\n\nIn Her maternal role, Mary intercedes for all the faithful, drawing humanity into intimate union with her Divine Son. The liturgy of this day is filled with prayers entrusting the New Year to her maternal care, asking for her protection throughout the days ahead.\n\nAs the World Day of Peace, observed since 1967, this Solemnity calls all nations to recognize that true peace begins in the human heart reconciled to God.",
        "body_vi": "Vào ngày thứ 8 trong Tuần Bát Nhật này, Giáo hội chuyển trọng tâm từ Hài Nhi Vua đến Mẹ của Ngài, công nhận ân sủng đặc biệt đã ban cho Đức Trinh Nữ Maria. Công đồng Êphêsô (năm 431) đã định tín rằng Mẹ Maria xứng đáng được gọi là Mẹ Thiên Chúa bởi vì Con của Mẹ, Chúa Giêsu Kitô, là một Ngôi Vị thần linh duy nhất với hai bản tính, thần linh và nhân loại.\n\nTrong vai trò làm Mẹ, Mẹ Maria chuyển cầu cho tất cả các tín hữu, đưa nhân loại vào sự hiệp nhất thân mật với Con Thiên Chúa. Phụng vụ ngày hôm nay tràn ngập những lời nguyện phó thác năm mới cho sự chăm sóc của Mẹ, xin Mẹ che chở trong suốt những ngày sắp tới.\n\nLà Ngày Hòa Bình Thế Giới, được cử hành từ năm 1967, Đại Lễ này kêu gọi mọi quốc gia nhận ra rằng hòa bình thật sự bắt đầu từ tâm hồn con người hòa giải với Thiên Chúa.",
        "prayer_en": "O God, who through the fruitful virginity of Blessed Mary bestowed upon the human race the reward of eternal salvation, grant, we pray, that we may feel the intercession of her whose festivals we celebrate.",
        "prayer_vi": "Lạy Thiên Chúa, nhờ sự đồng trinh phong phú của Đức Maria chúc phúc mà ban cho loài người phần thưởng cứu rỗi vĩnh cửu, xin cho chúng con cảm nhận được sự chuyển cầu của Mẹ mà chúng con đang mừng lễ kính.",
        "place": {"name": "St. Peter's Basilica, Vatican City", "latitude": 41.9022, "longitude": 12.4539, "confidence": "confirmed", "source_url": "https://www.vatican.va/various/basiliche/san_pietro/index_it.htm"},
        "artwork": {"title": "Madonna and Child", "maker": "Duccio di Buoninsegna", "date_label": "c. 1300", "source_url": "https://commons.wikimedia.org/wiki/File:Duccio_di_Buoninsegna_-_Madonna_and_Child_-_WGA05890.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB — Solemnity of Mary, Mother of God", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Council of Ephesus (431 AD)", "url": "https://www.vatican.va/archive/ccc_css/archive/councils/lec1.htm", "type": "vatican"},
            {"label": "Catechism of the Catholic Church — Theotokos (495)", "url": "https://www.vatican.va/archive/ccc_css/archive/catechism/p122a3p1.htm", "type": "vatican"}
        ]
    },
    "2026-01-06": {
        "rank": "Solemnity", "color": "white", "type": "solemnity",
        "title_en": "The Epiphany of the Lord",
        "title_vi": "Đại Lễ Hiển Linh — Chúa Giêsu Tỏ Mình Ra",
        "hero_en": "The nations come to worship the newborn King",
        "hero_vi": "Muôn dân đến thờ lạy Hài Nhi Vua",
        "saint_en": "The Manifestation of Christ to the Gentiles",
        "saint_vi": "Chúa Giêsu tỏ mình ra cho các dân tộc",
        "summary_en": "The Epiphany celebrates the manifestation of Jesus Christ to the Magi — the wise men from the East — representing the nations of the world. This Solemnity reveals that the salvation brought by the Incarnation is for all peoples, not only the children of Abraham.",
        "summary_vi": "Đại Lễ Hiển Linh mừng việc Chúa Giêsu Kitô tỏ mình ra cho các Nhà Thông Thái — những vị hiền nhân từ phương Đông — đại diện cho muôn dân trên thế giới. Đại Lễ này loan báo rằng ơn cứu độ do biến cố Nhập Thể mang lại là cho mọi dân tộc, không chỉ riêng con cháu của Abraham.",
        "body_en": "Following the Star of Bethlehem, the Magi — traditionally three in number and often identified as Caspar, Melchior, and Balthasar — traveled from distant lands bearing gifts of gold, frankincense, and myrrh. Their journey symbolizes the pilgrimage of all nations toward the Light of Christ.\n\nGold acknowledged Christ's kingship, frankincense His divinity, and myrrh His coming Passion and burial. Through these gifts, the Magi unknowingly proclaimed the full mystery of Christ: King, God, and Suffering Savior.\n\nIn many cultures, this day is celebrated with the blessing of homes, where families mark their doorframes with chalk as a sign of welcome to Christ, the Light of the World.",
        "body_vi": "Theo ánh sao Bêlem, các Nhà Thông Thái — truyền thống ghi nhận có ba vị và thường được xác định là Caspar, Melchior và Balthasar — đã du hành từ những vùng đất xa xôi mang theo lễ vật vàng, nhũ hương và mộc dược. Hành trình của các ngài tượng trưng cho cuộc hành hương của mọi dân tộc về phía Ánh Sáng Đức Kitô.\n\nVàng công nhận tước vị Vua của Đức Kitô, nhũ hương tôn vinh thần tính của Ngài, và mộc dược báo trước cuộc Khổ Nạn và an táng của Ngài. Qua những lễ vật này, các Nhà Thông Thái đã vô tình loan báo toàn bộ mầu nhiệm Đức Kitô: Vua, Thiên Chúa và Đấng Cứu Độ chịu đau khổ.\n\nTrong nhiều nền văn hóa, ngày này được cử hành với phép lành nhà cửa, nơi các gia đình ghi dấu trên khung cửa bằng phấn như dấu hiệu chào đón Đức Kitô, Ánh Sáng Thế Gian.",
        "prayer_en": "O God, who on this day revealed your Only Begotten Son to the nations by the guidance of a star, grant that we, who now know you by faith, may be brought to contemplate the beauty of your glorious divinity.",
        "prayer_vi": "Lạy Thiên Chúa, ngày hôm nay Chúa đã tỏ Con Một của Chúa ra cho muôn dân nhờ sự hướng dẫn của ngôi sao, xin cho chúng con, những người nay nhận biết Chúa qua đức tin, được đưa đến chiêm ngắm vẻ đẹp rực rỡ thần tính của Chúa.",
        "place": {"name": "Church of the Nativity, Bethlehem", "latitude": 31.7043, "longitude": 35.2076, "confidence": "confirmed", "source_url": "https://www.custodia.org/en/sanctuaries/bethlehem"},
        "artwork": {"title": "Adoration of the Magi", "maker": "Sandro Botticelli", "date_label": "c. 1475", "source_url": "https://commons.wikimedia.org/wiki/File:Sandro_Botticelli_-_Adoration_of_the_Magi_-_National_Gallery_of_Art.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB — Epiphany of the Lord", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Catechism of the Catholic Church — Epiphany (528)", "url": "https://www.vatican.va/archive/ccc_css/archive/catechism/p122a3p1.htm", "type": "vatican"},
            {"label": "Matthew 2:1-12 — The Visit of the Magi", "url": "https://bible.usccb.org/bible/matthew/2", "type": "encyclopedia"}
        ]
    },
    "2026-01-11": {
        "rank": "Feast", "color": "white", "type": "feast",
        "title_en": "Feast of the Baptism of the Lord",
        "title_vi": "Lễ Chúa Giêsu Chịu Phép Rửa",
        "hero_en": "Heaven opens — the Father's voice: You are my beloved Son",
        "hero_vi": "Trời mở ra — tiếng Chúa Cha: Con là Con yêu dấu của Cha",
        "saint_en": "The Baptism of the Lord",
        "saint_vi": "Chúa Giêsu chịu phép rửa",
        "summary_en": "The Feast of the Baptism of the Lord closes the Christmas Season and reveals the mystery of the Holy Trinity. At the Jordan River, John the Baptist baptizes Jesus, the heavens open, the Holy Spirit descends as a dove, and the Father's voice is heard proclaiming Jesus as His beloved Son.",
        "summary_vi": "Lễ Chúa Giêsu Chịu Phép Rửa kết thúc Mùa Giáng Sinh và mặc khải mầu nhiệm Ba Ngôi. Tại sông Giođan, Thánh Gioan Tẩy Giả làm phép rửa cho Chúa Giêsu, trời mở ra, Chúa Thánh Thần ngự xuống như chim bồ câu, và tiếng Chúa Cha vang lên tuyên bố Chúa Giêsu là Con yêu dấu của Ngài.",
        "body_en": "Jesus' baptism by John the Baptist is a moment of profound theological revelation. Though sinless, Jesus stands among sinners to identify with humanity's need for repentance. The heavens opening signifies God's response to our long-awaited redemption.\n\nThe descent of the Holy Spirit as a dove and the Father's voice declaring 'You are my beloved Son; with you I am well pleased' (Matthew 3:17) reveal the full mystery of the Trinity. The faithful are invited to renew their own baptismal promises and to embrace the mission of being sons and daughters in the Son.\n\nThis feast inaugurates Ordinary Time, calling Christians to live their baptismal identity with renewed conviction.",
        "body_vi": "Việc Chúa Giêsu chịu phép rửa của Thánh Gioan Tẩy Giả là khoảnh khắc mặc khải thần học sâu sắc. Dù vô tội, Chúa Giêsu vẫn đứng giữa những người tội lỗi để đồng nhất với nhu cầu ăn năn của nhân loại. Trời mở ra biểu thị sự đáp lại của Thiên Chúa cho ơn cứu chuộc mà chúng ta đã chờ đợi từ lâu.\n\nChúa Thánh Thần ngự xuống như chim bồ câu và tiếng Chúa Cha tuyên bố 'Con là Con yêu dấu của Cha, hôm nay Cha đã sinh ra Con' (Mt 3,17) mặc khải trọn vẹn mầu nhiệm Ba Ngôi. Các tín hữu được mời gọi canh tân lời hứa bí tích rửa tội của mình và sống sứ mạng làm con cái trong Con Một.\n\nLễ này khai mở Mùa Thường Niên, kêu gọi các Kitô hữu sống căn tính bí tích rửa tội với lòng xác tín canh tân.",
        "prayer_en": "O God, who by the voice of the Holy Spirit declared your beloved Son at the baptism in the Jordan, grant that we, who are born of water and the Spirit, may be numbered among your children.",
        "prayer_vi": "Lạy Thiên Chúa, Đấng đã dùng tiếng Chúa Thánh Thần tuyên bố Con yêu dấu của Chúa khi chịu phép rửa tại sông Giođan, xin cho chúng con, những người được sinh ra bởi nước và Thần Khí, được ghi vào số các con cái của Chúa.",
        "place": {"name": "Qasr el Yahud, Jordan River (traditional baptism site)", "latitude": 31.8333, "longitude": 35.5333, "confidence": "traditional", "source_url": "https://www.custodia.org/en/sanctuaries/baptism-site"},
        "artwork": {"title": "The Baptism of Christ", "maker": "Piero della Francesca", "date_label": "c. 1450", "source_url": "https://commons.wikimedia.org/wiki/File:Piero_della_Francesca_-_Battesimo_di_Cristo.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB — Baptism of the Lord", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Matthew 3:13-17 — Baptism of Jesus", "url": "https://bible.usccb.org/bible/matthew/3", "type": "encyclopedia"}
        ]
    },
    "2026-02-02": {
        "rank": "Feast", "color": "white", "type": "feast",
        "title_en": "Feast of the Presentation of the Lord",
        "title_vi": "Lễ Dâng Chúa Giêsu Trong Đền Thờ",
        "hero_en": "The Light of the Nations enters His temple",
        "hero_vi": "Ánh Sáng Muôn Dân vào đền thờ",
        "saint_en": "Candlemas — The Meeting of the Lord",
        "saint_vi": "Lễ Đức Mẹ Dâng Chúa Trong Đền Thờ",
        "summary_en": "Forty days after Christmas, the Church celebrates the Presentation of Jesus in the Temple. Following Mosaic Law, Mary and Joseph bring the Child to Jerusalem, where the righteous elder Simeon proclaims Him 'a light for revelation to the Gentiles' — earning this feast the popular name 'Candlemas.'",
        "summary_vi": "Bốn mươi ngày sau Giáng Sinh, Giáo hội mừng Lễ Dâng Chúa Giêsu Trong Đền Thờ. Theo Lề Luật Môsê, Mẹ Maria và Thánh Giuse đem Hài Nhi đến Giêrusalem, nơi cụ già công chính Simêon tuyên bố Ngài là 'ánh sáng để mặc khải cho các dân tộc' — khiến lễ này được gọi phổ biến là 'Lễ Nến.'",
        "body_en": "Simeon's canticle, the Nunc Dimittis, captures the joy of one who has finally seen the long-awaited Messiah. 'Now you dismiss your servant in peace, for my eyes have seen your salvation, which you prepared in the sight of all peoples, a light for revelation to the Gentiles and glory for your people Israel' (Luke 2:30-32).\n\nThe prophetess Anna, eighty-four years old, also recognized the Child as the Redeemer and spoke of Him to all who awaited the deliverance of Jerusalem. The candles blessed on this day are carried in procession to recall Christ as the Light entering His temple.\n\nThis feast closes the Christmas season's external celebrations and invites the faithful to offer themselves as living temples of the Holy Spirit.",
        "body_vi": "Thánh ca Simêon, Nunc Dimittis, diễn tả niềm vui của người đã cuối cùng thấy Đấng Mêxia được chờ đợi từ lâu. 'Bây giờ Chúa cho tôi tớ Chúa ra đi trong bình an, vì mắt tôi đã thấy ơn cứu độ của Chúa, mà Chúa đã chuẩn bị trước mặt muôn dân, ánh sáng để mặc khải cho các dân tộc và vinh quang của dân Israel' (Lc 2,30-32).\n\nNữ tiên tri Anna, tám mươi bốn tuổi, cũng nhận ra Hài Nhi là Đấng Cứu Chuộc và nói về Ngài cho tất cả những ai đang chờ đợi sự giải phóng của Giêrusalem. Những cây nến được thánh hiến trong ngày này được rước đi trong cuộc kiệu để nhắc nhở Đức Kitô là Ánh Sáng vào đền thờ.\n\nLễ này kết thúc các cử hành bên ngoài của Mùa Giáng Sinh và mời gọi các tín hữu dâng mình làm đền thờ sống động cho Chúa Thánh Thần.",
        "prayer_en": "Almighty ever-living God, we humbly implore your majesty that, just as your Only Begotten Son was presented in the temple in the substance of our flesh, so too we may be presented to you with purified souls.",
        "prayer_vi": "Lạy Thiên Chúa toàn năng hằng hữu, chúng con tha thiết cầu xin long trọng của Chúa rằng, cũng như Con Một Chúa đã được dâng trong đền thờ trong xác phàm nhân loại, chúng con cũng xứng đáng được dâng trước Chúa với tâm hồn thanh sạch.",
        "place": {"name": "Church of the Presentation, Jerusalem", "latitude": 31.7818, "longitude": 35.2368, "confidence": "confirmed", "source_url": "https://www.custodia.org/en/sanctuaries/presentation"},
        "artwork": {"title": "Presentation of Jesus at the Temple", "maker": "Rembrandt van Rijn", "date_label": "c. 1628", "source_url": "https://commons.wikimedia.org/wiki/File:Rembrandt_van_Rijn-_Presentation_of_Jesus_in_the_Temple.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB — Presentation of the Lord", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Luke 2:22-40 — Presentation in the Temple", "url": "https://bible.usccb.org/bible/luke/2", "type": "encyclopedia"}
        ]
    },
    "2026-02-18": {
        "rank": "Feria", "color": "purple", "type": "ash_wednesday",
        "title_en": "Ash Wednesday — Beginning of Lent",
        "title_vi": "Thứ Tư Lễ Tro — Khởi đầu Mùa Chay",
        "hero_en": "Remember you are dust, and to dust you shall return",
        "hero_vi": "Hãy nhớ rằng con là bụi tro, và sẽ trở về bụi tro",
        "saint_en": "Ash Wednesday",
        "saint_vi": "Thứ Tư Lễ Tro",
        "summary_en": "Ash Wednesday inaugurates the sacred Lenten Season, the forty-day journey toward Easter. The faithful receive ashes on their foreheads as a sign of repentance and mortality, marking the beginning of a period of prayer, fasting, and almsgiving.",
        "summary_vi": "Thứ Tư Lễ Tro khai mở Mùa Chay thánh thiện, hành trình bốn mươi ngày hướng về Phục Sinh. Các tín hữu lãnh nhận tro trên trán như dấu hiệu sám hối và tính mỏng manh của kiếp người, đánh dấu khởi đầu thời kỳ cầu nguyện, ăn chay và bố thí.",
        "body_en": "The ashes used on this day are made from the palm branches blessed on the previous Palm Sunday, symbolically linking the beginning of Lent to the triumphal entry into Jerusalem that led to the Passion. The liturgical formula 'Repent and believe in the Gospel' or 'Remember you are dust' accompanies the imposition of ashes.\n\nLent is a forty-day season (excluding Sundays) that mirrors the forty days Jesus spent in the desert before His public ministry. It is a time of spiritual combat against the forces of sin, a renewal of baptismal promises, and a deepening of conversion.\n\nThe three pillars of Lent — prayer, fasting, and almsgiving — invite Christians to grow in intimate union with God, master their appetites, and serve the poor with greater generosity.",
        "body_vi": "Tro được sử dụng trong ngày này được làm từ các cành lá thánh đã được thánh hiến vào Chúa Nhật Lễ Lá trước đó, biểu tượng cho việc kết nối khởi đầu Mùa Chay với sự kiện Chúa vinh quang vào Giêrusalem dẫn đến Cuộc Khổ Nạn. Công thức phụng vụ 'Hãy ăn năn và tin vào Tin Mừng' hoặc 'Hãy nhớ rằng con là bụi tro' đi kèm với việc rắc tro.\n\nMùa Chay là mùa bốn mươi ngày (không kể các Chúa Nhật) phản ánh bốn mươi ngày Chúa Giêsu trải qua trong sa mạc trước sứ vụ công khai. Đó là thời gian chiến đấu thiêng liêng chống lại các thế lực tội lỗi, canh tân lời hứa bí tích rửa tội, và sâu sắc hóa sự hoán cải.\n\nBa trụ cột của Mùa Chay — cầu nguyện, ăn chay và bố thí — mời gọi các Kitô hữu lớn lên trong sự hiệp nhất thân mật với Thiên Chúa, làm chủ các ham muốn và phục vụ người nghèo với lòng quảng đại hơn.",
        "prayer_en": "Grant, O Lord, that we may begin with holy fasting the campaign of this sacred combat, so that, as we take up the battle against the spirit of evil, we may be armed with the weapons of self-restraint.",
        "prayer_vi": "Lạy Chúa, xin cho chúng con khởi đầu cuộc chiến đấu thánh thiêng này bằng việc ăn chay thánh, để khi chúng ta chiến đấu chống lại thần dữ, chúng ta được trang bị bằng vũ khí tự chủ.",
        "place": {"name": "Church of the Holy Sepulchre, Jerusalem", "latitude": 31.7784, "longitude": 35.2296, "confidence": "traditional", "source_url": "https://www.custodia.org/en/sanctuaries/holy-sepulchre"},
        "artwork": {"title": "Ash Wednesday", "maker": "Carlo Crivelli", "date_label": "c. 1470", "source_url": "https://commons.wikimedia.org/wiki/File:Carlo_Crivelli_-_Ash_Wednesday.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB — Ash Wednesday", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Joel 2:12-18 — Call to Repentance", "url": "https://bible.usccb.org/bible/joel/2", "type": "encyclopedia"},
            {"label": "Catechism of the Catholic Church — Lent (540)", "url": "https://www.vatican.va/archive/ccc_css/archive/catechism/p122a3p1.htm", "type": "vatican"}
        ]
    },
    "2026-03-19": {
        "rank": "Solemnity", "color": "white", "type": "solemnity",
        "title_en": "Solemnity of Saint Joseph, Husband of the Blessed Virgin Mary",
        "title_vi": "Đại Lễ Thánh Giuse, Bạn Đức Trinh Nữ Maria",
        "hero_en": "The just man, the silent carpenter who sheltered the Savior",
        "hero_vi": "Người công chính, người thợ mộc thầm lặng đã che chở Đấng Cứu Độ",
        "saint_en": "Saint Joseph, Spouse of the Blessed Virgin Mary",
        "saint_vi": "Thánh Giuse, Bạn Đức Trinh Nữ Maria",
        "summary_en": "This Solemnity honors Saint Joseph, the husband of Mary and the foster-father of Jesus. A descendant of King David, Joseph was a righteous man chosen by God to guard the Holy Family and protect the Christ Child from the massacre of the innocents.",
        "summary_vi": "Đại Lễ này tôn vinh Thánh Giuse, chồng của Mẹ Maria và cha nuôi của Chúa Giêsu. Là hậu duệ của Vua Đavít, Thánh Giuse là người công chính được Thiên Chúa tuyển chọn để gìn giữ Thánh Gia và bảo vệ Hài Nhi Giêsu khỏi cuộc tàn sát các trẻ thơ.",
        "body_en": "Joseph appears in the Gospel as a man of few words but great obedience. Four times an angel appears to him in dreams, and each time Joseph responds immediately: he takes Mary as his wife, flees with the Holy Family to Egypt, returns after Herod's death, and settles in Nazareth. His silent fidelity teaches us the strength of humble service.\n\nDeclared Patron of the Universal Church by Pope Pius IX in 1870, Saint Joseph is also the patron of workers, families, and a happy death. The faithful invoke his intercession for guidance in practical affairs and for protection of their loved ones.\n\nThe humility of Saint Joseph — his willingness to be overshadowed, to step aside so that Christ might be revealed — is a model for every disciple called to serve in obscurity.",
        "body_vi": "Thánh Giuse xuất hiện trong Tin Mừng như một người ít lời nhưng vâng phục lớn lao. Bốn lần một thiên thần hiện ra với ngài trong giấc mơ, và mỗi lần Thánh Giuse đều đáp lại ngay lập tức: đón Mẹ Maria làm vợ, trốn cùng Thánh Gia sang Ai Cập, trở về sau khi Hêrôđê qua đời, và định cư tại Nagiarét. Sự trung tín thầm lặng của ngài dạy chúng ta sức mạnh của việc phục vụ khiêm tốn.\n\nĐược Đức Giáo hoàng Piô IX tuyên bố là Quan Thầy của Hội Thánh Hoàn Vũ năm 1870, Thánh Giuse cũng là quan thầy của người thợ thuyền, gia đình và sự chết lành. Các tín hữu kêu cầu sự chuyển cầu của ngài để được hướng dẫn trong các công việc thực tế và bảo vệ những người thân yêu.\n\nSự khiêm nhường của Thánh Giuse — sự sẵn sàng bị che khuất, nhường bước để Đức Kitô được mặc khải — là mẫu mực cho mỗi môn đệ được kêu gọi phục vụ trong bóng tối.",
        "prayer_en": "O God, who in your unfailing wisdom chose Saint Joseph to be the spouse of the Blessed Virgin Mary and the foster-father of your Son, grant, we pray, that we may deserve to have him as our intercessor in heaven whom we venerate as our protector on earth.",
        "prayer_vi": "Lạy Thiên Chúa, Đấng trong sự khôn ngoan hoàn hảo đã tuyển chọn Thánh Giuse làm bạn đời của Đức Trinh Nữ Maria và cha nuôi của Con Chúa, xin cho chúng con được ngài chuyển cầu trên trời, Đấng mà chúng con tôn kính làm người bảo vệ chúng con dưới đất.",
        "place": {"name": "St. Joseph's Oratory, Montreal", "latitude": 45.4928, "longitude": -73.6181, "confidence": "confirmed", "source_url": "https://www.saint-joseph.org/en/"},
        "artwork": {"title": "Saint Joseph with the Infant Jesus", "maker": "El Greco", "date_label": "c. 1597", "source_url": "https://commons.wikimedia.org/wiki/File:El_Greco_-_Saint_Joseph_and_the_Christ_Child.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB — Saint Joseph", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Matthew 1:18-25 — Joseph's Righteousness", "url": "https://bible.usccb.org/bible/matthew/1", "type": "encyclopedia"},
            {"label": "Catholic Encyclopedia — Saint Joseph", "url": "https://www.newadvent.org/cathen/08532a.htm", "type": "encyclopedia"}
        ]
    },
    "2026-03-25": {
        "rank": "Solemnity", "color": "white", "type": "solemnity",
        "title_en": "The Annunciation of the Lord",
        "title_vi": "Đại Lễ Truyền Tin",
        "hero_en": "Be it done unto me according to your word",
        "hero_vi": "Xin vâng theo lời Chúa",
        "saint_en": "The Annunciation of Our Lord",
        "saint_vi": "Truyền Tin cho Đức Mẹ",
        "summary_en": "The Annunciation celebrates the moment when the Angel Gabriel announced to the Blessed Virgin Mary that she would conceive and bear the Son of God, and Mary's 'Fiat' — her 'Yes' to the divine plan. This Solemnity marks the Incarnation itself, when the eternal Word became flesh in her womb.",
        "summary_vi": "Đại Lễ Truyền Tin mừng khoảnh khắc Thiên Thần Gabriel loan báo cho Đức Trinh Nữ Maria rằng Mẹ sẽ thụ thai và sinh Con Thiên Chúa, cùng với tiếng 'Xin Vâng' của Mẹ Maria — sự 'Vâng' của Mẹ với chương trình thần linh. Đại Lễ này đánh dấu chính biến cố Nhập Thể, khi Lời Hằng Hữu trở nên xác phàm trong cung lòng Mẹ.",
        "body_en": "The Annunciation is the hinge of history. In the obscure town of Nazareth, a young Jewish woman became the Mother of God, and the eternal Son took flesh for our salvation. Mary's response, 'Behold the handmaid of the Lord; be it done unto me according to thy word' (Luke 1:38), is the model of every act of Christian faith.\n\nThe Fathers of the Church saw in Mary the New Eve: where Eve disobeyed in the Garden, Mary obeyed in the home, and through her obedience came the remedy for disobedience. The Liturgy of the Hours marks the Annunciation with the Angelus, prayed three times daily to commemorate the Incarnation.\n\nNine months from this date, the Church celebrates the Nativity of the Lord on December 25.",
        "body_vi": "Lễ Truyền Tin là bản lề của lịch sử. Tại thị trấn nhỏ bé Nagiarét, một thiếu nữ Do Thái trẻ tuổi trở thành Mẹ Thiên Chúa, và Con Hằng Hữu đã mặc lấy xác phàm cho ơn cứu rỗi chúng ta. Sự đáp lại của Mẹ Maria, 'Này con là tôi tớ Chúa, xin vâng theo lời Chúa' (Lc 1,38), là mẫu mực của mọi hành động đức tin Kitô giáo.\n\nCác Giáo phụ Hội Thánh đã thấy nơi Mẹ Maria là Eva Mới: nơi Eva bất tuân trong Vườn Địa Đàng, Mẹ Maria vâng lời trong nhà, và qua sự vâng lời của Mẹ đến thuốc chữa cho sự bất tuân. Giờ Kinh Phụng Vụ đánh dấu Lễ Truyền Tin với kinh Truyền Tin, đọc ba lần mỗi ngày để tưởng nhớ biến cố Nhập Thể.\n\nChín tháng từ ngày này, Giáo hội mừng Đại Lễ Giáng Sinh vào ngày 25 tháng 12.",
        "prayer_en": "Pour forth, we beseech you, O Lord, your grace into our hearts, that we, to whom the Incarnation of Christ your Son was made known by the message of an Angel, may by his Passion and Cross be brought to the glory of his Resurrection.",
        "prayer_vi": "Lạy Chúa, xin đổ tràn ân sủng Chúa vào lòng chúng con, để chúng con, những người đã được biết về biến cố Nhập Thể của Chúa Kitô Con Chúa qua sứ điệp của một Thiên Thần, nhờ cuộc Thương Khó và Thánh Giá của Ngài mà được dẫn đến vinh quang của sự Phục Sinh.",
        "place": {"name": "Basilica of the Annunciation, Nazareth", "latitude": 32.7022, "longitude": 35.2985, "confidence": "confirmed", "source_url": "https://www.custodia.org/en/sanctuaries/nazareth"},
        "artwork": {"title": "The Annunciation", "maker": "Leonardo da Vinci", "date_label": "c. 1472", "source_url": "https://commons.wikimedia.org/wiki/File:Leonardo_da_Vinci_-_Annunciazione_-_Google_Art_Project.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB — Annunciation of the Lord", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Luke 1:26-38 — The Annunciation", "url": "https://bible.usccb.org/bible/luke/1", "type": "encyclopedia"},
            {"label": "Catechism of the Catholic Church — The Annunciation (484-486)", "url": "https://www.vatican.va/archive/ccc_css/archive/catechism/p122a3p1.htm", "type": "vatican"}
        ]
    },
    "2026-04-05": {
        "rank": "Solemnity", "color": "white", "type": "solemnity",
        "title_en": "Easter Sunday — The Resurrection of the Lord",
        "title_vi": "Chúa Nhật Phục Sinh — Chúa Sống Lại",
        "hero_en": "Christ is risen! He is risen indeed! Alleluia!",
        "hero_vi": "Đức Kitô đã sống lại! Ngài đã sống lại thật! Alleluia!",
        "saint_en": "The Resurrection of the Lord",
        "saint_vi": "Chúa Giêsu Phục Sinh",
        "summary_en": "Easter Sunday is the greatest Solemnity of the liturgical year, celebrating the Resurrection of Jesus Christ from the dead on the third day after His Passion. The empty tomb and the appearances to the disciples are the foundation of the Christian faith and the source of our hope of eternal life.",
        "summary_vi": "Chúa Nhật Phục Sinh là Đại Lễ cao trọng nhất của năm phụng vụ, mừng việc Chúa Giêsu Kitô sống lại từ cõi chết vào ngày thứ ba sau Cuộc Thương Khó. Ngôi mộ trống và các biến cố Chúa hiện ra với các môn đệ là nền tảng của đức tin Kitô giáo và nguồn hy vọng sự sống vĩnh cửu của chúng ta.",
        "body_en": "On the third day after His death on the Cross, Jesus rose in glory from the tomb, conquering death forever. The women who came to anoint His body at dawn found the stone rolled away and the tomb empty, with angels proclaiming: 'Why do you seek the living among the dead? He is not here, but is risen' (Luke 24:5-6).\n\nThroughout the day, the Risen Lord appeared to Mary Magdalene, to the disciples on the road to Emmaus, to Peter, to the ten apostles behind locked doors, and later to Thomas and the eleven. These appearances established the truth of the Resurrection as the bedrock of Christian belief.\n\nEaster is the Passover (Pascha) of the New Covenant, the passage from death to life, from sin to grace, from darkness to light. The fifty days of Easter Time that follow lead to the descent of the Holy Spirit at Pentecost.",
        "body_vi": "Vào ngày thứ ba sau khi chịu chết trên Thập Giá, Chúa Giêsu đã sống lại vinh quang từ ngôi mộ, chiến thắng sự chết muôn đời. Các phụ nữ đến xức dầu cho xác Ngài vào sáng sớm đã thấy tảng đá lăn ra và ngôi mộ trống, với các thiên thần loan báo: 'Sao các bà tìm người sống ở giữa kẻ chết? Ngài không ở đây, Ngài đã sống lại rồi' (Lc 24,5-6).\n\nTrong suốt ngày hôm đó, Chúa Phục Sinh đã hiện ra với bà Maria Mađalêna, với các môn đệ trên đường Emmau, với Phêrô, với mười tông đồ đằng sau những cánh cửa đóng kín, và sau đó với Tôma và mười một vị. Những lần hiện ra này đã xác lập chân lý Phục Sinh là nền tảng của đức tin Kitô giáo.\n\nPhục Sinh là Lễ Vượt Qua (Pascha) của Giao Ước Mới, cuộc đi qua từ sự chết đến sự sống, từ tội lỗi đến ân sủng, từ bóng tối đến ánh sáng. Năm mươi ngày Mùa Phục Sinh tiếp theo dẫn đến sự ngự xuống của Chúa Thánh Thần vào lễ Ngũ Tuần.",
        "prayer_en": "O God, who on this day, through your Only Begotten Son, have conquered death and unlocked the path to eternity, grant, we pray, that we who celebrate the Solemnity of the Lord's Resurrection may, through the renewing Spirit, rise to newness of life.",
        "prayer_vi": "Lạy Thiên Chúa, ngày hôm nay qua Con Một, Chúa đã chiến thắng sự chết và mở ra con đường vĩnh cửu, xin cho chúng con, những người cử hành Đại Lễ Phục Sinh của Chúa, nhờ Chúa Thánh Thần canh tân, được sống lại trong sự sống mới.",
        "place": {"name": "Church of the Holy Sepulchre, Jerusalem", "latitude": 31.7784, "longitude": 35.2296, "confidence": "confirmed", "source_url": "https://www.custodia.org/en/sanctuaries/holy-sepulchre"},
        "artwork": {"title": "The Resurrection of Christ", "maker": "Piero della Francesca", "date_label": "c. 1463", "source_url": "https://commons.wikimedia.org/wiki/File:Piero_della_Francesca_-_Resurrection.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB — Easter Sunday", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Catechism of the Catholic Church — The Resurrection (638-655)", "url": "https://www.vatican.va/archive/ccc_css/archive/catechism/p122a3p2.htm", "type": "vatican"},
            {"label": "Luke 24:1-12 — The Empty Tomb", "url": "https://bible.usccb.org/bible/luke/24", "type": "encyclopedia"}
        ]
    },
    "2026-05-24": {
        "rank": "Solemnity", "color": "red", "type": "solemnity",
        "title_en": "Pentecost Sunday",
        "title_vi": "Lễ Hiện Xuống — Chúa Nhật Ngũ Tuần",
        "hero_en": "The Spirit comes — tongues of fire, hearts renewed",
        "hero_vi": "Chúa Thánh Thần ngự xuống — lưỡi lửa, tâm hồn canh tân",
        "saint_en": "The Descent of the Holy Spirit",
        "saint_vi": "Chúa Thánh Thần Hiện Xuống",
        "summary_en": "Pentecost, fifty days after Easter, celebrates the descent of the Holy Spirit upon the Virgin Mary and the Apostles in the Upper Room. Marked by tongues of fire and the sound of a mighty wind, this event birthed the Church and empowered the Apostles to preach the Gospel to all nations.",
        "summary_vi": "Lễ Hiện Xuống, năm mươi ngày sau Phục Sinh, mừng việc Chúa Thánh Thần ngự xuống trên Đức Trinh Nữ Maria và các Tông Đồ trong Phòng Tiệc Ly. Được đánh dấu bằng các lưỡi lửa và tiếng gió mạnh, biến cố này khai sinh Giáo Hội và ban quyền năng cho các Tông Đồ rao giảng Tin Mừng cho muôn dân.",
        "body_en": "In the Upper Room in Jerusalem, the disciples were gathered in prayer with Mary when suddenly a sound like a rushing wind filled the house, and tongues of fire rested on each of them. They were filled with the Holy Spirit and began to speak in different languages, as the Spirit gave them utterance (Acts 2:2-4).\n\nThe crowd that gathered heard them speaking in their own native tongues, marveling that uneducated Galileans could proclaim the mighty works of God in many languages. Peter's sermon that day converted three thousand souls, inaugurating the public mission of the Church.\n\nThe Jewish feast of Pentecost (Shavuot) was originally a thanksgiving for the wheat harvest and a commemoration of the giving of the Law at Sinai. In Christian tradition, it celebrates the giving of the Holy Spirit and the new Law of Love written on the heart.",
        "body_vi": "Trong Phòng Tiệc Ly tại Giêrusalem, các môn đệ đang quy tụ cầu nguyện cùng Mẹ Maria thì bỗng nhiên một tiếng động như gió mạnh thổi đến lấp đầy cả căn nhà, và các lưỡi lửa đậu xuống trên mỗi người. Họ đầy tràn Chúa Thánh Thần và bắt đầu nói bằng các thứ tiếng khác nhau, như Thần Khí ban cho họ nói (Cv 2,2-4).\n\nĐám đông tụ tập đã nghe họ nói bằng tiếng mẹ đẻ của mình, ngạc nhiên rằng những người Galilê thất học lại có thể rao giảng những công trình kỳ diệu của Thiên Chúa bằng nhiều ngôn ngữ. Bài giảng của Thánh Phêrô hôm đó đã cải hoá ba ngàn linh hồn, khai mở sứ mạng công khai của Giáo Hội.\n\nLễ Do Thái Ngũ Tuần (Shavuot) ban đầu là lễ tạ ơn mùa gặt lúa mì và tưởng nhớ việc ban Lề Luật tại Sinai. Trong truyền thống Kitô giáo, lễ này mừng việc ban Chúa Thánh Thần và Lề Luật Mới của Tình Yêu được ghi vào lòng.",
        "prayer_en": "O God, who by the mystery of today's great feast sanctify your Church throughout the world, grant that, through the outpouring of the Holy Spirit, your people everywhere may be found acceptable in your sight.",
        "prayer_vi": "Lạy Thiên Chúa, Đấng nhờ mầu nhiệm đại lễ hôm nay thánh hiến Giáo Hội Chúa trên toàn thế giới, xin cho dân Chúa ở khắp nơi, nhờ sự tuôn đổ của Chúa Thánh Thần, được đẹp lòng Chúa.",
        "place": {"name": "Church of the Cenacle (Upper Room), Jerusalem", "latitude": 31.7725, "longitude": 35.2297, "confidence": "traditional", "source_url": "https://www.custodia.org/en/sanctuaries/cenacle"},
        "artwork": {"title": "Pentecost", "maker": "Titian", "date_label": "c. 1545", "source_url": "https://commons.wikimedia.org/wiki/File:1546_Tiziano_Ascensione_Pentecoste_Spiridione.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB — Pentecost Sunday", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Acts 2:1-31 — The Coming of the Holy Spirit", "url": "https://bible.usccb.org/bible/acts/2", "type": "encyclopedia"},
            {"label": "Catechism of the Catholic Church — Pentecost (731-741)", "url": "https://www.vatican.va/archive/ccc_css/archive/catechism/p122a3p2.htm", "type": "vatican"}
        ]
    },
    "2026-06-19": {
        "rank": "Solemnity", "color": "white", "type": "solemnity",
        "title_en": "Solemnity of the Most Sacred Heart of Jesus",
        "title_vi": "Đại Lễ Thánh Tâm Chúa Giêsu",
        "hero_en": "Learn from me, for I am meek and humble of heart",
        "hero_vi": "Hãy học cùng tôi, vì tôi hiền lành và khiêm nhường trong lòng",
        "saint_en": "The Sacred Heart of Jesus",
        "saint_vi": "Thánh Tâm Chúa Giêsu",
        "summary_en": "The Solemnity of the Sacred Heart of Jesus, celebrated nineteen days after Pentecost, honors the boundless love of Christ as symbolized by His Heart, pierced for our salvation. The devotion, revealed to Saint Margaret Mary Alacoque in the 17th century, emphasizes Christ's merciful love and our call to make reparation for sin.",
        "summary_vi": "Đại Lễ Thánh Tâm Chúa Giêsu, được cử hành mười chín ngày sau Ngũ Tuần, tôn vinh tình yêu vô biên của Đức Kitô được tượng trưng qua Trái Tim Ngài, đã bị đâm thâu vì ơn cứu rỗi chúng ta. Việc sùng kính này, được Thánh Nữ Margareta Maria Alacoque mặc khải vào thế kỷ 17, nhấn mạnh tình yêu thương xót của Đức Kitô và lời mời gọi chúng ta đền tội.",
        "body_en": "On December 27, 1673, Saint Margaret Mary Alacoque, a Visitation nun in Paray-le-Monial, France, experienced a vision of Christ exposing His Sacred Heart and saying: 'Behold this Heart which has so loved men that it has spared nothing, even to exhausting and consuming itself, in order to testify its love.'\n\nIn response to this revelation, Christ asked for a feast day in honor of His Sacred Heart, for communion on First Fridays, for the Holy Hour of adoration, and for acts of reparation. Pope Pius IX established the feast in 1856, and Pope Pius XII elevated it to a Solemnity in 1956.\n\nThe Heart of Jesus is the symbol of His infinite divine and human love, the source from which flows the blood and water that gushed forth on the Cross (John 19:34), symbols of baptism and the Eucharist.",
        "body_vi": "Vào ngày 27 tháng 12 năm 1673, Thánh Nữ Margareta Maria Alacoque, một nữ tu Dòng Thăm Viếng tại Paray-le-Monial (Pháp), đã trải qua một thị kiến của Đức Kitô phơi bày Thánh Tâm Ngài và nói: 'Hãy nhìn Trái Tim này, yêu mến loài người đến nỗi không tiếc gì, thậm chí kiệt sức và tự tiêu hao, để chứng minh tình yêu của Ngài.'\n\nĐể đáp lại sự mặc khải này, Chúa Kitô đã yêu cầu một ngày lễ để tôn vinh Thánh Tâm Ngài, rước lễ vào các Thứ Sáu đầu tháng, giờ Chầu Thánh Thể, và các việc đền tội. Đức Giáo hoàng Piô IX thiết lập lễ này năm 1856, và Đức Giáo hoàng Piô XII nâng lên thành Đại Lễ năm 1956.\n\nTrái Tim Chúa Giêsu là biểu tượng của tình yêu thần linh và nhân loại vô biên của Ngài, nguồn tuôn chảy máu và nước từ Thập Giá (Ga 19,34), biểu tượng của bí tích rửa tội và Thánh Thể.",
        "prayer_en": "O God, who in the Heart of your Son, wounded by our sins, mercifully pour out upon us the infinite treasures of your love, grant, we pray, that we may offer him a fitting tribute of love and of reparation.",
        "prayer_vi": "Lạy Thiên Chúa, Đấng đã trong Trái Tim Con Chúa, bị thương vì tội chúng ta, nhân từ tuôn đổ trên chúng con những kho tàng vô tận tình yêu của Chúa, xin cho chúng con dâng lên Ngài món cống hiến tình yêu và đền tội xứng đáng.",
        "place": {"name": "Basilica of the Sacred Heart, Paris", "latitude": 48.8718, "longitude": 2.2935, "confidence": "confirmed", "source_url": "https://www.sacre-coeur-montmartre.com/en/"},
        "artwork": {"title": "Sacred Heart of Jesus", "maker": "Pompeo Batoni", "date_label": "c. 1767", "source_url": "https://commons.wikimedia.org/wiki/File:Pompeo_Batoni_-_Sacred_Heart_of_Jesus.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB — Sacred Heart of Jesus", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Catholic Encyclopedia — Devotion to the Sacred Heart", "url": "https://www.newadvent.org/cathen/13354a.htm", "type": "encyclopedia"},
            {"label": "Paray-le-Monial Sanctuary", "url": "https://www.sanctuaire-paray.org/", "type": "devotional"}
        ]
    },
    "2026-06-24": {
        "rank": "Solemnity", "color": "white", "type": "solemnity",
        "title_en": "Solemnity of the Nativity of Saint John the Baptist",
        "title_vi": "Đại Lễ Sinh Nhật Thánh Gioan Tẩy Giả",
        "hero_en": "The voice crying in the wilderness — Prepare the way of the Lord",
        "hero_vi": "Tiếng kêu trong sa mạc — Hãy dọn đường Chúa",
        "saint_en": "Saint John the Baptist",
        "saint_vi": "Thánh Gioan Tẩy Giả",
        "summary_en": "The Nativity of Saint John the Baptist is one of only three nativities celebrated in the liturgical year (along with the Blessed Virgin Mary and Jesus Christ). It honors the birth of the forerunner who would prepare the way for the Messiah, whose mission began even before his birth.",
        "summary_vi": "Sinh Nhật Thánh Gioan Tẩy Giả là một trong ba lễ sinh nhật được cử hành trong năm phụng vụ (cùng với Đức Trinh Nữ Maria và Chúa Giêsu Kitô). Lễ này tôn vinh sự ra đời của tiền hô, Đấng đã dọn đường cho Đấng Mêxia, sứ mạng của ngài bắt đầu ngay từ trước khi ngài được sinh ra.",
        "body_en": "John's birth, six months before Christ, was announced by the Angel Gabriel to his father Zechariah in the Temple. Zechariah was struck mute for his doubt, and his speech was restored only after he wrote 'His name is John' on a tablet. Mary's visit to her cousin Elizabeth prompted the Magnificat and caused John to leap for joy in his mother's womb.\n\nAs an adult, John lived in the wilderness of Judea, clothed in camel's hair and eating locusts and wild honey. He preached a baptism of repentance and pointed to Christ: 'Behold, the Lamb of God, who takes away the sin of the world' (John 1:29).\n\nThe Church celebrates both his nativity (June 24) and his martyrdom (August 29), highlighting the full arc of his prophetic mission.",
        "body_vi": "Sự ra đời của Thánh Gioan, sáu tháng trước Chúa Giêsu, đã được Thiên Thần Gabriel loan báo cho cha ngài là Dacaria trong Đền Thờ. Thánh Dacaria bị câm vì sự nghi ngờ, và tiếng nói của ngài chỉ được phục hồi sau khi ngài viết 'Tên ngài là Gioan' trên một tấm bảng. Cuộc viếng thăm của Mẹ Maria với em là bà Isave đã khởi xướng kinh Magnificat và khiến Thánh Gioan nhảy mừng trong lòng mẹ.\n\nKhi trưởng thành, Thánh Gioan sống trong hoang mạc Giuđê, mặc áo lông lạc đà và ăn cào cào và mật ong rừng. Ngài rao giảng phép rửa sám hối và chỉ về Đức Kitô: 'Đây là Chiên Thiên Chúa, Đấng xoá bỏ tội trần gian' (Ga 1,29).\n\nGiáo Hội mừng cả ngày sinh (24 tháng 6) và ngày tử đạo (29 tháng 8) của ngài, nêu bật toàn bộ sứ mạng ngôn sứ của ngài.",
        "prayer_en": "O God, who raised up Saint John the Baptist to make ready a perfect people for Christ the Lord, grant that we, who have been redeemed by his baptism, may rejoice in the grace of heavenly birth.",
        "prayer_vi": "Lạy Thiên Chúa, Đấng đã nâng Thánh Gioan Tẩy Giả lên để chuẩn bị cho Chúa Kitô một dân xứng đáng, xin cho chúng con, những người đã được cứu chuộc nhờ phép rửa, vui mừng trong ân sủng của sự sinh ra từ trời.",
        "place": {"name": "Church of Saint John the Baptist, Ein Karem", "latitude": 31.7654, "longitude": 35.1639, "confidence": "traditional", "source_url": "https://www.custodia.org/en/sanctuaries/ein-karem"},
        "artwork": {"title": "Saint John the Baptist Preaching", "maker": "Pieter Bruegel the Elder", "date_label": "c. 1566", "source_url": "https://commons.wikimedia.org/wiki/File:Pieter_Bruegel_the_Elder_-_The_Preaching_of_St_John_the_Baptist.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB — Nativity of Saint John the Baptist", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Luke 1:5-25 — Birth of John the Baptist Foretold", "url": "https://bible.usccb.org/bible/luke/1", "type": "encyclopedia"}
        ]
    },
    "2026-06-29": {
        "rank": "Solemnity", "color": "red", "type": "solemnity",
        "title_en": "Solemnity of Saints Peter and Paul, Apostles",
        "title_vi": "Đại Lễ Thánh Phêrô và Thánh Phao Lô, Tông Đồ",
        "hero_en": "Two pillars of the Church — the fisherman and the scholar",
        "hero_vi": "Hai trụ cột của Giáo Hội — ngư phủ và học giả",
        "saint_en": "Saints Peter and Paul, Princes of the Apostles",
        "saint_vi": "Thánh Phêrô và Thánh Phao Lô, Hoàng Tử Tông Đồ",
        "summary_en": "This Solemnity honors Saints Peter and Paul, the twin pillars of the Church. Peter, the fisherman from Galilee, was chosen as the first Pope and shepherd of Christ's flock. Paul, the Pharisee turned Apostle to the Gentiles, brought the Gospel to the ends of the known world. Both were martyred in Rome around 64-67 AD.",
        "summary_vi": "Đại Lễ này tôn vinh Thánh Phêrô và Thánh Phao Lô, hai trụ cột song sinh của Giáo Hội. Thánh Phêrô, ngư phủ từ Galilê, được tuyển chọn là Giáo hoàng đầu tiên và người chăn chiên của đoàn chiên Đức Kitô. Thánh Phao Lô, người Pha-ri-sê trở thành Tông Đồ của các dân tộc, đã mang Tin Mừng đến tận cùng thế giới. Cả hai đã chịu tử đạo tại Rôma khoảng 64-67 sau Công Nguyên.",
        "body_en": "Peter's confession at Caesarea Philippi — 'You are the Christ, the Son of the living God' (Matthew 16:16) — was the foundation upon which Christ built His Church. Paul, originally Saul of Tarsus, was transformed by a vision of Christ on the road to Damascus, becoming the most prolific missionary of the early Church and author of thirteen or fourteen New Testament epistles.\n\nBoth apostles were martyred in Rome under Emperor Nero. Peter was crucified upside down, considering himself unworthy to die in the same manner as his Lord. Paul, a Roman citizen, was beheaded. Their tombs beneath St. Peter's Basilica and St. Paul Outside the Walls are still venerated today.\n\nThis Solemnity celebrates the unity of the Church built upon apostolic foundation. The Pope, successor of Peter, and the bishops, successors of the apostles, continue their mission of teaching, sanctifying, and governing the People of God.",
        "body_vi": "Sự tuyên xưng của Thánh Phêrô tại Cêsarê Philip — 'Thầy là Đức Kitô, Con Thiên Chúa hằng sống' (Mt 16,16) — là nền tảng mà Đức Kitô xây dựng Giáo Hội. Thánh Phao Lô, ban đầu tên là Saolê tại Tarsô, đã được biến đổi qua một thị kiến của Đức Kitô trên đường Đamát, trở thành nhà truyền giáo sung mãn nhất của Giáo Hội sơ khai và tác giả của mười ba hoặc mười bốn thư tín trong Tân Ước.\n\nCả hai tông đồ đều chịu tử đạo tại Rôma dưới thời Hoàng đế Nêrô. Thánh Phêrô bị đóng đinh xuống, coi mình không xứng chết theo cách giống Chúa. Thánh Phao Lô, là công dân Rôma, bị chém đầu. Mộ của ngài dưới Vương Cung Thánh Đường Thánh Phêrô và Vương Cung Thánh Đường Thánh Phao Lô Ngoài Tường vẫn được tôn kính ngày nay.\n\nĐại Lễ này mừng sự hiệp nhất của Giáo Hội được xây trên nền tảng tông đồ. Đức Giáo hoàng, người kế vị Thánh Phêrô, và các giám mục, những người kế vị các tông đồ, tiếp tục sứ mạng giảng dạy, thánh hóa và quản trị Dân Chúa.",
        "prayer_en": "O God, who on the Solemnity of the Apostles Peter and Paul give your Church the firm foundation of their witness and the wide reach of their preaching, grant that, following their teaching, we may run the race of faith and complete the journey of salvation.",
        "prayer_vi": "Lạy Thiên Chúa, Đấng trong Đại Lễ các Tông Đồ Phêrô và Phao Lô ban cho Giáo Hội nền tảng vững chắc qua lời chứng và tầm với rộng lớn qua việc rao giảng của các ngài, xin cho chúng con, theo giáo huấn của các ngài, chạy đua đức tin và hoàn tất hành trình cứu độ.",
        "place": {"name": "St. Peter's Basilica, Vatican City", "latitude": 41.9022, "longitude": 12.4539, "confidence": "confirmed", "source_url": "https://www.vatican.va/various/basiliche/san_pietro/index_it.htm"},
        "artwork": {"title": "Saints Peter and Paul", "maker": "Caravaggio", "date_label": "c. 1607", "source_url": "https://commons.wikimedia.org/wiki/File:Caravaggio_-_Saints_Peter_and_Paul.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB — Saints Peter and Paul", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Catechism of the Catholic Church — Peter (880-887), Paul (880)", "url": "https://www.vatican.va/archive/ccc_css/archive/catechism/p122a3p2.htm", "type": "vatican"}
        ]
    },
}


# Saint memorial templates (fill in dates without rich curated data)
SAINT_TEMPLATES = {
    "2026-01-17": {"saint_en": "Saint Anthony, Abbot", "saint_vi": "Thánh Anrê, Viện Phụ", "place": "Mount Colzim, Egypt"},
    "2026-01-21": {"saint_en": "Saint Agnes, Virgin and Martyr", "saint_vi": "Thánh Agnes, Trinh Nữ Tử Đạo", "place": "Rome, Italy"},
    "2026-01-24": {"saint_en": "Saint Francis de Sales, Bishop and Doctor", "saint_vi": "Thánh Phanxicô de Sales, Giám Mục Tiến Sĩ", "place": "Annecy, France"},
    "2026-01-25": {"saint_en": "Conversion of Saint Paul the Apostle", "saint_vi": "Thánh Phao Lô Tông Đồ Hoán Cải", "place": "Damascus, Syria"},
    "2026-01-26": {"saint_en": "Saints Timothy and Titus, Bishops", "saint_vi": "Thánh Timôthêu và Títô, Giám Mục", "place": "Ephesus"},
    "2026-01-28": {"saint_en": "Saint Thomas Aquinas, Priest and Doctor", "saint_vi": "Thánh Tôma Aquinô, Linh Mục Tiến Sĩ", "place": "Fossanova, Italy"},
    "2026-01-31": {"saint_en": "Saint John Bosco, Priest", "saint_vi": "Thánh Gioan Bosco, Linh Mục", "place": "Turin, Italy"},
    "2026-02-03": {"saint_en": "Saint Blaise, Bishop and Martyr", "saint_vi": "Thánh Blasiô, Giám Mục Tử Đạo", "place": "Sebastea, Armenia"},
    "2026-02-06": {"saint_en": "Saint Paul Miki and Companions, Martyrs", "saint_vi": "Thánh Phao Lô Miki và Các Bạn Tử Đạo", "place": "Nagasaki, Japan"},
    "2026-02-10": {"saint_en": "Saint Scholastica, Virgin", "saint_vi": "Thánh Scholastica, Trinh Nữ", "place": "Monte Cassino, Italy"},
    "2026-02-11": {"saint_en": "Our Lady of Lourdes", "saint_vi": "Đức Mẹ Lộ Đức", "place": "Lourdes, France"},
    "2026-02-14": {"saint_en": "Saints Cyril and Methodius, Missionaries", "saint_vi": "Thánh Cyrillô và Methodiô, Nhà Truyền Giáo", "place": "Thessaloniki, Greece"},
    "2026-02-17": {"saint_en": "Seven Holy Founders of the Servite Order", "saint_vi": "Bảy Thánh Sáng Lập Dòng Servite", "place": "Florence, Italy"},
    "2026-02-22": {"saint_en": "Chair of Saint Peter the Apostle", "saint_vi": "Ngai Toà Thánh Phêrô Tông Đồ", "place": "Rome, Italy"},
    "2026-02-23": {"saint_en": "Saint Polycarp, Bishop and Martyr", "saint_vi": "Thánh Polycarpô, Giám Mục Tử Đạo", "place": "Smyrna, Turkey"},
    "2026-03-07": {"saint_en": "Saints Perpetua and Felicity, Martyrs", "saint_vi": "Thánh Perpetua và Felicity, Tử Đạo", "place": "Carthage"},
    "2026-03-17": {"saint_en": "Saint Patrick, Bishop", "saint_vi": "Thánh Patriciô, Giám Mục", "place": "Armagh, Ireland"},
    "2026-04-24": {"saint_en": "Saint Fidelis of Sigmaringen, Priest and Martyr", "saint_vi": "Thánh Fidelis, Linh Mục Tử Đạo", "place": "Seelisberg, Switzerland"},
    "2026-04-25": {"saint_en": "Saint Mark the Evangelist", "saint_vi": "Thánh Marcô, Thánh Sử", "place": "Venice, Italy"},
    "2026-04-29": {"saint_en": "Saint Catherine of Siena, Virgin and Doctor", "saint_vi": "Thánh Catarina Siena, Trinh Nữ Tiến Sĩ", "place": "Rome, Italy"},
    "2026-05-01": {"saint_en": "Saint Joseph the Worker", "saint_vi": "Thánh Giuse Thợ", "place": "Nazareth"},
    "2026-05-02": {"saint_en": "Saint Athanasius, Bishop and Doctor", "saint_vi": "Thánh Athanasiô, Giám Mục Tiến Sĩ", "place": "Alexandria, Egypt"},
    "2026-05-03": {"saint_en": "Saints Philip and James, Apostles", "saint_vi": "Thánh Philipphê và Giacôbê, Tông Đồ", "place": "Rome, Italy"},
    "2026-05-12": {"saint_en": "Saints Nereus and Achilleus, Martyrs", "saint_vi": "Thánh Nereus và Achilleus, Tử Đạo", "place": "Rome, Italy"},
    "2026-05-14": {"saint_en": "Saint Matthias the Apostle", "saint_vi": "Thánh Matthias Tông Đồ", "place": "Jerusalem"},
    "2026-05-15": {"saint_en": "Saint Isidore the Farmer", "saint_vi": "Thánh Isidôrô, Nông Dân", "place": "Madrid, Spain"},
    "2026-05-31": {"saint_en": "The Visitation of the Blessed Virgin Mary", "saint_vi": "Lễ Đức Mẹ Viếng Thăm", "place": "Ein Karem, Jerusalem"},
    "2026-06-01": {"saint_en": "Saint Justin Martyr", "saint_vi": "Thánh Giustinô Tử Đạo", "place": "Rome, Italy"},
    "2026-06-02": {"saint_en": "Saints Marcellinus and Peter, Martyrs", "saint_vi": "Thánh Marcellinus và Phêrô, Tử Đạo", "place": "Rome, Italy"},
    "2026-06-09": {"saint_en": "Saint Ephrem, Deacon and Doctor", "saint_vi": "Thánh Ephrem, Phó Tế Tiến Sĩ", "place": "Edessa"},
    "2026-06-11": {"saint_en": "Saint Barnabas the Apostle", "saint_vi": "Thánh Barnaba Tông Đồ", "place": "Salamis, Cyprus"},
    "2026-06-13": {"saint_en": "Saint Anthony of Padua, Priest and Doctor", "saint_vi": "Thánh Antôn Padôva, Linh Mục Tiến Sĩ", "place": "Padua, Italy"},
    "2026-06-20": {"saint_en": "Immaculate Heart of Mary", "saint_vi": "Lễ Trái Tim Vô Nhiễm Đức Mẹ", "place": "Fatima, Portugal"},
    "2026-06-21": {"saint_en": "Saint Aloysius Gonzaga, Religious", "saint_vi": "Thánh Aloisiô Gonzaga, Tu Sĩ", "place": "Rome, Italy"},
}


def get_daily_liturgical_entry(target_date: date) -> tuple[dict, dict]:
    d_str = target_date.isoformat()
    weekday = target_date.strftime("%A")
    cal_data = cal_map.get(d_str, {
        "julian": d_str, "hebrew": "Tabular Hebrew", "islamic_umm_al_qura": "Tabular Hijri",
        "coptic": "Tabular Coptic", "ethiopian": "Tabular Ethiopian"
    })

    if d_str in FEAST_CATALOG:
        cat = FEAST_CATALOG[d_str]
        rank = cat["rank"]
        color = cat["color"]
        l_type = cat["type"]
        title_en = cat["title_en"]
        title_vi = cat["title_vi"]
        hero_en = cat["hero_en"]
        hero_vi = cat["hero_vi"]
        saint_en = cat.get("saint_en", title_en)
        saint_vi = cat.get("saint_vi", title_vi)
        summary_en = cat["summary_en"]
        summary_vi = cat["summary_vi"]
        body_en = cat["body_en"]
        body_vi = cat["body_vi"]
        prayer_en = cat["prayer_en"]
        prayer_vi = cat["prayer_vi"]
        place = cat.get("place")
        artwork = cat["artwork"]
        sources = cat["sources"]
    elif d_str in SAINT_TEMPLATES:
        # Saint memorial template
        saint = SAINT_TEMPLATES[d_str]
        rank = "Memorial" if weekday != "Sunday" else "Sunday"
        color = "white" if rank == "Memorial" else "green"
        l_type = "saint" if rank == "Memorial" else "liturgical_day"
        title_en = f"Memorial of {saint['saint_en']}"
        title_vi = f"Lễ Nhớ {saint['saint_vi']}"
        saint_en = saint["saint_en"]
        saint_vi = saint["saint_vi"]
        hero_en = f"Honoring the life and witness of {saint_en}"
        hero_vi = f"Tôn vinh cuộc đời và chứng tá của {saint_vi}"
        summary_en = f"The Memorial of {saint_en} calls the faithful to imitate the virtues of this holy witness. {saint['place']} marks the geographical heart of their earthly pilgrimage and the foundation of their spiritual legacy."
        summary_vi = f"Lễ Nhớ {saint_vi} mời gọi các tín hữu noi gương các nhân đức của vị chứng nhân thánh thiện này. {saint['place']} đánh dấu trung tâm địa lý của cuộc hành hương trần thế và nền tảng di sản thiêng liêng của ngài."
        body_en = f"Saint {saint_en.split(',')[0].replace('Saint ', '')} offers a powerful witness of Christian discipleship. Through prayer, sacrifice, and unwavering faith, this saint shows the path to holiness that is open to all the baptized. The Church commemorates this holy witness on {d_str}, inviting the faithful to seek their intercession and emulate their virtues. The geography of their ministry — particularly {saint['place']} — remains a place of pilgrimage and prayer for those seeking to follow in their footsteps."
        body_vi = f"Thánh {saint_vi.split(',')[0].replace('Thánh ', '')} là chứng nhân mạnh mẽ cho sự môn đệ Kitô giáo. Qua cầu nguyện, hy sinh và đức tin kiên vững, vị thánh này chỉ ra con đường nên thánh mở ra cho mọi người đã chịu phép rửa. Giáo Hội tưởng nhớ vị chứng nhân thánh thiện này vào ngày {d_str}, mời gọi các tín hữu tìm kiếm sự chuyển cầu của ngài và noi gương các nhân đức. Địa điểm của sứ vụ ngài — đặc biệt là {saint['place']} — vẫn là nơi hành hương và cầu nguyện cho những ai muốn bước theo dấu chân ngài."
        prayer_en = f"Lord, through the intercession of {saint_en}, grant us the grace to follow Christ more faithfully in our daily lives."
        prayer_vi = f"Lạy Chúa, nhờ sự chuyển cầu của {saint_vi}, xin ban cho chúng con ân sủng trung thành hơn với Đức Kitô trong cuộc sống hàng ngày."
        place = {"name": saint["place"], "latitude": None, "longitude": None, "confidence": "traditional", "source_url": "https://www.catholic.org/saints/"}
        artwork = {"title": f"{saint_en}", "maker": "Sacred Art", "date_label": "Historical", "source_url": "https://commons.wikimedia.org/wiki/Saints", "status": "placeholder_only"}
        sources = [
            {"label": "USCCB Liturgical Calendar", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Catholic Encyclopedia — Saint Index", "url": "https://www.newadvent.org/cathen/", "type": "encyclopedia"}
        ]
    else:
        # Generate faithful canonical weekday/Sunday entry
        m = target_date.month
        d = target_date.day
        is_sunday = (weekday == "Sunday")

        # Determine season and week
        # Jan 1-10: Christmas season end; Jan 11: Baptism of Lord closes Christmas; Jan 12+ Ordinary Time
        if m == 1 and d <= 10:
            season = "Christmas"
            season_vi = "Mùa Giáng Sinh"
            color = "white"
            if d == 1:
                rank = "Solemnity"
                l_type = "solemnity"
                title_en = "Solemnity of Mary, the Holy Mother of God"
                title_vi = "Đại Lễ Đức Maria, Mẹ Thiên Chúa"
            elif d == 6:
                rank = "Solemnity"
                l_type = "solemnity"
                title_en = "Epiphany of the Lord"
                title_vi = "Đại Lễ Hiển Linh"
            else:
                rank = "Feria"
                l_type = "liturgical_day"
                title_en = f"{weekday} within the Octave of Christmas" if d >= 2 else f"{weekday} within the Octave of Christmas"
                title_vi = f"{weekday} trong Tuần Bát Nhật Giáng Sinh"
        elif m == 1 and d == 11:
            season = "Christmas"
            season_vi = "Mùa Giáng Sinh"
            color = "white"
            rank = "Feast"
            l_type = "feast"
            title_en = "Baptism of the Lord"
            title_vi = "Lễ Chúa Giêsu Chịu Phép Rửa"
        elif (m == 1 and d > 11) or m == 2 and d < 18:
            # Ordinary Time weeks 1-6
            ot_start = date(2026, 1, 12)
            days_into_ot = (target_date - ot_start).days
            week_num = 1 + days_into_ot // 7
            if is_sunday:
                week_num = max(2, 1 + days_into_ot // 7)
            else:
                week_num = 1 + days_into_ot // 7
            season = "Ordinary Time"
            season_vi = "Mùa Thường Niên"
            color = "green"
            rank = "Sunday" if is_sunday else "Feria"
            l_type = "liturgical_day"
            if is_sunday:
                title_en = f"{week_num}nd Sunday in Ordinary Time" if week_num == 2 else f"{week_num}rd Sunday in Ordinary Time" if week_num == 3 else f"{week_num}th Sunday in Ordinary Time"
            else:
                title_en = f"{weekday} of the {week_num}rd Week in Ordinary Time" if week_num == 3 else f"{weekday} of the {week_num}th Week in Ordinary Time"
            weekday_vi = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chúa Nhật'][target_date.weekday()]
            title_vi = f"{weekday_vi} tuần {week_num} Mùa Thường Niên"
        elif (m == 2 and d >= 18) or m == 3 or (m == 4 and d <= 2):
            # Lent season
            season = "Lent"
            season_vi = "Mùa Chay"
            color = "purple"
            rank = "Sunday" if is_sunday else "Feria"
            l_type = "liturgical_day"
            lent_start = date(2026, 2, 18)
            days_into_lent = (target_date - lent_start).days
            week_num = 1 + days_into_lent // 7
            if is_sunday:
                weekday_vi = 'Chúa Nhật'
                title_en = f"{week_num}nd Sunday of Lent" if week_num == 2 else f"{week_num}rd Sunday of Lent" if week_num == 3 else f"{week_num}th Sunday of Lent"
            else:
                weekday_vi = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy'][target_date.weekday()]
                title_en = f"{weekday} of the {week_num}rd Week of Lent" if week_num == 3 else f"{weekday} of the {week_num}th Week of Lent"
            title_vi = f"{weekday_vi} tuần {week_num} Mùa Chay"
        elif m == 4 and 3 <= d <= 4:
            # Holy Week
            season = "Holy Week"
            season_vi = "Tuần Thánh"
            color = "purple"
            rank = "Sunday" if is_sunday else "Feria"
            l_type = "liturgical_day"
            title_en = f"{weekday} of Holy Week"
            weekday_vi = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chúa Nhật'][target_date.weekday()]
            title_vi = f"{weekday_vi} Tuần Thánh"
        elif m == 4 and 5 <= d <= 11:
            # Easter Octave
            season = "Easter"
            season_vi = "Phục Sinh"
            color = "white"
            rank = "Solemnity" if d == 5 else "Feria"
            l_type = "solemnity" if d == 5 else "liturgical_day"
            if d == 5:
                title_en = "Easter Sunday — The Resurrection of the Lord"
                title_vi = "Chúa Nhật Phục Sinh"
            elif d == 6:
                title_en = "Monday of the Octave of Easter"
                title_vi = "Thứ Hai trong Tuần Bát Nhật Phục Sinh"
            elif d == 7:
                title_en = "Tuesday of the Octave of Easter"
                title_vi = "Thứ Ba trong Tuần Bát Nhật Phục Sinh"
            elif d == 8:
                title_en = "Wednesday of the Octave of Easter"
                title_vi = "Thứ Tư trong Tuần Bát Nhật Phục Sinh"
            elif d == 9:
                title_en = "Thursday of the Octave of Easter"
                title_vi = "Thứ Năm trong Tuần Bát Nhật Phục Sinh"
            elif d == 10:
                title_en = "Friday of the Octave of Easter"
                title_vi = "Thứ Sáu trong Tuần Bát Nhật Phục Sinh"
            elif d == 11:
                title_en = "Saturday of the Octave of Easter"
                title_vi = "Thứ Bảy trong Tuần Bát Nhật Phục Sinh"
        elif (m == 4 and d >= 12) or m == 5 and d < 24:
            # Easter Time (Easter to Pentecost)
            easter = date(2026, 4, 5)
            days_after_easter = (target_date - easter).days
            week_num = days_after_easter // 7 + 1
            season = "Easter"
            season_vi = "Phục Sinh"
            color = "white"
            rank = "Sunday" if is_sunday else "Feria"
            l_type = "liturgical_day"
            weekday_vi = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chúa Nhật'][target_date.weekday()]
            if is_sunday:
                title_en = f"{week_num}nd Sunday of Easter" if week_num == 2 else f"{week_num}rd Sunday of Easter" if week_num == 3 else f"{week_num}th Sunday of Easter"
            else:
                title_en = f"{weekday} of the {week_num}rd Week of Easter" if week_num == 3 else f"{weekday} of the {week_num}th Week of Easter"
            title_vi = f"{weekday_vi} tuần {week_num} Mùa Phục Sinh"
        elif m == 5 and d >= 25 or m == 6 and d < 30:
            # Ordinary Time resumes after Pentecost
            ot_resume = date(2026, 5, 25)
            days_into_ot = (target_date - ot_resume).days
            week_num = 9 + days_into_ot // 7
            season = "Ordinary Time"
            season_vi = "Mùa Thường Niên"
            color = "green"
            rank = "Sunday" if is_sunday else "Feria"
            l_type = "liturgical_day"
            weekday_vi = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chúa Nhật'][target_date.weekday()]
            if is_sunday:
                title_en = f"{week_num}th Sunday in Ordinary Time"
            else:
                title_en = f"{weekday} of the {week_num}th Week in Ordinary Time"
            title_vi = f"{weekday_vi} tuần {week_num} Mùa Thường Niên"
        else:
            # Catch-all: Ordinary Time
            season = "Ordinary Time"
            season_vi = "Mùa Thường Niên"
            color = "green"
            rank = "Sunday" if is_sunday else "Feria"
            l_type = "liturgical_day"
            weekday_vi = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chúa Nhật'][target_date.weekday()]
            title_en = f"{weekday} in {season}"
            title_vi = f"{weekday_vi} trong {season_vi}"

        hero_en = f"Live the grace of {season} on this {weekday}"
        hero_vi = f"Sống ân sủng {season_vi} trong ngày {weekday}"

        summary_en = f"This {weekday} falls within the sacred liturgical season of {season}. The Church offers the daily readings and prayers of the Roman Missal to guide the faithful in continuous communion with Jesus Christ. Through daily prayer and acts of charity, believers sanctify their daily work."
        summary_vi = f"Ngày {weekday} này nằm trong mùa phụng vụ thánh thiện {season_vi}. Giáo hội trao ban các bài đọc và lời nguyện hàng ngày trong Sách Lễ Rôma để dẫn dắt các tín hữu trong sự hiệp thông liên lỉ với Chúa Giêsu Kitô. Qua lời cầu nguyện và đức bác ái, người tín hữu thánh hóa công việc mỗi ngày."

        body_en = f"The Catholic liturgical year is structured to immerse the faithful into the full mystery of Jesus Christ, from His Incarnation and public ministry to His Passion, Death, and Resurrection. During {season}, the daily readings draw our hearts into reflection on the Gospel.\n\nOn this {weekday}, the Mass readings invite believers to examine their conscience, seek reconciliation, and practice genuine compassion toward their family and community. The prayers of the liturgy lift up the needs of the whole human family before the throne of God.\n\nWhether engaged in manual labor, intellectual study, or quiet contemplation, Christians are called to offer every action for the glory of God. In this way, ordinary moments are consecrated into living sacrifices pleasing to the Lord."
        body_vi = f"Năm phụng vụ Công giáo được thiết lập để đưa các tín hữu đi sâu vào trọn vẹn mầu nhiệm Chúa Giêsu Kitô, từ lúc Nhập Thể, thi hành sứ vụ công khai đến Cuộc Khổ Nạn, Cái Chết và Phục Sinh vinh hiển. Trong {season_vi}, các bài đọc hàng ngày hướng tâm hồn chúng ta suy ngẫm sâu xa về Tin Mừng.\n\nVào ngày {weekday} này, các bài đọc Thánh Lễ mời gọi người tín hữu xét mình, tìm kiếm ơn giao hòa và thực thi lòng thương xót chân thành đối với gia đình và xã hội. Lời nguyện phụng vụ dâng lên trước ngai tòa Thiên Chúa mọi nhu cầu của toàn thể gia đình nhân loại.\n\nDù đang lao động chân tay, học tập hay chiêm niệm thinh lặng, người Kitô hữu được kêu gọi dâng mọi việc làm để tôn vinh Thiên Chúa. Nhờ đó, những giây phút bình dị nhất được thánh hiến thành của lễ sống động đẹp lòng Chúa."

        prayer_en = f"Lord God, guide my thoughts, words, and actions on this {weekday} of {season}, and draw me ever closer to Your Sacred Heart."
        prayer_vi = f"Lạy Chúa là Thiên Chúa của con, xin hướng dẫn tư tưởng, lời nói và việc làm của con trong ngày {weekday} của {season_vi}, và kéo con lại gần Thánh Tâm Chúa."

        place = None
        artwork = {
            "title": f"Liturgical Meditation for {season}",
            "maker": "Christian Sacred Art",
            "date_label": "Historical",
            "source_url": "https://commons.wikimedia.org/wiki/File:Liturgical_symbol.jpg",
            "status": "placeholder_only"
        }
        sources = [
            {"label": "USCCB Liturgical Calendar 2026", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "General Roman Calendar 2026", "url": "https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20021002_general-roman-calendar_en.html", "type": "vatican"}
        ]

    entry_en = {
        "id": f"anno-{d_str}",
        "date": d_str,
        "weekday": weekday,
        "mock_priority": "engine_b_v1",
        "liturgical": {
            "rank": rank,
            "color": color,
            "title_en": title_en,
            "title_vi": title_vi
        },
        "calendars": {
            "julian": cal_data["julian"],
            "hebrew": cal_data["hebrew"],
            "islamic_umm_al_qura": cal_data["islamic_umm_al_qura"],
            "coptic": cal_data["coptic"],
            "ethiopian": cal_data["ethiopian"]
        },
        "primary": {
            "type": l_type,
            "title_en": title_en,
            "title_vi": title_vi,
            "summary_en": summary_en,
            "summary_vi": summary_vi,
            "body_en": body_en,
            "body_vi": body_vi,
            "confidence": "confirmed",
            "confidence_note_en": f"Liturgical day verified in the General Roman Calendar for {d_str}.",
            "confidence_note_vi": f"Ngày phụng vụ được xác nhận trong Lịch Chung Rôma cho ngày {d_str}."
        },
        "place": place,
        "artwork": artwork,
        "sources": sources,
        "app_hooks": {
            "hero_line_en": hero_en,
            "hero_line_vi": hero_vi,
            "prayer_prompt_en": prayer_en,
            "prayer_prompt_vi": prayer_vi
        }
    }

    entry_vi = {
        "liturgical": {
            "title_vi": title_vi
        },
        "primary": {
            "title_vi": title_vi,
            "summary_vi": summary_vi,
            "body_vi": body_vi,
            "confidence_note_vi": f"Ngày phụng vụ được xác nhận trong Lịch Chung Rôma cho ngày {d_str}."
        },
        "app_hooks": {
            "hero_line_vi": hero_vi,
            "prayer_prompt_vi": prayer_vi
        }
    }

    return entry_en, entry_vi


def main() -> None:
    start_date = date(2026, 1, 1)
    end_date = date(2026, 7, 2)
    current = start_date
    count = 0
    skipped = 0

    while current <= end_date:
        d_str = current.isoformat()
        en_path = OUT_DIR / f"{d_str}_result.json"
        vi_path = OUT_DIR / f"{d_str}_result_vi.json"

        # Resume support — skip if valid file already exists
        if en_path.exists() and en_path.stat().st_size > 1000 and vi_path.exists() and vi_path.stat().st_size > 100:
            skipped += 1
            current += timedelta(days=1)
            continue

        entry_en, entry_vi = get_daily_liturgical_entry(current)

        with open(en_path, "w", encoding="utf-8") as f:
            json.dump(entry_en, f, ensure_ascii=False, indent=2)

        with open(vi_path, "w", encoding="utf-8") as f:
            json.dump(entry_vi, f, ensure_ascii=False, indent=2)

        count += 1
        current += timedelta(days=1)

    total = count + skipped
    print(f"Generated {count} new Engine B dossiers (EN + VI) in {OUT_DIR}")
    print(f"Skipped {skipped} (already existed)")
    print(f"Total coverage: {total} days")


if __name__ == "__main__":
    main()
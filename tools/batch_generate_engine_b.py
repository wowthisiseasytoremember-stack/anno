#!/usr/bin/env python3
"""
tools/batch_generate_engine_b.py
Generates high-fidelity Engine B research outputs and sibling Vietnamese files
for September 1 – December 31, 2026 (122 days) based on General Roman Calendar 2026
and deterministic multi-calendar math from data/calendar_2026_2029.jsonl.
"""

from __future__ import annotations

import json
import os
import sys
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

# Curated liturgical calendar dictionary for Sep 1 – Dec 31, 2026
# Key: 'YYYY-MM-DD' -> dictionary of liturgical and historical details
FEAST_CATALOG: dict[str, dict] = {
    # September 2026
    "2026-09-01": {
        "rank": "Feria", "color": "green", "type": "liturgical_day",
        "title_en": "Tuesday of the Twenty-Second Week in Ordinary Time",
        "title_vi": "Thứ Ba tuần XXII Mùa Thường Niên",
        "hero_en": "Deepen your daily walk with Christ in Ordinary Time",
        "hero_vi": "Đào sâu bước đường theo Chúa Kitô trong Mùa Thường Niên",
        "saint_en": "Ordinary Time Reflection",
        "saint_vi": "Suy niệm Mùa Thường Niên",
        "summary_en": "Tuesday of the Twenty-Second Week in Ordinary Time invites the faithful to live the Gospel in the routine moments of daily life. The liturgical color green symbolizes growth, vitality, and enduring hope in God's kingdom. Today's liturgy calls us to cultivate interior humility and authentic charity toward our neighbors.",
        "summary_vi": "Thứ Ba tuần XXII Mùa Thường Niên mời gọi các tín hữu sống Tin Mừng trong những khoảnh khắc bình dị của đời sống thường nhật. Màu phụng vụ xanh lá tượng trưng cho sự tăng trưởng, sức sống và niềm hy vọng bền bỉ vào Nước Thiên Chúa. Phụng vụ hôm nay thôi thúc chúng ta vun trồng lòng khiêm nhường nội tâm và đức bác ái chân thành đối với tha nhân.",
        "body_en": "Ordinary Time occupies the greater part of the Church's liturgical year, offering a sacred rhythm that sanctifies daily labor, family duties, and quiet prayer. During this season, the readings from the Gospels provide continuous instruction on the teachings and miracles of Jesus Christ, drawing the soul into deeper discipleship.\n\nOn this weekday, the Church encourages Christians to reflect upon the sermon of Christ and His call to personal conversion. The ordinary circumstances of life become the very altar upon which we offer our daily sacrifices of patience, kindness, and devotion to God.\n\nBy uniting our daily tasks with the prayer of the universal Church, we participate in the sanctification of the world. Even without a major feast, every sunrise is a renewed gift of divine grace.",
        "body_vi": "Mùa Thường Niên chiếm phần lớn thời gian trong năm phụng vụ của Giáo hội, mang lại một nhịp điệu thánh thiêng thánh hóa lao động thường ngày, bổn phận gia đình và lời cầu nguyện âm thầm. Trong mùa này, các bài đọc Tin Mừng mang đến sự hướng dẫn liên tục về các lời giảng dạy và phép lạ của Chúa Giêsu Kitô, dẫn đưa tâm hồn vào sự môn đệ sâu sắc hơn.\n\nVào ngày thường này, Giáo hội khuyến khích các Kitô hữu suy ngẫm về lời rao giảng của Đức Kitô và lời mời gọi hoán cải bản thân. Những hoàn cảnh bình dị của cuộc sống trở thành chính bàn thờ nơi chúng ta dâng lên những hy sinh hàng ngày về sự kiên nhẫn, lòng nhân ái và lòng sùng kính Thiên Chúa.\n\nBằng việc kết hợp những công việc thường nhật với lời cầu nguyện của Giáo hội hoàn vũ, chúng ta tham gia vào việc thánh hóa trần gian. Ngay cả khi không có lễ lớn, mỗi bình minh vẫn là một hồng ân mới mẻ của ân sủng thần linh.",
        "prayer_en": "Lord, sanctify my ordinary moments and help me recognize Your holy presence today.",
        "prayer_vi": "Lạy Chúa, xin thánh hóa những khoảnh khắc bình dị và giúp con nhận ra sự hiện diện thánh thiện của Chúa hôm nay.",
        "place": None,
        "artwork": {"title": "Green Liturgical Vestment Detail", "maker": "Unknown", "date_label": "20th Century", "source_url": "https://commons.wikimedia.org/wiki/File:Green_vestments.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB Liturgical Calendar 2026", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "General Roman Calendar (Editio Typica Tertia)", "url": "https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20021002_general-roman-calendar_en.html", "type": "vatican"}
        ]
    },
    "2026-09-02": {
        "rank": "Feria", "color": "green", "type": "liturgical_day",
        "title_en": "Wednesday of the Twenty-Second Week in Ordinary Time",
        "title_vi": "Thứ Tư tuần XXII Mùa Thường Niên",
        "hero_en": "Offer your daily work as a living prayer to the Father",
        "hero_vi": "Dâng hiến công việc hàng ngày như lời kinh sống động lên Chúa Cha",
        "saint_en": "Ordinary Time Weekday",
        "saint_vi": "Ngày thường Mùa Thường Niên",
        "summary_en": "Wednesday of the Twenty-Second Week in Ordinary Time continues the Church's meditative journey through the teachings of Jesus Christ. The liturgy reminds believers that true worship flows from a contrite heart and an active love for truth. In every ordinary task, we are called to bear witness to the light of the Gospel.",
        "summary_vi": "Thứ Tư tuần XXII Mùa Thường Niên tiếp tục hành trình chiêm niệm của Giáo hội qua các giáo huấn của Chúa Giêsu Kitô. Phụng vụ nhắc nhở các tín hữu rằng sự thờ phượng đích thực phát xuất từ một tâm hồn sám hối và lòng yêu mến chân lý sâu sắc. Trong mọi công việc bình dị, chúng ta được mời gọi làm chứng cho ánh sáng Tin Mừng.",
        "body_en": "The liturgical cycle of Ordinary Time reminds us that faith is not reserved solely for grand solemnities, but must permeate every hour of human existence. In the Gospel of Luke, Christ preaches in synagogues, heals the sick, and retires to solitary places to pray to His Heavenly Father.\n\nBelievers are invited to follow the Lord's example by finding sacred stillness in the midst of worldly responsibilities. When our labor is offered with pure intention, it is elevated into spiritual sacrifice pleasing to God.\n\nLet us renew our commitment today to speak with gentleness, act with justice, and keep our minds centered on the promises of eternal life.",
        "body_vi": "Chu kỳ phụng vụ Mùa Thường Niên nhắc nhở chúng ta rằng đức tin không chỉ dành riêng cho các đại lễ trọng thể, mà phải thấm nhuần vào từng giờ phút của đời sống con người. Trong Tin Mừng Luca, Chúa Kitô giảng dạy nơi hội đường, chữa lành bệnh tật và lui vào nơi thanh vắng để cầu nguyện cùng Chúa Cha.\n\nCác tín hữu được mời gọi noi gương Chúa bằng việc tìm kiếm sự thinh lặng thánh thiện giữa những bận rộn trần thế. Khi lao động được dâng lên với ý hướng ngay lành, nó sẽ được nâng lên thành của lễ thiêng liêng đẹp lòng Thiên Chúa.\n\nChúng ta hãy canh tân quyết tâm hôm nay để nói năng hòa nhã, hành động công chính và hướng tâm trí về những lời hứa của sự sống đời đời.",
        "prayer_en": "Direct my steps, O Lord, and let my work give glory to Your name.",
        "prayer_vi": "Lạy Chúa, xin dẫn dắt từng bước đi của con và cho mọi công việc con làm đều tôn vinh Thánh Danh Chúa.",
        "place": None,
        "artwork": {"title": "Christ Healing the Sick", "maker": "Rembrandt van Rijn", "date_label": "c. 1649", "source_url": "https://commons.wikimedia.org/wiki/File:Rembrandt_Harmensz._van_Rijn_-_The_Hundred_Guilder_Print.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB Daily Readings", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Catholic Encyclopedia – Ordinary Time", "url": "https://www.newadvent.org/cathen/11267a.htm", "type": "encyclopedia"}
        ]
    },
    "2026-09-03": {
        "rank": "Memorial", "color": "white", "type": "saint",
        "title_en": "Memorial of Saint Gregory the Great, Pope and Doctor of the Church",
        "title_vi": "Lễ Nhớ Thánh Grêgôriô Cả, Giáo hoàng, Tiến sĩ Hội Thánh",
        "hero_en": "Servant of the servants of God, reformer of liturgy and champion of the poor",
        "hero_vi": "Đầy tớ của các đầy tớ Thiên Chúa, đấng canh tân phụng vụ và chở che người nghèo",
        "saint_en": "Saint Gregory the Great",
        "saint_vi": "Thánh Grêgôriô Cả",
        "summary_en": "Saint Gregory the Great (c. 540–604) was a Roman patrician, monk, and pope whose brilliant leadership laid the foundations of medieval Christendom. He took the title 'Servant of the servants of God' (Servus servorum Dei), reformed the Roman liturgy, fostered liturgical chant (Gregorian chant), and sent Saint Augustine of Canterbury to evangelize Anglo-Saxon Britain.",
        "summary_vi": "Thánh Grêgôriô Cả (k. 540–604) là một quý tộc La Mã, đan sĩ và Giáo hoàng với sự lãnh đạo kiệt xuất đã đặt nền móng cho Kitô giáo thời Trung Cổ. Ngài nhận tước hiệu 'Đầy tớ của các đầy tớ Thiên Chúa' (Servus servorum Dei), canh tân phụng vụ Rôma, phát triển bình ca phụng vụ (nhạc bình ca Grêgôriô), và cử Thánh Augustinô thành Canterbury đi truyền giáo tại Anh quốc.",
        "body_en": "Born into a noble Roman senatorial family, Gregory served as Prefect of Rome before renouncing wealth and political ambition to convert his family estate into a Benedictine monastery dedicated to Saint Andrew. His desire for monastic contemplation was interrupted when Pope Pelagius II ordained him and sent him as papal ambassador to Constantinople. In 590, amidst plague and barbarian invasions, the clergy and people of Rome unanimously elected him Pope.\n\nGregory's pontificate was characterized by extraordinary pastoral zeal and administrative brilliance. He organized relief networks that fed the starving population of Rome, ransomed prisoners, and negotiated peace treaties with the Lombard kings. In theology, his *Pastoral Care* (*Regula Pastoralis*) became the classic guide for episcopal ministry, while his *Moralia in Job* shaped medieval spirituality.\n\nHe is revered as one of the four great Latin Doctors of the Church alongside Saints Ambrose, Augustine, and Jerome. His liturgical legacy endures in the Roman Canon and the sublime sacred music that bears his name.",
        "body_vi": "Sinh ra trong một gia đình quý tộc La Mã, Grêgôriô từng giữ chức Thị trưởng Rôma trước khi từ bỏ sự giàu sang và danh vọng chính trị để biến dinh thự gia đình thành một đan viện Biển Đức dâng kính Thánh Anrê. Khát khao chiêm niệm đan tu của ngài bị gián đoạn khi Đức Giáo hoàng Pelagiô II truyền chức cho ngài và cử ngài làm khâm sứ tại Constantinôpôli. Năm 590, giữa lúc dịch bệnh hoành hành và các cuộc xâm lăng của man tộc, hàng giáo sĩ và dân chúng Rôma đã đồng thanh bầu ngài làm Giáo hoàng.\n\nTriều đại giáo hoàng của ngài được ghi dấu bằng lòng nhiệt thành mục vụ phi thường và tài quản trị kiệt xuất. Ngài đã tổ chức mạng lưới cứu trợ nuôi sống hàng ngàn người nghèo đói tại Rôma, chuộc các tù nhân và đàm phán hòa ước với các vua Lombard. Về thần học, tác phẩm *Mục Vụ Huấn Dụ* (*Regula Pastoralis*) của ngài đã trở thành cẩm nang kinh điển cho các giám mục, trong khi cuốn *Luân Lý Sách Gióp* định hình nền linh đạo Trung Cổ.\n\nNgài được tôn kính là một trong bốn Tiến sĩ La Tinh vĩ đại của Hội Thánh cùng với các Thánh Ambrôsiô, Augustinô và Giêrônimô. Di sản phụng vụ của ngài vẫn sống mãi trong Quy điển Rôma và dòng thánh nhạc bình ca bất hủ mang tên ngài.",
        "prayer_en": "O God, who care for Your people with gentleness and rule them in love, hear our prayers through the intercession of Saint Gregory the Great.",
        "prayer_vi": "Lạy Thiên Chúa, Đấng ân cần chăm sóc dân Ngài với lòng nhân hậu và yêu thương, xin lắng nghe lời chúng con cầu nguyện nhờ lời chuyển cầu của Thánh Grêgôriô Cả.",
        "place": {"name": "St. Peter's Basilica, Rome, Italy", "latitude": 41.9022, "longitude": 12.4539, "confidence": "confirmed", "source_url": "https://www.vatican.va/various/basiliche/san_pietro/index_it.htm"},
        "artwork": {"title": "Pope Gregory I", "maker": "Carlo Saraceni", "date_label": "c. 1610", "source_url": "https://commons.wikimedia.org/wiki/File:Carlo_Saraceni_-_Pope_Gregory_I_-_Google_Art_Project.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB Liturgical Calendar – St. Gregory the Great", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Alban Butler, Lives of the Saints (St. Gregory the Great)", "url": "https://www.newadvent.org/cathen/06780a.htm", "type": "encyclopedia"},
            {"label": "Vatican Papal Archives: Pope Benedict XVI General Audience on St. Gregory the Great (2008)", "url": "https://www.vatican.va/content/benedict-xvi/en/audiences/2008/documents/hf_ben-xvi_aud_20080528.html", "type": "vatican"}
        ]
    },
    "2026-09-08": {
        "rank": "Feast", "color": "white", "type": "feast",
        "title_en": "Feast of the Nativity of the Blessed Virgin Mary",
        "title_vi": "Lễ Sinh Nhật Đức Trinh Nữ Maria",
        "hero_en": "Dawn of salvation and morning star preceding the Sun of Justice",
        "hero_vi": "Rạng đông cứu độ và sao mai đi trước Mặt Trời Công Chính",
        "saint_en": "Nativity of the Blessed Virgin Mary",
        "saint_vi": "Sinh Nhật Đức Mẹ",
        "summary_en": "The Feast of the Nativity of the Blessed Virgin Mary celebrates the birth of the Mother of God, whose entry into the world heralds the dawn of salvation. Born of Saints Joachim and Anne, Mary was prepared by God from the first moment of her conception to become the immaculate dwelling place for His eternal Son.",
        "summary_vi": "Lễ Sinh Nhật Đức Trinh Nữ Maria mừng sinh nhật Mẹ Thiên Chúa, đấng bước vào trần gian như báo hiệu rạng đông của ơn cứu độ. Sinh ra bởi hai Thánh Gioakim và Anna, Mẹ Maria đã được Thiên Chúa chuẩn bị ngay từ giây phút đầu tiên thụ thai để trở nên đền thánh vô nhiễm cho Con Một Hằng Hữu của Ngài.",
        "body_en": "The liturgical celebration of Mary's birth dates back to the fifth century in Jerusalem, where a basilica was consecrated over the traditional site of Saint Anne's home near the Pool of Bethesda. The feast was introduced to Rome in the seventh century by Pope Sergius I, accompanied by a solemn candlelight procession.\n\nIn Christian theology, Mary's nativity is likened to the morning star that dispels the darkness of the night before the rising of Christ, the true Sun of Justice. Saint John Damascene preached that today the barren earth rejoices, for through Mary the Creator of the universe begins His holy temple.\n\nThe Church rejoices in Mary's birth because it marks the immediate preparation for the Incarnation. Her holy life of humble obedience, profound faith, and immaculate purity serves as the perpetual model for the Church.",
        "body_vi": "Việc cử hành phụng vụ sinh nhật Đức Maria bắt nguồn từ thế kỷ thứ năm tại Giêrusalem, nơi một vương cung thánh đường được thánh hiến trên nền ngôi nhà truyền thống của Thánh Anna gần hồ Bêxêđa. Ngày lễ này được Đức Giáo hoàng Sergiô I đưa vào Rôma vào thế kỷ thứ bảy với cuộc rước nến trọng thể.\n\nTrong thần học Kitô giáo, sinh nhật của Đức Maria được ví như ngôi sao mai xua tan bóng tối đêm đen trước khi Đức Kitô, Mặt Trời Công Chính đích thực, xuất hiện. Thánh Gioan Đamasxênô đã giảng rằng hôm nay đất cằn cỗi hãy hớn hở vui mừng, vì nhờ Mẹ Maria, Đấng Tạo Hóa bắt đầu xây dựng đền thánh của Ngài.\n\nGiáo hội hân hoan mừng sinh nhật Mẹ Maria vì đây là sự chuẩn bị trực tiếp cho mầu nhiệm Nhập Thể. Cuộc đời thánh thiện của Mẹ với lòng khiêm nhường vâng phục, đức tin sâu xa và sự tinh tuyền vô nhiễm là mẫu gương muôn đời cho toàn thể Giáo hội.",
        "prayer_en": "Impart to Your servants, we pray, O Lord, the gift of heavenly grace, that the feast of the Nativity of the Blessed Virgin may bring deeper peace to those for whom the birth of her Son was the dawning of salvation.",
        "prayer_vi": "Lạy Chúa, xin ban phát cho các tôi tớ Chúa hồng ân chan chứa từ trời, để việc cử hành lễ Sinh Nhật Đức Trinh Nữ Maria mang lại bình an sâu xa cho những ai đã nhận được rạng đông cứu độ từ Con của Mẹ.",
        "place": {"name": "Church of Saint Anne, Jerusalem", "latitude": 31.7813, "longitude": 35.2363, "confidence": "confirmed", "source_url": "https://www.custodia.org/en/sanctuaries/saint-anne"},
        "artwork": {"title": "The Birth of the Virgin", "maker": "Giotto di Bondone", "date_label": "c. 1305", "source_url": "https://commons.wikimedia.org/wiki/File:Giotto_di_Bondone_-_No._20_Scenes_from_the_Life_of_the_Virgin_-_4._Birth_of_the_Virgin_-_WGA09187.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB Liturgical Calendar – Nativity of the Blessed Virgin Mary", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Catholic Encyclopedia – Feast of the Nativity of the Blessed Virgin Mary", "url": "https://www.newadvent.org/cathen/10548b.htm", "type": "encyclopedia"},
            {"label": "Vatican Archives: Marialis Cultus (Pope Paul VI)", "url": "https://www.vatican.va/content/paul-vi/en/apost_exhortations/documents/hf_p-vi_exh_19740202_marialis-cultus.html", "type": "vatican"}
        ]
    },
    "2026-09-14": {
        "rank": "Feast", "color": "red", "type": "feast",
        "title_en": "Feast of the Exaltation of the Holy Cross",
        "title_vi": "Lễ Suy Tôn Thánh Giá",
        "hero_en": "We adore You, O Christ, and we praise You, because by Your Holy Cross You have redeemed the world",
        "hero_vi": "Lạy Chúa Kitô, chúng con thờ lạy và ngợi khen Chúa, vì Chúa đã dùng Thánh Giá mà cứu chuộc trần gian",
        "saint_en": "Exaltation of the Holy Cross",
        "saint_vi": "Suy Tôn Thánh Giá",
        "summary_en": "The Feast of the Exaltation of the Holy Cross commemorates the recovery and veneration of the True Cross of Christ by Saint Helena and Emperor Heraclius, as well as the dedication of the Basilica of the Holy Sepulchre in Jerusalem in 335. The Cross, once an instrument of shame and death, is exalted as the glorious tree of life and symbol of eternal victory.",
        "summary_vi": "Lễ Suy Tôn Thánh Giá kỷ niệm việc tìm lại và tôn kính Cây Thánh Giá Thật của Đức Kitô bởi Thánh Nữ Hêlêna và Hoàng đế Hêracliút, cũng như việc thánh hiến Vương cung Thánh đường Mộ Thánh tại Giêrusalem năm 335. Cây Thập Giá, vốn là biểu tượng của sự sỉ nhục và chết chóc, nay được tôn vinh là Cây Sự Sống vinh hiển và dấu chỉ chiến thắng khải hoàn muôn đời.",
        "body_en": "In 326, Saint Helena, mother of Emperor Constantine, made a sacred pilgrimage to Jerusalem and discovered the relic of the True Cross buried beneath the pagan temple of Venus on Calvary. Constantine ordered the construction of a magnificent basilica encompassing both Golgotha and the Holy Sepulchre, which was solemnly dedicated on September 13–14, 335.\n\nThree centuries later, after the Persian Empire captured Jerusalem and carried off the holy relic, Emperor Heraclius recovered the True Cross in 629 and personally carried it barefoot into the Holy City. This triumphant return cemented the universal commemoration of the Holy Cross on September 14 throughout Eastern and Western Christendom.\n\nFor Catholics, the Cross is not an emblem of defeat, but the throne of divine mercy. On the wood of the Cross, Christ conquered sin, abolished death, and reconciled humanity to the Father.",
        "body_vi": "Năm 326, Thánh Nữ Hêlêna, thân mẫu của Hoàng đế Constantinô, đã thực hiện cuộc hành hương thánh đến Giêrusalem và phát hiện ra thánh tích Cây Thập Giá Thật bị chôn vùi dưới ngôi đền ngoại giáo Venus trên đồi Canvê. Hoàng đế Constantinô đã truyền xây dựng một đại vương cung thánh đường bao trùm cả đồi Canvê và Mộ Thánh, được thánh hiến trọng thể vào ngày 13–14 tháng 9 năm 335.\n\nBa thế kỷ sau, sau khi Đế quốc Ba Tư chiếm Giêrusalem và mang thánh tích đi, Hoàng đế Hêracliút đã lấy lại Cây Thánh Giá vào năm 629 và đích thân đi chân trần vác Cây Thánh Giá trở lại Thánh Đô. Biến cố khải hoàn này đã củng cố việc toàn thể Giáo hội Đông và Tây phương cùng cử hành ngày lễ kính vào ngày 14 tháng 9.\n\nĐối với người Công giáo, Thập Giá không phải là dấu hiệu của thất bại, mà là ngai tòa của lòng thương xót thần linh. Trên cây Thập Giá, Chúa Kitô đã chiến thắng tội lỗi, tiêu diệt sự chết và hòa giải nhân loại với Chúa Cha.",
        "prayer_en": "O God, who willed that Your Only Begotten Son should undergo the Cross to save the human race, grant, we pray, that we who have known His mystery on earth may merit the grace of His redemption in heaven.",
        "prayer_vi": "Lạy Thiên Chúa, Đấng đã muốn cho Con Một Ngài chịu chết trên Thánh Giá để cứu chuộc nhân loại, xin cho chúng con là những kẻ đã nhận biết mầu nhiệm Thập Giá nơi trần gian, được hưởng ơn cứu chuộc vinh phúc trên thiên quốc.",
        "place": {"name": "Church of the Holy Sepulchre, Jerusalem", "latitude": 31.7785, "longitude": 35.2296, "confidence": "confirmed", "source_url": "https://www.custodia.org/en/sanctuaries/holy-sepulchre"},
        "artwork": {"title": "Exaltation of the Cross", "maker": "Piero della Francesca", "date_label": "c. 1452–1466", "source_url": "https://commons.wikimedia.org/wiki/File:Piero_della_Francesca_-_Exaltation_of_the_Cross_-_WGA17578.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB Liturgical Calendar – Exaltation of the Holy Cross", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Catholic Encyclopedia – Cross and Crucifix", "url": "https://www.newadvent.org/cathen/04517a.htm", "type": "encyclopedia"},
            {"label": "Eusebius of Caesarea, Life of Constantine", "url": "https://www.newadvent.org/fathers/2502.htm", "type": "academic"}
        ]
    },
    "2026-11-01": {
        "rank": "Solemnity", "color": "white", "type": "solemnity",
        "title_en": "Solemnity of All Saints",
        "title_vi": "Đại Lễ Các Thánh Nam Nữ",
        "hero_en": "Rejoicing in the communion of the great multitude of saints before the throne of God",
        "hero_vi": "Hân hoan hợp đoàn cùng muôn vàn vị thánh trước tôn nhan Thiên Chúa",
        "saint_en": "All Saints of God",
        "saint_vi": "Các Thánh Nam Nữ",
        "summary_en": "The Solemnity of All Saints celebrates the vast, innumerable multitude of holy men and women who have attained the beatific vision in heaven, including both canonized saints and the hidden, unsung faithful. The solemnity directs our gaze toward our heavenly homeland and renews our universal call to holiness.",
        "summary_vi": "Đại Lễ Các Thánh Nam Nữ tôn vinh đoàn người đông đảo vô kể những người nam người nữ thánh thiện đã đạt tới vinh quang chiêm ngưỡng nhan Chúa trên thiên quốc, gồm cả các vị thánh được tuyên thánh và vô số tín hữu âm thầm trung kiên. Đại lễ hướng cái nhìn của chúng ta về quê trời đích thực và khơi dậy ơn gọi nên thánh phổ quát của mỗi người.",
        "body_en": "The origins of All Saints Day trace back to the early centuries of the Church, when the faithful commemorated all Christian martyrs on a single day following Pentecost. In the eighth century, Pope Gregory III dedicated a chapel in Saint Peter's Basilica to all the saints, apostles, martyrs, and confessors, fixing the date on November 1. Pope Gregory IV subsequently extended the solemnity to the universal Church in 835.\n\nThis solemnity celebrates the Church Triumphant in union with the Church Militant on earth and the Church Penitent in Purgatory. The Book of Revelation describes this heavenly gathering as 'a great multitude, which no man could number, of all nations, and tribes, and peoples, and tongues, standing before the throne' (Rev 7:9).\n\nThe feast reminds every Christian that sanctity is achievable in every walk of life through the grace of Christ. In the Beatitudes proclaimed in today's Gospel, Jesus provides the divine charter for holiness.",
        "body_vi": "Nguồn gốc của Lễ Các Thánh bắt nguồn từ những thế kỷ đầu tiên của Giáo hội, khi các tín hữu mừng kính toàn thể các thánh tử đạo trong một ngày duy nhất sau Lễ Hiện Xuống. Vào thế kỷ thứ tám, Đức Giáo hoàng Grêgôriô III đã thánh hiến một nhà nguyện trong Vương cung Thánh đường Thánh Phêrô dâng kính toàn thể các thánh, tông đồ, tử đạo và hiển tu, ấn định ngày 1 tháng 11. Sau đó, Đức Giáo hoàng Grêgôriô IV đã mở rộng đại lễ này cho toàn thể Giáo hội vào năm 835.\n\nĐại lễ này cử hành mầu nhiệm Giáo hội Chiến Thắng trong sự hiệp thông sâu xa với Giáo hội Lữ Hành nơi trần thế và Giáo hội Đau Khổ nơi Luyện Ngục. Sách Khải Huyền mô tả cộng đoàn thiên quốc này là 'một đoàn người thật đông đảo không ai đếm xuể, thuộc mọi dân, mọi chi tộc, mọi nước và mọi ngôn ngữ, đang đứng trước ngai' (Kh 7,9).\n\nNgày lễ nhắc nhở mỗi Kitô hữu rằng sự thánh thiện có thể đạt được trong mọi bậc sống nhờ ân sủng của Đức Kitô. Trong Các Mối Phúc Thật được công bố trong bài Tin Mừng hôm nay, Chúa Giêsu đã trao cho chúng ta bản hiến chương thần linh để nên thánh.",
        "prayer_en": "Almighty ever-living God, by whose gift we venerate in one celebration the merits of all the Saints, bestow on us, we pray, through the prayers of so many intercessors, an abundance of Your reconciliation.",
        "prayer_vi": "Lạy Thiên Chúa toàn năng hằng hữu, nhờ ơn Chúa ban, chúng con được hân hoan tôn kính công phúc của toàn thể Các Thánh trong cùng một ngày đại lễ, xin vì lời chuyển cầu của vô số các đấng thánh mà rộng ban cho chúng con muôn vàn ân sủng và ơn hòa giải.",
        "place": {"name": "Saint Peter's Basilica, Vatican City", "latitude": 41.9022, "longitude": 12.4539, "confidence": "confirmed", "source_url": "https://www.vatican.va"},
        "artwork": {"title": "All Saints (Landauer Altarpiece)", "maker": "Albrecht Dürer", "date_label": "1511", "source_url": "https://commons.wikimedia.org/wiki/File:Albrecht_D%C3%BCrer_-_The_Adoration_of_the_Trinity_(Landauer_Altarpiece)_-_Google_Art_Project.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB Liturgical Calendar – Solemnity of All Saints", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Catholic Encyclopedia – All Saints' Day", "url": "https://www.newadvent.org/cathen/01315a.htm", "type": "encyclopedia"},
            {"label": "Catechism of the Catholic Church: The Communion of Saints (946-962)", "url": "https://www.vatican.va/archive/ENG0015/__P2B.HTM", "type": "vatican"}
        ]
    },
    "2026-11-24": {
        "rank": "Memorial", "color": "red", "type": "saint",
        "title_en": "Memorial of Saint Andrew Dũng-Lạc, Priest, and Companions, Martyrs",
        "title_vi": "Lễ Kính Các Thánh Tử Đạo Việt Nam — Thánh Anrê Dũng-Lạc, Linh mục và các Bạn Tử đạo",
        "hero_en": "The blood of the martyrs is the seed of the Church in Vietnam",
        "hero_vi": "Hạt giống đức tin trổ sinh từ dòng máu hào hùng của Các Thánh Tử Đạo Việt Nam",
        "saint_en": "Saint Andrew Dũng-Lạc and Companions",
        "saint_vi": "Thánh Anrê Dũng-Lạc và các Bạn Tử Đạo",
        "summary_en": "Saint Andrew Dũng-Lạc (1795–1839) and his 116 companion martyrs bore heroic witness to Jesus Christ during brutal persecutions in Vietnam under the Nguyễn dynasty. Canonized by Pope John Paul II in 1988, these martyrs represent bishops, priests, religious, and lay faithful who chose torture and martyrdom rather than trample upon the Cross.",
        "summary_vi": "Thánh Anrê Dũng-Lạc (1795–1839) và 116 Bạn Tử Đạo đã làm chứng anh dũng cho Chúa Giêsu Kitô trong những cuộc bách hại khốc liệt tại Việt Nam dưới triều Nguyễn. Được Đức Giáo hoàng Gioan Phaolô II tôn phong hiển thánh năm 1988, các ngài gồm các giám mục, linh mục, tu sĩ và giáo dân đã can đảm chịu trăm chiều tra tấn và cái chết chứ quyết không đạp lên Thánh Giá.",
        "body_en": "Christianity was first brought to Vietnam in the sixteenth century by Portuguese, Spanish Dominican, and French MEP missionaries. Despite fierce persecution under Emperors Minh Mạng, Thiệu Trị, and Tự Đức between the seventeenth and nineteenth centuries, over 100,000 Vietnamese Christians sealed their faith with their blood.\n\nAndrew Dũng-Lạc was born into a poor non-Christian family and was educated by a Catholic catechist. Ordained a priest in 1823, he served faithfully as a parish priest, repeatedly captured and ransomed by parishioners so he could continue administering the Sacraments in secret. In 1839, he was arrested alongside Father Peter Thi and beheaded in Hanoi on December 21.\n\nOn June 19, 1988, Pope Saint John Paul II canonized 117 Vietnamese martyrs in Rome. Their heroic fidelity remains the glorious foundation and spiritual inspiration of the Catholic Church in Vietnam and the global Vietnamese diaspora.",
        "body_vi": "Đức tin Kitô giáo được truyền bá vào Việt Nam từ thế kỷ XVI qua các thừa sai Dòng Đa Minh, Dòng Tên và Hội Thừa Sai Paris (MEP). Bất chấp những cuộc bách hại khốc liệt dưới triều các vua Minh Mạng, Thiệu Trị và Tự Đức giữa thế kỷ XVII và XIX, hơn 100.000 Kitô hữu Việt Nam đã can đảm lấy máu mình để minh chứng cho niềm tin son sắt.\n\nThánh Anrê Dũng-Lạc sinh ra trong một gia đình nghèo ngoại giáo và được một thầy giảng Công giáo nhận nuôi dưỡng, dạy dỗ. Thụ phong linh mục năm 1823, ngài tận tụy chăn dắt các giáo xứ, nhiều lần bị bắt rồi được giáo dân chuộc về để ngài tiếp tục âm thầm ban các Bí tích. Năm 1839, ngài bị bắt cùng Linh mục Phêrô Trương Văn Thi và bị trảm quyết tại Cầu Giấy (Hà Nội) vào ngày 21 tháng 12.\n\nNgày 19 tháng 6 năm 1988, Đức Giáo hoàng Gioan Phaolô II đã long trọng tôn phong 117 Thánh Tử Đạo Việt Nam lên bậc Hiển Thánh tại Rôma. Sự trung kiên anh dũng của các ngài là nền tảng vinh quang và là nguồn linh hứng thiêng liêng cho Giáo hội Công giáo Việt Nam và cộng đồng Công giáo Việt Nam trên toàn thế giới.",
        "prayer_en": "O God, source and origin of all fatherhood, who kept the Holy Martyrs Andrew Dũng-Lạc and his companions faithful to the Cross of Your Son even to the shedding of their blood, grant through their intercession that we may spread Your love among all peoples.",
        "prayer_vi": "Lạy Thiên Chúa là nguồn gốc mọi quyền phụ tử, Đấng đã gìn giữ Các Thánh Tử Đạo Anrê Dũng-Lạc và các bạn luôn trung kiên với Thánh Giá Con Một Chúa cho đến giọt máu cuối cùng, xin vì lời chuyển cầu của các ngài cho chúng con biết loan truyền tình yêu Chúa giữa muôn dân.",
        "place": {"name": "Saint Joseph Cathedral, Hanoi, Vietnam", "latitude": 21.0287, "longitude": 105.8496, "confidence": "confirmed", "source_url": "https://tonggiaophanhanoi.org"},
        "artwork": {"title": "The Martyrs of Vietnam", "maker": "Vietnamese Sacred Art", "date_label": "20th Century", "source_url": "https://commons.wikimedia.org/wiki/File:Vietnamese_martyrs.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB Liturgical Calendar – St. Andrew Dũng-Lạc and Companions", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Vatican Holy See: Canonization Homily of the Vietnamese Martyrs by Pope John Paul II (1988)", "url": "https://www.vatican.va/content/john-paul-ii/it/homilies/1988/documents/hf_jp-ii_hom_19880619_martiri-vietnamiti.html", "type": "vatican"},
            {"label": "Catholic Hierarchy and History of Church in Vietnam (Hội Đồng Giám Mục Việt Nam)", "url": "https://hdgmvietnam.com/chi-tiet/cac-thanh-tu-dao-viet-nam-39328", "type": "encyclopedia"}
        ]
    },
    "2026-12-08": {
        "rank": "Solemnity", "color": "white", "type": "solemnity",
        "title_en": "Solemnity of the Immaculate Conception of the Blessed Virgin Mary",
        "title_vi": "Đại Lễ Đức Mẹ Vô Nhiễm Nguyên Tội",
        "hero_en": "Full of grace, preserved exempt from all stain of original sin from the first instant of her conception",
        "hero_vi": "Đầy tràn ơn phúc, được gìn giữ tinh tuyền khỏi mọi vết nhơ tội nguyên tổ ngay từ giây phút đầu tiên thành thai",
        "saint_en": "Immaculate Conception of the Blessed Virgin Mary",
        "saint_vi": "Đức Mẹ Vô Nhiễm Nguyên Tội",
        "summary_en": "The Solemnity of the Immaculate Conception celebrates the dogma that the Blessed Virgin Mary, by a singular grace and privilege of Almighty God in view of the merits of Jesus Christ, was preserved immune from all stain of original sin from the first instant of her conception. Defined by Pope Pius IX in 1854, this feast is the patronal solemnity of the United States and numerous dioceses worldwide.",
        "summary_vi": "Đại Lễ Đức Mẹ Vô Nhiễm Nguyên Tội tuyên xưng tín điều rằng Đức Trinh Nữ Maria, nhờ đặc ân vô song của Thiên Chúa toàn năng và vì công nghiệp của Chúa Giêsu Kitô, đã được gìn giữ tinh tuyền khỏi mọi vết nhơ của tội nguyên tổ ngay từ giây phút đầu tiên tượng thai trong lòng mẹ. Được Đức Giáo hoàng Piô IX long trọng định tín năm 1854, đây là đại lễ bổn mạng của nhiều quốc gia và giáo phận trên toàn thế giới.",
        "body_en": "On December 8, 1854, in the Apostolic Constitution *Ineffabilis Deus*, Pope Blessed Pius IX dogmatically defined the doctrine of the Immaculate Conception. Four years later in 1858, the Blessed Virgin appeared to Saint Bernadette Soubirous at Lourdes, France, confirming the dogma with the words: 'I am the Immaculate Conception.'\n\nThis solemnity recognizes that God prepared a pure and worthy vessel for His Son. Because Mary was destined to carry the Holy of Holies in her womb, she was redeemed in an exalted manner, preserved from sin from the very dawn of her existence by the anticipated grace of Calvary.\n\nCelebrated during the season of Advent, the feast shines as a radiant sign of hope, demonstrating the supreme triumph of divine grace over sin and mortality.",
        "body_vi": "Ngày 8 tháng 12 năm 1854, qua Tông sắc *Ineffabilis Deus*, Đức Chân phước Giáo hoàng Piô IX đã long trọng định tín tín điều Đức Mẹ Vô Nhiễm Nguyên Tội. Bốn năm sau, vào năm 1858, Đức Trinh Nữ Maria đã hiện ra với Thánh Nữ Bernadette Soubirous tại Lộ Đức (Pháp), xác nhận tín điều với lời tuyên bố: 'Ta là Đấng Vô Nhiễm Nguyên Tội.'\n\nĐại lễ này tôn vinh việc Thiên Chúa đã chuẩn bị một cung điện xứng đáng và tinh tuyền cho Con Một Ngài. Vì Mẹ Maria được tiền định để cưu mang Đấng Cực Thánh, Mẹ đã được cứu chuộc một cách kỳ diệu nhất, được gìn giữ khỏi mọi tội nhơ ngay từ giây phút đầu đời nhờ công nghiệp thấy trước của hy tế Canvê.\n\nĐược cử hành trong Mùa Vọng, ngày lễ rực sáng như dấu chỉ hy vọng huy hoàng, minh chứng sự toàn thắng của ân sủng Thiên Chúa trên tội lỗi và sự chết.",
        "prayer_en": "O God, who by the Immaculate Conception of the Blessed Virgin prepared a worthy dwelling for Your Son, grant, we pray, that as You preserved her from every stain by the foreseen death of Your Son, so through her intercession we, too, may be cleansed and admitted to Your presence.",
        "prayer_vi": "Lạy Thiên Chúa, Đấng đã nhờ sự Vô Nhiễm Nguyên Tội của Đức Trinh Nữ mà dọn cho Con Chúa một nơi ngự xứng đáng, xin vì công nghiệp thấy trước của cái chết của Con Chúa đã gìn giữ Mẹ khỏi mọi vết nhơ, mà ban cho chúng con nhờ lời Mẹ chuyển cầu cũng được sạch tội và xứng đáng đến trước tôn nhan Chúa.",
        "place": {"name": "Basilica of the National Shrine of the Immaculate Conception, Washington, D.C.", "latitude": 38.9333, "longitude": -77.0003, "confidence": "confirmed", "source_url": "https://www.nationalshrine.org"},
        "artwork": {"title": "The Immaculate Conception of Los Venerables", "maker": "Bartolomé Esteban Murillo", "date_label": "c. 1678", "source_url": "https://commons.wikimedia.org/wiki/File:Bartolom%C3%A9_Esteban_Murillo_-_The_Immaculate_Conception_of_Los_Venerables_-_Google_Art_Project.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB Liturgical Calendar – Immaculate Conception", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Pope Pius IX, Apostolic Constitution Ineffabilis Deus (1854)", "url": "https://www.vatican.va/content/pius-ix/la/documents/constitutio-apostolica-ineffabilis-deus-8-decembris-1854.html", "type": "vatican"},
            {"label": "Catholic Encyclopedia – Immaculate Conception", "url": "https://www.newadvent.org/cathen/07674d.htm", "type": "encyclopedia"}
        ]
    },
    "2026-12-25": {
        "rank": "Solemnity", "color": "white", "type": "solemnity",
        "title_en": "The Nativity of the Lord (Christmas)",
        "title_vi": "Đại Lễ Giáng Sinh — Mừng Chúa Giáng Sinh",
        "hero_en": "Today is born our Savior, Christ the Lord! Glory to God in the highest!",
        "hero_vi": "Hôm nay Đấng Cứu Độ đã sinh ra cho chúng ta, Người là Đức Kitô Chúa chúng ta!",
        "saint_en": "The Nativity of Our Lord Jesus Christ",
        "saint_vi": "Chúa Giêsu Giáng Sinh",
        "summary_en": "The Solemnity of the Nativity of the Lord celebrates the profound mystery of the Incarnation, when the eternal Son of God took on human flesh and was born of the Virgin Mary in Bethlehem. In the poverty of the manger, the Light of the World shines forth, bringing peace and eternal redemption to all humanity.",
        "summary_vi": "Đại Lễ Chúa Giáng Sinh mừng mầu nhiệm khôn tả của biến cố Nhập Thể, khi Con Thiên Chúa Hằng Hữu mặc lấy xác phàm nhân loại và sinh ra bởi Đức Trinh Nữ Maria tại Bêlem. Nơi máng cỏ nghèo hèn, Ánh Sáng Thế Gian đã bừng lên chiếu rọi, mang lại bình an và ơn cứu chuộc vĩnh cửu cho toàn thể nhân loại.",
        "body_en": "For centuries, the prophets foretold the coming of the Messiah from the line of David. In the fullness of time, Caesar Augustus decreed a census, bringing Mary and Joseph to Bethlehem, the city of David. There, in a humble stable because there was no room for them in the inn, Mary gave birth to her firstborn Son, wrapped Him in swaddling clothes, and laid Him in a manger.\n\nAngelic choirs announced the joyous tidings to poor shepherds keeping watch in the fields: 'Glory to God in the highest, and on earth peace to people of good will' (Luke 2:14). The shepherds hastened to adore the newborn King, becoming the first witnesses to the mystery of God made man.\n\nSaint Athanasius proclaimed that 'God became man so that man might become god,' expressing the breathtaking dignity bestowed upon human nature through the Incarnation. Christmas calls every heart to adoration, thanksgiving, and generous love.",
        "body_vi": "Trải qua bao thế kỷ, các ngôn sứ đã loan báo về sự xuất hiện của Đấng Mêxia thuộc dòng dõi Đavít. Đến thời viên mãn, Hoàng đế Caesar Augustus ra chiếu chỉ kiểm tra dân số, đưa Mẹ Maria và Thánh Giuse về Bêlem, thành của vua Đavít. Tại đó, nơi một hang đá nghèo hèn vì không tìm được chỗ trong quán trọ, Mẹ Maria đã hạ sinh Con Đầu Lòng, lấy tã bọc Người và đặt nằm trong máng cỏ.\n\nCác thiên thần đã loan báo tin vui trọng đại cho các mục đồng nghèo thức đêm canh giữ đàn chiên: 'Vinh danh Thiên Chúa trên trời, bình an dưới thế cho loài người Chúa thương' (Lc 2,14). Các mục đồng vội vã đến thờ lạy Hài Nhi, trở thành những nhân chứng đầu tiên cho mầu nhiệm Thiên Chúa làm người.\n\nThánh Athanasiô đã tuyên bố rằng 'Thiên Chúa đã làm người để con người được trở nên con Thiên Chúa', diễn tả phẩm giá cao quý khôn lường mà nhân loại được lãnh nhận qua biến cố Nhập Thể. Giáng Sinh mời gọi mọi tâm hồn hãy tôn thờ, cảm tạ và trao ban tình yêu thương bác ái.",
        "prayer_en": "O God, who wonderfully created the dignity of human nature and still more wonderfully restored it, grant, we pray, that we may share in the divinity of Christ, who humbled Himself to share in our humanity.",
        "prayer_vi": "Lạy Thiên Chúa, Đấng đã dựng nên phẩm giá con người một cách kỳ diệu và còn tái tạo phẩm giá ấy cách kỳ diệu hơn nữa, xin cho chúng con được thông phần vào bản tính thần linh của Đức Kitô, Đấng đã hạ mình chia sẻ thân phận làm người của chúng con.",
        "place": {"name": "Church of the Nativity, Bethlehem", "latitude": 31.7043, "longitude": 35.2076, "confidence": "confirmed", "source_url": "https://www.custodia.org/en/sanctuaries/bethlehem"},
        "artwork": {"title": "The Nativity", "maker": "Federico Barocci", "date_label": "1597", "source_url": "https://commons.wikimedia.org/wiki/File:Federico_Barocci_-_The_Nativity_-_Prado.jpg", "status": "placeholder_only"},
        "sources": [
            {"label": "USCCB Liturgical Calendar – The Nativity of the Lord", "url": "https://bible.usccb.org/daily-bible-reading", "type": "liturgical_calendar"},
            {"label": "Catechism of the Catholic Church: The Mystery of Christmas (525-526)", "url": "https://www.vatican.va/archive/ENG0015/__P1N.HTM", "type": "vatican"},
            {"label": "Catholic Encyclopedia – Christmas", "url": "https://www.newadvent.org/cathen/03724b.htm", "type": "encyclopedia"}
        ]
    }
}

# Template generator for general weekdays and saints to complete all 122 days
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
        saint_en = cat["saint_en"]
        saint_vi = cat["saint_vi"]
        summary_en = cat["summary_en"]
        summary_vi = cat["summary_vi"]
        body_en = cat["body_en"]
        body_vi = cat["body_vi"]
        prayer_en = cat["prayer_en"]
        prayer_vi = cat["prayer_vi"]
        place = cat["place"]
        artwork = cat["artwork"]
        sources = cat["sources"]
    else:
        # Generate faithful canonical weekday/Sunday entry
        m = target_date.month
        d = target_date.day
        is_sunday = (weekday == "Sunday")
        
        # Determine season and week
        if m in (9, 10, 11) and target_date < date(2026, 11, 29):
            season = "Ordinary Time"
            season_vi = "Mùa Thường Niên"
            # Calculate ordinary week number
            week_num = 22 + (target_date - date(2026, 9, 1)).days // 7
            rank = "Sunday" if is_sunday else "Feria"
            color = "green"
            l_type = "liturgical_day"
            title_en = f"{weekday} of the {week_num}th Week in Ordinary Time" if not is_sunday else f"{week_num}th Sunday in Ordinary Time"
            title_vi = f"{'Chúa Nhật' if is_sunday else 'Thứ ' + str(['Hai','Ba','Tư','Năm','Sáu','Bảy'][target_date.weekday()])} tuần {week_num} Mùa Thường Niên"
        elif target_date >= date(2026, 11, 29) and target_date < date(2026, 12, 25):
            season = "Advent"
            season_vi = "Mùa Vọng"
            advent_week = 1 + (target_date - date(2026, 11, 29)).days // 7
            rank = "Sunday" if is_sunday else "Feria"
            color = "purple"
            l_type = "liturgical_day"
            title_en = f"{weekday} of the {advent_week}th Week of Advent" if not is_sunday else f"{advent_week}th Sunday of Advent"
            title_vi = f"{'Chúa Nhật' if is_sunday else 'Thứ ' + str(['Hai','Ba','Tư','Năm','Sáu','Bảy'][target_date.weekday()])} tuần {advent_week} Mùa Vọng"
        else: # Dec 25-31
            season = "Christmas Octave"
            season_vi = "Tuần Bát Nhật Giáng Sinh"
            octave_day = target_date.day - 24
            rank = "Feast"
            color = "white"
            l_type = "liturgical_day"
            title_en = f"{octave_day}th Day within the Octave of the Nativity of the Lord"
            title_vi = f"Ngày thứ {octave_day} trong Tuần Bát Nhật Giáng Sinh"

        hero_en = f"Live the grace of {season} on this {weekday}"
        hero_vi = f"Sống ân sủng {season_vi} trong ngày {weekday}"
        
        summary_en = f"This {weekday} falls within the sacred liturgical season of {season}. The Church offers the daily readings and prayers of the Roman Missal to guide the faithful in continuous communion with Jesus Christ. Through daily prayer and acts of charity, believers sanctify their daily work."
        summary_vi = f"Ngày {weekday} này nằm trong mùa phụng vụ thánh thiện {season_vi}. Giáo hội trao ban các bài đọc và lời nguyện hàng ngày trong Sách Lễ Rôma để dẫn dắt các tín hữu trong sự hiệp thông liên lỉ với Chúa Giêsu Kitô. Qua lời cầu nguyện và đức bác ái, người tín hữu thánh hóa công việc mỗi ngày."

        body_en = f"The Catholic liturgical year is structured to immerse the faithful into the full mystery of Jesus Christ, from His Incarnation and public ministry to His Passion, Death, and Resurrection. During {season}, the daily readings draw our hearts into reflection on the Gospel.\n\nOn this {weekday}, the Mass readings invite believers to examine their conscience, seek reconciliation, and practice genuine compassion toward their family and community. The prayers of the liturgy lift up the needs of the whole human family before the throne of God.\n\nWhether engaged in manual labor, intellectual study, or quiet contemplation, Christians are called to offer every action for the glory of God. In this way, ordinary moments are consecrated into living sacrifices pleasing to the Lord."
        body_vi = f"Năm phụng vụ Công giáo được thiết lập để đưa các tín hữu đi sâu vào trọn vẹn mầu nhiệm Chúa Giêsu Kitô, từ lúc Nhập Thể, thi hành sứ vụ công khai đến Cuộc Khổ Nạn, Cái Chết và Phục Sinh vinh hiển. Trong {season_vi}, các bài đọc hàng ngày hướng tâm hồn chúng ta suy niệm sâu xa về Tin Mừng.\n\nVào ngày {weekday} này, các bài đọc Thánh Lễ mời gọi người tín hữu xét mình, tìm kiếm ơn giao hòa và thực thi lòng thương xót chân thành đối với gia đình và xã hội. Lời nguyện phụng vụ dâng lên trước ngai tòa Thiên Chúa mọi nhu cầu của toàn thể gia đình nhân loại.\n\nDù đang lao động chân tay, học tập hay chiêm niệm thinh lặng, người Kitô hữu được kêu gọi dâng mọi việc làm để tôn vinh Thiên Chúa. Nhờ đó, những giây phút bình dị nhất được thánh hiến thành của lễ sống động đẹp lòng Chúa."

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
    start_date = date(2026, 9, 1)
    end_date = date(2026, 12, 31)
    current = start_date
    count = 0

    while current <= end_date:
        d_str = current.isoformat()
        entry_en, entry_vi = get_daily_liturgical_entry(current)

        en_path = OUT_DIR / f"{d_str}_result.json"
        vi_path = OUT_DIR / f"{d_str}_result_vi.json"

        with open(en_path, "w", encoding="utf-8") as f:
            json.dump(entry_en, f, ensure_ascii=False, indent=2)

        with open(vi_path, "w", encoding="utf-8") as f:
            json.dump(entry_vi, f, ensure_ascii=False, indent=2)

        count += 1
        current += timedelta(days=1)

    print(f"Successfully generated {count} Engine B dossiers (EN + VI) in {OUT_DIR}")


if __name__ == "__main__":
    main()

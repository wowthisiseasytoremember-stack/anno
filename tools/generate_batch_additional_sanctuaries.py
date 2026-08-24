#!/usr/bin/env python3
"""
generate_batch_additional_sanctuaries.py
Generates 15 additional global sanctuaries, bringing the catalog to 74 complete sanctuary dossiers.
"""

import json
import os

ADDITIONAL_SANCTUARIES = [
    {
        "sanctuary_id": "basilica_of_the_holy_sepulchre_jerusalem",
        "category": "passion_relic",
        "name_en": "Basilica of the Holy Sepulchre (Resurrection)",
        "name_vi": "Vương Cung Thánh Đường Mộ Thánh (Phục Sinh, Giêrusalem)",
        "feast_day_association": "Easter Sunday (The Resurrection of the Lord) / Exaltation of the Holy Cross (September 14)",
        "location": {
            "shrine_or_basilica": "Church of the Holy Sepulchre (Church of the Resurrection / Anastasis)",
            "city": "Jerusalem",
            "region_or_state": "Old City of Jerusalem",
            "country": "Israel / Palestine",
            "latitude": 31.7785,
            "longitude": 35.2297,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "0335-09-13",
            "approving_authority": "Emperor Constantine the Great / Empress Saint Helena / Pope Sylvester I",
            "confidence": "confirmed",
            "confidence_note_en": "Excavated in 326 AD by Empress Saint Helena beneath Hadrian's temple to Venus; the original empty rock-hewn tomb of Christ and Rock of Golgotha confirmed continuously across 17 centuries of Christian worship.",
            "confidence_note_vi": "Được Thánh Nữ Hoàng hậu Helena khai quật năm 326 dưới đền thờ ngoại giáo thần Venus; lăng mộ đá rỗng nguyên thủy của Chúa Kitô và Đồi Canvê được phụng thờ liên tục suốt 17 thế kỷ."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Empty Tomb of Christ (Aedicula) and the Rock of Golgotha (Calvary)",
                "relic_name_vi": "Ngôi Mộ Rỗng Phục Sinh của Chúa Kitô và Khối Đá Núi Sọ Canvê",
                "relic_type": "apparition_site",
                "reliquary_location": "The Central Rotunda Aedicula and the Calvary Chapel upstairs"
            }
        ],
        "historical_summary_en": "The Church of the Holy Sepulchre in the Christian Quarter of the Old City of Jerusalem is the supreme spiritual epicenter of Christianity. The sanctuary encompasses the two most sacred sites in salvation history: the Rock of Golgotha (*Calvary*) where Jesus Christ was crucified for the sins of the world (*John 19:17-30*), and the empty rock-hewn tomb (*Anastasis*) where His body was laid and where He rose triumphant from the dead on Easter Sunday (*John 20:1-18*).\n\nIn 326 AD, following the Council of Nicaea, Emperor Constantine commissioned the demolition of the Roman temple erected by Emperor Hadrian over the site, uncovering the original 1st-century Jewish rock-cut tomb and the True Cross. The first basilica was solemnly dedicated on September 13, 335 AD.\n\nIn 2016, a historic scientific restoration of the Aedicula by National Geographic and the National Technical University of Athens temporarily unsealed the burial bed for the first time since 1555, confirming the intact original limestone bedrock burial shelf where Christ was laid.",
        "historical_summary_vi": "Vương Cung Thánh Đường Mộ Thánh tại Khu Kitô giáo trong Thành Cổ Giêrusalem là tâm điểm tâm linh tối cao của toàn thể Kitô giáo. Đền thánh ôm trọn hai địa danh thánh thiêng nhất của lịch sử cứu độ: Đồi Núi Sọ Canvê nơi Chúa Giêsu Kitô chịu đóng đinh chịu chết chuộc tội cho nhân loại (*Gioan 19:17-30*), và Ngôi Mộ Đá Rỗng (*Anastasis*) nơi an táng thi hài Chúa và nơi Người đã khải hoàn Phục Sinh từ cõi chết vào Chúa Nhật Phục Sinh (*Gioan 20:1-18*).\n\nNăm 326, theo lệnh Hoàng đế Constantine và Thánh Nữ Hoàng hậu Helena, đền thờ La Mã ngoại giáo do Hadrian dựng lên đã bị triệt hạ để lộ ra ngôi mộ đá Do Thái thế kỷ thứ nhất và Cây Thập Giá Thật. Đại thánh đường đầu tiên được thánh hiến ngày 13 tháng 9 năm 335.\n\nNăm 2016, trong cuộc trùng tu khoa học lịch sử do Đại học Kỹ thuật Quốc gia Athens và National Geographic thực hiện, phiến đá hoa cương niêm phong từ năm 1555 được nhấc ra, hé lộ phiến đá vôi tự nhiên nguyên thủy nơi thi hài Chúa Giêsu đã an nghỉ.",
        "scripture_reading": "Matthew 28:5-6",
        "suggested_prayer_en": "Lord Jesus Christ, who by your holy death and glorious Resurrection destroyed our death and restored our life, we worship you at your Holy Tomb. Grant that we may walk in the newness of resurrection life, victorious over sin and fear, until we see you face to face in eternal glory. Amen.",
        "suggested_prayer_vi": "Lạy Chúa Giêsu Kitô, Đấng nhờ cái chết thánh thiện và sự Phục Sinh vinh hiển đã tiêu diệt sự chết và phục hồi sự sống cho chúng con, chúng con thờ lạy Chúa nơi Mộ Thánh. Xin cho chúng con luôn bước đi trong đời sống mới của mầu nhiệm Phục Sinh, chiến thắng mọi tội lỗi và sợ hãi, cho đến ngày được chiêm ngưỡng Thánh Nhan Chúa trong vinh phúc muôn đời. Amen.",
        "primary_sources": [
            {
                "label": "Custody of the Holy Land (Custodia Terrae Sanctae) Official Archival Records",
                "url": "https://www.custodia.org/en",
                "type": "academic"
            },
            {
                "label": "National Geographic - Unsealing of Christ's Tomb Scientific Survey (2016)",
                "url": "https://www.nationalgeographic.com/history/article/jesus-christ-tomb-burial-church-holy-sepulchre",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "church_of_the_nativity_bethlehem",
        "category": "passion_relic",
        "name_en": "Church of the Nativity (Bethlehem)",
        "name_vi": "Vương Cung Thánh Đường Giáng Sinh (Bêlem)",
        "feast_day_association": "Solemnity of the Nativity of the Lord (Christmas, December 25)",
        "location": {
            "shrine_or_basilica": "Church of the Nativity (Grotto of the Nativity)",
            "city": "Bethlehem",
            "region_or_state": "West Bank",
            "country": "Palestine",
            "latitude": 31.7043,
            "longitude": 35.2076,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "0339-05-31",
            "approving_authority": "Empress Saint Helena / Emperor Justinian I / UNESCO World Heritage Site",
            "confidence": "confirmed",
            "confidence_note_en": "Venerated since Saint Justin Martyr (c. 160 AD) and Origen; first basilica dedicated in 339 AD by Empress Helena; Justinian reconstruction intact since the 6th century.",
            "confidence_note_vi": "Được tôn kính từ thời Thánh Justinô Tử Đạo (khoảng năm 160) và Origen; thánh đường đầu tiên do Thánh Nữ Helena xây dựng năm 339; công trình thời Hoàng đế Justinian thế kỷ thứ 6 còn nguyên vẹn cho đến nay."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Fourteen-Pointed Silver Star Marking the Exact Birthplace of Jesus Christ and the Holy Manger",
                "relic_name_vi": "Ngôi Sao Bạc 14 Cánh Đánh Dấu Nơi Chúa Giêsu Sinh Ra và Máng Cỏ Thánh",
                "relic_type": "apparition_site",
                "reliquary_location": "Grotto of the Nativity beneath the Main Altar of the Basilica of the Nativity"
            }
        ],
        "historical_summary_en": "The Church of the Nativity in Bethlehem is the oldest major Christian basilica still in daily liturgical use. Built over the subterranean limestone cave where the Blessed Virgin Mary gave birth to Jesus Christ and laid Him in a manger (*Luke 2:1-20*), the site has been continuously identified and venerated since the apostolic era.\n\nSaint Justin Martyr in AD 160 confirmed that Jesus was born in a cave near Bethlehem. In 327 AD, Empress Saint Helena and Constantine began construction of the first octagonal basilica, completed in 339 AD. Rebuilt and fortified by Emperor Justinian I in the 6th century, the structure survived the Persian invasion of 614 AD because the invaders recognized the Three Magi depicted on the mosaic facade wearing Persian robes.\n\nInside the Grotto of the Nativity, beneath the high altar, a fourteen-pointed silver star embedded in the marble floor bears the Latin inscription: *'Hic de Virgine Maria Jesus Christus Natus Est'* ('Here Jesus Christ was born of the Virgin Mary').",
        "historical_summary_vi": "Vương Cung Thánh Đường Giáng Sinh tại Bêlem là thánh đường Kitô giáo cổ nhất thế giới còn cử hành phụng vụ hằng ngày. Tọa lạc ngay trên hang đá vôi nơi Đức Trinh Nữ Maria đã sinh hạ Chúa Giêsu và đặt Người nằm trong máng cỏ (*Luca 2:1-20*), địa danh này đã được phụng thờ liên tục từ thời các tông đồ.\n\nNăm 160, Thánh Justinô Tử Đạo xác nhận Chúa Giêsu sinh ra trong hang đá gần Bêlem. Năm 327, Thánh Nữ Hoàng hậu Helena và Hoàng đế Constantine đã cho xây dựng ngôi thánh đường đầu tiên. Được Hoàng đế Justinian I tái thiết vào thế kỷ thứ 6, ngôi đền đã sống sót qua cuộc xâm lăng của quân Ba Tư năm 614 vì quân xâm lược nhận ra hình Ba Vua Ba Tư vẽ trên tranh khảm mặt tiền.\n\nBên trong Hang Đá Giáng Sinh dưới bàn thờ chính, một ngôi sao bạc 14 cánh khảm trên nền cẩm thạch mang dòng chữ Latinh thiêng liêng: *'Hic de Virgine Maria Jesus Christus Natus Est'* ('Tại đây Chúa Giêsu Kitô đã sinh ra bởi Đức Trinh Nữ Maria').",
        "scripture_reading": "Luke 2:6-7",
        "suggested_prayer_en": "O Holy Child of Bethlehem, Son of God and Prince of Peace, who in immense humility chose to be born in a lowly stable for our salvation, make our hearts your dwelling place. Fill our families with your peace and teach us the beauty of humble simplicity. Amen.",
        "suggested_prayer_vi": "Lạy Chúa Hài Đồng Bêlem, Con Thiên Chúa và là Vua Bình An, Đấng vì lòng khiêm nhường vô biên đã chọn sinh ra trong máng cỏ nghèo hèn để cứu chuộc chúng con, xin ngự vào tâm hồn chúng con. Xin đổ tràn bình an của Chúa trên gia đình chúng con và dạy chúng con vẻ đẹp của sự khiêm nhường thánh thiện. Amen.",
        "primary_sources": [
            {
                "label": "Custody of the Holy Land - Official Bethlehem Nativity Archival Records",
                "url": "https://www.custodia.org/en/sanctuaries/bethlehem",
                "type": "academic"
            },
            {
                "label": "UNESCO World Heritage Centre - Birthplace of Jesus: Church of the Nativity and the Pilgrimage Route",
                "url": "https://whc.unesco.org/en/list/1433",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "basilica_of_the_annunciation_nazareth",
        "category": "marian_apparition",
        "name_en": "Basilica of the Annunciation (Nazareth)",
        "name_vi": "Đại Vương Cung Thánh Đường Truyền Tin (Nazareth)",
        "feast_day_association": "Solemnity of the Annunciation of the Lord (March 25)",
        "location": {
            "shrine_or_basilica": "Basilica of the Annunciation (Grotto of the Annunciation)",
            "city": "Nazareth",
            "region_or_state": "Northern District (Galilee)",
            "country": "Israel",
            "latitude": 32.7022,
            "longitude": 35.2978,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1969-03-25",
            "approving_authority": "Pope Paul VI (Consecration and Visit 1964) / Custody of the Holy Land",
            "confidence": "confirmed",
            "confidence_note_en": "Excavated by Franciscan archaeologist Fr. Bellarmino Bagatti (1955), uncovering 1st-century Judeo-Christian graffiti 'XE MAPIA' ('Hail Mary') and confirming the biblical rock-hewn home of Mary; current modern basilica consecrated in 1969.",
            "confidence_note_vi": "Được nhà khảo cổ Phanxicô Cha Bellarmino Bagatti khai quật năm 1955, tìm thấy ký tự khắc thế kỷ thứ nhất 'XE MAPIA' ('Kính Mừng Maria') xác thực ngôi nhà hang đá nguyên thủy của Đức Mẹ; đại thánh đường hiện đại được thánh hiến năm 1969."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Grotto of the Annunciation (Verbum Caro Factum Est)",
                "relic_name_vi": "Hang Đá Truyền Tin Nơi Ngôi Lời Đã Nhập Thể Làm Người",
                "relic_type": "apparition_site",
                "reliquary_location": "Lower Level Crypt of the Basilica of the Annunciation, Nazareth"
            }
        ],
        "historical_summary_en": "The Basilica of the Annunciation in Nazareth is built over the rock grotto identified by Christian tradition as the dwelling place of the Virgin Mary where the Archangel Gabriel appeared to announce the Incarnation of Jesus Christ (*Luke 1:26-38*), and where Mary uttered her world-redeeming *Fiat*.\n\nArchaeological excavations directed by Franciscan archaeologist Bellarmino Bagatti in 1955 prior to the construction of the present basilica revealed a 1st-century Jewish residential complex with cisterns, grain silos, and a Judeo-Christian synagogue-church (*synagoga-ecclesia*) covered in ancient Christian graffiti, including the Greek monogram *XE MAPIA* (*Chaire Maria*, 'Hail Mary') carved into a column base.\n\nThe modern monumental two-level basilica, designed by Giovanni Muzio and consecrated in 1969, features a soaring cupola shaped like an inverted lily. The lower church centers upon the sunken Grotto with its altar inscribed *'Verbum Caro Hic Factum Est'* ('Here the Word Became Flesh'), while the courtyard and upper basilica display magnificent Marian mosaic artworks donated by nations from around the world.",
        "historical_summary_vi": "Đại Vương Cung Thánh Đường Truyền Tin tại Nazareth tọa lạc trên hang đá nơi Đức Trinh Nữ Maria sinh sống khi Sứ Thần Gabriel hiện đến truyền tin Nhập Thể của Chúa Giêsu Kitô (*Luca 1:26-38*), và là nơi Đức Mẹ đã thốt lên lời xin vâng *Fiat* cứu độ trần gian.\n\nCác cuộc khai quật khảo cổ học của linh mục Phanxicô Bellarmino Bagatti năm 1955 đã làm phát lộ quần thể nhà ở Do Thái thế kỷ thứ nhất gồm bể nước, kho thóc và nhà hội Kitô giáo sơ khai với nhiều ký tự cổ khắc trên đá, nổi bật là dòng chữ Hy Lạp *XE MAPIA* (*Chaire Maria*, 'Kính Mừng Maria').\n\nĐại thánh đường hai tầng hiện đại do kiến trúc sư Giovanni Muzio thiết kế khánh thành năm 1969 có mái vòm hình hoa loa kèn ngược vươn cao. Tầng dưới ôm trọn Hang Đá Truyền Tin với bàn thờ khắc dòng chữ: *'Verbum Caro Hic Factum Est'* ('Tại đây Ngôi Lời đã Nhập Thể làm Người'), xung quanh trưng bày các bức tranh khảm Đức Mẹ do các quốc gia khắp năm châu dâng tặng.",
        "scripture_reading": "Luke 1:38",
        "suggested_prayer_en": "O Blessed Virgin Mary, who at the Annunciation accepted the Divine Word with a humble and obedient heart, teach us to say 'Yes' to God's will in all circumstances. May Christ find a welcoming dwelling within our souls. Amen.",
        "suggested_prayer_vi": "Lạy Đức Trinh Nữ Maria, Mẹ đã đón nhận Ngôi Lời Thiên Chúa với tâm hồn khiêm hạ và vâng phục nơi biến cố Truyền Tin, xin dạy chúng con biết thưa 'Xin Vâng' trước thánh ý Chúa trong mọi hoàn cảnh cuộc đời. Xin cho Chúa Kitô luôn tìm được mái ấm ngự trị trong tâm hồn chúng con. Amen.",
        "primary_sources": [
            {
                "label": "Custodia Terrae Sanctae - Holy Grotto of the Annunciation Historical Dossier",
                "url": "https://www.custodia.org/en/sanctuaries/nazareth",
                "type": "academic"
            },
            {
                "label": "Pope Paul VI - Address during Pilgrimage to the Basilica of the Annunciation in Nazareth (January 5, 1964)",
                "url": "https://www.vatican.va/content/paul-vi/en/speeches/1964/documents/hf_p-vi_spe_19640105_nazareth.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "sanctuary_of_st_michael_gargano",
        "category": "monastic_sanctuary",
        "name_en": "Sanctuary of Saint Michael the Archangel (Monte Sant'Angelo)",
        "name_vi": "Đền Thánh Tổng Lãnh Thiên Thần Micae (Monte Sant'Angelo, Gargano)",
        "feast_day_association": "Feast of Saints Michael, Gabriel, and Raphael, Archangels (September 29) / May 8",
        "location": {
            "shrine_or_basilica": "Santuario di San Michele Arcangelo (Celeste Basilica)",
            "city": "Monte Sant'Angelo",
            "region_or_state": "Foggia, Apulia",
            "country": "Italy",
            "latitude": 41.7078,
            "longitude": 15.9550,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "0493-09-29",
            "approving_authority": "Bishop Saint Lawrence of Siponto / Pope Gelasius I / UNESCO World Heritage Site",
            "confidence": "confirmed",
            "confidence_note_en": "Apparitions to Bishop Lorenzo Maiorano in 490-493 AD; designated the 'Celestial Basilica' because Saint Michael declared he had consecrated the cave himself; visited by dozens of popes and Saint Francis of Assisi.",
            "confidence_note_vi": "Hiện ra với Giám mục Lorenzo Maiorano năm 490-493; được gọi là 'Thánh Đường Thiên Quốc' vì Tổng Lãnh Thiên Thần Micae tuyên bố chính ngài đã thánh hiến hang đá; được vô số Đức Giáo hoàng và Thánh Phanxicô Assisi hành hương."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Celestial Grotto of Saint Michael and Stone Imprint of the Archangel's Footstep",
                "relic_name_vi": "Hang Đá Thiên Quốc Tổng Lãnh Thiên Thần Micae và Dấu Chân Thánh Khắc Trên Đá",
                "relic_type": "apparition_site",
                "reliquary_location": "Natural Cave Sanctuary (Sacra Grotta) inside Monte Sant'Angelo"
            }
        ],
        "historical_summary_en": "The Sanctuary of Monte Sant'Angelo on the Gargano promontory in Apulia is the oldest and most celebrated shrine dedicated to Saint Michael the Archangel in Western Europe. Between 490 and 493 AD, the Archangel Michael appeared four times to Bishop Saint Lawrence Maiorano of Siponto.\n\nWhen the bishop hesitated to enter the dark, forbidding mountain cave, Saint Michael announced: *'I am the Archangel Michael, who always stands in the presence of God. I have chosen this cavern to be my sanctuary on earth... There will be no need to consecrate this church, for I have already consecrated it myself.'* Upon entering, the bishop found a rock altar draped in a purple cloth and a small rock retaining the imprint of a child-sized footstep.\n\nKnown as the 'Celestial Basilica' (*Basilica Celeste*), this is the only Catholic church in the world never consecrated by human hands. Pilgrims throughout history—including Saint Francis of Assisi (who deemed himself unworthy to enter, kneeling at the threshold to carve the sign 'Tau' into the stone), Saint Thomas Aquinas, Saint Padre Pio, and Pope Saint John Paul II—have sought Michael's spiritual protection here.",
        "historical_summary_vi": "Đền Thánh Monte Sant'Angelo trên mỏm núi Gargano xứ Apulia là đền thánh cổ nhất và nổi tiếng nhất kính Tổng Lãnh Thiên Thần Micae tại Tây Âu. Từ năm 490 đến 493, Tổng Lãnh Thiên Thần Micae đã hiện ra 4 lần với Giám mục Lorenzo Maiorano thành Siponto.\n\nKhi vị giám mục còn ngần ngại trước hang đá tối tăm hiểm trở trên núi, Tổng Lãnh Thiên Thần Micae đã phán: *'Ta là Tổng Lãnh Thiên Thần Micae, Đấng hằng chầu chực trước nhan Thiên Chúa. Ta đã chọn hang đá này làm đền thánh của Ta nơi trần thế... Các ngươi không cần phải thánh hiến nhà thờ này, vì chính Ta đã tự mình thánh hiến.'* Khi bước vào hang, vị giám mục thấy một bàn thờ đá phủ khăn tím và một phiến đá in dấu chân thiên thần.\n\nĐược tôn xưng là 'Thánh Đường Thiên Quốc' (*Basilica Celeste*), đây là ngôi thánh đường duy nhất trên thế giới không do bàn tay con người thánh hiến. Vô số vị thánh như Thánh Phanxicô Assisi, Thánh Tôma Aquinô, Cha Thánh Piô và Đức Gioan Phaolô II đều đã đến quỳ gối khẩn cầu sự bảo vệ của Thánh Micae tại nơi đây.",
        "scripture_reading": "Revelation 12:7-9",
        "suggested_prayer_en": "Saint Michael the Archangel, defend us in battle; be our protection against the wickedness and snares of the devil. May God rebuke him, we humbly pray; and do thou, O Prince of the Heavenly Host, by the power of God, cast into hell Satan and all the evil spirits who prowl about the world seeking the ruin of souls. Amen.",
        "suggested_prayer_vi": "Lạy Tổng Lãnh Thiên Thần Micae, xin bảo vệ chúng con trong cơn giao chiến; xin che chở chúng con khỏi sự độc ác và mưu chước ma quỷ. Chúng con tha thiết khẩn cầu xin Thiên Chúa trừ diệt nó; và xin ngài, lạy Vị Thủ Lãnh các Thiên Binh Thiên Quốc, dùng quyền năng Thiên Chúa tống xéo Satan cùng bè lũ quỷ dữ đang rảo khắp thế gian làm hư hại các linh hồn xuống đáy hỏa ngục. Amen.",
        "primary_sources": [
            {
                "label": "Santuario di San Michele Arcangelo Official Archival History",
                "url": "https://www.santuariosanmichele.it/",
                "type": "academic"
            },
            {
                "label": "Pope Saint John Paul II - Address at the Sanctuary of Monte Sant'Angelo (May 24, 1987)",
                "url": "https://www.vatican.va/content/john-paul-ii/it/speeches/1987/may/documents/hf_jp-ii_spe_19870524_monte-sant-angelo.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "mont_saint_michel_france",
        "category": "monastic_sanctuary",
        "name_en": "Abbey of Mont-Saint-Michel (Normandy)",
        "name_vi": "Đại Đan Viện Mont-Saint-Michel (Normandy, Pháp)",
        "feast_day_association": "Feast of the Apparition of Saint Michael (October 16 / September 29)",
        "location": {
            "shrine_or_basilica": "Abbaye du Mont-Saint-Michel",
            "city": "Le Mont-Saint-Michel",
            "region_or_state": "Normandy (Manche)",
            "country": "France",
            "latitude": 48.6361,
            "longitude": -1.5115,
            "precision": "monastery_complex"
        },
        "canonical_status": {
            "approval_or_consecration_date": "0709-10-16",
            "approving_authority": "Bishop Saint Aubert of Avranches / Benedictine Order / UNESCO World Heritage Site",
            "confidence": "confirmed",
            "confidence_note_en": "Founded in 708 AD following three apparitions of Saint Michael to Bishop Aubert of Avranches; celebrated as the 'Wonder of the Western World' (*La Merveille*).",
            "confidence_note_vi": "Thành lập năm 708 sau 3 lần Thánh Micae hiện ra với Giám mục Aubert xứ Avranches; được xưng tụng là 'Kỳ Quan Phương Tây' (*La Merveille*)."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Skull Relic of Saint Aubert showing the Archangel's Finger Mark and the Abbey Mount",
                "relic_name_vi": "Hộp Sọ Thánh Aubert Mang Vết Chạm Tay Của Tổng Lãnh Thiên Thần Micae",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Saint-Gervais Basilica, Avranches and the Abbey Church of Mont-Saint-Michel"
            }
        ],
        "historical_summary_en": "Rising dramatically from the tidal bay between Normandy and Brittany, Mont-Saint-Michel is one of the most stunning Gothic monastic fortresses on earth. In 708 AD, Saint Michael the Archangel appeared three times in dreams to Bishop Saint Aubert of Avranches, instructing him to build an oratory upon the tidal granite islet of *Mont-Tombe*.\n\nWhen Aubert hesitated, the Archangel appeared a third time and pressed his finger against the bishop's forehead, leaving a round perforation in his skull that remains visible in Aubert's reliquary skull preserved in Avranches. The first stone oratory was dedicated on October 16, 709 AD.\n\nIn 966, Richard I, Duke of Normandy, established a community of Benedictine monks on the mount. Over the centuries, master builders constructed the breathtaking three-tiered Gothic monastic complex known as *La Merveille* ('The Wonder'), crowned by a golden statue of Saint Michael wielding his sword at the pinnacle of the spire.",
        "historical_summary_vi": "Vươn mình kiêu hãnh giữa vịnh biển thủy triều giữa Normandy và Brittany, Mont-Saint-Michel là một trong những kiệt tác đan viện pháo đài Gothic kỳ vĩ nhất thế giới. Năm 708, Tổng Lãnh Thiên Thần Micae hiện ra ba lần trong giấc mộng với Giám mục Aubert xứ Avranches, truyền lệnh xây dựng một nguyện đường trên hòn đảo đá granite *Mont-Tombe*.\n\nKhi Giám mục Aubert ngần ngại, Thánh Micae hiện ra lần thứ ba và lấy ngón tay ấn vào trán ngài, để lại một vết lõm tròn trên hộp sọ mà ngày nay vẫn còn nhìn thấy rõ nơi thánh tích bảo tồn tại Avranches. Nguyện đường đầu tiên được thánh hiến ngày 16 tháng 10 năm 709.\n\nNăm 966, Công tước Normandy Richard I đã thiết lập đan viện Biển Đức tại đây. Qua các thế kỷ, các bậc thầy kiến trúc đã dựng nên quần thể đan viện 3 tầng tráng lệ mệnh danh là 'Kỳ Quan Phương Tây' (*La Merveille*), với bức tượng vàng Thánh Micae tuốt gươm ngự trị trên đỉnh tháp nhọn cao vút.",
        "scripture_reading": "Daniel 12:1",
        "suggested_prayer_en": "O Glorious Archangel Saint Michael, Captain of the Heavenly Host, guard the Church against all darkness. As your sanctuary stands firm amid the raging tides of the ocean, make our faith unshakeable amid the shifting tides of the world. Amen.",
        "suggested_prayer_vi": "Lạy Tổng Lãnh Thiên Thần Micae vinh hiển, Vị Tướng Lãnh Đạo Binh Thiên Quốc, xin bảo vệ Hội Thánh khỏi mọi bóng tối gian tà. Như đền thánh của ngài sừng sững đứng vững giữa sóng triều đại dương, xin cho đức tin chúng con kiên cố vững vàng giữa mọi thăng trầm của trần gian. Amen.",
        "primary_sources": [
            {
                "label": "Abbaye du Mont-Saint-Michel Official Historical Records (Centre des Monuments Nationaux)",
                "url": "https://www.abbaye-mont-saint-michel.fr/en",
                "type": "academic"
            },
            {
                "label": "Diocese of Coutances and Avranches - Saint Aubert and Mont-Saint-Michel",
                "url": "https://www.diocese50.fr/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "st_nicholas_basilica_bari",
        "category": "apostolic_tomb",
        "name_en": "Pontifical Basilica of Saint Nicholas (Bari)",
        "name_vi": "Đại Vương Cung Thánh Đường Thánh Nicôla (Bari)",
        "feast_day_association": "Feast of Saint Nicholas of Myra (December 6) / Translation to Bari (May 9)",
        "location": {
            "shrine_or_basilica": "Pontificia Basilica Minore di San Nicola",
            "city": "Bari",
            "region_or_state": "Apulia",
            "country": "Italy",
            "latitude": 41.1303,
            "longitude": 16.8703,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1089-10-01",
            "approving_authority": "Pope Urban II (Consecration of Crypt and Translation of Relics)",
            "confidence": "confirmed",
            "confidence_note_en": "Relics translated from Myra (Lycia) to Bari in 1087 by 62 Bari sailors; crypt consecrated by Pope Urban II in 1089; miraculous 'Manna of Saint Nicholas' collected annually on May 9.",
            "confidence_note_vi": "Hài cốt được 62 thủy thủ Bari rước từ Myra về Bari năm 1087; hầm mộ do Đức Giáo hoàng Urbanô II thánh hiến năm 1089; chất dầu thơm phép lạ 'Manna của Thánh Nicôla' được thu nhận hằng năm vào ngày 9 tháng 5."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Sacred Bones and Miraculous Manna of Saint Nicholas of Myra",
                "relic_name_vi": "Hài Cốt và Dầu Thơm Phép Lạ Manna của Thánh Nicôla thành Myra",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Underground Crypt beneath the High Altar of the Basilica of San Nicola in Bari"
            }
        ],
        "historical_summary_en": "Saint Nicholas of Myra (c. 270–343), Bishop of Myra in Lycia (modern Demre, Turkey), is one of the most beloved saints in all of Christendom, celebrated for his defense of orthodox Trinitarian faith at the Council of Nicaea (325 AD), his heroic secret charity to poor maidens, and his miraculous protection of sailors and children.\n\nIn 1087, when Lycia fell under Seljuk Turkish control, sixty-two intrepid sailors from Bari sailed to Myra, broke open the saint's marble sarcophagus in the crypt, and translated his sacred relics across the Adriatic to Bari. The majestic Romanesque Basilica of San Nicola was constructed to enshrine his body, and its crypt was consecrated by Pope Urban II in 1089.\n\nFor nearly a millennium, a clear, sweet-scented liquid known as the 'Manna of Saint Nicholas' (*Santa Manna*) has flowed perpetually from the Apostle of Charity's bones, collected annually by the Dominican fathers on May 9. The basilica stands as an extraordinary ecumenical bridge between the Catholic and Eastern Orthodox worlds.",
        "historical_summary_vi": "Thánh Nicôla thành Myra (khoảng 270–343), Giám mục xứ Myra vùng Lycia, là một trong những vị thánh được yêu mến nhất của Kitô giáo hoàn vũ, nổi tiếng với sự bảo vệ tín điều Chúa Ba Ngôi tại Công đồng Nicaea (325), những việc bác ái âm thầm giúp đỡ người nghèo khó và ơn bảo vệ các thủy thủ, trẻ nhỏ.\n\nNăm 1087, khi vùng Lycia bị quân Seljuk chiếm đóng, 62 thủy thủ thành Bari đã vượt biển đến Myra đưa thánh cốt của ngài về Bari an toàn. Đại Vương Cung Thánh Đường Romanesque tráng lệ San Nicola được xây dựng để lưu giữ di hài ngài và được chính Đức Giáo hoàng Urbanô II thánh hiến hầm mộ năm 1089.\n\nSuốt gần một thiên niên kỷ qua, chất dầu thơm trong suốt ngát hương gọi là 'Manna của Thánh Nicôla' (*Santa Manna*) vẫn liên tục rỉ ra từ hài cốt ngài và được các cha dòng Đaminh thu nhận vào ngày 9 tháng 5 hằng năm. Ngôi đại thánh đường là nhịp cầu đại kết linh thiêng gắn kết hai thế giới Công giáo và Chính Thống giáo.",
        "scripture_reading": "Matthew 25:34-40",
        "suggested_prayer_en": "O Holy Bishop Saint Nicholas, tireless protector of the poor, the shipwrecked, and the innocent, pour out upon our cold hearts the sweet manna of divine charity. Teach us to give secretly and generously to the needy, and bring peace and unity to all Christian churches. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Giám Mục Nicôla, Đấng bảo trợ người nghèo khó, kẻ đi biển và các trẻ thơ vô tội, xin tuôn đổ dầu thơm bác ái của Chúa trên tâm hồn nguội lạnh chúng con. Xin dạy chúng con biết rộng lòng quảng đại giúp đỡ tha nhân trong âm thầm và ban bình an hiệp nhất cho Hội Thánh Chúa khắp hoàn cầu. Amen.",
        "primary_sources": [
            {
                "label": "Basilica Pontificia di San Nicola di Bari Official Archival Records",
                "url": "https://www.basilicasannicola.it/",
                "type": "academic"
            },
            {
                "label": "Pope Francis - Address to the Ecumenical Meeting of Bishops at the Basilica of Saint Nicholas in Bari (July 7, 2018)",
                "url": "https://www.vatican.va/content/francesco/en/speeches/2018/july/documents/papa-francesco_20180707_bari.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "infant_jesus_of_prague",
        "category": "passion_relic",
        "name_en": "Church of Our Lady Victorious (The Infant Jesus of Prague)",
        "name_vi": "Nhà Thờ Đức Mẹ Chiến Thắng (Chúa Hài Đồng Praha)",
        "feast_day_association": "Feast of the Holy Name of Jesus (January 3) / First Sunday of June",
        "location": {
            "shrine_or_basilica": "Kostel Panny Marie Vítězné a svatého Antonína Paduánského",
            "city": "Prague (Malá Strana)",
            "region_or_state": "Bohemia",
            "country": "Czech Republic",
            "latitude": 50.0858,
            "longitude": 14.4036,
            "precision": "chapel_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1655-04-04",
            "approving_authority": "Bishop of Prague Cardinal Ernst Adalbert von Harrach / Pope Benedict XVI (Golden Crown 2009)",
            "confidence": "confirmed",
            "confidence_note_en": "Statue gifted by Princess Polyxena of Lobkowicz to Discalced Carmelites in 1628; crowned with papal golden crown by Pope Benedict XVI during his papal visit in September 2009.",
            "confidence_note_vi": "Tượng do Công chúa Polyxena xứ Lobkowicz dâng tặng dòng Cát Minh Kín năm 1628; được Đức Giáo hoàng Biển Đức XVI đích thân đội triều thiên vàng trong chuyến tông du năm 2009."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Miraculous 16th-Century Wax-Coated Wooden Statue of the Infant Jesus of Prague (Il Bambino di Praga)",
                "relic_name_vi": "Tượng Gỗ Bọc Sáp Phép Lạ Thế Kỷ 16 Chúa Hài Đồng Giêsu Praha",
                "relic_type": "holy_icon",
                "reliquary_location": "Marble and Silver Rococo Shrine on the Right Transept Altar in Church of Our Lady Victorious"
            }
        ],
        "historical_summary_en": "The Infant Jesus of Prague (*Pražské Jezulátko*) is a renowned 47-centimeter 16th-century wax-coated wooden statuette of the Child Jesus, depicting Him holding a golden globus cruciger in His left hand while His right hand is raised in blessing. Originating in Spain (traditionally associated with Saint Teresa of Ávila), the image was brought to Bohemia by Duchess María Manrique de Lara and gifted in 1628 by Princess Polyxena of Lobkowicz to the Discalced Carmelite friary of Our Lady Victorious in Prague.\n\nDuring the Thirty Years' War in 1631, Saxon troops sacked the friary, throwing the statue into the debris behind the high altar where its hands were broken off. In 1637, Father Cyril of the Mother of God returned and heard the statue speak: *'Have mercy on me, and I will have mercy on you. Give me my hands, and I will give you peace. The more you honor me, the more I will bless you!'*\n\nAfter the hands were restored, prosperity returned to Prague. Millions of pilgrims worldwide revere the Infant King, celebrated for countless miraculous healings, protection of families, and answers to heartfelt prayer. Pope Benedict XVI crowned the statue with a pure golden crown on September 26, 2009.",
        "historical_summary_vi": "Chúa Hài Đồng Giêsu Praha (*Pražské Jezulátko*) là pho tượng gỗ bọc sáp cao 47cm nổi tiếng thế giới tạc hình Chúa Giêsu Hài Đồng: tay trái cầm quả địa cầu mang thánh giá và tay phải giơ lên chúc lành. Xuất xứ từ Tây Ban Nha (gắn liền với truyền thống Thánh Nữ Têrêsa Ávila), pho tượng được Công chúa Polyxena xứ Lobkowicz dâng tặng cho đan viện Cát Minh Kín Đức Mẹ Chiến Thắng tại Praha năm 1628.\n\nTrong cuộc Chiến tranh 30 Năm (1631), quân xâm lược Saxon cướp phá tu viện và vứt bức tượng vào đống rác sau bàn thờ làm gãy cụt hai bàn tay. Năm 1637, Cha Cyril trở lại và bỗng nghe thấy tiếng Chúa phán ra từ pho tượng: *'Hãy xót thương Ta, Ta sẽ xót thương con. Hãy gắn lại đôi tay cho Ta, Ta sẽ ban bình an cho con. Càng tôn kính Ta bao nhiêu, Ta sẽ chúc phúc cho con bấy nhiêu!'*\n\nSau khi đôi tay tượng được phục hồi, bình an và ơn phúc đã tràn ngập thành Praha. Hàng triệu tín hữu trên toàn thế giới tôn sùng Chúa Hài Đồng Praha như nguồn cậy trông chở che các gia đình. Đức Giáo hoàng Biển Đức XVI đã đích thân trao vương miện vàng ròng cho pho tượng ngày 26 tháng 9 năm 2009.",
        "scripture_reading": "Isaiah 9:6",
        "suggested_prayer_en": "O Infant Jesus, I have recourse to You by Your Holy Mother, asking You to assist me in my necessity, for I firmly believe that Your Divinity can protect me. Deliver me from all distress and grant me the grace to possess You eternally with Mary and Joseph. Amen.",
        "suggested_prayer_vi": "Lạy Chúa Hài Đồng Giêsu, con chạy đến cùng Chúa nhờ lời chuyển cầu của Mẹ Thánh Chúa, xin Chúa cứu giúp con trong cơn gian nan khốn khó này, vì con tin vững vàng rằng Thiên Tính của Chúa có quyền năng che chở con. Xin giải thoát con khỏi mọi âu lo và ban cho con mai sau được hưởng nhan Chúa muôn đời cùng Đức Mẹ và Thánh Cả Giuse. Amen.",
        "primary_sources": [
            {
                "label": "Church of Our Lady Victorious - Infant Jesus of Prague Official Archives",
                "url": "https://www.pragjesu.cz/en/",
                "type": "academic"
            },
            {
                "label": "Pope Benedict XVI - Address at the Church of the Infant Jesus of Prague (September 26, 2009)",
                "url": "https://www.vatican.va/content/benedict-xvi/en/speeches/2009/september/documents/hf_ben-xvi_spe_20090926_bambin-gesu-praga.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "st_ignatius_church_rome",
        "category": "monastic_sanctuary",
        "name_en": "Church of Saint Ignatius of Loyola (Sant'Ignazio, Rome)",
        "name_vi": "Đại Thánh Đường Thánh Inhaxiô Loyola (Roma)",
        "feast_day_association": "Feast of Saint Ignatius of Loyola (July 31) / Saint Aloysius Gonzaga (June 21)",
        "location": {
            "shrine_or_basilica": "Chiesa di Sant'Ignazio di Loyola in Campo Marzio",
            "city": "Rome",
            "region_or_state": "Lazio",
            "country": "Italy",
            "latitude": 41.8992,
            "longitude": 12.4797,
            "precision": "chapel_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1722-01-01",
            "approving_authority": "Cardinal Ludovico Ludovisi / Pope Gregory XV / Jesuit Curia",
            "confidence": "confirmed",
            "confidence_note_en": "Built in 1626 honoring the canonization of Saint Ignatius; houses the monumental illusory Baroque ceiling frescoes and trompe-l'œil dome by Jesuit Brother Andrea Pozzo; enshrines the tombs of Jesuit saints Aloysius Gonzaga, John Berchmans, and Robert Bellarmine.",
            "confidence_note_vi": "Xây dựng năm 1626 kỷ niệm biến cố phong thánh cho Thánh Inhaxiô; kiệt tác bích họa trần thời Baroque và mái vòm ảo ảnh thị giác của Tu sĩ Dòng Tên Andrea Pozzo; bảo tồn thi hài các Thánh Dòng Tên Aloisiô Gonzaga, Gioan Berchmans và Roberto Bellarmino."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Lapis Lazuli Altar Sarcophagus of Saint Aloysius Gonzaga and Tomb of Saint Robert Bellarmine",
                "relic_name_vi": "Lăng Mộ Ngọc Lưu Ly Của Thánh Aloisiô Gonzaga và Mộ Thánh Roberto Bellarmino",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Chapel of Saint Aloysius Gonzaga and High Altar of Sant'Ignazio"
            }
        ],
        "historical_summary_en": "The Church of Saint Ignatius of Loyola at the Collegio Romano in Rome is a triumph of Counter-Reformation Baroque architecture and Jesuit missionary cosmology. Commissioned in 1626 by Cardinal Ludovico Ludovisi, the sanctuary celebrates the apostolic worldwide expansion of the Society of Jesus under Saint Ignatius.\n\nThe church's ceiling is world-famous for the breathtaking illusory fresco painted by Jesuit lay brother Andrea Pozzo between 1685 and 1694: *The Apotheosis of Saint Ignatius*. In this masterpiece of *quadratura*, rays of light stream from the pierced Heart of Christ to Saint Ignatius, which then reflect out to the four corners of the earth represented by allegories of the four known continents (Europe, Asia, Africa, America).\n\nSant'Ignazio serves as the resting place of major Jesuit saints: Saint Aloysius Gonzaga (1568–1591, patron of youth), Saint John Berchmans, and Saint Robert Bellarmine (Doctor of the Church), whose sacred remains are enshrined in sumptuous lapis lazuli, silver, and gilded bronze altars.",
        "historical_summary_vi": "Đại Thánh Đường Thánh Inhaxiô Loyola tại Trường Cao Đẳng Roma là đỉnh cao của kiến trúc Baroque thời Phản Cải Cách và thần học truyền giáo Dòng Tên. Được Đức Hồng y Ludovico Ludovisi khởi dựng năm 1626, đền thánh tôn vinh công cuộc loan báo Tin Mừng khắp năm châu của Dòng Tên dưới sự dẫn dắt của Thánh Inhaxiô.\n\nTrần nhà thờ nổi tiếng khắp thế giới với bức bích họa ảo ảnh thị giác ngoạn mục do Tu sĩ Dòng Tên Andrea Pozzo thực hiện (1685–1694): *Vinh Quang Thiên Quốc của Thánh Inhaxiô*. Trong kiệt tác này, những luồng ánh sáng từ Thánh Tâm Chúa Kitô chiếu rọi vào ngực Thánh Inhaxiô rồi phản chiếu rực rỡ đến 4 phương trời đại diện cho 4 lục địa (Châu Âu, Châu Á, Châu Phi và Châu Mỹ).\n\nĐền thờ là nơi an nghỉ của các vị thánh Dòng Tên lẫy lừng: Thánh Aloisiô Gonzaga (1568–1591, quan thầy giới trẻ), Thánh Gioan Berchmans và Thánh Roberto Bellarmino (Tiến Sĩ Hội Thánh), được an vị trong các bàn thờ đá ngọc lưu ly, bạc và đồng mạ vàng tuyệt mỹ.",
        "scripture_reading": "Luke 12:49",
        "suggested_prayer_en": "Lord Jesus Christ, who came to cast fire upon the earth and willed that it be ignited, ignite in our souls the holy fire of apostolic zeal. May all our thoughts, words, and actions be directed solely to your greater glory (*Ad Maiorem Dei Gloriam*). Amen.",
        "suggested_prayer_vi": "Lạy Chúa Giêsu Kitô, Đấng đã đến ném lửa vào trần gian và ước mong ngọn lửa ấy bùng cháy lên, xin thắp sáng trong tâm hồn chúng con ngọn lửa nhiệt thành tông đồ. Xin cho mọi tư tưởng, lời nói và việc làm của chúng con luôn quy hướng về vinh quang lớn hơn của Chúa (*Ad Maiorem Dei Gloriam*). Amen.",
        "primary_sources": [
            {
                "label": "Chiesa di Sant'Ignazio di Loyola Official Historical Dossier",
                "url": "https://santignazio.gesuiti.it/",
                "type": "academic"
            },
            {
                "label": "Jesuit Historical Institute (ARSI) - Andrea Pozzo and the Frescoes of Sant'Ignazio",
                "url": "https://www.jesuitonline.org/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "st_charbel_monastery_annaya",
        "category": "monastic_sanctuary",
        "name_en": "Monastery of Saint Maron - Sanctuary of Saint Charbel (Annaya)",
        "name_vi": "Đan Viện Thánh Maron - Đền Thánh Cha Thánh Charbel (Annaya, Liban)",
        "feast_day_association": "Feast of Saint Charbel Makhlouf (Third Sunday of July / December 24)",
        "location": {
            "shrine_or_basilica": "Monastery of Saint Maron - Annaya (Santuario di San Charbel)",
            "city": "Annaya (Byblos District)",
            "region_or_state": "Mount Lebanon Governorate",
            "country": "Lebanon",
            "latitude": 34.1481,
            "longitude": 35.8153,
            "precision": "tomb"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1977-10-09",
            "approving_authority": "Pope Paul VI (Canonization in Rome) / Maronite Patriarchate of Antioch",
            "confidence": "confirmed",
            "confidence_note_en": "Canonized by Pope Paul VI in 1977; body remained completely flexible and exuded miraculous fluid continuously from 1898 to 1965; over 29,000 documented miraculous healings recorded in the shrine registers.",
            "confidence_note_vi": "Được Đức Giáo hoàng Phaolô VI tuyên thánh năm 1977; thi hài hoàn toàn mềm mại và liên tục tiết ra chất dịch phép lạ từ năm 1898 đến 1965; hơn 29.000 phép lạ chữa lành được ghi nhận trong sổ lưu niệm đền thánh."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Incorrupt Body, Bone Relics, and Miraculous Oil of Saint Charbel Makhlouf",
                "relic_name_vi": "Thi Hài và Dầu Thánh Phép Lạ của Cha Thánh Charbel Makhlouf",
                "relic_type": "incorrupt_body",
                "reliquary_location": "Marble Tomb inside the Church of Saint Maron and the Hermitage of Saints Peter and Paul, Annaya"
            }
        ],
        "historical_summary_en": "Saint Charbel Makhlouf (Youssef Antoun Makhlouf, 1828–1898) was a Maronite Catholic monk and solitary hermit of the Lebanese Maronite Order who lived at the Hermitage of Saints Peter and Paul above the Monastery of Saint Maron in Annaya on Mount Lebanon. Living a life of extreme fasting, continuous Eucharistic adoration, and manual labor, Charbel spoke only in prayer and lived in complete union with God.\n\nOn December 16, 1898, while celebrating the Maronite Divine Liturgy, Charbel suffered a stroke at the moment of the elevation of the Sacred Host, whispering the liturgical prayer: *'Father of Truth, behold Your Son, a sacrifice pleasing to You.'* He died on Christmas Eve 1898.\n\nImmediately after his burial in the muddy monastery cemetery, dazzling beams of celestial light shone from his grave for forty-five consecutive nights. When exhumed, his body was found floating in muddy water but completely incorrupt, lifelike, and bleeding fresh blood and sweat. For sixty-seven years (1898–1965), his flexible body exuded a fragrant reddish perspiration that filled bottles and worked thousands of medically validated cures across Christians and Muslims alike.",
        "historical_summary_vi": "Thánh Charbel Makhlouf (Youssef Antoun Makhlouf, 1828–1898) là một đan sĩ và ẩn sĩ Công giáo nghi lễ Maronite thuộc Dòng Maronite Liban, ẩn tu tại Ẩn viện Thánh Phêrô và Phaolô trên đỉnh núi Annaya, Liban. Sống đời chay tịnh khắc khổ, chầu Thánh Thể liên lỉ thâu đêm và lao động chân tay, ngài chỉ mở miệng khi cầu nguyện và kết hợp mật thiết với Chúa.\n\nNgày 16 tháng 12 năm 1898, khi đang cử hành Thánh Lễ nghi lễ Maronite, Cha Charbel bị đột quỵ ngay lúc nâng cao Bánh Thánh, thì thào lời nguyện phụng vụ: *'Lạy Cha của Chân Lý, này Con Cha là hy lễ đẹp lòng Cha.'* Ngài qua đời vào Đêm Vọng Giáng Sinh năm 1898.\n\nNgay sau khi an táng nơi nghĩa trang đan viện lầy lội, những luồng ánh sáng chói lọi kỳ diệu đã phát ra từ ngôi mộ suốt 45 đêm liên tiếp. Khi quật mộ, thi thể ngài vẫn mềm mại hồng hào như người đang ngủ, không hề hư nát và rỉ ra chất dịch thơm ngát. Suốt 67 năm (1898–1965), thi hài ngài liên tục tiết ra chất dịch mồ hôi và máu chữa lành hàng chục ngàn ca bệnh nan y cho cả người Kitô giáo và Hồi giáo.",
        "scripture_reading": "Psalm 92:12-14",
        "suggested_prayer_en": "Lord God, who called Saint Charbel to solitary holiness on the heights of Mount Lebanon and glorified him with extraordinary miracles of healing, look upon our suffering. Through his intercession, grant health to the sick, peace to the Middle East, and salvation to all souls. Amen.",
        "suggested_prayer_vi": "Lạy Chúa là Thiên Chúa chúng con, Đấng đã gọi Cha Thánh Charbel lên đỉnh núi Liban để sống đời ẩn tu thánh thiện và tôn vinh ngài bằng muôn vàn phép lạ chữa lành kỳ diệu, xin đoái nhìn đến những nỗi đau khổ của chúng con. Nhờ lời chuyển cầu của ngài, xin chữa lành người bệnh tật, ban bình an cho vùng Trung Đông và ban ơn cứu độ cho muôn linh hồn. Amen.",
        "primary_sources": [
            {
                "label": "Monastery of Saint Maron Annaya Official Sanctuary & Medical Miracle Records",
                "url": "https://saintcharbel.com/",
                "type": "academic"
            },
            {
                "label": "Pope Paul VI - Homily for the Canonization of Saint Charbel Makhlouf (October 9, 1977)",
                "url": "https://www.vatican.va/content/paul-vi/en/homilies/1977/documents/hf_p-vi_hom_19771009_charbel.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "st_joseph_oratory_montreal",
        "category": "monastic_sanctuary",
        "name_en": "Saint Joseph's Oratory of Mount Royal (Montreal)",
        "name_vi": "Đền Thánh Cả Giuse Trên Núi Hoàng Gia (Montreal, Canada)",
        "feast_day_association": "Solemnity of Saint Joseph, Spouse of the Virgin Mary (March 19) / Saint André Bessette (January 6)",
        "location": {
            "shrine_or_basilica": "L'Oratoire Saint-Joseph du Mont-Royal",
            "city": "Montreal",
            "region_or_state": "Quebec",
            "country": "Canada",
            "latitude": 45.4925,
            "longitude": -73.6178,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1955-03-19",
            "approving_authority": "Pope Pius XII (Minor Basilica 1955) / Pope Benedict XVI (Canonization of Saint André 2010)",
            "confidence": "confirmed",
            "confidence_note_en": "Founded in 1904 by humble Holy Cross brother Saint André Bessette; world's largest shrine dedicated to Saint Joseph; Saint André canonized by Pope Benedict XVI on October 17, 2010.",
            "confidence_note_vi": "Được Thầy Dòng Thánh Giá khiêm nhường Thánh André Bessette thành lập năm 1904; đền thánh kính Thánh Cả Giuse lớn nhất thế giới; Thầy André được Đức Biển Đức XVI tuyên thánh ngày 17 tháng 10 năm 2010."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Heart Relic and Tomb of Saint André Bessette (Brother André)",
                "relic_name_vi": "Trái Tim Thánh Tích và Lăng Mộ của Thánh André Bessette (Thầy André)",
                "relic_type": "1st_class_tomb",
                "reliquary_location": "Heart Reliquary Museum and Black Marble Tomb in the Votive Chapel of the Oratory"
            }
        ],
        "historical_summary_en": "Saint Joseph's Oratory of Mount Royal in Montreal, Canada, crowned by a massive Renaissance dome that is the third-largest of its kind in the world, is the global epicenter of devotion to Saint Joseph. The monumental basilica owes its origin to the faith of a humble, unlettered Holy Cross religious brother, Saint André Bessette (1845–1937), who served for forty years as the simple doorkeeper of Collège Notre-Dame.\n\nEndowed with profound devotion to Saint Joseph, Brother André greeted thousands of sick and suffering visitors, rubbing them with oil from a lamp burning before the statue of Saint Joseph. Tens of thousands of spontaneous, scientifically documented physical cures occurred, prompting crowds to christen him the 'Miracle Man of Montreal.' Brother André consistently deflected praise, insisting: *'I am nothing; it is Saint Joseph who heals.'*\n\nIn 1904, Brother André constructed a tiny wooden chapel on Mount Royal. Over decades, spontaneous donations from grateful pilgrims funded the construction of the present colossal basilica, which welcomes over two million pilgrims annually. When Brother André died in 1937 at age ninety-one, over a million people braved bitter winter snows to file past his casket.",
        "historical_summary_vi": "Đền Thánh Cả Giuse Trên Núi Hoàng Gia tại Montreal, Canada, nổi bật với mái vòm thời Phục Hưng khổng lồ lớn thứ ba thế giới, là trung tâm tôn sùng Thánh Cả Giuse lớn nhất hành tinh. Ngôi đại vương cung thánh đường kỳ vĩ này bắt nguồn từ đức tin sắt đá của một thầy dòng khiêm nhường không biết chữ thuộc Dòng Thánh Giá là Thánh André Bessette (1845–1937), người đã làm người gác cổng trường Notre-Dame suốt 40 năm.\n\nVới lòng yêu mến Thánh Cả Giuse tha thiết, Thầy André đã đón tiếp hàng ngàn người bệnh tật đau khổ, lấy dầu từ ngọn đèn chầu trước tượng Thánh Giuse xức cho họ. Hàng chục ngàn người bại liệt, mù lòa, ung thư đã được chữa lành tức thì khiến dân chúng xưng tụng thầy là 'Người Làm Phép Lạ Thành Montreal'. Thầy luôn khiêm tốn nói: *'Tôi chẳng là gì cả, chính Thánh Giuse đã chữa lành.'*\n\nNăm 1904, Thầy André dựng một ngôi nhà nguyện gỗ nhỏ trên sườn núi. Nhờ sự đóng góp của các bệnh nhân được chữa lành, ngôi đại thánh đường nguy nga ngày nay đã được xây dựng, đón tiếp hơn 2 triệu khách hành hương mỗi năm. Khi Thầy André qua đời năm 1937 ở tuổi 91, hơn một triệu người đã đội tuyết lạnh giá xếp hàng đến kính viếng thi hài ngài.",
        "scripture_reading": "Matthew 1:20-24",
        "suggested_prayer_en": "O Saint Joseph, Foster Father of Jesus and Protector of the Universal Church, look upon our families and physical infirmities. Through the prayers of humble Saint André Bessette, grant healing to the sick, strength to fathers, and protect our homes under your righteous care. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Cả Giuse, Cha Nuôi Chúa Giêsu và Đấng Bảo Trợ Hội Thánh Hoàn Vũ, xin đoái nhìn đến gia đình và những yếu đuối tật nguyền nơi thân xác chúng con. Nhờ lời chuyển cầu của Thầy Thánh André khiêm nhường, xin ban ơn chữa lành cho các bệnh nhân, ban sức mạnh cho các người cha và che chở gia đình chúng con trong sự công chính của ngài. Amen.",
        "primary_sources": [
            {
                "label": "Saint Joseph's Oratory of Mount Royal Official Historical Archive",
                "url": "https://www.saint-joseph.org/en/",
                "type": "academic"
            },
            {
                "label": "Pope Benedict XVI - Homily for the Canonization of Saint André Bessette (October 17, 2010)",
                "url": "https://www.vatican.va/content/benedict-xvi/en/homilies/2010/documents/hf_ben-xvi_hom_20101017_canonizzazioni.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "national_shrine_immaculate_conception_dc",
        "category": "marian_apparition",
        "name_en": "Basilica of the National Shrine of the Immaculate Conception (Washington, D.C.)",
        "name_vi": "Đại Vương Cung Thánh Đường Quốc Gia Đức Mẹ Vô Nhiễm (Washington, D.C.)",
        "feast_day_association": "Solemnity of the Immaculate Conception, Patroness of the United States (December 8)",
        "location": {
            "shrine_or_basilica": "Basilica of the National Shrine of the Immaculate Conception",
            "city": "Washington",
            "region_or_state": "District of Columbia",
            "country": "United States",
            "latitude": 38.9331,
            "longitude": -77.0003,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1959-11-20",
            "approving_authority": "Pope Pius XI (Blessing of Foundation 1913) / Pope John Paul II (Minor Basilica 1990)",
            "confidence": "confirmed",
            "confidence_note_en": "Dedicated as the National Sanctuary of the Catholic Church in the United States; designated a Minor Basilica by Pope John Paul II in 1990; visited by Popes John Paul II, Benedict XVI, and Francis.",
            "confidence_note_vi": "Được cung hiến làm Đền Thánh Quốc Gia của Giáo hội Công giáo Hoa Kỳ; được Đức Gioan Phaolô II nâng lên hàng Tiểu Vương Cung Thánh Đường năm 1990; đã đón tiếp các Đức Giáo hoàng Gioan Phaolô II, Biển Đức XVI và Phanxicô."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Papal Coronation Tiara of Pope Saint Paul VI and Over 80 National Marian Chapels",
                "relic_name_vi": "Triều Thiên Ba Tầng Giáo Hoàng của Thánh Giáo Hoàng Phaolô VI và Hơn 80 Nguyện Đường Thánh Mẫu",
                "relic_type": "holy_icon",
                "reliquary_location": "Crypt Church and Great Upper Church of the National Shrine in Washington, D.C."
            }
        ],
        "historical_summary_en": "The Basilica of the National Shrine of the Immaculate Conception in Washington, D.C., is the largest Roman Catholic church in North America and one of the ten largest churches in the world. Designated by the American bishops in 1846 under the patronage of Our Lady of the Immaculate Conception, the foundation stone was blessed by Cardinal James Gibbons in 1920 with the personal support of Pope Pius XI.\n\nConstructed without steel framework entirely out of solid masonry stone and brick in the Byzantine-Romanesque style, the basilica was dedicated in November 1959 and completed with the dedication of the monumental *Trinity Dome* mosaic in 2017. The interior houses over eighty chapels honoring Our Lady under various global titles reflecting the immigrant diversity of American Catholicism, including Our Lady of La Vang (Vietnam), Our Lady of Guadalupe (Mexico), Our Lady of Czestochowa (Poland), and Our Lady of Knock (Ireland).\n\nIn 1964, Pope Paul VI donated his Papal Tiara to the National Shrine as a permanent gift to the American faithful in support of the poor. The National Shrine stands as the spiritual heart of Catholicism in the United States.",
        "historical_summary_vi": "Đại Vương Cung Thánh Đường Quốc Gia Đức Mẹ Vô Nhiễm Nguyên Tội tại Washington, D.C., là thánh đường Công giáo lớn nhất Bắc Mỹ và là một trong 10 ngôi thánh đường lớn nhất thế giới. Được các giám mục Hoa Kỳ chọn làm Đền Thánh Quan Thầy Quốc Gia từ năm 1846, viên đá đầu tiên được Đức Hồng y James Gibbons làm phép năm 1920 dưới sự bảo trợ của Đức Giáo hoàng Piô XI.\n\nĐược xây dựng hoàn toàn bằng kết cấu đá và gạch vững chắc theo phong cách Byzantine-Romanesque mà không cần khung thép chịu lực, ngôi thánh đường được thánh hiến năm 1959 và hoàn thiện kiệt tác khảm vàng vòm *Trinity Dome* năm 2017. Đền thánh có hơn 80 nguyện đường tôn kính Đức Mẹ dưới các tước hiệu của các cộng đoàn di dân, nổi bật như Nguyện Đường Đức Mẹ La Vang (Việt Nam), Đức Mẹ Guadalupe (Mexico), Đức Mẹ Czestochowa (Ba Lan) và Đức Mẹ Knock (Ireland).\n\nNăm 1964, Thánh Giáo hoàng Phaolô VI đã dâng tặng chiếc Triều Thiên Ba Tầng Giáo Hoàng của ngài cho Đền Thánh Quốc Gia làm quà tặng cho giáo dân Mỹ để ủng hộ người nghèo. Nơi đây là trái tim tâm linh rực rỡ của người Công giáo Hoa Kỳ.",
        "scripture_reading": "Revelation 12:1-2",
        "suggested_prayer_en": "O Mary, Immaculate Virgin, Patroness of the United States, we entrust our families, our leaders, and our nation to your maternal intercession. Protect our freedom to worship, guard the sanctity of human life, and lead all people into the peace and truth of your Son, Jesus Christ. Amen.",
        "suggested_prayer_vi": "Lạy Mẹ Maria Vô Nhiễm Nguyên Tội, Đấng Bảo Trợ Nước Mỹ, chúng con xin phó thác gia đình, các nhà lãnh đạo và quê hương đất nước chúng con cho sự cầu bầu từ mẫu của Mẹ. Xin bảo vệ tự do tôn giáo, bảo vệ sự thánh thiêng của sự sống con người và dẫn đưa muôn dân vào trong chân lý và bình an của Chúa Giêsu Kitô, Con Mẹ. Amen.",
        "primary_sources": [
            {
                "label": "Basilica of the National Shrine of the Immaculate Conception Official Archives",
                "url": "https://www.nationalshrine.org/",
                "type": "academic"
            },
            {
                "label": "Pope Francis - Homily for the Canonization of Junípero Serra at the National Shrine (September 23, 2015)",
                "url": "https://www.vatican.va/content/francesco/en/homilies/2015/documents/papa-francesco_20150923_usa-omelia-serra.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "notre_dame_de_paris",
        "category": "passion_relic",
        "name_en": "Cathedral of Notre-Dame de Paris (The Crown of Thorns)",
        "name_vi": "Nhà Thờ Chính Tòa Đức Bà Paris (Mão Gai Thánh)",
        "feast_day_association": "Solemnity of the Assumption (August 15) / Good Friday (Veneration of Crown of Thorns)",
        "location": {
            "shrine_or_basilica": "Cathédrale Notre-Dame de Paris",
            "city": "Paris",
            "region_or_state": "Île-de-France",
            "country": "France",
            "latitude": 48.8530,
            "longitude": 2.3499,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1182-05-19",
            "approving_authority": "Bishop Maurice de Sully / Pope Alexander III / Saint Louis IX (1239)",
            "confidence": "confirmed",
            "confidence_note_en": "Crown of Thorns acquired from Baldwin II of Constantinople by King Saint Louis IX in 1238; historically verified and venerated across eight centuries; heroically rescued by Father Jean-Marc Fournier during the April 15, 2019 fire.",
            "confidence_note_vi": "Mão Gai Thánh do Vua Thánh Louis IX chuộc từ Hoàng đế Baldwin II thành Constantinople năm 1238; được phụng thờ liên tục suốt 8 thế kỷ; được Cha Tuyên úy Jean-Marc Fournier dũng cảm xông vào biển lửa giải cứu trong trận hỏa hoạn ngày 15 tháng 4 năm 2019."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Sacred Crown of Thorns of Jesus Christ (Sainte Couronne d'Épines)",
                "relic_name_vi": "Mão Gai Cực Thánh của Chúa Giêsu Kitô (Sainte Couronne)",
                "relic_type": "passion_relic",
                "reliquary_location": "Cathedral Treasury and Reliquary of Saint Louis IX inside Notre-Dame de Paris"
            }
        ],
        "historical_summary_en": "The Cathedral of Notre-Dame de Paris, begun in 1163 under Bishop Maurice de Sully on the Île de la Cité, is the architectural masterpiece of French High Gothic art and the spiritual sanctuary preserving the foremost relic of the Passion: the Holy Crown of Thorns (*La Sainte Couronne d'Épines*).\n\nIn 1238, King Saint Louis IX purchased the Crown of Thorns from Baldwin II, the Latin Emperor of Constantinople. On August 19, 1239, King Louis, walking barefoot dressed in a simple tunic alongside his brother Robert, carried the sacred relic into Paris. Saint Louis built the sublime Sainte-Chapelle to enshrine the relic, which was later transferred to Notre-Dame de Paris following the French Revolution.\n\nThe relic consists of a circular ring of rushes (*Juncus balticus*) woven together, upon which seventy spikes of thorn branches (*Ziziphus spina-christi*) were originally tied. On April 15, 2019, when a catastrophic fire consumed the cathedral's wooden roof and collapsed its spire, the chaplain of the Paris Fire Brigade, Father Jean-Marc Fournier, formed a human chain with firefighters to penetrate the burning structure and rescue the Crown of Thorns and the Blessed Sacrament completely intact.",
        "historical_summary_vi": "Nhà Thờ Chính Tòa Đức Bà Paris, được khởi công xây dựng năm 1163 bởi Giám mục Maurice de Sully trên đảo Île de la Cité, là kiệt tác nghệ thuật Gothic đỉnh cao của nước Pháp và là nơi lưu giữ thánh tích Cuộc Khổ Nạn vô giá: Mão Gai Cực Thánh của Chúa Giêsu (*La Sainte Couronne d'Épines*).\n\nNăm 1238, Vua Thánh Louis IX đã chuộc lại Mão Gai Thánh từ Hoàng đế Baldwin II thành Constantinople. Ngày 19 tháng 8 năm 1239, Vua Louis IX đã đi chân trần mặc áo vải thô khiêm nhường rước Mão Gai Thánh tiến vào Paris. Ngài đã xây dựng kiệt tác nhà nguyện Sainte-Chapelle để cung nghinh Mão Gai, trước khi thánh tích được chuyển về Nhà thờ Đức Bà Paris sau Cách mạng Pháp.\n\nThánh tích gồm một vòng bện bằng thân cây cói (*Juncus balticus*) từng được gắn 70 nhánh gai nhọn (*Ziziphus spina-christi*). Ngày 15 tháng 4 năm 2019, khi trận đại hỏa hoạn thiêu rụi mái gỗ và làm sụp đổ tháp nhọn nhà thờ, Cha Tuyên úy Đội cứu hỏa Paris Jean-Marc Fournier đã cùng các chiến sĩ dũng cảm xông vào biển lửa giải cứu Mão Gai Thánh và Mình Thánh Chúa an toàn nguyên vẹn.",
        "scripture_reading": "John 19:2-3",
        "suggested_prayer_en": "Lord Jesus Christ, who wore the Crown of Thorns and suffered mockery and pain for our salvation, heal the wounds of pride and selfishness in our minds. Grant that we may honor You as King of our hearts and remain faithful witnesses to Your redeeming love. Amen.",
        "suggested_prayer_vi": "Lạy Chúa Giêsu Kitô, Đấng đã đội Mão Gai đau đớn và chịu mọi sự sỉ nhục để cứu chuộc chúng con, xin chữa lành những vết thương của lòng kiêu ngạo và ích kỷ trong tâm trí chúng con. Xin cho chúng con luôn tôn nhận Chúa là Vua của lòng chúng con và trung kiên làm chứng cho tình yêu cứu độ của Chúa trọn đời. Amen.",
        "primary_sources": [
            {
                "label": "Cathédrale Notre-Dame de Paris Official Historical and Restoration Documentation",
                "url": "https://www.notredamedeparis.fr/en/",
                "type": "academic"
            },
            {
                "label": "Archdiocese of Paris - The Holy Crown of Thorns and Relics of the Passion",
                "url": "https://dioceseparis.fr/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "saint_stephen_basilica_budapest",
        "category": "martyr_shrine",
        "name_en": "Saint Stephen's Basilica (The Holy Right Hand, Budapest)",
        "name_vi": "Đại Vương Cung Thánh Đường Thánh Stêphanô (Bàn Tay Phải Thánh, Budapest)",
        "feast_day_association": "Feast of Saint Stephen of Hungary (August 20)",
        "location": {
            "shrine_or_basilica": "Szent István-bazilika",
            "city": "Budapest",
            "region_or_state": "Central Hungary",
            "country": "Hungary",
            "latitude": 47.5009,
            "longitude": 19.0539,
            "precision": "chapel_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1905-11-09",
            "approving_authority": "Pope Gregory VII (Canonization 1083) / Pope Pius XI (Minor Basilica 1931)",
            "confidence": "confirmed",
            "confidence_note_en": "King Saint Stephen canonized in 1083 by Pope Gregory VII; incorrupt Holy Right Hand (*Szent Jobb*) verified since the 11th century; enshrined in the co-cathedral basilica of the Archdiocese of Esztergom-Budapest.",
            "confidence_note_vi": "Vua Thánh Stêphanô được Đức Giáo hoàng Grêgôriô VII tuyên thánh năm 1083; Bàn Tay Phải Thánh (*Szent Jobb*) không hư nát được kiểm chứng từ thế kỷ 11; bảo tồn trong thánh đường chính tòa Tổng Giáo phận Esztergom-Budapest."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Incorrupt Holy Right Hand of King Saint Stephen of Hungary (Szent Jobb)",
                "relic_name_vi": "Bàn Tay Phải Thánh Không Hư Nát của Vua Thánh Stêphanô Nước Hungary (Szent Jobb)",
                "relic_type": "incorrupt_body",
                "reliquary_location": "Holy Right Chapel (Szent Jobb Kápolna) inside Saint Stephen's Basilica, Budapest"
            }
        ],
        "historical_summary_en": "Saint Stephen's Basilica (*Szent István-bazilika*) in Budapest is the co-cathedral of the Archdiocese of Esztergom-Budapest and Hungary's premier sacred sanctuary, dedicated to King Saint Stephen I (975–1038), who unified the Hungarian tribes and established the Christian Kingdom of Hungary, receiving the Holy Crown from Pope Sylvester II in the year 1000 AD.\n\nOn his deathbed on August 15, 1038 (Feast of the Assumption), King Stephen lifted his crown and solemnly consecrated the Hungarian nation to the Virgin Mary (*Patrona Hungariae*). When his tomb was opened during his canonization in 1083 by King Saint Ladislaus I, his body had decomposed, but his right hand—the hand that had held the royal scepter, signed charters of Christian law, and distributed alms to the destitute—was found completely incorrupt and naturally mummified.\n\nPreserved today within an exquisite Neo-Gothic gilded silver reliquary inside the Holy Right Chapel, the *Szent Jobb* has been carried through the streets of Budapest every August 20 for centuries as the sacred symbol of Hungarian Catholic identity and perseverance.",
        "historical_summary_vi": "Đại Vương Cung Thánh Đường Thánh Stêphanô tại Budapest là đồng nhà thờ chính tòa của Tổng Giáo phận Esztergom-Budapest và là đền thánh lớn nhất nước Hungary, tôn kính Vua Thánh Stêphanô I (975–1038), người đã thống nhất các bộ tộc Magyar và thành lập Vương quốc Kitô giáo Hungary, đón nhận Vương Miện Thánh từ Đức Giáo hoàng Sylvester II năm 1000.\n\nTrên giường bệnh ngày 15 tháng 8 năm 1038 (Lễ Đức Mẹ Hồn Xác Lên Trời), Vua Stêphanô đã dâng triều thiên và tận hiến toàn thể dân tộc Hungary cho Đức Trinh Nữ Maria (*Patrona Hungariae*). Khi mở mộ ngài trong lễ phong thánh năm 1083, toàn thân thể đã tan rã ngoại trừ Bàn Tay Phải Thánh (*Szent Jobb*)—bàn tay từng cầm quyền trượng, ban hành luật pháp Kitô giáo và phát của bố thí cho người nghèo—vẫn hoàn toàn nguyên vẹn không hư nát.\n\nĐược bảo tồn trong hòm bạc mạ vàng Tân Gothic lộng lẫy trong Nguyện đường Bàn Tay Thánh, *Szent Jobb* được rước long trọng qua các đường phố Budapest vào ngày 20 tháng 8 hằng năm như biểu tượng đức tin bất diệt của người Công giáo Hungary.",
        "scripture_reading": "Psalm 89:20-24",
        "suggested_prayer_en": "Almighty God, who through King Saint Stephen established a Christian kingdom founded upon faith, justice, and charity, bless our nations. Grant that our leaders may govern with wisdom, defend the dignity of the poor, and lead their people in the peace of Christ. Amen.",
        "suggested_prayer_vi": "Lạy Thiên Chúa Toàn Năng, Đấng đã dùng Vua Thánh Stêphanô thiết lập một vương quốc Kitô giáo đặt nền tảng trên đức tin, công lý và bác ái, xin chúc lành cho các dân tộc chúng con. Xin ban cho các nhà lãnh đạo sự khôn ngoan công chính, biết bảo vệ người nghèo khổ và dẫn dắt muôn dân trong bình an của Chúa Kitô. Amen.",
        "primary_sources": [
            {
                "label": "Szent István Bazilika Budapest Official Archival Dossier",
                "url": "https://www.bazilika.biz/en",
                "type": "academic"
            },
            {
                "label": "Pope John Paul II - Address at Saint Stephen's Basilica, Budapest (August 20, 1991)",
                "url": "https://www.vatican.va/content/john-paul-ii/en/speeches/1991/august/documents/hf_jp-ii_spe_19910820_basilica-budapest.html",
                "type": "vatican"
            }
        ]
    }
]

def main():
    target_dir = "Anno/Resources/SacredSanctuaries"
    os.makedirs(target_dir, exist_ok=True)
    
    for item in ADDITIONAL_SANCTUARIES:
        filename = f"{item['sanctuary_id']}.json"
        path = os.path.join(target_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False, indent=2)
        print(f"Generated {filename}")

if __name__ == "__main__":
    main()

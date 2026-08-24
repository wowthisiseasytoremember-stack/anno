#!/usr/bin/env python3
"""
generate_batch_5_6.py
Generates Batch 5 (Doctors of the Church & Great Saint Shrines) & Batch 6 (Modern Mystics, Incorruptibles & Monastic Sanctuaries)
"""

import json
import os

BATCH_5 = [
    {
        "sanctuary_id": "st_matthew_salerno",
        "category": "apostolic_tomb",
        "name_en": "Salerno Cathedral Crypt (Tomb of Saint Matthew the Apostle)",
        "name_vi": "Hầm Mộ Nhà Thờ Chính Tòa Salerno (Lăng Mộ Thánh Mátthêu Tông Đồ)",
        "feast_day_association": "Feast of Saint Matthew, Apostle and Evangelist (September 21)",
        "location": {
            "shrine_or_basilica": "Cattedrale Primaziale di Santa Maria degli Angeli e San Matteo",
            "city": "Salerno",
            "region_or_state": "Campania",
            "country": "Italy",
            "latitude": 40.6797,
            "longitude": 14.7656,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1085-05-25",
            "approving_authority": "Pope Gregory VII (Consecration) / Bishop John of Salerno (Translation 954 AD)",
            "confidence": "confirmed",
            "confidence_note_en": "Relics translated to Salerno in 954 AD; Cathedral crypt consecrated by Pope Saint Gregory VII in 1085, where the Pope himself is also buried; continuous veneration of the Apostle's tomb.",
            "confidence_note_vi": "Hài cốt được rước về Salerno năm 954; Hầm mộ được chính Thánh Giáo hoàng Grêgôriô VII thánh hiến năm 1085 (nơi Đức Giáo hoàng cũng được an táng); truyền thống sùng kính liên tục qua hơn một thiên niên kỷ."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Sacred Bones of Saint Matthew the Apostle and Evangelist",
                "relic_name_vi": "Hài Cốt Thánh Mátthêu Tông Đồ và Tác Giả Sách Phúc Âm",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Under the Central Baroque Altar in the Crypt of Salerno Cathedral"
            }
        ],
        "historical_summary_en": "Saint Matthew (Levi), the tax collector of Capernaum who left his toll booth to follow Jesus (*Matthew 9:9*), authored the First Canonical Gospel directed primarily to Jewish Christians, demonstrating the fulfillment of Old Testament prophecies in Jesus Christ. Following Pentecost, Matthew preached the Gospel in Judea, Ethiopia, and Parthia before suffering martyrdom while offering the Holy Sacrifice of the Mass.\n\nIn the 5th century, the Apostle's body was discovered in Lucania (Paestum) and later hidden during barbarian invasions. In AD 954, Duke Gisulf I of Salerno orchestrated the solemn translation of Matthew's sacred remains to the coastal city of Salerno. In 1085, Norman conqueror Robert Guiscard completed the majestic Romanesque cathedral, which was consecrated by Pope Saint Gregory VII.\n\nThe cathedral crypt is a masterpiece of Baroque polychrome marble and frescoes executed by Belisario Corenzio. Matthew's tomb beneath the altar has been venerated by kings, pontiffs, and pilgrims for over a millennium as the resting place of the tax collector turned evangelist.",
        "historical_summary_vi": "Thánh Mátthêu (Lêvi), người thu thuế tại Capernaum đã dứt khoát đứng lên rời bỏ bàn thu thuế để theo Chúa Giêsu (*Mátthêu 9:9*), là tác giả của sách Phúc Âm Thứ Nhất dành cho người Do Thái, làm chứng Chúa Giêsu là Đấng Cứu Thế hoàn tất mọi lời tiên tri Cựu Ước. Sau Lễ Hiện Xuống, ngài đi rao giảng Tin Mừng tại Judea, Ethiopia và Parthia trước khi chịu tử đạo ngay bên bàn thờ khi đang cử hành Thánh Lễ.\n\nVào thế kỷ thứ 5, thi hài Thánh Tông đồ được tìm thấy tại vùng Lucania và được bảo tồn qua các cuộc xâm lăng của man tộc. Năm 954, Công tước Gisulf I xứ Salerno đã long trọng rước thánh tích về Salerno. Năm 1085, tướng Norman Robert Guiscard đã hoàn thành ngôi nhà thờ chính tòa tráng lệ và được chính Thánh Giáo hoàng Grêgôriô VII thánh hiến.\n\nGian hầm mộ của nhà thờ là một kiệt tác cẩm thạch đa sắc thời Baroque với các bức bích họa tuyệt mỹ của danh họa Belisario Corenzio. Lăng mộ Thánh Mátthêu dưới bàn thờ chính đã đón nhận vô số vị vua chúa, giáo hoàng và khách hành hương suốt một ngàn năm qua để kính viếng người thu thuế trở thành thánh sử Tin Mừng.",
        "scripture_reading": "Matthew 9:9-13",
        "suggested_prayer_en": "O Holy Apostle and Evangelist Saint Matthew, who promptly abandoned worldly riches at the call of the Master, inspire us with a spirit of complete detachment. Help us to hear the voice of Jesus calling us to repentance, and write the holy words of the Gospel upon the tablets of our hearts. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Mátthêu Tông Đồ và Thánh Sử vinh hiển, ngài đã mau mắn từ bỏ tiền tài của cải thế gian khi nghe tiếng Chúa gọi, xin truyền cho chúng con tinh thần thanh thoát từ bỏ. Xin giúp chúng con luôn nhạy bén lắng nghe tiếng Chúa Giêsu mời gọi hoán cải, và khắc ghi những lời thánh thiện của Tin Mừng vào sâu thẳm tâm hồn chúng con. Amen.",
        "primary_sources": [
            {
                "label": "Arcidiocesi di Salerno-Campagna-Acerno Official Cathedral Chronicles",
                "url": "https://www.diocesisalerno.it/",
                "type": "academic"
            },
            {
                "label": "Catholic Encyclopedia - Saint Matthew the Apostle and Salerno Relics",
                "url": "https://www.newadvent.org/cathen/10056b.htm",
                "type": "encyclopedia"
            }
        ]
    },
    {
        "sanctuary_id": "st_mark_venice",
        "category": "apostolic_tomb",
        "name_en": "Patriarchal Cathedral Basilica of Saint Mark (Venice)",
        "name_vi": "Đại Vương Cung Thánh Đường Thánh Máccô (Venice)",
        "feast_day_association": "Feast of Saint Mark the Evangelist (April 25)",
        "location": {
            "shrine_or_basilica": "Basilica Cattedrale Patriarcale di San Marco",
            "city": "Venice",
            "region_or_state": "Veneto",
            "country": "Italy",
            "latitude": 45.4345,
            "longitude": 12.3397,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1094-10-08",
            "approving_authority": "Doge Vitale Falier / Patriarch of Venice / Pope Urban II",
            "confidence": "confirmed",
            "confidence_note_en": "Relics translated from Alexandria to Venice in 828 AD by Venetian merchants Rustico da Torcello and Buono da Malamocco; miraculous rediscovery (*Inventio*) during church consecration in 1094.",
            "confidence_note_vi": "Hài cốt được rước từ Alexandria về Venice năm 828 bởi hai thương gia Rustico da Torcello và Buono da Malamocco; biến cố tái khám phá hài cốt kỳ diệu (*Inventio*) diễn ra khi thánh hiến đền thờ năm 1094."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Sacred Relics of Saint Mark the Evangelist, Disciple of Peter",
                "relic_name_vi": "Hài Cốt Thánh Máccô Tác Giả Phúc Âm, Môn Đệ Thánh Phêrô",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Marble Sarcophagus beneath the High Altar and the Pala d'Oro"
            }
        ],
        "historical_summary_en": "Saint Mark the Evangelist, companion of Saint Paul and disciple-interpreter of Saint Peter in Rome (*1 Peter 5:13*), authored the Second Gospel capturing Peter's direct apostolic testimony. Following his mission in Rome, Mark journeyed to Egypt, where he founded the Church of Alexandria, becoming its first bishop and suffering martyrdom around AD 68 when pagans dragged him through the streets.\n\nIn AD 828, two Venetian merchants, Buono di Malamocco and Rustico di Torcello, smuggled the Apostle's body out of Muslim-occupied Alexandria beneath layers of pork and cabbage to evade customs. Arriving in Venice, Doge Giustiniano Participazio hailed the arrival as the fulfillment of an ancient prophecy in which an angel greeted Mark in the Venetian lagoon: *'Pax tibi Marce, evangelista meus'* ('Peace be to you, Mark, my evangelist').\n\nThe Venetian Republic adopted the Winged Lion of Saint Mark as its eternal crest and constructed the breathtaking Byzantine-Gothic Basilica of Saint Mark. Adorned with over 8,000 square meters of shimmering gold glass mosaics and the famed *Pala d'Oro*, Saint Mark's tomb stands at the crossroads of Eastern and Western Christian culture.",
        "historical_summary_vi": "Thánh Máccô Thánh Sử, người bạn đồng hành của Thánh Phaolô và là người môn đệ ghi chép lời chứng trực tiếp của Thánh Phêrô tại Roma (*1 Phêrô 5:13*), là tác giả của sách Phúc Âm Thứ Hai. Sau sứ vụ tại Roma, ngài đến Ai Cập thành lập Tòa Thượng Phụ Alexandria, trở thành vị giám mục đầu tiên và chịu tử đạo vào khoảng năm 68 sau Công Nguyên khi bị dân ngoại kéo lê qua các đường phố.\n\nNăm 828, hai thương gia thành Venice là Buono di Malamocco và Rustico di Torcello đã bí mật rước thi hài Thánh Sử vượt biển thoát khỏi sự kiểm soát của quân Hồi giáo tại Alexandria về Venice. Tổng trấn Venice đã hân hoan đón nhận, xem đây là sự ứng nghiệm lời thiên thần từng báo trước cho Thánh Máccô bên đầm phá Venice: *'Pax tibi Marce, evangelista meus'* ('Bình an cho con, Máccô, thánh sử của Ta').\n\nCộng hòa Venice đã chọn biểu tượng Sư Tử Có Cánh của Thánh Máccô làm quốc huy và xây dựng Đại Vương Cung Thánh Đường San Marco nguy nga lộng lẫy theo phong cách Byzantine. Với hơn 8.000 mét vuông tranh ghép kính mạ vàng ròng cùng bức trướng *Pala d'Oro* vô giá, lăng mộ Thánh Máccô là biểu tượng đức tin kết nối hai nền văn minh Kitô giáo Đông - Tây.",
        "scripture_reading": "Mark 1:1-3",
        "suggested_prayer_en": "O Glorious Evangelist Saint Mark, faithful interpreter of Saint Peter, you proclaimed with urgency the Good News of the Kingdom of God. Strengthen our resolve to live the Gospel boldly, protect the unity of the Church, and grant that like the Winged Lion, we may fearlessly profess Christ as the Son of the Living God. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Máccô Thánh Sử vinh hiển, môn đệ trung thành của Thánh Phêrô, ngài đã hăng say loan báo Tin Mừng Nước Thiên Chúa cho muôn dân. Xin củng cố lòng can đảm của chúng con để sống trọn vẹn tinh thần Phúc Âm, gìn giữ sự hiệp nhất của Giáo hội và ban cho chúng con lòng dũng cảm như Sư Tử Có Cánh tuyên xưng Chúa Kitô là Con Thiên Chúa Hằng Sống. Amen.",
        "primary_sources": [
            {
                "label": "Procuratoria di San Marco - Historical and Archaeological Archive of the Basilica",
                "url": "http://www.basilicasanmarco.it/basilica/storia/?lang=en",
                "type": "academic"
            },
            {
                "label": "Pope Benedict XVI - Address during Pastoral Visit to Saint Mark's Basilica (May 8, 2011)",
                "url": "https://www.vatican.va/content/benedict-xvi/en/speeches/2011/may/documents/hf_ben-xvi_spe_20110508_san-marco.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "st_francis_and_clare_assisi",
        "category": "doctor_of_church",
        "name_en": "Papal Basilica of Saint Francis and Basilica of Saint Clare (Assisi)",
        "name_vi": "Đại Vương Cung Thánh Đường Thánh Phanxicô và Thánh Clara (Assisi)",
        "feast_day_association": "Feast of Saint Francis (October 4) / Feast of Saint Clare (August 11)",
        "location": {
            "shrine_or_basilica": "Basilica Papale di San Francesco d'Assisi",
            "city": "Assisi",
            "region_or_state": "Perugia, Umbria",
            "country": "Italy",
            "latitude": 43.0748,
            "longitude": 12.6056,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1253-05-25",
            "approving_authority": "Pope Gregory IX (Papal Bull 1228) / Pope Innocent IV (Consecration 1253)",
            "confidence": "confirmed",
            "confidence_note_en": "Saint Francis canonized in 1228 by Pope Gregory IX, who laid the foundation stone of the Basilica; Saint Clare canonized in 1255 by Pope Alexander IV; tombs verified and perpetually venerated in their respective crypts.",
            "confidence_note_vi": "Thánh Phanxicô được Đức Giáo hoàng Grêgôriô IX tuyên thánh năm 1228 và đặt viên đá đầu tiên xây dựng Vương cung thánh đường; Thánh Clara được Đức Alêxandrô IV tuyên thánh năm 1255; thi hài hai thánh được bảo tồn nguyên vẹn tại các hầm mộ ở Assisi."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Stone Tomb of Saint Francis of Assisi and the Incorrupt Body of Saint Clare",
                "relic_name_vi": "Lăng Mộ Đá Thánh Phanxicô Assisi và Thi Hài Thánh Nữ Clara",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Rock Crypt beneath the Lower Basilica of San Francesco / Crypt of Basilica di Santa Chiara"
            }
        ],
        "historical_summary_en": "Saint Francis of Assisi (1181–1226), the 'Poverello,' abandoned his inheritance as a wealthy cloth merchant's son to embrace radical evangelical poverty, hearing Christ's command from the San Damiano crucifix: *'Francis, go and repair My house, which is falling into ruins.'* He founded the Order of Friars Minor and, in 1224 on Mount La Verna, became the first documented saint to receive the Sacred Stigmata—the physical wounds of the Crucified Christ.\n\nSaint Clare of Assisi (1194–1253), inspired by Francis' preaching, consecrated her virginity on Palm Sunday 1212 and established the Order of Poor Clares at San Damiano, heroically turning away invading Saracen mercenaries by elevating the Blessed Sacrament before the monastery gates.\n\nThe Papal Basilica of San Francesco, perched upon the *Colle del Paradiso*, contains two levels adorned with sublime fresco cycles by Giotto, Cimabue, and Simone Martini, sheltering the stone pillar crypt containing Francis' tomb. Nearby, the Basilica of Santa Chiara protects Clare's body and the original 12th-century San Damiano Crucifix.",
        "historical_summary_vi": "Thánh Phanxicô Assisi (1181–1226), 'Người Nghèo Thành Assisi', đã từ bỏ gia tài nhung lụa của gia đình quý tộc để sống đời khó nghèo trọn hảo theo Tin Mừng, sau khi nghe tiếng Chúa phán từ cây Thánh Giá San Damiano: *'Phanxicô, hãy đi sửa lại ngôi nhà của Ta đang sụp đổ.'* Ngài sáng lập Dòng Anh Em Hèn Mọn (Dòng Phanxicô) và vào năm 1224 trên núi La Verna, ngài là vị thánh đầu tiên trong lịch sử được in Năm Dấu Thánh Chúa Giêsu trên thân xác.\n\nThánh Nữ Clara thành Assisi (1194–1253), được đánh động bởi gương sáng của Phanxicô, đã dâng hiến cuộc đời vào đêm Chúa Nhật Lễ Lá năm 1212, sáng lập Dòng Nữ Tu Nghèo Khó (Dòng Clara) tại San Damiano, và từng can đảm giơ cao Mình Thánh Chúa đẩy lùi đạo quân lính đánh thuê Saracen xâm lăng tu viện.\n\nĐại Vương Cung Thánh Đường Thánh Phanxicô tọa lạc trên đồi *Colle del Paradiso* gồm hai tầng lộng lẫy với các kiệt tác bích họa của Giotto và Cimabue, che chở hầm mộ đá của Thánh Phanxicô. Gần đó, Đền Thờ Thánh Clara bảo tồn thi hài Thánh Nữ và Cây Thánh Giá San Damiano nguyên bản từ thế kỷ 12.",
        "scripture_reading": "Galatians 6:14",
        "suggested_prayer_en": "Lord, make us instruments of your peace: where there is hatred, let us sow love; where there is injury, pardon; where there is doubt, faith; where there is despair, hope; where there is darkness, light; and where there is sadness, joy. Through the prayers of Saints Francis and Clare, grant us pure humility of heart. Amen.",
        "suggested_prayer_vi": "Lạy Chúa, xin làm cho con nên khí cụ bình an của Chúa: để nơi nào có oán thù, con đem lại yêu thương; nơi nào có lăng nhục, con đem lại thứ tha; nơi nào có hoài nghi, con đem lại đức tin; nơi nào có thất vọng, con đem lại hy vọng; nơi nào có tối tăm, con đem lại ánh sáng; nơi nào có ưu sầu, con đem lại niềm vui. Nhờ lời chuyển cầu của Thánh Phanxicô và Thánh Clara, xin ban cho chúng con tâm hồn khiêm nhường khó nghèo. Amen.",
        "primary_sources": [
            {
                "label": "Sacro Convento di San Francesco in Assisi Official Historical Archives",
                "url": "https://www.sanfrancescopatronoditalia.it/",
                "type": "academic"
            },
            {
                "label": "Pope Francis - Encyclical Fratelli Tutti signed at the Tomb of Saint Francis (2020)",
                "url": "https://www.vatican.va/content/francesco/en/encyclicals/documents/papa-francesco_20201003_enciclica-fratelli-tutti.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "st_anthony_of_padua",
        "category": "doctor_of_church",
        "name_en": "Pontifical Basilica of Saint Anthony of Padua (Il Santo)",
        "name_vi": "Đại Vương Cung Thánh Đường Thánh Antôn Pađôva",
        "feast_day_association": "Feast of Saint Anthony of Padua, Doctor of the Church (June 13)",
        "location": {
            "shrine_or_basilica": "Pontificia Basilica Minore di Sant'Antonio di Padova",
            "city": "Padua",
            "region_or_state": "Veneto",
            "country": "Italy",
            "latitude": 45.4014,
            "longitude": 11.8797,
            "precision": "chapel_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1232-05-30",
            "approving_authority": "Pope Gregory IX (Canonization in Spoleto)",
            "confidence": "confirmed",
            "confidence_note_en": "Canonized by Pope Gregory IX on May 30, 1232, merely 352 days after his death (the second fastest canonization in Church history); declared Evangelical Doctor of the Church (*Doctor Evangelicus*) by Pope Pius XII in 1946.",
            "confidence_note_vi": "Được Đức Giáo hoàng Grêgôriô IX tuyên thánh ngày 30 tháng 5 năm 1232, chỉ 352 ngày sau khi qua đời (vụ tuyên thánh nhanh thứ hai trong lịch sử Giáo hội); được Đức Piô XII tuyên phong là Tiến Sĩ Hội Thánh (*Doctor Evangelicus*) năm 1946."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Incorrupt Tongue, Vocal Cords, and Sarcophagus of Saint Anthony",
                "relic_name_vi": "Lưỡi và Dây Thanh Âm Không Hư Nát cùng Quan Tài Thánh Antôn",
                "relic_type": "incorrupt_body",
                "reliquary_location": "Chapel of the Relics (Treasury) and Ark of Saint Anthony Altar"
            }
        ],
        "historical_summary_en": "Saint Anthony of Padua (Fernando Martins de Bulhões, 1195–1231), born in Lisbon, Portugal, was an Augustinian canon who joined the newly founded Franciscan Friars Minor after seeing the relics of the first Franciscan martyrs of Morocco. Endowed with profound biblical erudition and burning eloquence, Anthony became known as the 'Hammer of Heretics' (*Malleus Haereticorum*) and 'Ark of the Testament' (*Arca Testamenti*).\n\nHis preaching throughout northern Italy and southern France was confirmed by numerous miracles, including the fish of Rimini gathering at the shoreline to hear the word of God when heretics refused to listen, and a starved donkey kneeling before the Blessed Sacrament to confound a skeptic.\n\nAnthony died at the Franciscan hermitage of Arcella near Padua on June 13, 1231, at age 35. When his tomb was opened thirty years later by Saint Bonaventure in 1263, Anthony's body had decomposed, but his tongue remained completely incorrupt, fresh, and red—a divine confirmation of the preaching that converted tens of thousands. The massive Byzantine-Gothic Basilica (*Il Santo*) receives millions of pilgrims seeking his powerful intercession.",
        "historical_summary_vi": "Thánh Antôn Pađôva (Fernando Martins de Bulhões, 1195–1231), sinh trưởng tại Lisbon, Bồ Đào Nha, là một kinh sĩ dòng Thánh Augustinô đã gia nhập Dòng Anh Em Hèn Mọn Phanxicô sau khi chứng kiến thi hài các vị tử đạo Phanxicô đầu tiên tại Maroc. Với sự uyên bác Kinh Thánh phi thường và tài hùng biện bốc lửa, ngài được mệnh danh là 'Búa Đập Dị Giáo' (*Malleus Haereticorum*) và 'Hòm Bia Giao Ước' (*Arca Testamenti*).\n\nSứ vụ giảng thuyết của ngài tại miền bắc nước Ý và miền nam nước Pháp được Thiên Chúa chuẩn nhận qua vô số phép lạ, như đàn cá ở Rimini nổi lên bờ nghe ngài giảng đạo khi những kẻ dị giáo bỏ đi, hay con lừa nhịn đói đã quỳ gối phục lạy trước Mình Thánh Chúa làm sáng tỏ đức tin cho kẻ hoài nghi.\n\nThánh Antôn qua đời tại tu viện Arcella gần Pađôva ngày 13 tháng 6 năm 1231 ở tuổi 35. Ba mươi năm sau, khi Thánh Bonaventura mở mộ ngài năm 1263, toàn bộ thi thể đã tan biến thành tro bụi ngoại trừ chiếc Lưỡi Thánh vẫn hoàn toàn tươi hồng nguyên vẹn—dấu chỉ Thiên Chúa chúc phúc cho chiếc lưỡi đã không mệt mỏi rao giảng Lời Chúa. Đại Vương Cung Thánh Đường (*Il Santo*) đón hàng triệu khách hành hương đến khẩn cầu ơn phù trợ mỗi năm.",
        "scripture_reading": "Luke 4:18-19",
        "suggested_prayer_en": "O Wonder-Working Saint Anthony of Padua, Evangelical Doctor and Helper in All Needs, you possessed an ardent love for the Infant Jesus and an unwearied zeal for the lost. Intercede for us in our temporal and spiritual trials, help us recover what is lost in our lives, and draw our hearts to the eternal treasures of Heaven. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Antôn Pađôva hay làm phép lạ, Tiến Sĩ Phúc Âm và là Đấng Bầu Cử trong mọi cơn gian nan, ngài đã hết lòng yêu mến Chúa Hài Đồng Giêsu và luôn thao thức tìm kiếm những con chiên lạc. Xin ngài cầu bầu cho chúng con trong những cơn thử thách phần hồn phần xác, giúp chúng con tìm lại những gì đã mất và hướng lòng chúng con về kho tàng vĩnh cửu trên Quê Trời. Amen.",
        "primary_sources": [
            {
                "label": "Basilica del Santo Official Historical and Relic Documentation",
                "url": "https://www.santantonio.org/en",
                "type": "academic"
            },
            {
                "label": "Pope Pius XII - Apostolic Letter Antoniana Solemnia Declaring Saint Anthony a Doctor of the Church (1946)",
                "url": "https://www.vatican.va/content/pius-xii/la/apost_letters/documents/hf_p-xii_apl_19460116_antoniana-solemnia.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "st_thomas_aquinas_toulouse",
        "category": "doctor_of_church",
        "name_en": "Church of the Jacobins (Tomb of Saint Thomas Aquinas)",
        "name_vi": "Đền Thờ Các Cha Dòng Đaminh (Lăng Mộ Thánh Tôma Aquinô)",
        "feast_day_association": "Feast of Saint Thomas Aquinas, Doctor of the Church (January 28)",
        "location": {
            "shrine_or_basilica": "Église des Jacobins de Toulouse",
            "city": "Toulouse",
            "region_or_state": "Occitanie (Haute-Garonne)",
            "country": "France",
            "latitude": 43.6033,
            "longitude": 1.4406,
            "precision": "chapel_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1369-01-28",
            "approving_authority": "Pope Urban V (Papal Translation) / Pope John XXII (Canonization 1323)",
            "confidence": "confirmed",
            "confidence_note_en": "Canonized by Pope John XXII in 1323; solemn translation of his relics to the Dominican mother church of Toulouse ordered by Blessed Pope Urban V in 1369; declared Universal Doctor of the Church (*Doctor Angelicus*) by Pope Saint Pius V in 1567.",
            "confidence_note_vi": "Được Đức Giáo hoàng Gioan XXII tuyên thánh năm 1323; Đức Chân Phước Urbanô V truyền lệnh rước thánh tích về tu viện mẹ Đaminh tại Toulouse năm 1369; Đức Thánh Cha Piô V tuyên phong là Tiến Sĩ Thiên Thần (*Doctor Angelicus*) năm 1567."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Major Relics and Skull of Saint Thomas Aquinas, the Angelic Doctor",
                "relic_name_vi": "Xương Thánh và Hộp Sọ của Thánh Tôma Aquinô, Tiến Sĩ Thiên Thần",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Gilded reliquary altar beneath the Palm Tree column of the Church of the Jacobins"
            }
        ],
        "historical_summary_en": "Saint Thomas Aquinas (1225–1274), the 'Angelic Doctor' (*Doctor Angelicus*), was the supreme philosopher and theologian of the Catholic Church, synthesizing Aristotelian philosophy with Christian divine revelation in his monumental masterwork, the *Summa Theologiae*. Joining the Dominican Order of Preachers against fierce family opposition, Thomas studied under Saint Albert the Great in Paris and Cologne.\n\nEndowed with profound mystical contemplation as well as intellectual brilliance, Thomas composed the sublime liturgical hymns for the Feast of Corpus Christi (*Pange Lingua*, *Tantum Ergo*, *Panis Angelicus*) at the request of Pope Urban IV. In December 1273, after experiencing an overpowering mystical ecstasy during Mass in Naples, he set down his pen, declaring: *'All that I have written seems like straw to me compared to what I have seen and what has been revealed to me.'*\n\nThomas died at the Cistercian Abbey of Fossanova on March 7, 1274, en route to the Council of Lyon. In 1369, Pope Urban V transferred his relics to the mother convent of the Dominican Order in Toulouse, where they rest beneath the famous 28-ribbed 'Palm Tree' pillar (*Le Palmier des Jacobins*).",
        "historical_summary_vi": "Thánh Tôma Aquinô (1225–1274), 'Tiến Sĩ Thiên Thần' (*Doctor Angelicus*), là nhà triết học và thần học lỗi lạc bậc nhất của Hội Thánh Công giáo, người đã tổng hợp triết học Aristotle với Mạc Khải Kitô giáo trong kiệt tác vĩ đại *Summa Theologiae* (Tổng Luận Thần Học). Vượt qua sự ngăn cấm khắc nghiệt của gia đình quý tộc, ngài gia nhập Dòng Thuyết Giáo (Dòng Đaminh) và theo học dưới sự hướng dẫn của Thánh Albertô Cả tại Paris và Cologne.\n\nKhông chỉ có trí tuệ siêu phàm, Thánh Tôma còn là một nhà chiêm niệm thánh thiện sâu sắc. Ngài đã sáng tác các bài thánh ca phụng vụ tuyệt mỹ cho Đại Lễ Mình Máu Thánh Chúa (*Pange Lingua*, *Tantum Ergo*, *Panis Angelicus*) theo yêu cầu của Đức Giáo hoàng Urbanô IV. Tháng 12 năm 1273, sau một thị kiến thần bí sâu xa trong Thánh Lễ tại Naples, ngài đã gác bút và thốt lên: *'Tất cả những gì tôi đã viết chỉ như rơm rác so với những gì tôi đã được chiêm ngưỡng và được mạc khải.'*\n\nThánh Tôma qua đời tại Tu viện Fossanova ngày 7 tháng 3 năm 1274 trên đường tham dự Công đồng Lyon. Năm 1369, Đức Giáo hoàng Urbanô V đã chuyển di hài ngài về tu viện mẹ của Dòng Đaminh tại Toulouse, nơi thánh tích ngài an nghỉ dưới cột trụ hình cây cọ nổi tiếng (*Le Palmier des Jacobins*).",
        "scripture_reading": "Wisdom 7:7-10",
        "suggested_prayer_en": "O Angelic Doctor Saint Thomas Aquinas, Light of the Church and Model of Theologians, you sought nothing on earth but Christ alone (*'Non nisi Te, Domine'*). Grant us clarity of mind to comprehend the mysteries of faith, humility of heart to seek divine wisdom above all worldly knowledge, and a burning devotion to the Holy Eucharist. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Tôma Aquinô Tiến Sĩ Thiên Thần, Ngọn Đuốc của Hội Thánh và là Khuôn Vàng Thước Ngọc của các nhà thần học, ngài không tìm kiếm điều gì trên trần gian ngoài một mình Chúa Kitô (*'Non nisi Te, Domine'*). Xin ban cho trí tuệ chúng con sự sáng suốt để hiểu thấu các mầu nhiệm đức tin, ban cho tâm hồn chúng con đức khiêm nhường để tìm kiếm sự khôn ngoan Thiên Chúa và lòng sùng kính tha thiết Bí Tích Thánh Thể. Amen.",
        "primary_sources": [
            {
                "label": "Pope Leo XIII - Encyclical Aeterni Patris on the Restoration of Christian Philosophy according to St. Thomas (1879)",
                "url": "https://www.vatican.va/content/leo-xiii/en/encyclicals/documents/hf_l-xiii_enc_04081879_aeterni-patris.html",
                "type": "vatican"
            },
            {
                "label": "Couvent des Jacobins de Toulouse Official Historical Archives",
                "url": "https://www.jacobins.toulouse.fr/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "st_augustine_pavia",
        "category": "doctor_of_church",
        "name_en": "Basilica of San Pietro in Ciel d'Oro (Tomb of Saint Augustine)",
        "name_vi": "Đại Vương Cung Thánh Đường San Pietro in Ciel d'Oro (Lăng Mộ Thánh Augustinô)",
        "feast_day_association": "Feast of Saint Augustine of Hippo, Doctor of the Church (August 28)",
        "location": {
            "shrine_or_basilica": "Basilica di San Pietro in Ciel d'Oro",
            "city": "Pavia",
            "region_or_state": "Lombardy",
            "country": "Italy",
            "latitude": 45.1894,
            "longitude": 9.1558,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "0725-01-01",
            "approving_authority": "King Liutprand of the Lombards / Pope Leo XIII / Pope Benedict XVI (Visit 2007)",
            "confidence": "confirmed",
            "confidence_note_en": "Relics translated from Sardinia to Pavia c. 725 AD by Lombard King Liutprand to protect them from Saracen raids; enclosed in the 14th-century Gothic marble masterpiece *Arca di Sant'Agostino*; confirmed by archaeological excavations in 1695 and papal visit of Benedict XVI in 2007.",
            "confidence_note_vi": "Hài cốt được Vua Lombard Liutprand rước từ Sardinia về Pavia khoảng năm 725 để bảo vệ khỏi quân Saracen; được an vị trong kiệt tác cẩm thạch Gothic thế kỷ 14 *Arca di Sant'Agostino*; được kiểm nghiệm khảo cổ năm 1695 và Đức Biển Đức XVI viếng thăm năm 2007."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Sacred Bones of Saint Augustine, Bishop of Hippo and Doctor of Grace",
                "relic_name_vi": "Hài Cốt Thánh Augustinô, Giám Mục Hippo và Tiến Sĩ Ân Sủng",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Arca di Sant'Agostino at the High Altar of San Pietro in Ciel d'Oro"
            }
        ],
        "historical_summary_en": "Saint Augustine of Hippo (354–430), the 'Doctor of Grace' (*Doctor Gratiae*), stands as the intellectual colossus of Western Christianity. Born in Thagaste (modern Algeria) to Saint Monica, Augustine wandered through the errors of Manichaeism and moral dissipation before experiencing his dramatic conversion in Milan under Saint Ambrose in 386, crying out: *'Late have I loved you, O Beauty ever ancient, ever new!'*\n\nAs Bishop of Hippo Regius, Augustine defended Catholic orthodoxy against Donatism, Pelagianism, and Arianism, authoring over five million words including the immortal spiritual autobiography *Confessions* and the monumental theology of history *The City of God* (*De Civitate Dei*).\n\nAugustine died on August 28, 430, as the Vandals besieged Hippo. When North Africa fell to Islamic conquest in the 8th century, King Liutprand of the Lombards purchased the sacred body for a great sum to rescue it from desecration, translating it to Pavia around 725 AD. Today, the Apostle of Grace rests within the *Arca di Sant'Agostino*, an exquisite 14th-century Gothic shrine adorned with ninety-five marble statues depicting his life.",
        "historical_summary_vi": "Thánh Augustinô thành Hippo (354–430), 'Tiến Sĩ Ân Sủng' (*Doctor Gratiae*), là một trong những cột trụ tư tưởng vĩ đại nhất của Kitô giáo Tây Phương. Sinh tại Thagaste (nay thuộc Algeria) là con của Thánh Nữ Monica, ngài từng lạc lối trong tà thuyết Manikê và lối sống đam mê nhục dục trước khi trải qua cuộc trở lại đạo kỳ diệu tại Milan năm 386 nhờ sự hướng dẫn của Thánh Ambrose, thốt lên lời nguyện bất hủ: *'Lạy Vẻ Đẹp cổ kính mà luôn tươi mới, con đã yêu Chúa quá muộn màng!'*\n\nTrên cương vị Giám mục Hippo Regius, ngài bảo vệ giáo lý chính truyền chống lại các bè rối Donatô, Pelagiô và Ariô, để lại gia sản hơn năm triệu từ ngữ thần học, nổi bật là tập tự thuật *Tự Thuật* (*Confessiones*) và kiệt tác *Thành Đô Thiên Chúa* (*De Civitate Dei*).\n\nThánh Augustinô qua đời ngày 28 tháng 8 năm 430 khi quân Vandal đang vây hãm thành Hippo. Vào thế kỷ thứ 8 khi Bắc Phi bị Hồi giáo chiếm đóng, Vua Liutprand nước Lombard đã dùng một số tiền lớn chuộc lại thánh tích ngài và rước về Pavia vào khoảng năm 725. Ngày nay, vị Tiến sĩ Ân Sủng an nghỉ trong kiệt tác cẩm thạch *Arca di Sant'Agostino* thế kỷ 14 chạm khắc 95 pho tượng tuyệt mỹ.",
        "scripture_reading": "Romans 13:13-14",
        "suggested_prayer_en": "O Great Doctor of Grace Saint Augustine, you sought Truth restlessly until your heart found its rest in God (*'Inquietum est cor nostrum donec requiescat in Te'*). Convert the hearts of all who wander in spiritual darkness; inflame our souls with a burning love for the Divine Beauty, and grant us perseverance in grace. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Augustinô Tiến Sĩ Ân Sủng, tâm hồn ngài từng khắc khoải không yên cho đến khi được nghỉ yên trong Chúa (*'Inquietum est cor nostrum donec requiescat in Te'*). Xin hoán cải tâm hồn những ai đang lạc lối trong bóng tối sai lầm; thắp lên trong lòng chúng con tình yêu nồng nàn dành cho Vẻ Đẹp Chân Lý Tuyệt Đối và ban cho chúng con ơn bền đỗ trong ân sủng đến cùng. Amen.",
        "primary_sources": [
            {
                "label": "Pope Benedict XVI - Homily at the Basilica of San Pietro in Ciel d'Oro, Pavia (April 22, 2007)",
                "url": "https://www.vatican.va/content/benedict-xvi/en/homilies/2007/documents/hf_ben-xvi_hom_20070422_pavia.html",
                "type": "vatican"
            },
            {
                "label": "Diocesi di Pavia - Official Arca di Sant'Agostino Archival Records",
                "url": "https://www.diocesi.pavia.it/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "st_benedict_and_scholastica_montecassino",
        "category": "doctor_of_church",
        "name_en": "Abbey of Montecassino (Tomb of Saint Benedict and Saint Scholastica)",
        "name_vi": "Đại Đan Viện Montecassino (Lăng Mộ Thánh Biển Đức và Thánh Nữ Scholastica)",
        "feast_day_association": "Feast of Saint Benedict, Patron of Europe (July 11) / Saint Scholastica (February 10)",
        "location": {
            "shrine_or_basilica": "Abbazia Territoriale di Montecassino",
            "city": "Cassino",
            "region_or_state": "Frosinone, Lazio",
            "country": "Italy",
            "latitude": 41.4900,
            "longitude": 13.8142,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1071-10-01",
            "approving_authority": "Pope Alexander II / Pope Paul VI (Proclaimed Patron of Europe 1964)",
            "confidence": "confirmed",
            "confidence_note_en": "Continuous monastic possession since Saint Benedict founded the abbey in 529 AD; tomb beneath the High Altar verified by archaeological surveys following WWII reconstruction (1950-1955); proclaimed Principal Patron of Europe by Pope Paul VI in 1964.",
            "confidence_note_vi": "Được đan viện bảo tồn liên tục từ khi Thánh Biển Đức lập tu viện năm 529; ngôi mộ dưới bàn thờ chính được kiểm chứng khảo cổ khi tái thiết sau Thế chiến II (1950-1955); được Đức Phaolô VI tuyên phong là Thánh Quan Thầy Toàn Châu Âu năm 1964."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Sarcophagus and Sacred Bones of Saint Benedict of Nursia and his Twin Sister Saint Scholastica",
                "relic_name_vi": "Quan Tài Hài Cốt Thánh Biển Đức Núrsia và Em Gái Song Sinh Thánh Nữ Scholastica",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Beneath the High Altar of the Basilica of Montecassino"
            }
        ],
        "historical_summary_en": "Saint Benedict of Nursia (c. 480–547), the 'Father of Western Monasticism' and Patron of Europe, withdrew from decadent Rome to live as a solitary hermit in the cave of Subiaco (*Sacro Speco*). In 529 AD, he climbed the mountain of Montecassino, demolished an ancient pagan temple to Apollo, and founded the cradle of Western monastic life. There he penned the immortal *Rule of Saint Benedict* (*Regula Benedicti*), harmonizing prayer and work under the motto *Ora et Labora*.\n\nHis twin sister, Saint Scholastica (c. 480–547), consecrated herself to God and founded a nearby monastery of nuns at Plumbariola. In a famous episode recorded by Pope Saint Gregory the Great in his *Dialogues*, when Benedict refused to prolong their final spiritual conversation past nightfall, Scholastica prayed with tears, prompting a violent thunderstorm that forced Benedict to stay, demonstrating that *'she was able to do more because she loved more.'*\n\nWhen Scholastica died days later, Benedict saw her soul ascend to Heaven in the likeness of a white dove; he laid her body in the tomb he had prepared for himself. Upon Benedict's death in 547, he was buried beside his sister in the same sepulcher beneath the high altar.",
        "historical_summary_vi": "Thánh Biển Đức thành Núrsia (khoảng 480–547), 'Tổ Phụ Đan Tu Tây Phương' và Quan Thầy Châu Âu, đã rời bỏ chốn phồn hoa trụy lạc của thành Rome để sống ẩn tu trong hang đá Subiaco (*Sacro Speco*). Năm 529, ngài lên đỉnh núi Montecassino, phá bỏ đền thờ tà thần Apollo để sáng lập cái nôi của đời sống đan tu Tây Phương. Tại đây ngài đã viết bản *Tu Luật Thánh Biển Đức* (*Regula Benedicti*) bất hủ, kết hợp hài hòa cầu nguyện và lao động qua châm ngôn *Ora et Labora* (Cầu nguyện và Lao động).\n\nNgười em gái song sinh của ngài là Thánh Nữ Scholastica (khoảng 480–547) cũng dâng mình cho Chúa và lập tu viện nữ tại Plumbariola gần đó. Trong biến cố nổi tiếng được Thánh Giáo hoàng Grêgôriô Cả ghi lại trong *Đối Thoại*, khi Thánh Biển Đức từ chối ở lại đàm đạo linh thiêng qua đêm, Thánh Nữ Scholastica đã khóc lóc cầu nguyện khiến trời nổi giông bão dữ dội buộc anh mình phải ở lại, minh chứng rằng *'người làm được nhiều hơn vì người đã yêu mến nhiều hơn.'*\n\nKhi Thánh Scholastica qua đời ít ngày sau đó, Thánh Biển Đức nhìn thấy linh hồn em gái bay lên trời dưới hình chim bồ câu trắng; ngài đã an táng em trong ngôi mộ ngài chuẩn bị cho mình. Khi Thánh Biển Đức qua đời năm 547, ngài được chôn cất chung một huyệt mộ với em gái dưới bàn thờ chính.",
        "scripture_reading": "Colossians 3:1-3",
        "suggested_prayer_en": "O Holy Patriarch Saint Benedict and Seraphic Virgin Saint Scholastica, you laid the spiritual foundations of Christian civilization through prayer, labor, and fraternal charity. Teach us to prefer nothing whatever to Christ (*'Christo omnino nihil praeponere'*), preserve peace in our monasteries and families, and guide our world back to God. Amen.",
        "suggested_prayer_vi": "Lạy Tổ Phụ Thánh Biển Đức và Thánh Nữ Đồng Trinh Scholastica, hai thánh đã đặt nền móng tâm linh vững chắc cho nền văn minh Kitô giáo qua đời sống cầu nguyện, lao động và đức ái huynh đệ. Xin dạy chúng con đừng chuộng sự gì hơn Chúa Kitô (*'Christo omnino nihil praeponere'*), gìn giữ bình an trong các gia đình, tu viện và dẫn đưa thế giới trở về cùng Thiên Chúa. Amen.",
        "primary_sources": [
            {
                "label": "Pope Saint Gregory the Great - Life and Miracles of Saint Benedict (Dialogues, Book II)",
                "url": "https://www.osb.org/our-roots/the-life-of-saint-benedict-by-st-gregory-the-great/",
                "type": "encyclopedia"
            },
            {
                "label": "Pope Paul VI - Apostolic Letter Pacis Nuntius Proclaiming St. Benedict Patron of Europe (1964)",
                "url": "https://www.vatican.va/content/paul-vi/la/apost_letters/documents/hf_p-vi_apl_19641024_pacis-nuntius.html",
                "type": "vatican"
            }
        ]
    }
]

BATCH_6 = [
    {
        "sanctuary_id": "st_dominic_bologna",
        "category": "monastic_sanctuary",
        "name_en": "Basilica of San Domenico (Arca di San Domenico)",
        "name_vi": "Đại Vương Cung Thánh Đường Thánh Đaminh (Bologna)",
        "feast_day_association": "Feast of Saint Dominic, Priest and Founder (August 8)",
        "location": {
            "shrine_or_basilica": "Basilica Patriarcale di San Domenico",
            "city": "Bologna",
            "region_or_state": "Emilia-Romagna",
            "country": "Italy",
            "latitude": 44.4897,
            "longitude": 11.3444,
            "precision": "chapel_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1234-07-13",
            "approving_authority": "Pope Gregory IX (Papal Bull Fons Sapientiae)",
            "confidence": "confirmed",
            "confidence_note_en": "Canonized by Pope Gregory IX in 1234; tomb adorned by Nicola Pisano, Niccolò dell'Arca, and young Michelangelo Buonarroti; body verified and preserved in the Arca di San Domenico.",
            "confidence_note_vi": "Được Đức Giáo hoàng Grêgôriô IX tuyên thánh năm 1234; lăng mộ do các danh họa Nicola Pisano, Niccolò dell'Arca và Michelangelo chạm khắc; thi hài được bảo tồn nguyên vẹn tại Arca di San Domenico."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Sacred Relics and Skull of Saint Dominic de Guzmán, Founder of the Order of Preachers",
                "relic_name_vi": "Hài Cốt và Hộp Sọ Thánh Đaminh de Guzmán, Đấng Sáng Lập Dòng Thuyết Giáo",
                "relic_type": "1st_class_bone",
                "reliquary_location": "The Monumental Arca di San Domenico inside the Saint Dominic Chapel"
            }
        ],
        "historical_summary_en": "Saint Dominic de Guzmán (1170–1221), born in Caleruega, Spain, founded the Order of Preachers (Dominicans) to combat the Albigensian heresy in southern France through rigorous intellectual defense of orthodox doctrine combined with radical evangelical poverty. Convinced that heretics could only be won through authentic Gospel witness and theological competence, Dominic sent his friars to the great university centers of Paris and Bologna.\n\nDominic lived a life of intense asceticism and perpetual contemplation, famously described as 'only speaking to God or of God' (*aut de Deo aut cum Deo*). Tradition attributes to Dominic the reception and global propagation of the Holy Rosary as a spiritual weapon of conversion.\n\nExhausted by preaching tours across Europe, Dominic died at the convent of Saint Nicholas in Bologna on August 6, 1221, promising his weeping brethren: *'Do not weep, for I shall be more useful to you after my death and I shall help you then more effectively than during my life.'* His tomb (*Arca di San Domenico*) is an artistic summit featuring sculptures by Nicola Pisano, Arnolfo di Cambio, and the youthful Michelangelo.",
        "historical_summary_vi": "Thánh Đaminh de Guzmán (1170–1221), sinh tại Caleruega, Tây Ban Nha, đã sáng lập Dòng Thuyết Giáo (Dòng Đaminh) nhằm đẩy lùi bè rối Albi tại miền nam nước Pháp bằng lập luận thần học uyên bác kết hợp với đời sống khó nghèo thánh thiện theo Phúc Âm. Với xác tín rằng chỉ có thể chinh phục kẻ lầm lạc bằng đời sống chứng nhân đích thực, Thánh Đaminh đã cử các tu sĩ của mình đến các trung tâm đại học lớn tại Paris và Bologna.\n\nNgài sống đời khổ chế nghiêm ngặt và chiêm niệm liên lỉ, với châm ngôn sống nổi tiếng là 'chỉ nói với Chúa hoặc nói về Chúa' (*aut de Deo aut cum Deo*). Truyền thống thánh thiện ghi nhận Thánh Đaminh đã đón nhận và truyền bá sâu rộng Chuỗi Mân Côi như vũ khí thiêng liêng hoán cải nhân loại.\n\nKiệt sức vì các chuyến truyền giáo khắp cõi Châu Âu, Thánh Đaminh qua đời tại tu viện Thánh Nicôla ở Bologna ngày 6 tháng 8 năm 1221, để lại lời hứa an ủi các môn đệ: *'Anh em đừng khóc, sau khi chết Thầy sẽ giúp ích cho anh em hữu hiệu hơn khi còn sống.'* Lăng mộ ngài (*Arca di San Domenico*) là kiệt tác nghệ thuật điêu khắc với sự đóng góp của Nicola Pisano và Michelangelo thời trẻ.",
        "scripture_reading": "2 Timothy 4:1-5",
        "suggested_prayer_en": "O Holy Father Saint Dominic, Preacher of Grace and Defender of the True Faith, you fulfilled your promise to intercede for your children before the throne of God. Illuminate our minds with the light of Catholic truth, inflame our hearts with apostolic zeal for the salvation of souls, and teach us to pray the Holy Rosary with devout contemplation. Amen.",
        "suggested_prayer_vi": "Lạy Cha Thánh Đaminh, Sứ Giả của Ân Sủng và Đấng Bảo Vệ Đức Tin Chân Thật, ngài đã giữ trọn lời hứa chuyển cầu cho đoàn con cái trước tòa Thiên Chúa. Xin soi sáng tâm trí chúng con bằng chân lý Tin Mừng, thắp lên trong lòng chúng con ngọn lửa nhiệt thành cứu rỗi các linh hồn và dạy chúng con biết sốt sắng lần chuỗi Mân Côi mỗi ngày. Amen.",
        "primary_sources": [
            {
                "label": "Curia Generalis Ordinis Praedicatorum (Dominican Curia) Official Historical Dossier",
                "url": "https://www.op.org/",
                "type": "academic"
            },
            {
                "label": "Pope Honorius III - Papal Bull Religiosam Vitam Confirming the Order of Preachers (1216)",
                "url": "https://www.vatican.va/content/vatican/en.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "st_therese_of_lisieux",
        "category": "doctor_of_church",
        "name_en": "Basilica of Saint Thérèse of Lisieux",
        "name_vi": "Đại Vương Cung Thánh Đường Thánh Têrêsa Hài Đồng Giêsu (Lisieux)",
        "feast_day_association": "Feast of Saint Thérèse of the Child Jesus, Doctor of the Church (October 1)",
        "location": {
            "shrine_or_basilica": "Basilique Sainte-Thérèse de Lisieux",
            "city": "Lisieux",
            "region_or_state": "Normandy (Calvados)",
            "country": "France",
            "latitude": 49.1397,
            "longitude": 0.2356,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1954-07-11",
            "approving_authority": "Pope Pius XI (Canonization 1925) / Pope John Paul II (Doctor of the Church 1997)",
            "confidence": "confirmed",
            "confidence_note_en": "Canonized by Pope Pius XI in 1925, who hailed her as the 'Star of his Pontificate'; declared Universal Patroness of Missions alongside Saint Francis Xavier in 1927; proclaimed Doctor of the Church (*Doctor Amoris*) by Pope John Paul II in 1997.",
            "confidence_note_vi": "Được Đức Giáo hoàng Piô XI tuyên thánh năm 1925 và tôn vinh là 'Ngôi Sao Triều Đại Giáo Hoàng'; Đức Piô XI tuyên phong là Bổn Mạng Các Xứ Truyền Giáo năm 1927; được Đức Gioan Phaolô II tuyên phong là Tiến Sĩ Hội Thánh (*Doctor Amoris*) năm 1997."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Major Reliquary of Saint Thérèse and the Carmel Crypt",
                "relic_name_vi": "Hòm Thánh Tích Thánh Nữ Têrêsa Hài Đồng Giêsu và Hầm Mộ Dòng Kín Carmêlô",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Carmel Chapel Shrine and Crypt of the Basilica of Saint Thérèse, Lisieux"
            }
        ],
        "historical_summary_en": "Saint Thérèse of Lisieux (Marie Françoise-Thérèse Martin, 1873–1897), known as the 'Little Flower of Jesus,' entered the Discalced Carmelite monastery of Lisieux at the age of fifteen after making a personal appeal to Pope Leo XIII in Rome. Living an entirely hidden life of contemplative prayer, she developed her revolutionary spiritual doctrine known as the 'Little Way' (*la petite voie*)—a path of spiritual childhood characterized by total trust, complete abandonment to God's merciful love, and sanctifying the smallest everyday actions.\n\nBefore succumbing to tuberculosis at the age of twenty-four, Thérèse wrote her spiritual autobiography *Story of a Soul* (*Histoire d'une âme*), which was translated into over sixty languages, sparking an unprecedented global wave of devotion. She promised: *'I want to spend my heaven in doing good upon earth. I will let fall a shower of roses.'*\n\nThe colossal Romano-Byzantine Basilica in Lisieux, consecrated in 1954, is France's second-most visited pilgrimage site after Lourdes. In 1997, on the centenary of her death, Pope John Paul II declared her the thirty-third Doctor of the Church—the youngest in ecclesiastical history.",
        "historical_summary_vi": "Thánh Nữ Têrêsa Hài Đồng Giêsu (Marie Françoise-Thérèse Martin, 1873–1897), 'Bông Hoa Nhỏ Của Chúa Giêsu', đã gia nhập Đan viện Cát Minh Kín tại Lisieux năm 15 tuổi sau khi đích thân khẩn khoản xin Đức Giáo hoàng Lêô XIII tại Roma. Sống đời chiêm niệm âm thầm khiêm hạ, ngài đã phát triển linh đạo 'Con Đường Nhỏ' (*la petite voie*)—con đường thơ ấu thiêng liêng dựa trên lòng phó thác trọn vẹn vào tình yêu thương xót của Chúa và thánh hóa từng cử chỉ nhỏ bé thường ngày.\n\nTrước khi qua đời vì bệnh lao phổi ở tuổi 24, Thánh Têrêsa đã hoàn tất tập tự thuật *Một Tâm Hồn* (*Histoire d'une âme*), được dịch ra hơn 60 ngôn ngữ và tạo nên làn sóng sùng kính kinh ngạc khắp thế giới. Ngài đã hứa trước khi nhắm mắt: *'Tôi muốn dùng cả thiên đàng của tôi để làm việc lành trên trần gian. Tôi sẽ làm mưa hoa hồng tuôn đổ xuống đất.'*\n\nĐại Vương Cung Thánh Đường Lisieux theo phong cách La Mã-Byzantine tráng lệ thánh hiến năm 1954 là trung tâm hành hương lớn thứ hai tại Pháp chỉ sau Lộ Đức. Năm 1997, nhân kỷ niệm 100 năm ngày ngài qua đời, Đức Thánh Cha Gioan Phaolô II đã long trọng tuyên phong ngài là Tiến Sĩ Hội Thánh trẻ tuổi nhất trong lịch sử.",
        "scripture_reading": "Matthew 18:3-4",
        "suggested_prayer_en": "O Saint Thérèse of the Child Jesus, Doctor of Divine Love and Patroness of Missions, you promised to spend your Heaven doing good upon earth. Shower your roses of grace upon our lives; teach us your Little Way of trust and surrender, and make our hearts burn with pure love for Jesus and the salvation of souls. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Nữ Têrêsa Hài Đồng Giêsu, Tiến Sĩ Tình Yêu và là Quan Thầy Các Xứ Truyền Giáo, ngài đã hứa dùng cả thiên đàng để làm việc lành cho trần gian. Xin tuôn đổ mưa hoa hồng ân sủng trên cuộc đời chúng con; dạy chúng con đi theo Con Đường Nhỏ của lòng cậy trông phó thác và thắp lên trong tâm hồn chúng con tình yêu mến Chúa nồng nàn để cứu rỗi các linh hồn. Amen.",
        "primary_sources": [
            {
                "label": "Pope John Paul II - Apostolic Letter Divini Amoris Scientia Declaring St. Thérèse a Doctor of the Church (1997)",
                "url": "https://www.vatican.va/content/john-paul-ii/en/apost_letters/1997/documents/hf_jp-ii_apl_17101997_divini-amoris.html",
                "type": "vatican"
            },
            {
                "label": "Sanctuaire Sainte-Thérèse de Lisieux Official Archives",
                "url": "https://www.therese-de-lisieux.catholique.fr/en/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "st_padre_pio_san_giovanni_rotondo",
        "category": "monastic_sanctuary",
        "name_en": "Sanctuary of Saint Pio of Pietrelcina (San Giovanni Rotondo)",
        "name_vi": "Đền Thánh Cha Thánh Piô Năm Dấu Thánh (San Giovanni Rotondo)",
        "feast_day_association": "Feast of Saint Pio of Pietrelcina (September 23)",
        "location": {
            "shrine_or_basilica": "Santuario di San Pio da Pietrelcina (Santa Maria delle Grazie)",
            "city": "San Giovanni Rotondo",
            "region_or_state": "Foggia, Apulia",
            "country": "Italy",
            "latitude": 41.7067,
            "longitude": 15.7042,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "2002-06-16",
            "approving_authority": "Pope John Paul II (Canonization in Rome)",
            "confidence": "confirmed",
            "confidence_note_en": "Canonized by Pope Saint John Paul II before 300,000 pilgrims in Saint Peter's Square on June 16, 2002; body exhumed in 2008 and found remarkably intact, venerated in the golden crypt designed by Renzo Piano.",
            "confidence_note_vi": "Được Thánh Giáo hoàng Gioan Phaolô II tuyên thánh ngày 16 tháng 6 năm 2002 trước 300.000 tín hữu; thi hài được khai quật năm 2008 và được bảo tồn nguyên vẹn trong hầm mộ dát vàng do kiến trúc sư Renzo Piano thiết kế."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Incorrupt Body, Stigmatized Gloves, and Blood Relics of Saint Padre Pio",
                "relic_name_vi": "Thi Hài Nguyên Vẹn, Găng Tay và Máu Thánh của Cha Thánh Piô Năm Dấu",
                "relic_type": "incorrupt_body",
                "reliquary_location": "Crystal Reliquary Crypt inside the Sanctuary Church of Saint Pio"
            }
        ],
        "historical_summary_en": "Saint Pio of Pietrelcina (Francesco Forgione, 1887–1968), known throughout the world as Padre Pio, was an Italian Capuchin Franciscan priest who lived at the friary of Our Lady of Grace in San Giovanni Rotondo on the Gargano peninsula. On September 20, 1918, while praying in thanksgiving after Mass in the choir loft, he received the visible Stigmata—the five bleeding wounds of Jesus Christ—which he bore continuously for exactly fifty years until their miraculous disappearance just before his death in 1968.\n\nPadre Pio was endowed with extraordinary charisms, including bilocation, reading of souls in confession, prophetic discernment, physical healing, and the odor of sanctity (a fragrant scent of roses and violets emanating from his wounds). He spent up to sixteen hours a day hearing confessions, reconciling tens of thousands of souls to God.\n\nIn addition to his immense spiritual ministry, Padre Pio founded the *Casa Sollievo della Sofferenza* ('Home for the Relief of Suffering'), one of Europe's premier research hospitals, as a living monument to Christian charity. The sanctuary attracts over six million pilgrims annually to contemplate the mystery of redemptive suffering.",
        "historical_summary_vi": "Cha Thánh Piô Năm Dấu (Francesco Forgione, 1887–1968), sinh tại Pietrelcina, là linh mục Dòng Anh Em Hèn Mọn Capuchin tại tu viện Đức Mẹ Ban Ơn ở San Giovanni Rotondo trên bán đảo Gargano. Ngày 20 tháng 9 năm 1918, khi đang cầu nguyện tạ ơn sau Thánh Lễ trên gác đàn, ngài đã được in Năm Dấu Thánh rỉ máu của Chúa Giêsu trên thân thể—và mang các vết thương đau đớn này liên tục suốt đúng 50 năm cho đến khi chúng tự động biến mất không dấu vết ngay trước khi ngài qua đời năm 1968.\n\nCha Thánh Piô được Chúa ban cho những đặc sủng phi thường như hiện diện hai nơi cùng lúc (song vị trí), đọc thấu tâm hồn các hối nhân trong tòa giải tội, tiên tri, chữa lành bệnh tật và tỏa hương thơm hoa hồng từ các vết thương. Ngài ngồi tòa giải tội tới 16 tiếng mỗi ngày, đưa hàng chục vạn tâm hồn trở về hòa giải với Thiên Chúa.\n\nBên cạnh sứ vụ thiêng liêng vĩ đại, ngài còn sáng lập bệnh viện hiện đại *Casa Sollievo della Sofferenza* ('Ngôi Nhà Xoa Dịu Đau Khổ') để chăm sóc người bệnh nghèo. Đền thánh San Giovanni Rotondo đón nhận hơn 6 triệu khách hành hương mỗi năm đến chiêm ngắm mầu nhiệm đau khổ cứu độ của Chúa Kitô.",
        "scripture_reading": "Galatians 2:20",
        "suggested_prayer_en": "O Saint Padre Pio of Pietrelcina, faithful minister of the Cross and tireless shepherd of souls, you bore upon your body the marks of Christ's Passion. Stay with us in our moments of suffering (*'Resta con me, Signore'*); teach us to pray with deep faith, and bring us the peace of the Risen Lord. Amen.",
        "suggested_prayer_vi": "Lạy Cha Thánh Piô Năm Dấu Thánh, người tôi tớ trung kiên của Thập Giá và là vị mục tử không biết mệt mỏi nơi tòa giải tội, ngài đã mang trên thân xác dấu tích Cuộc Khổ Nạn của Chúa Kitô. Xin ở lại với chúng con trong những giờ phút đau khổ thử thách; dạy chúng con biết cầu nguyện với lòng cậy trông vững vàng và ban cho chúng con bình an của Chúa Kitô Phục Sinh. Amen.",
        "primary_sources": [
            {
                "label": "Pope John Paul II - Homily for the Canonization of Padre Pio of Pietrelcina (June 16, 2002)",
                "url": "https://www.vatican.va/content/john-paul-ii/en/homilies/2002/documents/hf_jp-ii_hom_20020616_padre-pio.html",
                "type": "vatican"
            },
            {
                "label": "Convento Santuario Padre Pio Official Archival Documentation",
                "url": "https://www.padrepio.it/en/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "st_faustina_krakow_lagiewniki",
        "category": "monastic_sanctuary",
        "name_en": "Sanctuary of Divine Mercy (Kraków-Łagiewniki)",
        "name_vi": "Đền Thánh Lòng Chúa Thương Xót (Kraków-Łagiewniki)",
        "feast_day_association": "Feast of Divine Mercy (Second Sunday of Easter) / Saint Faustina (October 5)",
        "location": {
            "shrine_or_basilica": "Sanktuarium Bożego Miłosierdzia w Krakowie-Łagiewnikach",
            "city": "Kraków",
            "region_or_state": "Lesser Poland",
            "country": "Poland",
            "latitude": 50.0200,
            "longitude": 19.9381,
            "precision": "chapel_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "2002-08-17",
            "approving_authority": "Pope John Paul II (Consecration of Basilica and World Entrustment)",
            "confidence": "confirmed",
            "confidence_note_en": "Saint Faustina canonized as the first saint of the Great Jubilee 2000 by Pope John Paul II; Divine Mercy Sunday instituted for the Universal Church; Basilica consecrated and world entrusted to Divine Mercy by John Paul II on August 17, 2002.",
            "confidence_note_vi": "Thánh Faustina được Thánh Giáo hoàng Gioan Phaolô II tuyên thánh là vị thánh đầu tiên của Đại Năm Thánh 2000; Đại Lễ Lòng Chúa Thương Xót được thiết lập cho toàn thể Giáo hội; Vương Cung Thánh Đường được chính Đức Gioan Phaolô II cung hiến và dâng thế giới cho Lòng Thương Xót Chúa năm 2002."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Relics of Saint Faustina Kowalska and the Original Miraculous Image of Divine Mercy",
                "relic_name_vi": "Hài Cốt Thánh Faustina Kowalska và Bức Linh Ảnh Phép Lạ Lòng Chúa Thương Xót",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Convent Chapel of Saint Joseph beneath the Adolf Hyła Divine Mercy Painting"
            }
        ],
        "historical_summary_en": "Saint Maria Faustina Kowalska (Helena Kowalska, 1905–1938), known as the 'Apostle of Divine Mercy,' was a humble Polish religious sister belonging to the Congregation of the Sisters of Our Lady of Mercy in Kraków-Łagiewniki. Between 1931 and 1938, she received frequent mystical apparitions of Jesus Christ, who revealed to her the infinite depths of His unfathomable mercy for poor sinners.\n\nJesus instructed Faustina to have an image painted depicting Him with right hand raised in blessing and two radiant rays—one pale symbolizing water that cleanses souls and one red symbolizing blood that is the life of souls—streaming from His pierced Heart, with the signature *'Jezu, ufam Tobie'* ('Jesus, I trust in You'). Christ also dictated the Chaplet of Divine Mercy, requested the institution of Feast of Divine Mercy on the Second Sunday of Easter, and established the Hour of Great Mercy (3:00 PM).\n\nFaustina recorded these revelations in her 600-page *Diary* (*Divine Mercy in My Soul*). Dying of tuberculosis in 1938 at the age of thirty-three, her spiritual message spread across the globe. Today, the world sanctuary in Łagiewniki stands as the epicentre of divine reconciliation.",
        "historical_summary_vi": "Thánh Nữ Maria Faustina Kowalska (Helena Kowalska, 1905–1938), 'Tông Đồ Lòng Chúa Thương Xót', là một nữ tu khiêm nhường thuộc Dòng Các Nữ Tu Đức Mẹ Đấng Nhân Từ tại tu viện Kraków-Łagiewniki, Ba Lan. Từ năm 1931 đến 1938, ngài liên tục nhận được những thị kiến thần bí từ Chúa Giêsu, Đấng mạc khải cho ngài đại dương vô biên của Lòng Thương Xót Chúa dành cho các tội nhân khốn cùng.\n\nChúa Giêsu truyền dạy Faustina vẽ lại bức Linh Ảnh theo hình ảnh Người hiện ra: tay phải giơ lên chúc lành, từ Trái Tim tuôn trào hai luồng sáng—tia sáng trắng tượng trưng cho Nước thanh tẩy linh hồn và tia sáng đỏ tượng trưng cho Máu là nguồn sống linh hồn—cùng dòng chữ *'Jezu, ufam Tobie'* ('Lạy Chúa Giêsu, con tín thác vào Chúa'). Chúa cũng dạy ngài Kinh Chuỗi Lòng Thương Xót, truyền thiết lập Đại Lễ Lòng Thương Xót vào Chúa Nhật sau Lễ Phục Sinh và Giờ Thương Xót lúc 3 giờ chiều.\n\nThánh Nữ đã ghi chép lại các mạc khải trong tập *Nhật Ký Lòng Thương Xót Chúa Nơi Linh Hồn Tôi*. Qua đời vì bệnh lao năm 1938 khi mới 33 tuổi, sứ điệp của ngài đã lan tỏa khắp địa cầu. Ngày nay, Đền Thánh Quốc Tế tại Łagiewniki là trung tâm hiệp thông và cậy trông lớn nhất của lòng thương xót Chúa.",
        "scripture_reading": "Ephesians 2:4-7",
        "suggested_prayer_en": "Eternal Father, I offer You the Body and Blood, Soul and Divinity of Your dearly beloved Son, Our Lord Jesus Christ, in atonement for our sins and those of the whole world. For the sake of His sorrowful Passion, have mercy on us and on the whole world. Jesus, I trust in You! Amen.",
        "suggested_prayer_vi": "Lạy Cha Hằng Hữu, con xin dâng lên Cha Mình và Máu, Linh Hồn và Thần Tính của Con Rất Yêu Dấu Cha là Đức Giêsu Kitô, Chúa chúng con, để đền vì tội lỗi chúng con và toàn thế giới. Vì cuộc Khổ Nạn đau thương của Chúa Giêsu, xin Cha thương xót chúng con và toàn thế giới. Lạy Chúa Giêsu, con tín thác vào Chúa! Amen.",
        "primary_sources": [
            {
                "label": "Pope John Paul II - Homily for the Canonization of Saint Mary Faustina Kowalska (April 30, 2000)",
                "url": "https://www.vatican.va/content/john-paul-ii/en/homilies/2000/documents/hf_jp-ii_hom_20000430_faustina.html",
                "type": "vatican"
            },
            {
                "label": "Sanctuary of Divine Mercy Kraków-Łagiewniki Official Archives",
                "url": "https://www.milosierdzie.pl/index.php/en/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "st_john_vianney_ars",
        "category": "doctor_of_church",
        "name_en": "Sanctuary of the Curé of Ars (Saint John Vianney)",
        "name_vi": "Đền Thánh Cha Xứ Ars (Thánh Gioan Maria Vianney)",
        "feast_day_association": "Feast of Saint John Vianney, Patron of Parish Priests (August 4)",
        "location": {
            "shrine_or_basilica": "Sanctuaire du Saint Curé d'Ars (Basilique d'Ars)",
            "city": "Ars-sur-Formans",
            "region_or_state": "Ain, Auvergne-Rhône-Alpes",
            "country": "France",
            "latitude": 45.9928,
            "longitude": 4.8231,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1925-05-31",
            "approving_authority": "Pope Pius XI (Canonization) / Pope Benedict XVI (Year for Priests 2009)",
            "confidence": "confirmed",
            "confidence_note_en": "Canonized by Pope Pius XI in 1925 and declared Patron Saint of all Parish Priests worldwide in 1929; body exhumed in 1904 and found completely incorrupt.",
            "confidence_note_vi": "Được Đức Giáo hoàng Piô XI tuyên thánh năm 1925 và tôn phong là Bổn Mạng Các Linh Mục Chánh Xứ Toàn Cầu năm 1929; thi hài được khai quật năm 1904 hoàn toàn nguyên vẹn không hư nát."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Incorrupt Body and Incorrupt Heart of Saint John Mary Vianney",
                "relic_name_vi": "Thi Hài và Trái Tim Không Hư Nát của Thánh Gioan Maria Vianney",
                "relic_type": "incorrupt_body",
                "reliquary_location": "Glass Shrine above the Main Altar of the Basilica of Ars / Reliquary Chapel of the Heart"
            }
        ],
        "historical_summary_en": "Saint John Mary Vianney (1786–1859), known universally as the *Curé of Ars*, was a French parish priest who transformed the spiritually indifferent, post-Revolutionary farming village of Ars into a global beacon of holiness. Struggling with Latin in the seminary, Vianney's profound sanctity overcame his academic limitations, and in 1818 he was appointed pastor of Ars, famously praying: *'Lord, grant me the conversion of my parish; I am willing to suffer whatever you wish for the rest of my life.'*\n\nThrough relentless penance, nocturnal adoration before the tabernacle, and heroic charity, Vianney revitalized the faith of Ars. From 1830 onward, his fame as a confessor who could read souls drew over 100,000 pilgrims annually to the remote village. The Curé spent between 12 and 18 hours daily in the confessional, enduring physical assaults and nocturnal disturbances from the devil (*le grappin*).\n\nWhen he died on August 4, 1859, at the age of seventy-three, his body remained incorrupt and is preserved today in a magnificent bronze and glass shrine within the Basilica of Ars, standing as the patron and eternal model for the Catholic diocesan priesthood.",
        "historical_summary_vi": "Thánh Gioan Maria Vianney (1786–1859), được xưng tụng là *Cha Sở Xứ Ars*, là một linh mục chánh xứ người Pháp đã biến đổi ngôi làng nông thôn Ars khô khan nguội lạnh sau cuộc Cách mạng Pháp thành một trung tâm thánh thiện tỏa sáng khắp thế giới. Từng gặp nhiều khó khăn trong việc học tiếng Latinh ở chủng viện, lòng đạo đức sâu sắc của ngài đã vượt lên trên mọi giới hạn học vấn. Năm 1818, khi được bổ nhiệm về xứ Ars, ngài đã tha thiết cầu nguyện: *'Lạy Chúa, xin ban cho con ơn hoán cải giáo xứ của con; con sẵn sàng chịu mọi đau khổ Chúa muốn suốt đời con.'*\n\nNhờ đời sống hãm mình phạt xác liên lỉ, những đêm chầu Thánh Thể thâu đêm và tình bác ái anh dũng, Cha Vianney đã làm bừng cháy lại ngọn lửa đức tin tại Ars. Từ năm 1830, tài năng thấu suốt tâm can nơi tòa giải tội của ngài đã thu hút hơn 100.000 khách hành hương mỗi năm đổ về ngôi làng hẻo lánh. Ngài ngồi tòa giải tội từ 12 đến 18 tiếng mỗi ngày và kiên cường vượt qua những đòn tấn công quấy phá dữ dội của ma quỷ (*le grappin*).\n\nKhi ngài qua đời ngày 4 tháng 8 năm 1859 ở tuổi 73, thi hài ngài không hề hư nát và ngày nay được bảo tồn trong hòm kính cẩm thạch tại Vương Cung Thánh Đường Ars, trở thành Đấng Bảo Trợ và mẫu gương ngời sáng muôn đời cho hàng linh mục chánh xứ.",
        "scripture_reading": "Jeremiah 3:15",
        "suggested_prayer_en": "O Holy Curé of Ars, Saint John Vianney, you spent your life at the altar and in the confessional seeking the salvation of souls. Pray for all priests throughout the world; grant them zeal, purity, and pastoral charity, and teach us to love the Sacrament of Penance and the Holy Sacrifice of the Mass with all our hearts. Amen.",
        "suggested_prayer_vi": "Lạy Cha Thánh Gioan Maria Vianney, Đấng Bảo Trợ các linh mục chánh xứ, ngài đã hiến trọn cuộc đời bên bàn thờ và tòa giải tội để mưu ích cho phần rỗi các linh hồn. Xin cầu bầu cho hàng linh mục trên toàn thế giới; ban cho các ngài lòng nhiệt thành, đức khiết tịnh và đức ái mục tử, đồng thời dạy chúng con biết hết lòng yêu mến Bí Tích Giải Tội và Hy Tế Thánh Thể trọn đời. Amen.",
        "primary_sources": [
            {
                "label": "Pope Benedict XVI - Letter for the Inauguration of the Year for Priests on the 150th Anniversary of the Curé of Ars (2009)",
                "url": "https://www.vatican.va/content/benedict-xvi/en/letters/2009/documents/hf_ben-xvi_let_20090616_anno-sacerdotale.html",
                "type": "vatican"
            },
            {
                "label": "Sanctuaire du Saint Curé d'Ars Official Historical Documentation",
                "url": "https://arsnet.org/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "st_catherine_monastery_mount_sinai",
        "category": "monastic_sanctuary",
        "name_en": "Sacred Autonomous Monastery of Saint Catherine at Mount Sinai",
        "name_vi": "Tu Viện Thánh Catarina trên Núi Sinai",
        "feast_day_association": "Feast of Saint Catherine of Alexandria (November 25)",
        "location": {
            "shrine_or_basilica": "Holy Monastery of the God-trodden Mount Sinai (Saint Catherine's)",
            "city": "Saint Catherine",
            "region_or_state": "South Sinai Governorate",
            "country": "Egypt",
            "latitude": 28.5558,
            "longitude": 33.9761,
            "precision": "monastery_complex"
        },
        "canonical_status": {
            "approval_or_consecration_date": "0565-01-01",
            "approving_authority": "Emperor Justinian I / UNESCO World Heritage Designation / Holy See Recognition",
            "confidence": "confirmed",
            "confidence_note_en": "Built by Emperor Justinian I between 548 and 565 AD enclosing the traditional site of the Burning Bush; holds the oldest continuously operating Christian monastic library and the relics of Saint Catherine discovered c. 800 AD.",
            "confidence_note_vi": "Được Hoàng đế Justinian I xây dựng từ năm 548 đến 565 bao quanh Bụi Gai Bốc Cháy; bảo tồn thư viện đan viện Kitô giáo hoạt động liên tục cổ nhất thế giới và hài cốt Thánh Nữ Catarina được tìm thấy khoảng năm 800."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Holy Skull and Incorrupt Left Hand of Saint Catherine and the Living Burning Bush",
                "relic_name_vi": "Hộp Sọ và Bàn Tay Trái Thánh Catarina cùng Bụi Gai Bốc Cháy Đang Sống",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Marble Shrine beside the High Altar of the Transfiguration Basilica and the Bush Enclosure"
            }
        ],
        "historical_summary_en": "The Monastery of Saint Catherine at the foot of Mount Horeb (Mount Sinai) in the Sinai Peninsula is the oldest continuously inhabited Christian monastery in the world. Founded around 330 AD by Empress Saint Helena, who constructed a small chapel at the site of the Burning Bush (*Exodus 3:2*), the complex was transformed by Byzantine Emperor Justinian I between 548 and 565 AD into a fortified fortress-monastery to protect the hermit monks from nomadic raiders.\n\nAround 800 AD, the uncorrupted relics of Saint Catherine of Alexandria—the 4th-century virgin-martyr and philosopher whose body was transported by angels to the peak of Mount Sinai after her beheading—were discovered by the monks. The monastery was rededicated to her honor and became one of the foremost pilgrimage centers of the Christian East and West.\n\nThe monastery preserves an incomparable collection of early Christian art, including the 6th-century encaustic icon of *Christ Pantocrator*, the world's second-largest collection of ancient codices and manuscripts after the Vatican Library, and the living descendant of the biblical Burning Bush (*Rubus sanctus*).",
        "historical_summary_vi": "Tu viện Thánh Catarina dưới chân Núi Horeb (Núi Sinai) trên bán đảo Sinai là tu viện Kitô giáo hoạt động liên tục cổ nhất trên thế giới. Được Thánh Nữ Hoàng hậu Helena khởi dựng vào khoảng năm 330 với một nguyện đường nhỏ tại vị trí Bụi Gai Bốc Cháy (*Xuất Hành 3:2*), toàn bộ quần thể đã được Hoàng đế Byzantine Justinian I xây dựng kiên cố từ năm 548 đến 565 thành một pháo đài đan viện bất khả xâm phạm bảo vệ các đan sĩ ẩn tu.\n\nKhoảng năm 800, các đan sĩ đã tìm thấy thi hài nguyên vẹn của Thánh Nữ Catarina thành Alexandria—vị thánh trinh nữ tử đạo thế kỷ thứ 4 mà thi thể tương truyền được các thiên thần đưa lên đỉnh núi Sinai sau khi chịu trảm quyết. Tu viện được đổi tên theo ngài và trở thành một trong những điểm hành hương linh thiêng bậc nhất của Kitô giáo Đông - Tây.\n\nTu viện lưu giữ bộ sưu tập nghệ thuật Kitô giáo cổ đại vô giá gồm linh ảnh *Chúa Kitô Đấng Cứu Thế* thế kỷ thứ 6, kho tàng thủ bản cổ xưa lớn thứ hai thế giới chỉ sau Thư viện Vatican, và bụi gai thần bí (*Rubus sanctus*) vẫn tươi tốt xanh tươi qua ngàn năm.",
        "scripture_reading": "Exodus 3:2-5",
        "suggested_prayer_en": "O God, who gave the Law to Moses on the holy mountain of Sinai and miraculously preserved the relics of your virgin martyr Saint Catherine, remove from our eyes the dust of worldly distractions. Grant that we may approach your holy presence with reverence and stand in the unquenchable fire of your divine love. Amen.",
        "suggested_prayer_vi": "Lạy Thiên Chúa, Đấng đã ban Luật cho Môsê trên đỉnh núi thánh Sinai và gìn giữ di cốt Thánh Nữ Tử Đạo Catarina một cách kỳ diệu, xin gạt bỏ khỏi mắt chúng con những phù phiếm thế gian. Xin cho chúng con biết tiến lại gần nhan thánh Chúa với lòng tôn kính sâu xa và được bừng cháy trong ngọn lửa tình yêu bất diệt của Chúa. Amen.",
        "primary_sources": [
            {
                "label": "Holy Monastery of Sinai Official Historical and Manuscript Archives",
                "url": "https://www.sinaimonastery.com/",
                "type": "academic"
            },
            {
                "label": "Pope John Paul II - Homily during Mount Sinai Pilgrimage (February 26, 2000)",
                "url": "https://www.vatican.va/content/john-paul-ii/en/homilies/2000/documents/hf_jp-ii_hom_20000226_sinai.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "mar_saba_monastery_judean_desert",
        "category": "monastic_sanctuary",
        "name_en": "The Great Lavra of Saint Sabas (Mar Saba Monastery)",
        "name_vi": "Đại Đan Viện Thánh Sabas (Tu Viện Mar Saba)",
        "feast_day_association": "Feast of Saint Sabas the Sanctified (December 5) / Saint John Damascene (December 4)",
        "location": {
            "shrine_or_basilica": "Holy Lavra of Saint Sabbas the Sanctified (Mar Saba)",
            "city": "Kidron Valley (near Bethlehem)",
            "region_or_state": "Judean Desert (West Bank)",
            "country": "Palestine",
            "latitude": 31.7050,
            "longitude": 35.3314,
            "precision": "monastery_complex"
        },
        "canonical_status": {
            "approval_or_consecration_date": "0483-01-01",
            "approving_authority": "Patriarch Sallustius of Jerusalem (486 AD) / Pope Paul VI (Relic Return 1965)",
            "confidence": "confirmed",
            "confidence_note_en": "Founded in 483 AD by Saint Sabas the Sanctified; home of Doctor of the Church Saint John of Damascus (8th c.); intact incorrupt body of Saint Sabas returned from Venice to Mar Saba by Pope Paul VI in 1965.",
            "confidence_note_vi": "Được Thánh Sabas thành lập năm 483; là nơi tu trì và sáng tác của Tiến Sĩ Hội Thánh Gioan Đamasquinô (thế kỷ 8); thi hài nguyên vẹn của Thánh Sabas được Đức Giáo hoàng Phaolô VI trao trả từ Venice về lại Mar Saba năm 1965."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Incorrupt Body of Saint Sabas and the Tomb of Saint John Damascene",
                "relic_name_vi": "Thi Hài Nguyên Vẹn của Thánh Sabas và Lăng Mộ Thánh Gioan Đamasquinô",
                "relic_type": "incorrupt_body",
                "reliquary_location": "Glass Shrine inside the Church of the Theotokos and the Rock Cave of Saint John Damascene"
            }
        ],
        "historical_summary_en": "Perched dramatically upon the sheer rock cliffs of the Kidron Gorge in the barren Judean Desert between Bethlehem and the Dead Sea, Mar Saba (The Great Lavra of Saint Sabas) is one of the oldest continuously inhabited monasteries in the world. Founded in 483 AD by Saint Sabas the Sanctified (439–532), a Cappadocian monk guided by divine vision to a cliffside cave, the lavra grew to house hundreds of desert hermits following a strict rule of silence, fasting, and nocturnal psalmody.\n\nIn the 8th century, Saint John of Damascus (John Damascene, c. 676–749), Doctor of the Church and last of the Greek Fathers, retired to Mar Saba. In his solitary cliff cell, he composed the monumental *Fount of Knowledge* (*De Fide Orthodoxa*), defended the veneration of holy icons against Byzantine iconoclasm, and composed some of Eastern Christianity's most sublime liturgical hymns and the *Octoechos*.\n\nDuring the Crusades, the incorrupt body of Saint Sabas was taken to Venice for safekeeping; in October 1965, following the historic meeting between Pope Paul VI and Patriarch Athenagoras I, Pope Paul VI returned the holy body to Mar Saba in a solemn gesture of ecumenical brotherhood, where it rests intact today.",
        "historical_summary_vi": "Tọa lạc ngoạn mục trên vách đá dựng đứng của thung lũng Kidron giữa sa mạc Judea khô cằn nối Bethlehem và Biển Chết, Mar Saba (Đại Đan Viện Thánh Sabas) là một trong những tu viện cổ kính nhất thế giới còn duy trì đời sống đan tu liên tục. Được Thánh Sabas (439–532), một đan sĩ xứ Cappadocia thành lập năm 483 sau khi nhận thị kiến dẫn lối vào hang đá sa mạc, đan viện nhanh chóng quy tụ hàng trăm ẩn sĩ sống đời thinh lặng, chay tịnh nghiêm ngặt và tụng niệm thánh vịnh thâu đêm.\n\nVào thế kỷ thứ 8, Thánh Gioan Đamasquinô (khoảng 676–749), Tiến Sĩ Hội Thánh và là vị Giáo phụ Hy Lạp cuối cùng, đã lui về ẩn tu tại Mar Saba. Trong hang đá tĩnh mịch, ngài đã viết kiệt tác *Nguồn Mạch Tri Thức* (*De Fide Orthodoxa*), can trường bảo vệ sự tôn kính các Linh Ảnh thánh chống lại phái phá hủy ảnh tượng và sáng tác những bài thánh ca phụng vụ Đông Phương tuyệt mỹ.\n\nTrong thời Thập Tự Chinh, thi hài nguyên vẹn của Thánh Sabas được đưa về Venice cất giữ; đến tháng 10 năm 1965, sau cuộc gặp gỡ lịch sử giữa Đức Giáo hoàng Phaolô VI và Thượng Phụ Athenagoras I, Đức Phaolô VI đã long trọng trao trả thi hài Thánh Sabas về lại tu viện Mar Saba trong tinh thần huynh đệ đại kết, nơi ngài an nghỉ trọn vẹn cho đến ngày nay.",
        "scripture_reading": "Isaiah 35:1-2",
        "suggested_prayer_en": "O Lord God of the Desert, who made the barren wilderness of Judea blossom with the holy asceticism of Saint Sabas and the sublime wisdom of Saint John Damascene, deliver us from the distractions of the world. Grant us silence of heart, steadfast courage in defending Catholic truth, and a burning desire for contemplation. Amen.",
        "suggested_prayer_vi": "Lạy Thiên Chúa của miền Sa Mạc, Đấng đã làm cho vùng sa mạc hoang vu Judea trổ sinh hoa trái thánh thiện nhờ đời sống khổ chế của Thánh Sabas và sự khôn ngoan siêu việt của Thánh Gioan Đamasquinô, xin giải thoát chúng con khỏi những xao động thế trần. Xin ban cho tâm hồn chúng con sự thinh lặng thánh thiện, lòng can đảm bảo vệ chân lý đức tin và lòng khao khát chiêm niệm nhan Chúa muôn đời. Amen.",
        "primary_sources": [
            {
                "label": "Greek Orthodox Patriarchate of Jerusalem - Holy Lavra of Saint Sabas Records",
                "url": "https://jerusalem-patriarchate.info/",
                "type": "academic"
            },
            {
                "label": "Pope Benedict XVI - General Audience on Saint John Damascene (May 6, 2009)",
                "url": "https://www.vatican.va/content/benedict-xvi/en/audiences/2009/documents/hf_ben-xvi_aud_20090506.html",
                "type": "vatican"
            }
        ]
    }
]

def main():
    target_dir = "Anno/Resources/SacredSanctuaries"
    os.makedirs(target_dir, exist_ok=True)
    
    for item in BATCH_5 + BATCH_6:
        filename = f"{item['sanctuary_id']}.json"
        path = os.path.join(target_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False, indent=2)
        print(f"Generated {filename}")

if __name__ == "__main__":
    main()

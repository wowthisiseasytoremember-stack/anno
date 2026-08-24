#!/usr/bin/env python3
"""
generate_batch_8.py
Generates Batch 8 (Asian Martyrs, The Americas & Regional Shrines)
12 rich, high-craft, fully documented sanctuaries with authentic Vietnamese Catholic terminology.
"""

import json
import os

BATCH_8 = [
    {
        "sanctuary_id": "phat_diem_cathedral_ninh_binh",
        "category": "martyr_shrine",
        "name_en": "Phát Diệm Stone Cathedral Complex",
        "name_vi": "Quần Thể Nhà Thờ Đá Phát Diệm",
        "feast_day_association": "Feast of the Holy Vietnamese Martyrs (November 24) / Our Lady of the Rosary (October 7)",
        "location": {
            "shrine_or_basilica": "Nhà thờ Chính tòa Phát Diệm (Quần thể Nhà thờ Đá)",
            "city": "Kim Sơn",
            "region_or_state": "Ninh Bình",
            "country": "Vietnam",
            "latitude": 20.0928,
            "longitude": 106.0797,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1899-12-01",
            "approving_authority": "Father Peter Trần Lục (Cụ Sáu) / Bishop Alexandre Marcou / Diocese of Phát Diệm",
            "confidence": "confirmed",
            "confidence_note_en": "Constructed between 1875 and 1899 by the legendary priest Fr. Peter Trần Lục (Cụ Sáu); hailed as a peerless architectural synthesis of Vietnamese pagoda temple architecture and Catholic basilica cosmology.",
            "confidence_note_vi": "Được Cha Phêrô Trần Lục (Cụ Sáu) chủ trì xây dựng từ năm 1875 đến 1899; được tôn vinh là kiệt tác kiến trúc độc nhất vô nhị kết hợp hài hòa văn hóa đình chùa Á Đông và thần học Công giáo."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Whole Monolithic Stone Chapel of the Immaculate Heart of Mary and Tomb of Father Trần Lục",
                "relic_name_vi": "Nguyện Đường Đá Trái Tim Đức Mẹ Nguyên Khối và Lăng Mộ Cụ Sáu Trần Lục",
                "relic_type": "1st_class_tomb",
                "reliquary_location": "Stone Chapel (Nhà Thờ Trái Tim Đức Mẹ) and Forecourt of Phương Đình"
            }
        ],
        "historical_summary_en": "The Phát Diệm Cathedral complex in Kim Sơn, Ninh Bình, constructed between 1875 and 1899 under the leadership of Father Peter Trần Lục (popularly known as *Cụ Sáu*), stands as one of the most culturally profound Christian monuments in Asia. Built entirely of natural ironwood (*gỗ sắt*), massive stone blocks, and terracotta tiles, the complex synthesizes traditional Vietnamese imperial palace and pagoda architecture with Catholic liturgical theology.\n\nThe complex includes the grand cathedral (*Nhà Thờ Lớn*), five distinct chapels, three artificial grottoes, a bell tower pavilion (*Phương Đình*), and a monumental pond featuring a central statue of Christ the King. The most extraordinary building is the Chapel of the Immaculate Heart of Mary (*Nhà Thờ Đá*), sculpted entirely out of monolithic white limestone blocks from the pillars, walls, and altar to the window grates.\n\nPhát Diệm emerged as the spiritual fortress of Catholicism in North Vietnam, producing hundreds of martyrs and serving as a testament to the inculturation of Christian faith in Vietnamese soil.",
        "historical_summary_vi": "Quần thể Nhà thờ Chính tòa Phát Diệm tại huyện Kim Sơn, tỉnh Ninh Bình, được Cha Phêrô Trần Lục (Cụ Sáu) chủ trì xây dựng từ năm 1875 đến 1899, là một trong những công trình kiến trúc Kitô giáo độc đáo bậc nhất Châu Á. Được dựng hoàn toàn bằng gỗ lim nguyên khối, đá xanh tự nhiên và ngói mũi hài, công trình là sự kết hợp tuyệt mỹ giữa kiến trúc cung đình đình chùa truyền thống Việt Nam và thần học phụng vụ Công giáo.\n\nQuần thể gồm Nhà Thờ Lớn nguy nga, 5 nhà nguyện độc lập, 3 hang đá nhân tạo, tháp chuông Phương Đình bề thế và hồ nước trung tâm có tượng Chúa Kitô Vua. Nổi bật nhất là Nhà Thờ Trái Tim Đức Mẹ (thường gọi là Nhà Thờ Đá) được tạc hoàn toàn bằng đá xanh nguyên khối từ cột, kèo, tường, bàn thờ cho đến chấn song cửa sổ.\n\nPhát Diệm từng là cái nôi đức tin vững chắc của miền Bắc, nơi sản sinh nhiều vị anh hùng tử đạo và là biểu tượng vĩ đại của sự hội nhập văn hóa Công giáo vào lòng dân tộc Việt Nam.",
        "scripture_reading": "1 Peter 2:4-5",
        "suggested_prayer_en": "O Almighty God, who inspired Father Peter Trần Lục and the faithful of Phát Diệm to build a house of prayer in living stone and native craft, strengthen the Church in Vietnam. Grant that our hearts may be living stones built into a spiritual temple of faith, charity, and steadfast witness. Amen.",
        "suggested_prayer_vi": "Lạy Thiên Chúa Toàn Năng, Đấng đã soi sáng cho Cha Cụ Sáu và các tiền nhân xây dựng Đền Thánh Phát Diệm bằng đá vững bền và tinh hoa văn hóa dân tộc, xin nâng đỡ Giáo hội Việt Nam. Xin biến đổi tâm hồn chúng con thành những viên đá sống động xây nên ngôi đền thờ thiêng liêng của đức tin, lòng bác ái và sự trung kiên làm chứng cho Chúa muôn đời. Amen.",
        "primary_sources": [
            {
                "label": "Diocese of Phát Diệm Official Historical and Architectural Archives",
                "url": "https://phatdiem.org/",
                "type": "academic"
            },
            {
                "label": "Missions Étrangères de Paris (MEP) - Historical Dossier on Father Trần Lục and Phát Diệm",
                "url": "https://irfa.paris/en/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "phu_nhai_basilica_nam_dinh",
        "category": "marian_apparition",
        "name_en": "Minor Basilica of Our Lady of the Immaculate Conception (Phú Nhai)",
        "name_vi": "Vương Cung Thánh Đường Đức Mẹ Vô Nhiễm Nguyên Tội Phú Nhai",
        "feast_day_association": "Solemnity of the Immaculate Conception (December 8)",
        "location": {
            "shrine_or_basilica": "Vương Cung Thánh Đường Đức Mẹ Phú Nhai",
            "city": "Xuân Trường",
            "region_or_state": "Nam Định",
            "country": "Vietnam",
            "latitude": 20.3017,
            "longitude": 106.3350,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "2008-12-23",
            "approving_authority": "Pope Benedict XVI (Decree of Minor Basilica) / Bishop Joseph Hoàng Văn Tiệm",
            "confidence": "confirmed",
            "confidence_note_en": "First church built in 1866; present monumental French Gothic basilica completed in 1933; elevated to Minor Basilica by Pope Benedict XVI on December 23, 2008.",
            "confidence_note_vi": "Ngôi thánh đường đầu tiên dựng năm 1866; thánh đường Gothic Pháp nguy nga hiện nay hoàn tất năm 1933; được Đức Giáo hoàng Biển Đức XVI nâng lên hàng Tiểu Vương Cung Thánh Đường ngày 23 tháng 12 năm 2008."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Relics of the Dominican Martyrs of Tonkin and the Miraculous Statue of the Immaculate Conception",
                "relic_name_vi": "Hài Cốt Các Thánh Tử Đạo Dòng Đaminh Xứ Bắc và Tượng Đức Mẹ Vô Nhiễm Phép Lạ",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Side Altar of the Holy Martyrs and Central Retablo of Phú Nhai Basilica"
            }
        ],
        "historical_summary_en": "The Minor Basilica of Our Lady of the Immaculate Conception at Phú Nhai, located in Xuân Trường district, Nam Định province, is one of the largest and most majestic Gothic Catholic churches in Southeast Asia. The Catholic roots of Phú Nhai trace back to the early Dominican evangelization of Tonkin in the 18th century, enduring severe persecutions under Kings Minh Mạng and Tự Đức.\n\nIn 1866, immediately after the cessation of religious persecution, Spanish Dominican Bishop Emmanuel Riaño constructed a parish church dedicated to the Immaculate Conception. The present monumental French Gothic basilica, featuring twin bell towers rising forty-four meters and a nave spanning eighty meters in length, was constructed by Spanish friars and completed in 1933.\n\nOn December 23, 2008, Pope Benedict XVI signed the papal decree elevating the sanctuary of Phú Nhai to the status of a Minor Basilica. It stands as the pilgrimage epicenter of the Diocese of Bùi Chu, enshrining the heroic memory of thousands of local martyrs who laid down their lives for Christ.",
        "historical_summary_vi": "Vương Cung Thánh Đường Đức Mẹ Vô Nhiễm Nguyên Tội Phú Nhai, tọa lạc tại huyện Xuân Trường, tỉnh Nam Định, là một trong những thánh đường phong cách Gothic lớn và tráng lệ nhất Đông Nam Á. Cội nguồn đức tin của Phú Nhai gắn liền với công cuộc truyền giáo của các thừa sai Dòng Đaminh Tây Ban Nha từ thế kỷ 18, từng trải qua những cơn bách hại khốc liệt dưới triều vua Minh Mạng và Tự Đức.\n\nNăm 1866, sau khi sắc chỉ tự do tôn giáo được ban hành, Đức Giám mục Emmanuel Riaño đã cho khởi công xây dựng ngôi thánh đường kính Đức Mẹ Vô Nhiễm. Công trình đại thánh đường Gothic hiện nay với hai tháp chuông cao 44 mét và lòng nhà thờ dài 80 mét được hoàn thành năm 1933.\n\nNgày 23 tháng 12 năm 2008, Đức Thánh Cha Biển Đức XVI đã ban Tông sắc nâng Đền Thánh Phú Nhai lên hàng Tiểu Vương Cung Thánh Đường. Nơi đây là trung tâm hành hương lớn của Giáo phận Bùi Chu, ghi dấu muôn vàn tấm gương tử đạo anh dũng của các bậc tiền nhân.",
        "scripture_reading": "Luke 1:28",
        "suggested_prayer_en": "O Queen of Phú Nhai, Mother Conceived Without Original Sin, you accompanied our ancestors through the storms of persecution and martyrdom. Preserve the Catholic faith in our land, protect all Christian families in unity and holiness, and lead us safely to the eternal joy of Heaven. Amen.",
        "suggested_prayer_vi": "Lạy Đức Mẹ Phú Nhai, Mẹ Vô Nhiễm Nguyên Tội, Mẹ đã đồng hành cùng tổ tiên chúng con qua bao giông bão của các cuộc bách hại tử đạo. Xin Mẹ gìn giữ đức tin Công giáo trên quê hương đất nước, bảo vệ các gia đình trong sự hiệp nhất thánh thiện và dẫn đưa chúng con về hưởng niềm vui vĩnh cửu trên Quê Trời. Amen.",
        "primary_sources": [
            {
                "label": "Diocese of Bùi Chu - Official History and Papal Decree of Phú Nhai Basilica",
                "url": "https://gpbuichu.org/",
                "type": "academic"
            },
            {
                "label": "Vatican Congregation for Divine Worship - Decree of Minor Basilica for Phú Nhai (2008)",
                "url": "https://www.vatican.va/content/vatican/en.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "fr_truong_buu_diep_tac_say",
        "category": "martyr_shrine",
        "name_en": "Shrine of Father Francis Xavier Trương Bửu Diệp (Tắc Sậy)",
        "name_vi": "Trung Tâm Hành Hương Cha Phanxicô Xaviê Trương Bửu Diệp (Tắc Sậy)",
        "feast_day_association": "Anniversary of Martyrdom of Fr. Trương Bửu Diệp (March 12)",
        "location": {
            "shrine_or_basilica": "Trung tâm Hành hương Tắc Sậy (Nhà thờ Tắc Sậy)",
            "city": "Giá Rai (Tân Phong)",
            "region_or_state": "Bạc Liêu / Cà Mau",
            "country": "Vietnam",
            "latitude": 9.2319,
            "longitude": 105.3214,
            "precision": "tomb"
        },
        "canonical_status": {
            "approval_or_consecration_date": "2014-10-31",
            "approving_authority": "Congregation for the Causes of Saints (Nihil Obstat) / Bishop Paul Bùi Văn Đọc",
            "confidence": "confirmed",
            "confidence_note_en": "Servant of God; official Cause of Canonization opened on October 31, 2014 with Vatican *Nihil Obstat*; universal pilgrimage center in the Mekong Delta venerated by Catholics and non-Catholics alike.",
            "confidence_note_vi": "Đấng Đáng Kính Tôi Tớ Chúa; Tiến trình Phong Thánh được Tòa Thánh phê chuẩn sắc lệnh *Nihil Obstat* ngày 31 tháng 10 năm 2014; trung tâm hành hương lớn nhất miền Tây Nam Bộ thu hút hàng triệu tín hữu và người ngoài Công giáo."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Sacred Tomb and Relics of Servant of God Father Francis Xavier Trương Bửu Diệp",
                "relic_name_vi": "Lăng Mộ và Di Hài Cha Tôi Tớ Chúa Phanxicô Xaviê Trương Bửu Diệp",
                "relic_type": "1st_class_tomb",
                "reliquary_location": "Mausoleum of Father Diệp at Tắc Sậy Pilgrimage Center"
            }
        ],
        "historical_summary_en": "Father Francis Xavier Trương Bửu Diệp (1897–1946) was a Vietnamese Catholic diocesan priest who served as pastor of Tắc Sậy parish in Bạc Liêu in the Mekong Delta. Ordained in 1924, Father Diệp was renowned for his profound humility, tireless pastoral charity, and selfless care for the impoverished peasants of the delta.\n\nIn March 1946, during the chaotic turmoil of the First Indochina War, militant forces arrested Father Diệp along with approximately seventy Catholic parishioners, confining them in an agricultural warehouse. When his captors threatened to execute the entire flock, Father Diệp heroically offered his own life in exchange for the release of his parishioners, declaring: *'I will not flee; as the shepherd, I must stay to live and die with my sheep.'*\n\nOn the night of March 12, 1946, Father Diệp was stripped, tortured, and martyred, his body cast into a pond with three fatal machete wounds to the back of his neck. All seventy parishioners were spared and released. His tomb at Tắc Sậy has become the most visited pilgrimage sanctuary in the Mekong Delta, renowned for extraordinary graces, healings, and reconciliation.",
        "historical_summary_vi": "Cha Phanxicô Xaviê Trương Bửu Diệp (1897–1946) là linh mục giáo phận Cần Thơ, chánh xứ họ đạo Tắc Sậy thuộc tỉnh Bạc Liêu vùng đồng bằng sông Cửu Long. Thụ phong linh mục năm 1924, ngài nổi tiếng với đời sống khiêm nhường thánh thiện, hết lòng chăm lo cho người nghèo khó và các gia đình bần nông trong xứ đạo.\n\nVào tháng 3 năm 1946, giữa bối cảnh chiến tranh loạn lạc, một nhóm vũ trang đã ập vào bắt giữ Cha Diệp cùng khoảng 70 giáo dân giam trong một lẫm lúa. Khi quân lính đe dọa sát hại toàn bộ con chiên, Cha Diệp đã anh dũng tình nguyện nộp mạng để đổi lấy tự do cho đoàn chiên, khảng khái nói: *'Tôi sống giữa đoàn chiên, và nếu có chết cũng chết giữa đoàn chiên, tôi không đi đâu cả.'*\n\nĐêm ngày 12 tháng 3 năm 1946, Cha Diệp đã chịu tra tấn dã man và tử đạo, thi thể bị chém ba nhát chém sau gáy và vứt xuống ao. Toàn bộ 70 giáo dân được tha mạng trở về bình an. Lăng mộ Cha tại Tắc Sậy ngày nay trở thành trung tâm hành hương linh thiêng bậc nhất Tây Nam Bộ, thu hút hàng triệu lượt người thuộc mọi tôn giáo đến xin ơn và tạ ơn.",
        "scripture_reading": "John 10:11-15",
        "suggested_prayer_en": "Lord Jesus Christ, the Good Shepherd who laid down your life for the sheep, we thank you for the heroic pastoral sacrifice of your Servant Father Francis Xavier Trương Bửu Diệp. Through his intercession, grant healing to the sick, comfort to the afflicted, and raise him to the honors of the altar. Amen.",
        "suggested_prayer_vi": "Lạy Chúa Giêsu Kitô, Mục Tử Nhân Lành đã thí mạng sống vì đàn chiên, chúng con cảm tạ Chúa đã ban cho chúng con mẫu gương mục tử anh dũng của Cha Tôi Tớ Chúa Phanxicô Xaviê Trương Bửu Diệp. Nhờ lời chuyển cầu của ngài, xin Chúa ban ơn chữa lành cho các bệnh nhân, an ủi kẻ khốn cùng và sớm cho ngài được tôn phong lên bậc Hiển Thánh. Amen.",
        "primary_sources": [
            {
                "label": "Diocese of Cần Thơ - Official Canonization Process Documentation for Servant of God Fr. Trương Bửu Diệp",
                "url": "https://gpcantho.com/",
                "type": "academic"
            },
            {
                "label": "Congregation for the Causes of Saints - Vatican Decree Nihil Obstat for Fr. Trương Bửu Diệp (October 31, 2014)",
                "url": "https://www.vatican.va/content/vatican/en.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "ba_giong_martyrs_shrine",
        "category": "martyr_shrine",
        "name_en": "National Shrine of the Vietnamese Martyrs at Ba Giồng",
        "name_vi": "Trung Tâm Hành Hương Các Thánh Tử Đạo Ba Giồng",
        "feast_day_association": "Feast of Saint Peter Nguyễn Văn Lựu and the Ba Giồng Martyrs (April 7 / November 24)",
        "location": {
            "shrine_or_basilica": "Trung tâm Hành hương Ba Giồng",
            "city": "Chợ Gạo",
            "region_or_state": "Tiền Giang",
            "country": "Vietnam",
            "latitude": 10.4206,
            "longitude": 106.3986,
            "precision": "tomb"
        },
        "canonical_status": {
            "approval_or_consecration_date": "2004-06-01",
            "approving_authority": "Bishop Paul Bùi Văn Đọc / Diocese of Mỹ Tho",
            "confidence": "confirmed",
            "confidence_note_en": "Site of execution of Saint Peter Nguyễn Văn Lựu and thousands of Catholic martyrs between 1859 and 1862 under Emperor Tự Đức; designated Diocesan Pilgrimage Center for the Vietnamese Martyrs by Bishop Paul Bùi Văn Đọc in 2004.",
            "confidence_note_vi": "Nơi pháp trường xử trảm Thánh Linh mục Phêrô Nguyễn Văn Lựu và hàng ngàn giáo dân tử đạo thời vua Tự Đức (1859-1862); được Đức Giám mục Phaolô Bùi Văn Đọc thiết lập thành Trung Tâm Hành Hương Các Thánh Tử Đạo năm 2004."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Bone Relics of Saint Peter Nguyễn Văn Lựu and the Martyred Faithful of Ba Giồng",
                "relic_name_vi": "Hài Cốt Thánh Phêrô Nguyễn Văn Lựu và Hài Cốt Hàng Ngàn Đấng Tử Đạo Ba Giồng",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Martyrs' Ossuary and Altar at Ba Giồng Pilgrimage Center"
            }
        ],
        "historical_summary_en": "Ba Giồng, located in Chợ Gạo district, Tiền Giang province, is one of the most venerated sites of martyrdom in southern Vietnam. Established as a Christian settlement in 1702, Ba Giồng became the epicenter of intense anti-Catholic persecution during the reign of Emperor Tự Đức under the *Phân Sáp* (Dispersion) Edicts between 1859 and 1862.\n\nOn April 7, 1861, Father Peter Nguyễn Văn Lựu, pastor of Ba Giồng, was beheaded at the local execution ground after refusing to trample upon the crucifix, uttering his immortal confession: *'I will not step on the Cross; I prefer to die for the Lord.'* Canonized by Pope John Paul II in 1988, Saint Peter Lựu was martyred alongside dozens of local catechists.\n\nDuring the brutal enforcement of the Dispersion Edict in 1862, several thousand Catholic men, women, and children from surrounding villages were rounded up, tied together, and buried alive or burned in large pits across Ba Giồng. In 2004, Bishop Paul Bùi Văn Đọc established the modern pilgrimage center and ossuary memorial, honoring the steadfast fidelity of these southern Vietnamese witnesses of the faith.",
        "historical_summary_vi": "Ba Giồng, tọa lạc tại huyện Chợ Gạo, tỉnh Tiền Giang, là một trong những thánh địa tử đạo linh thiêng bậc nhất miền Nam Việt Nam. Được hình thành từ năm 1702, giáo xứ Ba Giồng đã trở thành tâm điểm của những cuộc bách hại đạo tàn khốc dưới thời vua Tự Đức qua các sắc lệnh Phân Sáp (1859–1862).\n\nNgày 7 tháng 4 năm 1861, Cha sở Phêrô Nguyễn Văn Lựu đã anh dũng chịu trảm quyết tại pháp trường Ba Giồng sau khi kiên quyết từ chối đạp lên Thánh Giá, để lại lời tuyên xưng bất hủ: *'Đạo đã thấm nhập trong xương tủy tôi, làm sao tôi bỏ được. Thà tôi chịu chết chứ không bao giờ khóa quá.'* Ngài được Thánh Giáo hoàng Gioan Phaolô II tuyên thánh năm 1988.\n\nTrong đợt thi hành lệnh Phân Sáp năm 1862, hàng ngàn giáo dân Ba Giồng gồm cả người già, phụ nữ và trẻ em đã bị trói chùm vùi sống hoặc thiêu sống dưới các hố chôn tập thể vì kiên trung giữ đạo. Năm 2004, Đức Giám mục Phaolô Bùi Văn Đọc đã khánh thành Trung tâm Hành hương và nhà hài cốt lưu giữ di cốt các đấng tử đạo anh hùng.",
        "scripture_reading": "Matthew 10:32-33",
        "suggested_prayer_en": "O Holy Vietnamese Martyrs of Ba Giồng, especially Saint Peter Nguyễn Văn Lựu, who shed your blood on this soil rather than deny the Cross of Christ, pray for our families. Grant us an unshakeable faith, courageous charity, and the grace to remain faithful disciples of Jesus until our last breath. Amen.",
        "suggested_prayer_vi": "Lạy Các Thánh Tử Đạo Việt Nam tại Ba Giồng, đặc biệt là Thánh Linh mục Phêrô Nguyễn Văn Lựu, các ngài đã đổ máu đào trên mảnh đất này thà chịu chết chứ không chối bỏ Thánh Giá Chúa Kitô, xin cầu bầu cho gia đình chúng con. Xin ban cho chúng con một đức tin kiên trung, lòng mến sắt son và ơn bền đỗ theo chân Chúa Giêsu đến hơi thở cuối cùng. Amen.",
        "primary_sources": [
            {
                "label": "Diocese of Mỹ Tho - Official Historical Dossier of Ba Giồng Martyrs Sanctuary",
                "url": "https://giaophanmytho.net/",
                "type": "academic"
            },
            {
                "label": "Pope John Paul II - Apostolic Constitution Canonizing 117 Vietnamese Martyrs (June 19, 1988)",
                "url": "https://www.vatican.va/content/john-paul-ii/la/apost_constitutions/documents/hf_jp-ii_apc_19880619_vietnam.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "chonjinam_and_mirinae_korea",
        "category": "martyr_shrine",
        "name_en": "Chonjinam and Mirinae Holy Sites (Cradle of Korean Catholicism)",
        "name_vi": "Thánh Địa Chonjinam và Mirinae (Cái Nôi Công Giáo Hàn Quốc)",
        "feast_day_association": "Feast of Saint Andrew Kim Taegon, Paul Chong Hasang and Companions (September 20)",
        "location": {
            "shrine_or_basilica": "Chonjinam Shrine & Mirinae Holy Ground",
            "city": "Gwangju & Anseong",
            "region_or_state": "Gyeonggi-do",
            "country": "South Korea",
            "latitude": 37.1103,
            "longitude": 127.3517,
            "precision": "tomb"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1984-05-06",
            "approving_authority": "Pope John Paul II (Canonization of 103 Korean Martyrs in Seoul)",
            "confidence": "confirmed",
            "confidence_note_en": "Unique in global church history as a church founded by lay scholars studying Catholic books in 1779 at Chonjinam Hermitage; Saint Andrew Kim Taegon (first Korean priest, martyred 1846) buried at Mirinae; 103 Martyrs canonized by Pope John Paul II in 1984.",
            "confidence_note_vi": "Hiện tượng độc nhất vô nhị trong lịch sử Giáo hội khi đức tin được khởi xướng bởi các học giả giáo dân tự nghiên cứu sách báo năm 1779 tại Chonjinam; Thánh Anrê Kim Taegon (linh mục tiên khởi, tử đạo 1846) an nghỉ tại Mirinae; 103 Thánh Tử Đạo được Đức Gioan Phaolô II tuyên thánh năm 1984."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Tomb and Sacred Relics of Saint Andrew Kim Taegon and the Five Lay Founders of Korean Catholicism",
                "relic_name_vi": "Lăng Mộ Hài Cốt Thánh Anrê Kim Taegon và Năm Vị Tiền Bối Giáo Dân Sáng Lập",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Tomb Chapel at Mirinae Shrine and Founders' Hill at Chonjinam"
            }
        ],
        "historical_summary_en": "The foundation of the Catholic Church in Korea is unique in global ecclesiastical history: it was established not by foreign missionaries, but by native Korean lay intellectuals (*Silhak* scholars) who studied Catholic theological books imported from Beijing. In the winter of 1779, at the remote mountain hermitage of Chonjinam in Gwangju, scholars Yi Byeok, Yi Seung-hun, and Jeong Yak-jong gathered for a historic theological conference, embracing the Gospel and establishing the first Korean Catholic community.\n\nDecades of savage state persecutions followed (1801, 1839, 1846, 1866), during which over 10,000 Korean believers laid down their lives. Among them was Saint Andrew Kim Taegon (1821–1846), the first native Korean priest, who was beheaded at Saenamteo near Seoul on September 16, 1846, at age twenty-five. His disciples smuggled his body to the hidden mountain village of Mirinae ('Milky Way') in Anseong, where his tomb became a sanctuary of solace.\n\nOn May 6, 1984, during the bicentennial of the Korean Church, Pope John Paul II canonized 103 Korean Martyrs in Seoul—the first canonization outside Rome in modern times—cementing Chonjinam and Mirinae as the eternal symbols of lay initiative and martyr fidelity.",
        "historical_summary_vi": "Sự ra đời của Giáo hội Công giáo tại Hàn Quốc là một hiện tượng kỳ diệu độc nhất vô nhị: đức tin được gieo mầm không phải bởi các thừa sai ngoại quốc, mà bởi chính các học giả trí thức Nho học bản địa (*Silhak*). Mùa đông năm 1779, tại am Chonjinam hẻo lánh trên núi vùng Gwangju, các học giả Lý Bích (Yi Byeok), Lý Thừa Huân (Yi Seung-hun) và Đinh Nhược Chung (Jeong Yak-jong) đã họp bàn nghiên cứu các sách thần học Công giáo từ Bắc Kinh, đón nhận đức tin và khai sinh cộng đoàn Công giáo đầu tiên.\n\nCác cuộc bách hại tàn khốc sau đó (1801, 1839, 1846, 1866) đã cướp đi sinh mạng của hơn mười ngàn tín hữu. Nổi bật nhất là Thánh Anrê Kim Taegon (1821–1846), linh mục tiên khởi người Hàn Quốc, chịu trảm quyết tại Saenamteo gần Seoul ngày 16 tháng 9 năm 1846 khi mới 25 tuổi. Các giáo dân đã bí mật đưa thi hài ngài về an táng tại ngôi làng ẩn khuất Mirinae ('Dải Ngân Hà') tại Anseong.\n\nNgày 6 tháng 5 năm 1984, nhân kỷ niệm 200 năm Giáo hội Hàn Quốc, Thánh Giáo hoàng Gioan Phaolô II đã chủ sự Thánh Lễ tuyên thánh cho 103 Thánh Tử Đạo Hàn Quốc tại Seoul—lễ phong thánh đầu tiên ngoài thành Roma trong lịch sử hiện đại—tôn vinh Chonjinam và Mirinae thành biểu tượng bất diệt của tinh thần tông đồ giáo dân.",
        "scripture_reading": "John 12:24-26",
        "suggested_prayer_en": "O Lord, who blessed the Church in Korea with the brilliant faith of its lay founders and the blood of Saint Andrew Kim Taegon and his companion martyrs, inflame our hearts with apostolic initiative. Make us fearless heralds of the Gospel in our modern society and grant peace to the entire Korean peninsula. Amen.",
        "suggested_prayer_vi": "Lạy Chúa, Đấng đã chúc phúc cho Giáo hội Hàn Quốc qua ngọn lửa đức tin của các bậc tiền bối giáo dân và máu đào của Thánh Anrê Kim Taegon cùng các bạn tử đạo, xin thắp lên trong lòng chúng con tinh thần dấn thân tông đồ. Xin ban cho chúng con lòng can đảm loan báo Tin Mừng giữa lòng thế giới hôm nay và ban bình an hiệp nhất cho toàn thể bán đảo Triều Tiên. Amen.",
        "primary_sources": [
            {
                "label": "Catholic Bishops' Conference of Korea (CBCK) - Historical Archives of Chonjinam and Mirinae",
                "url": "https://cbck.or.kr/en",
                "type": "academic"
            },
            {
                "label": "Pope John Paul II - Homily for the Canonization of 103 Korean Martyrs in Seoul (May 6, 1984)",
                "url": "https://www.vatican.va/content/john-paul-ii/en/homilies/1984/documents/hf_jp-ii_hom_19840506_canonizzazione-corea.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "basilica_of_bom_jesus_goa",
        "category": "apostolic_tomb",
        "name_en": "Basilica of Bom Jesus (Tomb of Saint Francis Xavier)",
        "name_vi": "Đại Vương Cung Thánh Đường Bom Jesus (Lăng Mộ Thánh Phanxicô Xaviê)",
        "feast_day_association": "Feast of Saint Francis Xavier, Patron of Missions (December 3)",
        "location": {
            "shrine_or_basilica": "Basilica of Bom Jesus (Basílica do Bom Jesus)",
            "city": "Old Goa (Velha Goa)",
            "region_or_state": "Goa",
            "country": "India",
            "latitude": 15.5008,
            "longitude": 73.9117,
            "precision": "chapel_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1605-05-15",
            "approving_authority": "Archbishop Aleixo de Menezes / Pope Gregory XV (Canonization 1622) / Pope Pius XII (Minor Basilica 1946)",
            "confidence": "confirmed",
            "confidence_note_en": "Canonized by Pope Gregory XV in 1622; incorrupt body translated to Goa in 1554 and enshrined in the silver mausoleum crafted by Florentine sculptor Giovanni Battista Foggini; UNESCO World Heritage Site.",
            "confidence_note_vi": "Được Đức Giáo hoàng Grêgôriô XV tuyên thánh năm 1622; thi hài nguyên vẹn được rước về Goa năm 1554 an vị trong hòm bạc cẩm thạch do danh họa Florence Giovanni Battista Foggini chế tác; Di sản Thế giới UNESCO."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Incorrupt Body and Sacred Relics of Saint Francis Xavier, Apostle of the Indies and Japan",
                "relic_name_vi": "Thi Hài Nguyên Vẹn Không Hư Nát của Thánh Phanxicô Xaviê, Tông Đồ Xứ Ấn và Nhật Bản",
                "relic_type": "incorrupt_body",
                "reliquary_location": "Silver Casket in the Chapel of Saint Francis Xavier inside the Basilica of Bom Jesus"
            }
        ],
        "historical_summary_en": "Saint Francis Xavier (1506–1552), co-founder of the Society of Jesus (Jesuits) with Saint Ignatius of Loyola, is hailed as the greatest Catholic missionary since Saint Paul. Sent to Asia in 1541 as Apostolic Nuncio, Francis embarked on an epic decade-long missionary journey covering tens of thousands of nautical miles across India, Malacca, the Moluccas, and Japan, baptizing hundreds of thousands of souls with his own hands until his right arm grew exhausted.\n\nOn December 3, 1552, at the age of forty-six, Francis died of fever on the barren island of Shangchuan (*Sancian*) off the coast of mainland China while awaiting a boat to enter the closed Middle Kingdom. Buried in quicklime so his bones could later be transported, his body was exhumed months later and found completely fresh, supple, and incorrupt, exuding a sweet fragrance.\n\nIn 1554, Xavier's uncorrupted body was translated in triumph to Old Goa and placed within the magnificent Jesuit Basilica of Bom Jesus. Enshrined in a silver casket atop a three-tiered Florentine marble mausoleum gifted by Cosimo III de' Medici, Saint Francis Xavier remains the beloved 'Goencho Saib' (Lord of Goa) and Universal Patron of Catholic Missions.",
        "historical_summary_vi": "Thánh Phanxicô Xaviê (1506–1552), đồng sáng lập Dòng Tên (Dòng Chúa Giêsu) cùng Thánh Inhaxiô Loyola, được tôn vinh là nhà truyền giáo vĩ đại nhất của Giáo hội kể từ thời Thánh Phaolô Tông Đồ. Được cử sang Châu Á năm 1541 với tư cách Khâm Sứ Tòa Thánh, ngài đã thực hiện chuyến hải trình truyền giáo phi thường kéo dài một thập kỷ qua Ấn Độ, Malacca, quần đảo Maluku và Nhật Bản, đích thân rửa tội cho hàng trăm ngàn tín hữu đến mức cánh tay phải mỏi nhừ.\n\nNgày 3 tháng 12 năm 1552, ở tuổi 46, ngài qua đời vì sốt rét trên đảo hoang Thượng Xuyên ngoài khơi bờ biển Trung Hoa khi đang ngóng đợi thuyền đưa ngài vào đại lục. Thi hài ngài được chôn với vôi sống để sau này tiện cải táng, nhưng khi quật mộ nhiều tháng sau, thi thể ngài vẫn hoàn toàn mềm mại, tươi hồng nguyên vẹn và tỏa hương thơm ngào ngạt.\n\nNăm 1554, thi hài Thánh Phanxicô Xaviê được rước về Goa và an vị trong Vương Cung Thánh Đường Bom Jesus. Nằm trong hòm bạc tráng lệ trên bệ cẩm thạch Florence do Đại công tước Cosimo III de' Medici trao tặng, Thánh Phanxicô Xaviê là Đấng Bảo Trợ Toàn Cầu của Các Xứ Truyền Giáo.",
        "scripture_reading": "1 Corinthians 9:16-19",
        "suggested_prayer_en": "O Great Apostle of the Indies and Japan, Saint Francis Xavier, you burned with an unquenchable fire to bring the light of Christ to all nations. Inflame our hearts with your missionary zeal; teach us to seek the salvation of souls above all worldly comforts, and bring the Gospel to the ends of the earth. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Phanxicô Xaviê, Tông Đồ Vĩ Đại của Xứ Ấn và Nhật Bản, ngài đã bừng cháy ngọn lửa không bao giờ tắt để đem ánh sáng Chúa Kitô đến cho muôn dân nước. Xin thắp lên trong lòng chúng con ngọn lửa nhiệt thành truyền giáo; dạy chúng con biết đặt phần rỗi các linh hồn lên trên mọi tiện nghi danh lợi trần thế và hăng say loan báo Tin Mừng cho đến tận cùng trái đất. Amen.",
        "primary_sources": [
            {
                "label": "Archdiocese of Goa and Daman - Official Historical Dossier of Bom Jesus Basilica",
                "url": "https://archgoadaman.org/",
                "type": "academic"
            },
            {
                "label": "Pope Pius XI - Apostolic Letter Gravem Sane Declaring St. Francis Xavier Patron of Missions (1927)",
                "url": "https://www.vatican.va/content/pius-xi/la/apost_letters/documents/hf_p-xi_apl_19271214_gravem-sane.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "quiapo_black_nazarene_manila",
        "category": "passion_relic",
        "name_en": "Minor Basilica of the Black Nazarene (Quiapo Church)",
        "name_vi": "Vương Cung Thánh Đường Chúa Nazareno Đen (Nhà Thờ Quiapo, Manila)",
        "feast_day_association": "Feast of the Black Nazarene / Traslación (January 9) / Good Friday",
        "location": {
            "shrine_or_basilica": "Minor Basilica of the Black Nazarene (Saint John the Baptist Parish)",
            "city": "Quiapo, Manila",
            "region_or_state": "Metro Manila (NCR)",
            "country": "Philippines",
            "latitude": 14.5986,
            "longitude": 120.9847,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1987-12-11",
            "approving_authority": "Pope Innocent X (Papal Bull 1650) / Pope John Paul II (Minor Basilica 1987)",
            "confidence": "confirmed",
            "confidence_note_en": "Arrived in Manila in 1606 brought by Augustinian Recollect missionaries from Mexico; papal confraternity established by Pope Innocent X in 1650; elevated to Minor Basilica by Pope John Paul II in 1987.",
            "confidence_note_vi": "Được các thừa sai Dòng Augustinô Recoleto rước từ Mexico đến Manila năm 1606; Huynh đoàn Giáo hoàng được Đức Innôcentê X chuẩn nhận năm 1650; được Đức Gioan Phaolô II nâng lên hàng Tiểu Vương Cung Thánh Đường năm 1987."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Miraculous 17th-Century Dark Mesquite-Wood Statue of the Nazarene Carrying the Cross",
                "relic_name_vi": "Tượng Gỗ Mun Phép Lạ Thế Kỷ 17 Tạc Chúa Giêsu Nazareno Vác Thánh Giá",
                "relic_type": "holy_icon",
                "reliquary_location": "Main Retablo of the Minor Basilica of the Black Nazarene, Quiapo"
            }
        ],
        "historical_summary_en": "The Black Nazarene (*Nuestro Padre Jesús Nazareno*) is a life-sized dark wooden statue of Jesus Christ carrying the heavy Cross on His way to Mount Calvary, carved by an anonymous indigenous Mexican artisan in the 16th century out of dark mesquite wood. On May 31, 1606, Augustinian Recollect missionaries brought the sacred statue aboard a Manila galleon to the Philippines.\n\nThroughout four centuries, the statue miraculously survived multiple devastating catastrophic fires (1791 and 1929), powerful earthquakes (1645 and 1863), and the massive artillery bombardment during the Battle of Manila in 1945 that destroyed surrounding neighborhoods, emerging entirely unscathed. In 1787, Archbishop Basilio Sancho de Santas Justa y Rufina ordered the solemn translation (*Traslación*) of the image to the Saint John the Baptist parish in Quiapo.\n\nThe annual *Traslación* on January 9 is the largest religious gathering in Asia, drawing over six million barefoot devotees (*namamasan*) who accompany the carriage in massive waves of prayer, thanksgiving, and penance, seeking to touch the ropes or the sacred statue of Christ who bears their daily struggles.",
        "historical_summary_vi": "Chúa Nazareno Đen (*Nuestro Padre Jesús Nazareno*) là bức tượng gỗ kích thước người thật tạc hình ảnh Chúa Giêsu Kitô gục ngã dưới sức nặng của Thập Giá trên đường lên Núi Sọ, do một nghệ nhân bản địa Mexico tạc vào thế kỷ 16 từ loại gỗ sẫm màu mesquite. Ngày 31 tháng 5 năm 1606, các linh mục Dòng Augustinô Recoleto đã đưa pho tượng thánh vượt Thái Bình Dương trên tàu buồm galleon về Manila.\n\nTrải qua hơn 4 thế kỷ, bức tượng đã sống sót kỳ diệu qua nhiều trận hỏa hoạn kinh hoàng (1791 và 1929), các trận động đất dữ dội (1645 và 1863) và trận ném bom tàn phá khốc liệt trong Trận chiến Manila năm 1945. Năm 1787, Tổng Giám mục Manila đã cho rước tượng (*Traslación*) về tôn kính tại Nhà thờ Thánh Gioan Baotixita ở Quiapo.\n\nLễ rước *Traslación* hằng năm vào ngày 9 tháng 1 là sự kiện tôn giáo quy mô lớn nhất Châu Á, quy tụ hơn 6 triệu tín hữu đi chân trần (*namamasan*) chen chúc hộ tống cỗ kiệu trong biển người cầu nguyện, tạ ơn và đền tội, với niềm khao khát được chạm tay vào dây kéo kiệu hay vào tà áo Chúa Giêsu Đấng gánh vác mọi đau khổ cuộc đời.",
        "scripture_reading": "Isaiah 53:4-5",
        "suggested_prayer_en": "Lord Jesus of Nazareth, who carried the crushing weight of the Cross for our salvation, look upon the burdens and suffering of our lives. Grant strength to the weary, heal our afflictions of body and soul, and teach us to follow in your footsteps with patient and persevering love. Amen.",
        "suggested_prayer_vi": "Lạy Chúa Giêsu Nazareno, Đấng đã vác lấy sức nặng đè nát của Thập Giá để cứu chuộc chúng con, xin đoái nhìn đến những gánh nặng và đau khổ trong cuộc đời chúng con. Xin ban sức mạnh cho những tâm hồn mệt mỏi, chữa lành các tật nguyền thể xác và linh hồn, và dạy chúng con biết kiên vững bước theo chân Chúa trong tình yêu mến sắt son. Amen.",
        "primary_sources": [
            {
                "label": "Minor Basilica of the Black Nazarene Official Archival Documentation",
                "url": "https://quiapochurch.com.ph/",
                "type": "academic"
            },
            {
                "label": "CBCP (Catholic Bishops' Conference of the Philippines) - Historical Dossier on the Traslacion of Quiapo",
                "url": "https://cbcpnews.net/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "north_american_martyrs_auriesville",
        "category": "martyr_shrine",
        "name_en": "National Shrine of Our Lady of Martyrs (Auriesville)",
        "name_vi": "Đền Thánh Quốc Gia Các Thánh Tử Đạo Bắc Mỹ (Auriesville)",
        "feast_day_association": "Feast of the North American Martyrs / Saints Isaac Jogues and Companions (October 19)",
        "location": {
            "shrine_or_basilica": "National Shrine of Our Lady of Martyrs (The Coliseum)",
            "city": "Auriesville",
            "region_or_state": "New York",
            "country": "United States",
            "latitude": 42.9292,
            "longitude": -74.3167,
            "precision": "apparition_ground"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1930-06-29",
            "approving_authority": "Pope Pius XI (Canonization of North American Martyrs) / USCCB National Shrine",
            "confidence": "confirmed",
            "confidence_note_en": "Site of the 17th-century Mohawk village of Ossernenon, where Saints Isaac Jogues, René Goupil, and John de Lalande were martyred (1642-1646); birthplace of Saint Kateri Tekakwitha (1656); canonized by Pope Pius XI in 1930.",
            "confidence_note_vi": "Địa điểm ngôi làng Ossernenon của bộ tộc Mohawk thế kỷ 17, nơi các Thánh Isaac Jogues, René Goupil và John de Lalande chịu tử đạo (1642-1646); nơi sinh của Thánh Nữ Kateri Tekakwitha (1656); được Đức Piô XI tuyên thánh năm 1930."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Holy Ground of Ossernenon and Relics of Saints Isaac Jogues, René Goupil, and Jean de Lalande",
                "relic_name_vi": "Đất Thánh Pháp Trường Ossernenon và Hài Cốt Các Thánh Tử Đạo Dòng Tên Bắc Mỹ",
                "relic_type": "1st_class_bone",
                "reliquary_location": "The Great Coliseum Basilica and The Ravine of the Martyrs at Auriesville"
            }
        ],
        "historical_summary_en": "The National Shrine of Our Lady of Martyrs in Auriesville, New York, sits atop the historic site of Ossernenon, a 17th-century fortified Mohawk village overlooking the Mohawk River. It is sanctified by the martyrdom of three French Jesuit missionaries—Saint René Goupil (martyred 1642, the first canonized martyr in North America), Saint Isaac Jogues (martyred 1646), and Saint Jean de Lalande (martyred 1646)—and is the birthplace of Saint Kateri Tekakwitha (1656–1680), the 'Lily of the Mohawks.'\n\nFather Isaac Jogues and surgeon René Goupil were captured in 1642, enduring brutal torture including the chewing and slicing off of their fingers. When Goupil made the Sign of the Cross over a Mohawk child's forehead, he was killed with a tomahawk blow. Jogues escaped to France, where Pope Urban VIII granted him a special dispensation to celebrate Mass with his mutilated hands, saying: *'It would be shameful if a martyr of Christ could not drink the Blood of Christ.'*\n\nDriven by love for souls, Father Jogues returned to Ossernenon in 1646 as a peace envoy and was martyred by a tomahawk strike on October 18, 1646. The massive circular Coliseum at Auriesville, seating 10,000 pilgrims, stands as a monument to apostolic heroism.",
        "historical_summary_vi": "Đền Thánh Quốc Gia Đức Mẹ Các Vị Tử Đạo tại Auriesville, New York, tọa lạc trên vị trí pháo đài cổ Ossernenon của người da đỏ Mohawk thế kỷ 17 bên bờ sông Mohawk. Nơi đây được thánh hóa bởi máu tử đạo của ba thừa sai Dòng Tên người Pháp—Thánh René Goupil (tử đạo 1642, vị thánh tử đạo đầu tiên tại Bắc Mỹ), Thánh Isaac Jogues (tử đạo 1646) và Thánh Jean de Lalande (tử đạo 1646)—đồng thời là quê hương của Thánh Nữ Kateri Tekakwitha (1656–1680), 'Bông Hoa Huệ của Người Mohawk'.\n\nCha Isaac Jogues và y sĩ René Goupil bị bắt năm 1642 và phải chịu những đòn tra tấn dã man như bị chặt đứt các ngón tay. Khi Goupil làm Dấu Thánh Giá trên trán một em bé Mohawk, ngài đã bị chém rìu vào đầu tử đạo. Cha Jogues trốn thoát về Pháp và được Đức Giáo hoàng Urbanô VIII đặc cách cho phép dâng Lễ bằng đôi bàn tay cụt ngón, với lời ca ngợi: *'Thật bất xứng nếu một vị tử đạo của Chúa Kitô lại không được uống Máu Chúa Kitô.'*\n\nVì tình yêu cứu rỗi các linh hồn, Cha Jogues đã dũng cảm trở lại làng Ossernenon năm 1646 và chịu tử đạo ngày 18 tháng 10 năm 1646. Đền thờ Đại Đấu Trường (The Coliseum) hình tròn khổng lồ chứa 10.000 người là tượng đài bất khuất của lòng quả cảm truyền giáo.",
        "scripture_reading": "2 Corinthians 4:8-10",
        "suggested_prayer_en": "O Holy North American Martyrs, Saints Isaac Jogues, René Goupil, and companions, you sowed the seeds of faith in this continent through your suffering and martyrdom. Grant us an apostolic courage that does not shrink before hostility, and inspire a new springtime of vocations and vibrant faith throughout the Americas. Amen.",
        "suggested_prayer_vi": "Lạy Các Thánh Tử Đạo Bắc Mỹ, Thánh Isaac Jogues, Thánh René Goupil và các bạn, các ngài đã gieo hạt giống đức tin trên lục địa này bằng máu đào và sự hy sinh anh dũng. Xin ban cho chúng con lòng can đảm truyền giáo không sờn lòng trước nghịch cảnh, và làm trổ sinh một mùa xuân mới dồi dào ơn gọi và đức tin sống động trên khắp Châu Mỹ. Amen.",
        "primary_sources": [
            {
                "label": "National Shrine of Our Lady of Martyrs Official Historical Archive",
                "url": "https://www.ourladyofmartyrs.org/",
                "type": "academic"
            },
            {
                "label": "Pope Pius XI - Apostolic Constitution for the Canonization of the North American Martyrs (1930)",
                "url": "https://www.vatican.va/content/vatican/en.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "st_elizabeth_ann_seton_emmitsburg",
        "category": "doctor_of_church",
        "name_en": "National Shrine of Saint Elizabeth Ann Seton (Emmitsburg)",
        "name_vi": "Đền Thánh Quốc Gia Thánh Nữ Elizabeth Ann Seton (Emmitsburg)",
        "feast_day_association": "Feast of Saint Elizabeth Ann Seton (January 4)",
        "location": {
            "shrine_or_basilica": "National Shrine of Saint Elizabeth Ann Seton (Basilica of Saint Elizabeth Ann Seton)",
            "city": "Emmitsburg",
            "region_or_state": "Maryland",
            "country": "United States",
            "latitude": 39.6978,
            "longitude": -77.3228,
            "precision": "chapel_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1975-09-14",
            "approving_authority": "Pope Paul VI (First Native-Born US Saint Canonization)",
            "confidence": "confirmed",
            "confidence_note_en": "Canonized by Pope Paul VI on September 14, 1975 as the first native-born citizen of the United States to be raised to sainthood; foundress of the Sisters of Charity of Saint Joseph and pioneer of the American Catholic parochial school system.",
            "confidence_note_vi": "Được Đức Giáo hoàng Phaolô VI tuyên thánh ngày 14 tháng 9 năm 1975 là vị thánh tiên khởi sinh ra trên đất nước Hoa Kỳ; đấng sáng lập Dòng Nữ Tử Bác Ái Thánh Giuse và đặt nền móng cho hệ thống trường học Công giáo Hoa Kỳ."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Sacred Bones and Tomb of Saint Elizabeth Ann Seton (Mother Seton)",
                "relic_name_vi": "Hài Cốt và Lăng Mộ Thánh Nữ Elizabeth Ann Seton (Mẹ Seton)",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Altar of Relics inside the Basilica of the National Shrine of Saint Elizabeth Ann Seton"
            }
        ],
        "historical_summary_en": "Saint Elizabeth Ann Bayley Seton (1774–1821), born in New York City into an aristocratic Episcopalian family, was a devoted wife, mother of five children, and social philanthropist. Following the early death of her husband William Magee Seton in Livorno, Italy, in 1803, Elizabeth was deeply moved by the living faith and Eucharistic devotion of Italian Catholic friends, leading to her reception into the Catholic Church at Saint Peter's Church in New York in 1805, facing total ostracism from family and society.\n\nIn 1809, invited by Bishop John Carroll of Baltimore, Mother Seton relocated to Emmitsburg, Maryland, where she founded the Sisters of Charity of Saint Joseph—the first congregation of religious sisters established in the United States. She opened Saint Joseph's Free Academy, pioneering the parochial Catholic school system in America.\n\nMother Seton lived a life centered upon the Real Presence of Jesus in the Blessed Sacrament and filial devotion to Our Lady. Dying of tuberculosis on January 4, 1821, at the age of forty-six, she left a flourishing spiritual legacy. On September 14, 1975, Pope Paul VI canonized her before a crowd of 100,000 pilgrims in Saint Peter's Square.",
        "historical_summary_vi": "Thánh Nữ Elizabeth Ann Bayley Seton (1774–1821), sinh trưởng tại Thành phố New York trong một gia đình quý tộc Anh Giáo, là một người vợ tận tụy, người mẹ của 5 người con và là nhà từ thiện xã hội. Sau khi người chồng William Magee Seton qua đời sớm tại Livorno, Ý năm 1803, ngài đã được đánh động sâu xa bởi đức tin và lòng tôn sùng Thánh Thể của các gia đình Công giáo Ý, dẫn đến quyết định gia nhập Giáo hội Công giáo tại Nhà thờ Thánh Phêrô New York năm 1805 dù bị gia đình ruồng bỏ.\n\nNăm 1809, theo lời mời của Đức Giám mục John Carroll, Mẹ Seton chuyển về Emmitsburg, Maryland, nơi ngài sáng lập Dòng Nữ Tử Bác Ái Thánh Giuse—dòng nữ tiên khởi được thành lập trên đất Mỹ. Ngài đã mở trường Thánh Giuse miễn phí cho học sinh nghèo, đặt nền móng tiên phong cho toàn bộ hệ thống trường học Công giáo giáo xứ tại Hoa Kỳ.\n\nMẹ Seton sống đời thánh thiện đặt trung tâm nơi Bí Tích Thánh Thể và lòng yêu mến Đức Mẹ. Qua đời vì bệnh lao ngày 4 tháng 1 năm 1821 ở tuổi 46, ngài để lại một di sản tâm linh rực rỡ. Ngày 14 tháng 9 năm 1975, Đức Giáo hoàng Phaolô VI đã long trọng tuyên thánh cho ngài trước 100.000 tín hữu tại Quảng trường Thánh Phêrô.",
        "scripture_reading": "Matthew 25:35-40",
        "suggested_prayer_en": "Lord God, you blessed Saint Elizabeth Ann Seton with an ardent love for the Holy Eucharist and a courageous charity for the education of the young and the care of the poor. Grant that inspired by her example, we may serve Christ with joy in our neighbors and walk faithfully in the light of His Gospel. Amen.",
        "suggested_prayer_vi": "Lạy Chúa là Thiên Chúa chúng con, Chúa đã ban cho Thánh Nữ Elizabeth Ann Seton lòng yêu mến Thánh Thể nồng nàn và đức bác ái can trường trong việc giáo dục người trẻ và chăm sóc người nghèo khó. Xin cho chúng con noi gương sáng của ngài, biết hân hoan phụng sự Chúa Kitô nơi tha nhân và bước đi trung thành trong ánh sáng Tin Mừng của Chúa. Amen.",
        "primary_sources": [
            {
                "label": "National Shrine of Saint Elizabeth Ann Seton Official Archives",
                "url": "https://setonshrine.org/",
                "type": "academic"
            },
            {
                "label": "Pope Paul VI - Homily for the Canonization of Elizabeth Ann Bayley Seton (September 14, 1975)",
                "url": "https://www.vatican.va/content/paul-vi/en/homilies/1975/documents/hf_p-vi_hom_19750914_seton.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "sainte_anne_de_beaupre_quebec",
        "category": "marian_apparition",
        "name_en": "Basilica of Sainte-Anne-de-Beaupré (Quebec)",
        "name_vi": "Đại Vương Cung Thánh Đường Thánh Anna Beaupré (Quebec)",
        "feast_day_association": "Feast of Saints Joachim and Anne, Parents of the Blessed Virgin Mary (July 26)",
        "location": {
            "shrine_or_basilica": "Basilique Sainte-Anne-de-Beaupré",
            "city": "Sainte-Anne-de-Beaupré",
            "region_or_state": "Quebec",
            "country": "Canada",
            "latitude": 47.0236,
            "longitude": -70.9281,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1876-05-07",
            "approving_authority": "Pope Leo XIII (Minor Basilica 1887) / Pope Francis (Papal Mass 2022)",
            "confidence": "confirmed",
            "confidence_note_en": "First miraculous healing recorded in 1658 (Louis Guimont cured of crippling scoliosis); elevated to Minor Basilica by Pope Leo XIII in 1887; celebrated as the premier healing shrine in North America.",
            "confidence_note_vi": "Phép lạ chữa lành đầu tiên được ghi nhận năm 1658 (Louis Guimont được khỏi tật gù lưng bại liệt); được Đức Giáo hoàng Lêô XIII nâng lên hàng Tiểu Vương Cung Thánh Đường năm 1887; đền thánh chữa lành lớn nhất Bắc Mỹ."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Major Relic of the Forearm Bone of Saint Anne and the Miraculous Statue",
                "relic_name_vi": "Xương Cẳng Tay Thánh Nữ Anna (Bà Ngoại Chúa Giêsu) và Tượng Phép Lạ",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Gold and Enamel Reliquary Chapel inside the Basilica of Sainte-Anne-de-Beaupré"
            }
        ],
        "historical_summary_en": "The Basilica of Sainte-Anne-de-Beaupré, situated along the Saint Lawrence River twenty miles northeast of Quebec City, is the oldest pilgrimage site in North America. In 1658, French Breton sailors caught in a ferocious storm on the Saint Lawrence vowed to build a chapel to Good Saint Anne (*Bonne Sainte-Anne*), the patroness of seafarers, if they survived. Upon landing safely at Beaupré, they fulfilled their promise.\n\nDuring construction in 1658, a local laborer named Louis Guimont, suffering from crippling rheumatism and lumbar deformity, placed three foundation stones in devotion to Saint Anne and was instantly and completely cured before multiple witnesses. Countless physical healings followed, evidenced by the vast pillars covered in discarded crutches, canes, and prostheses flanking the entrance.\n\nIn 1892, Cardinal Elzéar-Alexandre Taschereau obtained a major relic of Saint Anne's forearm from Saint Paul Outside the Walls in Rome. Over a million pilgrims, including indigenous First Nations peoples who hold Saint Anne in supreme veneration, journey annually to the majestic Neo-Romanesque basilica.",
        "historical_summary_vi": "Đại Vương Cung Thánh Đường Thánh Anna Beaupré, tọa lạc bên bờ sông Saint Lawrence cách thành phố Quebec 30 cây số về phía đông bắc, là trung tâm hành hương cổ kính nhất Bắc Mỹ. Năm 1658, các thủy thủ người Breton nước Pháp gặp phải cơn giông bão dữ dội trên sông đã khấn hứa xây một nhà nguyện kính Thánh Anna (*Bonne Sainte-Anne*)—quan thầy các thủy thủ—nếu được bình an thoát nạn. Khi cập bến Beaupré an toàn, họ đã giữ trọn lời thề.\n\nTrong lúc đặt móng nhà nguyện năm 1658, một người thợ địa phương tên Louis Guimont bị bệnh gù lưng và bại liệt cột sống nặng đã thành kính đặt ba viên đá nền và được chữa lành hoàn toàn tức thì trước sự chứng kiến của nhiều người. Vô số phép lạ chữa lành đã tiếp nối, minh chứng qua những hàng cột chất đầy nạng gỗ và gậy chống của các bệnh nhân được chữa lành nơi lối vào.\n\nNăm 1892, Đức Hồng y Taschereau đã rước thánh tích xương cẳng tay Thánh Anna từ Đền thờ Thánh Phaolô Ngoại Thành ở Roma về đền thánh. Mỗi năm có hơn một triệu khách hành hương, đặc biệt là các thổ dân bản địa Canada vốn hết lòng sùng kính Bà Ngoại Thánh Anna, đổ về kính viếng đại thánh đường.",
        "scripture_reading": "Proverbs 31:25-30",
        "suggested_prayer_en": "Good Saint Anne, Mother of the Virgin Mary and Grandmother of Jesus, you welcomed thousands of suffering souls to your shrine in Beaupré. Look upon our physical and spiritual afflictions; obtain for us health of body and soul, and teach our families to walk in holiness and mutual love. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Nữ Anna Nhân Lành, Thân Mẫu của Đức Trinh Nữ Maria và là Bà Ngoại của Chúa Giêsu, ngài đã mở rộng vòng tay đón nhận hàng triệu tâm hồn đau khổ tại đền thánh Beaupré. Xin đoái nhìn đến những tật nguyền đau yếu của thân xác và tâm hồn chúng con; xin chữa lành và ban ơn nâng đỡ cho gia đình chúng con luôn bước đi trong thánh thiện và yêu thương. Amen.",
        "primary_sources": [
            {
                "label": "Sanctuaire Sainte-Anne-de-Beaupré Official Archival Records",
                "url": "https://sainte-anne-de-beaupre.com/en",
                "type": "academic"
            },
            {
                "label": "Pope Francis - Homily at the National Shrine of Sainte-Anne-de-Beaupré (July 28, 2022)",
                "url": "https://www.vatican.va/content/francesco/en/homilies/2022/documents/20220728-omelia-quebec.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "senor_de_los_milagros_lima",
        "category": "passion_relic",
        "name_en": "Sanctuary of Las Nazarenas (Señor de los Milagros)",
        "name_vi": "Đền Thánh Các Nữ Tu Nazarenas (Chúa Các Phép Lạ, Lima)",
        "feast_day_association": "Feast of Señor de los Milagros / Purple Month (October 18 & 28)",
        "location": {
            "shrine_or_basilica": "Santuario y Monasterio de Las Nazarenas",
            "city": "Lima",
            "region_or_state": "Lima Province",
            "country": "Peru",
            "latitude": -12.0447,
            "longitude": -77.0353,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1771-01-20",
            "approving_authority": "Viceroy Manuel de Amat / Pope Benedict XVI (Papal Blessing 2005)",
            "confidence": "confirmed",
            "confidence_note_en": "Mural painted in 1651 by an enslaved Angolan African (*Benito*); survived catastrophic earthquakes of 1655, 1687, and 1746 that leveled Lima; recognized by the Holy See as the Patron of Lima and all Peruvians worldwide.",
            "confidence_note_vi": "Bức bích họa do một nô lệ người Angola (*Benito*) vẽ năm 1651 trên tường đất; sống sót kỳ diệu qua các trận siêu động đất năm 1655, 1687 và 1746 san phẳng thủ đô Lima; được Tòa Thánh tôn vinh là Quan Thầy thành phố Lima."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Miraculous 1651 Adobe Wall Mural of the Crucified Christ (Cristo Moreno)",
                "relic_name_vi": "Bức Bích Họa Phép Lạ Trên Tường Đất Năm 1651 Tạc Chúa Chịu Đóng Đinh (Chúa Da Ngăm)",
                "relic_type": "holy_icon",
                "reliquary_location": "High Altar Retablo of the Church of Las Nazarenas, Lima"
            }
        ],
        "historical_summary_en": "In approximately 1651, in the impoverished Pachacamilla neighborhood of Lima, Peru, an enslaved Angolan African named Benito (or Pedro Dalcón) painted a poignant mural of the Crucified Christ with the Holy Spirit and God the Father upon a rough adobe mud-brick wall. On November 13, 1655, a catastrophic 7.8 magnitude earthquake struck Lima and Callao, flattening nearly the entire city; miraculously, the fragile adobe wall bearing the fresco remained completely standing without a single crack.\n\nIn 1671, civil authorities attempted to erase the mural due to unruly crowds, but every artisan sent to destroy it experienced trembling, fainting, or witnessed the image glow with divine light. In 1687 and again in the apocalyptic earthquake of 1746, the city was flattened, yet the adobe mural stood undisturbed.\n\nA monastery of Discalced Nazarene Carmelite nuns was erected around the wall to protect it perpetually. Every October during *Mes Morado* ('The Purple Month'), hundreds of thousands of faithful wearing purple tunics accompany the two-ton silver litter carrying a replica of the *Cristo Moreno* through Lima in what is recognized as one of the world's largest annual religious processions.",
        "historical_summary_vi": "Vào khoảng năm 1651, tại khu phố nghèo Pachacamilla ở thủ đô Lima, Peru, một người nô lệ da đen gốc Angola tên Benito đã vẽ một bức bích họa đơn sơ cảm động tạc hình Chúa Giêsu chịu đóng đinh cùng Chúa Cha và Chúa Thánh Thần trên một bức tường đất bùn mộc mạc. Ngày 13 tháng 11 năm 1655, một trận siêu động đất kinh hoàng 7,8 độ richter đã san phẳng gần như toàn bộ thành phố Lima; kỳ lạ thay, bức tường đất mỏng manh mang bức bích họa vẫn đứng vững nguyên vẹn không một vết nứt.\n\nNăm 1671, chính quyền địa phương cử thợ đến đập bỏ bức tường vì sợ đám đông tụ tập, nhưng những người thợ được cử đến đều bị run rẩy, ngất xỉu hoặc nhìn thấy bức tranh tỏa hào quang chói lọi. Trong các trận động đất năm 1687 và 1746 phá hủy cả thành phố, bức tường tranh vẫn sừng sững uy nghiêm.\n\nMột đan viện các nữ tu Dòng Kín Nazarenas đã được xây dựng bao quanh bức tường để chăm sóc bảo tồn. Hằng năm vào tháng 10 (*Tháng Màu Tím - Mes Morado*), hàng triệu tín hữu mặc áo thụng tím tham gia cuộc rước kiệu bạc khổng lồ nặng hai tấn cung nghinh Linh Ảnh Chúa Các Phép Lạ qua khắp các đường phố Lima, tạo nên một trong những lễ hội tôn giáo lớn nhất thế giới.",
        "scripture_reading": "Colossians 1:19-20",
        "suggested_prayer_en": "Lord of Miracles, Cristo Moreno, who stood unshaken through the violent earthquakes of history, be the solid anchor of our lives. Protect our families from spiritual and temporal disasters, heal our infirmities, and unite our hearts in fraternal solidarity and unfailing charity. Amen.",
        "suggested_prayer_vi": "Lạy Chúa Các Phép Lạ (*Señor de los Milagros*), Đấng đã đứng vững vàng kiên cố qua bao trận siêu động đất của lịch sử, xin làm tảng đá neo đậu vững chắc cho cuộc đời chúng con. Xin bảo vệ gia đình chúng con khỏi mọi hiểm họa tâm linh và thể xác, chữa lành những đau yếu bệnh tật và liên kết tâm hồn chúng con trong tình bác ái huynh đệ bền vững. Amen.",
        "primary_sources": [
            {
                "label": "Archdiocese of Lima - Official History and Chronicles of Señor de los Milagros",
                "url": "https://arzobispadodelima.org/",
                "type": "academic"
            },
            {
                "label": "Pope Francis - Message for the Festivity of the Lord of Miracles (October 2020)",
                "url": "https://www.vatican.va/content/francesco/es/messages/pont-messages/2020/documents/papa-francesco_20201018_messaggio-senordelosmilagros.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "our_lady_of_lujan_argentina",
        "category": "marian_apparition",
        "name_en": "Basilica of Our Lady of Luján (Patroness of Argentina)",
        "name_vi": "Đại Vương Cung Thánh Đường Đức Mẹ Luján (Quan Thầy Nước Argentina)",
        "feast_day_association": "Feast of Our Lady of Luján (May 8)",
        "location": {
            "shrine_or_basilica": "Basílica Nacional de Nuestra Señora de Luján",
            "city": "Luján",
            "region_or_state": "Buenos Aires Province",
            "country": "Argentina",
            "latitude": -34.5647,
            "longitude": -59.1217,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1887-05-08",
            "approving_authority": "Pope Leo XIII (Papal Coronation) / Pope Pius XI (Patroness of Argentina, Uruguay, and Paraguay 1930)",
            "confidence": "confirmed",
            "confidence_note_en": "Statue brought in 1630; crowned with papal crown by Pope Leo XIII on May 8, 1887; declared Principal Patroness of Argentina, Uruguay, and Paraguay by Pope Pius XI in 1930; spiritual cradle of Cardinal Jorge Mario Bergoglio (Pope Francis).",
            "confidence_note_vi": "Tượng Đức Mẹ được rước đến năm 1630; Đức Giáo hoàng Lêô XIII ban triều thiên vàng ngày 8 tháng 5 năm 1887; Đức Piô XI tuyên phong là Đấng Bảo Trợ Argentina, Uruguay và Paraguay năm 1930; là ngôi nhà tâm linh của Đức Giáo hoàng Phanxicô."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Miraculous 1630 Terracotta Statue of the Immaculate Conception and Tomb of Negro Manuel",
                "relic_name_vi": "Tượng Đất Nung Phép Lạ Năm 1630 của Đức Mẹ Vô Nhiễm và Mộ Người Nô Lệ Manuel",
                "relic_type": "holy_icon",
                "reliquary_location": "Main Chamber of the High Altar Retablo in the Basilica of Luján"
            }
        ],
        "historical_summary_en": "In May 1630, a Portuguese merchant named Antonio Sáenz de Saavedra requested a small terracotta image of the Immaculate Conception from Brazil for his estate in Sumampa. The image was transported in a wooden box aboard an oxcart convoy. When the caravan reached the banks of the Luján River (forty miles west of Buenos Aires), the oxen pulling one specific cart suddenly stopped and refused to move, despite the drovers' repeated whipping and unloading of extra cargo.\n\nWhen the drovers lifted out the small crate containing the terracotta statue of the Virgin Mary, the oxen effortlessly moved forward. Realizing that heaven had designated the site for her sanctuary, the local inhabitants received the image with tears of joy. An enslaved Afro-descendant young man named Manuel Costa dos Santos (*Negro Manuel*) consecrated his entire life to serving the Virgin, faithfully maintaining the chapel for fifty-six years until his death.\n\nThe monumental French Neo-Gothic Basilica of Luján, constructed between 1890 and 1935, is the national shrine of Argentina, hosting millions of pilgrims annually. Cardinal Jorge Mario Bergoglio (Pope Francis) was a frequent pilgrim to Luján, spending long hours in the confessional and entrusting his Petrine ministry to Our Lady of Luján.",
        "historical_summary_vi": "Vào tháng 5 năm 1630, một thương gia người Bồ Đào Nha tên Antonio Sáenz de Saavedra đã đặt mua một bức tượng nhỏ bằng đất nung tạc Đức Mẹ Vô Nhiễm từ Brazil để mang về trang trại ở Sumampa. Bức tượng được cất trong một chiếc hộp gỗ chở trên đoàn xe bò. Khi đoàn xe đến bờ sông Luján (cách Buenos Aires 60 cây số về phía tây), những con bò kéo cỗ xe chở tượng bỗng dừng khựng lại và kiên quyết không chịu bước tiếp dù bị quất roi và dỡ bớt đồ đạc.\n\nChỉ khi người ta nhấc chiếc thùng gỗ đựng tượng Đức Mẹ xuống đất thì đàn bò mới chịu kéo xe đi tiếp dễ dàng. Nhận ra thánh ý thiên đàng muốn Mẹ ngự lại nơi đây, dân làng đã vui mừng đón nhận linh tượng. Một người thanh niên nô lệ da đen tên Manuel (*Negro Manuel*) đã tự nguyện tận hiến trọn đời để phụng sự Đức Mẹ, trung thành chăm sóc nguyện đường suốt 56 năm cho đến ngày qua đời.\n\nĐại Vương Cung Thánh Đường Tân Gothic lộng lẫy tại Luján xây dựng từ năm 1890 đến 1935 là trung tâm đền thánh quốc gia của Argentina. Đức Thánh Cha Phanxicô khi còn là Tổng Giám mục Buenos Aires đã thường xuyên hành hương bộ về Luján ngồi tòa giải tội và dâng trọn triều đại giáo hoàng của ngài cho Đức Mẹ Luján.",
        "scripture_reading": "Luke 1:46-49",
        "suggested_prayer_en": "O Blessed Virgin Mary of Luján, Mother of Hope and Patroness of Argentina, you chose to remain among the humble people on the banks of the river. Protect our nations from division and despair, accompany our journey with your maternal care, and guide all peoples to the peace of your Divine Son. Amen.",
        "suggested_prayer_vi": "Lạy Đức Mẹ Luján, Mẹ của Niềm Hy Vọng và Quan Thầy Nước Argentina, Mẹ đã chọn ở lại giữa những người khiêm hạ bên bờ sông Luján. Xin bảo vệ các quốc gia chúng con khỏi sự chia rẽ và tuyệt vọng, đồng hành với cuộc lữ hành trần thế của chúng con bằng tình mẫu tử dịu hiền và dẫn đưa muôn dân về trong bình an của Con Chí Thánh Mẹ. Amen.",
        "primary_sources": [
            {
                "label": "Basílica Nacional de Nuestra Señora de Luján Official Archival History",
                "url": "https://santuariodelujan.org.ar/",
                "type": "academic"
            },
            {
                "label": "Pope Francis - Message to Pilgrims of the National Shrine of Our Lady of Luján (May 2021)",
                "url": "https://www.vatican.va/content/francesco/es/messages/pont-messages/2021/documents/papa-francesco_20210508_videomessaggio-madonna-lujan.html",
                "type": "vatican"
            }
        ]
    }
]

def main():
    target_dir = "Anno/Resources/SacredSanctuaries"
    os.makedirs(target_dir, exist_ok=True)
    
    for item in BATCH_8:
        filename = f"{item['sanctuary_id']}.json"
        path = os.path.join(target_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False, indent=2)
        print(f"Generated {filename}")

if __name__ == "__main__":
    main()

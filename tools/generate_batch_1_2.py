#!/usr/bin/env python3
"""
generate_batch_1_2.py
Generates Batch 1 (Major World Marian Apparitions I) & Batch 2 (Marian Apparitions II & Regional Sanctuaries)
"""

import json
import os

BATCH_1 = [
    {
        "sanctuary_id": "our_lady_of_guadalupe",
        "category": "marian_apparition",
        "name_en": "Basilica of Our Lady of Guadalupe",
        "name_vi": "Vương Cung Thánh Đường Đức Mẹ Guadalupe",
        "feast_day_association": "Feast of Our Lady of Guadalupe (December 12)",
        "location": {
            "shrine_or_basilica": "Insigne y Nacional Basílica de Santa María de Guadalupe",
            "city": "Mexico City",
            "region_or_state": "Federal District",
            "country": "Mexico",
            "latitude": 19.4847,
            "longitude": -99.1175,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1531-12-12",
            "approving_authority": "Bishop Juan de Zumárraga / Pope Benedict XIV (Papal Bull 1754)",
            "confidence": "confirmed",
            "confidence_note_en": "Formally confirmed by Archbishop Juan de Zumárraga following the miraculous preservation of the Tilma in 1531; declared Patroness of the Americas by Pope Pius XII and confirmed by Pope John Paul II in 1999.",
            "confidence_note_vi": "Được Đức Giám mục Juan de Zumárraga chính thức công nhận sau khi phép lạ in hình trên áo Tilma xảy ra năm 1531; Đức Giáo hoàng Piô XII tuyên phong là Quan Thầy Toàn Châu Mỹ và Đức Gioan Phaolô II tái khẳng định năm 1999."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Miraculous Tilma of Saint Juan Diego",
                "relic_name_vi": "Áo Choàng Tilma Phép Lạ của Thánh Juan Diego",
                "relic_type": "miraculous_textile",
                "reliquary_location": "Suspended above the High Altar in the New Basilica"
            }
        ],
        "historical_summary_en": "In December 1531, on Tepeyac Hill north of Mexico City, the Blessed Virgin Mary appeared four times to Saint Juan Diego Cuauhtlatoatzin, a Chichimeca convert to Christianity. Speaking in his native Nahuatl tongue, Our Lady identified herself as the Mother of the True God and requested that a temple be erected on the site. When Juan Diego sought the bishop's authorization, Bishop Juan de Zumárraga asked for an indisputable sign of heaven.\n\nOn December 12, 1531, the Virgin instructed Juan Diego to climb the arid, frozen summit of Tepeyac to gather blooming Castilian roses—flowers completely unseasonal to winter Mexico. Juan Diego gathered them into his agave-fiber mantle (*tilma*). When he opened the cloak before Bishop Zumárraga, the roses cascaded to the floor, revealing the full-length celestial portrait of the Virgin Mary miraculously imprinted upon the coarse fabric.\n\nScientific examinations in the 20th and 21st centuries have verified that the cactus-fiber fabric, which normally disintegrates within two decades, remains completely intact after five centuries without paint sizing, brushstrokes, or protective varnish. The image spurred the rapid conversion of over nine million indigenous Americans to the Catholic faith within a single decade, forever bridging the indigenous and European worlds.",
        "historical_summary_vi": "Vào tháng 12 năm 1531, trên đồi Tepeyac phía bắc Thành phố Mexico, Đức Trinh Nữ Maria đã hiện ra bốn lần với Thánh Juan Diego Cuauhtlatoatzin, một người bản địa Chichimeca tân tòng. Bằng ngôn ngữ Nahuatl thổ dân, Đức Mẹ xưng mình là Mẹ của Thiên Chúa Thật và nguyện ước một nguyện đường được xây dựng tại nơi đây. Khi Juan Diego đến trình Đức Giám mục Juan de Zumárraga, ngài đã xin một dấu chỉ siêu nhiên để xác thực.\n\nNgày 12 tháng 12 năm 1531, Đức Mẹ chỉ dẫn Juan Diego leo lên đỉnh đồi Tepeyac băng giá để hái những bông hồng xứ Castille đang nở rộ giữa mùa đông khô cằn. Juan Diego bọc hoa trong chiếc áo choàng bằng sợi xương rồng (*tilma*). Khi mở áo choàng trước mặt Đức Giám mục, những đóa hoa rơi xuống sàn, để lộ hình ảnh Đức Mẹ tuyệt mỹ in đậm trên từng thớ vải thô ráp.\n\nCác cuộc kiểm định khoa học hiện đại xác nhận rằng sợi vải dệt từ cây thùa tự nhiên—vốn sẽ mục nát sau 20 năm—vẫn nguyên vẹn tuyệt hảo suốt 5 thế kỷ mà không hề có dấu vết nét cọ, lớp sơn lót hay hóa chất bảo quản. Phép lạ này đã đưa hơn chín triệu người bản địa gia nhập Giáo hội Công giáo chỉ trong một thập niên, trở thành biểu tượng hiệp nhất đức tin vĩ đại của Châu Mỹ.",
        "scripture_reading": "Revelation 12:1",
        "suggested_prayer_en": "O Holy Virgin of Guadalupe, Mother of the Americas and Star of the New Evangelization, look with maternal tenderness upon our families and nations. As you left your immaculate image upon the humble tilma of Juan Diego, imprint upon our souls the virtues of faith, humility, and steadfast charity. Lead us always to your Divine Son, Jesus Christ, who lives and reigns forever and ever. Amen.",
        "suggested_prayer_vi": "Lạy Đức Mẹ Guadalupe, Quan Thầy Toàn Châu Mỹ và Ngôi Sao của công cuộc Tân Phúc Âm Hóa, xin thương đoái nhìn đến các gia đình và quốc gia chúng con. Như Mẹ đã in dấu thánh nhan Mẹ trên tà áo khiêm nhường của Thánh Juan Diego, xin cũng khắc ghi vào tâm hồn chúng con lòng tin kính sâu xa, đức khiêm nhường và lòng bác ái vững bền. Xin dẫn đưa chúng con đến cùng Con Chí Thánh của Mẹ là Chúa Giêsu Kitô, Đấng hằng sống và hiển trị muôn đời. Amen.",
        "primary_sources": [
            {
                "label": "Nican Mopohua (16th Century Nahuatl Narrative by Antonio Valeriano)",
                "url": "https://www.vatican.va/roman_curia/congregations/csaints/documents/rc_con_csaints_doc_20020731_juan-diego_en.html",
                "type": "vatican"
            },
            {
                "label": "Pontifical Academy of the Immaculate Conception - Tilma Technical Documentation",
                "url": "https://www.catholicnewsagency.com/resource/55416/our-lady-of-guadalupe",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "our_lady_of_lourdes",
        "category": "marian_apparition",
        "name_en": "Sanctuary of Our Lady of Lourdes",
        "name_vi": "Đền Thánh Đức Mẹ Lộ Đức",
        "feast_day_association": "Feast of Our Lady of Lourdes (February 11)",
        "location": {
            "shrine_or_basilica": "Sanctuaire de Notre-Dame de Lourdes (Grotte de Massabielle)",
            "city": "Lourdes",
            "region_or_state": "Hautes-Pyrénées",
            "country": "France",
            "latitude": 43.0975,
            "longitude": -0.0581,
            "precision": "apparition_ground"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1862-01-18",
            "approving_authority": "Bishop Bertrand-Sévère Laurence / Pope Pius IX",
            "confidence": "confirmed",
            "confidence_note_en": "Declared authentic by Bishop Laurence of Tarbes on January 18, 1862, confirming 18 apparitions in 1858; recognized by the Holy See with 70 medically certified miraculous healings validated by the Lourdes International Medical Bureau.",
            "confidence_note_vi": "Được Đức Giám mục Bertrand-Sévère Laurence giáo phận Tarbes công nhận chính thức ngày 18 tháng 1 năm 1862, xác thực 18 lần hiện ra năm 1858; Tòa Thánh đã phê chuẩn và công nhận 70 phép lạ chữa lành y khoa được Hội đồng Y khoa Quốc tế Lộ Đức thẩm định."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Miraculous Spring of Massabielle and Grotto of Apparitions",
                "relic_name_vi": "Suối Nguồn Phép Lạ Massabielle và Hang Đá Hiện Ra",
                "relic_type": "apparition_site",
                "reliquary_location": "Grotte de Massabielle beneath the Basilica of the Immaculate Conception"
            }
        ],
        "historical_summary_en": "Between February 11 and July 16, 1858, the Blessed Virgin Mary appeared eighteen times to fourteen-year-old Bernadette Soubirous at the rock grotto of Massabielle on the banks of the Gave de Pau river. During the ninth apparition on February 25, the Lady instructed Bernadette to dig into the mud and drink from the water that emerged, uncovering a subterranean freshwater spring that flows continuously to this day with documented therapeutic and miraculous properties.\n\nOn March 25, 1858, the Feast of the Annunciation, the Lady revealed her heavenly identity in the local Bigourdan Occitan dialect: *'Que soi era Immaculada Concepcion'* ('I am the Immaculate Conception'). This self-revelation came merely four years after Pope Pius IX defined the dogma of the Immaculate Conception in the Apostolic Constitution *Ineffabilis Deus*, providing a divine seal through an unlettered peasant girl who had never encountered the theological term.\n\nThe Sanctuary of Lourdes has developed into the foremost Marian healing shrine on earth, receiving millions of sick and disabled pilgrims annually. The Lourdes Medical Bureau, operating under stringent empirical criteria, investigates claims of physical healing, verifying complete, spontaneous, and scientifically inexplicable cures.",
        "historical_summary_vi": "Từ ngày 11 tháng 2 đến ngày 16 tháng 7 năm 1858, Đức Trinh Nữ Maria đã hiện ra 18 lần với cô thiếu nữ 14 tuổi Bernadette Soubirous tại hang đá Massabielle bên bờ sông Gave de Pau. Trong lần hiện ra thứ 9 vào ngày 25 tháng 2, Đức Mẹ dạy Bernadette cào đất uống nước bùn, từ đó làm tuôn trào dòng suối nước mát lành liên lỉ cho đến tận ngày nay, mang lại vô số ơn chữa lành thể xác và tâm linh.\n\nNgày 25 tháng 3 năm 1858, vào ngày Lễ Truyền Tin, Đức Mẹ đã mạc khải danh tánh của Mẹ bằng tiếng địa phương Gascon: *'Que soi era Immaculada Concepcion'* ('Ta là Đấng Vô Nhiễm Nguyên Tội'). Lời mạc khải này diễn ra chỉ bốn năm sau khi Đức Giáo hoàng Piô IX công bố tín điều Vô Nhiễm Nguyên Tội qua Tông sắc *Ineffabilis Deus*, trở thành dấu ấn siêu nhiên xác nhận tín điều qua một thiếu nữ mộc mạc chưa từng học thần học.\n\nĐền Thánh Lộ Đức đã trở thành trung tâm hành hương chữa lành lớn nhất thế giới, đón nhận hàng triệu bệnh nhân mỗi năm. Văn phòng Y khoa Quốc tế Lộ Đức áp dụng các tiêu chuẩn khoa học thực nghiệm khắt khe nhất để kiểm chứng các phép lạ chữa lành tức thì, dứt điểm và vượt quá quy luật tự nhiên.",
        "scripture_reading": "Luke 1:28",
        "suggested_prayer_en": "O Ever-Immaculate Virgin Mary, Mother of Mercy and Health of the Sick, you chose the humble grotto of Lourdes to manifest the glory of your Conception and the healing grace of your Son. Look upon our infirmities of body and soul; wash us in the cleansing waters of repentance, and obtain for us the strength to embrace the cross with joyful fidelity. Through Jesus Christ our Lord. Amen.",
        "suggested_prayer_vi": "Lạy Đức Trinh Nữ Maria Vô Nhiễm Nguyên Tội, Mẹ Lòng Thương Xót và là Đấng Cứu Giúp các bệnh nhân, Mẹ đã chọn hang đá khiêm hạ Lộ Đức để tỏ bày vinh quang và ân sủng chữa lành của Con Mẹ. Xin đoái nhìn đến những yếu đuối tật nguyền nơi thân xác và tâm hồn chúng con; xin thanh tẩy chúng con trong dòng nước sám hối và ban cho chúng con lòng can đảm vác thánh giá theo Chúa trọn đời. Nhờ Đức Giêsu Kitô, Chúa chúng con. Amen.",
        "primary_sources": [
            {
                "label": "Lourdes Medical Bureau (Bureau des Constatations Médicales) Official Archives",
                "url": "https://www.lourdes-france.org/en/miraculous-cures/",
                "type": "academic"
            },
            {
                "label": "Pope Pius XII - Encyclical Le Pèlerinage de Lourdes (1957)",
                "url": "https://www.vatican.va/content/pius-xii/en/encyclicals/documents/hf_p-xii_enc_02071957_le-pelerinage-de-lourdes.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "our_lady_of_fatima",
        "category": "marian_apparition",
        "name_en": "Sanctuary of Our Lady of Fátima",
        "name_vi": "Đền Thánh Đức Mẹ Fátima",
        "feast_day_association": "Feast of Our Lady of Fátima (May 13)",
        "location": {
            "shrine_or_basilica": "Santuário de Nossa Senhora do Rosário de Fátima (Cova da Iria)",
            "city": "Fátima",
            "region_or_state": "Santarém",
            "country": "Portugal",
            "latitude": 39.6321,
            "longitude": -8.6738,
            "precision": "apparition_ground"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1930-10-13",
            "approving_authority": "Bishop José Alves Correia da Silva / Pope Pius XI",
            "confidence": "confirmed",
            "confidence_note_en": "Officially approved by Bishop da Silva of Leiria on October 13, 1930; elevated to Papal status by subsequent pontiffs; canonization of visionary shepherds Francisco and Jacinta Marto by Pope Francis in 2017.",
            "confidence_note_vi": "Được Đức Giám mục José Alves Correia da Silva giáo phận Leiria phê chuẩn chính thức ngày 13 tháng 10 năm 1930; Đức Giáo hoàng Phanxicô đã tuyên thánh cho hai thị nhân Francisco và Jacinta Marto vào năm 2017."
        },
        "primary_relics": [
            {
                "relic_name_en": "Tombs of Saints Francisco and Jacinta Marto and Servant of God Sister Lúcia dos Santos",
                "relic_name_vi": "Lăng Mộ Hai Thánh Trẻ Francisco, Jacinta Marto và Đấng Đáng Kính Nữ Tu Lúcia",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Inside the Basilica of Our Lady of the Rosary of Fátima"
            }
        ],
        "historical_summary_en": "From May 13 to October 13, 1917, against the backdrop of the First World War and the impending Bolshevik Revolution, the Blessed Virgin Mary appeared six times to three young shepherd children—Lúcia dos Santos (age 10) and her cousins Francisco (age 9) and Jacinta Marto (age 7)—at the Cova da Iria near Fátima, Portugal. Our Lady requested daily recitation of the Holy Rosary for world peace, devotion to her Immaculate Heart, and reparation for sins.\n\nDuring her final apparition on October 13, 1917, the 'Miracle of the Sun' (*O Milagre do Sol*) occurred before a crowd of over 70,000 witnesses, including secular journalists, freethinkers, and scientists. Following torrential rains, the sun emerged as an opaque rotating disc in the sky, cast multicoloured shafts of light across the landscape, and plunged precipitously toward the earth before returning to its normal orbit, instantly drying the drenched ground and clothes of the crowd.\n\nThe message of Fátima included prophetic revelations concerning the end of World War I, the rise of totalitarian communism in Russia, the persecution of the Church, and the assassination attempt against Pope John Paul II on May 13, 1981, which the Pope attributed entirely to the maternal hand of Our Lady of Fátima.",
        "historical_summary_vi": "Từ ngày 13 tháng 5 đến ngày 13 tháng 10 năm 1917, giữa bối cảnh Thế chiến thứ nhất tàn khốc, Đức Trinh Nữ Maria đã hiện ra 6 lần với ba trẻ chăn chiên—Lúcia dos Santos (10 tuổi) cùng hai em họ Francisco (9 tuổi) và Jacinta Marto (7 tuổi)—tại đồi Cova da Iria, Fátima, Bồ Đào Nha. Đức Mẹ tha thiết kêu gọi lần chuỗi Mân Côi mỗi ngày để cầu nguyện cho hòa bình thế giới, tôn sùng Trái Tim Vô Nhiễm Mẹ và làm việc đền tạ tội lỗi.\n\nTrong lần hiện ra cuối cùng ngày 13 tháng 10 năm 1917, 'Phép lạ Mặt Trời Nhảy Múa' đã diễn ra trước sự chứng kiến của hơn 70.000 người thuộc mọi thành phần xã hội, gồm cả các ký giả vô thần và các nhà khoa học. Sau cơn mưa tầm tã, mặt trời xoay tròn như một bánh xe lửa, tỏa muôn luồng ánh sáng rực rỡ và lao thẳng xuống đất trước khi trở lại quỹ đạo bình thường, làm khô ráo hoàn toàn y phục và mặt đất lầy lội trong chớp mắt.\n\nSứ điệp Fátima chứa đựng các mạc khải tiên tri về sự kết thúc Thế chiến I, sự bành trướng của chủ nghĩa cộng sản vô thần tại Nga, các cuộc bách hại Giáo hội, và biến cố Đức Giáo hoàng Gioan Phaolô II bị ám sát ngày 13 tháng 5 năm 1981, điều mà Đức Giáo hoàng luôn xác quyết rằng chính bàn tay Đức Mẹ Fátima đã cứu sống ngài.",
        "scripture_reading": "Luke 1:46-55",
        "suggested_prayer_en": "O Most Holy Virgin Mary, Queen of the Holy Rosary and Refuge of Sinners, you revealed at Fátima the path of conversion, reparation, and peace for a troubled world. Grant us the grace to consecrate our hearts entirely to your Immaculate Heart, to pray your Rosary with devotion, and to offer our daily trials for the salvation of souls. Through Jesus Christ our Lord. Amen.",
        "suggested_prayer_vi": "Lạy Mẹ Maria, Nữ Vương Rất Thánh Mân Côi và là Nơi Trú Ẩn của các tội nhân, Mẹ đã mạc khải tại Fátima con đường hoán cải, đền tạ và hòa bình cho toàn nhân loại. Xin ban ơn giúp chúng con biết tận hiến trọn vẹn cho Trái Tim Vô Nhiễm Mẹ, siêng năng lần chuỗi Mân Côi và hiến dâng những hy sinh hằng ngày để mưu ích cho phần rỗi các linh hồn. Nhờ Đức Giêsu Kitô, Chúa chúng con. Amen.",
        "primary_sources": [
            {
                "label": "Congregation for the Doctrine of the Faith - The Message of Fatima (Cardinal Joseph Ratzinger)",
                "url": "https://www.vatican.va/roman_curia/congregations/cfaith/documents/rc_con_cfaith_doc_20000626_message-fatima_en.html",
                "type": "vatican"
            },
            {
                "label": "Official Shrine of Fatima Historical Archives (Santuário de Fátima)",
                "url": "https://www.fatima.pt/en",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "holy_house_of_loreto",
        "category": "marian_apparition",
        "name_en": "Basilica of the Holy House of Loreto",
        "name_vi": "Đại Vương Cung Thánh Đường Nhà Thánh Loreto",
        "feast_day_association": "Feast of Our Lady of Loreto (December 10)",
        "location": {
            "shrine_or_basilica": "Pontificia Basilica Minore della Santa Casa di Loreto",
            "city": "Loreto",
            "region_or_state": "Ancona, Marche",
            "country": "Italy",
            "latitude": 43.4410,
            "longitude": 13.6105,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1310-01-01",
            "approving_authority": "Pope Clement V / Pope John Paul II (Apostolic Letter 1994)",
            "confidence": "confirmed",
            "confidence_note_en": "Supported by continuous papal bulls since Clement V (1310) and archaeological surveys by Fr. Bellarmino Bagatti confirming stones, mortar, and graffiti matching the 1st-century Grotto of the Annunciation in Nazareth.",
            "confidence_note_vi": "Được chuẩn nhận qua nhiều Tông sắc của các Đức Giáo hoàng từ thời Clêmentê V (1310); các cuộc khảo cổ học của Cha Bellarmino Bagatti xác nhận cấu trúc đá, vữa và ký tự khắc trên đá hoàn toàn trùng khớp với Hang Đá Truyền Tin thế kỷ thứ nhất tại Nazareth."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Three Stone Walls of the Holy House of the Annunciation",
                "relic_name_vi": "Ba Bức Tường Đá Thánh của Ngôi Nhà Truyền Tin Nazareth",
                "relic_type": "holy_icon",
                "reliquary_location": "Enclosed within the Marble Screen designed by Bramante inside the Basilica"
            }
        ],
        "historical_summary_en": "According to ancient Catholic tradition, the Holy House of Loreto is the earthly dwelling in Nazareth where the Virgin Mary was born, raised, and received the Annunciation of the Archangel Gabriel, and where the Word became Flesh (*Verbum Caro Factum Est*). Following the fall of the Crusader Kingdom of Jerusalem in 1291, historical documents—specifically the *Chartularium Culisanense* of 1294—record that the stone structure was carefully dismantled and transported from Palestine to Illyria (Trsat, Croatia) and subsequently to the shores of the Marche in Italy by the noble Byzantine family named De Angelis (Angeli).\n\nArchaeological and mineralogical investigations led by Franciscan biblical scholar Bellarmino Bagatti in the 1960s confirmed that the three walls consist of Nabataean limestone cut with ancient techniques and bonded by mortar composed of chemical elements native to the Levant, entirely unknown to medieval central Italy. Furthermore, graffiti scratched into the stones contains Nabataean-Greek monograms identical to those excavated beneath the Basilica of the Annunciation in Nazareth.\n\nThe Holy House stands today enveloped by a masterpiece of Italian Renaissance marble relief designed by Donato Bramante and executed by Sansovino and Sangallo. It has been venerated by hundreds of saints and pontiffs as the sanctified cradle of the Incarnation.",
        "historical_summary_vi": "Theo truyền thống thánh thiêng của Giáo hội, Nhà Thánh Loreto chính là căn nhà tại Nazareth nơi Đức Trinh Nữ Maria sinh trưởng, đón nhận lời Truyền Tin của Sứ thần Gabriel và là nơi Ngôi Lời đã Nhập Thể làm Người (*Verbum Caro Factum Est*). Sau khi Vương quốc Thập Tự Quân sụp đổ năm 1291, các văn thư lịch sử (đặc biệt là *Chartularium Culisanense* năm 1294) ghi nhận các phiến đá của ngôi nhà đã được tháo dỡ và chuyên chở từ Đất Thánh sang Illyria (Croatia) rồi cập bến Loreto, nước Ý bởi gia tộc quý tộc Byzantine mang họ De Angelis (các Thiên Thần).\n\nCác cuộc khảo cứu khảo cổ học và khoáng vật học do linh mục học giả Phanxicô Bellarmino Bagatti thực hiện thập niên 1960 xác nhận rằng ba bức tường gồm các khối đá vôi kiểu Nabataean kết dính bằng loại vữa chỉ có ở vùng Trung Đông, hoàn toàn không hiện diện tại nước Ý thời Trung Cổ. Hơn thế nữa, các ký tự Hy Lạp-Aramaic khắc trên đá hoàn toàn trùng khớp với các di chỉ được khai quật tại Vương cung Thánh đường Truyền Tin ở Nazareth.\n\nNgôi Nhà Thánh ngày nay được bao bọc bởi lớp phù điêu cẩm thạch tuyệt tác thời Phục Hưng do danh họa Donato Bramante thiết kế, là nơi hành hương chiêm niệm mầu nhiệm Nhập Thể được vô số vị Thánh và Giáo hoàng tôn kính.",
        "scripture_reading": "John 1:14",
        "suggested_prayer_en": "O Lord God Almighty, who in your unfathomable mercy consecrated the dwelling of the Blessed Virgin Mary by the Incarnation of your Word, grant that through the intercession of Our Lady of Loreto, our homes may become sanctuaries of faith, pure love, and humble obedience to your Holy Will. Through the same Christ our Lord. Amen.",
        "suggested_prayer_vi": "Lạy Thiên Chúa Toàn Năng, Đấng đã thánh hóa ngôi nhà của Đức Trinh Nữ Maria qua mầu nhiệm Ngôi Lời Nhập Thể, xin nhờ lời chuyển cầu của Đức Mẹ Loreto, biến đổi gia đình chúng con thành đền thánh của đức tin, tình yêu tinh tuyền và sự vâng phục thánh ý Chúa trong khiêm hạ. Nhờ Đức Kitô, Chúa chúng con. Amen.",
        "primary_sources": [
            {
                "label": "Pope John Paul II - Letter for the Seventh Centenary of the Shrine of Loreto (1993)",
                "url": "https://www.vatican.va/content/john-paul-ii/it/letters/1993/documents/hf_jp-ii_let_19930815_loreto.html",
                "type": "vatican"
            },
            {
                "label": "Sanctuary of the Holy House of Loreto - Historical & Archaeological Dossier",
                "url": "https://www.santuarioloreto.va/en.html",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "our_lady_of_czestochowa",
        "category": "marian_apparition",
        "name_en": "Jasna Góra Monastery - Our Lady of Częstochowa",
        "name_vi": "Tu Viện Jasna Góra - Đức Mẹ Częstochowa",
        "feast_day_association": "Feast of Our Lady of Częstochowa (August 26)",
        "location": {
            "shrine_or_basilica": "Sanktuarium Matki Bożej Częstochowskiej na Jasnej Górze",
            "city": "Częstochowa",
            "region_or_state": "Silesian Voivodeship",
            "country": "Poland",
            "latitude": 50.8126,
            "longitude": 19.0971,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1717-09-08",
            "approving_authority": "Pope Clement XI (Papal Coronation) / Paulite Order",
            "confidence": "confirmed",
            "confidence_note_en": "Coronated with papal crowns by Pope Clement XI in 1717; declared Queen and Protector of Poland by King John Casimir in the Lwów Oath (1656); deeply venerated by Pope Saint John Paul II.",
            "confidence_note_vi": "Được Đức Giáo hoàng Clêmentê XI đội triều thiên vàng năm 1717; Vua John Casimir đã tuyên thệ tôn phong Đức Mẹ là Nữ Vương và Đấng Bảo Trợ Ba Lan tại Lwów năm 1656; là trung tâm linh đạo sùng kính của Thánh Giáo hoàng Gioan Phaolô II."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Miraculous Icon of the Black Madonna of Częstochowa",
                "relic_name_vi": "Linh Ảnh Phép Lạ Đức Mẹ Đen Częstochowa",
                "relic_type": "holy_icon",
                "reliquary_location": "Chapel of the Miraculous Image at Jasna Góra Monastery"
            }
        ],
        "historical_summary_en": "The Holy Icon of Our Lady of Częstochowa, traditionally attributed to Saint Luke the Evangelist painting upon a cypress wood table top from the Holy Family's home in Nazareth, was brought to the Jasna Góra ('Luminous Mount') Paulite monastery in 1382 by Prince Władysław of Opole. The icon depicts the Hodegetria ('She who shows the Way'), with the Virgin directing the faithful's gaze to the Christ Child held in her left arm.\n\nIn 1430, Hussite iconoclasts raided the sanctuary, striking the Madonna's cheek twice with a saber; miraculous traditions record that blood welled from the wood before the blade broke, leaving permanent scars that successive restorations intentionally preserved. During the Swedish Deluge of 1655, a small garrison of 70 Paulite monks and 160 soldiers successfully defended Jasna Góra against a siege of over 4,000 Swedish invaders, an event that transformed the shrine into the spiritual citadel of Polish national sovereignty.\n\nUnder Soviet communist occupation, the Black Madonna became the banner of non-violent spiritual resistance led by Cardinal Stefan Wyszyński and Cardinal Karol Wojtyła (Pope John Paul II), culminating in the Solidarity movement and the spiritual revival of Eastern Europe.",
        "historical_summary_vi": "Linh ảnh Thánh Đức Mẹ Częstochowa, theo truyền thống được chính Thánh Sử Luca vẽ trên mặt bàn gỗ trắc bá tại tư gia Thánh Gia ở Nazareth, đã được Hoàng tử Władysław vùng Opole rước về tu viện các cha dòng Thánh Phaolô Ẩn Tu tại Jasna Góra ('Núi Sáng') vào năm 1382. Bức linh ảnh thuộc thể loại Hodegetria ('Đấng Chỉ Đường'), trong đó Đức Mẹ ẵm Chúa Hài Đồng bên tay trái và hướng mọi ánh nhìn về Người.\n\nNăm 1430, nhóm cướp Hussite đã xông vào đền thánh và dùng gươm chém hai nhát sâu vào gò má Đức Mẹ; truyền tụng ghi lại máu đã rỉ ra từ vết chém khiến lưỡi gươm gãy vụn, để lại hai vết sẹo không thể xóa nhòa qua các lần phục chế. Năm 1655, trong cuộc xâm lược của quân Thụy Điển, 70 tu sĩ dòng Phaolô cùng 160 binh lính đã kiên cường bảo vệ đền thánh đẩy lùi hơn 4.000 quân xâm lược, đưa Jasna Góra trở thành thành lũy tâm linh bảo vệ nền độc lập của Ba Lan.\n\nTrong thời kỳ bách hại đức tin dưới chế độ độc tài thế kỷ 20, Linh ảnh Đức Mẹ Đen là ngọn cờ quy tụ sức mạnh phản kháng bất bạo động dưới sự lãnh đạo của Đức Hồng y Stefan Wyszyński và Đức Hồng y Karol Wojtyła (sau là Thánh Giáo hoàng Gioan Phaolô II), khơi nguồn cho phong trào Công đoàn Đoàn kết và sự hồi sinh đức tin tại Đông Âu.",
        "scripture_reading": "John 19:26-27",
        "suggested_prayer_en": "O Queen of Poland and Mother of the Church, Black Madonna of Jasna Góra, you bear upon your countenance the scars of suffering yet radiate the unconquerable light of Christ. Guard our families, sustain nations facing oppression, and teach us to remain steadfast in fidelity to the Cross and the Gospel. Through Christ our Lord. Amen.",
        "suggested_prayer_vi": "Lạy Nữ Vương Ba Lan và là Mẹ Hội Thánh, Đức Mẹ Đen Jasna Góra, Mẹ mang trên khuôn mặt thánh thiện những vết thương đau khổ nhưng vẫn tỏa rạng ánh sáng khải hoàn của Chúa Kitô. Xin bảo vệ các gia đình chúng con, nâng đỡ các dân tộc đang chịu thử thách bách hại và dạy chúng con luôn kiên trung theo Chúa đến cùng dưới bóng Thánh Giá. Nhờ Đức Kitô, Chúa chúng con. Amen.",
        "primary_sources": [
            {
                "label": "Jasna Góra Paulite Monastery Official Historical Archive",
                "url": "https://jasnagora.pl/en/",
                "type": "academic"
            },
            {
                "label": "Pope John Paul II - Homily at Jasna Góra Shrine (June 4, 1979)",
                "url": "https://www.vatican.va/content/john-paul-ii/en/homilies/1979/documents/hf_jp-ii_hom_19790604_polonia-jasna-gora.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "our_lady_of_aparecida",
        "category": "marian_apparition",
        "name_en": "National Sanctuary of Our Lady of Aparecida",
        "name_vi": "Vương Cung Thánh Đường Đức Mẹ Aparecida",
        "feast_day_association": "Feast of Our Lady of Aparecida (October 12)",
        "location": {
            "shrine_or_basilica": "Santuário Nacional de Nossa Senhora da Conceição Aparecida",
            "city": "Aparecida",
            "region_or_state": "São Paulo",
            "country": "Brazil",
            "latitude": -22.8497,
            "longitude": -45.2338,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1904-09-08",
            "approving_authority": "Pope Saint Pius X (Papal Decree) / Consecrated by Pope John Paul II (1980)",
            "confidence": "confirmed",
            "confidence_note_en": "Papal coronation granted by Pope Pius X in 1904; declared Principal Patroness of Brazil by Pope Pius XI in 1930; Basilica consecrated in person by Pope John Paul II on July 4, 1980.",
            "confidence_note_vi": "Được Đức Thánh Cha Piô X ban sắc lệnh đội triều thiên năm 1904; Đức Giáo hoàng Piô XI tuyên phong là Đấng Bảo Trợ Nước Brazil năm 1930; Vương Cung Thánh Đường được chính Đức Gioan Phaolô II cung hiến ngày 4 tháng 7 năm 1980."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Miraculous Terracotta Statue of the Immaculate Conception",
                "relic_name_vi": "Tượng Phép Lạ Mẹ Vô Nhiễm Nguyên Tội Bằng Đất Nung",
                "relic_type": "holy_icon",
                "reliquary_location": "Niche of Gold and Bulletproof Crystal in the Main Transept"
            }
        ],
        "historical_summary_en": "In October 1717, three impoverished fishermen—Domingos Garcia, João Alves, and Filipe Pedroso—were tasked with procuring fish from the Paraíba do Sul river for the banquet of the Count of Assumar, Governor of São Paulo. After hours of fruitless casting, João Alves cast his net and retrieved the headless terracotta body of a small statue of Our Lady of the Immaculate Conception. Casting his net a second time, he pulled up the missing head, which perfectly fit the torso.\n\nUpon reassembling the small blackened statue, the fishermen cast their nets once more and were overwhelmed by an unprecedented catch that threatened to sink their boats. The devotion grew rapidly in Pedroso's family chapel as candles miraculously rekindled themselves during prayers and enslaved people praying before the image experienced liberation from chains.\n\nThe Basilica of Aparecida, constructed between 1955 and 1980, is the second-largest Catholic church in the world after Saint Peter's Basilica in Rome, hosting over twelve million pilgrims each year and serving as the vibrant spiritual heart of Latin American Catholicism.",
        "historical_summary_vi": "Vào tháng 10 năm 1717, ba người ngư dân nghèo—Domingos Garcia, João Alves và Filipe Pedroso—được giao nhiệm vụ đánh bắt cá trên sông Paraíba do Sul để chuẩn bị yến tiệc đón Bá tước Assumar, Thống đốc vùng São Paulo. Sau nhiều giờ kéo lưới không được một con cá nào, João Alves quăng mẻ lưới mới và vớt được phần thân bằng đất nung bị mất đầu của một bức tượng Đức Mẹ Vô Nhiễm. Quăng lưới lần thứ hai, ông vớt được phần đầu tượng và khi ghép lại thì vừa khít hoàn hảo.\n\nSau khi kính cẩn hợp nhất pho tượng nhỏ sẫm màu, các ngư dân lại buông lưới và lập tức kéo lên được lượng cá nhiều đến mức thuyền suýt chìm. Lòng tôn sùng lan tỏa nhanh chóng tại nguyện đường gia đình Pedroso với những ngọn nến tự bừng sáng trong lúc cầu nguyện và những người nô lệ được giải thoát khỏi xiềng xích khi quỳ gối khẩn cầu trước tượng Mẹ.\n\nVương Cung Thánh Đường Aparecida, được xây dựng từ năm 1955 đến 1980, là thánh đường Công giáo lớn thứ hai trên thế giới chỉ sau Đền Thờ Thánh Phêrô tại Roma, đón tiếp hơn 12 triệu khách hành hương mỗi năm và là trái tim tâm linh rực rỡ của Giáo hội Mỹ Latinh.",
        "scripture_reading": "Luke 5:4-7",
        "suggested_prayer_en": "O Lady Aparecida, Queen and Patroness of Brazil, who revealed your maternal favor to humble fishermen in their hour of need, cast your merciful eyes upon all who struggle in poverty, affliction, or spiritual darkness. Bring abundance to our spiritual nets and draw all nations into the unity of your Son's Kingdom. Through Jesus Christ our Lord. Amen.",
        "suggested_prayer_vi": "Lạy Đức Mẹ Aparecida, Nữ Vương và Đấng Bảo Trợ nước Brazil, Mẹ đã tỏ bày tình mẫu tử dịu hiền cho những người dân chài nghèo khổ trong lúc gian nan, xin đoái nhìn đến tất cả những ai đang chịu thử thách vì nghèo đói, đau thương hay tăm tối linh hồn. Xin làm cho mẻ lưới thiêng liêng của chúng con được đầy tràn ân sủng và dẫn đưa muôn dân về trong Nước Con Chí Thánh của Mẹ. Nhờ Đức Giêsu Kitô, Chúa chúng con. Amen.",
        "primary_sources": [
            {
                "label": "National Sanctuary of Aparecida Official Archival History",
                "url": "https://www.a12.com/santuario",
                "type": "academic"
            },
            {
                "label": "Pope Francis - Homily at the Basilica of the Shrine of Our Lady of Aparecida (July 24, 2013)",
                "url": "https://www.vatican.va/content/francesco/en/homilies/2013/documents/papa-francesco_20130724_gmg-omelia-aparecida.html",
                "type": "vatican"
            }
        ]
    }
]

BATCH_2 = [
    {
        "sanctuary_id": "our_lady_of_knock",
        "category": "marian_apparition",
        "name_en": "Sanctuary of Our Lady of Knock",
        "name_vi": "Đền Thánh Đức Mẹ Knock",
        "feast_day_association": "Feast of Our Lady of Knock (August 17)",
        "location": {
            "shrine_or_basilica": "Knock Shrine (Basilica of Our Lady, Queen of Ireland)",
            "city": "Knock",
            "region_or_state": "County Mayo",
            "country": "Ireland",
            "latitude": 53.7915,
            "longitude": -8.9174,
            "precision": "apparition_ground"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1879-10-08",
            "approving_authority": "Archbishop John MacHale / Pope John Paul II (Golden Rose 1979) / Pope Francis (International Sanctuary 2021)",
            "confidence": "confirmed",
            "confidence_note_en": "Formally examined by the Diocesan Commission of Inquiry in 1879 and 1936, confirming fifteen eyewitness testimonies; designated an International Eucharistic and Marian Sanctuary by Pope Francis in 2021.",
            "confidence_note_vi": "Được Hội đồng Điều tra Giáo phận thẩm định năm 1879 và 1936, xác nhận lời chứng của 15 nhân chứng tận mắt; được Đức Giáo hoàng Phanxicô nâng lên hàng Đền thánh Quốc tế Thánh Thể và Thánh Mẫu năm 2021."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Apparition Gable Wall of Saint John the Baptist Church",
                "relic_name_vi": "Bức Tường Đầu Hồi Nơi Đức Mẹ Hiện Ra tại Nhà Thờ Thánh Gioan Baotixita",
                "relic_type": "apparition_site",
                "reliquary_location": "Enclosed within the Apparition Chapel at Knock Shrine"
            }
        ],
        "historical_summary_en": "On the torrential evening of August 21, 1879, a silent, celestial apparition took place at the southern gable of Saint John the Baptist Church in the small village of Knock, County Mayo. Fifteen witnesses aged between 5 and 74 gazed for two hours in pouring rain at a radiant manifestation: the Blessed Virgin Mary clothed in white robes and a golden crown, Saint Joseph bowing reverently toward her, Saint John the Evangelist vested as a bishop holding a book of Gospels, and to their left, a plain altar upon which stood a young Lamb surrounded by angels and an upright Cross.\n\nRemarkably, unlike other Marian apparitions, no spoken words were uttered by the heavenly figures, and the ground directly beneath the gable wall remained completely dry throughout the heavy downpour. The apparition occurred during a period of immense national trauma in Ireland, marked by the Great Famine's aftermath, the Land Wars, and mass emigration.\n\nThe silent, Eucharistic-centered apparition conveyed a profound message of solidarity and hope: the Lamb of God sacrificed upon the altar remains the eternal source of consolation. Knock has received visits from Pope John Paul II (1979), Mother Teresa of Calcutta (1993), and Pope Francis (2018).",
        "historical_summary_vi": "Vào buổi chiều tối mưa bão ngày 21 tháng 8 năm 1879, một biến cố hiện ra trong thinh lặng thánh thiện đã xảy ra tại bức tường đầu hồi phía nam nhà thờ Thánh Gioan Baotixita ở ngôi làng nhỏ Knock, Quận Mayo. Mười lăm nhân chứng tuổi từ 5 đến 74 đã chiêm ngắm suốt hai tiếng đồng hồ dưới cơn mưa như trút nước một cảnh tượng rực rỡ: Đức Trinh Nữ Maria mặc áo trắng đội triều thiên vàng, Thánh Giuse cúi mình cung kính về phía Mẹ, Thánh Sử Gioan trong phẩm phục giám mục tay cầm sách Phúc Âm, và bên cạnh là một bàn thờ có Chiên Con đứng trước Thánh Giá uy nghi giữa các thiên thần bay lượn.\n\nKhác biệt với các cuộc hiện ra khác, các đấng thánh hoàn toàn thinh lặng không thốt nên lời, và nền đất dưới chân tường đầu hồi hoàn toàn khô ráo mặc cho mưa bão xung quanh. Biến cố diễn ra đúng vào thời kỳ dân tộc Ireland gánh chịu hậu quả nặng nề của nạn đói, khủng hoảng ruộng đất và làn sóng di cư ồ ạt.\n\nSứ điệp thinh lặng đặt trung tâm vào Hy tế Thánh Thể đã mang lại niềm hy vọng và an ủi vô biên: Chiên Thiên Chúa hiến tế trên bàn thờ là nguồn ơn cứu chuộc bất diệt. Đền thánh đã vinh dự đón tiếp Thánh Giáo hoàng Gioan Phaolô II (1979), Mẹ Thánh Teresa Calcutta (1993) và Đức Giáo hoàng Phanxicô (2018).",
        "scripture_reading": "John 1:29",
        "suggested_prayer_en": "O Lady of Knock, Queen of Ireland and Comfort of the Afflicted, you stood in silent prayer at the foot of the Lamb of God. In the storms and silent trials of our lives, teach us to contemplate the sacred mystery of the Eucharist with profound adoration and unwavering faith. Guide our hearts into the peace of Christ. Amen.",
        "suggested_prayer_vi": "Lạy Đức Mẹ Knock, Nữ Vương nước Ireland và là Nguồn An Ủi kẻ âu lo, Mẹ đã đứng trong sự thinh lặng cầu nguyện dưới chân Chiên Thiên Chúa. Giữa những giông bão và thử thách âm thầm của cuộc đời, xin dạy chúng con biết chiêm ngắm mầu nhiệm Thánh Thể với lòng cung kính sâu xa và đức tin kiên vững. Xin dẫn dắt tâm hồn chúng con vào bình an của Chúa Kitô. Amen.",
        "primary_sources": [
            {
                "label": "Knock Shrine Official Commission of Inquiry Records (1879 & 1936)",
                "url": "https://www.knockshrine.ie/history/",
                "type": "academic"
            },
            {
                "label": "Pope Francis - Message on Elevation of Knock to International Sanctuary (March 19, 2021)",
                "url": "https://www.vatican.va/content/francesco/en/messages/pont-messages/2021/documents/papa-francesco_20210319_messaggio-santuario-knock.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "our_lady_of_walsingham",
        "category": "marian_apparition",
        "name_en": "Catholic National Shrine of Our Lady of Walsingham",
        "name_vi": "Đền Thánh Quốc Gia Đức Mẹ Walsingham",
        "feast_day_association": "Feast of Our Lady of Walsingham (September 24)",
        "location": {
            "shrine_or_basilica": "Basilica of Our Lady of Walsingham (Slipper Chapel)",
            "city": "Walsingham",
            "region_or_state": "Norfolk",
            "country": "United Kingdom",
            "latitude": 52.8943,
            "longitude": 0.8741,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1061-01-01",
            "approving_authority": "Papal Bull of Pope Urban VI / Rescript of Pope Leo XIII (1897)",
            "confidence": "confirmed",
            "confidence_note_en": "Venerated since the vision of Richeldis de Faverches in 1061; restored as England's National Catholic Shrine under Pope Leo XIII in 1897 and elevated to Minor Basilica by Pope Francis in 2015.",
            "confidence_note_vi": "Được tôn kính từ thị kiến của bà Richeldis de Faverches năm 1061; được Đức Giáo hoàng Lêô XIII phục hồi thành Đền thánh Quốc gia Công giáo Anh năm 1897 và Đức Giáo hoàng Phanxicô nâng lên hàng Tiểu Vương Cung Thánh Đường năm 2015."
        },
        "primary_relics": [
            {
                "relic_name_en": "The 14th-Century Slipper Chapel and Restored Holy House",
                "relic_name_vi": "Nguyện Đường Chiếc Hài Thế Kỷ 14 và Nhà Thánh Nazareth Phục Hồi",
                "relic_type": "apparition_site",
                "reliquary_location": "Slipper Chapel Sanctuary, Houghton St Giles, Walsingham"
            }
        ],
        "historical_summary_en": "In the year 1061, a Saxon noblewoman named Richeldis de Faverches experienced three mystical visions in which the Blessed Virgin Mary took her in spirit to Nazareth to show her the house where the Annunciation occurred. Our Lady instructed Richeldis to build an exact replica of the Holy House in Walsingham, Norfolk, so that all who visited could experience the joy of Mary's *Fiat* and the mystery of the Incarnation.\n\nWalsingham swiftly grew into one of medieval Christendom's four greatest pilgrimage destinations alongside Jerusalem, Rome, and Santiago de Compostela, earning England the title 'Our Lady's Dowry' (*Dos Mariae*). Every monarch from Henry III to Henry VIII made pilgrimages on foot to the shrine, famously removing their shoes at the Slipper Chapel (one mile away) to complete the journey barefoot.\n\nIn 1538, during the English Reformation under King Henry VIII, the shrine and priory were dissolved and the miraculous statue was brought to London to be publicly burned. In 1897, Pope Leo XIII authorized the restoration of the shrine at the surviving 14th-century Slipper Chapel, re-establishing Walsingham as a vital beacon of reconciliation, prayer, and Catholic renewal in Britain.",
        "historical_summary_vi": "Vào năm 1061, một nữ quý tộc Saxon tên là Richeldis de Faverches đã nhận ba thị kiến thần bí trong đó Đức Mẹ đưa tâm hồn bà đến Nazareth để chiêm ngắm ngôi nhà nơi diễn ra biến cố Truyền Tin. Đức Mẹ truyền dạy bà xây dựng một bản sao Nhà Thánh Nazareth tại Walsingham, hạt Norfolk, để mọi người đến kính viếng có thể cảm nhận niềm hân hoan của lời xin vâng *Fiat* và mầu nhiệm Nhập Thể.\n\nWalsingham nhanh chóng trở thành một trong bốn trung tâm hành hương vĩ đại nhất của Kitô giáo thời Trung Cổ cùng với Jerusalem, Roma và Santiago de Compostela, đem lại cho nước Anh danh hiệu cao quý 'Của Hồi Môn của Đức Mẹ' (*Dos Mariae*). Mọi vị vua Anh từ Henry III đến Henry VIII đều đi chân trần hành hương đến đền thánh, cởi hài tại Nguyện đường Chiếc Hài (cách đó một dặm) để tiến vào nơi thánh.\n\nNăm 1538, trong cuộc Cải cách dưới thời Henry VIII, tu viện bị triệt phá và tượng Đức Mẹ bị đưa về London thiêu hủy. Đến năm 1897, Đức Giáo hoàng Lêô XIII đã phê chuẩn việc tái lập đền thánh tại Nguyện đường Chiếc Hài thế kỷ 14 còn nguyên vẹn, đưa Walsingham trở lại thành biểu tượng hiệp nhất, cầu nguyện và hồi sinh đức tin Công giáo tại Vương quốc Anh.",
        "scripture_reading": "Luke 1:38",
        "suggested_prayer_en": "All holy and ever-living God, who in the Annunciation of the Blessed Virgin Mary willed that your Word should take flesh in human weakness, grant that through the intercession of Our Lady of Walsingham, England and all nations may rediscover the joy of the Gospel and walk in peace and fraternal charity. Through Christ our Lord. Amen.",
        "suggested_prayer_vi": "Lạy Thiên Chúa Hằng Sống Toàn Năng, Đấng đã muốn Ngôi Lời Nhập Thể trong thân phận yếu đuối của con người nơi biến cố Truyền Tin cho Đức Trinh Nữ Maria, xin nhờ lời chuyển cầu của Đức Mẹ Walsingham, giúp các dân tộc tái khám phá niềm vui của Tin Mừng và bước đi trong bình an, bác ái huynh đệ. Nhờ Đức Kitô, Chúa chúng con. Amen.",
        "primary_sources": [
            {
                "label": "Catholic National Shrine of Our Lady of Walsingham Official Archives",
                "url": "https://www.walsingham.org.uk/history/",
                "type": "academic"
            },
            {
                "label": "Pope Francis - Decree of Minor Basilica for Walsingham Slipper Chapel (2015)",
                "url": "https://www.cbcew.org.uk/walsingham-shrine-granted-minor-basilica-status/",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "our_lady_of_the_pillar",
        "category": "marian_apparition",
        "name_en": "Cathedral-Basilica of Our Lady of the Pillar",
        "name_vi": "Đại Vương Cung Thánh Đường Đức Mẹ Trụ Cột",
        "feast_day_association": "Solemnity of Our Lady of the Pillar (October 12)",
        "location": {
            "shrine_or_basilica": "Catedral-Basílica de Nuestra Señora del Pilar",
            "city": "Zaragoza",
            "region_or_state": "Aragon",
            "country": "Spain",
            "latitude": 41.6567,
            "longitude": -0.8783,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "0040-01-02",
            "approving_authority": "Apostolic Tradition / Papal Bull of Pope Innocent XIII (1723)",
            "confidence": "confirmed",
            "confidence_note_en": "Celebrated in church tradition as the first Marian apparition in Christian history (a bilocation occurring before the Assumption of the Virgin); formally recognized by papal bulls since Callixtus III (1456) and confirmed by the Sacred Congregation of Rites in 1723.",
            "confidence_note_vi": "Được tôn kính là cuộc hiện ra đầu tiên của Đức Mẹ trong lịch sử Kitô giáo (dưới hình thức song vị trí khi Đức Mẹ còn đang sống trước biến cố Mông Triệu); được các Đức Giáo hoàng chuẩn nhận từ thời Callixtus III (1456) và Bộ Phụng Tự xác nhận năm 1723."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Sacred Jasper Column and Wooden Image of Our Lady",
                "relic_name_vi": "Trụ Đá Ngọc Thạch Thánh và Tượng Gỗ Cổ Kính của Đức Mẹ",
                "relic_type": "holy_icon",
                "reliquary_location": "Holy Chapel (Santa Capilla) inside the Basilica of the Pillar"
            }
        ],
        "historical_summary_en": "According to ancient Iberian tradition documented in the 13th-century *Moralia in Job*, Saint James the Greater (*Santiago*) was preaching the Gospel along the banks of the Ebro River in Caesaraugusta (modern Zaragoza) in the year AD 40. Discouraged by the hardness of the pagan population's hearts and facing fierce resistance, the Apostle knelt in nocturnal prayer with eight disciples.\n\nThe Blessed Virgin Mary—who was at that time still living in Jerusalem or Ephesus—miraculously appeared to James in bilocation, accompanied by choirs of angels. She presented him with a column of green jasper stone and a small wooden statue of herself, instructing him to build a chapel on the site and promising that the faith of Spain would remain as enduring and unshakable as the pillar itself until the end of time.\n\nSaint James constructed a primitive adobe chapel around the pillar, which survived centuries of Roman persecutions, Visigothic conflicts, and Muslim rule intact. The monumental Baroque basilica that now encloses the Holy Pillar stands as the bedrock of Hispanic faith, attracting millions of pilgrims celebrating the patroness of all Hispanic peoples.",
        "historical_summary_vi": "Theo truyền thống cổ xưa của xứ Hispania được ghi chép trong tác phẩm *Moralia in Job* thế kỷ 13, Thánh Giacôbê Tiền tông đồ đang miệt mài rao giảng Tin Mừng bên bờ sông Ebro tại Caesaraugusta (nay là Zaragoza) vào năm 40 sau Công Nguyên. Giữa sự nản lòng vì dân ngoại cứng lòng và sự bách hại khắc nghiệt, Thánh Tông đồ đã quỳ gối cầu nguyện trong đêm cùng 8 môn đệ.\n\nĐức Trinh Nữ Maria—khi đó vẫn còn đang sinh sống tại Jerusalem hoặc Ephesus—đã hiện ra với Thánh Giacôbê dưới hình thức hiện diện song vị trí kỳ diệu, giữa các thiên thần hầu cận. Đức Mẹ trao cho ngài một trụ đá ngọc thạch jasper xanh cùng một pho tượng gỗ nhỏ tạc hình Mẹ, truyền xây một nhà nguyện tại nơi đây và hứa rằng đức tin của xứ sở này sẽ vững bền như chính trụ đá cho đến tận thế.\n\nThánh Giacôbê đã dựng ngôi nhà nguyện đầu tiên quanh trụ đá, và nơi đây đã kỳ diệu đứng vững qua các cuộc bách hại thời La Mã, thời Visigoth và thời Hồi giáo chiếm đóng. Vương Cung Thánh Đường nguy nga ngày nay là nền tảng đức tin vững chắc của toàn thể thế giới nói tiếng Tây Ban Nha.",
        "scripture_reading": "1 Corinthians 3:11",
        "suggested_prayer_en": "O Sovereign Queen of the Pillar, Mother of Mercy and Strength of Apostles, you gave courage to Saint James upon the banks of the Ebro and promised an unshakeable foundation of faith. Grant that our hearts may be anchored upon Christ the solid Rock, steadfast amid all worldly tempests and faithful unto eternal life. Through Christ our Lord. Amen.",
        "suggested_prayer_vi": "Lạy Đức Mẹ Trụ Cột, Mẹ Lòng Thương Xót và là Sức Mạnh của các Tông Đồ, Mẹ đã ban ơn can đảm cho Thánh Giacôbê bên dòng sông Ebro và hứa ban nền tảng đức tin vững chắc như trụ đá. Xin cho tâm hồn chúng con luôn bám rễ sâu nơi Chúa Kitô là Tảng Đá Cứu Độ, kiên vững giữa mọi giông tố cuộc đời và trung thành cho đến ngày hưởng phúc trường sinh. Nhờ Đức Kitô, Chúa chúng con. Amen.",
        "primary_sources": [
            {
                "label": "Cathedral-Basilica of the Pillar Archival History (Cabildo Metropolitano de Zaragoza)",
                "url": "https://catedraldezaragoza.es/",
                "type": "academic"
            },
            {
                "label": "Pope Saint John Paul II - Address at the Basilica of Our Lady of the Pillar (October 10, 1984)",
                "url": "https://www.vatican.va/content/john-paul-ii/es/speeches/1984/october/documents/hf_jp-ii_spe_19841010_virgen-pilar.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "our_lady_of_la_vang",
        "category": "marian_apparition",
        "name_en": "National Shrine of Our Lady of La Vang",
        "name_vi": "Trung Tâm Hành Hương Toàn Quốc Đức Mẹ La Vang",
        "feast_day_association": "Solemnity of the Assumption (August 15)",
        "location": {
            "shrine_or_basilica": "Trung tâm Hành hương Đức Mẹ La Vang",
            "city": "Hải Lăng",
            "region_or_state": "Quảng Trị",
            "country": "Vietnam",
            "latitude": 16.7118,
            "longitude": 107.2144,
            "precision": "apparition_ground"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1901-08-08",
            "approving_authority": "Bishop Louis Caspar / Pope John XXIII (Minor Basilica 1961) / Pope John Paul II (Message 1998)",
            "confidence": "confirmed",
            "confidence_note_en": "Formally blessed by Bishop Caspar in 1901; elevated to Minor Basilica by Pope John XXIII in 1961; recognized by Pope John Paul II in 1998 as the National Marian Shrine of Vietnam on the bicentennial of the apparitions.",
            "confidence_note_vi": "Được Đức Cha Louis Caspar làm phép đền thánh năm 1901; Đức Giáo hoàng Gioan XXIII nâng lên hàng Tiểu Vương Cung Thánh Đường năm 1961; Đức Thánh Cha Gioan Phaolô II long trọng gửi sứ điệp công nhận là Trung tâm Hành hương Thánh Mẫu Toàn quốc dịp kỷ niệm 200 năm Đức Mẹ hiện ra (1998)."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Ancient Banyan Tree Apparition Grounds and Bell Tower Relic",
                "relic_name_vi": "Linh Địa Cây Đa Nơi Đức Mẹ Hiện Ra và Di Tích Tháp Cổ",
                "relic_type": "apparition_site",
                "reliquary_location": "The Ancient Sanctuary Memorial Plaza at La Vang"
            }
        ],
        "historical_summary_en": "In the year 1798, during the fierce anti-Catholic persecution under King Cảnh Thịnh of the Tây Sơn dynasty, numerous Vietnamese Catholics from Quảng Trị fled into the remote, malaria-ridden jungle of La Vang (near Dinh Cát). Stricken by tropical fever, starvation, and fear of wild beasts, the faithful gathered each evening beneath a large banyan tree to pray the Holy Rosary.\n\nOne evening in 1798, a radiant Lady wearing traditional Vietnamese royal attire (*áo dài*) and holding the Infant Jesus in her arms appeared near the tree, accompanied by two angels. She comforted the suffering Christians in sweet Vietnamese words: *'Children, what you have asked for, I have granted. From now on, whoever comes to pray to me in this place will have their prayers heard.'* She taught them to boil the leaves of the wild *vằng* bush to heal their fevers and promised continuous maternal protection.\n\nDespite successive waves of severe persecution, the faithful built a thatch chapel that grew into the spiritual haven of Vietnamese Catholicism. Today, La Vang stands as the supreme national pilgrimage sanctuary for millions of Vietnamese Catholics at home and across the worldwide diaspora.",
        "historical_summary_vi": "Vào năm 1798, dưới triều đại vua Cảnh Thịnh triều Tây Sơn, một sắc chỉ cấm đạo ngặt nghèo được ban hành khiến nhiều giáo dân vùng Quảng Trị phải trốn vào rừng sâu nước độc La Vang (gần Dinh Cát). Giữa cảnh ốm đau vì sốt rét rừng, đói khát và sợ thú dữ, các tín hữu đêm đêm quây quần dưới gốc cây đa cổ thụ để cùng nhau sốt sắng lần chuỗi Mân Côi.\n\nMột đêm nọ năm 1798, Đức Mẹ rực rỡ trong trang phục áo dài truyền thống bế Chúa Hài Đồng cùng hai thiên thần đã hiện ra bên gốc cây đa. Đức Mẹ âu yếm phán bảo: *'Các con hãy tin tưởng, cam lòng chịu khổ, Mẹ đã nhận lời các con kêu xin. Từ nay về sau, hễ ai chạy đến cầu khẩn Mẹ tại chốn này, Mẹ sẽ ban ơn phù hộ.'* Đức Mẹ còn dạy họ hái lá vằng đun nước uống để chữa lành bệnh tật và hứa ban ơn che chở liên lỉ.\n\nVượt qua bao thăng trầm và các cuộc bách hại khốc liệt, ngôi nguyện đường tranh lá thô sơ xưa kia đã trở thành linh địa thiêng liêng bậc nhất của người Công giáo Việt Nam. Ngày nay, La Vang là trung tâm hành hương quy tụ hàng triệu lượt tín hữu trong nước và hải ngoại về bên Mẹ mỗi năm.",
        "scripture_reading": "Luke 1:48-49",
        "suggested_prayer_en": "O Lady of La Vang, Loving Mother of Vietnam and Queen of Martyrs, you comforted our ancestors in the deep jungles during their hours of bitter persecution. Bless our nation, protect our families, preserve the Catholic faith in our hearts, and grant that we may remain loyal witnesses to the Gospel of Christ in all circumstances. Through Christ our Lord. Amen.",
        "suggested_prayer_vi": "Lạy Đức Mẹ La Vang, Mẹ Dịu Hiền của dân tộc Việt Nam và là Nữ Vương các Thánh Tử Đạo, Mẹ đã đến an ủi tổ tiên chúng con nơi rừng sâu nước độc trong cơn bách hại đau thương. Xin Mẹ chúc lành cho quê hương đất nước, gìn giữ các gia đình, bảo tồn đức tin son sắt nơi tâm hồn chúng con và ban cho chúng con lòng can đảm làm chứng nhân cho Tin Mừng của Chúa trong mọi hoàn cảnh. Nhờ Đức Kitô, Chúa chúng con. Amen.",
        "primary_sources": [
            {
                "label": "Pope John Paul II - Message to the Church in Vietnam for the Bicentennial of the Apparitions of Our Lady of La Vang (July 16, 1998)",
                "url": "https://www.vatican.va/content/john-paul-ii/vi/messages/pont-messages/1998/documents/hf_jp-ii_mes_19980716_la-vang.html",
                "type": "vatican"
            },
            {
                "label": "Archdiocese of Huế - Historical Records and Chronicles of La Vang Sanctuary",
                "url": "https://tonggiaophanhue.org/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "our_lady_of_tra_kieu",
        "category": "marian_apparition",
        "name_en": "National Shrine of Our Lady of Trà Kiệu",
        "name_vi": "Trung Tâm Hành Hương Đức Mẹ Trà Kiệu",
        "feast_day_association": "Feast of Our Lady Help of Christians / Trà Kiệu Commemoration (May 31)",
        "location": {
            "shrine_or_basilica": "Trung tâm Hành hương Đức Mẹ Trà Kiệu",
            "city": "Duy Xuyên",
            "region_or_state": "Quảng Nam",
            "country": "Vietnam",
            "latitude": 15.8239,
            "longitude": 108.2394,
            "precision": "apparition_ground"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1885-09-21",
            "approving_authority": "Diocese of Đà Nẵng / Bishop Jean-Pierre-Alexandre Bruyère",
            "confidence": "confirmed",
            "confidence_note_en": "Documented by Fr. Jean-Baptiste Bruyère and approved by the local ordinary following the miraculous defense of the Christian village from September 1 to 21, 1885; celebrated as the Marian Shrine of the Diocese of Đà Nẵng.",
            "confidence_note_vi": "Được Cha Jean-Baptiste Bruyère ghi chép và Tòa Giám mục công nhận sau biến cố giải cứu làng Công giáo Trà Kiệu từ ngày 1 đến 21 tháng 9 năm 1885; trở thành Trung tâm Hành hương Thánh Mẫu Giáo phận Đà Nẵng."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Apparition Hilltop Shrine (Bửu Châu) and Cannon Defense Memorial",
                "relic_name_vi": "Đồi Bửu Châu Nơi Đức Mẹ Hiện Ra và Di Tích Phòng Thủ",
                "relic_type": "apparition_site",
                "reliquary_location": "Bửu Châu Hill Chapel, Trà Kiệu"
            }
        ],
        "historical_summary_en": "In September 1885, during the Văn Thân uprising targeting Catholic communities in central Vietnam, a force of several thousand heavily armed insurgents surrounded the small Catholic village of Trà Kiệu in Quảng Nam province. The village was defended by only a few hundred poorly equipped faithful led by their pastor, Father Jean Bruyère, who gathered the women and children inside the parish church to pray the Rosary continuously before the Blessed Sacrament.\n\nBetween September 10 and 11, 1885, the attackers positioned artillery on the surrounding Bửu Châu hills to bombard the church. However, cannon shells repeatedly failed to hit the roof or deflected harmlessly. The assailants later testified that they saw a radiant Lady dressed in dazzling white standing upon the church roof, with her maternal mantle turning away incoming artillery rounds, accompanied by a troop of luminous children guarding the ramparts.\n\nOverwhelmed by the heavenly apparition and internal discord, the besieging forces broke camp and fled on September 21, 1885. In thanksgiving, the faithful built the shrine of Our Lady Help of Christians on Bửu Châu hill, which remains a deeply revered pilgrimage sanctuary in Central Vietnam.",
        "historical_summary_vi": "Vào tháng 9 năm 1885, trong phong trào Văn Thân nhắm vào các cộng đoàn Công giáo miền Trung, hàng ngàn nghĩa binh vũ trang đã bao vây giáo họ Trà Kiệu thuộc tỉnh Quảng Nam. Ngôi làng nhỏ chỉ có vài trăm giáo dân với vũ khí thô sơ dưới sự hướng dẫn của Cha sở Jean Bruyère, đã tập hợp phụ nữ và trẻ em vào nhà thờ liên lỉ cầu nguyện chuỗi Mân Côi trước Mình Thánh Chúa.\n\nTừ ngày 10 đến 11 tháng 9 năm 1885, quân bao vây đặt đại bác trên đỉnh đồi Bửu Châu nã đạn xối xả vào nhà thờ. Lạ lùng thay, đạn pháo bắn ra đều rơi lệch hướng hoặc không nổ. Quân tấn công sau đó khai nhận họ nhìn thấy một Bà Đẹp rực rỡ mặc áo trắng tinh khôi đứng trên nóc nhà thờ, dang rộng tà áo chở che làm lệch hướng đạn pháo, bên cạnh có đoàn trẻ nhỏ sáng láng đứng bảo vệ lũy làng.\n\nTrước hiện tượng siêu nhiên và sự phân rã nội bộ, đoàn quân vây hãm đã rút lui vào ngày 21 tháng 9 năm 1885. Để ghi ơn cứu mạng lạ lùng, cộng đoàn đã xây dựng Đền Thánh Đức Mẹ Phù Hộ Các Tín Hữu trên đồi Bửu Châu, trở thành trung tâm hành hương linh thiêng thu hút hàng trăm ngàn tín hữu khắp miền Trung.",
        "scripture_reading": "Psalm 91:1-4",
        "suggested_prayer_en": "O Lady of Trà Kiệu, Mother of the Afflicted and Help of Christians, you shielded your children from deadly assaults and showed the power of confident prayer. Stand guard over our lives in times of spiritual warfare and moral danger; cover our youth with your mantle of purity, and guide our families to victory in Christ. Amen.",
        "suggested_prayer_vi": "Lạy Đức Mẹ Trà Kiệu, Mẹ Ban Ơn Phù Hộ Các Giáo Hữu, Mẹ đã dang tay che chở con cái Mẹ thoát khỏi làn tên mũi đạn trong cơn nguy biến nhờ lời kinh Mân Côi tha thiết. Xin Mẹ tiếp tục bảo vệ chúng con trong những cơn cám dỗ và gian nan thử thách linh hồn; xin chở che giới trẻ bằng tà áo trinh khiết của Mẹ và dẫn dắt gia đình chúng con luôn trung kiên theo Chúa. Amen.",
        "primary_sources": [
            {
                "label": "Diocese of Đà Nẵng - Historical Chronicles of Trà Kiệu Marian Sanctuary",
                "url": "https://giaophandanang.org/",
                "type": "academic"
            },
            {
                "label": "Missions Étrangères de Paris (MEP) - Annales du Sanctuaire de Trà Kiệu (1885)",
                "url": "https://irfa.paris/en/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "our_lady_of_siluva",
        "category": "marian_apparition",
        "name_en": "Sanctuary of Our Lady of Šiluva",
        "name_vi": "Đền Thánh Đức Mẹ Šiluva",
        "feast_day_association": "Feast of the Nativity of the Blessed Virgin Mary (September 8)",
        "location": {
            "shrine_or_basilica": "Šiluvos Švč. Mergelės Marijos Gimimo bazilika",
            "city": "Šiluva",
            "region_or_state": "Raseiniai District",
            "country": "Lithuania",
            "latitude": 55.5310,
            "longitude": 23.2246,
            "precision": "apparition_ground"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1775-08-17",
            "approving_authority": "Pope Pius VI (Papal Coronation) / Papal Bull 1775",
            "confidence": "confirmed",
            "confidence_note_en": "Officially confirmed by Pope Pius VI with papal coronation decrees in 1775; visited and honored by Pope John Paul II in September 1993 during his historic Baltic pilgrimage.",
            "confidence_note_vi": "Được Đức Giáo hoàng Piô VI phê chuẩn chính thức qua sắc lệnh đội triều thiên năm 1775; được Thánh Giáo hoàng Gioan Phaolô II đến viếng thăm và tôn vinh trong chuyến tông du lịch sử vùng Baltic năm 1993."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Apparition Rock and Miraculous Painting of the Virgin and Child",
                "relic_name_vi": "Phiến Đá Nơi Đức Mẹ Hiện Ra và Bức Tranh Phép Lạ Đức Mẹ Ẵm Chúa Hài Đồng",
                "relic_type": "holy_icon",
                "reliquary_location": "Chapel of the Apparition (built directly over the apparition rock) and the Basilica Main Altar"
            }
        ],
        "historical_summary_en": "In the early 17th century, following the Protestant Reformation, the Catholic parish in Šiluva, Lithuania, had been seized by Calvinists, and the Catholic faith was almost completely eradicated in the region. Before the church was confiscated around 1569, the last parish priest had placed the sacred chalices, documents, and an ancient icon of the Virgin into an ironclad chest and buried it in a field.\n\nIn the summer of 1608, several young shepherd children grazing their flocks in the field witnessed a miraculous vision: a beautiful young woman with weeping eyes, holding an infant in her arms and clothed in flowing blue and white robes, standing atop a large rock. The Calvinist pastor of the town was summoned to reprimand the children for superstition; upon arriving at the rock with a crowd, the pastor also saw the weeping Lady. When asked why she wept, she replied: *'Formerly in this place, my Son was adored and honored, but now this ground is given over to plowing and sowing.'*\n\nThe apparition led to the miraculous rediscovery of the buried chest by a blind nonagenarian whose sight was instantly restored. The event catalyzed the massive re-conversion of Lithuania to the Catholic faith, establishing Šiluva as one of the earliest documented Marian apparitions in Europe.",
        "historical_summary_vi": "Vào đầu thế kỷ 17, sau phong trào Cải cách Kháng cách, giáo xứ Công giáo tại Šiluva, Lithuania đã bị những người theo thuyết Calvin tịch thu, và đức tin Công giáo gần như bị xóa sổ hoàn toàn trong vùng. Trước khi nhà thờ bị chiếm đoạt năm 1569, vị linh mục chánh xứ cuối cùng đã cất giấu chén thánh, sổ sách và linh ảnh Đức Mẹ cổ kính vào một chiếc rương sắt rồi chôn giấu ngoài cánh đồng.\n\nVào mùa hè năm 1608, các em nhỏ chăn chiên trên cánh đồng bỗng nhìn thấy một thị kiến kỳ diệu: một Người Nữ xinh đẹp đang bồng Hài Nhi trên tay, nước mắt tuôn rơi, mặc áo xanh da trời đứng trên một tảng đá lớn. Vị mục sư Calvin địa phương liền dẫn đám đông tới để quở trách các em vì mê tín; nhưng khi vừa tới nơi, chính vị mục sư cũng nhìn thấy Người Nữ đang khóc. Khi được hỏi vì sao Người khóc, Đức Mẹ đáp: *'Trước đây tại nơi này, Con Ta đã được tôn thờ và phụng sự, nhưng giờ đây đất này lại bị đem ra cày cấy gieo hạt.'*\n\nBiến cố hiện ra đã dẫn đến việc tìm lại chiếc rương sắt chôn giấu nhờ một cụ già mù 90 tuổi được sáng mắt ngay tức khắc khi chỉ đúng vị trí. Phép lạ này đã khơi mào cho phong trào tái trở lại đạo Công giáo mãnh liệt của toàn thể dân tộc Lithuania, đưa Šiluva trở thành một trong những cuộc hiện ra đầu tiên của Đức Mẹ được Giáo hội công nhận tại Châu Âu.",
        "scripture_reading": "Jeremiah 31:15-17",
        "suggested_prayer_en": "O Mother of God of Šiluva, who wept over the loss of faith and the neglect of your Divine Son, soften our hard hearts and awaken in us a burning desire for authentic conversion. Guard our parishes in true Catholic doctrine, strengthen families in living faith, and lead our society back to the worship of Christ. Amen.",
        "suggested_prayer_vi": "Lạy Mẹ Thiên Chúa tại Šiluva, Mẹ đã rơi lệ vì đức tin bị mai một và Con Chí Thánh của Mẹ bị lãng quên, xin làm mềm lòng chai đá chúng con và thắp lên trong tâm hồn chúng con lòng khao khát hoán cải chân thành. Xin gìn giữ các giáo xứ trong giáo lý tinh tuyền, củng cố các gia đình trong đức tin sống động và dẫn đưa xã hội chúng con trở về phụng thờ Chúa Kitô. Amen.",
        "primary_sources": [
            {
                "label": "Archdiocese of Kaunas - Official Documentation of Šiluva Apparitions",
                "url": "https://kaunoarkivyskupija.lt/",
                "type": "academic"
            },
            {
                "label": "Pope John Paul II - Prayer at the Sanctuary of Our Lady of Šiluva (September 7, 1993)",
                "url": "https://www.vatican.va/content/john-paul-ii/lt/speeches/1993/september/documents/hf_jp-ii_spe_19930907_siluva.html",
                "type": "vatican"
            }
        ]
    }
]

def main():
    target_dir = "Anno/Resources/SacredSanctuaries"
    os.makedirs(target_dir, exist_ok=True)
    
    for item in BATCH_1 + BATCH_2:
        filename = f"{item['sanctuary_id']}.json"
        path = os.path.join(target_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False, indent=2)
        print(f"Generated {filename}")

if __name__ == "__main__":
    main()

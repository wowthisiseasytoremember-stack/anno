#!/usr/bin/env python3
"""
generate_batch_3_4.py
Generates Batch 3 (Modern Apparitions & Special Shrines) & Batch 4 (Apostolic Tombs & Patristic Basilicas)
"""

import json
import os

BATCH_3 = [
    {
        "sanctuary_id": "our_lady_of_banneux",
        "category": "marian_apparition",
        "name_en": "Sanctuary of Our Lady of Banneux (Virgin of the Poor)",
        "name_vi": "Đền Thánh Đức Mẹ Banneux (Đức Mẹ Kẻ Nghèo)",
        "feast_day_association": "Feast of Our Lady of Banneux (January 15)",
        "location": {
            "shrine_or_basilica": "Sanctuaire de la Vierge des Pauvres de Banneux Notre-Dame",
            "city": "Banneux (Louveigné)",
            "region_or_state": "Liège",
            "country": "Belgium",
            "latitude": 50.5186,
            "longitude": 5.8242,
            "precision": "apparition_ground"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1949-08-22",
            "approving_authority": "Bishop Louis-Joseph Kerkhofs / Pope Pius XII",
            "confidence": "confirmed",
            "confidence_note_en": "Formally recognized as authentic supernatural apparitions by Bishop Kerkhofs of Liège in 1949 with confirmation from the Holy See.",
            "confidence_note_vi": "Được Đức Giám mục Louis-Joseph Kerkhofs giáo phận Liège chính thức công nhận tính chất siêu nhiên đích thực vào năm 1949 với sự phê chuẩn của Tòa Thánh."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Miraculous Spring Dedicated to All Nations",
                "relic_name_vi": "Suối Nguồn Phép Lạ Dành Cho Muôn Dân Nước",
                "relic_type": "apparition_site",
                "reliquary_location": "The Spring Esplanade at Banneux Sanctuary"
            }
        ],
        "historical_summary_en": "Between January 15 and March 2, 1933, the Blessed Virgin Mary appeared eight times to eleven-year-old Mariette Beco in the small rural village of Banneux, Belgium, nestled in the Ardennes plateau. Clothed in a brilliant white gown with a blue sash and a golden rose on her right foot, the Lady stepped gently across the snow.\n\nDuring her second apparition on January 18, Our Lady led Mariette to a small spring of water beside the road. The Virgin instructed the child to plunge her hands into the freezing stream, proclaiming: *'Push your hands into the water... This spring is reserved for me... reserved for all nations, to bring comfort to the sick.'* On February 15, the Lady revealed her heavenly title: *'I am the Virgin of the Poor'* (*La Vierge des Pauvres*), promising to intercede especially for those burdened by spiritual poverty, destitution, and physical distress.\n\nOccurring in the immediate shadow of Adolf Hitler's rise to power in neighboring Germany in January 1933, the message of Banneux offered a heavenly counterpoint of peace, humility, and maternal tenderness for all nations, transcending racial and nationalistic hatreds.",
        "historical_summary_vi": "Từ ngày 15 tháng 1 đến ngày 2 tháng 3 năm 1933, Đức Trinh Nữ Maria đã hiện ra tám lần với cô bé 11 tuổi Mariette Beco tại ngôi làng nông thôn nhỏ Banneux, nước Bỉ, trên vùng cao nguyên Ardennes. Mặc áo trắng tinh khôi với thắt lưng xanh và bông hồng vàng trên mu bàn chân phải, Đức Mẹ bước đi nhẹ nhàng trên tuyết trắng.\n\nTrong lần hiện ra thứ hai ngày 18 tháng 1, Đức Mẹ dẫn Mariette đến một dòng suối nhỏ bên đường. Mẹ dạy cô bé nhúng hai bàn tay vào làn nước băng giá và phán: *'Hãy nhúng tay con vào nước... Dòng suối này dành riêng cho Mẹ... dành cho mọi dân tộc để xoa dịu những người đau yếu tật nguyền.'* Ngày 15 tháng 2, Mẹ mạc khải danh hiệu: *'Ta là Đức Mẹ Kẻ Nghèo'* (*La Vierge des Pauvres*), hứa sẽ cầu bầu đặc biệt cho những người chịu cảnh nghèo khó tinh thần, cô thế và đau đớn bệnh tật.\n\nDiễn ra đúng vào thời điểm Adolf Hitler lên nắm quyền tại nước Đức láng giềng vào tháng 1 năm 1933, sứ điệp Banneux là lời mời gọi của thiên đàng về hòa bình, đức khiêm nhường và tình mẫu tử dành cho muôn dân tộc, vượt lên trên mọi hận thù chủng tộc và chủ nghĩa dân tộc cực đoan.",
        "scripture_reading": "Matthew 5:3",
        "suggested_prayer_en": "O Virgin of the Poor, Mother of the Savior and Queen of All Nations, you revealed the healing waters of grace for the sick and the destitute. Comfort all who carry heavy burdens of body or spirit, strengthen the poor and afflicted, and teach us to love our neighbor with the tender compassion of Christ. Amen.",
        "suggested_prayer_vi": "Lạy Đức Mẹ Kẻ Nghèo, Mẹ Đấng Cứu Thế và là Nữ Vương Muôn Dân Nước, Mẹ đã tỏ lộ dòng suối ân sủng chữa lành cho những người bệnh tật và nghèo khổ. Xin an ủi tất cả những ai đang mang gánh nặng thể xác hay tâm hồn, nâng đỡ người nghèo hèn và dạy chúng con biết yêu thương tha nhân bằng lòng trắc ẩn dịu hiền của Chúa Kitô. Amen.",
        "primary_sources": [
            {
                "label": "Sanctuaire de Banneux Notre-Dame Official Historical Archives",
                "url": "https://www.banneux-nd.be/en/",
                "type": "academic"
            },
            {
                "label": "Pope John Paul II - Letter on the 50th Anniversary of the Banneux Apparitions (1983)",
                "url": "https://www.vatican.va/content/john-paul-ii/fr/letters/1983/documents/hf_jp-ii_let_19830508_banneux.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "our_lady_of_beauraing",
        "category": "marian_apparition",
        "name_en": "Sanctuary of Our Lady of Beauraing (The Virgin with the Golden Heart)",
        "name_vi": "Đền Thánh Đức Mẹ Beauraing (Đức Mẹ Trái Tim Vàng)",
        "feast_day_association": "Feast of Our Lady of Beauraing (November 29)",
        "location": {
            "shrine_or_basilica": "Sanctuaire de Notre-Dame de Beauraing",
            "city": "Beauraing",
            "region_or_state": "Namur",
            "country": "Belgium",
            "latitude": 50.1111,
            "longitude": 4.9575,
            "precision": "apparition_ground"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1949-07-02",
            "approving_authority": "Bishop André-Marie Charue / Sacred Congregation of the Holy Office",
            "confidence": "confirmed",
            "confidence_note_en": "Approved by Bishop André-Marie Charue of Namur on July 2, 1949, with a decree confirming the supernatural character of the thirty-three apparitions.",
            "confidence_note_vi": "Được Đức Giám mục André-Marie Charue giáo phận Namur công nhận ngày 2 tháng 7 năm 1949 qua sắc lệnh xác thực tính chất siêu nhiên của 33 lần hiện ra."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Hawthorn Tree Apparition Ground",
                "relic_name_vi": "Cội Cây Sơn Tra Nơi Đức Mẹ Hiện Ra",
                "relic_type": "apparition_site",
                "reliquary_location": "The Hawthorn Garden at the Beauraing Sanctuary"
            }
        ],
        "historical_summary_en": "Between November 29, 1932, and January 3, 1933, the Blessed Virgin Mary appeared thirty-three times to five children—Fernande, Gilberte, and Albert Voisin, along with Andrée and Gilberte Degeimbre—near a hawthorn tree by the convent of the Sisters of Christian Doctrine in Beauraing, Belgium. The children saw a radiant Lady in a cloudless light, wearing a flowing white dress and holding her hands joined in prayer.\n\nIn the final apparitions, as she opened her arms in blessing, the Lady revealed within her chest a radiant Heart of pure gold surrounded by luminous rays (*Le Cœur d'Or*). She announced: *'I am the Immaculate Virgin... I will convert sinners... Do you love my Son? Do you love me? Then sacrifice yourselves for me.'*\n\nThe apparitions were witnessed during their culmination by crowds of over thirty thousand people who observed the ecstatic state of the children under medical supervision. The sanctuary stands as an enduring monument to Mary's Immaculate, Golden Heart and her maternal call for personal conversion and sacrifice for the redemption of sinners.",
        "historical_summary_vi": "Từ ngày 29 tháng 11 năm 1932 đến ngày 3 tháng 1 năm 1933, Đức Trinh Nữ Maria đã hiện ra 33 lần với 5 trẻ nhỏ—Fernande, Gilberte, Albert Voisin cùng hai chị em Andrée và Gilberte Degeimbre—bên cội cây sơn tra gần tu viện các Nữ tu Giáo lý Kitô giáo tại Beauraing, nước Bỉ. Các em nhìn thấy một Bà Đẹp rực rỡ trong ánh sáng thanh khiết, mặc áo trắng dài và chắp tay cầu nguyện.\n\nTrong những lần hiện ra cuối cùng, khi dang rộng đôi tay chúc lành, Đức Mẹ đã để lộ nơi lồng ngực một Trái Tim bằng vàng ròng sáng chói tỏa ra muôn ngàn tia sáng (*Le Cœur d'Or*). Đức Mẹ phán: *'Ta là Trinh Nữ Vô Nhiễm... Ta sẽ hoán cải các tội nhân... Các con có yêu mến Con Ta không? Các con có yêu mến Mẹ không? Vậy hãy hi sinh vì Mẹ.'*\n\nNhững lần hiện ra cuối cùng đã diễn ra trước sự chứng kiến của hơn ba mươi ngàn người và được các bác sĩ kiểm nghiệm trạng thái xuất thần của các em. Đền thánh Beauraing là biểu tượng bất diệt tôn vinh Trái Tim Vàng Vô Nhiễm của Mẹ và lời mời gọi tha thiết hoán cải, hi sinh để cầu cho các tội nhân được ơn cứu độ.",
        "scripture_reading": "Proverbs 4:23",
        "suggested_prayer_en": "O Immaculate Virgin of the Golden Heart, Mother of Beauraing, you manifested the burning charity of your maternal heart for all people. Ignite in our souls a true love for your Divine Son Jesus; help us to offer our daily sacrifices with joy, and obtain the grace of conversion for hardened sinners. Through Christ our Lord. Amen.",
        "suggested_prayer_vi": "Lạy Đức Trinh Nữ Vô Nhiễm Trái Tim Vàng tại Beauraing, Mẹ đã tỏ bày tình yêu thương bừng cháy của trái tim từ mẫu dành cho nhân loại. Xin thắp lên trong tâm hồn chúng con lòng mến yêu tha thiết Con Chí Thánh của Mẹ là Chúa Giêsu; giúp chúng con biết vui lòng dâng những hy sinh hằng ngày và cầu xin ơn hoán cải cho các tội nhân cứng lòng. Nhờ Đức Kitô, Chúa chúng con. Amen.",
        "primary_sources": [
            {
                "label": "Sanctuaire de Beauraing Official Historical Archives",
                "url": "https://beauraing-sanctuaire.be/en/",
                "type": "academic"
            },
            {
                "label": "Pope John Paul II - Homily at the Sanctuary of Beauraing (May 18, 1985)",
                "url": "https://www.vatican.va/content/john-paul-ii/fr/homilies/1985/documents/hf_jp-ii_hom_19850518_beauraing.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "our_lady_of_akita",
        "category": "marian_apparition",
        "name_en": "Sanctuary of Our Lady of Akita (Seitai Hoshikai)",
        "name_vi": "Đền Thánh Đức Mẹ Akita (Dòng Nữ Tỳ Thánh Thể)",
        "feast_day_association": "Feast of Our Lady of the Rosary (October 7) / September 15",
        "location": {
            "shrine_or_basilica": "Seitai Hoshikai (Handmaids of the Holy Eucharist Convent)",
            "city": "Akita",
            "region_or_state": "Akita Prefecture, Tohoku",
            "country": "Japan",
            "latitude": 39.7547,
            "longitude": 140.1481,
            "precision": "apparition_ground"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1984-04-22",
            "approving_authority": "Bishop John Shojiro Ito / Cardinal Joseph Ratzinger (CDF)",
            "confidence": "confirmed",
            "confidence_note_en": "Officially approved by Bishop John Shojiro Ito of Niigata on Easter Sunday 1984 as authentic supernatural occurrences; confirmed as worthy of belief by Cardinal Joseph Ratzinger (Pope Benedict XVI) in 1988.",
            "confidence_note_vi": "Được Đức Giám mục Gioan Shojiro Ito giáo phận Niigata chính thức công nhận vào Chúa Nhật Phục Sinh năm 1984; Đức Hồng y Joseph Ratzinger (Bộ Giáo Lý Đức Tin) xác nhận đáng tin cậy vào năm 1988."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Miraculous Weeping Katsura-Wood Statue of Our Lady of All Nations",
                "relic_name_vi": "Tượng Gỗ Katsura Chảy Máu và Nước Mắt của Đức Mẹ Mọi Dân Tộc",
                "relic_type": "holy_icon",
                "reliquary_location": "Main Chapel of the Handmaids of the Holy Eucharist, Yuzawadai, Akita"
            }
        ],
        "historical_summary_en": "Between 1973 and 1981, at the convent of the Handmaids of the Holy Eucharist in Yuzawadai, Akita, extraordinary mystical phenomena occurred surrounding Sister Agnes Katsuko Sasagawa, a deaf religious sister. On June 12, 1973, Sister Agnes witnessed brilliant rays of light emanating from the tabernacle, followed by the appearance of a cross-shaped wound upon her left palm that bled profusely on Thursdays and Fridays.\n\nOn July 6, 1973, a three-foot wooden statue of Our Lady carved from Katsura wood began speaking to Sister Agnes, promising the restoration of her hearing (which occurred miraculously in 1982) and conveying urgent messages calling for prayer, penance, and Eucharistic reparation. Between 1975 and 1981, the wooden statue wept human tears and perspired a sweet-scented fluid on 101 separate occasions before hundreds of witnesses, including the local ordinary, Bishop John Shojiro Ito.\n\nForensic investigations conducted by Professor Sagisaka of the Department of Legal Medicine at Akita University and the Gifu University School of Medicine conclusively established that the tears and blood were genuine human fluids belonging to blood types AB, B, and O. The messages warned of severe global trials and divisions within the Church while promising that the Rosary and the Sign of the Cross would remain unconquerable shields of protection.",
        "historical_summary_vi": "Từ năm 1973 đến 1981, tại tu viện Dòng Nữ Tỳ Thánh Thể ở Yuzawadai, Akita, những hiện tượng siêu nhiên phi thường đã diễn ra xung quanh Nữ tu Agnes Katsuko Sasagawa, một nữ tu bị điếc hoàn toàn. Ngày 12 tháng 6 năm 1973, Sơ Agnes nhìn thấy ánh sáng chói lọi phát ra từ nhà tạm, và sau đó xuất hiện vết thương hình thánh giá rỉ máu nơi lòng bàn tay trái vào các ngày thứ Năm và thứ Sáu.\n\nNgày 6 tháng 7 năm 1973, pho tượng Đức Mẹ tạc bằng gỗ Katsura cao khoảng 90cm bắt đầu cất tiếng nói với Sơ Agnes, hứa sẽ chữa lành đôi tai cho sơ (phép lạ phục hồi thính giác đã xảy ra năm 1982) và truyền ban các sứ điệp khẩn thiết kêu gọi cầu nguyện, đền tội và tôn sùng Thánh Thể. Từ năm 1975 đến 1981, pho tượng gỗ đã 101 lần chảy nước mắt và toát ra mồ hôi thơm ngát trước sự chứng kiến của hàng trăm người, bao gồm chính Đức Giám mục Gioan Shojiro Ito.\n\nCác cuộc phân tích pháp y của Giáo sư Sagisaka thuộc Khoa Pháp Y Đại học Akita và Đại học Gifu đã chứng minh không thể chối cãi rằng các chất dịch và máu chảy ra từ tượng gỗ là máu và nước mắt của con người (thuộc nhóm máu AB, B và O). Sứ điệp Akita cảnh báo về những thử thách nặng nề và sự chia rẽ trong Giáo hội, đồng thời khẳng định chuỗi Mân Côi và Dấu Thánh Giá sẽ là lá chắn vững bền bảo vệ các tín hữu.",
        "scripture_reading": "Joel 2:12-13",
        "suggested_prayer_en": "O Most Sacred Heart of Jesus, truly present in the Holy Eucharist, we offer you our prayers, actions, and sufferings in union with the sorrowful and Immaculate Heart of Mary. Weep with us over the sins of the world, heal our spiritual deafness, and make us faithful instruments of reconciliation and peace. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Tâm Chúa Giêsu, Đấng đang hiện diện thực sự trong Bí Tích Thánh Thể, chúng con xin dâng lên Chúa mọi kinh nguyện, việc làm và những hy sinh thống khổ của chúng con, hợp cùng Trái Tim Vô Nhiễm Sầu Bi của Mẹ Maria. Xin Mẹ đoái thương những giọt nước mắt sám hối của chúng con, chữa lành sự điếc lác tâm linh và biến đổi chúng con thành những khí cụ bình an, hòa giải của Chúa. Amen.",
        "primary_sources": [
            {
                "label": "Diocese of Niigata - Pastoral Letter of Bishop John Shojiro Ito on the Apparitions of Akita (1984)",
                "url": "https://catholicnewsagency.com/resource/55415/our-lady-of-akita",
                "type": "vatican"
            },
            {
                "label": "Seitai Hoshikai Official Sanctuary & Medical Examination Dossier",
                "url": "https://seitaihoshikai.com/us/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "our_lady_of_kibeho",
        "category": "marian_apparition",
        "name_en": "Sanctuary of Our Lady of Kibeho (Mother of the Word)",
        "name_vi": "Đền Thánh Đức Mẹ Kibeho (Mẹ Ngôi Lời)",
        "feast_day_association": "Feast of Our Lady of Kibeho (November 28)",
        "location": {
            "shrine_or_basilica": "Sanctuaire Notre-Dame de Kibeho (Mère du Verbe)",
            "city": "Kibeho",
            "region_or_state": "Nyaruguru, Southern Province",
            "country": "Rwanda",
            "latitude": -2.6539,
            "longitude": 29.5539,
            "precision": "apparition_ground"
        },
        "canonical_status": {
            "approval_or_consecration_date": "2001-06-29",
            "approving_authority": "Bishop Augustin Misago / Holy See (CDF Declaration)",
            "confidence": "confirmed",
            "confidence_note_en": "Officially approved by Bishop Augustin Misago of Gikongoro in communion with the Holy See on June 29, 2001, for the visions of Alphonsine Mumureke, Nathalie Mukamazimpaka, and Marie Claire Mukangango.",
            "confidence_note_vi": "Được Đức Giám mục Augustin Misago giáo phận Gikongoro hiệp thông với Tòa Thánh chính thức công nhận ngày 29 tháng 6 năm 2001 đối với ba thị nhân: Alphonsine Mumureke, Nathalie Mukamazimpaka và Marie Claire Mukangango."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Apparition Grounds and Chapel of Our Lady of Sorrows",
                "relic_name_vi": "Linh Địa Hiện Ra và Nguyện Đường Đức Mẹ Sầu Bi Kibeho",
                "relic_type": "apparition_site",
                "reliquary_location": "Sanctuary of Our Lady of Kibeho, Nyaruguru"
            }
        ],
        "historical_summary_en": "On November 28, 1981, at a boarding school run by religious sisters in Kibeho, Rwanda, the Blessed Virgin Mary appeared to sixteen-year-old Alphonsine Mumureke, followed by subsequent apparitions to Nathalie Mukamazimpaka and Marie Claire Mukangango. Our Lady identified herself in the Kinyarwanda language as *'Nyina wa Jambo'* ('Mother of the Word') and issued a sorrowful call for sincere repentance, fraternal love, and the restoration of the Rosary of the Seven Sorrows.\n\nOn August 19, 1982, the visionaries witnessed an agonizing eight-hour vision known as the 'Day of Tears.' They saw riverbanks flowing with blood, burning villages, decapitated bodies, and horrifying mass violence. Our Lady warned that if human hearts did not repent and renounce tribal animosity, Rwanda would descend into an abyss of darkness.\n\nTwelve years later, in 1994, the devastating Rwandan Genocide erupted, fulfilling the prophetic visions with tragic precision. Kibeho is the first and only Vatican-approved Marian apparition site on the African continent, standing today as a global sanctuary of healing, reconciliation, and divine mercy.",
        "historical_summary_vi": "Ngày 28 tháng 11 năm 1981, tại một trường nữ sinh nội trú do các nữ tu điều hành ở Kibeho, Rwanda, Đức Trinh Nữ Maria đã hiện ra với cô nữ sinh 16 tuổi Alphonsine Mumureke, và sau đó hiện ra với Nathalie Mukamazimpaka và Marie Claire Mukangango. Đức Mẹ xưng mình bằng tiếng Kinyarwanda là *'Nyina wa Jambo'* ('Mẹ Ngôi Lời') và tha thiết kêu gọi hoán cải nội tâm, sống đức ái huynh đệ và cổ võ việc lần Chuỗi Bảy Sự Thương Khó Đức Mẹ.\n\nNgày 19 tháng 8 năm 1982, các thị nhân đã trải qua thị kiến đau thương kéo dài 8 giờ đồng hồ gọi là 'Ngày Của Những Giọt Nước Mắt'. Các em nhìn thấy những dòng sông cuộn máu, những ngôi làng bốc cháy, những thi thể lìa đầu và cảnh tượng tàn sát man rợ. Đức Mẹ nghẹn ngào cảnh báo rằng nếu nhân loại không chịu ăn năn sám hối và từ bỏ hận thù bộ tộc, Rwanda sẽ rơi vào thảm kịch kinh hoàng.\n\nMười hai năm sau, vào năm 1994, nạn diệt chủng Rwanda bùng nổ tàn khốc, ứng nghiệm chính xác thị kiến tiên tri năm xưa. Kibeho là đền thánh Mẹ hiện ra đầu tiên và duy nhất tại Lục địa Châu Phi được Tòa Thánh Vatican chính thức phê chuẩn, trở thành ngọn hải đăng của sự hòa giải, chữa lành và lòng thương xót Chúa.",
        "scripture_reading": "Luke 2:34-35",
        "suggested_prayer_en": "O Mother of the Word, Our Lady of Kibeho, you wept over the impending darkness of human hatred and invited us to sincere repentance. Melt the coldness of our hearts, banish all seeds of division and tribalism from our communities, and teach us to pray your Rosary of Seven Sorrows with deep contrition. Through Jesus Christ our Lord. Amen.",
        "suggested_prayer_vi": "Lạy Mẹ Ngôi Lời, Đức Mẹ Kibeho, Mẹ đã rơi lệ trước bóng tối hận thù của con người và mời gọi chúng con thật lòng sám hối. Xin làm tan chảy sự băng giá trong tâm hồn chúng con, xua tan mọi mầm mống chia rẽ hận thù trong cộng đoàn và dạy chúng con biết sốt sắng lần hạt Bảy Sự Thương Khó của Mẹ với lòng thống hối chân thành. Nhờ Đức Giêsu Kitô, Chúa chúng con. Amen.",
        "primary_sources": [
            {
                "label": "Declaration of the Bishop of Gikongoro on the Apparitions of Kibeho (June 29, 2001)",
                "url": "https://www.vatican.va/roman_curia/congregations/cfaith/documents/rc_con_cfaith_doc_20010629_kibeho_en.html",
                "type": "vatican"
            },
            {
                "label": "Sanctuary of Our Lady of Kibeho Official Documentation",
                "url": "https://kibeho-sanctuary.com/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "chapel_of_miraculous_medal",
        "category": "marian_apparition",
        "name_en": "Chapel of Our Lady of the Miraculous Medal (Rue du Bac)",
        "name_vi": "Nguyện Đường Đức Mẹ Ban Ơn (Rue du Bac)",
        "feast_day_association": "Feast of Our Lady of the Miraculous Medal (November 27)",
        "location": {
            "shrine_or_basilica": "Chapelle Notre-Dame de la Médaille Miraculeuse",
            "city": "Paris",
            "region_or_state": "Île-de-France",
            "country": "France",
            "latitude": 48.8509,
            "longitude": 2.3236,
            "precision": "exact_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1836-02-16",
            "approving_authority": "Archbishop Hyacinthe-Louis de Quélen / Pope Leo XIII",
            "confidence": "confirmed",
            "confidence_note_en": "Canonical investigation led by Archbishop de Quélen of Paris in 1836 confirmed the authenticity of the visions and the miraculous conversions wrought through the Medal; Saint Catherine Labouré canonized by Pope Pius XII in 1947.",
            "confidence_note_vi": "Được Đức Tổng Giám mục Hyacinthe-Louis de Quélen giáo phận Paris chuẩn nhận năm 1836; Thánh Catherine Labouré được Đức Giáo hoàng Piô XII tuyên thánh năm 1947."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Incorrupt Body of Saint Catherine Labouré and the Armchair of Our Lady",
                "relic_name_vi": "Thi Hài Toàn Vẹn Không Hư Nát của Thánh Nữ Catherine Labouré và Ghế Đức Mẹ",
                "relic_type": "incorrupt_body",
                "reliquary_location": "Glass reliquary under the side altar of the Virgin at Rue du Bac"
            }
        ],
        "historical_summary_en": "In 1830, in the chapel of the Daughters of Charity at 140 Rue du Bac in Paris, the Blessed Virgin Mary appeared three times to a humble novice, Saint Catherine Labouré. In the nocturnal hours of July 18, Catherine was led by her guardian angel to the sanctuary, where she knelt beside Our Lady seated in the director's armchair, resting her hands upon the Virgin's knees for over two hours in intimate conversation.\n\nOn November 27, 1830, Our Lady appeared standing atop a globe, crushing the serpent's head underfoot, with radiant beams of light streaming from rings on her fingers onto the earth. An oval frame formed around the vision containing the golden inscription: *'O Mary, conceived without sin, pray for us who have recourse to thee.'* The image turned, revealing the letter 'M' surmounted by a cross, the Sacred Heart of Jesus encircled with thorns, and the Immaculate Heart of Mary pierced by a sword.\n\nThe Virgin instructed Catherine to have a medal struck after this model, promising abundant graces to all who wore it with faith around their neck. Millions of medals were struck, prompting such an outpouring of documented physical cures and sudden spiritual conversions (including the famous conversion of Alphonse Ratisbonne in 1842) that the faithful spontaneously christened it 'The Miraculous Medal.'",
        "historical_summary_vi": "Vào năm 1830, tại nhà nguyện Tu hội Nữ Tử Bác Ái Vinh Sơn số 140 phố Rue du Bac ở Paris, Đức Trinh Nữ Maria đã hiện ra 3 lần với nữ tập sinh khiêm nhường là Thánh Catherine Labouré. Đêm ngày 18 tháng 7, được thiên thần bản mệnh dẫn đường vào nhà nguyện, Catherine đã quỳ bên Đức Mẹ ngồi trên chiếc ghế bành của cha giám đốc, đặt hai tay lên đầu gối Mẹ và tâm sự sốt sắng suốt hai giờ đồng hồ.\n\nNgày 27 tháng 11 năm 1830, Đức Mẹ lại hiện ra đứng trên quả địa cầu, gót chân đạp nát đầu con rắn, từ các ngón tay Mẹ tỏa ra muôn vàn luồng ánh sáng rực rỡ chiếu xuống mặt đất. Một khung hình bầu dục hiện ra bao quanh với dòng chữ vàng: *'Lạy Mẹ Maria vô nhiễm nguyên tội, xin cầu cho chúng con là kẻ chạy đến cùng Mẹ.'* Khi khung hình quay lại, xuất hiện chữ 'M' mang thánh giá bên trên, cùng Thánh Tâm Chúa Giêsu đội mão gai và Trái Tim Vô Nhiễm Mẹ bị lưỡi gươm đâm thấu.\n\nĐức Mẹ truyền cho Catherine cho đúc mẫu Ảnh theo hình ảnh này và hứa ban muôn ơn lành cho những ai đeo Ảnh với lòng tin cậy. Hàng triệu mẫu Ảnh đã được phân phát khắp nơi, tạo nên vô số phép lạ chữa lành và các cuộc hoán cải đức tin kinh ngạc (như cuộc trở lại đạo nổi tiếng của luật sư Do Thái Alphonse Ratisbonne năm 1842), khiến các tín hữu gọi đây là 'Ảnh Đức Mẹ Ban Ơn Phép Lạ'.",
        "scripture_reading": "Genesis 3:15",
        "suggested_prayer_en": "O Mary, conceived without sin, pray for us who have recourse to thee! You offered your Miraculous Medal as a sign of heavenly protection and abundant grace. Pour out the radiant rays of Christ's mercy upon our families, heal our spiritual blindness, and draw all hearts to the Sacred Heart of your Divine Son. Amen.",
        "suggested_prayer_vi": "Lạy Mẹ Maria vô nhiễm nguyên tội, xin cầu cho chúng con là kẻ chạy đến cùng Mẹ! Mẹ đã ban Mẫu Ảnh Phép Lạ làm dấu chỉ che chở của thiên đàng và tuôn đổ muôn ơn lành. Xin chiếu tỏa những luồng ánh sáng xót thương của Chúa Kitô trên gia đình chúng con, chữa lành sự mù lòa tâm linh và dẫn đưa muôn tâm hồn về cùng Thánh Tâm Con Cực Thánh của Mẹ. Amen.",
        "primary_sources": [
            {
                "label": "Chapelle Notre-Dame de la Médaille Miraculeuse Official Archives",
                "url": "https://www.medaille-miraculeuse.fr/en/",
                "type": "academic"
            },
            {
                "label": "Pope Pius XII - Bull of Canonization of Saint Catherine Labouré (1947)",
                "url": "https://www.vatican.va/content/pius-xii/fr/apost_constitutions/documents/hf_p-xii_apc_19470727_doctor-virtutum.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "shrine_of_our_lady_of_altotting",
        "category": "marian_apparition",
        "name_en": "Gnadenkapelle of Our Lady of Altötting",
        "name_vi": "Nguyện Đường Ân Sủng Đức Mẹ Altötting",
        "feast_day_association": "Feast of the Nativity of the Blessed Virgin Mary (September 8)",
        "location": {
            "shrine_or_basilica": "Gnadenkapelle (Chapel of Grace)",
            "city": "Altötting",
            "region_or_state": "Bavaria",
            "country": "Germany",
            "latitude": 48.2267,
            "longitude": 12.6775,
            "precision": "chapel_altar"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1489-09-01",
            "approving_authority": "Diocese of Passau / Pope Pius VI / Pope Benedict XVI (Golden Rose 2006)",
            "confidence": "confirmed",
            "confidence_note_en": "Celebrated since 1489 following the verified miraculous resuscitation of a drowned child; awarded the Golden Rose by Bavarian native Pope Benedict XVI in 2006.",
            "confidence_note_vi": "Được tôn kính từ năm 1489 sau phép lạ cải tử hoàn sinh của một bé trai chết đuối; được Đức Giáo hoàng Biển Đức XVI trao tặng Bông Hồng Vàng vào năm 2006."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Miraculous 14th-Century Linden-Wood Black Madonna Statue and Royal Heart Urns",
                "relic_name_vi": "Tượng Gỗ Đoạn Mẹ Đen Altötting Thế Kỷ 14 và Các Bình Bạc Đựng Trái Tim Hoàng Gia",
                "relic_type": "holy_icon",
                "reliquary_location": "Silver Rococo Altar inside the octagonal Gnadenkapelle"
            }
        ],
        "historical_summary_en": "The Chapel of Grace (*Gnadenkapelle*) in Altötting, Bavaria, is an octagonal pre-Romanesque structure dating back to around 700 AD, traditionally built on the site of an ancient baptistery founded by Saint Rupert of Salzburg. In 1489, a three-year-old boy drowned in the nearby river and his lifeless body was recovered. The grieving mother took the dead child and laid him before the wooden statue of the Virgin Mary in the chapel, praying with desperate tears; miraculously, life returned to the child before eyewitnesses.\n\nShortly thereafter, a second miracle occurred when a boy crushed under a horse cart was instantaneously restored to health after being commended to Our Lady of Altötting. The shrine immediately became the premier pilgrimage center of Central Europe, known as the 'Heart of Bavaria' (*Herz Bayerns*).\n\nTradition established that the hearts of Bavarian monarchs (including King Ludwig II) were preserved in ornate silver urns placed within niches surrounding the miraculous image. Pope Benedict XVI, born in nearby Marktl am Inn, considered Altötting his spiritual home, donating his episcopal ring to the shrine in 2006.",
        "historical_summary_vi": "Nguyện đường Ân Sủng (*Gnadenkapelle*) tại Altötting, vùng Bavaria, là công trình hình bát giác cổ kính xây dựng từ khoảng năm 700 sau Công Nguyên, tương truyền do Thánh Rupert thành Salzburg lập nên làm nhà rửa tội. Năm 1489, một bé trai 3 tuổi bị rơi xuống sông chết đuối và vớt được thi thể lạnh ngắt. Người mẹ đau đớn bế xác con đến đặt trước tượng Đức Mẹ bằng gỗ đoạn trong nguyện đường, khóc lóc cầu xin; lạ lùng thay, đứa trẻ bỗng mở mắt hồi sinh trước sự kinh ngạc của mọi người.\n\nNgay sau đó, phép lạ thứ hai diễn ra khi một cậu bé bị xe ngựa cán nát thân thể đã được chữa lành tức thì sau khi được phó thác cho Đức Mẹ Altötting. Đền thánh nhanh chóng trở thành trung tâm hành hương hàng đầu của Trung Âu, được mệnh danh là 'Trái Tim của Xứ Bavaria' (*Herz Bayerns*).\n\nTheo truyền thống vương triều, trái tim của các vị vua xứ Bavaria (kể cả Vua Ludwig II) đều được đặt trong các bình bạc chạm trổ tinh xảo đặt xung quanh linh tượng Mẹ. Đức Giáo hoàng Biển Đức XVI, người sinh trưởng tại Marktl am Inn gần đó, luôn coi Altötting là ngôi nhà tâm linh của ngài và đã dâng tặng chiếc nhẫn Giám mục của ngài cho đền thánh năm 2006.",
        "scripture_reading": "Luke 7:14-15",
        "suggested_prayer_en": "O Lady of Altötting, Mother of Grace and Patroness of Bavaria, you listened to the desperate prayers of a grieving mother and restored her child to life. Look with maternal pity upon our spiritual death and infirmities; restore us to vibrant life in Christ, and preserve our families in steadfast faith and charity. Amen.",
        "suggested_prayer_vi": "Lạy Đức Mẹ Altötting, Mẹ Ân Sủng và Quan Thầy Xứ Bavaria, Mẹ đã lắng nghe tiếng kêu van xé lòng của người mẹ mất con và ban ơn hồi sinh cho đứa trẻ. Xin Mẹ đoái nhìn đến những sự chết thiêng liêng và tật nguyền nơi tâm hồn chúng con; xin phục hồi sự sống thánh thiện trong Chúa Kitô và gìn giữ gia đình chúng con luôn kiên vững trong đức tin và đức ái. Amen.",
        "primary_sources": [
            {
                "label": "Gnadenkapelle Altötting Official Historical Chronicles",
                "url": "https://altoetting.de/en/",
                "type": "academic"
            },
            {
                "label": "Pope Benedict XVI - Address at the Chapel of Grace, Altötting (September 11, 2006)",
                "url": "https://www.vatican.va/content/benedict-xvi/en/speeches/2006/september/documents/hf_ben-xvi_spe_20060911_altoetting-welcome.html",
                "type": "vatican"
            }
        ]
    }
]

BATCH_4 = [
    {
        "sanctuary_id": "st_peter_basilica_vatican",
        "category": "apostolic_tomb",
        "name_en": "Papal Basilica of Saint Peter in the Vatican",
        "name_vi": "Đại Vương Cung Thánh Đường Thánh Phêrô tại Vatican",
        "feast_day_association": "Solemnity of Saints Peter and Paul, Apostles (June 29) / Chair of Saint Peter (February 22)",
        "location": {
            "shrine_or_basilica": "Basilica Papale di San Pietro in Vaticano",
            "city": "Vatican City",
            "region_or_state": "Rome",
            "country": "Vatican City State",
            "latitude": 41.9022,
            "longitude": 12.4539,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1626-11-18",
            "approving_authority": "Pope Urban VIII / Pope Paul VI (Announcement of Relics 1968)",
            "confidence": "confirmed",
            "confidence_note_en": "Archaeological excavations (1939-1949) directed by Msgr. Ludwig Kaas and epigraphist Margherita Guarducci identified the 2nd-century Aedicula, the Red Wall, and the Greek graffiti 'PETROS ENI' ('Peter is within'), confirming the tomb and bones of Saint Peter beneath Bernini's Baldacchino.",
            "confidence_note_vi": "Các cuộc khai quật khảo cổ (1939-1949) do Đức ông Ludwig Kaas và nhà văn bia Margherita Guarducci thực hiện đã xác định Nhà Tạm thế kỷ thứ 2, Bức Tường Đỏ và ký tự Hy Lạp 'PETROS ENI' ('Phêrô ở đây'), chứng minh thi hài và lăng mộ Thánh Phêrô bên dưới Tán Che Bernini."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Bones of Saint Peter the Apostle, Prince of the Apostles",
                "relic_name_vi": "Hài Cốt Thánh Phêrô Tông Đồ, Thủ Lãnh Các Tông Đồ",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Vatican Necropolis beneath the Papal Altar of the Confessio"
            }
        ],
        "historical_summary_en": "Saint Peter the Apostle, chosen by Jesus Christ as the Rock upon which He built His Church (*Matthew 16:18*), was martyred by inverted crucifixion in approximately AD 64-67 in the Circus of Caligula and Nero at the foot of the Vatican Hill. Christian believers secretly buried his body in an adjacent pagan necropolis along the Via Cornelia.\n\nIn the 4th century, Emperor Constantine the Great leveled the steep necropolis slope to construct the first monumental basilica directly over Peter's tomb, aligning the high altar with the Apostle's burial spot. During the Renaissance and Baroque eras, architects including Bramante, Michelangelo, and Bernini erected the current magnificent basilica, crowned by Michelangelo's soaring dome.\n\nBeneath Bernini's bronze Baldacchino lies the Confessio and the Vatican Necropolis. Rigorous modern excavations confirmed that the bone fragments discovered in a marble niche wrapped in purple cloth dyed with gold thread belong to a robust male of the first century, verifying two millennia of uninterrupted Christian tradition.",
        "historical_summary_vi": "Thánh Phêrô Tông Đồ, người được Chúa Giêsu Kitô tuyển chọn làm Tảng Đá xây dựng Hội Thánh (*Mátthêu 16:18*), đã chịu tử đạo bằng cách đóng đinh ngược đầu vào khoảng năm 64-67 sau Công Nguyên tại Đấu trường Caligula và Nero dưới chân đồi Vatican. Các tín hữu tiên khởi đã bí mật an táng thi hài ngài tại nghĩa trang liền kề dọc theo đường Via Cornelia.\n\nVào thế kỷ thứ 4, Hoàng đế Constantine Đại Đế đã san phẳng sườn đồi để xây dựng Vương cung Thánh đường đầu tiên đặt bàn thờ chính thẳng đứng trên ngôi mộ Thánh Tông đồ. Đến thời Phục Hưng và Baroque, các bậc thầy kiến trúc như Bramante, Michelangelo và Bernini đã xây dựng nên kiệt tác đền thờ ngày nay với mái vòm kỳ vĩ.\n\nBên dưới Tán Che bằng đồng của Bernini là Bàn Thờ Tuyên Xưng và Khu Nghĩa Trang Cổ Vatican. Các cuộc khai quật khảo cổ học thế kỷ 20 đã chứng minh những mẩu hài cốt tìm thấy trong hốc đá cẩm thạch bọc vải màu tím dệt chỉ vàng chính là xương của một người đàn ông thế kỷ thứ nhất, xác thực trọn vẹn truyền thống hai ngàn năm của Hội Thánh.",
        "scripture_reading": "Matthew 16:18-19",
        "suggested_prayer_en": "O Glorious Apostle Saint Peter, Prince of the Apostles and Rock of the Church, you shed your blood in Rome in ultimate testimony to the Risen Lord. Pray for the Holy Father, preserve the Church in spotless fidelity to the Gospel, and obtain for us the courage to profess our faith in Christ without fear. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Phêrô Tông Đồ vinh hiển, Thủ Lãnh các Tông Đồ và là Tảng Đá của Hội Thánh, ngài đã đổ máu đào tại Roma để làm chứng cho Chúa Kitô Phục Sinh. Xin ngài cầu bầu cho Đức Thánh Cha, gìn giữ Giáo hội luôn trung kiên với Tin Mừng và ban cho chúng con lòng can đảm tuyên xưng đức tin kiên vững trọn đời. Amen.",
        "primary_sources": [
            {
                "label": "Pope Paul VI - General Audience Announcing the Identification of Saint Peter's Relics (June 26, 1968)",
                "url": "https://www.vatican.va/content/paul-vi/it/audiences/1968/documents/hf_p-vi_aud_19680626.html",
                "type": "vatican"
            },
            {
                "label": "Fabbrica di San Pietro - Official Archaeological Necropolis Reports",
                "url": "https://www.basilicasanpietro.va/en/tomb-of-saint-peter",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "st_paul_outside_the_walls",
        "category": "apostolic_tomb",
        "name_en": "Papal Basilica of Saint Paul Outside the Walls",
        "name_vi": "Đại Vương Cung Thánh Đường Thánh Phaolô Ngoại Thành",
        "feast_day_association": "Solemnity of Saints Peter and Paul (June 29) / Conversion of Saint Paul (January 25)",
        "location": {
            "shrine_or_basilica": "Basilica Papale di San Paolo fuori le Mura",
            "city": "Rome",
            "region_or_state": "Lazio",
            "country": "Italy",
            "latitude": 41.8586,
            "longitude": 12.4764,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1854-12-10",
            "approving_authority": "Pope Pius IX / Consecrated by Pope Siricius (390 AD)",
            "confidence": "confirmed",
            "confidence_note_en": "Tomb inscription 'PAULO APOSTOLO MART...' dating to the 4th century confirmed under the Papal Altar; in 2009, Pope Benedict XVI announced carbon-14 dating confirming the interior tomb remains date to the 1st/2nd century.",
            "confidence_note_vi": "Bia mộ khắc dòng chữ thế kỷ thứ 4 'PAULO APOSTOLO MART...' được xác nhận dưới Bàn Thờ Giáo Hoàng; năm 2009, Đức Giáo hoàng Biển Đức XVI công bố kết quả giám định carbon-14 xác nhận hài cốt trong mộ có niên đại từ thế kỷ thứ nhất/thứ hai."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Sarcophagus and Relics of Saint Paul the Apostle and His Prison Chains",
                "relic_name_vi": "Quan Tài Hài Cốt Thánh Phaolô Tông Đồ và Dây Xích Tù Ngục",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Directly beneath the Papal High Altar Confessio"
            }
        ],
        "historical_summary_en": "Saint Paul of Tarsus, the 'Apostle to the Gentiles,' was beheaded around AD 64-67 along the Via Laurentina at *Aquae Salviae* (modern Tre Fontane) during the Neronian persecution. As a Roman citizen, Paul was spared crucifixion and suffered decapitation by sword. A devout Roman matron named Lucina retrieved his body and interred it in her family estate alongside the Via Ostiense, two miles outside the Aurelian Walls of Rome.\n\nEmperor Constantine erected the first basilica over the tomb in 324 AD, later expanded by Emperors Valentinian II, Theodosius I, and Arcadius into a magnificent five-aisled basilica. Although a catastrophic fire destroyed much of the medieval basilica in 1823, it was faithfully reconstructed by contributions from Catholic and world leaders, rededicated by Pope Pius IX in 1854.\n\nIn December 2006, Vatican archaeologists excavated a massive marble sarcophagus beneath the papal altar bearing the 4th-century inscription *PAULO APOSTOLO MART...* ('To Paul, Apostle, Martyr'). Scientific probes revealed fragments of bone, precious incense, and linen interwoven with pure gold lamé thread.",
        "historical_summary_vi": "Thánh Phaolô thành Tarsô, 'Tông Đồ Dân Ngoại', đã chịu trảm quyết vì đạo vào khoảng năm 64-67 sau Công Nguyên tại *Aquae Salviae* (nay là Tre Fontane) dọc đường Via Laurentina dưới thời bạo chúa Nero. Vì mang quyền công dân La Mã, ngài không bị đóng đinh mà chịu tử đạo bằng gươm chém. Một phụ nữ quý tộc đạo đức tên là Lucina đã thu nhận thi hài ngài và an táng trong khu đất gia đình bên đường Via Ostiense, cách tường thành Roma hai dặm.\n\nHoàng đế Constantine đã dựng ngôi thánh đường đầu tiên trên mộ ngài vào năm 324, sau đó được các Hoàng đế Valentinian II, Theodosius I và Arcadius mở rộng thành đại thánh đường nguy nga gồm 5 gian. Dù một trận hỏa hoạn lớn thiêu rụi phần lớn ngôi đền năm 1823, thánh đường đã được tái thiết hoàn hảo nhờ sự đóng góp của giáo hội toàn cầu và được Đức Piô IX thánh hiến năm 1854.\n\nTháng 12 năm 2006, các nhà khảo cổ Vatican đã khai quật khối quách đá cẩm thạch khổng lồ nằm ngay dưới bàn thờ chính mang dòng chữ khắc thế kỷ thứ 4: *PAULO APOSTOLO MART...* ('Kính dâng Phaolô, Tông đồ, Tử đạo'). Các mẫu xét nghiệm khoa học đã tìm thấy các mảnh xương thánh, hương trầm quý và sợi vải lanh dệt chỉ vàng ròng.",
        "scripture_reading": "2 Timothy 4:7-8",
        "suggested_prayer_en": "O Great Apostle Saint Paul, Teacher of the Gentiles and Herald of Christ, you ran the race and kept the faith unto the shedding of your blood. Ignite in our hearts a burning zeal for the Gospel; teach us to glory only in the Cross of our Lord Jesus Christ, and make us fearless witnesses to His Truth. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Phaolô Tông Đồ vinh hiển, Thầy Dạy Dân Ngoại và là Sứ Giả của Chúa Kitô, ngài đã chiến đấu trong trận chiến cao đẹp, đã chạy hết chặng đường và giữ vững đức tin cho đến giọt máu cuối cùng. Xin thắp lên trong tâm hồn chúng con ngọn lửa nhiệt thành truyền giáo; dạy chúng con chỉ tự hào nơi Thập Giá Chúa Giêsu Kitô và trở nên những chứng nhân can trường cho Chân Lý. Amen.",
        "primary_sources": [
            {
                "label": "Pope Benedict XVI - Homily for the Conclusion of the Pauline Year (June 28, 2009)",
                "url": "https://www.vatican.va/content/benedict-xvi/en/homilies/2009/documents/hf_ben-xvi_hom_20090628_chius-anno-paolino.html",
                "type": "vatican"
            },
            {
                "label": "Papal Basilica of Saint Paul Outside the Walls Official Archaeological Documentation",
                "url": "https://www.basilicasanpaolo.org/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "st_james_santiago_de_compostela",
        "category": "apostolic_tomb",
        "name_en": "Cathedral of Santiago de Compostela",
        "name_vi": "Đại Vương Cung Thánh Đường Santiago de Compostela",
        "feast_day_association": "Feast of Saint James the Greater, Apostle (July 25)",
        "location": {
            "shrine_or_basilica": "Catedral Basílica de Santiago de Compostela",
            "city": "Santiago de Compostela",
            "region_or_state": "Galicia",
            "country": "Spain",
            "latitude": 42.8806,
            "longitude": -8.5446,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1884-11-01",
            "approving_authority": "Pope Leo XIII (Papal Bull Deus Omnipotens) / Bishop Theodemir of Iria Flavia (814 AD)",
            "confidence": "confirmed",
            "confidence_note_en": "Rediscovered in 814 AD by the hermit Pelagius guided by heavenly stars (*Campus Stellae*); definitively confirmed by Pope Leo XIII in the Papal Bull *Deus Omnipotens* (1884) following archaeological excavations by Archbishop Payá y Rico.",
            "confidence_note_vi": "Được ẩn sĩ Pelagius tái khám phá năm 814 dưới sự dẫn lối của các vì sao trên trời (*Campus Stellae*); được Đức Giáo hoàng Lêô XIII chính thức xác nhận qua Tông sắc *Deus Omnipotens* năm 1884 sau cuộc khai quật khảo cổ của Tổng Giám mục Payá y Rico."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Relics of Saint James the Greater and his Disciples Theodore and Athanasius",
                "relic_name_vi": "Hài Cốt Thánh Giacôbê Tiền Tông Đồ cùng Hai Môn Đệ Theodorus và Athanasius",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Silver Casket in the Crypt beneath the High Altar"
            }
        ],
        "historical_summary_en": "Saint James the Greater, son of Zebedee and brother of Saint John the Evangelist, was among the inner circle of Christ's apostles who witnessed the Transfiguration and the Agony in Gethsemane. After evangelizing the Iberian Peninsula, James returned to Judea, where in AD 44 he became the first apostle to suffer martyrdom, beheaded by order of King Herod Agrippa I (*Acts 12:1-2*).\n\nAccording to early medieval accounts, his faithful disciples Theodore and Athanasius transported his body by sea to the coast of Galicia, interring him in a Roman mausoleum. In approximately 814 AD, a hermit named Pelagius followed a miraculous shower of lights above the forest to discover the long-forgotten Roman crypt (*Campus Stellae*, 'Field of Stars' / Compostela). Bishop Theodemir verified the apostolic tomb, prompting King Alfonso II of Asturias to construct the first sanctuary.\n\nThroughout the Middle Ages, the *Camino de Santiago* became the artery of European unity, drawing millions of pilgrims wearing the scallop shell badge across France and Spain. The Cathedral of Santiago de Compostela remains one of Christianity's supreme pilgrimage goals.",
        "historical_summary_vi": "Thánh Giacôbê Tiền, con ông Giêbêđê và là anh của Thánh Sử Gioan, thuộc nhóm ba môn đệ thân tín nhất của Chúa Giêsu từng chứng kiến biến cố Biến Hình trên núi Tabor và sự Thống Khổ nơi vườn Cây Dầu. Sau khi rao giảng Tin Mừng tại bán đảo Iberia, ngài trở về Judea và vào năm 44 sau Công Nguyên, ngài trở thành vị Tông Đồ đầu tiên chịu tử đạo, bị chém đầu theo lệnh vua Herod Agrippa I (*Công vụ 12:1-2*).\n\nTheo truyền tích Trung Cổ, hai môn đệ trung thành là Theodorus và Athanasius đã đưa thi hài ngài vượt biển về lại bờ biển xứ Galicia và an táng trong một ngôi mộ La Mã cổ. Khoảng năm 814, một ẩn sĩ tên là Pelagius nhìn thấy những luồng ánh sao kỳ lạ dẫn đường đến ngôi mộ cổ trong rừng (*Campus Stellae*, 'Cánh Đồng Sao' / Compostela). Đức Giám mục Theodemir đã xác thực lăng mộ và Vua Alfonso II xứ Asturias đã cho xây dựng ngôi thánh đường đầu tiên.\n\nSuốt thời Trung Cổ, Con Đường Hành Hương *Camino de Santiago* đã trở thành huyết mạch kết nối toàn cõi Châu Âu, đưa hàng triệu người mang biểu tượng vỏ sò hành hương từ khắp nơi về kính viếng mộ ngài. Đại Vương Cung Thánh Đường Santiago de Compostela ngày nay vẫn là đích đến tâm linh thiêng liêng rực rỡ bậc nhất.",
        "scripture_reading": "Acts 12:1-2",
        "suggested_prayer_en": "O Holy Apostle Saint James, Patron of Pilgrims and First Martyr among the Apostles, you walked the arduous roads to proclaim Christ to the ends of the earth. Guide our earthly pilgrimage; grant us endurance in trials, protect all travelers on the way, and bring us safely to the eternal homeland of Heaven. Through Christ our Lord. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Giacôbê Tông Đồ vinh hiển, Đấng Bảo Trợ các khách hành hương và là Vị Tử Đạo tiên khởi trong hàng Tông Đồ, ngài đã băng qua vạn dặm đường dài để rao giảng Tin Mừng cho muôn dân. Xin đồng hành cùng cuộc hành hương trần thế của chúng con; ban ơn kiên trì nâng đỡ những người lữ hành trên mọi nẻo đường và dẫn đưa chúng con về bến bờ quê hương Vĩnh Cửu. Nhờ Đức Kitô, Chúa chúng con. Amen.",
        "primary_sources": [
            {
                "label": "Pope Leo XIII - Papal Bull Deus Omnipotens (November 1, 1884)",
                "url": "https://www.vatican.va/content/leo-xiii/la/apost_constitutions/documents/hf_l-xiii_apc_18841101_deus-omnipotens.html",
                "type": "vatican"
            },
            {
                "label": "Archdiocese of Santiago de Compostela Official Cathedral Archives",
                "url": "https://catedraldesantiago.es/en/",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "st_john_the_evangelist_ephesus",
        "category": "apostolic_tomb",
        "name_en": "Basilica and Tomb of Saint John the Evangelist",
        "name_vi": "Đền Thờ và Lăng Mộ Thánh Gioan Tông Đồ tại Ephesus",
        "feast_day_association": "Feast of Saint John, Apostle and Evangelist (December 27)",
        "location": {
            "shrine_or_basilica": "Basilica of Saint John (Ayasuluk Hill)",
            "city": "Selçuk (Ephesus)",
            "region_or_state": "İzmir Province",
            "country": "Turkey",
            "latitude": 37.9525,
            "longitude": 27.3672,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "0565-01-01",
            "approving_authority": "Emperor Justinian I / Early Church Patristic Tradition (Polycrates of Ephesus / Eusebius)",
            "confidence": "confirmed",
            "confidence_note_en": "Documented by Bishop Polycrates of Ephesus (c. 190 AD) and Eusebius of Caesarea; monumental 6-domed Justinian Basilica excavated by Austrian Archaeological Institute (1927-present) confirming the 1st-century apostolic tomb.",
            "confidence_note_vi": "Được Giám mục Polycrates xứ Ephesus ghi nhận (khoảng năm 190) và Sử gia Eusebius thành Caesarea xác thực; Đại thánh đường 6 mái vòm thời Hoàng đế Justinian được Viện Khảo cổ Áo khai quật xác nhận ngôi mộ tông đồ thế kỷ thứ nhất."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Tomb of Saint John the Apostle and Beloved Disciple",
                "relic_name_vi": "Lăng Mộ Thánh Gioan Tông Đồ, Môn Đệ Chúa Yêu",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Central Crypt Altar under the Dome of the Basilica of Saint John, Ayasuluk"
            }
        ],
        "historical_summary_en": "Saint John the Evangelist, the 'Beloved Disciple' who rested his head upon Jesus' chest at the Last Supper and stood with the Virgin Mary at the foot of the Cross (*John 19:26-27*), accompanied Our Lady to Ephesus in Asia Minor after the dispersal of the apostles. Following his exile on the Isle of Patmos, where he penned the Book of Revelation, John returned to Ephesus, where he governed the churches of Asia, composed the Fourth Gospel and three epistles, and died in peace at extreme old age around AD 100.\n\nPatristic writers, including Saint Irenaeus of Lyons and Bishop Polycrates of Ephesus in his letter to Pope Victor I (c. 190 AD), recorded that John was buried on Ayasuluk Hill overlooking Ephesus. In the 4th century, Constantine built a church over the tomb, which Emperor Justinian I and Empress Theodora replaced in the 6th century with a colossal six-domed cruciform basilica modeled after the Church of the Holy Apostles in Constantinople.\n\nThroughout late antiquity and the Middle Ages, pilgrims flocked to the tomb, collecting the holy dust (*manna*) that miraculously issued from the apertures of the tomb on the apostle's feast day.",
        "historical_summary_vi": "Thánh Gioan Tông Đồ, 'Người Môn Đệ Chúa Yêu', người đã tựa đầu vào ngực Chúa Giêsu trong Bữa Tiệc Ly và đứng kiên trung dưới chân Thập Giá cùng Đức Mẹ (*Gioan 19:26-27*), đã phụng dưỡng Đức Mẹ và đến sinh sống tại Ephesus thuộc vùng Tiểu Á sau khi các tông đồ phân tán đi truyền giáo. Sau thời gian bị lưu đày tại đảo Patmos—nơi ngài viết sách Khải Huyền—Thánh Gioan trở về Ephesus, coi sóc các giáo đoàn miền Tiểu Á, hoàn tất sách Phúc Âm thứ Tư cùng ba bức thư tông đồ và qua đời bình an ở tuổi đại thọ khoảng năm 100 sau Công Nguyên.\n\nCác Giáo phụ tiên khởi như Thánh Irenaeus thành Lyon và Giám mục Polycrates xứ Ephesus trong thư gửi Đức Giáo hoàng Victor I (năm 190) đều xác nhận Thánh Gioan được an táng trên đồi Ayasuluk nhìn xuống Ephesus. Vào thế kỷ thứ 4, Hoàng đế Constantine dựng thánh đường trên mộ ngài, và đến thế kỷ thứ 6 Hoàng đế Justinian I cùng Hoàng hậu Theodora đã xây dựng một đại vương cung thánh đường 6 mái vòm hình chữ thập tráng lệ.\n\nSuốt thời Cổ đại và Trung Cổ, các đoàn khách hành hương từ khắp nơi trên thế giới đã đổ về viếng lăng mộ Thánh Gioan, tôn kính vị Tông Đồ của Tình Yêu đã ghi lại những mạc khải thâm sâu nhất về Ngôi Lời Thiên Chúa.",
        "scripture_reading": "John 21:20-24",
        "suggested_prayer_en": "O Beloved Apostle Saint John, Herald of the Divine Word and Theologian of Love, you contemplated the mysteries of the Sacred Heart and received Mary as your Mother at the Cross. Grant that we may abide deeply in Christ's love, hear His divine voice with clarity, and love one another in truth and deed. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Gioan Tông Đồ kính yêu, Sứ Giả của Ngôi Lời Thiên Chúa và là Nhà Thần Học của Tình Yêu, ngài đã được kề bên Thánh Tâm Chúa và nhận Đức Mẹ làm Mẹ dưới chân Thập Giá. Xin cho chúng con biết hằng ở lại trong tình yêu của Chúa Kitô, biết lắng nghe tiếng Chúa trong thinh lặng và biết yêu thương nhau bằng hành động và chân lý. Amen.",
        "primary_sources": [
            {
                "label": "Eusebius of Caesarea - Church History (Historia Ecclesiastica, Book III)",
                "url": "https://www.newadvent.org/fathers/250103.htm",
                "type": "encyclopedia"
            },
            {
                "label": "Austrian Archaeological Institute (ÖAI) - Ephesus Ayasuluk Excavation Reports",
                "url": "https://www.oeaw.ac.at/en/oeai/research/classical-studies/ephesos",
                "type": "academic"
            }
        ]
    },
    {
        "sanctuary_id": "st_andrew_apostle_amalfi",
        "category": "apostolic_tomb",
        "name_en": "Cathedral of Saint Andrew the Apostle (Amalfi)",
        "name_vi": "Đại Vương Cung Thánh Đường Thánh Anrê Tông Đồ (Amalfi)",
        "feast_day_association": "Feast of Saint Andrew the Apostle (November 30)",
        "location": {
            "shrine_or_basilica": "Cattedrale di Sant'Andrea Apostolo (Duomo di Amalfi)",
            "city": "Amalfi",
            "region_or_state": "Salerno, Campania",
            "country": "Italy",
            "latitude": 40.6342,
            "longitude": 14.6028,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1208-05-08",
            "approving_authority": "Cardinal Pietro Capuano / Pope Innocent III",
            "confidence": "confirmed",
            "confidence_note_en": "Relics translated from Constantinople to Amalfi in 1208 by Cardinal Pietro Capuano following the Fourth Crusade; celebrated continuously with the verified miraculous liquefaction of the 'Manna of Saint Andrew'.",
            "confidence_note_vi": "Hài cốt được Đức Hồng y Pietro Capuano chuyển từ Constantinople về Amalfi năm 1208 sau cuộc Thập Tự Chinh thứ tư; được Giáo hội tôn kính với hiện tượng tiết ra chất dầu thơm phép lạ 'Manna của Thánh Anrê'."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Major Relics and Skull of Saint Andrew the First-Called Apostle",
                "relic_name_vi": "Xương Thánh và Hộp Sọ của Thánh Anrê Tông Đồ, Đấng Được Kêu Gọi Đầu Tiên",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Crypt of Saint Andrew beneath the High Altar of Amalfi Cathedral"
            }
        ],
        "historical_summary_en": "Saint Andrew the Apostle, brother of Saint Simon Peter and the *Protokletos* ('First-Called') by Christ, preached the Gospel across Greece, Thrace, and the Black Sea region before suffering martyrdom in Patras, Achaea, around AD 60. Bound to a decussate (X-shaped) cross, Andrew preached the faith continuously to the crowd for two days from the cross before breathing his last.\n\nIn AD 357, his relics were solemnly translated to the Church of the Holy Apostles in Constantinople by order of Emperor Constantius II. In 1208, following the Fourth Crusade, Cardinal Pietro Capuano brought the sacred body of the Apostle to his native maritime republic of Amalfi, enshrining the relics inside the magnificent crypt of the cathedral.\n\nFor over eight centuries, a fragrant, crystal-clear liquid known as the 'Manna of Saint Andrew' (*La Manna di Sant'Andrea*) has periodically issued from the tomb in the crypt during major liturgical feasts, collected in glass vials by the clergy before the faithful as a tangible sign of apostolic blessing.",
        "historical_summary_vi": "Thánh Anrê Tông Đồ, anh trai của Thánh Phêrô và là *Protokletos* ('Đấng Được Kêu Gọi Đầu Tiên') bởi Chúa Giêsu, đã rao giảng Tin Mừng khắp Hy Lạp, Thrace và vùng Biển Đen trước khi chịu tử đạo tại Patras, Achaea vào khoảng năm 60 sau Công Nguyên. Bị trói vào cây thập giá hình chữ X, Thánh Anrê vẫn kiên cường rao giảng đức tin liên tục suốt hai ngày cho đám đông trước khi trút hơi thở cuối cùng.\n\nNăm 357, hài cốt ngài được Hoàng đế Constantius II rước về an vị tại Đại thánh đường Các Thánh Tông Đồ ở Constantinople. Đến năm 1208, sau cuộc Thập Tự Chinh thứ tư, Đức Hồng y Pietro Capuano đã rước thi hài Thánh Tông đồ về quê hương Amalfi và cung hiến trong gian hầm mộ lộng lẫy dưới bàn thờ chính nhà thờ chính tòa.\n\nSuốt hơn tám thế kỷ qua, một chất lỏng trong suốt ngát hương thơm gọi là 'Manna của Thánh Anrê' (*La Manna di Sant'Andrea*) vẫn kỳ diệu rỉ ra từ ngôi mộ trong hầm vào các ngày lễ trọng, được các giáo sĩ thu nhận vào bình thủy tinh trước sự chứng kiến của giáo dân như dấu chỉ phúc lành tông truyền.",
        "scripture_reading": "John 1:40-42",
        "suggested_prayer_en": "O Holy Apostle Saint Andrew, First-Called Disciple and Lover of the Cross, you joyfully recognized Jesus as the Messiah and led your brother Peter to Him. Teach us to embrace our daily crosses with holy joy, make us zealous heralds of Christ, and draw all separated brethren into the full unity of the Church. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Anrê Tông Đồ vinh hiển, Đấng Được Kêu Gọi Đầu Tiên và là Người Mến Yêu Thập Giá, ngài đã hân hoan nhận ra Chúa Giêsu là Đấng Cứu Thế và dẫn đưa người em Phêrô đến cùng Người. Xin dạy chúng con biết vui lòng vác thánh giá hằng ngày, ban cho chúng con lòng nhiệt thành loan báo Tin Mừng và dẫn đưa mọi người về trong sự hiệp nhất hoàn hảo của Hội Thánh. Amen.",
        "primary_sources": [
            {
                "label": "Arcidiocesi di Amalfi-Cava de' Tirreni Official Historical Records",
                "url": "https://www.diocesiaic.it/",
                "type": "academic"
            },
            {
                "label": "Pope Paul VI - Apostolic Letter on the Return of Saint Andrew's Relic to Patras (1964)",
                "url": "https://www.vatican.va/content/paul-vi/la/apost_letters/documents/hf_p-vi_apl_19640922_in-patrensi.html",
                "type": "vatican"
            }
        ]
    },
    {
        "sanctuary_id": "st_thomas_apostle_mylapore",
        "category": "apostolic_tomb",
        "name_en": "San Thome Cathedral Basilica (Tomb of Saint Thomas)",
        "name_vi": "Đại Vương Cung Thánh Đường San Thome (Lăng Mộ Thánh Tôma Tông Đồ)",
        "feast_day_association": "Feast of Saint Thomas the Apostle (July 3)",
        "location": {
            "shrine_or_basilica": "National Shrine of Saint Thomas Cathedral Basilica",
            "city": "Mylapore, Chennai",
            "region_or_state": "Tamil Nadu",
            "country": "India",
            "latitude": 13.0336,
            "longitude": 80.2783,
            "precision": "crypt"
        },
        "canonical_status": {
            "approval_or_consecration_date": "1896-01-01",
            "approving_authority": "Pope Leo XIII / Pope Benedict XVI (National Shrine 2006)",
            "confidence": "confirmed",
            "confidence_note_en": "Continuous historical tradition of the Saint Thomas Christians (Nasranis) attested by Saint Ephrem the Syrian (4th c.) and Marco Polo (1292); archaeological surveys confirm ancient apostolic tomb beneath the high altar.",
            "confidence_note_vi": "Truyền thống lịch sử liên tục của cộng đoàn Kitô hữu Thánh Tôma (Nasrani) được Thánh Ephrem xứ Syria (thế kỷ 4) và Marco Polo (1292) ghi nhận; khảo cổ học xác thực lăng mộ tông đồ cổ xưa dưới bàn thờ chính."
        },
        "primary_relics": [
            {
                "relic_name_en": "The Bone Relics of Saint Thomas the Apostle and the Miraculous Bleeding Cross",
                "relic_name_vi": "Xương Thánh Tôma Tông Đồ và Cây Thập Tự Chảy Máu Phép Lạ",
                "relic_type": "1st_class_bone",
                "reliquary_location": "Underground Tomb Chapel beneath the High Altar of San Thome Basilica"
            }
        ],
        "historical_summary_en": "Saint Thomas the Apostle, famed for his confession of faith *'My Lord and my God!'* (*John 20:28*), traveled beyond the eastern frontiers of the Roman Empire, evangelizing Mesopotamia, Persia, and reaching the Malabar Coast of India (Muziris / Cranganore) in AD 52. He established seven flourishing Christian communities (*Ezharappallikal*) along the coast of Kerala before journeying east to the Coromandel Coast.\n\nIn AD 72, while praying at St. Thomas Mount near Mylapore (modern Chennai), Saint Thomas was pierced by a lance and martyred for the Christian faith. His disciples interred his body at Mylapore on the shores of the Bay of Bengal, where his tomb became a beacon of prayer for Indian Christians across two millennia.\n\nPatristic writers from Saint Ephrem in Edessa to Saint Gregory of Tours chronicled the Indian pilgrimage to Saint Thomas' tomb. Portuguese explorers rebuilt the sanctuary in the 16th century, and the current majestic Neo-Gothic basilica, built in 1896, enshrines the tomb in its subterranean crypt alongside the sacred relic of the lance tip that pierced the Apostle.",
        "historical_summary_vi": "Thánh Tôma Tông Đồ, vị tông đồ nổi tiếng với lời tuyên xưng đức tin bất hủ *'Lạy Chúa của con, lạy Thiên Chúa của con!'* (*Gioan 20:28*), đã vượt qua biên giới phía đông của Đế chế La Mã, rao giảng Tin Mừng qua Lưỡng Hà, Ba Tư và cập bến bờ biển Malabar của Ấn Độ vào năm 52 sau Công Nguyên. Ngài lập nên 7 cộng đoàn Kitô hữu đầu tiên (*Ezharappallikal*) tại Kerala trước khi tiến sang bờ biển Coromandel.\n\nNăm 72 sau Công Nguyên, khi đang cầu nguyện trên đỉnh đồi Thánh Tôma gần Mylapore (nay là Chennai), ngài đã bị những kẻ thù ghét đạo đâm ngọn giáo xuyên qua tim tử đạo. Các môn đệ đã an táng thi hài ngài tại bờ biển Mylapore, nơi ngôi mộ trở thành cội nguồn đức tin của các Kitô hữu Ấn Độ suốt hai ngàn năm.\n\nCác giáo phụ cổ đại như Thánh Ephrem và sử gia phương Tây Marco Polo đều ghi chép về các đoàn hành hương đến mộ Thánh Tôma. Ngôi đại vương cung thánh đường phong cách Tân Gothic xây dựng năm 1896 ngày nay bảo tồn lăng mộ tông đồ nguyên thủy dưới hầm mộ cùng mũi giáo thánh đã đâm xuyên trái tim vị tông đồ.",
        "scripture_reading": "John 20:26-29",
        "suggested_prayer_en": "O Apostle Saint Thomas, who touched the sacred wounds of the Risen Lord and cried out in adoration, 'My Lord and my God!', strengthen our faith in moments of doubt. Protect the Church in India and throughout Asia, and grant that we may surrender our lives wholly to Christ in unwavering faith. Amen.",
        "suggested_prayer_vi": "Lạy Thánh Tôma Tông Đồ vinh hiển, ngài đã được chạm vào các vết thương thánh của Chúa Phục Sinh và sấp mình tuyên xưng 'Lạy Chúa của con, lạy Thiên Chúa của con!', xin củng cố đức tin cho chúng con trong những lúc nghi nan thử thách. Xin bảo vệ Giáo hội tại Ấn Độ và khắp Châu Á, và ban cho chúng con lòng tận hiến trọn vẹn cho Chúa Kitô đến muôn đời. Amen.",
        "primary_sources": [
            {
                "label": "Catholic Bishops' Conference of India (CBCI) - San Thome National Shrine Records",
                "url": "https://www.cbci.in/",
                "type": "academic"
            },
            {
                "label": "Pope John Paul II - Address at the Tomb of the Apostle Saint Thomas, Madras (February 5, 1986)",
                "url": "https://www.vatican.va/content/john-paul-ii/en/speeches/1986/february/documents/hf_jp-ii_spe_19860205_madras-san-tome.html",
                "type": "vatican"
            }
        ]
    }
]

def main():
    target_dir = "Anno/Resources/SacredSanctuaries"
    os.makedirs(target_dir, exist_ok=True)
    
    for item in BATCH_3 + BATCH_4:
        filename = f"{item['sanctuary_id']}.json"
        path = os.path.join(target_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False, indent=2)
        print(f"Generated {filename}")

if __name__ == "__main__":
    main()

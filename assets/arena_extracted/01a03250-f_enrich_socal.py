import json
with open('socal_vietnamese_catholic_pilgrimage_la_vang.json', 'r', encoding='utf-8') as f:
    d=json.load(f)

d['overview_en'] = d['overview_en'] + " For older immigrants who fled by boat after 1975, this sanctuary is not tourism — it is a homecoming. The 12-foot marble statue wears the áo dài they wore in Quảng Trị; the steel ribbon curls like the jungle paths their ancestors walked; the rock embedded in the landscape was brought from Vietnam itself. Visitors can touch the statue, read each of the 117 martyrs' names and deaths, walk the rosary garden, attend Vietnamese-language Mass at nearby parishes, or simply sit in silence beneath the glass canopy. For a congregation: a half-day trip (morning Mass at a Vietnamese parish, then 30 minutes to the shrine, 2 hours of prayer and reading, return by afternoon) works beautifully. For individuals: arrive at opening, pray at the martyrs wall, touch the statue, then sit with the brick from the original shrine — a physical bridge between Quảng Trị and Orange County. For a longer pilgrimage, pair with a visit to Our Lady of Guadalupe at Mission San Juan Capistrano (south) or St. Barbara in Westminster (north), making a 2-day or 3-day circuit of Vietnamese Catholic sites in Southern California."

d['overview_vi'] = d['overview_vi'] + " Đối với những người lớn tuổi đã chạy trốn bằng thuyền sau năm 1975, đền thờ này không phải là du lịch — nó là một cuộc về nhà. Tượng đá cẩm thạch cao 12 feet mặc áo dài mà họ đã mặc ở Quảng Trị; dải thép cuộn như những con đường rừng mà tổ tiên họ đã bước; đá được hòa nhập vào cảnh quan được mang từ Việt Nam. Người viếng có thể chạm vào tượng, đọc từng cái tên và cái chết của 117 vị tử đạo, đi bộ trong vườn chuỗi tràng hạt, tham dự Thánh Lễ bằng tiếng Việt tại các giáo xứ gần đó, hoặc đơn giản ngồi im lặng dưới mái vòm kính. Cho một cộng đồng: một chuyến đi nửa ngày (Thánh Lễ buổi sáng tại giáo xứ Việt Nam, sau đó 30 phút đến đền thờ, 2 giờ cầu nguyện và đọc, trở về buổi chiều) hoạt động tuyệt vời. Cho một cá nhân: đến lúc mở cửa, cầu nguyện tại bức tường các vị tử đạo, chạm vào tượng, sau đó ngồi với viên gạch từ đền thờ nguyên thủy — một cầu nối vật lý giữa Quảng Trị và Quận Orange. Để có một cuộc hành hương dài hơn, kết hợp với chuyến viếng Đức Mẹ Guadalupe tại Mission San Juan Capistrano (phía nam) hoặc Thánh Barbara ở Westminster (phía bắc), tạo thành một vòng tuần hoàn 2 hoặc 3 ngày qua các địa điểm Công Giáo Việt Nam tại Miền Nam California."

activities = {
    "our_lady_la_vang_shrine_christ_cathedral": "Things to do for this station: (1) Touch the marble statue's áo dài — feel the Vietnamese fabric; (2) Read the 117 martyrs' steel panel slowly; (3) Light a candle at the outdoor altar; (4) Walk the rosary garden with a prayer for Vietnam; (5) Attend a Vietnamese-language Mass at a nearby parish (St. Barbara, Westminster, or Christ Cathedral's own Vietnamese services); (6) Bring a photo from your home church in Vietnam and leave it briefly at the statue's feet.",
    "martyrs_wall_117_vietnamese_christian": "Things to do for the martyrs wall: (1) Read slowly — each name has a method of death; (2) Say a Hail Mary for each martyr; (3) If with a congregation, form a circle around the wall and pray together; (4) Take a photo of the wall to share with family in Vietnam so they know their martyrs are remembered in California.",
    "rosary_gardens_christ_cathedral_pilgrimage": "Things to do in the gardens: (1) Walk slowly — the stones from Vietnam underfoot; (2) Sit at the outdoor Mass altar and imagine Quảng Trị's jungle becoming this plaza; (3) For groups: host a communal Vietnamese prayer (Mân Côi / Rosary) in the plaza; (4) For older immigrants: sit near the steel ribbon, which loops like the path from persecution to safety."
}

for w in d['waypoints']:
    wid = w['waypoint_id']
    if wid in activities:
        w['historical_summary_en'] = w['historical_summary_en'].rstrip('.') + '. ' + activities[wid]
    if wid == 'our_lady_la_vang_shrine_christ_cathedral':
        w['historical_summary_vi'] = w['historical_summary_vi'].rstrip('.') + '. Đối với người lớn tuổi, vẻ đẹp của tượng đá này — áo dài, khăn đống, bàn tay bế Hài Nhi — chính là vẻ đẹp của quê hương mà họ mang theo trong tim; khi chạm vào tượng, họ không chỉ chạm vào đá mà chạm vào ký ức của một Vietnam từng bị bách hại nhưng vẫn sống.'
    elif wid == 'martyrs_wall_117_vietnamese_christian':
        w['historical_summary_vi'] = w['historical_summary_vi'].rstrip('.') + '. Khi đọc từng cái tên trên bức tường thép, người hành hương già nên dành thời gian — mỗi cái tên là một câu chuyện về một người mẹ, một cha, một đứa trẻ đã không chối đức tin; hãy nói một Kinh Lạy Nữ Vương cho từng vị, để các vị không bị quên trong đất Mỹ.'
    elif wid == 'rosary_gardens_christ_cathedral_pilgrimage':
        w['historical_summary_vi'] = w['historical_summary_vi'].rstrip('.') + '. Vườn chuỗi tràng hạt này là nơi để người hành hương già bước chậm — không vội vàng — vì mỗi bước chân trên đá từ Quảng Trị là một bước chân về nhà; hãy mang theo một bức ảnh từ nhà thờ Việt Nam và để nó trên băng ghế, như một lời cầu nguyện thầm lặng.'

with open('socal_vietnamese_catholic_pilgrimage_la_vang.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print('Enriched with awe, beauty, cultural depth, and practical activities.')

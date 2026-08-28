import SwiftUI

struct TodayView: View {
    let entry: AnnoEntry
    @Binding var language: LanguageMode
    let onShowSources: () -> Void

    @State private var isBookmarked: Bool = false
    @State private var bookmarkScale: CGFloat = 1.0
    @State private var isShowingArtCanvas: Bool = false

    private var localizedText: LocalizedEntryText {
        LocalizedEntryText(entry: entry, language: language)
    }

    private var calendarPillsData: [(label: String, value: String)] {
        [
            ("Julian", entry.calendars.julian),
            ("Hebrew", entry.calendars.hebrew),
            ("Islamic", entry.calendars.islamicUmmAlQura),
            ("Coptic", entry.calendars.coptic),
            ("Ethiopian", entry.calendars.ethiopian)
        ]
    }

    var body: some View {
        ScrollView {
            VStack(spacing: 28) {
                dateBlock
                headerSection
                artworkCard
                quickActionsBar
                summaryCard

                if let place = entry.place {
                    sacredPlaceCard(place: place)
                }

                if let connectedRoute = SacredGeographyLoader.shared.routes.first(where: { $0.isLiturgicallyConnected(to: entry) }) {
                    liturgicalPilgrimageCard(route: connectedRoute)
                }

                prayerPromptCard
                sourceConfidenceCard
            }
            .padding(.horizontal, 20)
            .padding(.top, 16)
            .padding(.bottom, 48)
        }
        .liturgicalAtmosphere(named: entry.liturgical.color)
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                languagePicker
            }
        }
        .fullScreenCover(isPresented: $isShowingArtCanvas) {
            SacredArtCanvas(
                entry: entry,
                language: $language,
                onDismiss: { isShowingArtCanvas = false }
            )
        }
    }

    // MARK: - 10. Language Picker

    private var languagePicker: some View {
        Picker(
            language == .vietnamese ? "Ngôn ngữ" : "Language",
            selection: $language
        ) {
            Text("EN").tag(LanguageMode.english)
            Text("VI").tag(LanguageMode.vietnamese)
        }
        .pickerStyle(.segmented)
        .frame(width: 84)
        .tint(AnnoTheme.goldLeaf)
    }

    // MARK: - 2. Date Block

        private var dateBlock: some View {
            VStack(spacing: 8) {
                Text(language == .vietnamese ? "HÔM NAY" : "TODAY")
                    .font(Typography.captionSemiboldSerif)
                    .foregroundStyle(AnnoTheme.incense)
                    .tracking(2.5)

                Text(TodayDateFormatter.format(
                    dateString: entry.date,
                    parsedDate: entry.parsedDate,
                    language: language
                ))
                .font(Typography.title2BoldSerif)
                .foregroundStyle(AnnoTheme.vellum)
                .multilineTextAlignment(.center)

                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(calendarPillsData, id: \.label) { item in
                            calendarPill(label: item.label, value: item.value)
                        }
                    }
                    .padding(.horizontal, 4)
                }
            }
            .frame(maxWidth: .infinity)
        }

        private func calendarPill(label: String, value: String) -> some View {
            Text("\(label): \(value)")
                .font(Typography.caption2Medium)
                .foregroundStyle(AnnoTheme.incense)
                .padding(.horizontal, 10)
                .padding(.vertical, 5)
                .background {
                    Capsule()
                        .strokeBorder(AnnoTheme.ash, lineWidth: 1)
                }
        }

        // MARK: - 3. Saint / Event Header

        private var headerSection: some View {
            VStack(alignment: .leading, spacing: 12) {
                Text(localizedText.title)
                    .font(Typography.largeTitleBoldSerif)
                    .foregroundStyle(AnnoTheme.vellum)
                    .frame(maxWidth: .infinity, alignment: .leading)

                Text(localizedText.heroLine)
                    .font(Typography.title3ItalicSerif)
                    .foregroundStyle(AnnoTheme.gilt)
                    .frame(maxWidth: .infinity, alignment: .leading)

                HStack(spacing: 6) {
                    Circle()
                        .fill(liturgicalColor(for: entry.liturgical.color))
                        .frame(width: 6, height: 6)

                    Text("\(entry.liturgical.rank) · \(entry.liturgical.color)")
                        .font(Typography.captionMedium)
                        .foregroundStyle(AnnoTheme.vellum)
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
                .background {
                    Capsule()
                        .fill(AnnoTheme.choir)
                        .strokeBorder(AnnoTheme.ash, lineWidth: 1)
                }
            }
        }

    // Expanded liturgical color palette – uses AnnoTheme tokens consistently.
    private func liturgicalColor(for colorName: String) -> Color {
        let name = colorName.lowercased()
        switch name {
        case "red", "đỏ":                              return AnnoTheme.crimson
        case "white", "gold", "trắng", "vàng":        return AnnoTheme.goldLeaf
        case "blue", "lapis", "xanh":                 return AnnoTheme.lapis
        case "green":                                  return AnnoTheme.verdigris
        case "violet", "purple":                      return AnnoTheme.advent
        case "rose":                                   return Color(hex: 0xB3666E)
        case "black":                                  return AnnoTheme.ash
        default:                                       return AnnoTheme.incense
        }
    }

    // MARK: - 4. Hero Artwork Card

        private var artworkCard: some View {
            Button(action: {
                Haptics.light()
                isShowingArtCanvas = true
            }) {
                VStack(alignment: .leading, spacing: 14) {
                    ZStack(alignment: .bottomTrailing) {
                        AsyncImage(url: URL(string: entry.artwork.sourceUrl)) { phase in
                            switch phase {
                            case .empty:
                                ShimmerPlaceholder()
                            case .success(let image):
                                image
                                    .resizable()
                                    .aspectRatio(contentMode: .fill)
                            case .failure:
                                ZStack {
                                    AnnoTheme.choir
                                    Image(systemName: "photo.on.rectangle.angled")
                                        .font(.largeTitle)
                                        .foregroundStyle(AnnoTheme.incense.opacity(0.4))
                                }
                            @unknown default:
                                ShimmerPlaceholder()
                            }
                        }
                        .frame(height: 220)
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                        .shadow(color: .black.opacity(0.4), radius: 20, y: 10)

                        // Zoom indicator badge
                        HStack(spacing: 4) {
                            Image(systemName: "arrow.up.left.and.arrow.down.right")
                                .font(.system(size: 10, weight: .bold))
                            Text(language == .vietnamese ? "Phóng to 4K" : "Zoom 4K")
                                .font(.system(size: 10, weight: .semibold))
                        }
                        .foregroundStyle(AnnoTheme.goldLeaf)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(AnnoTheme.narthex.opacity(0.85))
                        .clipShape(Capsule())
                        .overlay(Capsule().stroke(AnnoTheme.goldLeaf.opacity(0.5), lineWidth: 0.8))
                        .padding(10)
                    }
                    .accessibilityLabel(entry.artwork.title)

                    VStack(alignment: .leading, spacing: 6) {
                        HStack(alignment: .top, spacing: 8) {
                            Text(entry.artwork.title)
                                .font(Typography.headlineSerif)
                                .foregroundStyle(AnnoTheme.vellum)
                                .lineLimit(2)

                            Spacer(minLength: 0)

                            Text(entry.artwork.status)
                                .font(Typography.caption2Bold)
                                .foregroundStyle(AnnoTheme.choir)
                                .padding(.horizontal, 8)
                                .padding(.vertical, 3)
                                .background {
                                    Capsule()
                                        .fill(AnnoTheme.goldLeaf)
                                }
                        }

                        Text("\(entry.artwork.maker) · \(entry.artwork.dateLabel)")
                            .font(Typography.caption)
                            .foregroundStyle(AnnoTheme.incense)
                    }
                }
            }
            .buttonStyle(.plain)
        }

        // MARK: - 5. Quick-Actions Bar

        private var quickActionsBar: some View {
            HStack(spacing: 12) {
                Button(action: {
                    Haptics.light()
                    onShowSources()
                }) {
                    HStack(spacing: 6) {
                        Image(systemName: "books.vertical.fill")
                        Text(language == .vietnamese ? "Nguồn (\(entry.sources.count))" : "Sources (\(entry.sources.count))")
                    }
                    .font(Typography.captionMedium)
                    .foregroundStyle(AnnoTheme.vellum)
                    .padding(.horizontal, 14)
                    .padding(.vertical, 8)
                    .background {
                        Capsule()
                            .fill(AnnoTheme.choir)
                            .strokeBorder(AnnoTheme.ash, lineWidth: 1)
                    }
                }
                .buttonStyle(.plain)

                Spacer()

                ConfidenceBadge(
                    label: localizedText.confidenceLabel,
                    confidence: entry.primary.confidence
                )
                .accessibilityLabel(localizedText.confidenceLabel)

                Button(action: {
                    Haptics.selection()
                    toggleBookmark()
                }) {
                    Image(systemName: isBookmarked ? "bookmark.fill" : "bookmark")
                        .font(.system(size: 16, weight: .semibold))
                        .foregroundStyle(isBookmarked ? AnnoTheme.goldLeaf : AnnoTheme.incense)
                        .padding(10)
                        .background {
                            Circle()
                                .fill(AnnoTheme.choir)
                                .strokeBorder(AnnoTheme.ash, lineWidth: 1)
                        }
                        .scaleEffect(bookmarkScale)
                }
                .buttonStyle(.plain)
                .accessibilityLabel(
                    isBookmarked
                        ? (language == .vietnamese ? "Bỏ lưu trữ" : "Remove bookmark")
                        : (language == .vietnamese ? "Lưu trữ" : "Bookmark")
                )
            }
        }

        private func toggleBookmark() {
            withAnimation(.spring(response: 0.3, dampingFraction: 0.5)) {
                isBookmarked.toggle()
                bookmarkScale = 1.3
            }
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
                withAnimation(.spring(response: 0.3, dampingFraction: 0.5)) {
                    bookmarkScale = 1.0
                }
            }
        }

        // MARK: - 6. Summary Text

        private var summaryCard: some View {
            Text(localizedText.summary)
                .font(Typography.bodySerif)
                .lineSpacing(5)
                .foregroundStyle(AnnoTheme.vellum)
                .frame(maxWidth: .infinity, alignment: .leading)
                .annoCard()
        }

    // MARK: - 7. Sacred Place Section

        private func sacredPlaceCard(place: SacredPlace) -> some View {
            VStack(alignment: .leading, spacing: 12) {
                HStack(alignment: .top) {
                    HStack(spacing: 8) {
                        Image(systemName: "mappin.and.ellipse")
                            .foregroundStyle(AnnoTheme.goldLeaf)
                        Text(place.name)
                            .font(Typography.headlineSerif)
                            .foregroundStyle(AnnoTheme.vellum)
                    }
                    Spacer()
                    ConfidenceBadge(
                        label: placeConfidenceLabel(place.confidence),
                        confidence: place.confidence
                    )
                    .accessibilityLabel(placeConfidenceLabel(place.confidence))
                }

                HStack {
                    Text(String(format: "%.4f, %.4f", place.latitude, place.longitude))
                        .font(.caption.monospacedDigit())
                        .foregroundStyle(AnnoTheme.incense)

                    Spacer()

                    if let url = mapsURL(for: place) {
                        Link(destination: url) {
                            HStack(spacing: 4) {
                                Text(language == .vietnamese ? "Mở trong Bản đồ" : "Open in Maps")
                                Image(systemName: "arrow.up.right")
                            }
                            .font(Typography.captionSemibold)
                            .foregroundStyle(AnnoTheme.goldLeaf)
                        }
                        .buttonStyle(.plain)
                        .accessibilityLabel(
                            language == .vietnamese
                                ? "Mở \(place.name) trong Bản đồ"
                                : "Open \(place.name) in Maps"
                        )
                    }
                }
            }
            .annoCard()
        }

        private func liturgicalPilgrimageCard(route: PilgrimageRoute) -> some View {
            VStack(alignment: .leading, spacing: 12) {
                HStack(spacing: 8) {
                    Image(systemName: "sparkles")
                        .foregroundStyle(AnnoTheme.goldLeaf)
                    Text(language == .vietnamese ? "Hành hương cùng Phụng vụ hôm nay" : "Walk this path today")
                        .font(Typography.headlineSerif)
                        .foregroundStyle(AnnoTheme.goldLeaf)

                    Spacer()

                    Text("\(route.waypoints.count) \(language == .vietnamese ? "Trạm" : "Stations")")
                        .font(Typography.caption2MonospacedSemibold)
                        .foregroundStyle(AnnoTheme.narthex)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 3)
                        .background(Capsule().fill(AnnoTheme.goldLeaf))
                }

                VStack(alignment: .leading, spacing: 4) {
                    Text(route.title(for: language))
                        .font(Typography.subheadlineSemiboldSerif)
                        .foregroundStyle(AnnoTheme.vellum)

                    Text(route.spiritualTheme(for: language))
                        .font(Typography.captionItalic)
                        .foregroundStyle(AnnoTheme.incense)
                        .lineLimit(2)
                }

                // Preview first 3 stations
                HStack(spacing: 6) {
                    ForEach(route.waypoints.prefix(3)) { wp in
                        HStack(spacing: 4) {
                            Text("\(wp.order)")
                                .font(Typography.caption2Bold)
                                .foregroundStyle(AnnoTheme.goldLeaf)
                            Text(wp.name(for: language))
                                .font(Typography.caption2)
                                .foregroundStyle(AnnoTheme.vellum)
                                .lineLimit(1)
                        }
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(RoundedRectangle(cornerRadius: 6).fill(AnnoTheme.ash.opacity(0.6)))

                        if wp.order < min(route.waypoints.count, 3) {
                            Image(systemName: "chevron.right")
                                .font(.system(size: 8))
                                .foregroundStyle(AnnoTheme.incense.opacity(0.6))
                        }
                    }
                }

                if let firstWp = route.waypoints.first, let mapsUrl = mapsURL(for: SacredPlace(name: firstWp.nameEn, latitude: firstWp.latitude, longitude: firstWp.longitude, confidence: .confirmed, sourceUrl: "")) {
                    Link(destination: mapsUrl) {
                        HStack(spacing: 6) {
                            Image(systemName: "map.fill")
                            Text(language == .vietnamese ? "Xem Lộ Trình Trên Bản Đồ" : "Explore Route on Map")
                        }
                        .font(Typography.captionSemibold)
                        .foregroundStyle(AnnoTheme.narthex)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 10)
                        .background(
                            LinearGradient(
                                colors: [AnnoTheme.gilt, AnnoTheme.goldLeaf],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )
                        .clipShape(RoundedRectangle(cornerRadius: 8))
                        .shadow(color: AnnoTheme.goldLeaf.opacity(0.3), radius: 6, y: 2)
                    }
                    .buttonStyle(.plain)
                }
            }
            .annoCard()
        }

    private func mapsURL(for place: SacredPlace) -> URL? {
        var components = URLComponents()
        components.scheme = "https"
        components.host = "maps.apple.com"
        components.queryItems = [
            URLQueryItem(name: "ll", value: "\(place.latitude),\(place.longitude)"),
            URLQueryItem(name: "q", value: place.name)
        ]
        return components.url
    }

    private func placeConfidenceLabel(_ confidence: ConfidenceLevel) -> String {
        switch confidence {
        case .confirmed: return language == .vietnamese ? "Đã xác nhận" : "Confirmed"
        case .traditional: return language == .vietnamese ? "Theo truyền thống" : "Traditional"
        case .disputed: return language == .vietnamese ? "Còn tranh luận" : "Disputed"
        case .contextual: return language == .vietnamese ? "Theo bối cảnh" : "Contextual"
        }
    }

    // MARK: - 8. Prayer Prompt Card

        private var prayerPromptCard: some View {
            VStack(alignment: .leading, spacing: 12) {
                HStack(spacing: 8) {
                    Image(systemName: "hands.sparkles")
                        .foregroundStyle(AnnoTheme.goldLeaf)
                    Text(language == .vietnamese ? "Lời nguyện" : "Prayer prompt")
                        .font(Typography.headlineSerif)
                        .foregroundStyle(AnnoTheme.goldLeaf)
                }

                Text(localizedText.prayerPrompt)
                    .font(Typography.bodySerif)
                    .lineSpacing(5)
                    .foregroundStyle(AnnoTheme.vellum)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .annoCard()
        }

        // MARK: - 9. Source Confidence Card

        private var sourceConfidenceCard: some View {
            VStack(alignment: .leading, spacing: 12) {
                Text(localizedText.confidenceNote)
                    .font(Typography.captionSerif)
                    .lineSpacing(4)
                    .foregroundStyle(AnnoTheme.incense)

                Button(action: {
                    Haptics.light()
                    onShowSources()
                }) {
                    HStack(spacing: 6) {
                        Text(language == .vietnamese ? "Xem nguồn" : "Read sources")
                        Image(systemName: "chevron.right")
                            .font(Typography.captionBold)
                    }
                    .font(Typography.subheadlineSemibold)
                    .foregroundStyle(AnnoTheme.goldLeaf)
                }
                .buttonStyle(.plain)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .annoCard()
        }
}

// MARK: - Helper Types

private enum TodayDateFormatter {
    private static let utc = TimeZone(secondsFromGMT: 0)!

    private static let parser: DateFormatter = {
        let df = DateFormatter()
        df.locale = Locale(identifier: "en_US_POSIX")
        df.calendar = Calendar(identifier: .gregorian)
        df.timeZone = utc
        df.dateFormat = "yyyy-MM-dd"
        return df
    }()

    private static let enFormatter: DateFormatter = {
        let df = DateFormatter()
        df.locale = Locale(identifier: "en_US")
        df.calendar = Calendar(identifier: .gregorian)
        df.timeZone = utc
        df.dateFormat = "MMMM d, yyyy"
        return df
    }()

    private static let viFormatter: DateFormatter = {
        let df = DateFormatter()
        df.locale = Locale(identifier: "vi_VN")
        df.calendar = Calendar(identifier: .gregorian)
        df.timeZone = utc
        df.dateFormat = "d 'tháng' M, yyyy"
        return df
    }()

    static func format(dateString: String, parsedDate: Date?, language: LanguageMode) -> String {
        guard let date = parsedDate ?? parser.date(from: dateString) else {
            return dateString
        }
        return language == .english
            ? enFormatter.string(from: date)
            : viFormatter.string(from: date)
    }
}

// Enhanced shimmer placeholder – warmer gold-tinged animation that echoes the ecclesial palette.
private struct ShimmerPlaceholder: View {
    @State private var phase: CGFloat = -1.0

    var body: some View {
        GeometryReader { geo in
            Rectangle()
                .fill(
                    LinearGradient(
                        gradient: Gradient(colors: [
                            AnnoTheme.choir,
                            AnnoTheme.ash,
                            AnnoTheme.choir
                        ]),
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .overlay(
                    LinearGradient(
                        gradient: Gradient(colors: [
                            .clear,
                            AnnoTheme.gilt.opacity(0.15),
                            .clear
                        ]),
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                    .offset(x: phase * geo.size.width)
                    .blur(radius: 20)
                )
                .clipped()
        }
        .onAppear {
            withAnimation(.linear(duration: 1.8).repeatForever(autoreverses: false)) {
                phase = 1.0
            }
        }
    }
}

// MARK: - Preview

private enum PreviewData {
    static let sampleEntry = AnnoEntry(
        id: "2026-07-03",
        date: "2026-07-03",
        weekday: "Friday",
        mockPriority: "week_real_data",
        liturgical: LiturgicalInfo(
            rank: "Feast",
            color: "Red",
            titleEn: "St. Thomas, Apostle",
            titleVi: "Thánh Tôma, Tông đồ"
        ),
        calendars: CalendarConversions(
            julian: "June 20, 2026",
            hebrew: "18 Tammuz 5786",
            islamicUmmAlQura: "18 Muharram 1448",
            coptic: "26 Paoni 1742",
            ethiopian: "26 Sene 2018"
        ),
        primary: PrimaryContent(
            type: "Feast",
            titleEn: "Feast of Saint Thomas the Apostle",
            titleVi: "Lễ Thánh Tôma Tông Đồ",
            summaryEn: "Saint Thomas, also called Didymus, was one of the Twelve Apostles of Jesus Christ, according to the New Testament. He is informally known as 'Doubting Thomas' because he initially doubted Jesus' resurrection when told of it, followed later by his confession of faith, 'My Lord and my God!' on seeing the wounds of Christ.",
            summaryVi: "Thánh Tôma, còn gọi là Điđimô, là một trong Mười Hai Tông Đồ của Chúa Giêsu Kitô theo Tân Ước. Ngài thường được gọi một cách dân dã là 'Tôma đa nghi' vì ban đầu đã nghi ngờ sự phục sinh của Chúa Giêsu, sau đó ngài đã tuyên xưng đức tin mạnh mẽ: 'Lạy Chúa của con, lạy Thiên Chúa của con!' khi nhìn thấy các vết thương của Chúa Kitô.",
            confidence: .confirmed,
            confidenceNoteEn: "Historical attestation of the feast day is universally recognized across Roman, Byzantine, and Syriac liturgical traditions.",
            confidenceNoteVi: "Việc xác nhận ngày lễ theo lịch sử được công nhận rộng rãi trong các truyền thống phụng vụ Rôma, Đông Phương và Syriac."
        ),
        place: SacredPlace(
            name: "St. Thomas Mount",
            latitude: 13.0067,
            longitude: 80.2020,
            confidence: .traditional,
            sourceUrl: "https://en.wikipedia.org/wiki/St._Thomas_Mount"
        ),
        artwork: ArtworkCandidate(
            title: "The Incredulity of Saint Thomas",
            maker: "Caravaggio",
            dateLabel: "c. 1601–1602",
            sourceUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Caravaggio_-_The_Incredulity_of_Saint_Thomas.jpg/1280px-Caravaggio_-_The_Incredulity_of_Saint_Thomas.jpg",
            status: "Public Domain"
        ),
        sources: [
            SourceRef(label: "Roman Missal", url: "https://example.com/missal", type: "Liturgical"),
            SourceRef(label: "Patristic Commentary", url: "https://example.com/patristic", type: "Historical")
        ],
        appHooks: AppHooks(
            heroLineEn: "Blessed are those who have not seen and yet have believed.",
            heroLineVi: "Phúc cho những ai không thấy mà tin.",
            prayerPromptEn: "Grant us, O Almighty God, to glory in the feast of your blessed Apostle Thomas, that we may always be sustained by his intercession and believing, may have life in the name of Jesus Christ.",
            prayerPromptVi: "Lạy Thiên Chúa toàn năng, xin cho chúng con được hân hoan mừng lễ Thánh Tông đồ Tôma, để nhờ lời ngài chuyển cầu, chúng con luôn giữ vững đức tin vào danh Chúa Giêsu Kitô."
        )
    )
}

#Preview {
    NavigationStack {
        TodayView(
            entry: PreviewData.sampleEntry,
            language: .constant(.english),
            onShowSources: {}
        )
    }
    .preferredColorScheme(.dark)
}

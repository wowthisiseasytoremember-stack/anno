import SwiftUI

struct SoCalPilgrimageHero: View {
    let content: SoCalExemplarContent
    let language: LanguageMode
    let visitedCount: Int
    let totalCount: Int

    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var revealed = false

    private var progress: Double {
        guard totalCount > 0 else { return 0 }
        return Double(visitedCount) / Double(totalCount)
    }

    var body: some View {
        ZStack {
            SolemnityBloom(tint: AnnoTheme.lapis, active: true)
                .frame(height: 210)

            VStack(spacing: 12) {
                HStack {
                    Text(language == .vietnamese ? "TUYẾN HÀNH HƯƠNG NỔI BẬT" : "FEATURED PILGRIMAGE")
                        .font(Typography.captionBold)
                        .tracking(1.4)
                        .foregroundStyle(AnnoTheme.gilt)

                    Spacer()

                    Image(systemName: AnnoSymbol.marian)
                        .foregroundStyle(AnnoTheme.gilt)
                        .symbolEffect(.appear, value: revealed)
                }

                VStack(alignment: .leading, spacing: 6) {
                    Text(language == .vietnamese
                         ? content.opening.titleVi
                         : content.opening.titleEn)
                        .font(Typography.title2BoldSerif)
                        .foregroundStyle(AnnoTheme.vellum)
                        .fixedSize(horizontal: false, vertical: true)

                    Text(language == .vietnamese
                         ? content.opening.hookVi
                         : content.opening.hookEn)
                        .font(Typography.subheadlineSerif)
                        .foregroundStyle(AnnoTheme.incense)
                        .fixedSize(horizontal: false, vertical: true)
                }
                .frame(maxWidth: .infinity, alignment: .leading)

                SacredDivider(tint: AnnoTheme.goldLeaf, intensity: .solemnity)

                VStack(alignment: .leading, spacing: 6) {
                    HStack {
                        Text(language == .vietnamese ? "Tiến trình" : "Progress")
                            .font(Typography.captionSemibold)
                            .foregroundStyle(AnnoTheme.incense)
                        Spacer()
                        Text("\(visitedCount)/\(totalCount)")
                            .font(Typography.caption2MonospacedSemibold)
                            .foregroundStyle(AnnoTheme.gilt)
                    }

                    GeometryReader { proxy in
                        ZStack(alignment: .leading) {
                            Capsule()
                                .fill(AnnoTheme.ash.opacity(0.7))
                            Capsule()
                                .fill(
                                    LinearGradient(
                                        colors: [AnnoTheme.lapis, AnnoTheme.goldLeaf, AnnoTheme.gilt],
                                        startPoint: .leading,
                                        endPoint: .trailing
                                    )
                                )
                                .frame(width: max(0, proxy.size.width * progress))
                        }
                    }
                    .frame(height: 7)
                    .accessibilityHidden(true)
                }
            }
            .padding(16)
        }
        .background {
            RoundedRectangle(cornerRadius: AnnoTheme.radiusHero, style: .continuous)
                .fill(
                    LinearGradient(
                        colors: [
                            AnnoTheme.lapis.opacity(0.30),
                            AnnoTheme.surfaceRaised,
                            AnnoTheme.narthex
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
        }
        .overlay {
            RoundedRectangle(cornerRadius: AnnoTheme.radiusHero, style: .continuous)
                .strokeBorder(AnnoTheme.gilt.opacity(0.62), lineWidth: 1.2)
        }
        .shadow(color: AnnoTheme.goldLeaf.opacity(0.22), radius: 16, y: 6)
        .scaleEffect(reduceMotion || revealed ? 1 : 0.97)
        .opacity(revealed ? 1 : 0)
        .animation(reduceMotion ? nil : AnnoMotion.immersive, value: revealed)
        .accessibilityElement(children: .combine)
        .onAppear { revealed = true }
    }
}

struct PilgrimageSessionControl: View {
    let isActive: Bool
    let startedAt: Date?
    let language: LanguageMode
    let onBegin: () -> Void
    let onEnd: () -> Void

    private var startedLabel: String? {
        guard let startedAt else { return nil }
        return startedAt.formatted(date: .omitted, time: .shortened)
    }

    var body: some View {
        Group {
            if isActive {
                HStack(spacing: 10) {
                    ZStack {
                        Circle()
                            .fill(AnnoTheme.verdigris.opacity(0.18))
                            .frame(width: 38, height: 38)

                        Image(systemName: "figure.walk.motion")
                            .foregroundStyle(AnnoTheme.verdigris)
                            .symbolEffect(.pulse)
                    }

                    VStack(alignment: .leading, spacing: 2) {
                        Text(
                            language == .vietnamese
                                ? "HÀNH HƯƠNG ĐANG DIỄN RA"
                                : "PILGRIMAGE ACTIVE"
                        )
                        .font(Typography.caption2Bold)
                        .tracking(1.0)
                        .foregroundStyle(AnnoTheme.verdigris)

                        if let startedLabel {
                            Text(
                                language == .vietnamese
                                    ? "Bắt đầu lúc \(startedLabel)"
                                    : "Started \(startedLabel)"
                            )
                            .font(Typography.caption2)
                            .foregroundStyle(AnnoTheme.incense)
                        }
                    }

                    Spacer()

                    Button {
                        onEnd()
                    } label: {
                        Text(
                            language == .vietnamese
                                ? "Kết thúc lúc này"
                                : "End for now"
                        )
                        .font(Typography.caption2Medium)
                        .foregroundStyle(AnnoTheme.incense)
                    }
                    .buttonStyle(.plain)
                }
                .padding(12)
                .background {
                    RoundedRectangle(
                        cornerRadius: AnnoTheme.radiusCard,
                        style: .continuous
                    )
                    .fill(AnnoTheme.surfaceInset)
                }
                .overlay {
                    RoundedRectangle(
                        cornerRadius: AnnoTheme.radiusCard,
                        style: .continuous
                    )
                    .strokeBorder(AnnoTheme.verdigris.opacity(0.45), lineWidth: 1)
                }
            } else {
                Button {
                    onBegin()
                } label: {
                    HStack(spacing: 10) {
                        Image(systemName: "figure.walk.motion")
                            .symbolRenderingMode(.hierarchical)
                        Text(
                            language == .vietnamese
                                ? "Bắt Đầu Hành Hương"
                                : "Begin Pilgrimage"
                        )
                        Spacer()
                        Image(systemName: "sparkles")
                    }
                    .font(Typography.subheadlineSemiboldSerif)
                    .foregroundStyle(AnnoTheme.narthex)
                    .padding(.horizontal, 14)
                    .padding(.vertical, 12)
                    .background {
                        LinearGradient(
                            colors: [AnnoTheme.gilt, AnnoTheme.goldLeaf],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    }
                    .clipShape(
                        RoundedRectangle(
                            cornerRadius: AnnoTheme.radiusCard,
                            style: .continuous
                        )
                    )
                    .shadow(
                        color: AnnoTheme.goldLeaf.opacity(0.28),
                        radius: 10,
                        y: 4
                    )
                }
                .buttonStyle(.plain)
            }
        }
    }
}

struct SoCalChapterHeader: View {
    let chapter: SoCalExemplarContent.Chapter
    let language: LanguageMode

    var body: some View {
        VStack(alignment: .leading, spacing: 5) {
            Text(
                language == .vietnamese
                    ? "CHƯƠNG \(chapter.order)"
                    : "CHAPTER \(chapter.order)"
            )
            .font(Typography.caption2Bold)
            .tracking(1.6)
            .foregroundStyle(AnnoTheme.gilt)

            Text(chapter.geographicName)
                .font(Typography.headlineSerif)
                .foregroundStyle(AnnoTheme.vellum)
                .fixedSize(horizontal: false, vertical: true)

            Text(chapter.role(for: language))
                .font(Typography.captionItalic)
                .foregroundStyle(AnnoTheme.incense)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(12)
        .background {
            RoundedRectangle(cornerRadius: AnnoTheme.radiusCard, style: .continuous)
                .fill(AnnoTheme.lapis.opacity(0.13))
        }
        .overlay {
            RoundedRectangle(cornerRadius: AnnoTheme.radiusCard, style: .continuous)
                .strokeBorder(AnnoTheme.lapis.opacity(0.42), lineWidth: 1)
        }
    }
}

struct SoCalStationRitualView: View {
    let station: SoCalExemplarContent.Station
    let language: LanguageMode

    private var tint: Color {
        switch station.stationRole {
        case "witness":
            return AnnoTheme.crimson
        case "reflection":
            return AnnoTheme.rose
        case "institution":
            return AnnoTheme.verdigris
        case "marian_parish", "arrival":
            return AnnoTheme.lapis
        default:
            return AnnoTheme.goldLeaf
        }
    }

    private var intensity: SacredIntensity {
        station.momentLevel == "climax" ? .solemnity :
            (station.momentLevel == "highlight" ? .feast : .ordinary)
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            if let label = station.momentLabel(for: language),
               station.momentLevel != "reflection",
               station.momentLevel != "context" {
                SacredMomentBanner(
                    title: label,
                    subtitle: station.title(for: language),
                    symbol: station.stationRole == "witness"
                        ? AnnoSymbol.martyr
                        : (station.stationRole.contains("marian") || station.stationRole == "arrival"
                            ? AnnoSymbol.marian
                            : AnnoSymbol.sacred),
                    intensity: intensity,
                    tint: tint
                )
            }

            ritualRow(
                label: language == .vietnamese ? "ĐẾN" : "ARRIVE",
                symbol: "location.fill",
                text: station.arrive(for: language)
            )
            ritualRow(
                label: language == .vietnamese ? "NHÌN" : "LOOK",
                symbol: "eye.fill",
                text: station.look(for: language)
            )
            ritualRow(
                label: language == .vietnamese ? "BIẾT" : "KNOW",
                symbol: "book.closed.fill",
                text: station.know(for: language)
            )
            ritualRow(
                label: language == .vietnamese ? "CẦU NGUYỆN" : "PRAY",
                symbol: AnnoSymbol.prayer,
                text: station.pray(for: language),
                emphasized: true
            )
            ritualRow(
                label: language == .vietnamese ? "TIẾP TỤC" : "CONTINUE",
                symbol: "arrow.right",
                text: station.continueText(for: language)
            )
        }
        .annoSurface(.devotional)
    }

    @ViewBuilder
    private func ritualRow(
        label: String,
        symbol: String,
        text: String,
        emphasized: Bool = false
    ) -> some View {
        HStack(alignment: .top, spacing: 10) {
            AnnoIconBadge(
                symbol: symbol,
                tint: emphasized ? AnnoTheme.goldLeaf : tint,
                size: 38
            )

            VStack(alignment: .leading, spacing: 3) {
                Text(label)
                    .font(Typography.caption2Bold)
                    .tracking(1.2)
                    .foregroundStyle(emphasized ? AnnoTheme.goldLeaf : tint)

                Text(text)
                    .font(emphasized ? Typography.bodySerif.italic() : Typography.captionSerif)
                    .foregroundStyle(AnnoTheme.vellum)
                    .fixedSize(horizontal: false, vertical: true)
            }
        }
    }
}

struct PilgrimageVisitButton: View {
    let isVisited: Bool
    let language: LanguageMode
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 8) {
                Image(systemName: isVisited ? "checkmark.seal.fill" : "mappin.and.ellipse")
                Text(
                    isVisited
                        ? (language == .vietnamese ? "Đã Viếng" : "Visited")
                        : (language == .vietnamese ? "Tôi Đang Ở Đây" : "I'm Here")
                )
            }
            .font(Typography.subheadlineSemiboldSerif)
            .foregroundStyle(isVisited ? AnnoTheme.gilt : AnnoTheme.narthex)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 12)
            .background {
                RoundedRectangle(cornerRadius: AnnoTheme.radiusCard, style: .continuous)
                    .fill(isVisited ? AnnoTheme.surfaceRaised : AnnoTheme.goldLeaf)
            }
            .overlay {
                RoundedRectangle(cornerRadius: AnnoTheme.radiusCard, style: .continuous)
                    .strokeBorder(
                        isVisited ? AnnoTheme.gilt.opacity(0.5) : AnnoTheme.goldLeaf,
                        lineWidth: 1
                    )
            }
        }
        .buttonStyle(.plain)
        .disabled(isVisited)
        .accessibilityHint(
            isVisited
                ? ""
                : (language == .vietnamese
                    ? "Ghi lại điểm hành hương này trên thiết bị"
                    : "Records this pilgrimage station as visited on this device")
        )
    }
}

struct PilgrimageCompletionKeepsake: View {
    let content: SoCalExemplarContent
    let routeId: String
    let language: LanguageMode
    let completionDate: Date?

    private var dateText: String {
        guard let completionDate else { return "" }
        return completionDate.formatted(date: .long, time: .omitted)
    }

    private var shareText: String {
        [
            language == .vietnamese ? content.completion.titleVi : content.completion.titleEn,
            language == .vietnamese ? content.opening.titleVi : content.opening.titleEn,
            language == .vietnamese ? content.completion.invocationVi : content.completion.invocationEn,
            dateText
        ]
        .filter { !$0.isEmpty }
        .joined(separator: "\n")
    }

    var body: some View {
        VStack(spacing: 14) {
            ZStack {
                SolemnityBloom(tint: AnnoTheme.lapis, active: true)
                    .frame(height: 120)

                SacredAureole(
                    tint: AnnoTheme.goldLeaf,
                    intensity: .solemnity,
                    diameter: 78
                )

                Text("A")
                    .font(.system(size: 42, weight: .bold, design: .serif))
                    .foregroundStyle(AnnoTheme.gilt)
            }

            Text(content.completion.title(for: language).uppercased())
                .font(Typography.title2BoldSerif)
                .foregroundStyle(AnnoTheme.gilt)
                .multilineTextAlignment(.center)

            Text(content.completion.body(for: language))
                .font(Typography.bodySerif)
                .foregroundStyle(AnnoTheme.vellum)
                .multilineTextAlignment(.center)
                .fixedSize(horizontal: false, vertical: true)

            SacredDivider(tint: AnnoTheme.goldLeaf, intensity: .solemnity)

            Text(content.completion.invocation(for: language))
                .font(Typography.headlineSerif.italic())
                .foregroundStyle(AnnoTheme.goldLeaf)
                .multilineTextAlignment(.center)

            if !dateText.isEmpty {
                Text(dateText)
                    .font(Typography.captionSerif)
                    .foregroundStyle(AnnoTheme.incense)
            }

            if let routeURL = AnnoDeepLink.pilgrimage(
                routeId: routeId,
                stationId: nil
            ).url {
                ShareLink(
                    item: routeURL,
                    subject: Text(
                        language == .vietnamese
                            ? content.opening.titleVi
                            : content.opening.titleEn
                    ),
                    message: Text(shareText)
                ) {
                    Label(
                        language == .vietnamese ? "Chia Sẻ Kỷ Niệm" : "Share Keepsake",
                        systemImage: "square.and.arrow.up"
                    )
                    .font(Typography.subheadlineSemiboldSerif)
                    .foregroundStyle(AnnoTheme.narthex)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 11)
                    .background(AnnoTheme.goldLeaf)
                    .clipShape(
                        RoundedRectangle(
                            cornerRadius: AnnoTheme.radiusCard,
                            style: .continuous
                        )
                    )
                }
            }
        }
        .padding(18)
        .background {
            RoundedRectangle(cornerRadius: AnnoTheme.radiusHero, style: .continuous)
                .fill(
                    LinearGradient(
                        colors: [
                            AnnoTheme.lapis.opacity(0.34),
                            AnnoTheme.narthex,
                            AnnoTheme.goldLeaf.opacity(0.10)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
        }
        .overlay {
            RoundedRectangle(cornerRadius: AnnoTheme.radiusHero, style: .continuous)
                .strokeBorder(AnnoTheme.gilt.opacity(0.72), lineWidth: 1.4)
        }
        .shadow(color: AnnoTheme.goldLeaf.opacity(0.30), radius: 18, y: 7)
        .accessibilityElement(children: .contain)
    }
}

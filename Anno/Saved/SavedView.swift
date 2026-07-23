import SwiftUI

struct SavedView: View {
    let language: LanguageMode
    @State private var showingPaywall = false
    @State private var glowOpacity: Double = 0.4
    @State private var appeared = false

    var body: some View {
        ScrollView {
            VStack(spacing: 32) {
                heroSection
                hoaThiengTracker
                previewCollections
            }
            .padding(.horizontal, 20)
            .padding(.top, 24)
            .padding(.bottom, 48)
        }
        .background {
            ZStack {
                AnnoTheme.narthex.ignoresSafeArea()

                RadialGradient(
                    gradient: Gradient(colors: [
                        AnnoTheme.goldLeaf.opacity(0.06),
                        AnnoTheme.narthex.opacity(0.0)
                    ]),
                    center: .top,
                    startRadius: 0,
                    endRadius: 400
                )
                .ignoresSafeArea(edges: .top)
            }
        }
        .navigationTitle(language == .vietnamese ? "Đã lưu" : "Saved")
        .sheet(isPresented: $showingPaywall) {
            ArchivePaywallView(language: language)
        }
        .onAppear {
            withAnimation(.easeOut(duration: 0.8)) {
                appeared = true
            }
        }
    }

    // MARK: - Hero Empty State

    private var heroSection: some View {
        VStack(spacing: 24) {
            bookmarkHero
            titleBlock
            unlockButton
        }
        .frame(maxWidth: .infinity)
        .opacity(appeared ? 1 : 0)
        .offset(y: appeared ? 0 : 12)
    }

    private var bookmarkHero: some View {
        ZStack {
            // Outer gold glow — pulsing
            Circle()
                .fill(
                    RadialGradient(
                        gradient: Gradient(colors: [
                            AnnoTheme.goldLeaf.opacity(glowOpacity * 0.35),
                            AnnoTheme.goldLeaf.opacity(0.0)
                        ]),
                        center: .center,
                        startRadius: 10,
                        endRadius: 70
                    )
                )
                .frame(width: 140, height: 140)

            Image(systemName: "bookmark.fill")
                .font(.system(size: 52, weight: .light))
                .foregroundStyle(
                    LinearGradient(
                        colors: [AnnoTheme.goldLeaf, AnnoTheme.gilt],
                        startPoint: .top,
                        endPoint: .bottom
                    )
                )
                .shadow(color: AnnoTheme.goldLeaf.opacity(0.3), radius: 12, y: 4)
        }
        .padding(.top, 16)
        .onAppear {
            withAnimation(
                .easeInOut(duration: 2.8)
                .repeatForever(autoreverses: true)
            ) {
                glowOpacity = 1.0
            }
        }
        .accessibilityHidden(true)
    }

    private var titleBlock: some View {
        VStack(spacing: 10) {
            Text(language == .vietnamese ? "Bộ sưu tập đã lưu" : "Saved Collections")
                .font(.title2.weight(.semibold))
                .fontDesign(.serif)
                .foregroundStyle(AnnoTheme.vellum)
                .multilineTextAlignment(.center)
                .accessibilityAddTraits(.isHeader)

            Text(language == .vietnamese
                 ? "Lưu các ngày lễ, tác phẩm nghệ thuật thánh và địa điểm hành hương để trở lại sau."
                 : "Save feast days, sacred artwork, and pilgrimage sites to revisit later.")
                .font(.subheadline)
                .fontDesign(.serif)
                .foregroundStyle(AnnoTheme.incense)
                .multilineTextAlignment(.center)
                .fixedSize(horizontal: false, vertical: true)
                .lineSpacing(3)
        }
        .padding(.horizontal, 8)
    }

    private var unlockButton: some View {
        Button {
            showingPaywall = true
        } label: {
            HStack(spacing: 8) {
                Image(systemName: "lock.open.fill")
                    .font(.subheadline.weight(.semibold))
                Text(language == .vietnamese ? "Mở khóa bộ sưu tập" : "Unlock Collections")
                    .font(.headline)
                    .fontDesign(.serif)
            }
            .foregroundStyle(AnnoTheme.narthex)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 15)
            .background(
                LinearGradient(
                    colors: [AnnoTheme.goldLeaf, AnnoTheme.gilt],
                    startPoint: .leading,
                    endPoint: .trailing
                )
            )
            .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
            .shadow(color: AnnoTheme.goldLeaf.opacity(0.25), radius: 12, y: 6)
        }
        .buttonStyle(.plain)
        .accessibilityLabel(
            language == .vietnamese
                ? "Mở khóa bộ sưu tập đã lưu"
                : "Unlock saved collections"
        )
        .accessibilityHint(
            language == .vietnamese
                ? "Mở trang đăng ký Anno Plus"
                : "Opens the Anno Plus subscription page"
        )
    }

    // MARK: - Hoa Thiêng Tracker (Gamification)

    @AppStorage("hoaThiengMorning") private var morningChecked = false
    @AppStorage("hoaThiengCommunion") private var communionChecked = false
    @AppStorage("hoaThiengNight") private var nightChecked = false

    private var hoaThiengTracker: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text(language == .vietnamese ? "HOA THIÊNG (SPIRITUAL BOUQUET)" : "SPIRITUAL BOUQUET")
                .font(.caption.weight(.semibold))
                .foregroundStyle(AnnoTheme.incense)
                .tracking(2.0)
                .padding(.leading, 4)
                .accessibilityAddTraits(.isHeader)

            VStack(spacing: 0) {
                trackerRow(
                    icon: "sunrise.fill",
                    titleEn: "Morning Offering",
                    titleVi: "Dâng Ngày",
                    isChecked: $morningChecked
                )
                Divider().background(AnnoTheme.ash).padding(.leading, 44)
                trackerRow(
                    icon: "sparkles",
                    titleEn: "Communion / Mass",
                    titleVi: "Rước Lễ",
                    isChecked: $communionChecked
                )
                Divider().background(AnnoTheme.ash).padding(.leading, 44)
                trackerRow(
                    icon: "moon.stars.fill",
                    titleEn: "Night Offering",
                    titleVi: "Dâng Đêm",
                    isChecked: $nightChecked
                )
            }
            .background(AnnoTheme.choir)
            .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
            .overlay(RoundedRectangle(cornerRadius: 12).stroke(AnnoTheme.ash, lineWidth: 1))
            .shadow(color: AnnoTheme.cardShadow.color, radius: AnnoTheme.cardShadow.radius, y: AnnoTheme.cardShadow.y)
        }
        .opacity(appeared ? 1 : 0)
        .offset(y: appeared ? 0 : 16)
        .animation(.spring(response: 0.6, dampingFraction: 0.8).delay(0.1), value: appeared)
    }

    private func trackerRow(icon: String, titleEn: String, titleVi: String, isChecked: Binding<Bool>) -> some View {
        Button {
            let generator = UIImpactFeedbackGenerator(style: .medium)
            generator.impactOccurred()
            withAnimation(.spring(response: 0.3, dampingFraction: 0.6)) {
                isChecked.wrappedValue.toggle()
            }
        } label: {
            HStack(spacing: 16) {
                Image(systemName: icon)
                    .font(.title3)
                    .foregroundStyle(isChecked.wrappedValue ? AnnoTheme.goldLeaf : AnnoTheme.incense.opacity(0.5))
                    .frame(width: 32)

                Text(language == .vietnamese ? titleVi : titleEn)
                    .font(.subheadline.weight(.medium))
                    .fontDesign(.serif)
                    .foregroundStyle(isChecked.wrappedValue ? AnnoTheme.vellum : AnnoTheme.incense)

                Spacer()

                ZStack {
                    Circle()
                        .stroke(isChecked.wrappedValue ? AnnoTheme.goldLeaf : AnnoTheme.ash, lineWidth: 2)
                        .frame(width: 24, height: 24)

                    if isChecked.wrappedValue {
                        Circle()
                            .fill(AnnoTheme.goldLeaf)
                            .frame(width: 16, height: 16)
                            .transition(.scale)
                    }
                }
            }
            .padding(.vertical, 16)
            .padding(.horizontal, 16)
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
    }

    // MARK: - Preview Collections

    private var previewCollections: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text(language == .vietnamese ? "BỘ SƯU TẬP" : "COLLECTIONS")
                .font(.caption.weight(.semibold))
                .foregroundStyle(AnnoTheme.incense)
                .tracking(2.0)
                .padding(.leading, 4)
                .accessibilityAddTraits(.isHeader)

            ForEach(Array(mockCollections.enumerated()), id: \.element.icon) { index, item in
                collectionCard(item: item)
                    .opacity(appeared ? 1 : 0)
                    .offset(y: appeared ? 0 : 16)
                    .animation(
                        .spring(response: 0.6, dampingFraction: 0.8)
                            .delay(0.15 * Double(index)),
                        value: appeared
                    )
            }
        }
    }

    private func collectionCard(item: MockCollection) -> some View {
        HStack(spacing: 14) {
            Image(systemName: item.icon)
                .font(.title3.weight(.medium))
                .foregroundStyle(AnnoTheme.goldLeaf)
                .frame(width: 40, height: 40)
                .background(
                    RoundedRectangle(cornerRadius: 8, style: .continuous)
                        .fill(AnnoTheme.goldLeaf.opacity(0.1))
                )

            VStack(alignment: .leading, spacing: 3) {
                Text(item.title(for: language))
                    .font(.subheadline.weight(.semibold))
                    .fontDesign(.serif)
                    .foregroundStyle(AnnoTheme.vellum)

                Text(item.subtitle(for: language))
                    .font(.caption)
                    .foregroundStyle(AnnoTheme.incense)
            }

            Spacer()

            Image(systemName: "lock.fill")
                .font(.caption)
                .foregroundStyle(AnnoTheme.incense.opacity(0.5))
        }
        .annoCard()
        .accessibilityElement(children: .combine)
        .accessibilityLabel(item.accessibilityLabel(for: language))
    }

    // MARK: - Mock Data

    private var mockCollections: [MockCollection] {
        [
            MockCollection(
                icon: "person.2.fill",
                titleEn: "Saints",
                titleVi: "Các Thánh",
                subtitleEn: "Feast days & martyrologies",
                subtitleVi: "Ngày lễ & sổ tử đạo",
                countPlaceholder: 365
            ),
            MockCollection(
                icon: "paintpalette.fill",
                titleEn: "Sacred Art",
                titleVi: "Nghệ Thuật Thánh",
                subtitleEn: "Paintings, icons & mosaics",
                subtitleVi: "Tranh, thánh tượng & khảm",
                countPlaceholder: 248
            ),
            MockCollection(
                icon: "mappin.and.ellipse",
                titleEn: "Pilgrimage Sites",
                titleVi: "Địa Điểm Hành Hương",
                subtitleEn: "Shrines, churches & holy wells",
                subtitleVi: "Đền thờ, nhà thờ & giếng thánh",
                countPlaceholder: 183
            )
        ]
    }
}

// MARK: - Mock Collection Model

private struct MockCollection {
    let icon: String
    let titleEn: String
    let titleVi: String
    let subtitleEn: String
    let subtitleVi: String
    let countPlaceholder: Int

    func title(for language: LanguageMode) -> String {
        language == .vietnamese ? titleVi : titleEn
    }

    func subtitle(for language: LanguageMode) -> String {
        language == .vietnamese ? subtitleVi : subtitleEn
    }

    func accessibilityLabel(for language: LanguageMode) -> String {
        if language == .vietnamese {
            return "\(titleVi), \(subtitleVi), bị khóa"
        }
        return "\(titleEn), \(subtitleEn), locked"
    }
}

// MARK: - Preview

#Preview {
    NavigationStack {
        SavedView(language: .english)
    }
    .preferredColorScheme(.dark)
}

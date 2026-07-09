import MapKit
import SwiftUI

struct SacredSiteMapView: View {
    let entries: [AnnoEntry]
    let language: LanguageMode

    /// Tracks whether the bottom sheet is expanded.
    @State private var sheetExpanded: Bool = false

    private var siteEntries: [AnnoEntry] {
        entries.filter { $0.place != nil }
    }

    /// Computes a region that fits all sacred site pins.
    private var fittingRegion: MapCameraPosition {
        let places = siteEntries.compactMap(\.place)
        guard !places.isEmpty else {
            return .automatic
        }

        let lats = places.map(\.latitude)
        let lons = places.map(\.longitude)

        guard let minLat = lats.min(), let maxLat = lats.max(),
              let minLon = lons.min(), let maxLon = lons.max() else {
            return .automatic
        }

        let center = CLLocationCoordinate2D(
            latitude: (minLat + maxLat) / 2,
            longitude: (minLon + maxLon) / 2
        )

        // Add padding so pins aren't on the edge.
        let latDelta = max((maxLat - minLat) * 1.4, 2.0)
        let lonDelta = max((maxLon - minLon) * 1.4, 2.0)

        return .region(MKCoordinateRegion(
            center: center,
            span: MKCoordinateSpan(latitudeDelta: latDelta, longitudeDelta: lonDelta)
        ))
    }

    var body: some View {
        ZStack(alignment: .top) {
            mapLayer

            // Atmospheric radial gradient overlay matching TodayView.
            atmosphereOverlay
        }
        .safeAreaInset(edge: .bottom) {
            bottomSheet
        }
        .background(AnnoTheme.narthex)
        .navigationTitle(language == .vietnamese ? "Bản đồ" : "Sacred Sites")
        .navigationBarTitleDisplayMode(.inline)
    }

    // MARK: - Map Layer

    private var mapLayer: some View {
        Map(initialPosition: fittingRegion) {
            ForEach(siteEntries) { entry in
                if let place = entry.place {
                    Annotation(
                        LocalizedEntryText(entry: entry, language: language).title,
                        coordinate: CLLocationCoordinate2D(
                            latitude: place.latitude,
                            longitude: place.longitude
                        ),
                        anchor: .bottom
                    ) {
                        sacredPinView(confidence: place.confidence, placeName: place.name)
                    }
                }
            }
        }
        .mapStyle(.standard(elevation: .realistic, emphasis: .muted))
        .ignoresSafeArea(edges: .top)
    }

    // MARK: - Custom Pin Annotation

    /// Gold pin with a small liturgical confidence-colored dot at its center.
    private func sacredPinView(confidence: ConfidenceLevel, placeName: String) -> some View {
        VStack(spacing: 0) {
            ZStack {
                // Outer gold pin body
                Image(systemName: "mappin.circle.fill")
                    .font(.system(size: 30, weight: .bold))
                    .foregroundStyle(AnnoTheme.goldLeaf)
                    .shadow(color: .black.opacity(0.5), radius: 4, y: 2)

                // Inner confidence-color dot
                Circle()
                    .fill(AnnoTheme.confidenceColor(confidence))
                    .frame(width: 10, height: 10)
                    .offset(y: -1)
            }

            // Pin tail shadow
            Image(systemName: "triangle.fill")
                .font(.system(size: 8))
                .foregroundStyle(AnnoTheme.goldLeaf)
                .rotationEffect(.degrees(180))
                .offset(y: -4)
                .shadow(color: .black.opacity(0.3), radius: 2, y: 1)
        }
        .accessibilityLabel(
            language == .vietnamese
                ? "Ghim địa điểm: \(placeName)"
                : "Sacred site pin: \(placeName)"
        )
        .accessibilityAddTraits(.isButton)
    }

    // MARK: - Atmosphere Overlay

    private var atmosphereOverlay: some View {
        RadialGradient(
            gradient: Gradient(colors: [
                AnnoTheme.narthex.opacity(0.6),
                AnnoTheme.narthex.opacity(0.0)
            ]),
            center: .top,
            startRadius: 0,
            endRadius: 200
        )
        .frame(height: 200)
        .allowsHitTesting(false)
        .ignoresSafeArea(edges: .top)
    }

    // MARK: - Bottom Sheet

    private var bottomSheet: some View {
        VStack(spacing: 0) {
            // Drag handle
            sheetHandle

            if sheetExpanded {
                sheetContent
                    .transition(.move(edge: .bottom).combined(with: .opacity))
            } else {
                sheetPeek
                    .transition(.opacity)
            }
        }
        .background {
            RoundedRectangle(cornerRadius: 16, style: .continuous)
                .fill(AnnoTheme.narthex)
                .shadow(color: .black.opacity(0.5), radius: 20, y: -8)
                .overlay(
                    RoundedRectangle(cornerRadius: 16, style: .continuous)
                        .stroke(AnnoTheme.ash, lineWidth: 1)
                )
        }
        .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
        .padding(.horizontal, 8)
        .padding(.bottom, 4)
    }

    private var sheetHandle: some View {
        VStack(spacing: 12) {
            Capsule()
                .fill(AnnoTheme.incense.opacity(0.5))
                .frame(width: 36, height: 4)
                .padding(.top, 10)

            Button {
                withAnimation(.spring(response: 0.35, dampingFraction: 0.8)) {
                    sheetExpanded.toggle()
                }
            } label: {
                HStack(spacing: 8) {
                    Image(systemName: "mappin.and.ellipse")
                        .foregroundStyle(AnnoTheme.goldLeaf)

                    Text(language == .vietnamese
                         ? "\(siteEntries.count) Địa điểm thánh"
                         : "\(siteEntries.count) Sacred Sites")
                        .font(.subheadline.weight(.semibold))
                        .fontDesign(.serif)
                        .foregroundStyle(AnnoTheme.vellum)

                    Spacer()

                    Image(systemName: sheetExpanded ? "chevron.down" : "chevron.up")
                        .font(.caption.weight(.bold))
                        .foregroundStyle(AnnoTheme.incense)
                }
                .padding(.horizontal, 16)
                .padding(.bottom, sheetExpanded ? 8 : 12)
            }
            .buttonStyle(.plain)
            .accessibilityLabel(
                language == .vietnamese
                    ? (sheetExpanded ? "Thu gọn danh sách" : "Mở rộng danh sách")
                    : (sheetExpanded ? "Collapse site list" : "Expand site list")
            )
            .accessibilityHint(
                language == .vietnamese
                    ? "\(siteEntries.count) địa điểm thánh"
                    : "\(siteEntries.count) sacred sites"
            )
        }
    }

    private var sheetPeek: some View {
        EmptyView()
    }

    private var sheetContent: some View {
        ScrollView {
            SacredSiteListView(entries: siteEntries, language: language)
                .padding(.horizontal, 8)
                .padding(.bottom, 16)
        }
        .frame(maxHeight: 360)
    }
}

// MARK: - Preview

#Preview {
    NavigationStack {
        SacredSiteMapView(
            entries: [
                AnnoEntry(
                    id: "2026-07-03",
                    date: "2026-07-03",
                    weekday: "Friday",
                    mockPriority: "week_real_data",
                    liturgical: LiturgicalInfo(
                        rank: "Feast", color: "Red",
                        titleEn: "St. Thomas, Apostle",
                        titleVi: "Thánh Tôma, Tông đồ"
                    ),
                    calendars: CalendarConversions(
                        julian: "June 20, 2026", hebrew: "18 Tammuz 5786",
                        islamicUmmAlQura: "18 Muharram 1448",
                        coptic: "26 Paoni 1742", ethiopian: "26 Sene 2018"
                    ),
                    primary: PrimaryContent(
                        type: "Feast",
                        titleEn: "Feast of Saint Thomas the Apostle",
                        titleVi: "Lễ Thánh Tôma Tông Đồ",
                        summaryEn: "Saint Thomas was one of the Twelve Apostles.",
                        summaryVi: "Thánh Tôma là một trong Mười Hai Tông Đồ.",
                        confidence: .confirmed,
                        confidenceNoteEn: "Universally recognized.",
                        confidenceNoteVi: "Được công nhận rộng rãi."
                    ),
                    place: SacredPlace(
                        name: "St. Thomas Mount",
                        latitude: 13.0067, longitude: 80.2020,
                        confidence: .traditional,
                        sourceUrl: "https://en.wikipedia.org/wiki/St._Thomas_Mount"
                    ),
                    artwork: ArtworkCandidate(
                        title: "The Incredulity of Saint Thomas",
                        maker: "Caravaggio", dateLabel: "c. 1601–1602",
                        sourceUrl: "", status: "Public Domain"
                    ),
                    sources: [],
                    appHooks: AppHooks(
                        heroLineEn: "Blessed are those who have not seen and yet have believed.",
                        heroLineVi: "Phúc cho những ai không thấy mà tin.",
                        prayerPromptEn: "", prayerPromptVi: ""
                    )
                )
            ],
            language: .english
        )
    }
    .preferredColorScheme(.dark)
}

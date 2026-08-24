import MapKit
import SwiftUI

public enum MapExplorationMode: String, CaseIterable, Identifiable {
    case pilgrimages = "Pilgrimages"
    case sanctuaries = "Sanctuaries"
    case feastSites = "Feast Sites"

    public var id: String { rawValue }

    public func title(for language: LanguageMode) -> String {
        switch self {
        case .pilgrimages:
            return language == .vietnamese ? "Đại Lộ Hành Hương" : "Pilgrimage Routes"
        case .sanctuaries:
            return language == .vietnamese ? "72 Thánh Địa" : "72 Sanctuaries"
        case .feastSites:
            return language == .vietnamese ? "Địa Điểm Lễ" : "Feast Sites"
        }
    }
}

public struct SacredSiteMapView: View {
    public let entries: [AnnoEntry]
    public let currentEntry: AnnoEntry?
    public let language: LanguageMode

    @StateObject private var geoLoader = SacredGeographyLoader.shared
    @StateObject private var audioPlayer = AudioDevotionalPlayer.shared

    @State private var mode: MapExplorationMode = .pilgrimages
    @State private var selectedCalling: SpiritualCalling = .all
    @State private var selectedRegion: PilgrimageRegion = .all
    @State private var sheetExpanded: Bool = false
    @State private var selectedWaypoint: PilgrimageWaypoint?
    @State private var selectedSanctuary: Sanctuary?
    @State private var position: MapCameraPosition = .automatic

    public init(entries: [AnnoEntry], currentEntry: AnnoEntry? = nil, language: LanguageMode) {
        self.entries = entries
        self.currentEntry = currentEntry ?? entries.first
        self.language = language
    }

    private var siteEntries: [AnnoEntry] {
        entries.filter { $0.place != nil }
    }

    private var filteredRoutes: [PilgrimageRoute] {
        geoLoader.routes.filter { route in
            let callingMatch = (selectedCalling == .all || route.calling == selectedCalling)
            let regionMatch = (selectedRegion == .all || route.regionCategory == selectedRegion)
            return callingMatch && regionMatch
        }
    }

    private var connectedRoutesToToday: [PilgrimageRoute] {
        guard let today = currentEntry else { return [] }
        return geoLoader.routes.filter { $0.isLiturgicallyConnected(to: today) }
    }

    public var body: some View {
        ZStack(alignment: .top) {
            mapLayer

            // Atmospheric gradient & Inquiry Controls
            VStack(spacing: 8) {
                atmosphereOverlay

                inquiryHeaderView

                modePickerBar
                    .padding(.horizontal, 16)

                if mode == .pilgrimages {
                    callingFilterCarousel
                    routeSelectionCarousel
                } else if mode == .sanctuaries {
                    sanctuaryCategoryFilter
                }
            }
        }
        .safeAreaInset(edge: .bottom) {
            bottomSheet
        }
        .background(AnnoTheme.narthex)
        .navigationTitle(language == .vietnamese ? "Bản đồ Thánh Địa" : "Sacred Geography")
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            if geoLoader.routes.isEmpty {
                geoLoader.loadData()
            }
            updateCameraPosition()
        }
        .onChange(of: mode) { _ in
            updateCameraPosition()
        }
        .onChange(of: geoLoader.selectedRoute) { _ in
            updateCameraPosition()
        }
    }

    // MARK: - Spiritual Inquiry Header

    private var inquiryHeaderView: some View {
        VStack(spacing: 4) {
            Text(language == .vietnamese
                 ? "Hôm nay bạn muốn bước theo con đường của ai?"
                 : "Whose path will you walk today?")
                .font(.system(size: 15, weight: .semibold, design: .serif))
                .foregroundStyle(
                    LinearGradient(
                        colors: [AnnoTheme.gilt, AnnoTheme.goldLeaf],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
                .shadow(color: AnnoTheme.goldLeaf.opacity(0.3), radius: 6, y: 1)

            if let today = currentEntry, !connectedRoutesToToday.isEmpty {
                HStack(spacing: 5) {
                    Image(systemName: "sparkles")
                        .font(.system(size: 10))
                        .foregroundStyle(AnnoTheme.candleGlow)
                    Text(language == .vietnamese
                         ? "Gắn liền với lễ: \(today.liturgical.titleVi)"
                         : "In season with: \(today.liturgical.titleEn)")
                        .font(.caption2)
                        .fontDesign(.serif)
                        .foregroundStyle(AnnoTheme.vellum.opacity(0.85))
                }
                .padding(.horizontal, 10)
                .padding(.vertical, 2)
                .background(
                    Capsule()
                        .fill(AnnoTheme.narthex.opacity(0.75))
                        .overlay(Capsule().stroke(AnnoTheme.goldLeaf.opacity(0.35), lineWidth: 0.8))
                )
            }
        }
        .padding(.horizontal, 16)
        .padding(.top, 4)
    }

    // MARK: - Map Layer

    private var mapLayer: some View {
        Map(position: $position) {
            switch mode {
            case .feastSites:
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

            case .pilgrimages:
                if let route = geoLoader.selectedRoute {
                    // Glowing gold pilgrimage path
                    MapPolyline(coordinates: route.coordinates)
                        .stroke(
                            LinearGradient(
                                colors: [AnnoTheme.gilt, AnnoTheme.goldLeaf, AnnoTheme.candleGlow],
                                startPoint: .leading,
                                endPoint: .trailing
                            ),
                            style: StrokeStyle(lineWidth: 4.5, lineCap: .round, lineJoin: .round)
                        )

                    // Numbered Waypoints with Halo
                    ForEach(route.waypoints) { wp in
                        Annotation(
                            wp.name(for: language),
                            coordinate: wp.coordinate,
                            anchor: .bottom
                        ) {
                            Button {
                                Haptics.light()
                                withAnimation(.spring(response: 0.35, dampingFraction: 0.8)) {
                                    selectedWaypoint = wp
                                    sheetExpanded = true
                                }
                            } label: {
                                waypointPinView(waypoint: wp, isSelected: (selectedWaypoint ?? route.waypoints.first)?.id == wp.id)
                            }
                            .buttonStyle(.plain)
                        }
                    }
                }

            case .sanctuaries:
                ForEach(geoLoader.filteredSanctuaries(category: geoLoader.selectedCategory)) { sanctuary in
                    Annotation(
                        sanctuary.name(for: language),
                        coordinate: sanctuary.coordinate,
                        anchor: .bottom
                    ) {
                        Button {
                            Haptics.light()
                            withAnimation(.spring(response: 0.35, dampingFraction: 0.8)) {
                                selectedSanctuary = sanctuary
                                sheetExpanded = true
                            }
                        } label: {
                            sanctuaryPinView(sanctuary: sanctuary, isSelected: selectedSanctuary?.id == sanctuary.id)
                        }
                        .buttonStyle(.plain)
                    }
                }
            }
        }
        .mapStyle(.standard(elevation: .realistic, emphasis: .muted))
        .ignoresSafeArea(edges: .top)
    }

    // MARK: - Mode Picker Bar

    private var modePickerBar: some View {
        HStack(spacing: 6) {
            ForEach(MapExplorationMode.allCases) { m in
                Button {
                    Haptics.selection()
                    withAnimation(.spring(response: 0.3, dampingFraction: 0.8)) {
                        mode = m
                        sheetExpanded = false
                    }
                } label: {
                    Text(m.title(for: language))
                        .font(.caption.weight(mode == m ? .bold : .medium))
                        .fontDesign(.serif)
                        .foregroundStyle(mode == m ? AnnoTheme.narthex : AnnoTheme.vellum)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 8)
                        .background {
                            if mode == m {
                                Capsule()
                                    .fill(
                                        LinearGradient(
                                            colors: [AnnoTheme.gilt, AnnoTheme.goldLeaf],
                                            startPoint: .topLeading,
                                            endPoint: .bottomTrailing
                                        )
                                    )
                                    .shadow(color: AnnoTheme.goldLeaf.opacity(0.4), radius: 6, y: 2)
                            } else {
                                Capsule()
                                    .fill(AnnoTheme.narthex.opacity(0.85))
                                    .overlay(Capsule().stroke(AnnoTheme.ash, lineWidth: 1))
                            }
                        }
                }
                .buttonStyle(.plain)
            }
        }
        .padding(4)
        .background(
            Capsule()
                .fill(AnnoTheme.narthex.opacity(0.85))
                .shadow(color: .black.opacity(0.4), radius: 10, y: 4)
        )
    }

    // MARK: - Spiritual Calling Filter

    private var callingFilterCarousel: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 6) {
                ForEach(SpiritualCalling.allCases) { calling in
                    let isSelected = selectedCalling == calling
                    Button {
                        Haptics.selection()
                        withAnimation(.spring(response: 0.3, dampingFraction: 0.8)) {
                            selectedCalling = calling
                            if let firstMatch = filteredRoutes.first {
                                geoLoader.selectedRoute = firstMatch
                                selectedWaypoint = firstMatch.waypoints.first
                            }
                        }
                    } label: {
                        HStack(spacing: 4) {
                            Image(systemName: calling.icon)
                                .font(.system(size: 10))
                            Text(calling.title(for: language))
                                .font(.caption2.weight(isSelected ? .bold : .regular))
                                .fontDesign(.serif)
                        }
                        .foregroundStyle(isSelected ? AnnoTheme.narthex : AnnoTheme.vellum)
                        .padding(.horizontal, 10)
                        .padding(.vertical, 5)
                        .background(
                            Capsule()
                                .fill(isSelected ? AnnoTheme.goldLeaf : AnnoTheme.narthex.opacity(0.8))
                                .overlay(Capsule().stroke(isSelected ? AnnoTheme.goldLeaf : AnnoTheme.ash, lineWidth: 1))
                        )
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.horizontal, 16)
        }
    }

    // MARK: - Route Selection Carousel

    private var routeSelectionCarousel: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                ForEach(filteredRoutes) { route in
                    let isSelected = geoLoader.selectedRoute?.id == route.id
                    let isConnected = currentEntry.map { route.isLiturgicallyConnected(to: $0) } ?? false

                    Button {
                        Haptics.light()
                        withAnimation(.spring(response: 0.35, dampingFraction: 0.8)) {
                            geoLoader.selectedRoute = route
                            selectedWaypoint = route.waypoints.first
                        }
                    } label: {
                        HStack(spacing: 6) {
                            if isConnected {
                                Image(systemName: "sparkles")
                                    .font(.caption2)
                                    .foregroundStyle(AnnoTheme.goldLeaf)
                            } else {
                                Image(systemName: "figure.walk")
                                    .font(.caption2)
                                    .foregroundStyle(isSelected ? AnnoTheme.goldLeaf : AnnoTheme.incense)
                            }

                            Text(route.title(for: language))
                                .font(.caption.weight(isSelected ? .semibold : .regular))
                                .fontDesign(.serif)
                                .foregroundStyle(isSelected ? AnnoTheme.vellum : AnnoTheme.incense)
                                .lineLimit(1)

                            Text("(\(route.waypoints.count))")
                                .font(.caption2.monospacedDigit())
                                .foregroundStyle(AnnoTheme.goldLeaf.opacity(0.85))
                        }
                        .padding(.horizontal, 10)
                        .padding(.vertical, 6)
                        .background(
                            RoundedRectangle(cornerRadius: 8)
                                .fill(isSelected ? AnnoTheme.goldLeaf.opacity(0.18) : AnnoTheme.narthex.opacity(0.8))
                                .overlay(
                                    RoundedRectangle(cornerRadius: 8)
                                        .stroke(isSelected ? AnnoTheme.goldLeaf : (isConnected ? AnnoTheme.goldLeaf.opacity(0.5) : AnnoTheme.ash), lineWidth: isSelected ? 1.5 : 1)
                                )
                        )
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.horizontal, 16)
        }
    }

    // MARK: - Sanctuary Category Filter

    private var sanctuaryCategoryFilter: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 6) {
                Button {
                    Haptics.selection()
                    withAnimation { geoLoader.selectedCategory = nil }
                } label: {
                    Text(language == .vietnamese ? "Tất cả (72)" : "All (72)")
                        .font(.caption2.weight(geoLoader.selectedCategory == nil ? .bold : .regular))
                        .fontDesign(.serif)
                        .foregroundStyle(geoLoader.selectedCategory == nil ? AnnoTheme.narthex : AnnoTheme.vellum)
                        .padding(.horizontal, 10)
                        .padding(.vertical, 5)
                        .background(Capsule().fill(geoLoader.selectedCategory == nil ? AnnoTheme.goldLeaf : AnnoTheme.narthex.opacity(0.8)).overlay(Capsule().stroke(AnnoTheme.ash, lineWidth: 1)))
                }
                .buttonStyle(.plain)

                ForEach(geoLoader.availableCategories, id: \.self) { cat in
                    let isSelected = geoLoader.selectedCategory == cat
                    Button {
                        Haptics.selection()
                        withAnimation { geoLoader.selectedCategory = cat }
                    } label: {
                        Text(cat.replacingOccurrences(of: "_", with: " ").capitalized)
                            .font(.caption2.weight(isSelected ? .bold : .regular))
                            .fontDesign(.serif)
                            .foregroundStyle(isSelected ? AnnoTheme.narthex : AnnoTheme.vellum)
                            .padding(.horizontal, 10)
                            .padding(.vertical, 5)
                            .background(Capsule().fill(isSelected ? AnnoTheme.goldLeaf : AnnoTheme.narthex.opacity(0.8)).overlay(Capsule().stroke(AnnoTheme.ash, lineWidth: 1)))
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.horizontal, 16)
        }
    }

    // MARK: - Custom Pin Views

    private func waypointPinView(waypoint: PilgrimageWaypoint, isSelected: Bool) -> some View {
        VStack(spacing: 0) {
            ZStack {
                if isSelected {
                    Circle()
                        .stroke(AnnoTheme.goldLeaf.opacity(0.4), lineWidth: 5)
                        .frame(width: 42, height: 42)
                }

                Circle()
                    .fill(isSelected ? AnnoTheme.goldLeaf : AnnoTheme.narthex)
                    .frame(width: isSelected ? 32 : 26, height: isSelected ? 32 : 26)
                    .overlay(Circle().stroke(AnnoTheme.goldLeaf, lineWidth: 1.5))
                    .shadow(color: .black.opacity(0.6), radius: 4, y: 2)

                Text("\(waypoint.order)")
                    .font(.caption.weight(.bold))
                    .fontDesign(.serif)
                    .foregroundStyle(isSelected ? AnnoTheme.narthex : AnnoTheme.goldLeaf)
            }

            Image(systemName: "triangle.fill")
                .font(.system(size: 6))
                .foregroundStyle(AnnoTheme.goldLeaf)
                .rotationEffect(.degrees(180))
                .offset(y: -2)
        }
    }

    private func sanctuaryPinView(sanctuary: Sanctuary, isSelected: Bool) -> some View {
        VStack(spacing: 0) {
            ZStack {
                if isSelected {
                    Circle()
                        .stroke(AnnoTheme.goldLeaf.opacity(0.4), lineWidth: 4)
                        .frame(width: 38, height: 38)
                }

                Circle()
                    .fill(isSelected ? AnnoTheme.goldLeaf : AnnoTheme.narthex)
                    .frame(width: 28, height: 28)
                    .overlay(Circle().stroke(AnnoTheme.confidenceColor(sanctuary.canonicalStatus.confidenceLevel), lineWidth: 1.8))
                    .shadow(color: .black.opacity(0.5), radius: 4, y: 2)

                Image(systemName: "cross.fill")
                    .font(.system(size: 11))
                    .foregroundStyle(isSelected ? AnnoTheme.narthex : AnnoTheme.goldLeaf)
            }

            Image(systemName: "triangle.fill")
                .font(.system(size: 6))
                .foregroundStyle(AnnoTheme.goldLeaf)
                .rotationEffect(.degrees(180))
                .offset(y: -2)
        }
    }

    private func sacredPinView(confidence: ConfidenceLevel, placeName: String) -> some View {
        VStack(spacing: 0) {
            ZStack {
                Image(systemName: "mappin.circle.fill")
                    .font(.system(size: 30, weight: .bold))
                    .foregroundStyle(AnnoTheme.goldLeaf)
                    .shadow(color: .black.opacity(0.5), radius: 4, y: 2)

                Circle()
                    .fill(AnnoTheme.confidenceColor(confidence))
                    .frame(width: 10, height: 10)
                    .offset(y: -1)
            }

            Image(systemName: "triangle.fill")
                .font(.system(size: 8))
                .foregroundStyle(AnnoTheme.goldLeaf)
                .rotationEffect(.degrees(180))
                .offset(y: -4)
                .shadow(color: .black.opacity(0.3), radius: 2, y: 1)
        }
    }

    // MARK: - Atmosphere Overlay

    private var atmosphereOverlay: some View {
        RadialGradient(
            gradient: Gradient(colors: [
                AnnoTheme.narthex.opacity(0.92),
                AnnoTheme.narthex.opacity(0.0)
            ]),
            center: .top,
            startRadius: 0,
            endRadius: 180
        )
        .frame(height: 140)
        .allowsHitTesting(false)
        .ignoresSafeArea(edges: .top)
    }

    // MARK: - Bottom Sheet

    private var bottomSheet: some View {
        VStack(spacing: 0) {
            sheetHandle

            if sheetExpanded {
                sheetDetailContent
                    .transition(.move(edge: .bottom).combined(with: .opacity))
            }
        }
        .background {
            RoundedRectangle(cornerRadius: 20, style: .continuous)
                .fill(AnnoTheme.narthex.opacity(0.94))
                .background(.ultraThinMaterial.opacity(0.4))
                .shadow(color: .black.opacity(0.65), radius: 24, y: -10)
                .overlay(
                    RoundedRectangle(cornerRadius: 20, style: .continuous)
                        .stroke(
                            LinearGradient(
                                colors: [AnnoTheme.goldLeaf.opacity(0.4), AnnoTheme.ash],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            ),
                            lineWidth: 1
                        )
                )
        }
        .clipShape(RoundedRectangle(cornerRadius: 20, style: .continuous))
        .padding(.horizontal, 8)
        .padding(.bottom, 4)
    }

    private var sheetHandle: some View {
        VStack(spacing: 8) {
            Capsule()
                .fill(AnnoTheme.incense.opacity(0.4))
                .frame(width: 36, height: 4)
                .padding(.top, 10)

            Button {
                Haptics.selection()
                withAnimation(.spring(response: 0.35, dampingFraction: 0.8)) {
                    sheetExpanded.toggle()
                }
            } label: {
                HStack(spacing: 8) {
                    Image(systemName: mode == .pilgrimages ? "map.circle.fill" : "mappin.and.ellipse")
                        .foregroundStyle(AnnoTheme.goldLeaf)

                    Text(sheetTitle)
                        .font(.subheadline.weight(.semibold))
                        .fontDesign(.serif)
                        .foregroundStyle(AnnoTheme.vellum)
                        .lineLimit(1)

                    Spacer()

                    Image(systemName: sheetExpanded ? "chevron.down" : "chevron.up")
                        .font(.caption.weight(.bold))
                        .foregroundStyle(AnnoTheme.incense)
                }
                .padding(.horizontal, 16)
                .padding(.bottom, sheetExpanded ? 8 : 12)
            }
            .buttonStyle(.plain)
        }
    }

    private var sheetTitle: String {
        switch mode {
        case .feastSites:
            return language == .vietnamese ? "\(siteEntries.count) Địa điểm Lễ" : "\(siteEntries.count) Sacred Feast Sites"
        case .pilgrimages:
            if let r = geoLoader.selectedRoute {
                return "\(r.title(for: language)) (\(r.waypoints.count) Stations)"
            }
            return language == .vietnamese ? "Đại lộ hành hương" : "Pilgrimage Highway"
        case .sanctuaries:
            if let s = selectedSanctuary {
                return s.name(for: language)
            }
            return language == .vietnamese ? "72 Thánh địa Hoàn Vũ" : "72 Global Sanctuaries"
        }
    }

    private var sheetDetailContent: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                switch mode {
                case .feastSites:
                    SacredSiteListView(entries: siteEntries, language: language)

                case .pilgrimages:
                    if let route = geoLoader.selectedRoute {
                        pilgrimageRouteDetailView(route: route)
                    }

                case .sanctuaries:
                    if let sanctuary = selectedSanctuary {
                        sanctuaryDetailView(sanctuary: sanctuary)
                    } else {
                        sanctuaryListView
                    }
                }
            }
            .padding(.horizontal, 16)
            .padding(.bottom, 20)
        }
        .frame(maxHeight: 420)
    }

    // MARK: - Route Detail View

    private func pilgrimageRouteDetailView(route: PilgrimageRoute) -> some View {
        VStack(alignment: .leading, spacing: 14) {
            // Spiritual theme & badges
            HStack(spacing: 8) {
                Label("\(route.durationDays) \(language == .vietnamese ? "ngày" : "days")", systemImage: "clock")
                Label(route.difficultyDisplay, systemImage: "figure.walk")
                if route.distanceKm > 0 {
                    Label(String(format: "%.0f km", route.distanceKm), systemImage: "ruler")
                }
                if let today = currentEntry, route.isLiturgicallyConnected(to: today) {
                    HStack(spacing: 3) {
                        Image(systemName: "sparkles")
                        Text(language == .vietnamese ? "Hôm nay" : "Today")
                    }
                    .font(.caption2.weight(.bold))
                    .foregroundStyle(AnnoTheme.narthex)
                    .padding(.horizontal, 6)
                    .padding(.vertical, 2)
                    .background(Capsule().fill(AnnoTheme.goldLeaf))
                }
            }
            .font(.caption2)
            .foregroundStyle(AnnoTheme.goldLeaf)

            Text(route.spiritualTheme(for: language))
                .font(.subheadline.italic())
                .fontDesign(.serif)
                .foregroundStyle(AnnoTheme.vellum)

            Divider().background(AnnoTheme.ash)

            // Selected Waypoint Focus
            let currentWp = selectedWaypoint ?? route.waypoints.first
            if let wp = currentWp {
                VStack(alignment: .leading, spacing: 10) {
                    HStack(alignment: .top) {
                        VStack(alignment: .leading, spacing: 2) {
                            Text("Station \(wp.order): \(wp.name(for: language))")
                                .font(.headline)
                                .fontDesign(.serif)
                                .foregroundStyle(AnnoTheme.goldLeaf)
                        }

                        Spacer()

                        HStack(spacing: 8) {
                            if let mapsUrl = appleMapsUrl(latitude: wp.latitude, longitude: wp.longitude) {
                                Link(destination: mapsUrl) {
                                    Image(systemName: "arrow.triangle.turn.up.right.diamond.fill")
                                        .font(.caption)
                                        .foregroundStyle(AnnoTheme.goldLeaf)
                                        .padding(7)
                                        .background(Circle().fill(AnnoTheme.goldLeaf.opacity(0.15)))
                                }
                            }
                        }
                    }

                    Text(wp.historicalSummary(for: language))
                        .font(.caption)
                        .lineSpacing(3)
                        .foregroundStyle(AnnoTheme.vellum.opacity(0.92))

                    if !wp.sacredRelic(for: language).isEmpty {
                        HStack(alignment: .top, spacing: 8) {
                            Image(systemName: "sparkles")
                                .font(.caption2)
                                .foregroundStyle(AnnoTheme.goldLeaf)
                            VStack(alignment: .leading, spacing: 2) {
                                Text(language == .vietnamese ? "Thánh Tích & Di Sản" : "Sacred Relics")
                                    .font(.caption2.weight(.bold))
                                    .foregroundStyle(AnnoTheme.goldLeaf)
                                Text(wp.sacredRelic(for: language))
                                    .font(.caption2)
                                    .foregroundStyle(AnnoTheme.vellum)
                            }
                        }
                        .padding(10)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(
                            RoundedRectangle(cornerRadius: 8)
                                .fill(AnnoTheme.choir.opacity(0.6))
                                .overlay(RoundedRectangle(cornerRadius: 8).stroke(AnnoTheme.goldLeaf.opacity(0.2), lineWidth: 0.8))
                        )
                    }

                    if !wp.suggestedPrayer(for: language).isEmpty {
                        VStack(alignment: .leading, spacing: 4) {
                            Text(language == .vietnamese ? "Lời Nguyện Hành Hương" : "Pilgrim's Prayer")
                                .font(.caption2.weight(.bold))
                                .foregroundStyle(AnnoTheme.goldLeaf)

                            Text(wp.suggestedPrayer(for: language))
                                .font(.caption.italic())
                                .fontDesign(.serif)
                                .lineSpacing(2)
                                .foregroundStyle(AnnoTheme.vellum)
                        }
                        .padding(12)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(
                            RoundedRectangle(cornerRadius: 10)
                                .fill(AnnoTheme.narthex)
                                .overlay(RoundedRectangle(cornerRadius: 10).stroke(AnnoTheme.goldLeaf.opacity(0.35), lineWidth: 1))
                        )
                    }

                    // Multimedia & AR Action Buttons
                    HStack(spacing: 8) {
                        Button {
                            Haptics.light()
                            SacredSpatialAudioEngine.shared.playStationNarration(waypoint: wp, language: language)
                        } label: {
                            HStack(spacing: 6) {
                                Image(systemName: "speaker.wave.2.fill")
                                Text(language == .vietnamese ? "Nghe Lời Nguyện" : "Listen to Prayer")
                            }
                            .font(.caption2.weight(.semibold))
                            .foregroundStyle(AnnoTheme.narthex)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 8)
                            .background(
                                Capsule()
                                    .fill(
                                        LinearGradient(
                                            colors: [AnnoTheme.gilt, AnnoTheme.goldLeaf],
                                            startPoint: .topLeading,
                                            endPoint: .bottomTrailing
                                        )
                                    )
                            )
                        }
                        .buttonStyle(.plain)

                        if let _ = wp.associated3DReliquaryId {
                            Button {
                                Haptics.selection()
                            } label: {
                                HStack(spacing: 6) {
                                    Image(systemName: "arkit")
                                    Text(language == .vietnamese ? "Chiêm Ngắm 3D" : "View in AR")
                                }
                                .font(.caption2.weight(.semibold))
                                .foregroundStyle(AnnoTheme.goldLeaf)
                                .padding(.horizontal, 12)
                                .padding(.vertical, 8)
                                .background(
                                    Capsule()
                                        .fill(AnnoTheme.choir.opacity(0.8))
                                        .overlay(Capsule().stroke(AnnoTheme.goldLeaf.opacity(0.6), lineWidth: 1))
                                )
                            }
                            .buttonStyle(.plain)
                        }
                    }
                    .padding(.top, 2)

                    // Stepper Navigation
                    HStack {
                        let currentIndex = route.waypoints.firstIndex(where: { $0.id == wp.id }) ?? 0
                        if currentIndex > 0 {
                            Button {
                                Haptics.selection()
                                withAnimation {
                                    selectedWaypoint = route.waypoints[currentIndex - 1]
                                }
                            } label: {
                                HStack(spacing: 4) {
                                    Image(systemName: "chevron.left")
                                    Text(language == .vietnamese ? "Trạm trước" : "Prev Station")
                                }
                                .font(.caption2.weight(.medium))
                                .foregroundStyle(AnnoTheme.incense)
                            }
                        }

                        Spacer()

                        if currentIndex < route.waypoints.count - 1 {
                            Button {
                                Haptics.selection()
                                withAnimation {
                                    selectedWaypoint = route.waypoints[currentIndex + 1]
                                }
                            } label: {
                                HStack(spacing: 4) {
                                    Text(language == .vietnamese ? "Trạm kế tiếp" : "Next Station")
                                    Image(systemName: "chevron.right")
                                }
                                .font(.caption2.weight(.semibold))
                                .foregroundStyle(AnnoTheme.goldLeaf)
                            }
                        }
                    }
                    .padding(.top, 4)
                }
            }

            // Waypoints Quick Switcher
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 8) {
                    ForEach(route.waypoints) { wp in
                        let isSel = (selectedWaypoint ?? route.waypoints.first)?.id == wp.id
                        Button {
                            Haptics.light()
                            withAnimation {
                                selectedWaypoint = wp
                            }
                        } label: {
                            Text("\(wp.order). \(wp.name(for: language))")
                                .font(.caption2)
                                .fontDesign(.serif)
                                .foregroundStyle(isSel ? AnnoTheme.narthex : AnnoTheme.vellum)
                                .padding(.horizontal, 10)
                                .padding(.vertical, 5)
                                .background(Capsule().fill(isSel ? AnnoTheme.goldLeaf : AnnoTheme.ash))
                        }
                        .buttonStyle(.plain)
                    }
                }
            }
        }
    }

    // MARK: - Sanctuary Detail View

    private func sanctuaryDetailView(sanctuary: Sanctuary) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                VStack(alignment: .leading, spacing: 2) {
                    Text(sanctuary.name(for: language))
                        .font(.headline)
                        .fontDesign(.serif)
                        .foregroundStyle(AnnoTheme.goldLeaf)

                    Text("\(sanctuary.location.city), \(sanctuary.location.country)")
                        .font(.caption2)
                        .foregroundStyle(AnnoTheme.incense)
                }

                Spacer()

                if let mapsUrl = appleMapsUrl(latitude: sanctuary.location.latitude, longitude: sanctuary.location.longitude) {
                    Link(destination: mapsUrl) {
                        Image(systemName: "arrow.triangle.turn.up.right.diamond.fill")
                            .font(.caption)
                            .foregroundStyle(AnnoTheme.goldLeaf)
                            .padding(6)
                            .background(Circle().fill(AnnoTheme.goldLeaf.opacity(0.15)))
                    }
                }
            }

            Text(sanctuary.historicalSummary(for: language))
                .font(.caption)
                .lineSpacing(3)
                .foregroundStyle(AnnoTheme.vellum)

            if !sanctuary.suggestedPrayer(for: language).isEmpty {
                VStack(alignment: .leading, spacing: 4) {
                    Text(language == .vietnamese ? "Lời Nguyện Thánh Địa" : "Sanctuary Prayer")
                        .font(.caption2.weight(.bold))
                        .foregroundStyle(AnnoTheme.goldLeaf)

                    Text(sanctuary.suggestedPrayer(for: language))
                        .font(.caption.italic())
                        .fontDesign(.serif)
                        .foregroundStyle(AnnoTheme.vellum)
                }
                .padding(12)
                .background(RoundedRectangle(cornerRadius: 10).fill(AnnoTheme.narthex).overlay(RoundedRectangle(cornerRadius: 10).stroke(AnnoTheme.goldLeaf.opacity(0.35), lineWidth: 1)))
            }

            // Multimedia & AR Action Buttons
            HStack(spacing: 8) {
                Button {
                    Haptics.light()
                    AudioDevotionalPlayer.shared.play(
                        trackId: sanctuary.id,
                        title: sanctuary.name(for: language),
                        saint: sanctuary.categoryDisplay,
                        audioUrl: "bundle://hagiography_\(sanctuary.id)",
                        duration: 180
                    )
                } label: {
                    HStack(spacing: 6) {
                        Image(systemName: "speaker.wave.2.fill")
                        Text(language == .vietnamese ? "Nghe Lời Nguyện" : "Listen to Prayer")
                    }
                    .font(.caption2.weight(.semibold))
                    .foregroundStyle(AnnoTheme.narthex)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 8)
                    .background(
                        Capsule()
                            .fill(
                                LinearGradient(
                                    colors: [AnnoTheme.gilt, AnnoTheme.goldLeaf],
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                            )
                    )
                }
                .buttonStyle(.plain)

                if let _ = sanctuary.associated3DReliquaryId {
                    Button {
                        Haptics.selection()
                    } label: {
                        HStack(spacing: 6) {
                            Image(systemName: "arkit")
                            Text(language == .vietnamese ? "Chiêm Ngắm 3D" : "View in AR")
                        }
                        .font(.caption2.weight(.semibold))
                        .foregroundStyle(AnnoTheme.goldLeaf)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 8)
                        .background(
                            Capsule()
                                .fill(AnnoTheme.choir.opacity(0.8))
                                .overlay(Capsule().stroke(AnnoTheme.goldLeaf.opacity(0.6), lineWidth: 1))
                        )
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.top, 2)
        }
    }

    private var sanctuaryListView: some View {
        VStack(spacing: 8) {
            ForEach(geoLoader.filteredSanctuaries(category: geoLoader.selectedCategory)) { s in
                Button {
                    Haptics.selection()
                    withAnimation {
                        selectedSanctuary = s
                    }
                } label: {
                    HStack {
                        VStack(alignment: .leading, spacing: 2) {
                            Text(s.name(for: language))
                                .font(.caption.weight(.semibold))
                                .fontDesign(.serif)
                                .foregroundStyle(AnnoTheme.vellum)
                            Text("\(s.location.city), \(s.location.country)")
                                .font(.caption2)
                                .foregroundStyle(AnnoTheme.incense)
                        }
                        Spacer()
                        Image(systemName: "chevron.right")
                            .font(.caption2)
                            .foregroundStyle(AnnoTheme.incense)
                    }
                    .padding(10)
                    .background(RoundedRectangle(cornerRadius: 8).fill(AnnoTheme.choir.opacity(0.5)).overlay(RoundedRectangle(cornerRadius: 8).stroke(AnnoTheme.ash, lineWidth: 0.8)))
                }
                .buttonStyle(.plain)
            }
        }
    }

    // MARK: - Camera & Coordinate Math

    private func updateCameraPosition() {
        switch mode {
        case .feastSites:
            let places = siteEntries.compactMap(\.place)
            if !places.isEmpty {
                let coords = places.map { CLLocationCoordinate2D(latitude: $0.latitude, longitude: $0.longitude) }
                fitCoordinates(coords)
            }
        case .pilgrimages:
            if let r = geoLoader.selectedRoute, !r.waypoints.isEmpty {
                fitCoordinates(r.coordinates)
            }
        case .sanctuaries:
            let list = geoLoader.filteredSanctuaries(category: geoLoader.selectedCategory)
            if !list.isEmpty {
                fitCoordinates(list.map(\.coordinate))
            }
        }
    }

    private func fitCoordinates(_ coords: [CLLocationCoordinate2D]) {
        guard !coords.isEmpty else { return }
        let lats = coords.map(\.latitude)
        let lons = coords.map(\.longitude)

        guard let minLat = lats.min(), let maxLat = lats.max(),
              let minLon = lons.min(), let maxLon = lons.max() else { return }

        let center = CLLocationCoordinate2D(
            latitude: (minLat + maxLat) / 2,
            longitude: (minLon + maxLon) / 2
        )

        let latDelta = max((maxLat - minLat) * 1.5, 0.05)
        let lonDelta = max((maxLon - minLon) * 1.5, 0.05)

        position = .region(MKCoordinateRegion(
            center: center,
            span: MKCoordinateSpan(latitudeDelta: latDelta, longitudeDelta: lonDelta)
        ))
    }

    private func appleMapsUrl(latitude: Double, longitude: Double) -> URL? {
        var components = URLComponents()
        components.scheme = "http"
        components.host = "maps.apple.com"
        components.queryItems = [
            URLQueryItem(name: "ll", value: "\(latitude),\(longitude)")
        ]
        return components.url
    }
}

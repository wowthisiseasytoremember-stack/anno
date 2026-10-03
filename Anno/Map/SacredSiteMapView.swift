import MapKit
import SwiftUI

public enum MapExplorationMode: String, CaseIterable, Identifiable {
    case pilgrimages = "Pilgrimages"
    case sanctuaries = "Sanctuaries"
    case feastSites = "Feast Sites"

    // v1 intentionally exposes pilgrimage routes + feast sites only.
    // The legacy 72-sanctuary catalog is deferred with the reliquary work.
    public static var allCases: [MapExplorationMode] {
        [.pilgrimages, .feastSites]
    }

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
    private enum PilgrimageSegmentState {
        case future
        case next
        case completed
    }

    private struct PilgrimageMapSegment: Identifiable {
        let id: String
        let coordinates: [CLLocationCoordinate2D]
        let state: PilgrimageSegmentState
    }

    public let entries: [AnnoEntry]
    public let currentEntry: AnnoEntry?
    public let language: LanguageMode

    @StateObject private var geoLoader = SacredGeographyLoader.shared
    @StateObject private var exemplarContent = SoCalExemplarContentLoader.shared
    @StateObject private var progressStore = PilgrimageProgressStore.shared
    @StateObject private var locationService = PilgrimageLocationService.shared
    @AppStorage("anno.socalExemplarHeroSeen") private var hasSeenSoCalExemplarHero = false
    @State private var lastHapticArrivalChapterId: String?

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

    private var selectedRouteIsSoCalExemplar: Bool {
        guard let route = geoLoader.selectedRoute else { return false }
        return route.routeId == exemplarContent.content?.routeId
    }

    private func isSoCalExemplar(_ route: PilgrimageRoute) -> Bool {
        route.routeId == exemplarContent.content?.routeId
    }

    private func exemplarStation(
        route: PilgrimageRoute,
        waypoint: PilgrimageWaypoint
    ) -> SoCalExemplarContent.Station? {
        guard isSoCalExemplar(route) else { return nil }
        return exemplarContent.content?.station(id: waypoint.waypointId)
    }

    private func exemplarChapter(
        route: PilgrimageRoute,
        waypoint: PilgrimageWaypoint
    ) -> SoCalExemplarContent.Chapter? {
        guard isSoCalExemplar(route) else { return nil }
        return exemplarContent.content?.chapter(containing: waypoint.waypointId)
    }

    private func exemplarRequiredStationIds(
        route: PilgrimageRoute
    ) -> [String] {
        guard isSoCalExemplar(route) else {
            return route.waypoints.map(\.waypointId)
        }
        return exemplarContent.content?.coreRequiredStationIds ?? []
    }

    private func exemplarVisitedCount(route: PilgrimageRoute) -> Int {
        progressStore.visitedCount(
            routeId: route.routeId,
            requiredStationIds: exemplarRequiredStationIds(route: route)
        )
    }

    private func exemplarIsComplete(route: PilgrimageRoute) -> Bool {
        progressStore.hasVisitedAll(
            routeId: route.routeId,
            requiredStationIds: exemplarRequiredStationIds(route: route)
        )
    }

    private func isChapterComplete(
        route: PilgrimageRoute,
        chapter: SoCalExemplarContent.Chapter
    ) -> Bool {
        let stationIds = chapter.stations
            .filter { $0.stationRole != "optional_context" }
            .map(\.id)

        return progressStore.hasVisitedAll(
            routeId: route.routeId,
            requiredStationIds: stationIds
        )
    }

    private func soCalPilgrimageSegments(
        route: PilgrimageRoute
    ) -> [PilgrimageMapSegment] {
        guard isSoCalExemplar(route),
              let content = exemplarContent.content,
              let core = content.variants.first(where: { $0.id == "core" }) else {
            return []
        }

        let chapterNodes: [(chapter: SoCalExemplarContent.Chapter, waypoint: PilgrimageWaypoint)] =
            core.chapterIds.compactMap { chapterId in
                guard let chapter = content.chapters.first(where: {
                    $0.id == chapterId
                }) else {
                    return nil
                }

                guard let stationId = chapter.stations
                    .first(where: { $0.stationRole != "optional_context" })?
                    .id,
                      let waypoint = route.waypoints.first(where: {
                          $0.waypointId == stationId
                      }) else {
                    return nil
                }

                return (chapter, waypoint)
            }

        guard chapterNodes.count > 1 else {
            return []
        }

        return (0..<(chapterNodes.count - 1)).map { index in
            let source = chapterNodes[index]
            let destination = chapterNodes[index + 1]

            let state: PilgrimageSegmentState
            if isChapterComplete(route: route, chapter: destination.chapter) {
                state = .completed
            } else if isChapterComplete(route: route, chapter: source.chapter) {
                state = .next
            } else {
                state = .future
            }

            return PilgrimageMapSegment(
                id: "\(source.chapter.id)->\(destination.chapter.id)",
                coordinates: [
                    source.waypoint.coordinate,
                    destination.waypoint.coordinate
                ],
                state: state
            )
        }
    }

    public var body: some View {
        ZStack(alignment: .top) {
            mapLayer

            if !geoLoader.isLoading && mode == .pilgrimages && filteredRoutes.isEmpty {
                emptyPilgrimageState
                    .padding(.horizontal, AnnoTheme.lg)
                    .padding(.top, 180)
                    .transition(.opacity)
            }

            // Atmospheric gradient & Inquiry Controls
            VStack(spacing: 8) {
                atmosphereOverlay

                inquiryHeaderView

                modePickerBar
                    .padding(.horizontal, 16)

                if mode == .pilgrimages {
                    callingFilterCarousel
                    routeSelectionCarousel
                    arrivalMagicBar
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
        .sensoryFeedback(.selection, trigger: mode)
        .onAppear {
            if geoLoader.routes.isEmpty {
                geoLoader.loadData()
            }

            selectedWaypoint =
                geoLoader.selectedWaypoint
                ?? geoLoader.selectedRoute?.waypoints.first

            if selectedRouteIsSoCalExemplar && !hasSeenSoCalExemplarHero {
                selectedWaypoint = geoLoader.selectedRoute?.waypoints.first
                sheetExpanded = true
                hasSeenSoCalExemplarHero = true
            }

            updateCameraPosition()
        }
        .onDisappear {
            locationService.stop()
        }
        .onChange(of: mode) { _, _ in
            updateCameraPosition()
        }
        .onChange(of: geoLoader.selectedRoute) { _, route in
            if let route,
               geoLoader.selectedWaypoint?.waypointId != selectedWaypoint?.waypointId {
                selectedWaypoint = geoLoader.selectedWaypoint ?? route.waypoints.first
            }
            updateCameraPosition()
        }
        .onChange(of: geoLoader.selectedWaypoint) { _, waypoint in
            if let waypoint {
                selectedWaypoint = waypoint
                sheetExpanded = true
                updateCameraPosition()
            }
        }
        .onChange(of: locationService.latestLocation) { _, _ in
            handleLocationMomentIfNeeded()
        }
    }

    private var arrivalMagicBar: some View {
        Group {
            switch locationService.authorizationStatus {
            case .notDetermined:
                Button {
                    Haptics.light()
                    locationService.begin()
                } label: {
                    HStack(spacing: 8) {
                        Image(systemName: "location.fill")
                        Text(
                            language == .vietnamese
                                ? "Bật Phép Màu Khi Đến Nơi"
                                : "Enable Arrival Magic"
                        )
                        Spacer()
                        Image(systemName: "sparkles")
                    }
                    .font(Typography.captionSemibold)
                    .foregroundStyle(AnnoTheme.narthex)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 9)
                    .background(AnnoTheme.goldLeaf)
                    .clipShape(Capsule())
                }
                .buttonStyle(.plain)
                .padding(.horizontal, 16)

            case .authorizedWhenInUse, .authorizedAlways:
                if let nearby = locationService.nearestRelevantChapter() {
                    Button {
                        openNearbyChapter(nearby.chapter)
                    } label: {
                        HStack(spacing: 8) {
                            Image(
                                systemName: nearby.proximity == .arrived
                                    ? "mappin.and.ellipse"
                                    : "location.viewfinder"
                            )
                            .symbolRenderingMode(.hierarchical)
                            .foregroundStyle(
                                nearby.proximity == .arrived
                                    ? AnnoTheme.gilt
                                    : AnnoTheme.goldLeaf
                            )

                            VStack(alignment: .leading, spacing: 1) {
                                Text(
                                    nearby.proximity == .arrived
                                        ? (language == .vietnamese ? "BẠN ĐÃ ĐẾN" : "YOU'VE ARRIVED")
                                        : (language == .vietnamese ? "ĐANG ĐẾN GẦN" : "APPROACHING")
                                )
                                .font(Typography.caption2Bold)
                                .tracking(1.0)
                                .foregroundStyle(AnnoTheme.gilt)

                                Text(nearby.chapter.title(for: language))
                                    .font(Typography.captionSemiboldSerif)
                                    .foregroundStyle(AnnoTheme.vellum)
                                    .lineLimit(2)
                            }

                            Spacer()

                            Text(distanceLabel(nearby.distanceMeters))
                            .font(Typography.caption2MonospacedSemibold)
                            .foregroundStyle(AnnoTheme.incense)
                        }
                        .padding(.horizontal, 12)
                        .padding(.vertical, 9)
                        .background {
                            Capsule()
                                .fill(AnnoTheme.narthex.opacity(0.92))
                        }
                        .overlay {
                            Capsule()
                                .strokeBorder(
                                    nearby.proximity == .arrived
                                        ? AnnoTheme.gilt.opacity(0.85)
                                        : AnnoTheme.goldLeaf.opacity(0.45),
                                    lineWidth: nearby.proximity == .arrived ? 1.4 : 1
                                )
                        }
                    }
                    .buttonStyle(.plain)
                    .padding(.horizontal, 16)
                } else if locationService.isActive {
                    HStack(spacing: 8) {
                        Image(systemName: "location.fill")
                            .foregroundStyle(AnnoTheme.verdigris)
                        Text(
                            language == .vietnamese
                                ? "Phép màu khi đến nơi đang bật"
                                : "Arrival Magic is on"
                        )
                        .font(Typography.caption2Medium)
                        .foregroundStyle(AnnoTheme.incense)
                        Spacer()
                    }
                    .padding(.horizontal, 12)
                    .padding(.vertical, 7)
                    .background {
                        Capsule()
                            .fill(AnnoTheme.narthex.opacity(0.82))
                    }
                    .padding(.horizontal, 16)
                } else {
                    Button {
                        Haptics.light()
                        locationService.begin()
                    } label: {
                        HStack(spacing: 8) {
                            Image(systemName: "location.fill")
                            Text(
                                language == .vietnamese
                                    ? "Tiếp Tục Phép Màu Khi Đến Nơi"
                                    : "Resume Arrival Magic"
                            )
                            Spacer()
                            Image(systemName: "play.fill")
                        }
                        .font(Typography.captionSemibold)
                        .foregroundStyle(AnnoTheme.vellum)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 9)
                        .background {
                            Capsule()
                                .fill(AnnoTheme.narthex.opacity(0.92))
                        }
                        .overlay {
                            Capsule()
                                .strokeBorder(
                                    AnnoTheme.goldLeaf.opacity(0.45),
                                    lineWidth: 1
                                )
                        }
                    }
                    .buttonStyle(.plain)
                    .padding(.horizontal, 16)
                }

            case .denied, .restricted:
                HStack(spacing: 8) {
                    Image(systemName: "location.slash.fill")
                        .foregroundStyle(AnnoTheme.incense)
                    Text(
                        language == .vietnamese
                            ? "Vị trí đang tắt — nút “Tôi Đang Ở Đây” vẫn hoạt động"
                            : "Location is off — “I'm Here” still works"
                    )
                    .font(Typography.caption2Medium)
                    .foregroundStyle(AnnoTheme.incense)
                    Spacer()
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 7)
                .background {
                    Capsule()
                        .fill(AnnoTheme.narthex.opacity(0.82))
                }
                .padding(.horizontal, 16)

            @unknown default:
                EmptyView()
            }
        }
    }

    private func distanceLabel(_ meters: Double) -> String {
        if meters < 1_000 {
            return "\(Int(meters.rounded())) m"
        }

        return String(format: "%.1f km", meters / 1_000)
    }

    private func openNearbyChapter(_ chapter: PilgrimageChapterLocation) {
        guard let route = geoLoader.routes.first(where: {
            $0.routeId == "socal_vietnamese_catholic_pilgrimage_la_vang"
        }),
        let waypoint = route.waypoints.first(where: {
            $0.waypointId == chapter.representativeWaypointId
        }) else {
            return
        }

        geoLoader.selectedRoute = route
        geoLoader.selectedWaypoint = waypoint
        selectedWaypoint = waypoint
        sheetExpanded = true
        Haptics.sacredArrival(.feast)
        updateCameraPosition()
    }

    private func handleLocationMomentIfNeeded() {
        guard let nearby = locationService.nearestRelevantChapter(),
              nearby.proximity == .arrived else {
            return
        }

        guard lastHapticArrivalChapterId != nearby.chapter.id else {
            return
        }

        lastHapticArrivalChapterId = nearby.chapter.id
        Haptics.sacredArrival(.solemnity)
    }

    private var emptyPilgrimageState: some View {
        AnnoStateView(
            symbol: AnnoSymbol.pilgrimage,
            title: language == .vietnamese
                ? "Không có tuyến đường phù hợp"
                : "No pilgrimage routes match",
            message: language == .vietnamese
                ? "Hãy xóa bộ lọc để xem lại năm tuyến hành hương chủ lực."
                : "Clear the filters to return to Anno's five flagship pilgrimage routes.",
            tint: AnnoTheme.goldLeaf,
            actionTitle: language == .vietnamese ? "Hiển thị tất cả" : "Show all"
        ) {
            withAnimation(AnnoMotion.selection) {
                selectedCalling = .all
                selectedRegion = .all
                geoLoader.selectedRoute = geoLoader.routes.first
                selectedWaypoint = geoLoader.routes.first?.waypoints.first
            }
        }
    }

    // MARK: - Spiritual Inquiry Header

    private var inquiryHeaderView: some View {
        VStack(spacing: 4) {
            Text(language == .vietnamese
                 ? "Hôm nay bạn muốn bước theo con đường của ai?"
                 : "Whose path will you walk today?")
                .font(Typography.subheadlineSemibold)
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
                        .font(Typography.iconCaption)
                        .foregroundStyle(AnnoTheme.candleGlow)
                    Text(language == .vietnamese
                         ? "Gắn liền với lễ: \(today.liturgical.titleVi)"
                         : "In season with: \(today.liturgical.titleEn)")
                        .font(Typography.caption2)
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
            UserAnnotation()

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
                    if isSoCalExemplar(route) {
                        ForEach(soCalPilgrimageSegments(route: route)) { segment in
                            switch segment.state {
                            case .completed:
                                MapPolyline(coordinates: segment.coordinates)
                                    .stroke(
                                        LinearGradient(
                                            colors: [
                                                AnnoTheme.gilt,
                                                AnnoTheme.goldLeaf,
                                                AnnoTheme.candleGlow
                                            ],
                                            startPoint: .leading,
                                            endPoint: .trailing
                                        ),
                                        style: StrokeStyle(
                                            lineWidth: 5.5,
                                            lineCap: .round,
                                            lineJoin: .round
                                        )
                                    )

                            case .next:
                                MapPolyline(coordinates: segment.coordinates)
                                    .stroke(
                                        AnnoTheme.candleGlow.opacity(0.90),
                                        style: StrokeStyle(
                                            lineWidth: 4.5,
                                            lineCap: .round,
                                            lineJoin: .round,
                                            dash: [10, 7]
                                        )
                                    )

                            case .future:
                                MapPolyline(coordinates: segment.coordinates)
                                    .stroke(
                                        AnnoTheme.incense.opacity(0.28),
                                        style: StrokeStyle(
                                            lineWidth: 3,
                                            lineCap: .round,
                                            lineJoin: .round
                                        )
                                    )
                            }
                        }
                    } else {
                        MapPolyline(coordinates: route.coordinates)
                            .stroke(
                                LinearGradient(
                                    colors: [
                                        AnnoTheme.gilt,
                                        AnnoTheme.goldLeaf,
                                        AnnoTheme.candleGlow
                                    ],
                                    startPoint: .leading,
                                    endPoint: .trailing
                                ),
                                style: StrokeStyle(
                                    lineWidth: 4.5,
                                    lineCap: .round,
                                    lineJoin: .round
                                )
                            )
                    }

                    // Numbered Waypoints with Halo
                    ForEach(route.waypoints) { wp in
                        Annotation(
                            wp.name(for: language),
                            coordinate: wp.coordinate,
                            anchor: .bottom
                        ) {
                            Button {
                                let moment = PilgrimageMomentRegistry.shared.moment(
                                    routeId: route.routeId,
                                    waypointId: wp.waypointId
                                )
                                Haptics.sacredArrival(
                                    moment?.level.sacredIntensity ?? .ordinary
                                )

                                withAnimation(
                                    moment?.level == .climax
                                        ? AnnoMotion.immersive
                                        : AnnoMotion.selection
                                ) {
                                    selectedWaypoint = wp
                                    sheetExpanded = true
                                }
                            } label: {
                                waypointPinView(
                                    route: route,
                                    waypoint: wp,
                                    isSelected: (selectedWaypoint ?? route.waypoints.first)?.id == wp.id
                                )
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
                            withAnimation(AnnoMotion.selection) {
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
                    withAnimation(AnnoMotion.selection) {
                        mode = m
                        sheetExpanded = false
                    }
                } label: {
                    Text(m.title(for: language))
                        .font(Typography.captionSemiboldSerif)
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
                        withAnimation(AnnoMotion.selection) {
                            selectedCalling = calling
                            if let firstMatch = filteredRoutes.first {
                                geoLoader.selectedRoute = firstMatch
                                selectedWaypoint = firstMatch.waypoints.first
                            }
                        }
                    } label: {
                        HStack(spacing: 4) {
                            Image(systemName: AnnoSymbol.spiritualCalling(calling))
                                .font(Typography.iconCaption)
                            Text(calling.title(for: language))
                                .font(Typography.caption2Medium)
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
                        withAnimation(AnnoMotion.selection) {
                            geoLoader.selectedRoute = route
                            selectedWaypoint = route.waypoints.first
                            if isSoCalExemplar(route) {
                                sheetExpanded = true
                            }
                        }
                    } label: {
                        HStack(spacing: 6) {
                            if isConnected {
                                Image(systemName: "sparkles")
                                    .font(Typography.caption2)
                                    .foregroundStyle(AnnoTheme.goldLeaf)
                                    .symbolEffect(.appear, value: isConnected)
                            } else {
                                Image(systemName: "figure.walk")
                                    .font(Typography.caption2)
                                    .foregroundStyle(isSelected ? AnnoTheme.goldLeaf : AnnoTheme.incense)
                            }

                            Text(route.title(for: language))
                                .font(Typography.captionSemiboldSerif)
                                .foregroundStyle(isSelected ? AnnoTheme.vellum : AnnoTheme.incense)
                                .lineLimit(2)

                            Text("(\(route.waypoints.count))")
                                .font(Typography.caption2MonospacedSemibold)
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
                        .font(Typography.caption2Medium)
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
                            .font(Typography.caption2Medium)
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

    private func waypointPinView(
        route: PilgrimageRoute,
        waypoint: PilgrimageWaypoint,
        isSelected: Bool
    ) -> some View {
        let moment = PilgrimageMomentRegistry.shared.moment(
            routeId: route.routeId,
            waypointId: waypoint.waypointId
        )
        let intensity = moment?.level.sacredIntensity ?? (isSelected ? .feast : .ordinary)
        let baseSize: CGFloat = {
            switch moment?.level {
            case .climax: return isSelected ? 40 : 34
            case .highlight: return isSelected ? 36 : 30
            case nil: return isSelected ? 32 : 26
            }
        }()

        return VStack(spacing: 0) {
            ZStack {
                if intensity > .ordinary {
                    SacredAureole(
                        tint: AnnoTheme.goldLeaf,
                        intensity: intensity,
                        diameter: moment?.level == .climax ? 58 : 48
                    )
                }

                Circle()
                    .fill(isSelected ? AnnoTheme.goldLeaf : AnnoTheme.narthex)
                    .frame(width: baseSize, height: baseSize)
                    .overlay(
                        Circle()
                            .stroke(
                                moment?.level == .climax
                                    ? AnnoTheme.gilt
                                    : AnnoTheme.goldLeaf,
                                lineWidth: moment?.level == .climax ? 2.2 : 1.5
                            )
                    )
                    .shadow(
                        color: moment != nil
                            ? AnnoTheme.gilt.opacity(isSelected ? 0.52 : 0.28)
                            : .black.opacity(0.6),
                        radius: moment != nil ? (isSelected ? 10 : 6) : 4,
                        y: 2
                    )

                Text("\(waypoint.order)")
                    .font(Typography.captionBoldSerif)
                    .foregroundStyle(isSelected ? AnnoTheme.narthex : AnnoTheme.goldLeaf)

                if progressStore.isVisited(
                    routeId: route.routeId,
                    waypointId: waypoint.waypointId
                ) {
                    Image(systemName: "checkmark.seal.fill")
                        .font(Typography.iconSmall)
                        .foregroundStyle(AnnoTheme.verdigris)
                        .background(Circle().fill(AnnoTheme.narthex))
                        .offset(x: baseSize * 0.43, y: baseSize * 0.40)
                }

                if let moment {
                    Image(systemName: moment.level == .climax ? "sparkles" : AnnoSymbol.sacred)
                        .font(Typography.iconTiny)
                        .foregroundStyle(
                            moment.level == .climax
                                ? AnnoTheme.gilt
                                : AnnoTheme.goldLeaf
                        )
                        .offset(x: baseSize * 0.45, y: -baseSize * 0.40)
                        .symbolEffect(.appear, value: isSelected)
                }
            }

            Image(systemName: "triangle.fill")
                .font(Typography.iconTiny)
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
                    .font(Typography.iconCaption2)
                    .foregroundStyle(isSelected ? AnnoTheme.narthex : AnnoTheme.goldLeaf)
            }

            Image(systemName: "triangle.fill")
                .font(Typography.iconTiny)
                .foregroundStyle(AnnoTheme.goldLeaf)
                .rotationEffect(.degrees(180))
                .offset(y: -2)
        }
    }

    private func sacredPinView(confidence: ConfidenceLevel, placeName: String) -> some View {
        VStack(spacing: 0) {
            ZStack {
                Image(systemName: "mappin.circle.fill")
                    .font(Typography.iconSacredPin)
                    .foregroundStyle(AnnoTheme.goldLeaf)
                    .shadow(color: .black.opacity(0.5), radius: 4, y: 2)

                Circle()
                    .fill(AnnoTheme.confidenceColor(confidence))
                    .frame(width: 10, height: 10)
                    .offset(y: -1)
            }

            Image(systemName: "triangle.fill")
                .font(Typography.iconSmall)
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
                withAnimation(AnnoMotion.selection) {
                    sheetExpanded.toggle()
                }
            } label: {
                HStack(spacing: 8) {
                    Image(systemName: mode == .pilgrimages ? "map.circle.fill" : "mappin.and.ellipse")
                        .foregroundStyle(AnnoTheme.goldLeaf)

                    Text(sheetTitle)
                        .font(Typography.subheadlineSemibold)
                        .foregroundStyle(AnnoTheme.vellum)
                        .lineLimit(2)
                        .fixedSize(horizontal: false, vertical: true)

                    Spacer()

                    Image(systemName: sheetExpanded ? "chevron.down" : "chevron.up")
                        .font(Typography.captionBoldSerif)
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
            if isSoCalExemplar(route),
               let content = exemplarContent.content {
                SoCalPilgrimageHero(
                    content: content,
                    language: language,
                    visitedCount: exemplarVisitedCount(route: route),
                    totalCount: exemplarRequiredStationIds(route: route).count
                )
            }

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
                    .font(Typography.caption2Bold)
                    .foregroundStyle(AnnoTheme.narthex)
                    .padding(.horizontal, 6)
                    .padding(.vertical, 2)
                    .background(Capsule().fill(AnnoTheme.goldLeaf))
                }
            }
            .font(Typography.caption2)
            .foregroundStyle(AnnoTheme.goldLeaf)

            Text(route.spiritualTheme(for: language))
                .font(Typography.bodySerif.italic())
                
                .foregroundStyle(AnnoTheme.vellum)

            Divider().background(AnnoTheme.ash)

            // Selected Waypoint Focus
            let currentWp = selectedWaypoint ?? route.waypoints.first
            if let wp = currentWp {
                let moment = PilgrimageMomentRegistry.shared.moment(
                    routeId: route.routeId,
                    waypointId: wp.waypointId
                )

                VStack(alignment: .leading, spacing: 10) {
                    if let moment {
                        SacredMomentBanner(
                            title: moment.level == .climax
                                ? (language == .vietnamese
                                    ? "Khoảnh Khắc Hành Hương Lớn"
                                    : "Major Pilgrimage Moment")
                                : (language == .vietnamese
                                    ? "Điểm Nhấn Hành Hương"
                                    : "Pilgrimage Highlight"),
                            subtitle: moment.label(for: language),
                            symbol: moment.level == .climax
                                ? "sparkles"
                                : AnnoSymbol.sacred,
                            intensity: moment.level.sacredIntensity,
                            tint: AnnoTheme.goldLeaf
                        )
                    }

                    if let chapter = exemplarChapter(route: route, waypoint: wp) {
                        SoCalChapterHeader(chapter: chapter, language: language)
                    }

                    if let station = exemplarStation(route: route, waypoint: wp) {
                        SoCalStationRitualView(
                            station: station,
                            language: language
                        )

                        PilgrimageVisitButton(
                            isVisited: progressStore.isVisited(
                                routeId: route.routeId,
                                waypointId: wp.waypointId
                            ),
                            language: language
                        ) {
                            progressStore.markVisited(route: route, waypoint: wp)

                            if exemplarIsComplete(route: route) {
                                progressStore.markCompleted(routeId: route.routeId)
                                Haptics.pilgrimageComplete()
                            } else if let station = exemplarStation(route: route, waypoint: wp) {
                                Haptics.sacredArrival(
                                    station.momentLevel == "climax"
                                        ? .solemnity
                                        : (station.momentLevel == "highlight" ? .feast : .ordinary)
                                )
                            } else {
                                Haptics.medium()
                            }
                        }
                    }

                    HStack(alignment: .top) {
                        VStack(alignment: .leading, spacing: 2) {
                            Text("Station \(wp.order): \(wp.name(for: language))")
                                .font(Typography.headlineSerif)
                                .foregroundStyle(AnnoTheme.goldLeaf)
                        }

                        Spacer()

                        HStack(spacing: 8) {
                            if let mapsUrl = appleMapsUrl(latitude: wp.latitude, longitude: wp.longitude) {
                                Link(destination: mapsUrl) {
                                    Image(systemName: "arrow.triangle.turn.up.right.diamond.fill")
                                        .font(Typography.captionSerif)
                                        .foregroundStyle(AnnoTheme.goldLeaf)
                                        .padding(7)
                                        .background(Circle().fill(AnnoTheme.goldLeaf.opacity(0.15)))
                                }
                            }

                            if let stationLink = AnnoDeepLink.pilgrimage(
                                route: route,
                                waypoint: wp
                            ) {
                                ShareLink(
                                    item: stationLink,
                                    subject: Text(route.title(for: language)),
                                    message: Text(
                                        language == .vietnamese
                                            ? "Mở điểm hành hương này trong Anno."
                                            : "Open this pilgrimage station in Anno."
                                    )
                                ) {
                                    Image(systemName: "square.and.arrow.up")
                                        .font(Typography.captionSerif)
                                        .foregroundStyle(AnnoTheme.goldLeaf)
                                        .padding(7)
                                        .background(
                                            Circle()
                                                .fill(AnnoTheme.goldLeaf.opacity(0.15))
                                        )
                                }
                            }
                        }
                    }

                    if exemplarStation(route: route, waypoint: wp) == nil {
                        Text(wp.historicalSummary(for: language))
                            .font(Typography.captionSerif)
                            .lineSpacing(3)
                            .foregroundStyle(AnnoTheme.vellum.opacity(0.92))
                    }

                    if exemplarStation(route: route, waypoint: wp) == nil,
                       !wp.sacredRelic(for: language).isEmpty {
                        HStack(alignment: .top, spacing: 8) {
                            Image(systemName: "sparkles")
                                .font(Typography.caption2)
                                .foregroundStyle(AnnoTheme.goldLeaf)
                            VStack(alignment: .leading, spacing: 2) {
                                Text(language == .vietnamese ? "Thánh Tích & Di Sản" : "Sacred Relics")
                                    .font(Typography.caption2Bold)
                                    .foregroundStyle(AnnoTheme.goldLeaf)
                                Text(wp.sacredRelic(for: language))
                                    .font(Typography.caption2)
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

                    if exemplarStation(route: route, waypoint: wp) == nil,
                       !wp.suggestedPrayer(for: language).isEmpty {
                        VStack(alignment: .leading, spacing: 4) {
                            Text(language == .vietnamese ? "Lời Nguyện Hành Hương" : "Pilgrim's Prayer")
                                .font(Typography.caption2Bold)
                                .foregroundStyle(AnnoTheme.goldLeaf)

                            Text(wp.suggestedPrayer(for: language))
                                .font(Typography.captionItalic)
                                
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
                                .font(Typography.caption2Medium)
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
                                .font(Typography.caption2Medium)
                                .foregroundStyle(AnnoTheme.goldLeaf)
                            }
                        }
                    }
                    .padding(.top, 4)
                }
            }

            if isSoCalExemplar(route),
               exemplarIsComplete(route: route),
               let content = exemplarContent.content {
                PilgrimageCompletionKeepsake(
                    content: content,
                    routeId: route.routeId,
                    language: language,
                    completionDate: progressStore.completionDate(routeId: route.routeId)
                )
                .transition(.scale.combined(with: .opacity))
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
                            HStack(spacing: 4) {
                                if progressStore.isVisited(
                                    routeId: route.routeId,
                                    waypointId: wp.waypointId
                                ) {
                                    Image(systemName: "checkmark")
                                        .font(Typography.iconTiny)
                                }

                                Text("\(wp.order). \(wp.name(for: language))")
                            }
                            .font(Typography.caption2)
                            .foregroundStyle(isSel ? AnnoTheme.narthex : AnnoTheme.vellum)
                            .padding(.horizontal, 10)
                            .padding(.vertical, 5)
                            .background(
                                Capsule().fill(
                                    isSel
                                        ? AnnoTheme.goldLeaf
                                        : (progressStore.isVisited(
                                            routeId: route.routeId,
                                            waypointId: wp.waypointId
                                        )
                                            ? AnnoTheme.verdigris.opacity(0.55)
                                            : AnnoTheme.ash)
                                )
                            )
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
                        .font(Typography.headlineSerif)
                        .foregroundStyle(AnnoTheme.goldLeaf)

                    Text("\(sanctuary.location.city), \(sanctuary.location.country)")
                        .font(Typography.caption2)
                        .foregroundStyle(AnnoTheme.incense)
                }

                Spacer()

                if let mapsUrl = appleMapsUrl(latitude: sanctuary.location.latitude, longitude: sanctuary.location.longitude) {
                    Link(destination: mapsUrl) {
                        Image(systemName: "arrow.triangle.turn.up.right.diamond.fill")
                            .font(Typography.captionSerif)
                            .foregroundStyle(AnnoTheme.goldLeaf)
                            .padding(6)
                            .background(Circle().fill(AnnoTheme.goldLeaf.opacity(0.15)))
                    }
                }
            }

            Text(sanctuary.historicalSummary(for: language))
                .font(Typography.captionSerif)
                .lineSpacing(3)
                .foregroundStyle(AnnoTheme.vellum)

            if !sanctuary.suggestedPrayer(for: language).isEmpty {
                VStack(alignment: .leading, spacing: 4) {
                    Text(language == .vietnamese ? "Lời Nguyện Thánh Địa" : "Sanctuary Prayer")
                        .font(Typography.caption2Bold)
                        .foregroundStyle(AnnoTheme.goldLeaf)

                    Text(sanctuary.suggestedPrayer(for: language))
                        .font(Typography.captionItalic)
                        
                        .foregroundStyle(AnnoTheme.vellum)
                }
                .padding(12)
                .background(RoundedRectangle(cornerRadius: 10).fill(AnnoTheme.narthex).overlay(RoundedRectangle(cornerRadius: 10).stroke(AnnoTheme.goldLeaf.opacity(0.35), lineWidth: 1)))
            }

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
                                .font(Typography.captionSemiboldSerif)
                                
                                .foregroundStyle(AnnoTheme.vellum)
                            Text("\(s.location.city), \(s.location.country)")
                                .font(Typography.caption2)
                                .foregroundStyle(AnnoTheme.incense)
                        }
                        Spacer()
                        Image(systemName: "chevron.right")
                            .font(Typography.caption2)
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

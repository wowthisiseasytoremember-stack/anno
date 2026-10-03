import Combine
import Foundation

@MainActor
public final class SacredGeographyLoader: ObservableObject {
    public static let shared = SacredGeographyLoader()

    @Published public var routes: [PilgrimageRoute] = []
    @Published public var sanctuaries: [Sanctuary] = []
    @Published public var selectedRoute: PilgrimageRoute?
    @Published public var selectedWaypoint: PilgrimageWaypoint?
    @Published public var selectedSanctuary: Sanctuary?
    @Published public var selectedCategory: String? = nil
    @Published public var isLoading: Bool = false
    @Published public var errorMessage: String? = nil

    private struct FlagshipRoutesManifest: Decodable {
        let flagshipRoutes: [FlagshipRouteReference]

        enum CodingKeys: String, CodingKey {
            case flagshipRoutes = "flagship_routes"
        }
    }

    private struct FlagshipRouteReference: Decodable {
        let routeId: String
        let file: String

        enum CodingKeys: String, CodingKey {
            case routeId = "route_id"
            case file
        }
    }

    private static let fallbackFlagships: [FlagshipRouteReference] = [
        .init(routeId: "socal_vietnamese_catholic_pilgrimage_la_vang", file: "socal_vietnamese_catholic_pilgrimage_la_vang.json"),
        .init(routeId: "holy_land_passion", file: "holy_land_passion.json"),
        .init(routeId: "rome_seven_churches", file: "rome_seven_churches.json"),
        .init(routeId: "camino_de_santiago", file: "camino_de_santiago.json"),
        .init(routeId: "basilica_of_our_lady_of_guadalupe", file: "basilica_of_our_lady_of_guadalupe.json")
    ]

    public init() {
        loadData()
    }

    public func loadData() {
        isLoading = true
        errorMessage = nil

        let manifest = loadManifest()
        let references = manifest?.flagshipRoutes ?? Self.fallbackFlagships

        var loadedRoutes: [PilgrimageRoute] = []
        var missingRouteIds: [String] = []

        for reference in references {
            guard let route = loadRoute(reference) else {
                missingRouteIds.append(reference.routeId)
                continue
            }
            loadedRoutes.append(route)
        }

        // v1 intentionally exposes only the five flagship pilgrimage routes.
        // Legacy sanctuary/reliquary geography remains archived for possible v2 use.
        routes = loadedRoutes
        sanctuaries = []

        if let selectedRoute, loadedRoutes.contains(where: { $0.routeId == selectedRoute.routeId }) {
            self.selectedRoute = selectedRoute
        } else {
            self.selectedRoute = loadedRoutes.first
        }

        if !missingRouteIds.isEmpty {
            errorMessage = "Missing v1 pilgrimage routes: \(missingRouteIds.joined(separator: ", "))"
        } else if manifest == nil {
            errorMessage = "flagship_routes_v1.json was unavailable; loaded the built-in v1 route list."
        }

        isLoading = false
    }

    private func loadManifest() -> FlagshipRoutesManifest? {
        if let bundledURL = Bundle.main.url(forResource: "flagship_routes_v1", withExtension: "json"),
           let data = try? Data(contentsOf: bundledURL),
           let manifest = try? JSONDecoder().decode(FlagshipRoutesManifest.self, from: data) {
            return manifest
        }

        for relativePath in [
            "Anno/Resources/flagship_routes_v1.json",
            "Resources/flagship_routes_v1.json"
        ] {
            let path = (FileManager.default.currentDirectoryPath as NSString).appendingPathComponent(relativePath)
            if let data = try? Data(contentsOf: URL(fileURLWithPath: path)),
               let manifest = try? JSONDecoder().decode(FlagshipRoutesManifest.self, from: data) {
                return manifest
            }
        }

        return nil
    }

    private func loadRoute(_ reference: FlagshipRouteReference) -> PilgrimageRoute? {
        let fileURL = URL(fileURLWithPath: reference.file)
        let resourceName = fileURL.deletingPathExtension().lastPathComponent
        let fileExtension = fileURL.pathExtension.isEmpty ? "json" : fileURL.pathExtension

        let bundleCandidates: [URL?] = [
            Bundle.main.url(forResource: resourceName, withExtension: fileExtension, subdirectory: "PilgrimageRoutes"),
            Bundle.main.url(forResource: resourceName, withExtension: fileExtension)
        ]

        for candidate in bundleCandidates.compactMap({ $0 }) {
            if let route = decodeRoute(at: candidate, expectedRouteId: reference.routeId) {
                return route
            }
        }

        for relativePath in [
            "Anno/Resources/PilgrimageRoutes/\(reference.file)",
            "Resources/PilgrimageRoutes/\(reference.file)"
        ] {
            let path = (FileManager.default.currentDirectoryPath as NSString).appendingPathComponent(relativePath)
            let candidate = URL(fileURLWithPath: path)
            if FileManager.default.fileExists(atPath: candidate.path),
               let route = decodeRoute(at: candidate, expectedRouteId: reference.routeId) {
                return route
            }
        }

        return nil
    }

    private func decodeRoute(at url: URL, expectedRouteId: String) -> PilgrimageRoute? {
        guard let data = try? Data(contentsOf: url),
              let route = try? JSONDecoder().decode(PilgrimageRoute.self, from: data),
              route.routeId == expectedRouteId else {
            return nil
        }
        return route
    }

    public var availableCategories: [String] {
        []
    }

    public func filteredSanctuaries(category: String?) -> [Sanctuary] {
        []
    }
}

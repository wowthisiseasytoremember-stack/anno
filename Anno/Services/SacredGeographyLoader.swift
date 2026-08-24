import Foundation
import Combine
import CoreLocation

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

    public init() {
        loadData()
    }

    public func loadData() {
        isLoading = true
        errorMessage = nil

        // Try loading compiled master catalog first
        if let url = Bundle.main.url(forResource: "sacred_geography_master", withExtension: "json") {
            do {
                let data = try Data(contentsOf: url)
                let master = try JSONDecoder().decode(SacredGeographyMaster.self, from: data)
                self.routes = master.pilgrimageRoutes
                self.sanctuaries = master.sanctuaries
                if self.selectedRoute == nil, let first = self.routes.first {
                    self.selectedRoute = first
                }
                self.isLoading = false
                return
            } catch {
                print("Failed to decode sacred_geography_master.json from bundle: \(error)")
            }
        }

        // Fallback: search common project asset paths
        let candidatePaths = [
            "Anno/Resources/sacred_geography_master.json",
            "Resources/sacred_geography_master.json"
        ]

        for relPath in candidatePaths {
            let fullPath = (FileManager.default.currentDirectoryPath as NSString).appendingPathComponent(relPath)
            if FileManager.default.fileExists(atPath: fullPath),
               let data = try? Data(contentsOf: URL(fileURLWithPath: fullPath)),
               let master = try? JSONDecoder().decode(SacredGeographyMaster.self, from: data) {
                self.routes = master.pilgrimageRoutes
                self.sanctuaries = master.sanctuaries
                if self.selectedRoute == nil, let first = self.routes.first {
                    self.selectedRoute = first
                }
                self.isLoading = false
                return
            }
        }

        self.isLoading = false
    }

    public var availableCategories: [String] {
        Array(Set(sanctuaries.map(\.category))).sorted()
    }

    public func filteredSanctuaries(category: String?) -> [Sanctuary] {
        guard let cat = category, !cat.isEmpty, cat != "all" else {
            return sanctuaries
        }
        return sanctuaries.filter { $0.category == cat }
    }
}

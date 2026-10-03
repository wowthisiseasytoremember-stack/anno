import Combine
import Foundation

@MainActor
final class PilgrimageSessionStore: ObservableObject {
    static let shared = PilgrimageSessionStore()

    @Published private(set) var activeRouteId: String?
    @Published private(set) var currentStationId: String?
    @Published private(set) var startedAt: Date?

    private let defaults: UserDefaults

    init(defaults: UserDefaults = .standard) {
        self.defaults = defaults
        activeRouteId = defaults.string(forKey: Keys.activeRouteId)
        currentStationId = defaults.string(forKey: Keys.currentStationId)
        startedAt = defaults.object(forKey: Keys.startedAt) as? Date
    }

    func isActive(routeId: String) -> Bool {
        activeRouteId == routeId
    }

    func begin(routeId: String, stationId: String?) {
        activeRouteId = routeId
        currentStationId = stationId
        startedAt = Date()
        persist()
    }

    func updateCurrentStation(routeId: String, stationId: String) {
        guard activeRouteId == routeId else { return }
        currentStationId = stationId
        persist()
    }

    func end(routeId: String) {
        guard activeRouteId == routeId else { return }
        clear()
    }

    func complete(routeId: String) {
        guard activeRouteId == routeId else { return }
        clear()
    }

    private func clear() {
        activeRouteId = nil
        currentStationId = nil
        startedAt = nil

        defaults.removeObject(forKey: Keys.activeRouteId)
        defaults.removeObject(forKey: Keys.currentStationId)
        defaults.removeObject(forKey: Keys.startedAt)
    }

    private func persist() {
        defaults.set(activeRouteId, forKey: Keys.activeRouteId)
        defaults.set(currentStationId, forKey: Keys.currentStationId)
        defaults.set(startedAt, forKey: Keys.startedAt)
    }

    private enum Keys {
        static let activeRouteId = "anno.pilgrimage.session.activeRouteId"
        static let currentStationId = "anno.pilgrimage.session.currentStationId"
        static let startedAt = "anno.pilgrimage.session.startedAt"
    }
}

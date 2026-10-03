import CoreLocation
import Foundation

struct PilgrimageChapterLocation: Identifiable, Hashable, Sendable {
    let id: String
    let titleEn: String
    let titleVi: String
    let representativeWaypointId: String
    let latitude: Double
    let longitude: Double
    let approachRadiusMeters: Double
    let arrivalRadiusMeters: Double

    var location: CLLocation {
        CLLocation(latitude: latitude, longitude: longitude)
    }

    func title(for language: LanguageMode) -> String {
        language == .vietnamese ? titleVi : titleEn
    }
}

@MainActor
final class PilgrimageLocationService: NSObject, ObservableObject, CLLocationManagerDelegate {
    static let shared = PilgrimageLocationService()

    @Published private(set) var authorizationStatus: CLAuthorizationStatus
    @Published private(set) var latestLocation: CLLocation?
    @Published private(set) var isActive = false

    private let manager = CLLocationManager()

    static let soCalChapters: [PilgrimageChapterLocation] = [
        .init(
            id: "christ_cathedral_la_vang",
            titleEn: "Christ Cathedral / Our Lady of La Vang",
            titleVi: "Christ Cathedral / Đức Mẹ La Vang",
            representativeWaypointId: "our_lady_la_vang_shrine_christ_cathedral",
            latitude: 33.7870499,
            longitude: -117.8991339,
            approachRadiusMeters: 350,
            arrivalRadiusMeters: 120
        ),
        .init(
            id: "st_columban",
            titleEn: "Saint Columban Catholic Church",
            titleVi: "Giáo Xứ Thánh Columban",
            representativeWaypointId: "st_columban_church_garden_grove",
            latitude: 33.77812,
            longitude: -117.94418,
            approachRadiusMeters: 300,
            arrivalRadiusMeters: 100
        ),
        .init(
            id: "vietnamese_catholic_center",
            titleEn: "Vietnamese Catholic Center",
            titleVi: "Trung Tâm Công Giáo Việt Nam",
            representativeWaypointId: "vietnamese_catholic_center_santa_ana",
            latitude: 33.7589895,
            longitude: -117.9216506,
            approachRadiusMeters: 300,
            arrivalRadiusMeters: 100
        ),
        .init(
            id: "our_lady_of_la_vang_parish",
            titleEn: "Our Lady of La Vang Catholic Church",
            titleVi: "Giáo Xứ Đức Mẹ La Vang",
            representativeWaypointId: "our_lady_of_la_vang_church_santa_ana",
            latitude: 33.7428866,
            longitude: -117.9208725,
            approachRadiusMeters: 300,
            arrivalRadiusMeters: 100
        ),
        .init(
            id: "st_barbara",
            titleEn: "Saint Barbara Catholic Church",
            titleVi: "Giáo Xứ Thánh Barbara",
            representativeWaypointId: "st_barbara_parish_westminster",
            latitude: 33.737313,
            longitude: -117.937589,
            approachRadiusMeters: 300,
            arrivalRadiusMeters: 100
        )
    ]

    override private init() {
        authorizationStatus = manager.authorizationStatus
        super.init()

        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyNearestTenMeters
        manager.distanceFilter = 10
        manager.activityType = .other
        manager.pausesLocationUpdatesAutomatically = true
    }

    func begin() {
        switch authorizationStatus {
        case .notDetermined:
            manager.requestWhenInUseAuthorization()

        case .authorizedWhenInUse, .authorizedAlways:
            isActive = true
            manager.startUpdatingLocation()

        case .denied, .restricted:
            isActive = false

        @unknown default:
            isActive = false
        }
    }

    func stop() {
        manager.stopUpdatingLocation()
        isActive = false
    }

    func proximity(
        to chapter: PilgrimageChapterLocation
    ) -> (kind: Proximity, distanceMeters: Double)? {
        guard let latestLocation else { return nil }

        let distance = latestLocation.distance(from: chapter.location)

        if distance <= chapter.arrivalRadiusMeters {
            return (.arrived, distance)
        }

        if distance <= chapter.approachRadiusMeters {
            return (.approaching, distance)
        }

        return (.far, distance)
    }

    func nearestRelevantChapter() -> (
        chapter: PilgrimageChapterLocation,
        proximity: Proximity,
        distanceMeters: Double
    )? {
        Self.soCalChapters.compactMap { chapter in
            guard let result = proximity(to: chapter),
                  result.kind != .far else {
                return nil
            }

            return (
                chapter: chapter,
                proximity: result.kind,
                distanceMeters: result.distanceMeters
            )
        }
        .min { lhs, rhs in
            lhs.distanceMeters < rhs.distanceMeters
        }
    }

    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        authorizationStatus = manager.authorizationStatus

        if authorizationStatus == .authorizedWhenInUse
            || authorizationStatus == .authorizedAlways {
            isActive = true
            manager.startUpdatingLocation()
        } else if authorizationStatus == .denied
                    || authorizationStatus == .restricted {
            isActive = false
            manager.stopUpdatingLocation()
        }
    }

    func locationManager(
        _ manager: CLLocationManager,
        didUpdateLocations locations: [CLLocation]
    ) {
        guard let location = locations.last,
              location.horizontalAccuracy >= 0 else {
            return
        }

        latestLocation = location
    }

    enum Proximity: String, Sendable {
        case far
        case approaching
        case arrived
    }
}

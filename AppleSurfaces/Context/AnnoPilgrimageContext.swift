import CoreLocation
import CoreMotion
import Foundation

struct AnnoPilgrimageStationContext: Hashable, Sendable {
    let stationId: String
    let title: String
    let latitude: Double
    let longitude: Double
    let approachRadiusMeters: Double
    let arrivalRadiusMeters: Double

    var location: CLLocation {
        CLLocation(latitude: latitude, longitude: longitude)
    }
}

enum AnnoPilgrimageProximity: String, Sendable {
    case far
    case approaching
    case arrived
}

struct AnnoPilgrimageContextSnapshot: Sendable {
    let stationId: String?
    let proximity: AnnoPilgrimageProximity
    let distanceMeters: Double?
    let isStationary: Bool
    let localHour: Int

    var timeOfDay: TimeOfDay {
        switch localHour {
        case 5..<8:
            return .dawn
        case 8..<17:
            return .day
        case 17..<21:
            return .evening
        default:
            return .night
        }
    }

    enum TimeOfDay: String, Sendable {
        case dawn
        case day
        case evening
        case night
    }
}

enum AnnoPilgrimageContextEvaluator {
    static func proximity(
        userLocation: CLLocation,
        station: AnnoPilgrimageStationContext
    ) -> (AnnoPilgrimageProximity, Double) {
        let distance = userLocation.distance(from: station.location)

        if distance <= station.arrivalRadiusMeters {
            return (.arrived, distance)
        }

        if distance <= station.approachRadiusMeters {
            return (.approaching, distance)
        }

        return (.far, distance)
    }

    static var supportsPedometer: Bool {
        CMPedometer.isStepCountingAvailable()
    }

    static var supportsDistance: Bool {
        CMPedometer.isDistanceAvailable()
    }

    static var supportsRelativeAltitude: Bool {
        CMAltimeter.isRelativeAltitudeAvailable()
    }
}

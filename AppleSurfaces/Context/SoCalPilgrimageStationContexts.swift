import Foundation

/// Geographic chapter-level proximity contexts for the Orange County exemplar.
///
/// GPS/location is intentionally coarse. The three Christ Cathedral spiritual
/// stations share one campus arrival context; QR/NFC/AR/image recognition can
/// disambiguate the exact physical station inside the campus.
enum SoCalPilgrimageStationContexts {
    static let christCathedral = AnnoPilgrimageStationContext(
        stationId: "christ_cathedral_la_vang",
        title: "Christ Cathedral / Our Lady of La Vang",
        latitude: 33.7870499,
        longitude: -117.8991339,
        approachRadiusMeters: 350,
        arrivalRadiusMeters: 120
    )

    static let saintColumban = AnnoPilgrimageStationContext(
        stationId: "st_columban",
        title: "Saint Columban Catholic Church",
        latitude: 33.77812,
        longitude: -117.94418,
        approachRadiusMeters: 300,
        arrivalRadiusMeters: 100
    )

    static let vietnameseCatholicCenter = AnnoPilgrimageStationContext(
        stationId: "vietnamese_catholic_center",
        title: "Vietnamese Catholic Center",
        latitude: 33.7589895,
        longitude: -117.9216506,
        approachRadiusMeters: 300,
        arrivalRadiusMeters: 100
    )

    static let ourLadyOfLaVangParish = AnnoPilgrimageStationContext(
        stationId: "our_lady_of_la_vang_parish",
        title: "Our Lady of La Vang Catholic Church",
        latitude: 33.7428866,
        longitude: -117.9208725,
        approachRadiusMeters: 300,
        arrivalRadiusMeters: 100
    )

    static let saintBarbara = AnnoPilgrimageStationContext(
        stationId: "st_barbara",
        title: "Saint Barbara Catholic Church",
        latitude: 33.737313,
        longitude: -117.937589,
        approachRadiusMeters: 300,
        arrivalRadiusMeters: 100
    )

    static let all: [AnnoPilgrimageStationContext] = [
        christCathedral,
        saintColumban,
        vietnameseCatholicCenter,
        ourLadyOfLaVangParish,
        saintBarbara
    ]
}

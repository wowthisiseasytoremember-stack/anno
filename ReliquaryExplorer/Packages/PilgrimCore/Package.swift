// swift-tools-version: 6.0
// Shared domain / business-logic package used by both the iOS/iPadOS app
// and the visionOS app. UI-adjacent but platform-neutral SwiftUI lives here
// too; only AR *session* plumbing and *CoreLocation* plumbing are pushed to
// the per-platform app targets (see Apps/iOS and Apps/visionOS).
//
// Swift 5 language mode is chosen deliberately: RealityKit `Entity` and
// `CLLocationManager` are not `Sendable`, and this project has not been
// compile-validated against Swift 6 strict concurrency. Migrating to
// Swift 6 mode is a contained follow-up (the seams are already actors/
// protocols).

import PackageDescription

let package = Package(
    name: "PilgrimCore",
    defaultLocalization: "en",
    platforms: [
        .iOS(.v17),
        .visionOS(.v1),
    ],
    products: [
        .library(name: "PilgrimCore", targets: ["PilgrimCore"]),
    ],
    targets: [
        .target(
            name: "PilgrimCore",
            dependencies: [],
            resources: [
                .process("Resources"),
            ],
            swiftSettings: [
                .swiftLanguageMode(.v5),
            ]
        ),
        .testTarget(
            name: "PilgrimCoreTests",
            dependencies: ["PilgrimCore"],
            resources: [
                .process("Fixtures"),
            ],
            swiftSettings: [
                .swiftLanguageMode(.v5),
            ]
        ),
    ]
)

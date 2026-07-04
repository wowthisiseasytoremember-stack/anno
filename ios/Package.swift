// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "AnnoPilgrimageMap",
    defaultLocalization: "en",
    platforms: [
        .iOS(.v17)
    ],
    products: [
        .library(
            name: "AnnoPilgrimageMap",
            targets: ["AnnoPilgrimageMap"]
        )
    ],
    targets: [
        .target(
            name: "AnnoPilgrimageMap"
        )
    ]
)

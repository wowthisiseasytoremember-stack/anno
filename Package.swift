// swift-tools-version:5.10
import PackageDescription

let package = Package(
    name: "AnnoStoreKit",
    platforms: [
        .macOS(.v13),
        .iOS(.v17)
    ],
    targets: [
        .target(
            name: "AnnoStoreKit",
            path: "storekit-core",
            sources: [
                "Sources/StoreKitProvider.swift",
                "Sources/StoreService.swift",
                "Sources/MockStoreProvider.swift",
                "Sources/EntitlementManager.swift"
            ]
        ),
        .testTarget(
            name: "AnnoStoreKitTests",
            dependencies: ["AnnoStoreKit"],
            path: "storekit-core",
            sources: [
                "Tests/StoreKitProviderTests.swift"
            ]
        )
    ]
)

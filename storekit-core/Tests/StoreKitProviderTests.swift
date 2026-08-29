// StoreKitProviderTests.swift
// Linux-compatible XCTest for the StoreKit abstraction layer.
import XCTest
@testable import AnnoStoreKit

final class StoreKitProviderTests: XCTestCase {

    func testFreshMockIsNotPremium() async throws {
        let provider = MockStoreProvider()
        let info = try await provider.getCustomerInfo()
        XCTAssertFalse(info.entitlements.active["premium"]?.isActive == true)
    }

    func testPurchaseGrantsPremium() async throws {
        let provider = MockStoreProvider()
        let service = StoreService(provider: provider)
        let offerings = try await service.loadOfferings()
        let yearly = try XCTUnwrap(offerings.first { $0.package.productIdentifier == "anno.subscription.yearly" })
        try await service.purchase(yearly.package)
        let info = try await provider.getCustomerInfo()
        XCTAssertTrue(service.isPremium(in: info))
    }

    func testRestoreClearsPremium() async throws {
        let provider = MockStoreProvider(initialPremium: true)
        let service = StoreService(provider: provider)
        try await service.restore()
        let info = try await provider.getCustomerInfo()
        XCTAssertFalse(service.isPremium(in: info))
    }

    func testOfferingsCount() async throws {
        let provider = MockStoreProvider()
        let offerings = try await provider.getOfferings()
        XCTAssertEqual(offerings.count, 2)
    }

    func testPurchaseFailureThrows() async {
        let provider = MockStoreProvider(failsPurchase: true)
        let pkg = StorePackage(id: "x", productIdentifier: "anno.subscription.yearly", localizedPrice: "$19.99", isTrial: true)
        do {
            try await provider.purchase(pkg)
            XCTFail("expected purchase to throw")
        } catch {
            // expected
        }
    }

    func testEntitlementManagerTier() async throws {
        let manager = EntitlementManager()
        let freeInfo = StoreCustomerInfo(entitlements: StoreEntitlements(active: [:]))
        XCTAssertEqual(manager.currentTier(in: freeInfo), .free)
        let premiumInfo = StoreCustomerInfo(
            entitlements: StoreEntitlements(active: ["premium": StoreEntitlement(identifier: "premium", isActive: true)])
        )
        XCTAssertEqual(manager.currentTier(in: premiumInfo), .premium)
    }
}

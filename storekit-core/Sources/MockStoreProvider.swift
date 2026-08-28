// MockStoreProvider.swift
// Deterministic in-memory test implementation of StoreKitProvider. Linux-testable.
import Foundation

public enum MockStoreError: Error { case purchaseFailed }

public final class MockStoreProvider: StoreKitProvider {
    private var premiumActive: Bool
    private let failsPurchase: Bool

    private let yearly = StorePackage(
        id: "yearly",
        productIdentifier: "anno.subscription.yearly",
        localizedPrice: "$19.99",
        isTrial: true
    )
    private let monthly = StorePackage(
        id: "monthly",
        productIdentifier: "anno.subscription.monthly",
        localizedPrice: "$2.99",
        isTrial: false
    )

    public init(initialPremium: Bool = false, failsPurchase: Bool = false) {
        self.premiumActive = initialPremium
        self.failsPurchase = failsPurchase
    }

    public func getOfferings() async throws -> [StoreOffering] {
        try? await Task.sleep(nanoseconds: 10_000_000)
        return [
            StoreOffering(id: "yearly_offer", title: "Anno Premium — Yearly", package: yearly),
            StoreOffering(id: "monthly_offer", title: "Anno Premium — Monthly", package: monthly)
        ]
    }

    public func getCustomerInfo() async throws -> StoreCustomerInfo {
        try? await Task.sleep(nanoseconds: 10_000_000)
        let entitlement = StoreEntitlement(identifier: "premium", isActive: premiumActive)
        return StoreCustomerInfo(entitlements: StoreEntitlements(active: ["premium": entitlement]))
    }

    public func purchase(_ package: StorePackage) async throws {
        try? await Task.sleep(nanoseconds: 10_000_000)
        if failsPurchase { throw MockStoreError.purchaseFailed }
        premiumActive = true
    }

    public func restorePurchases() async throws {
        try? await Task.sleep(nanoseconds: 10_000_000)
        premiumActive = false
    }
}

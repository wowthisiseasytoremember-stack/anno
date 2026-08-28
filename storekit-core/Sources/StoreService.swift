// StoreService.swift
// Logic-only service wrapping a StoreKitProvider. No SwiftUI/StoreKit/UIKit imports.
import Foundation

public final class StoreService {
    private let provider: StoreKitProvider

    public init(provider: StoreKitProvider) {
        self.provider = provider
    }

    public func loadOfferings() async throws -> [StoreOffering] {
        try await provider.getOfferings()
    }

    public func customerInfo() async throws -> StoreCustomerInfo {
        try await provider.getCustomerInfo()
    }

    public func purchase(_ package: StorePackage) async throws {
        try await provider.purchase(package)
    }

    public func restore() async throws {
        try await provider.restorePurchases()
    }

    public func isPremium(in info: StoreCustomerInfo) -> Bool {
        info.entitlements.active["premium"]?.isActive == true
    }
}

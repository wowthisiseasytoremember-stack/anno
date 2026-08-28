// StoreKitProvider.swift
// Linux-testable StoreKit abstraction for Anno.
// CONSTRAINT: NO external framework imports (no StoreKit/UIKit/SwiftUI/RevenueCat).
// Local domain types only so this module compiles + tests under `swift test` on Linux.
import Foundation

public struct StorePackage: Identifiable, Sendable {
    public let id: String
    public let productIdentifier: String
    public let localizedPrice: String
    public let isTrial: Bool
    public init(id: String, productIdentifier: String, localizedPrice: String, isTrial: Bool) {
        self.id = id
        self.productIdentifier = productIdentifier
        self.localizedPrice = localizedPrice
        self.isTrial = isTrial
    }
}

public struct StoreOffering: Identifiable, Sendable {
    public let id: String
    public let title: String
    public let package: StorePackage
    public init(id: String, title: String, package: StorePackage) {
        self.id = id
        self.title = title
        self.package = package
    }
}

public struct StoreEntitlement: Sendable {
    public let identifier: String
    public let isActive: Bool
    public init(identifier: String, isActive: Bool) {
        self.identifier = identifier
        self.isActive = isActive
    }
}

public struct StoreEntitlements: Sendable {
    public let active: [String: StoreEntitlement]
    public init(active: [String: StoreEntitlement]) { self.active = active }
}

public struct StoreCustomerInfo: Sendable {
    public let entitlements: StoreEntitlements
    public init(entitlements: StoreEntitlements) { self.entitlements = entitlements }
}

public protocol StoreKitProvider {
    func getOfferings() async throws -> [StoreOffering]
    func getCustomerInfo() async throws -> StoreCustomerInfo
    func purchase(_ package: StorePackage) async throws
    func restorePurchases() async throws
}

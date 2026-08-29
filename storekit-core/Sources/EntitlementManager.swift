// EntitlementManager.swift
// Pure-Swift entitlement mapping. No app imports (independent of Anno/Services/EntitlementService.swift).
import Foundation

public enum EntitlementTier: Equatable, Sendable {
    case free
    case premium
    public var isPremium: Bool { self == .premium }
}

public struct EntitlementManager {
    public init() {}

    public func currentTier(in info: StoreCustomerInfo) -> EntitlementTier {
        info.entitlements.active["premium"]?.isActive == true ? .premium : .free
    }
}

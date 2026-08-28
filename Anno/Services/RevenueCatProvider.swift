// RevenueCatProvider.swift
// macOS/iOS production StoreKitProvider backed by the RevenueCat SDK.
// NOTE: not part of the Linux Package.swift target — imports RevenueCat.
import Foundation
import RevenueCat

final class RevenueCatProvider: StoreKitProvider {

    func getOfferings() async throws -> [StoreOffering] {
        let offerings = try await Purchases.shared.getOfferings()
        guard let current = offerings.current else { return [] }
        return current.availablePackages.map { pkg in
            StoreOffering(
                id: pkg.identifier,
                title: current.identifier,
                package: StorePackage(
                    id: pkg.identifier,
                    productIdentifier: pkg.storeProduct.productIdentifier,
                    localizedPrice: pkg.localizedPriceString,
                    isTrial: (pkg.storeProduct.introDiscount?.paymentMode == .freeTrial)
                )
            )
        }
    }

    func getCustomerInfo() async throws -> StoreCustomerInfo {
        let info = try await Purchases.shared.getCustomerInfo()
        var active: [String: StoreEntitlement] = [:]
        for (id, ent) in info.entitlements.all {
            active[id] = StoreEntitlement(identifier: id, isActive: ent.isActive)
        }
        return StoreCustomerInfo(entitlements: StoreEntitlements(active: active))
    }

    func purchase(_ package: StorePackage) async throws {
        // Map local product identifier back to a RevenueCat Package via current offerings.
        let offerings = try await Purchases.shared.getOfferings()
        guard let rcPackage = offerings.current?.availablePackages.first(where: { $0.storeProduct.productIdentifier == package.productIdentifier }) else {
            throw NSError(domain: "Anno", code: -1, userInfo: [NSLocalizedDescriptionKey: "Package not found in current offerings"])
        }
        _ = try await Purchases.shared.purchase(package: rcPackage)
    }

    func restorePurchases() async throws {
        _ = try await Purchases.shared.restorePurchases()
    }
}

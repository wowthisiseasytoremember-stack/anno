import Foundation
import StoreKit
import SwiftUI

// MARK: - Entitlement Tier

public enum EntitlementTier: Equatable, Hashable, Sendable {
    case free
    case singleDayUnlocked(dateString: String)
    case premium
    case pilgrim

    public var isPremiumOrAbove: Bool {
        switch self {
        case .premium, .pilgrim:
            return true
        case .free, .singleDayUnlocked:
            return false
        }
    }

    public var isPilgrim: Bool {
        self == .pilgrim
    }
}

// MARK: - Paywall Trigger Enum

public enum PaywallTriggerType: String, CaseIterable, Identifiable, Sendable {
    case archiveHistoryGate = "archive_history_gate"
    case pilgrimRouteGate = "pilgrim_route_gate"
    case audioNarrationGate = "audio_narration_gate"
    case spiritualBouquetGate = "spiritual_bouquet_gate"

    public var id: String { rawValue }
}

public enum PaywallAction {
    case viewDate(Date)
    case accessPilgrimageRoutes
    case listenAudio(weeklyCount: Int)
    case saveBookmark(currentCount: Int)
}

// MARK: - Entitlement Service

@MainActor
public final class EntitlementService: ObservableObject {
    public static let shared = EntitlementService()

    // MARK: Product Identifiers
    public static let dayPassProductID = "com.anno.unlock.day_pass"
    public static let premiumAnnualProductID = "com.anno.subscription.premium.annual"
    public static let premiumMonthlyProductID = "com.anno.subscription.premium.monthly"
    public static let pilgrimAnnualProductID = "com.anno.subscription.pilgrim.annual"
    public static let pilgrimMonthlyProductID = "com.anno.subscription.pilgrim.monthly"

    public static let allProductIDs: Set<String> = [
        dayPassProductID,
        premiumAnnualProductID,
        premiumMonthlyProductID,
        pilgrimAnnualProductID,
        pilgrimMonthlyProductID
    ]

    // MARK: - Published State
    @Published public private(set) var currentTier: EntitlementTier = .free
    @Published public private(set) var unlockedSingleDays: Set<String> = []
    @Published public private(set) var products: [Product] = []
    @Published public private(set) var purchasedProductIDs: Set<String> = []
    @Published public private(set) var isProcessing: Bool = false
    @Published public var errorMessage: String? = nil
    @Published public var presentedPaywall: PaywallTriggerType? = nil

    // MARK: - Mock / Preview Overrides
    public var isMockMode: Bool = false
    public var mockOverrideTier: EntitlementTier? = nil
    public var mockOverrideUnlockedDays: Set<String> = []

    private var transactionListenerTask: Task<Void, Never>? = nil
    private let dateFormatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        formatter.timeZone = TimeZone(secondsFromGMT: 0)
        return formatter
    }()

    // MARK: - Initialization
    public init(isMockMode: Bool = false) {
        self.isMockMode = isMockMode
        if !isMockMode {
            startTransactionListener()
            Task {
                await loadProducts()
                await updateCustomerProductStatus()
            }
        }
    }

    deinit {
        transactionListenerTask?.cancel()
    }

    // MARK: - Static Mock Factory for Previews
    public static func mock(tier: EntitlementTier = .free, unlockedDays: Set<String> = []) -> EntitlementService {
        let service = EntitlementService(isMockMode: true)
        service.mockOverrideTier = tier
        service.mockOverrideUnlockedDays = unlockedDays
        service.currentTier = tier
        service.unlockedSingleDays = unlockedDays
        return service
    }

    // MARK: - StoreKit 2 Transaction Listener
    public func startTransactionListener() {
        transactionListenerTask?.cancel()
        transactionListenerTask = Task.detached { [weak self] in
            for await result in Transaction.updates {
                do {
                    let transaction = try self?.checkVerified(result)
                    if let transaction = transaction {
                        await self?.updateCustomerProductStatus()
                        await transaction.finish()
                    }
                } catch {
                    print("[EntitlementService] Unverified transaction update: \(error)")
                }
            }
        }
    }

    // MARK: - Load Products
    public func loadProducts() async {
        guard !isMockMode else { return }
        do {
            let storeProducts = try await Product.products(for: Self.allProductIDs)
            self.products = storeProducts.sorted { $0.price < $1.price }
        } catch {
            print("[EntitlementService] Failed to load StoreKit products: \(error)")
            self.errorMessage = error.localizedDescription
        }
    }

    // MARK: - Purchase
    @discardableResult
    public func purchase(_ product: Product) async throws -> Transaction? {
        if isMockMode {
            applyMockPurchase(productID: product.id)
            return nil
        }

        isProcessing = true
        defer { isProcessing = false }

        let result = try await product.purchase()
        switch result {
        case .success(let verification):
            let transaction = try checkVerified(verification)
            await updateCustomerProductStatus()
            await transaction.finish()
            return transaction
        case .userCancelled:
            return nil
        case .pending:
            return nil
        @unknown default:
            return nil
        }
    }

    public func purchase(productID: String) async throws {
        if isMockMode {
            applyMockPurchase(productID: productID)
            return
        }
        guard let product = products.first(where: { $0.id == productID }) else {
            throw NSError(domain: "Anno.EntitlementService", code: 404, userInfo: [NSLocalizedDescriptionKey: "Product \(productID) not found"])
        }
        try await purchase(product)
    }

    public func purchaseSingleDay(for date: Date) async throws {
        let dateKey = dateFormatter.string(from: date)
        if isMockMode {
            unlockedSingleDays.insert(dateKey)
            if currentTier == .free {
                currentTier = .singleDayUnlocked(dateString: dateKey)
            }
            return
        }

        try await purchase(productID: Self.dayPassProductID)
        unlockedSingleDays.insert(dateKey)
        saveUnlockedDays()
    }

    // MARK: - Restore Purchases
    public func restorePurchases() async throws {
        if isMockMode {
            return
        }

        isProcessing = true
        defer { isProcessing = false }

        try await AppStore.sync()
        await updateCustomerProductStatus()
    }

    // MARK: - Entitlement Verification & State Resolution
    public func updateCustomerProductStatus() async {
        if isMockMode {
            if let mockTier = mockOverrideTier {
                self.currentTier = mockTier
                self.unlockedSingleDays = mockOverrideUnlockedDays
            }
            return
        }

        var activeProductIDs: Set<String> = []
        var resolvedTier: EntitlementTier = .free

        for await result in Transaction.currentEntitlements {
            do {
                let transaction = try checkVerified(result)
                activeProductIDs.insert(transaction.productID)

                if transaction.productID == Self.pilgrimAnnualProductID ||
                   transaction.productID == Self.pilgrimMonthlyProductID {
                    resolvedTier = .pilgrim
                } else if (transaction.productID == Self.premiumAnnualProductID ||
                           transaction.productID == Self.premiumMonthlyProductID) &&
                           resolvedTier != .pilgrim {
                    resolvedTier = .premium
                } else if transaction.productID == Self.dayPassProductID &&
                          !resolvedTier.isPremiumOrAbove {
                    loadUnlockedDays()
                }
            } catch {
                print("[EntitlementService] Entitlement verification failed: \(error)")
            }
        }

        self.purchasedProductIDs = activeProductIDs
        self.currentTier = resolvedTier
    }

    // MARK: - Verification Helper
    private func checkVerified<T>(_ result: VerificationResult<T>) throws -> T {
        switch result {
        case .unverified(_, let error):
            throw error
        case .verified(let safe):
            return safe
        }
    }

    // MARK: - Feature Gate Checking

    public func effectiveTier() -> EntitlementTier {
        if let mock = mockOverrideTier {
            return mock
        }
        return currentTier
    }

    public func canAccessDate(_ date: Date) -> Bool {
        let tier = effectiveTier()
        if tier.isPremiumOrAbove {
            return true
        }

        // Today is always free
        let calendar = Calendar.current
        if calendar.isDateInToday(date) {
            return true
        }

        let dateKey = dateFormatter.string(from: date)
        if unlockedSingleDays.contains(dateKey) || mockOverrideUnlockedDays.contains(dateKey) {
            return true
        }

        return false
    }

    public func canAccessPilgrimageRoute() -> Bool {
        let tier = effectiveTier()
        return tier.isPilgrim
    }

    public func canAccessAudio(weeklyListenCount: Int) -> Bool {
        let tier = effectiveTier()
        if tier.isPremiumOrAbove {
            return true
        }
        return weeklyListenCount < 3
    }

    public func canCreateBookmark(currentSavedCount: Int) -> Bool {
        let tier = effectiveTier()
        if tier.isPremiumOrAbove {
            return true
        }
        return currentSavedCount < 5
    }

    public func checkPaywall(for action: PaywallAction) -> PaywallTriggerType? {
        switch action {
        case .viewDate(let date):
            if !canAccessDate(date) {
                return .archiveHistoryGate
            }
        case .accessPilgrimageRoutes:
            if !canAccessPilgrimageRoute() {
                return .pilgrimRouteGate
            }
        case .listenAudio(let weeklyCount):
            if !canAccessAudio(weeklyListenCount: weeklyCount) {
                return .audioNarrationGate
            }
        case .saveBookmark(let currentCount):
            if !canCreateBookmark(currentSavedCount: currentCount) {
                return .spiritualBouquetGate
            }
        }
        return nil
    }

    // MARK: - Private Persistence for Single Day Unlocks
    private let singleDayStorageKey = "com.anno.unlocked_days"

    private func saveUnlockedDays() {
        let array = Array(unlockedSingleDays)
        UserDefaults.standard.set(array, forKey: singleDayStorageKey)
    }

    private func loadUnlockedDays() {
        if let array = UserDefaults.standard.stringArray(forKey: singleDayStorageKey) {
            unlockedSingleDays = Set(array)
        }
    }

    private func applyMockPurchase(productID: String) {
        purchasedProductIDs.insert(productID)
        if productID == Self.pilgrimAnnualProductID || productID == Self.pilgrimMonthlyProductID {
            currentTier = .pilgrim
        } else if productID == Self.premiumAnnualProductID || productID == Self.premiumMonthlyProductID {
            currentTier = .premium
        }
    }
}

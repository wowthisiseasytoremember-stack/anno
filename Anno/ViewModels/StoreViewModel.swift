// StoreViewModel.swift
// SwiftUI-facing view model. Holds a StoreService (logic-only) and publishes state.
// NOTE: not part of the Linux Package.swift target — imports SwiftUI.
import Foundation
import SwiftUI

@Observable
final class StoreViewModel {

    private let service: StoreService

    var offerings: [StoreOffering] = []
    var isPremium: Bool = false
    var isLoading: Bool = false
    var errorMessage: String?

    init(service: StoreService) {
        self.service = service
    }

    @MainActor
    func load() async {
        isLoading = true
        defer { isLoading = false }
        do {
            offerings = try await service.loadOfferings()
            let info = try await service.customerInfo()
            isPremium = service.isPremium(in: info)
        } catch {
            errorMessage = error.localizedDescription
        }
    }

    @MainActor
    func purchase(_ package: StorePackage) async {
        isLoading = true
        defer { isLoading = false }
        do {
            try await service.purchase(package)
            let info = try await service.customerInfo()
            isPremium = service.isPremium(in: info)
        } catch {
            errorMessage = error.localizedDescription
        }
    }

    @MainActor
    func restore() async {
        isLoading = true
        defer { isLoading = false }
        do {
            try await service.restore()
            let info = try await service.customerInfo()
            isPremium = service.isPremium(in: info)
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}

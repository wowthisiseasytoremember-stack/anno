import CoreLocation
import Foundation

/// Loads and validates the sanctuary registry.
///
/// The registry ships as `SanctuariesConfig.json` inside the package
/// resources; `load(url:)` exists so tests (and, later, a downloaded
/// config) can inject data from anywhere.
public struct SanctuaryCatalog: Sendable {
    public let sites: [SanctuarySite]

    public init(sites: [SanctuarySite]) {
        self.sites = sites
    }

    // MARK: - Loading

    public static let defaultResourceName = "SanctuariesConfig"

    public static func load(
        bundle: Bundle = .module,
        resource: String = defaultResourceName
    ) throws -> SanctuaryCatalog {
        guard let url = bundle.url(forResource: resource, withExtension: "json") else {
            throw SanctuaryCatalogError.resourceMissing(resource)
        }
        return try load(url: url)
    }

    public static func load(url: URL, decoder: JSONDecoder = JSONDecoder()) throws -> SanctuaryCatalog {
        do {
            let data = try Data(contentsOf: url)
            let sites = try decoder.decode([SanctuarySite].self, from: data)
            return try SanctuaryCatalog(sites: sites).validated()
        } catch let error as SanctuaryCatalogError {
            throw error
        } catch {
            throw SanctuaryCatalogError.undecodable(underlying: error)
        }
    }

    // MARK: - Access

    public func site(withID id: String) -> SanctuarySite? {
        sites.first { $0.id == id }
    }

    // MARK: - Validation

    /// Sanity limits so bad data fails loudly at load instead of silently
    /// at a trailhead. Region-monitoring radii under ~100 m are permitted
    /// (GNSS + Wi-Fi can still service them) but flagged ranges are rejected.
    public static let acceptableRadiusRange: ClosedRange<Double> = 20...5_000

    public func validated() throws -> SanctuaryCatalog {
        var seen = Set<String>()
        var duplicates: [String] = []
        for site in sites where !seen.insert(site.id).inserted {
            duplicates.append(site.id)
        }
        if !duplicates.isEmpty {
            throw SanctuaryCatalogError.duplicateSiteIDs(duplicates.sorted())
        }

        var invalidRadius: [String] = []
        var invalidCoordinate: [String] = []
        var missingNarration: [String] = []

        for site in sites {
            if !Self.acceptableRadiusRange.contains(site.radiusMeters) {
                invalidRadius.append(site.id)
            }
            if abs(site.latitude) > 90 || abs(site.longitude) > 180 {
                invalidCoordinate.append(site.id)
            }
            if site.narrations.isEmpty {
                missingNarration.append(site.id)
            }
        }

        if !invalidRadius.isEmpty {
            throw SanctuaryCatalogError.invalidRadius(
                siteIDs: invalidRadius,
                allowed: Self.acceptableRadiusRange
            )
        }
        if !invalidCoordinate.isEmpty {
            throw SanctuaryCatalogError.invalidCoordinate(siteIDs: invalidCoordinate)
        }
        if !missingNarration.isEmpty {
            throw SanctuaryCatalogError.missingNarration(siteIDs: missingNarration)
        }
        return self
    }
}

public enum SanctuaryCatalogError: Error, Equatable, Sendable {
    case resourceMissing(String)
    case undecodable(underlying: Error)
    case duplicateSiteIDs([String])
    case invalidRadius(siteIDs: [String], allowed: ClosedRange<Double>)
    case invalidCoordinate(siteIDs: [String])
    case missingNarration(siteIDs: [String])

    public static func == (lhs: SanctuaryCatalogError, rhs: SanctuaryCatalogError) -> Bool {
        switch (lhs, rhs) {
        case let (.resourceMissing(a), .resourceMissing(b)): a == b
        case let (.duplicateSiteIDs(a), .duplicateSiteIDs(b)): a == b
        case let (.invalidRadius(a, r1), .invalidRadius(b, r2)): a == b && r1 == r2
        case let (.invalidCoordinate(a), .invalidCoordinate(b)): a == b
        case let (.missingNarration(a), .missingNarration(b)): a == b
        case (.undecodable, .undecodable): true
        default: false
        }
    }
}

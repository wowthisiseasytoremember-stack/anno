import Foundation

public enum LanguageMode: String, CaseIterable, Identifiable {
    case english = "EN"
    case vietnamese = "VI"

    public var id: String { rawValue }
}

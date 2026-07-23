import Foundation

enum LanguageMode: String, CaseIterable, Identifiable {
    case english = "EN"
    case vietnamese = "VI"

    var id: String { rawValue }
}

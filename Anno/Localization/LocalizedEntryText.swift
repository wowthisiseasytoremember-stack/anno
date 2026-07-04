import Foundation

struct LocalizedEntryText {
    let entry: AnnoEntry
    let language: LanguageMode

    var title: String {
        language == .vietnamese ? entry.primary.titleVi : entry.primary.titleEn
    }

    var summary: String {
        language == .vietnamese ? entry.primary.summaryVi : entry.primary.summaryEn
    }

    var liturgicalTitle: String {
        language == .vietnamese ? entry.liturgical.titleVi : entry.liturgical.titleEn
    }

    var heroLine: String {
        language == .vietnamese ? entry.appHooks.heroLineVi : entry.appHooks.heroLineEn
    }

    var prayerPrompt: String {
        language == .vietnamese ? entry.appHooks.prayerPromptVi : entry.appHooks.prayerPromptEn
    }

    var confidenceNote: String {
        language == .vietnamese ? entry.primary.confidenceNoteVi : entry.primary.confidenceNoteEn
    }

    var confidenceLabel: String {
        switch entry.primary.confidence {
        case .confirmed:
            return language == .vietnamese ? "Đã xác nhận" : "Confirmed"
        case .traditional:
            return language == .vietnamese ? "Theo truyền thống" : "Traditional"
        case .disputed:
            return language == .vietnamese ? "Còn tranh luận" : "Disputed"
        case .contextual:
            return language == .vietnamese ? "Theo bối cảnh" : "Contextual"
        }
    }
}

import SwiftUI

struct SourceSheet: View {
    let entry: AnnoEntry
    let language: LanguageMode

    private var groupedSources: [(String, [SourceRef])] {
        Dictionary(grouping: entry.sources, by: \.type)
            .map { ($0.key, $0.value) }
            .sorted { $0.0 < $1.0 }
    }

    var body: some View {
        NavigationStack {
            List {
                Section(language == .vietnamese ? "Ghi chú độ tin cậy" : "Confidence note") {
                    Text(LocalizedEntryText(entry: entry, language: language).confidenceNote)
                        .foregroundStyle(AnnoTheme.vellum)
                        .fixedSize(horizontal: false, vertical: true)
                        .listRowBackground(AnnoTheme.choir)
                }

                ForEach(groupedSources, id: \.0) { type, sources in
                    Section(type.replacingOccurrences(of: "_", with: " ").capitalized) {
                        ForEach(sources) { source in
                            SourceRow(source: source)
                                .listRowBackground(AnnoTheme.choir)
                        }
                    }
                }
            }
            .scrollContentBackground(.hidden)
            .background(AnnoTheme.narthex)
            .navigationTitle(language == .vietnamese ? "Nguồn" : "Sources")
        }
    }
}

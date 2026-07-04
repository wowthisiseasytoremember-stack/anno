import SwiftUI

struct WeekCalendarView: View {
    @ObservedObject var store: FixtureStore
    let language: LanguageMode

    var body: some View {
        NavigationStack {
            List(store.weekEntries) { entry in
                EntryListRow(
                    entry: entry,
                    language: language,
                    isSelected: store.selectedEntryID == entry.id
                )
                .listRowBackground(AnnoTheme.narthex)
                .onTapGesture {
                    store.select(entry)
                }
            }
            .scrollContentBackground(.hidden)
            .background(AnnoTheme.narthex)
            .navigationTitle(language == .vietnamese ? "Lịch" : "Calendar")
        }
    }
}

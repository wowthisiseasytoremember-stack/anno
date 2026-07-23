import SwiftUI
import Foundation

// MARK: - MonthCalendarView

struct MonthCalendarView: View {
    let entries: [AnnoEntry]
    let language: LanguageMode
    let onSelectEntry: (AnnoEntry) -> Void

    @State private var displayedMonth: Date
    @State private var selectedDate: Date

    // MARK: Init

    init(entries: [AnnoEntry], language: LanguageMode, onSelectEntry: @escaping (AnnoEntry) -> Void) {
        self.entries = entries
        self.language = language
        self.onSelectEntry = onSelectEntry

        let today = Date()
        let cal = Self.makeCalendar()
        let comps = cal.dateComponents([.year, .month], from: today)
        let startOfThisMonth = cal.date(from: comps) ?? today

        _displayedMonth = State(initialValue: startOfThisMonth)
        _selectedDate  = State(initialValue: today)
    }

    // MARK: Calendar / Formatters

    private static func makeCalendar() -> Calendar {
        var cal = Calendar(identifier: .gregorian)
        cal.firstWeekday = 1 // Sunday
        return cal
    }

    private var calendar: Calendar { Self.makeCalendar() }

    private var isoFormatter: DateFormatter {
        let f = DateFormatter()
        f.calendar = Calendar(identifier: .gregorian)
        f.locale = Locale(identifier: "en_US_POSIX")
        f.timeZone = .current
        f.dateFormat = "yyyy-MM-dd"
        return f
    }

    private var monthYearFormatter: DateFormatter {
        let f = DateFormatter()
        f.locale = Locale(identifier: language == .vietnamese ? "vi_VN" : "en_US")
        f.calendar = calendar
        f.dateFormat = "MMMM yyyy"
        return f
    }

    private var fullDateFormatter: DateFormatter {
        let f = DateFormatter()
        f.locale = Locale(identifier: language == .vietnamese ? "vi_VN" : "en_US")
        f.calendar = calendar
        f.dateStyle = .full
        return f
    }

    // MARK: Derived Data

    private var navigationTitle: String {
        language == .english ? "Calendar" : "Lịch"
    }

    private var entriesByDate: [String: [AnnoEntry]] {
        Dictionary(grouping: entries, by: { $0.date })
    }

    private var selectedDateKey: String {
        isoFormatter.string(from: selectedDate)
    }

    private var selectedDayEntries: [AnnoEntry] {
        entriesByDate[selectedDateKey] ?? []
    }

    private var startOfDisplayedMonth: Date {
        let comps = calendar.dateComponents([.year, .month], from: displayedMonth)
        return calendar.date(from: comps) ?? displayedMonth
    }

    private var dayCells: [Date?] {
        let first = startOfDisplayedMonth
        let count = calendar.range(of: .day, in: .month, for: first)?.count ?? 0
        let weekdayOfFirst = calendar.component(.weekday, from: first) // 1 = Sunday
        let leading = max(weekdayOfFirst - calendar.firstWeekday, 0)

        var cells: [Date?] = Array(repeating: nil, count: leading)
        for d in 0..<count {
            cells.append(calendar.date(byAdding: .day, value: d, to: first))
        }
        while cells.count % 7 != 0 { cells.append(nil) }
        return cells
    }

    // MARK: Layout Constants

    private let gridColumns = Array(
        repeating: GridItem(.flexible(), spacing: 6),
        count: 7
    )

    // MARK: Body

    var body: some View {
        ZStack {
            AnnoTheme.narthex.ignoresSafeArea()

            ScrollView {
                VStack(spacing: 16) {
                    monthHeader
                    weekdayHeader
                    calendarGrid
                    detailPanel
                }
                .padding(.horizontal, 16)
                .padding(.vertical, 12)
            }
            .scrollContentBackground(.hidden)
            .scrollIndicators(.hidden)
        }
        .navigationTitle(navigationTitle)
        .navigationBarTitleDisplayMode(.inline)
        .toolbarColorScheme(.dark, for: .navigationBar)
        .toolbarBackground(AnnoTheme.narthex, for: .navigationBar)
        .toolbarBackground(.visible, for: .navigationBar)
    }

    // MARK: - Month Header

    private var monthHeader: some View {
        HStack(spacing: 12) {
            Button { changeMonth(by: -1) } label: {
                Image(systemName: "chevron.left")
                    .font(.body.weight(.semibold))
                    .foregroundColor(AnnoTheme.goldLeaf)
                    .frame(width: 36, height: 36)
                    .background(AnnoTheme.choir)
                    .clipShape(Circle())
                    .overlay(Circle().stroke(AnnoTheme.ash, lineWidth: 1))
            }

            Spacer()

            Text(monthYearFormatter.string(from: displayedMonth).localizedCapitalized)
                .font(.title3.weight(.bold))
                .foregroundColor(AnnoTheme.vellum)
                .monospacedDigit()

            Spacer()

            Button { changeMonth(by: 1) } label: {
                Image(systemName: "chevron.right")
                    .font(.body.weight(.semibold))
                    .foregroundColor(AnnoTheme.goldLeaf)
                    .frame(width: 36, height: 36)
                    .background(AnnoTheme.choir)
                    .clipShape(Circle())
                    .overlay(Circle().stroke(AnnoTheme.ash, lineWidth: 1))
            }
        }
        .padding(.top, 4)
    }

    // MARK: - Weekday Header

    private var weekdayHeader: some View {
        let en = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        let vi = ["CN", "T2", "T3", "T4", "T5", "T6", "T7"]
        let symbols = (language == .english) ? en : vi

        return LazyVGrid(columns: gridColumns, spacing: 4) {
            ForEach(Array(symbols.enumerated()), id: \.offset) { idx, sym in
                Text(sym)
                    .font(.caption.weight(.semibold))
                    .foregroundColor(idx == 0 ? AnnoTheme.goldLeaf : AnnoTheme.incense)
                    .frame(maxWidth: .infinity)
                    .fixedSize(horizontal: false, vertical: true)
            }
        }
    }

    // MARK: - Calendar Grid

    private var calendarGrid: some View {
        LazyVGrid(columns: gridColumns, spacing: 10) {
            ForEach(Array(dayCells.enumerated()), id: \.offset) { _, cell in
                if let date = cell {
                    dayCell(for: date)
                } else {
                    Color.clear.frame(height: 44)
                }
            }
        }
        .padding(12)
        .annoCard()
    }

    private func dayCell(for date: Date) -> some View {
        let dayNum = calendar.component(.day, from: date)
        let isToday = calendar.isDate(date, inSameDayAs: Date())
        let isSelected = calendar.isDate(date, inSameDayAs: selectedDate)
        let isSunday = calendar.component(.weekday, from: date) == 1

        let key = isoFormatter.string(from: date)
        let dayEntries = entriesByDate[key] ?? []
        let dotColors = Array(dayEntries.prefix(2)).map { liturgicalColor(for: $0.liturgical.color) }

        return Button {
            withAnimation(.easeInOut(duration: 0.25)) {
                selectedDate = date
            }
        } label: {
            VStack(spacing: 4) {
                ZStack {
                    if isSelected {
                        Circle()
                            .fill(AnnoTheme.goldLeaf)
                            .frame(width: 32, height: 32)
                    } else if isToday {
                        Circle()
                            .stroke(AnnoTheme.goldLeaf, lineWidth: 1.4)
                            .frame(width: 32, height: 32)
                    }

                    Text("\(dayNum)")
                        .font(.callout.monospacedDigit().weight(isSelected ? .bold : .regular))
                        .foregroundColor(
                            isSelected
                                ? AnnoTheme.narthex
                                : (isSunday ? AnnoTheme.goldLeaf : AnnoTheme.vellum)
                        )
                        .fixedSize(horizontal: false, vertical: true)
                }
                .frame(height: 32)

                HStack(spacing: 3) {
                    if dotColors.isEmpty {
                        Circle().fill(Color.clear).frame(width: 4, height: 4)
                    } else {
                        ForEach(Array(dotColors.enumerated()), id: \.offset) { _, color in
                            Circle().fill(color).frame(width: 4, height: 4)
                        }
                    }
                }
                .frame(height: 6)
            }
            .frame(maxWidth: .infinity, minHeight: 44)
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
        .accessibilityLabel(accessibilityLabel(for: date, entriesCount: dayEntries.count))
        .accessibilityAddTraits(isSelected ? [.isSelected] : [])
    }

    private func accessibilityLabel(for date: Date, entriesCount: Int) -> String {
        let dateString = fullDateFormatter.string(from: date)
        if entriesCount == 0 {
            return language == .english
                ? "\(dateString). No events."
                : "\(dateString). Không có sự kiện."
        }
        return language == .english
            ? "\(dateString). \(entriesCount) event(s)."
            : "\(dateString). \(entriesCount) sự kiện."
    }

    // MARK: - Detail Panel

    private var detailPanel: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(fullDateFormatter.string(from: selectedDate).localizedCapitalized)
                .font(.headline)
                .foregroundColor(AnnoTheme.vellum)
                .fixedSize(horizontal: false, vertical: true)

            if let first = selectedDayEntries.first {
                conversionsView(for: first.calendars)
            }

            if selectedDayEntries.isEmpty {
                Text(language == .english
                     ? "No events for this day."
                     : "Không có sự kiện cho ngày này.")
                    .font(.subheadline)
                    .foregroundColor(AnnoTheme.incense)
                    .fixedSize(horizontal: false, vertical: true)
                    .padding(.vertical, 6)
            } else {
                VStack(alignment: .leading, spacing: 8) {
                    ForEach(selectedDayEntries, id: \.id) { entry in
                        eventRow(entry)
                    }
                }
            }

            Button {
                if let first = selectedDayEntries.first {
                    onSelectEntry(first)
                }
            } label: {
                Text(language == .english ? "Open This Day" : "Mở ngày này")
                    .font(.headline)
                    .foregroundColor(AnnoTheme.narthex)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 14)
                    .background(selectedDayEntries.isEmpty ? AnnoTheme.ash : AnnoTheme.goldLeaf)
                    .clipShape(RoundedRectangle(cornerRadius: 12))
            }
            .disabled(selectedDayEntries.isEmpty)
            .padding(.top, 4)
        }
        .padding(14)
        .annoCard()
        .id(selectedDateKey)
        .transition(.opacity)
        .animation(.easeInOut(duration: 0.25), value: selectedDateKey)
    }

    // MARK: - Calendar Conversions

    private func conversionsView(for c: CalendarConversions) -> some View {
        let items: [(String, String)] = [
            ("Julian",       c.julian),
            ("Hebrew",       c.hebrew),
            ("Umm al-Qura",  c.islamicUmmAlQura),
            ("Coptic",       c.coptic),
            ("Ethiopian",    c.ethiopian)
        ]

        return ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                ForEach(items, id: \.0) { label, value in
                    VStack(spacing: 1) {
                        Text(label)
                            .font(.system(size: 8, weight: .semibold))
                            .foregroundColor(AnnoTheme.incense)
                            .fixedSize(horizontal: false, vertical: true)
                        Text(value)
                            .font(.system(size: 10, weight: .medium))
                            .foregroundColor(AnnoTheme.vellum)
                            .fixedSize(horizontal: true, vertical: true)
                    }
                    .padding(.horizontal, 10)
                    .padding(.vertical, 6)
                    .background(AnnoTheme.narthex)
                    .clipShape(Capsule())
                    .overlay(Capsule().stroke(AnnoTheme.ash, lineWidth: 0.5))
                }
            }
        }
    }

    // MARK: - Event Row

    private func eventRow(_ entry: AnnoEntry) -> some View {
        let loc = LocalizedEntryText(entry: entry, language: language)

        return HStack(alignment: .top, spacing: 10) {
            RoundedRectangle(cornerRadius: 2)
                .fill(liturgicalColor(for: entry.liturgical.color))
                .frame(width: 4)

            VStack(alignment: .leading, spacing: 4) {
                Text(loc.title)
                    .font(.subheadline.weight(.semibold))
                    .foregroundColor(AnnoTheme.vellum)
                    .fixedSize(horizontal: false, vertical: true)

                if !loc.liturgicalTitle.isEmpty {
                    Text(loc.liturgicalTitle)
                        .font(.caption)
                        .foregroundColor(AnnoTheme.incense)
                        .fixedSize(horizontal: false, vertical: true)
                }

                HStack(spacing: 8) {
                    Text(entry.liturgical.rank)
                        .font(.caption2.weight(.medium))
                        .foregroundColor(AnnoTheme.incense)
                        .fixedSize(horizontal: false, vertical: true)

                    ConfidenceBadge(label: loc.confidenceLabel, confidence: entry.primary.confidence)
                }
            }

            Spacer(minLength: 8)
        }
        .padding(10)
        .background(AnnoTheme.narthex)
        .clipShape(RoundedRectangle(cornerRadius: 8))
        .overlay(RoundedRectangle(cornerRadius: 8).stroke(AnnoTheme.ash, lineWidth: 1))
    }

    // MARK: - Helpers

    private func liturgicalColor(for raw: String) -> Color {
        switch raw.lowercased() {
        case "red":              return AnnoTheme.crimson
        case "green":            return AnnoTheme.verdigris
        case "white":            return AnnoTheme.vellum
        case "violet", "purple": return AnnoTheme.advent
        case "gold":             return AnnoTheme.goldLeaf
        default:                 return AnnoTheme.incense
        }
    }

    private func changeMonth(by value: Int) {
        guard let newMonth = calendar.date(byAdding: .month, value: value, to: displayedMonth) else {
            return
        }
        withAnimation(.easeInOut(duration: 0.25)) {
            displayedMonth = newMonth
            // If the selected date falls outside the new month, snap to the first day.
            if !calendar.isDate(selectedDate, equalTo: newMonth, toGranularity: .month) {
                selectedDate = startOfMonth(for: newMonth)
            }
        }
    }

    private func startOfMonth(for date: Date) -> Date {
        let comps = calendar.dateComponents([.year, .month], from: date)
        return calendar.date(from: comps) ?? date
    }
}

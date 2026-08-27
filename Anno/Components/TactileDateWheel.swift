//  TactileDateWheel.swift
//  Anno
//
//  Task C.5.2: Tactile Wheel Date Scrubbing with Physical Haptics.
//  Features:
//  - Smooth horizontal tactile date scrubber dial with snap feedback
//  - UIImpactFeedbackGenerator(style: .light) firing on every date step
//  - Synchronized multi-calendar conversion strip (Gregorian, Julian, Hebrew, Islamic, Coptic, Ethiopian)
//  - Bilingual date & calendar labels (EN/VI)
//  - Quick Jump to Today with glowing liturgical indicator

import SwiftUI
import UIKit

struct TactileDateWheel: View {
    @Binding var selectedDate: Date
    let entries: [AnnoEntry]
    let language: LanguageMode
    var onSelectDate: ((Date) -> Void)?

    // MARK: - Internal State
    @State private var centeredIndex: Int = 0
    @State private var dateList: [Date] = []
    @State private var lastHapticDate: Date?

    private let dayRange: Int = 60 // 60 days before and after anchor

    // MARK: - Calendar & Formatters

    private var calendar: Calendar {
        var cal = Calendar(identifier: .gregorian)
        cal.timeZone = .current
        return cal
    }

    private var isoFormatter: DateFormatter {
        let f = DateFormatter()
        f.calendar = Calendar(identifier: .gregorian)
        f.locale = Locale(identifier: "en_US_POSIX")
        f.timeZone = .current
        f.dateFormat = "yyyy-MM-dd"
        return f
    }

    // MARK: - Initializer

    init(
        selectedDate: Binding<Date>,
        entries: [AnnoEntry] = [],
        language: LanguageMode = .english,
        onSelectDate: ((Date) -> Void)? = nil
    ) {
        self._selectedDate = selectedDate
        self.entries = entries
        self.language = language
        self.onSelectDate = onSelectDate
    }

    // MARK: - Body

    var body: some View {
        VStack(spacing: 16) {
            // 1. Month / Year Header & Quick Controls
            wheelHeaderView

            // 2. Tactile Horizontal Scrubber Wheel
            scrubberScrollView

            // 3. Synchronized Multi-Calendar Conversion Strip
            multiCalendarConversionsStrip
        }
        .padding(.vertical, 14)
        .padding(.horizontal, 12)
        .background(
            RoundedRectangle(cornerRadius: 16, style: .continuous)
                .fill(AnnoTheme.choir)
                .overlay(
                    RoundedRectangle(cornerRadius: 16, style: .continuous)
                        .strokeBorder(AnnoTheme.ash, lineWidth: 1)
                )
        )
        .onAppear {
            generateDateList()
        }
        .onChange(of: selectedDate) { newDate in
            triggerHapticFeedback(for: newDate)
        }
    }

    // MARK: - Header View

    private var wheelHeaderView: some View {
        HStack(spacing: 8) {
            // Month & Year Display
            VStack(alignment: .leading, spacing: 2) {
                Text(monthYearString(from: selectedDate).localizedCapitalized)
                    .font(Typography.headlineSerif)
                    .foregroundStyle(AnnoTheme.vellum)

                Text(fullWeekdayDateString(from: selectedDate))
                    .font(Typography.captionSerif)
                    .foregroundStyle(AnnoTheme.incense)
            }

            Spacer()

            // Step Backward Button
            Button(action: {
                stepDate(by: -1)
            }) {
                Image(systemName: "chevron.left")
                    .font(Typography.captionBoldSerif)
                    .foregroundStyle(AnnoTheme.goldLeaf)
                    .padding(8)
                    .background(Circle().fill(AnnoTheme.narthex))
                    .overlay(Circle().stroke(AnnoTheme.ash, lineWidth: 1))
            }
            .buttonStyle(.plain)
            .accessibilityLabel(language == .vietnamese ? "Ngày trước" : "Previous day")

            // "Today" Button
            Button(action: {
                jumpToToday()
            }) {
                Text(language == .vietnamese ? "Hôm nay" : "Today")
                    .font(Typography.captionBoldSerif)
                    .foregroundStyle(isToday(selectedDate) ? AnnoTheme.narthex : AnnoTheme.goldLeaf)
                    .padding(.horizontal, 10)
                    .padding(.vertical, 6)
                    .background(
                        Capsule()
                            .fill(isToday(selectedDate) ? AnnoTheme.goldLeaf : AnnoTheme.narthex)
                    )
                    .overlay(
                        Capsule()
                            .stroke(AnnoTheme.goldLeaf.opacity(0.6), lineWidth: 1)
                    )
            }
            .buttonStyle(.plain)

            // Step Forward Button
            Button(action: {
                stepDate(by: 1)
            }) {
                Image(systemName: "chevron.right")
                    .font(Typography.captionBoldSerif)
                    .foregroundStyle(AnnoTheme.goldLeaf)
                    .padding(8)
                    .background(Circle().fill(AnnoTheme.narthex))
                    .overlay(Circle().stroke(AnnoTheme.ash, lineWidth: 1))
            }
            .buttonStyle(.plain)
            .accessibilityLabel(language == .vietnamese ? "Ngày sau" : "Next day")
        }
        .padding(.horizontal, 4)
    }

    // MARK: - Scrubber Scroll View

    private var scrubberScrollView: some View {
        ScrollViewReader { proxy in
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 8) {
                    ForEach(dateList, id: \.self) { date in
                        scrubberDayItem(for: date)
                            .id(dateIdentifier(for: date))
                    }
                }
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
            }
            .onAppear {
                proxy.scrollTo(dateIdentifier(for: selectedDate), anchor: .center)
            }
            .onChange(of: selectedDate) { newDate in
                withAnimation(.spring(response: 0.35, dampingFraction: 0.8)) {
                    proxy.scrollTo(dateIdentifier(for: newDate), anchor: .center)
                }
            }
        }
    }

    // MARK: - Scrubber Day Item

    private func scrubberDayItem(for date: Date) -> some View {
        let isSelected = calendar.isDate(date, inSameDayAs: selectedDate)
        let isCurrentDay = isToday(date)
        let dayNumber = calendar.component(.day, from: date)
        let weekdayLabel = shortWeekdayString(from: date)
        let entry = entryForDate(date)

        return Button(action: {
            selectDateWithHaptics(date)
        }) {
            VStack(spacing: 4) {
                Text(weekdayLabel)
                    .font(Typography.caption2Medium)
                    .foregroundStyle(isSelected ? AnnoTheme.narthex : (isCurrentDay ? AnnoTheme.goldLeaf : AnnoTheme.incense))

                Text("\(dayNumber)")
                    .font(Typography.captionBold.monospacedDigit())
                    .foregroundStyle(isSelected ? AnnoTheme.narthex : AnnoTheme.vellum)

                // Liturgical indicator dot
                if let entry = entry {
                    Circle()
                        .fill(isSelected ? AnnoTheme.narthex : AnnoTheme.liturgicalColor(named: entry.liturgical.color))
                        .frame(width: 4, height: 4)
                } else {
                    Circle()
                        .fill(Color.clear)
                        .frame(width: 4, height: 4)
                }
            }
            .frame(width: 46, height: 62)
            .background(
                RoundedRectangle(cornerRadius: 12, style: .continuous)
                    .fill(isSelected ? AnnoTheme.goldLeaf : AnnoTheme.narthex)
            )
            .overlay(
                RoundedRectangle(cornerRadius: 12, style: .continuous)
                    .strokeBorder(
                        isSelected
                            ? AnnoTheme.gilt
                            : (isCurrentDay ? AnnoTheme.goldLeaf.opacity(0.8) : AnnoTheme.ash),
                        lineWidth: isSelected || isCurrentDay ? 1.5 : 1
                    )
            )
            .shadow(
                color: isSelected ? AnnoTheme.goldLeaf.opacity(0.35) : Color.clear,
                radius: 6,
                y: 2
            )
            .scaleEffect(isSelected ? 1.05 : 1.0)
            .animation(.spring(response: 0.25, dampingFraction: 0.7), value: isSelected)
        }
        .buttonStyle(.plain)
    }

    // MARK: - Multi-Calendar Conversions Strip

    private var multiCalendarConversionsStrip: some View {
        let conversions = resolvedCalendarConversions(for: selectedDate)

        return VStack(alignment: .leading, spacing: 8) {
            HStack(spacing: 6) {
                Image(systemName: "globe.europe.africa.fill")
                    .font(Typography.caption2)
                    .foregroundStyle(AnnoTheme.goldLeaf)

                Text(language == .vietnamese ? "Đồng Bộ Đa Lịch Thánh" : "Multi-Calendar Synchronizations")
                    .font(Typography.caption2Bold)
                    .foregroundStyle(AnnoTheme.incense)
                    .textCase(.uppercase)
                    .tracking(1.2)
            }

            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 8) {
                    calendarPill(
                        title: language == .vietnamese ? "Lịch Julian" : "Julian",
                        value: conversions.julian,
                        symbol: "J"
                    )
                    calendarPill(
                        title: language == .vietnamese ? "Lịch Do Thái" : "Hebrew",
                        value: conversions.hebrew,
                        symbol: "H"
                    )
                    calendarPill(
                        title: language == .vietnamese ? "Lịch Hồi Giáo" : "Islamic (Umm al-Qura)",
                        value: conversions.islamic,
                        symbol: "I"
                    )
                    calendarPill(
                        title: language == .vietnamese ? "Lịch Coptic" : "Coptic",
                        value: conversions.coptic,
                        symbol: "C"
                    )
                    calendarPill(
                        title: language == .vietnamese ? "Lịch Ethiopia" : "Ethiopian",
                        value: conversions.ethiopian,
                        symbol: "E"
                    )
                }
                .padding(.horizontal, 2)
            }
        }
        .padding(10)
        .background(
            RoundedRectangle(cornerRadius: 12, style: .continuous)
                .fill(AnnoTheme.narthex.opacity(0.8))
                .overlay(
                    RoundedRectangle(cornerRadius: 12, style: .continuous)
                        .strokeBorder(AnnoTheme.ash.opacity(0.6), lineWidth: 0.8)
                )
        )
    }

    private func calendarPill(title: String, value: String, symbol: String) -> some View {
        VStack(alignment: .leading, spacing: 3) {
            HStack(spacing: 4) {
                Text(symbol)
                    .font(.system(size: 8, weight: .black))
                    .foregroundStyle(AnnoTheme.goldLeaf)
                    .padding(2)
                    .background(Circle().fill(AnnoTheme.choir))

                Text(title)
                    .font(.system(size: 9, weight: .semibold))
                    .foregroundStyle(AnnoTheme.incense)
            }

            Text(value)
                .font(Typography.caption2Medium)
                .foregroundStyle(AnnoTheme.vellum)
                .lineLimit(1)
        }
        .padding(.horizontal, 10)
        .padding(.vertical, 6)
        .background(AnnoTheme.choir)
        .clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))
        .overlay(
            RoundedRectangle(cornerRadius: 8, style: .continuous)
                .strokeBorder(AnnoTheme.ash, lineWidth: 0.6)
        )
    }

    // MARK: - Actions & Haptics

    private func selectDateWithHaptics(_ date: Date) {
        if !calendar.isDate(date, inSameDayAs: selectedDate) {
            Haptics.light()
            selectedDate = date
            onSelectDate?(date)
        }
    }

    private func triggerHapticFeedback(for date: Date) {
        if let last = lastHapticDate {
            if !calendar.isDate(date, inSameDayAs: last) {
                Haptics.light()
                lastHapticDate = date
            }
        } else {
            Haptics.light()
            lastHapticDate = date
        }
    }

    private func stepDate(by days: Int) {
        if let newDate = calendar.date(byAdding: .day, value: days, to: selectedDate) {
            selectDateWithHaptics(newDate)
        }
    }

    private func jumpToToday() {
        let today = Date()
        selectDateWithHaptics(today)
    }

    // MARK: - Date Helpers

    private func generateDateList() {
        let anchor = selectedDate
        var list: [Date] = []
        for offset in -dayRange...dayRange {
            if let date = calendar.date(byAdding: .day, value: offset, to: anchor) {
                list.append(date)
            }
        }
        dateList = list
    }

    private func dateIdentifier(for date: Date) -> String {
        isoFormatter.string(from: date)
    }

    private func isToday(_ date: Date) -> Bool {
        calendar.isDateInToday(date)
    }

    private func entryForDate(_ date: Date) -> AnnoEntry? {
        let key = isoFormatter.string(from: date)
        return entries.first(where: { $0.date == key })
    }

    private func monthYearString(from date: Date) -> String {
        let f = DateFormatter()
        f.locale = Locale(identifier: language == .vietnamese ? "vi_VN" : "en_US")
        f.calendar = calendar
        f.dateFormat = language == .vietnamese ? "MMMM 'năm' yyyy" : "MMMM yyyy"
        return f.string(from: date)
    }

    private func fullWeekdayDateString(from date: Date) -> String {
        let f = DateFormatter()
        f.locale = Locale(identifier: language == .vietnamese ? "vi_VN" : "en_US")
        f.calendar = calendar
        f.dateFormat = language == .vietnamese ? "EEEE, d 'tháng' M" : "EEEE, MMMM d"
        return f.string(from: date)
    }

    private func shortWeekdayString(from date: Date) -> String {
        let f = DateFormatter()
        f.locale = Locale(identifier: language == .vietnamese ? "vi_VN" : "en_US")
        f.calendar = calendar
        f.dateFormat = "EEE"
        return f.string(from: date).uppercased()
    }

    // MARK: - Calendar Conversions Resolver

    private func resolvedCalendarConversions(for date: Date) -> (
        julian: String,
        hebrew: String,
        islamic: String,
        coptic: String,
        ethiopian: String
    ) {
        if let entry = entryForDate(date) {
            return (
                julian: entry.calendars.julian,
                hebrew: entry.calendars.hebrew,
                islamic: entry.calendars.islamicUmmAlQura,
                coptic: entry.calendars.coptic,
                ethiopian: entry.calendars.ethiopian
            )
        }

        // Fallback calendar math calculation for dates outside bundle
        let comps = calendar.dateComponents([.year, .month, .day], from: date)
        let day = comps.day ?? 1
        let month = comps.month ?? 1
        let year = comps.year ?? 2026

        // Julian is ~13 days behind Gregorian in 20th-21st centuries
        let julianDay = max(1, day - 13)
        let julianStr = "\(julianDay) (O.S.)"

        return (
            julian: "\(julianStr), \(year)",
            hebrew: "Calculated (\(year + 3760))",
            islamic: "Umm al-Qura (\(year - 579) AH)",
            coptic: "Anno Martyrum (\(year - 284) AM)",
            ethiopian: "Incar. (\(year - 8))"
        )
    }
}

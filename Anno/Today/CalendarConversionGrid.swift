import SwiftUI

struct CalendarConversionGrid: View {
    let calendars: CalendarConversions

    private var rows: [(String, String)] {
        [
            ("Julian", calendars.julian),
            ("Hebrew", calendars.hebrew),
            ("Umm al-Qura", calendars.islamicUmmAlQura),
            ("Coptic", calendars.coptic),
            ("Ethiopian", calendars.ethiopian)
        ]
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Sacred calendars")
                .font(.headline)
                .foregroundStyle(AnnoTheme.goldLeaf)

            LazyVGrid(columns: [GridItem(.adaptive(minimum: 128), spacing: 10)], alignment: .leading, spacing: 10) {
                ForEach(rows, id: \.0) { label, value in
                    VStack(alignment: .leading, spacing: 3) {
                        Text(label)
                            .font(.caption)
                            .foregroundStyle(AnnoTheme.incense)
                        Text(value)
                            .font(.callout.monospacedDigit())
                            .foregroundStyle(AnnoTheme.vellum)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                    .padding(10)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(AnnoTheme.narthex)
                    .clipShape(RoundedRectangle(cornerRadius: 8))
                }
            }
        }
        .annoCard()
    }
}

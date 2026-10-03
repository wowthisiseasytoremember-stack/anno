import SwiftUI

struct SettingsView: View {
    @Binding var language: LanguageMode
    @Environment(\.dismiss) private var dismiss

    private var sectionHeaderColor: Color { AnnoTheme.goldLeaf }

    var body: some View {
        NavigationStack {
            List {
                Section {
                    Picker(
                        language == .vietnamese ? "Ngôn ngữ" : "Language",
                        selection: $language
                    ) {
                        Text("English").tag(LanguageMode.english)
                        Text("Tiếng Việt").tag(LanguageMode.vietnamese)
                    }
                    .foregroundStyle(AnnoTheme.vellum)
                    .listRowBackground(AnnoTheme.choir)
                } header: {
                    sectionHeader(language == .vietnamese ? "NGÔN NGỮ" : "LANGUAGE")
                } footer: {
                    Text(language == .vietnamese
                         ? "Anno v1 ưu tiên tiếng Anh; hỗ trợ tiếng Việt bắt đầu từ các lễ trọng và nội dung đã được biên soạn."
                         : "Anno v1 is English-first; Vietnamese support begins with major feasts and content that has been prepared.")
                        .foregroundStyle(AnnoTheme.incense)
                        .font(Typography.captionSerif)
                }

                Section {
                    infoRow(
                        icon: "calendar",
                        title: language == .vietnamese ? "Nội dung" : "Content",
                        detail: language == .vietnamese ? "Phụng vụ Công giáo hằng ngày" : "Daily Catholic devotional"
                    )
                    infoRow(
                        icon: "map",
                        title: language == .vietnamese ? "Hành hương" : "Pilgrimage",
                        detail: language == .vietnamese ? "5 tuyến đường chủ lực" : "5 flagship routes"
                    )
                    infoRow(
                        icon: "scroll",
                        title: language == .vietnamese ? "Phiên bản" : "Version",
                        detail: "1.0"
                    )
                } header: {
                    sectionHeader(language == .vietnamese ? "ANNO V1" : "ANNO V1")
                }

                Section {
                    VStack(spacing: 8) {
                        Image(systemName: "cross")
                            .font(Typography.title2BoldSerif)
                            .foregroundStyle(AnnoTheme.goldLeaf.opacity(0.4))

                        Text("Anno")
                            .font(Typography.headlineSerif)
                            .foregroundStyle(AnnoTheme.incense)

                        Text(language == .vietnamese
                             ? "Mỗi ngày kể từ Nhập Thể đều đã được đánh số."
                             : "Every day since the Incarnation has been numbered.")
                            .font(Typography.captionSerif)
                            .foregroundStyle(AnnoTheme.incense.opacity(0.7))
                            .multilineTextAlignment(.center)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 16)
                    .listRowBackground(AnnoTheme.clearRow)
                }
            }
            .scrollContentBackground(.hidden)
            .background(AnnoTheme.narthex)
            .navigationTitle(language == .vietnamese ? "Cài đặt" : "Settings")
            .navigationBarTitleDisplayMode(.inline)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .toolbarBackground(AnnoTheme.narthex, for: .navigationBar)
            .toolbarBackground(.visible, for: .navigationBar)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        Haptics.light()
                        dismiss()
                    } label: {
                        Image(systemName: "xmark.circle.fill")
                            .foregroundStyle(AnnoTheme.incense)
                            .font(Typography.title3ItalicSerif)
                    }
                    .accessibilityLabel(language == .vietnamese ? "Đóng" : "Close")
                }
            }
        }
    }

    private func sectionHeader(_ title: String) -> some View {
        Text(title)
            .foregroundStyle(sectionHeaderColor)
            .font(Typography.captionSemiboldSerif)
    }

    private func infoRow(icon: String, title: String, detail: String) -> some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .foregroundStyle(AnnoTheme.goldLeaf)
                .frame(width: 24)
                .accessibilityHidden(true)

            Text(title)
                .foregroundStyle(AnnoTheme.vellum)

            Spacer(minLength: 12)

            Text(detail)
                .font(Typography.captionSerif)
                .foregroundStyle(AnnoTheme.incense)
                .multilineTextAlignment(.trailing)
        }
        .listRowBackground(AnnoTheme.choir)
        .accessibilityElement(children: .combine)
    }
}

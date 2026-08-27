import SwiftUI

struct SettingsView: View {
    @Binding var language: LanguageMode
    @Environment(\.dismiss) private var dismiss

    @State private var notificationsEnabled = true
    @State private var homeTradition: HomeTradition = .roman

    private var sectionHeaderColor: Color { AnnoTheme.goldLeaf }

    var body: some View {
        NavigationStack {
            List {
                // MARK: - Language
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
                    Text(language == .vietnamese ? "NGÔN NGỮ" : "LANGUAGE")
                        .foregroundStyle(sectionHeaderColor)
                        .font(Typography.captionSemiboldSerif)
                }

                // MARK: - Tradition
                Section {
                    Picker(
                        language == .vietnamese ? "Truyền thống chính" : "Home tradition",
                        selection: $homeTradition
                    ) {
                        ForEach(HomeTradition.allCases) { tradition in
                            Text(tradition.displayName(language: language))
                                .tag(tradition)
                        }
                    }
                    .foregroundStyle(AnnoTheme.vellum)
                    .listRowBackground(AnnoTheme.choir)
                } header: {
                    Text(language == .vietnamese ? "TRUYỀN THỐNG" : "TRADITION")
                        .foregroundStyle(sectionHeaderColor)
                        .font(Typography.captionSemiboldSerif)
                } footer: {
                    Text(language == .vietnamese
                         ? "Chọn truyền thống để ưu tiên nội dung phụng vụ và thánh nhân."
                         : "Choose a tradition to prioritize liturgical content and saints.")
                        .foregroundStyle(AnnoTheme.incense)
                        .font(Typography.captionSerif)
                }

                // MARK: - Notifications
                Section {
                    Toggle(isOn: $notificationsEnabled) {
                        Label {
                            Text(language == .vietnamese ? "Nhắc nhở hằng ngày" : "Daily reminder")
                                .foregroundStyle(AnnoTheme.vellum)
                        } icon: {
                            Image(systemName: "bell.badge")
                                .foregroundStyle(AnnoTheme.goldLeaf)
                        }
                    }
                    .tint(AnnoTheme.goldLeaf)
                    .listRowBackground(AnnoTheme.choir)
                } header: {
                    Text(language == .vietnamese ? "THÔNG BÁO" : "NOTIFICATIONS")
                        .foregroundStyle(sectionHeaderColor)
                        .font(Typography.captionSemiboldSerif)
                }

                // MARK: - About
                Section {
                    aboutRow(
                        icon: "scroll",
                        title: language == .vietnamese ? "Giới thiệu Anno" : "About Anno",
                        detail: language == .vietnamese ? "Phiên bản 1.0" : "Version 1.0"
                    )

                    aboutRow(
                        icon: "envelope",
                        title: language == .vietnamese ? "Liên hệ" : "Contact",
                        detail: "hello@anno.app"
                    )

                    aboutRow(
                        icon: "doc.text",
                        title: language == .vietnamese ? "Chính sách bảo mật" : "Privacy Policy",
                        detail: nil
                    )

                    aboutRow(
                        icon: "doc.plaintext",
                        title: language == .vietnamese ? "Điều khoản sử dụng" : "Terms of Use",
                        detail: nil
                    )
                } header: {
                    Text(language == .vietnamese ? "THÔNG TIN" : "ABOUT")
                        .foregroundStyle(sectionHeaderColor)
                        .font(Typography.captionSemiboldSerif)
                }

                // MARK: - Footer
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
                            .foregroundStyle(AnnoTheme.incense.opacity(0.6))
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
                }
            }
        }
    }

    private func aboutRow(icon: String, title: String, detail: String?) -> some View {
        HStack {
            Label {
                Text(title)
                    .foregroundStyle(AnnoTheme.vellum)
            } icon: {
                Image(systemName: icon)
                    .foregroundStyle(AnnoTheme.goldLeaf)
                    .frame(width: 24)
            }

            Spacer()

            if let detail {
                Text(detail)
                    .font(Typography.captionSerif)
                    .foregroundStyle(AnnoTheme.incense)
            } else {
                Image(systemName: "chevron.right")
                    .font(Typography.captionBold)
                    .foregroundStyle(AnnoTheme.incense)
            }
        }
        .listRowBackground(AnnoTheme.choir)
    }
}

// MARK: - Home Tradition

enum HomeTradition: String, CaseIterable, Identifiable {
    case roman = "roman"
    case byzantine = "byzantine"
    case coptic = "coptic"
    case syriac = "syriac"

    var id: String { rawValue }

    func displayName(language: LanguageMode) -> String {
        switch self {
        case .roman:
            return language == .vietnamese ? "Công giáo La Mã" : "Roman Catholic"
        case .byzantine:
            return language == .vietnamese ? "Đông Phương Byzantine" : "Byzantine"
        case .coptic:
            return language == .vietnamese ? "Cốp-tích" : "Coptic"
        case .syriac:
            return language == .vietnamese ? "Syriac" : "Syriac"
        }
    }
}

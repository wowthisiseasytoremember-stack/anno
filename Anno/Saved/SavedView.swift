import SwiftUI

struct SavedView: View {
    let language: LanguageMode
    @State private var showingPaywall = false

    var body: some View {
        NavigationStack {
            VStack(alignment: .leading, spacing: 18) {
                Image(systemName: "bookmark")
                    .font(.system(size: 34, weight: .light))
                    .foregroundStyle(AnnoTheme.goldLeaf)

                Text(language == .vietnamese ? "Bộ sưu tập đã lưu" : "Saved collections")
                    .font(.title2.weight(.semibold))
                    .foregroundStyle(AnnoTheme.vellum)

                Text(language == .vietnamese ? "Lưu ngày, tác phẩm và địa điểm hành hương để trở lại sau." : "Save days, artwork, and pilgrimage places to revisit.")
                    .foregroundStyle(AnnoTheme.incense)
                    .fixedSize(horizontal: false, vertical: true)

                Button {
                    showingPaywall = true
                } label: {
                    Label(language == .vietnamese ? "Mở khóa bộ sưu tập" : "Unlock collections", systemImage: "lock.open")
                }
                .buttonStyle(.borderedProminent)
                .tint(AnnoTheme.goldLeaf)
                .foregroundStyle(AnnoTheme.narthex)

                Spacer()
            }
            .padding(20)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(AnnoTheme.narthex.ignoresSafeArea())
            .navigationTitle(language == .vietnamese ? "Đã lưu" : "Saved")
            .sheet(isPresented: $showingPaywall) {
                ArchivePaywallView(language: language)
            }
        }
    }
}

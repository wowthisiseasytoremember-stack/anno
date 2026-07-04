import SwiftUI

struct ArchivePaywallView: View {
    let language: LanguageMode

    private var copy: ProductCopy {
        ProductCopy(language: language)
    }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    Text(copy.title)
                        .font(.largeTitle.weight(.semibold))
                        .foregroundStyle(AnnoTheme.vellum)
                        .fixedSize(horizontal: false, vertical: true)

                    Text(copy.subtitle)
                        .font(.title3)
                        .foregroundStyle(AnnoTheme.incense)
                        .fixedSize(horizontal: false, vertical: true)

                    VStack(alignment: .leading, spacing: 12) {
                        ForEach(copy.benefits, id: \.self) { benefit in
                            Label(benefit, systemImage: "checkmark.seal")
                                .foregroundStyle(AnnoTheme.vellum)
                                .fixedSize(horizontal: false, vertical: true)
                        }
                    }
                    .annoCard()

                    Button(copy.primaryPlan) {}
                        .buttonStyle(.borderedProminent)
                        .tint(AnnoTheme.goldLeaf)
                        .foregroundStyle(AnnoTheme.narthex)

                    Button(copy.secondaryPlan) {}
                        .buttonStyle(.bordered)
                        .tint(AnnoTheme.goldLeaf)

                    HStack {
                        Button("Restore") {}
                        Spacer()
                        Button("Terms") {}
                        Spacer()
                        Button("Privacy") {}
                    }
                    .font(.caption)
                    .foregroundStyle(AnnoTheme.incense)
                }
                .padding(20)
            }
            .background(AnnoTheme.narthex.ignoresSafeArea())
            .navigationTitle("Anno Plus")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

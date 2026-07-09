import SwiftUI

struct ArchivePaywallView: View {
    let language: LanguageMode
    @Environment(\.dismiss) private var dismiss

    @State private var appeared = false
    @State private var heroGlow: Double = 0.5

    private var copy: ProductCopy {
        ProductCopy(language: language)
    }

    /// Maps each benefit (by index) to a contextual SF Symbol.
    private let benefitIcons: [String] = [
        "magnifyingglass",
        "mappin.and.ellipse",
        "paintpalette",
        "waveform",
        "bookmark.fill",
        "doc.text.magnifyingglass"
    ]

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 0) {
                    heroSection
                    benefitsSection
                    pricingSection
                    legalFooter
                }
                .padding(.bottom, 32)
            }
            .scrollBounceBehavior(.basedOnSize)
            .background {
                ZStack {
                    AnnoTheme.narthex.ignoresSafeArea()

                    // Subtle warm radial from top
                    RadialGradient(
                        gradient: Gradient(colors: [
                            AnnoTheme.goldLeaf.opacity(0.08),
                            AnnoTheme.narthex.opacity(0.0)
                        ]),
                        center: .top,
                        startRadius: 0,
                        endRadius: 350
                    )
                    .ignoresSafeArea(edges: .top)
                }
            }
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        dismiss()
                    } label: {
                        Image(systemName: "xmark.circle.fill")
                            .font(.title3)
                            .symbolRenderingMode(.hierarchical)
                            .foregroundStyle(AnnoTheme.incense)
                    }
                    .accessibilityLabel(
                        language == .vietnamese ? "Đóng" : "Close"
                    )
                }
            }
            .onAppear {
                withAnimation(.easeOut(duration: 0.7)) {
                    appeared = true
                }
            }
        }
    }

    // MARK: - Hero Section

    private var heroSection: some View {
        VStack(spacing: 18) {
            ZStack {
                // Radial gold glow behind cross
                Circle()
                    .fill(
                        RadialGradient(
                            gradient: Gradient(colors: [
                                AnnoTheme.goldLeaf.opacity(heroGlow * 0.25),
                                AnnoTheme.goldLeaf.opacity(0.0)
                            ]),
                            center: .center,
                            startRadius: 5,
                            endRadius: 80
                        )
                    )
                    .frame(width: 160, height: 160)

                Image(systemName: "cross.fill")
                    .font(.system(size: 44, weight: .light))
                    .foregroundStyle(
                        LinearGradient(
                            colors: [AnnoTheme.goldLeaf, AnnoTheme.gilt],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
                    .shadow(color: AnnoTheme.goldLeaf.opacity(0.4), radius: 16, y: 4)
            }
            .onAppear {
                withAnimation(
                    .easeInOut(duration: 3.0)
                    .repeatForever(autoreverses: true)
                ) {
                    heroGlow = 1.0
                }
            }
            .accessibilityHidden(true)

            VStack(spacing: 10) {
                Text(copy.title)
                    .font(.largeTitle.weight(.bold))
                    .fontDesign(.serif)
                    .foregroundStyle(
                        LinearGradient(
                            colors: [AnnoTheme.goldLeaf, AnnoTheme.gilt],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .multilineTextAlignment(.center)
                    .fixedSize(horizontal: false, vertical: true)
                    .accessibilityAddTraits(.isHeader)

                Text(copy.subtitle)
                    .font(.subheadline)
                    .fontDesign(.serif)
                    .foregroundStyle(AnnoTheme.incense)
                    .multilineTextAlignment(.center)
                    .fixedSize(horizontal: false, vertical: true)
                    .lineSpacing(3)
            }
        }
        .padding(.horizontal, 24)
        .padding(.top, 28)
        .padding(.bottom, 8)
        .opacity(appeared ? 1 : 0)
        .offset(y: appeared ? 0 : 16)
    }

    // MARK: - Benefits Section

    private var benefitsSection: some View {
        VStack(spacing: 0) {
            ForEach(Array(copy.benefits.enumerated()), id: \.offset) { index, benefit in
                benefitRow(
                    icon: benefitIcons[safe: index] ?? "checkmark.seal",
                    text: benefit
                )
                .opacity(appeared ? 1 : 0)
                .offset(y: appeared ? 0 : 12)
                .animation(
                    .spring(response: 0.5, dampingFraction: 0.8)
                        .delay(0.08 * Double(index) + 0.2),
                    value: appeared
                )

                if index < copy.benefits.count - 1 {
                    Divider()
                        .background(AnnoTheme.ash)
                        .padding(.leading, 56)
                }
            }
        }
        .annoCard()
        .padding(.horizontal, 20)
        .padding(.top, 20)
    }

    private func benefitRow(icon: String, text: String) -> some View {
        HStack(spacing: 14) {
            Image(systemName: icon)
                .font(.body.weight(.medium))
                .foregroundStyle(AnnoTheme.goldLeaf)
                .frame(width: 32, height: 32)
                .accessibilityHidden(true)

            Text(text)
                .font(.subheadline)
                .fontDesign(.serif)
                .foregroundStyle(AnnoTheme.vellum)
                .fixedSize(horizontal: false, vertical: true)

            Spacer()
        }
        .padding(.vertical, 12)
        .accessibilityElement(children: .combine)
        .accessibilityLabel(text)
    }

    // MARK: - Pricing Section

    private var pricingSection: some View {
        VStack(spacing: 12) {
            // Primary CTA — full-width gold gradient
            Button {
                // StoreKit purchase action
            } label: {
                VStack(spacing: 4) {
                    Text(copy.primaryPlan)
                        .font(.headline)
                        .fontDesign(.serif)

                    Text(language == .vietnamese ? "Tiết kiệm nhất" : "Best value")
                        .font(.caption2.weight(.medium))
                        .textCase(.uppercase)
                        .tracking(1.0)
                        .opacity(0.8)
                }
                .foregroundStyle(AnnoTheme.narthex)
                .frame(maxWidth: .infinity)
                .padding(.vertical, 16)
                .background(
                    LinearGradient(
                        colors: [AnnoTheme.goldLeaf, AnnoTheme.gilt],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
                .shadow(color: AnnoTheme.goldLeaf.opacity(0.3), radius: 16, y: 6)
            }
            .buttonStyle(.plain)
            .accessibilityLabel(
                language == .vietnamese
                    ? "Gói hằng năm, bốn mươi chín đô la chín mươi chín xu mỗi năm, tiết kiệm nhất"
                    : "Annual plan, forty-nine dollars and ninety-nine cents per year, best value"
            )

            // Secondary CTA — bordered outline
            Button {
                // StoreKit purchase action
            } label: {
                Text(copy.secondaryPlan)
                    .font(.subheadline.weight(.medium))
                    .fontDesign(.serif)
                    .foregroundStyle(AnnoTheme.goldLeaf)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 14)
                    .background(
                        RoundedRectangle(cornerRadius: 12, style: .continuous)
                            .strokeBorder(AnnoTheme.goldLeaf.opacity(0.4), lineWidth: 1)
                    )
            }
            .buttonStyle(.plain)
            .accessibilityLabel(
                language == .vietnamese
                    ? "Gói hằng tháng, năm đô la chín mươi chín xu mỗi tháng"
                    : "Monthly plan, five dollars and ninety-nine cents per month"
            )
        }
        .padding(.horizontal, 20)
        .padding(.top, 28)
        .opacity(appeared ? 1 : 0)
        .animation(.easeOut(duration: 0.6).delay(0.6), value: appeared)
    }

    // MARK: - Legal Footer

    private var legalFooter: some View {
        VStack(spacing: 12) {
            // Restore purchases
            Button {
                // Restore action
            } label: {
                Text(language == .vietnamese ? "Khôi phục giao dịch" : "Restore Purchases")
                    .font(.caption.weight(.medium))
                    .foregroundStyle(AnnoTheme.incense)
            }
            .buttonStyle(.plain)
            .accessibilityLabel(
                language == .vietnamese
                    ? "Khôi phục giao dịch mua trước đó"
                    : "Restore previous purchases"
            )

            // Terms & Privacy
            HStack(spacing: 20) {
                Button {
                    // Terms action
                } label: {
                    Text(language == .vietnamese ? "Điều khoản" : "Terms")
                        .font(.caption2)
                        .foregroundStyle(AnnoTheme.incense.opacity(0.7))
                }
                .buttonStyle(.plain)

                Text("·")
                    .font(.caption2)
                    .foregroundStyle(AnnoTheme.incense.opacity(0.4))
                    .accessibilityHidden(true)

                Button {
                    // Privacy action
                } label: {
                    Text(language == .vietnamese ? "Quyền riêng tư" : "Privacy")
                        .font(.caption2)
                        .foregroundStyle(AnnoTheme.incense.opacity(0.7))
                }
                .buttonStyle(.plain)
            }

            Text(language == .vietnamese
                 ? "Thanh toán sẽ được tính vào tài khoản Apple ID của bạn."
                 : "Payment will be charged to your Apple ID account.")
                .font(.caption2)
                .foregroundStyle(AnnoTheme.incense.opacity(0.5))
                .multilineTextAlignment(.center)
                .fixedSize(horizontal: false, vertical: true)
        }
        .padding(.horizontal, 20)
        .padding(.top, 24)
        .opacity(appeared ? 1 : 0)
        .animation(.easeOut(duration: 0.5).delay(0.8), value: appeared)
    }
}

// MARK: - Safe Array Subscript

private extension Array {
    subscript(safe index: Index) -> Element? {
        indices.contains(index) ? self[index] : nil
    }
}

// MARK: - Preview

#Preview {
    ArchivePaywallView(language: .english)
        .preferredColorScheme(.dark)
}

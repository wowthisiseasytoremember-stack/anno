//  WelcomeView.swift
//  Anno
//
//  A gentle first-run welcome shown once.

import SwiftUI

struct WelcomeView: View {
    var onContinue: () -> Void
    @State private var appear = false

    var body: some View {
        ZStack {
            AnnoTheme.narthex.ignoresSafeArea()

            VStack(spacing: 24) {
                Spacer()

                // Anno mark / cross icon
                Image(systemName: "cross.case.fill")
                    .font(.system(size: 60, weight: .light))
                    .foregroundStyle(AnnoTheme.goldLeaf)
                    .opacity(appear ? 1 : 0)
                    .scaleEffect(appear ? 1 : 0.8)

                VStack(spacing: 12) {
                    Text("Welcome to Anno")
                        .font(AnnoTheme.display(34, weight: .semibold))
                        .foregroundStyle(AnnoTheme.vellum)
                        .multilineTextAlignment(.center)

                    Rectangle()
                        .fill(AnnoTheme.goldLeaf)
                        .frame(width: 100, height: 1)

                    Text("A daily companion for the liturgical year — Scripture, saints, sacred places, and pilgrimage paths in English and Vietnamese.")
                        .font(AnnoTheme.body(16))
                        .foregroundStyle(AnnoTheme.incense)
                        .multilineTextAlignment(.center)
                        .padding(.horizontal, 28)
                }
                .opacity(appear ? 1 : 0)
                .offset(y: appear ? 0 : 16)

                Spacer()

                VStack(spacing: 14) {
                    featureRow(icon: "sun.horizon.fill", title: "Daily Office", subtitle: "Readings for every day of the Church year")
                    featureRow(icon: "map.fill", title: "Sacred Geography", subtitle: "Pilgrimage routes, sanctuaries, and holy sites")
                    featureRow(icon: "textformat.alt", title: "Bilingual EN / VI", subtitle: "Every text in both languages")
                }
                .padding(.horizontal, 28)
                .opacity(appear ? 1 : 0)
                .offset(y: appear ? 0 : 24)

                Spacer()

                Button {
                    Haptics.soft()
                    onContinue()
                } label: {
                    Text("Begin")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(AnnoGildedButtonStyle(prominent: true))
                .padding(.horizontal, 28)
                .padding(.bottom, 20)
                .opacity(appear ? 1 : 0)
            }
        }
        .presentationBackground(.clear)
        .onAppear {
            withAnimation(.spring(response: 0.8, dampingFraction: 0.8)) { appear = true }
        }
    }

    private func featureRow(icon: String, title: String, subtitle: String) -> some View {
        HStack(spacing: 14) {
            Image(systemName: icon)
                .font(.system(size: 17))
                .foregroundStyle(AnnoTheme.goldLeaf)
                .frame(width: 40, height: 40)
                .background(Circle().fill(AnnoTheme.choir))
                .overlay(Circle().strokeBorder(AnnoTheme.ash, lineWidth: 0.8))
            VStack(alignment: .leading, spacing: 2) {
                Text(title).font(AnnoTheme.body(15, weight: .semibold)).foregroundStyle(AnnoTheme.vellum)
                Text(subtitle).font(AnnoTheme.caption(12)).foregroundStyle(AnnoTheme.incense)
            }
            Spacer()
        }
    }
}

/// Button style matching Anno's gilded aesthetic
struct AnnoGildedButtonStyle: ButtonStyle {
    var prominent: Bool = false

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(AnnoTheme.body(17, weight: .semibold))
            .foregroundStyle(prominent ? AnnoTheme.narthex : AnnoTheme.goldLeaf)
            .padding(.vertical, 14)
            .frame(maxWidth: .infinity)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(prominent ? AnnoTheme.goldLeaf : AnnoTheme.choir)
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(AnnoTheme.ash, lineWidth: 1)
                    )
            )
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .animation(.easeOut(duration: 0.1), value: configuration.isPressed)
    }
}

#Preview {
    WelcomeView(onContinue: {})
        .preferredColorScheme(.dark)
}
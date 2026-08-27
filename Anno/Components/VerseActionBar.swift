//  VerseActionBar.swift
//  Anno
//
//  Reusable action row for a verse: bookmark toggle and share.

import SwiftUI
import SwiftData

struct VerseActionBar: View {
    let reference: VerseReference
    let text: String
    var tint: Color = AnnoTheme.rose

    @Environment(\.modelContext) private var context
    @State private var isBookmarked = false
    @State private var shareImage: ShareableImage?

    var body: some View {
        HStack(spacing: 12) {
            bookmarkButton

            if let shareImage {
                ShareLink(
                    item: shareImage,
                    preview: SharePreview(reference.displayString, image: shareImage.image)
                ) {
                    actionIcon("square.and.arrow.up")
                }
                .simultaneousGesture(TapGesture().onEnded { Haptics.light() })
            } else {
                actionIcon("square.and.arrow.up").opacity(0.4)
            }
        }
        .onAppear {
            isBookmarked = BookmarkActions.exists(reference, in: context)
            prepareShareImage()
        }
    }

    private var bookmarkButton: some View {
        Button {
            withAnimation(.spring(response: 0.35, dampingFraction: 0.55)) {
                isBookmarked = BookmarkActions.toggle(reference: reference, text: text, in: context)
            }
            if isBookmarked { Haptics.success() } else { Haptics.light() }
        } label: {
            Image(systemName: isBookmarked ? "heart.fill" : "heart")
                .font(Typography.subheadlineSemibold)
                .foregroundStyle(isBookmarked ? AnyShapeStyle(tint) : AnyShapeStyle(AnnoTheme.incense))
                .symbolEffect(.bounce, value: isBookmarked)
                .frame(width: 42, height: 42)
                .background(Circle().fill(AnnoTheme.choir))
                .overlay(Circle().strokeBorder(AnnoTheme.goldLeaf.opacity(0.25), lineWidth: 0.8))
        }
        .accessibilityLabel(isBookmarked ? "Remove bookmark" : "Add bookmark")
        .accessibilityHint("Saves this verse to your collection")
    }

    private func actionIcon(_ name: String) -> some View {
        Image(systemName: name)
            .font(Typography.subheadlineSemibold)
            .foregroundStyle(AnnoTheme.incense)
            .frame(width: 42, height: 42)
            .background(Circle().fill(AnnoTheme.choir))
            .overlay(Circle().strokeBorder(AnnoTheme.goldLeaf.opacity(0.25), lineWidth: 0.8))
    }

    private func prepareShareImage() {
        guard shareImage == nil,
              let ui = ShareCardRenderer.render(verse: text, reference: reference.displayString) else { return }
        shareImage = ShareableImage(uiImage: ui, caption: "\(text)\n\n— \(reference.displayString)")
    }
}
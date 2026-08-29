//  SacredArtCanvas.swift
//  Anno
//
//  Task C.5.1: High-Resolution Zoomable Sacred Art Canvas.
//  Features:
//  - Interactive pinch-to-zoom (MagnificationGesture) up to 6.0x
//  - Pan navigation (DragGesture) with rubber-band bounds clamping
//  - Double-tap gesture for instant 1.0x <-> 2.5x toggle
//  - High-resolution async loading state with shimmer placeholder and error retry
//  - Expandable bottom sheet displaying bilingual theological commentary & provenance
//  - Tactile haptics and floating HUD controls

import SwiftUI
import Combine

// MARK: - Sacred Art Image Loader

@MainActor
final class SacredArtImageCache: ObservableObject {
    static let shared = SacredArtImageCache()

    private var memoryCache = NSCache<NSURL, UIImage>()

    init() {
        memoryCache.countLimit = 64
        memoryCache.totalCostLimit = 100 * 1024 * 1024 // 100 MB
    }

    func image(for url: URL) -> UIImage? {
        memoryCache.object(forKey: url as NSURL)
    }

    func insertImage(_ image: UIImage, for url: URL) {
        memoryCache.setObject(image, forKey: url as NSURL)
    }
}

// MARK: - SacredArtCanvas View

struct SacredArtCanvas: View {
    let dossier: ArtDossier
    @Binding var language: LanguageMode
    var onDismiss: (() -> Void)?

    // MARK: - Gesture & Zoom State
    @State private var currentScale: CGFloat = 1.0
    @State private var gestureScale: CGFloat = 1.0
    @State private var currentOffset: CGSize = .zero
    @State private var gestureOffset: CGSize = .zero

    // MARK: - UI & Commentary Sheet State
    @State private var isCommentaryExpanded: Bool = false
    @State private var isControlsVisible: Bool = true
    @State private var loadedImage: UIImage?
    @State private var isLoadingHighRes: Bool = true
    @State private var loadFailed: Bool = false

    private let minScale: CGFloat = 1.0
    private let maxScale: CGFloat = 6.0
    private let doubleTapZoomScale: CGFloat = 2.5

    private var effectiveScale: CGFloat {
        max(minScale, min(maxScale, currentScale * gestureScale))
    }

    private var effectiveOffset: CGSize {
        CGSize(
            width: currentOffset.width + gestureOffset.width,
            height: currentOffset.height + gestureOffset.height
        )
    }

    // MARK: - Initializers

    init(
        dossier: ArtDossier,
        language: Binding<LanguageMode>,
        onDismiss: (() -> Void)? = nil
    ) {
        self.dossier = dossier
        self._language = language
        self.onDismiss = onDismiss
    }

    init(
        entry: AnnoEntry,
        language: Binding<LanguageMode>,
        onDismiss: (() -> Void)? = nil
    ) {
        self.dossier = ArtDossier(from: entry)
        self._language = language
        self.onDismiss = onDismiss
    }

    // MARK: - Body

    var body: some View {
        GeometryReader { geometry in
            ZStack(alignment: .bottom) {
                // 1. Dark Ecclesial Background
                AnnoTheme.narthex
                    .ignoresSafeArea()
                    .onTapGesture {
                        withAnimation(.easeInOut(duration: 0.25)) {
                            isControlsVisible.toggle()
                        }
                    }

                // 2. Interactive Zoomable Art Canvas
                zoomableImageLayer(in: geometry)

                // 3. Floating HUD Controls (Top & Floating Badges)
                if isControlsVisible {
                    topHUDControls
                        .transition(.opacity.combined(with: .move(edge: .top)))
                }

                // 4. Expandable Bottom Sheet with Bilingual Theological Commentary
                commentaryBottomSheet(in: geometry)
                    .transition(.move(edge: .bottom).combined(with: .opacity))
            }
        }
        .task {
            await loadImageAsset()
        }
        .preferredColorScheme(.dark)
    }

    // MARK: - Zoomable Image Layer

    @ViewBuilder
    private func zoomableImageLayer(in geometry: GeometryProxy) -> some View {
        ZStack {
            if let image = loadedImage {
                Image(uiImage: image)
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .scaleEffect(effectiveScale)
                    .offset(effectiveOffset)
                    .simultaneousGesture(magnificationGesture(in: geometry))
                    .simultaneousGesture(panGesture(in: geometry))
                    .onTapGesture(count: 2) { location in
                        handleDoubleTap()
                    }
                    .onTapGesture(count: 1) {
                        withAnimation(.easeInOut(duration: 0.25)) {
                            isControlsVisible.toggle()
                        }
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else if loadFailed {
                errorRetryView
            } else {
                canvasShimmerPlaceholder
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    // MARK: - Gestures

    private func magnificationGesture(in geometry: GeometryProxy) -> some Gesture {
        MagnificationGesture()
            .onChanged { value in
                gestureScale = value
            }
            .onEnded { value in
                let newScale = max(minScale, min(maxScale, currentScale * value))
                withAnimation(AnnoTheme.canvasSpring) {
                    currentScale = newScale
                    gestureScale = 1.0
                    if newScale <= 1.0 {
                        currentOffset = .zero
                        gestureOffset = .zero
                    } else {
                        clampOffset(in: geometry)
                    }
                }
                Haptics.selection()
            }
    }

    private func panGesture(in geometry: GeometryProxy) -> some Gesture {
        DragGesture()
            .onChanged { value in
                if effectiveScale > 1.0 {
                    gestureOffset = value.translation
                }
            }
            .onEnded { value in
                if effectiveScale > 1.0 {
                    currentOffset.width += value.translation.width
                    currentOffset.height += value.translation.height
                    gestureOffset = .zero

                    withAnimation(AnnoTheme.canvasSpring) {
                        clampOffset(in: geometry)
                    }
                }
            }
    }

    private func handleDoubleTap() {
        Haptics.light()
        withAnimation(AnnoTheme.canvasSpring) {
            if effectiveScale > 1.1 {
                currentScale = 1.0
                gestureScale = 1.0
                currentOffset = .zero
                gestureOffset = .zero
            } else {
                currentScale = doubleTapZoomScale
                gestureScale = 1.0
            }
        }
    }

    private func clampOffset(in geometry: GeometryProxy) {
        guard effectiveScale > 1.0 else {
            currentOffset = .zero
            return
        }

        let maxOffsetX = max(0, (geometry.size.width * (effectiveScale - 1)) / 2)
        let maxOffsetY = max(0, (geometry.size.height * (effectiveScale - 1)) / 2)

        currentOffset.width = min(max(currentOffset.width, -maxOffsetX), maxOffsetX)
        currentOffset.height = min(max(currentOffset.height, -maxOffsetY), maxOffsetY)
    }

    // MARK: - Floating Top HUD

    private var topHUDControls: some View {
        VStack(spacing: 0) {
            HStack(spacing: 12) {
                // Dismiss / Close Button
                if let onDismiss = onDismiss {
                    Button(action: {
                        Haptics.light()
                        onDismiss()
                    }) {
                        Image(systemName: "xmark.circle.fill")
                            .font(Typography.iconTitle2)
                            .foregroundStyle(AnnoTheme.vellum, AnnoTheme.choir.opacity(0.8))
                            .background(Circle().fill(AnnoTheme.choir))
                    }
                    .buttonStyle(.plain)
                    .accessibilityLabel(language == .vietnamese ? "Đóng" : "Close")
                }

                Spacer()

                // Zoom Level Badge & Reset
                if effectiveScale > 1.05 {
                    Button(action: {
                        handleDoubleTap()
                    }) {
                        HStack(spacing: 4) {
                            Image(systemName: "arrow.counterclockwise")
                                .font(Typography.caption2Bold)
                            Text(String(format: "%.1fx", effectiveScale))
                                .font(Typography.captionBold.monospacedDigit())
                        }
                        .foregroundStyle(AnnoTheme.goldLeaf)
                        .padding(.horizontal, 10)
                        .padding(.vertical, 6)
                        .background(AnnoTheme.choir.opacity(0.85))
                        .clipShape(Capsule())
                        .overlay(Capsule().stroke(AnnoTheme.ash, lineWidth: 1))
                    }
                    .buttonStyle(.plain)
                }

                // Language Mode Selector
                Picker("Language", selection: $language) {
                    Text("EN").tag(LanguageMode.english)
                    Text("VI").tag(LanguageMode.vietnamese)
                }
                .pickerStyle(.segmented)
                .frame(width: 80)
                .tint(AnnoTheme.goldLeaf)

                // Info / Commentary Toggle
                Button(action: {
                    Haptics.light()
                    withAnimation(.spring(response: 0.35, dampingFraction: 0.8)) {
                        isCommentaryExpanded.toggle()
                    }
                }) {
                    Image(systemName: isCommentaryExpanded ? "info.circle.fill" : "info.circle")
                        .font(Typography.iconTitle)
                        .foregroundStyle(isCommentaryExpanded ? AnnoTheme.goldLeaf : AnnoTheme.vellum)
                        .padding(6)
                        .background(Circle().fill(AnnoTheme.choir.opacity(0.85)))
                        .overlay(Circle().stroke(AnnoTheme.ash, lineWidth: 1))
                }
                .buttonStyle(.plain)
                .accessibilityLabel(language == .vietnamese ? "Hồ sơ nghệ thuật" : "Art dossier info")
            }
            .padding(.horizontal, 20)
            .padding(.top, 16)

            Spacer()
        }
    }

    // MARK: - Commentary Bottom Sheet

    @ViewBuilder
    private func commentaryBottomSheet(in geometry: GeometryProxy) -> some View {
        VStack(spacing: 0) {
            // Drag Handle & Header Banner
            Button(action: {
                Haptics.light()
                withAnimation(.spring(response: 0.35, dampingFraction: 0.8)) {
                    isCommentaryExpanded.toggle()
                }
            }) {
                VStack(spacing: 8) {
                    Capsule()
                        .fill(AnnoTheme.incense.opacity(0.5))
                        .frame(width: 36, height: 4)
                        .padding(.top, 8)

                    HStack(alignment: .center, spacing: 10) {
                        VStack(alignment: .leading, spacing: 2) {
                            Text(dossier.title)
                                .font(Typography.headlineSerif)
                                .foregroundStyle(AnnoTheme.vellum)
                                .lineLimit(1)

                            Text("\(dossier.artist) · \(dossier.yearCreated)")
                                .font(Typography.captionSerif)
                                .foregroundStyle(AnnoTheme.incense)
                                .lineLimit(1)
                        }

                        Spacer()

                        Image(systemName: isCommentaryExpanded ? "chevron.down" : "chevron.up")
                            .font(Typography.subheadlineSemibold)
                            .foregroundStyle(AnnoTheme.goldLeaf)
                    }
                    .padding(.horizontal, 16)
                    .padding(.bottom, 10)
                }
                .frame(maxWidth: .infinity)
                .contentShape(Rectangle())
            }
            .buttonStyle(.plain)

            // Expanded Theological & Provenance Content
            if isCommentaryExpanded {
                ScrollView {
                    VStack(alignment: .leading, spacing: 16) {
                        // Feast Association
                        HStack(spacing: 6) {
                            Image(systemName: "cross.fill")
                                .font(Typography.caption2)
                                .foregroundStyle(AnnoTheme.goldLeaf)
                            Text(dossier.feastAssociation)
                                .font(Typography.captionSemiboldSerif)
                                .foregroundStyle(AnnoTheme.gilt)
                        }
                        .padding(.horizontal, 10)
                        .padding(.vertical, 4)
                        .background(AnnoTheme.narthex)
                        .clipShape(Capsule())

                        // Theological Significance (New York Serif)
                        VStack(alignment: .leading, spacing: 8) {
                            Text(language == .vietnamese ? "Ý Nghĩa Thần Học & Chiêm Niệm" : "Theological Significance & Contemplation")
                                .font(Typography.subheadlineSemiboldSerif)
                                .foregroundStyle(AnnoTheme.goldLeaf)

                            Text(dossier.localizedTheologicalSignificance(for: language))
                                .font(Typography.bodySerif)
                                .lineSpacing(5)
                                .foregroundStyle(AnnoTheme.vellum)
                                .fixedSize(horizontal: false, vertical: true)
                        }

                        Divider()
                            .background(AnnoTheme.ash)

                        // Provenance & Metadata Grid
                        VStack(alignment: .leading, spacing: 8) {
                            Text(language == .vietnamese ? "Xuất Xứ & Thông Tin Kiệt Tác" : "Provenance & Masterwork Data")
                                .font(Typography.captionBold)
                                .foregroundStyle(AnnoTheme.incense)
                                .textCase(.uppercase)

                            metadataRow(
                                label: language == .vietnamese ? "Chất liệu" : "Medium",
                                value: dossier.medium
                            )
                            metadataRow(
                                label: language == .vietnamese ? "Kích thước" : "Dimensions",
                                value: dossier.dimensions
                            )
                            metadataRow(
                                label: language == .vietnamese ? "Địa điểm hiện tại" : "Current Location",
                                value: dossier.currentLocation
                            )
                            metadataRow(
                                label: language == .vietnamese ? "Bản quyền" : "License",
                                value: dossier.licenseType
                            )
                        }
                    }
                    .padding(.horizontal, 20)
                    .padding(.bottom, 32)
                }
                .frame(maxHeight: geometry.size.height * 0.45)
            }
        }
        .background(
            RoundedRectangle(cornerRadius: 16, style: .continuous)
                .fill(AnnoTheme.choir.opacity(0.96))
                .overlay(
                    RoundedRectangle(cornerRadius: 16, style: .continuous)
                        .strokeBorder(AnnoTheme.ash, lineWidth: 1)
                )
                .shadow(color: .black.opacity(0.6), radius: 24, y: -6)
        )
        .padding(.horizontal, 8)
        .padding(.bottom, 8)
    }

    private func metadataRow(label: String, value: String) -> some View {
        HStack(alignment: .top, spacing: 8) {
            Text(label)
                .font(Typography.captionSerif)
                .foregroundStyle(AnnoTheme.incense)
                .frame(width: 110, alignment: .leading)

            Text(value)
                .font(Typography.captionMedium)
                .foregroundStyle(AnnoTheme.vellum)
                .frame(maxWidth: .infinity, alignment: .leading)
        }
    }

    // MARK: - Loading & Error States

    private var canvasShimmerPlaceholder: some View {
        VStack(spacing: 16) {
            ProgressView()
                .tint(AnnoTheme.goldLeaf)
                .scaleEffect(1.3)

            Text(language == .vietnamese ? "Đang tải tác phẩm 4K..." : "Loading sacred masterwork...")
                .font(Typography.captionMedium)
                .foregroundStyle(AnnoTheme.incense)
        }
    }

    private var errorRetryView: some View {
        VStack(spacing: 16) {
            Image(systemName: "exclamationmark.triangle")
                .font(Typography.iconLarge)
                .foregroundStyle(AnnoTheme.crimson)

            Text(language == .vietnamese ? "Không thể tải ảnh độ phân giải cao" : "Unable to load high-resolution artwork")
                .font(Typography.subheadlineSemibold)
                .foregroundStyle(AnnoTheme.vellum)

            Button(action: {
                Task {
                    await loadImageAsset()
                }
            }) {
                HStack(spacing: 6) {
                    Image(systemName: "arrow.clockwise")
                    Text(language == .vietnamese ? "Thử lại" : "Retry")
                }
                .font(Typography.captionBoldSerif)
                .foregroundStyle(AnnoTheme.narthex)
                .padding(.horizontal, 16)
                .padding(.vertical, 8)
                .background(AnnoTheme.goldLeaf)
                .clipShape(Capsule())
            }
            .buttonStyle(.plain)
        }
        .padding(24)
        .annoCard()
    }

    // MARK: - Async Image Downloader with Cache

    private func loadImageAsset() async {
        guard let url = URL(string: dossier.imageUrlHighres.isEmpty ? dossier.imageUrlThumb : dossier.imageUrlHighres) else {
            loadFailed = true
            isLoadingHighRes = false
            return
        }

        // Check memory cache
        if let cached = SacredArtImageCache.shared.image(for: url) {
            self.loadedImage = cached
            self.isLoadingHighRes = false
            self.loadFailed = false
            return
        }

        isLoadingHighRes = true
        loadFailed = false

        do {
            var request = URLRequest(url: url)
            request.timeoutInterval = 20
            let (data, response) = try await URLSession.shared.data(for: request)

            guard (response as? HTTPURLResponse)?.statusCode == 200,
                  let image = UIImage(data: data) else {
                throw URLError(.badServerResponse)
            }

            SacredArtImageCache.shared.insertImage(image, for: url)
            self.loadedImage = image
            self.isLoadingHighRes = false
            self.loadFailed = false
        } catch {
            // Try fallback to thumb url if different
            if !dossier.imageUrlThumb.isEmpty, dossier.imageUrlThumb != dossier.imageUrlHighres,
               let thumbUrl = URL(string: dossier.imageUrlThumb) {
                if let thumbData = try? await URLSession.shared.data(from: thumbUrl).0,
                   let thumbImage = UIImage(data: thumbData) {
                    SacredArtImageCache.shared.insertImage(thumbImage, for: thumbUrl)
                    self.loadedImage = thumbImage
                    self.isLoadingHighRes = false
                    self.loadFailed = false
                    return
                }
            }
            self.loadFailed = true
            self.isLoadingHighRes = false
        }
    }
}

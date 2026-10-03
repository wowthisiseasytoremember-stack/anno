import ImagePlayground
import SwiftUI
import UIKit

/// Staged Apple Intelligence keepsake surface.
///
/// This is intentionally outside the shipping target until the deployment
/// target/Xcode lane can validate the current Image Playground APIs.
@available(iOS 27.0, *)
struct AnnoPilgrimageKeepsakePlayground: View {
    let routeTitle: String
    let invocation: String
    let sourceImage: Image?
    let onImageCreated: (URL) -> Void
    let onAdaptiveGlyphCreated: (NSAdaptiveImageGlyph) -> Void

    @Environment(\.supportsImagePlayground) private var supportsImagePlayground
    @State private var showingPlayground = false

    private var prompt: String {
        """
        A luminous Catholic pilgrimage keepsake for \(routeTitle).
        Marian blue, warm gold leaf, illuminated-manuscript ornament,
        subtle Orange County pilgrimage route geometry, reverent and celebratory,
        devotional postcard rather than historical reconstruction.
        Include no invented historical people or documentary claims.
        Invocation: \(invocation)
        """
    }

    var body: some View {
        Button {
            showingPlayground = true
        } label: {
            Label("Create Pilgrimage Keepsake", systemImage: "sparkles.rectangle.stack")
        }
        .disabled(!supportsImagePlayground)
        .imagePlaygroundSheet(
            isPresented: $showingPlayground,
            concept: prompt,
            sourceImage: sourceImage,
            onCompletion: { url in
                onImageCreated(url)
            },
            onAdaptiveImageGlyphCreation: { glyph in
                onAdaptiveGlyphCreated(glyph)
            },
            onCancellation: {}
        )
    }
}

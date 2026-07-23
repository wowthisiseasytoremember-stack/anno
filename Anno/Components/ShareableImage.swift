//  ShareableImage.swift
//  DailyDevotionKJVForWomen
//
//  A Transferable wrapper so rendered share cards can be shared as both an
//  image and accompanying text via ShareLink.
//

import SwiftUI
import UniformTypeIdentifiers
import CoreTransferable

/// A rendered verse card ready to share.
struct ShareableImage: Transferable {
    let uiImage: UIImage
    let caption: String

    var image: Image { Image(uiImage: uiImage) }

    static var transferRepresentation: some TransferRepresentation {
        DataRepresentation(exportedContentType: .png) { shareable in
            shareable.uiImage.pngData() ?? Data()
        }
        .suggestedFileName("devotional-verse.png")
    }
}
//
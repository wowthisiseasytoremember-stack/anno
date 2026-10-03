import SwiftUI
import Vision
import VisionKit

/// Native VisionKit scanner for Anno field-test QR markers and physical text.
///
/// Stage in the app target when the camera permission/device lane is available.
struct AnnoSacredCameraScanner: UIViewControllerRepresentable {
    let onDeepLink: (URL) -> Void
    let onRecognizedText: (String) -> Void

    static var isSupported: Bool {
        DataScannerViewController.isSupported
    }

    static var isAvailable: Bool {
        DataScannerViewController.isAvailable
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(
            onDeepLink: onDeepLink,
            onRecognizedText: onRecognizedText
        )
    }

    func makeUIViewController(
        context: Context
    ) -> DataScannerViewController {
        let scanner = DataScannerViewController(
            recognizedDataTypes: [
                .text(
                    languages: ["vi-VN", "en-US"],
                    textContentType: nil
                ),
                .barcode(symbologies: [.qr])
            ],
            qualityLevel: .balanced,
            recognizesMultipleItems: true,
            isHighFrameRateTrackingEnabled: false,
            isPinchToZoomEnabled: true,
            isGuidanceEnabled: true,
            isHighlightingEnabled: true
        )

        scanner.delegate = context.coordinator
        return scanner
    }

    func updateUIViewController(
        _ scanner: DataScannerViewController,
        context: Context
    ) {
        guard !context.coordinator.didStartScanning,
              Self.isAvailable else {
            return
        }

        do {
            try scanner.startScanning()
            context.coordinator.didStartScanning = true
        } catch {
            #if DEBUG
            print("Anno Sacred Camera failed to start: \(error)")
            #endif
        }
    }

    static func dismantleUIViewController(
        _ scanner: DataScannerViewController,
        coordinator: Coordinator
    ) {
        scanner.stopScanning()
        coordinator.didStartScanning = false
    }

    final class Coordinator: NSObject, DataScannerViewControllerDelegate {
        var didStartScanning = false

        private let onDeepLink: (URL) -> Void
        private let onRecognizedText: (String) -> Void

        init(
            onDeepLink: @escaping (URL) -> Void,
            onRecognizedText: @escaping (String) -> Void
        ) {
            self.onDeepLink = onDeepLink
            self.onRecognizedText = onRecognizedText
        }

        func dataScanner(
            _ dataScanner: DataScannerViewController,
            didTapOn item: RecognizedItem
        ) {
            switch item {
            case .barcode(let barcode):
                guard let payload = barcode.payloadStringValue,
                      let url = URL(string: payload),
                      AnnoDeepLink(url: url) != nil else {
                    return
                }

                Haptics.sacredArrival(.feast)
                onDeepLink(url)

            case .text(let text):
                let transcript = text.transcript
                    .trimmingCharacters(in: .whitespacesAndNewlines)

                guard !transcript.isEmpty else { return }

                Haptics.selection()
                onRecognizedText(transcript)

            @unknown default:
                break
            }
        }
    }
}

import CoreGraphics
import Foundation
import Vision

struct AnnoRecognizedTextLine: Hashable, Sendable {
    let text: String
    let confidence: Float
    let boundingBox: CGRect
}

struct AnnoRecognizedCode: Hashable, Sendable {
    let payload: String
    let symbology: String
    let boundingBox: CGRect
}

/// On-device analysis building block for the future Sacred Camera.
///
/// The camera UI remains staged; this analyzer is intentionally independent
/// from AVCapture/VisionKit so it can be tested with still fixtures first.
enum AnnoSacredCameraAnalyzer {
    static func recognizeText(
        in image: CGImage,
        languages: [String] = ["vi-VN", "en-US"]
    ) throws -> [AnnoRecognizedTextLine] {
        let request = VNRecognizeTextRequest()
        request.recognitionLevel = .accurate
        request.recognitionLanguages = languages
        request.usesLanguageCorrection = true

        let handler = VNImageRequestHandler(cgImage: image)
        try handler.perform([request])

        return (request.results ?? []).compactMap { observation in
            guard let candidate = observation.topCandidates(1).first else {
                return nil
            }

            return AnnoRecognizedTextLine(
                text: candidate.string,
                confidence: candidate.confidence,
                boundingBox: observation.boundingBox
            )
        }
    }

    static func recognizeCodes(
        in image: CGImage
    ) throws -> [AnnoRecognizedCode] {
        let request = VNDetectBarcodesRequest()
        let handler = VNImageRequestHandler(cgImage: image)
        try handler.perform([request])

        return (request.results ?? []).compactMap { observation in
            guard let payload = observation.payloadStringValue else {
                return nil
            }

            return AnnoRecognizedCode(
                payload: payload,
                symbology: observation.symbology.rawValue,
                boundingBox: observation.boundingBox
            )
        }
    }
}

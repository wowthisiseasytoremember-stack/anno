import CoreNFC
import Foundation

/// Field-test helper for writing Anno's compact station URLs to writable NDEF tags.
///
/// Keep outside the shipping target until the NFC entitlement/device lane is
/// activated. Every written tag resolves through the same `anno://p/lv/N`
/// deep-link router used by QR markers.
final class AnnoNFCMarkerWriter: NSObject, NFCNDEFReaderSessionDelegate {
    static let shared = AnnoNFCMarkerWriter()

    private var session: NFCNDEFReaderSession?
    private var pendingMessage: NFCNDEFMessage?

    private override init() {
        super.init()
    }

    var isSupported: Bool {
        NFCNDEFReaderSession.readingAvailable
    }

    func beginWriting(markerIndex: Int) {
        guard isSupported,
              let payload = AnnoPhysicalPilgrimageMarker.nfcPayload(
                index: markerIndex
              ) else {
            return
        }

        pendingMessage = NFCNDEFMessage(records: [payload])

        let session = NFCNDEFReaderSession(
            delegate: self,
            queue: nil,
            invalidateAfterFirstRead: false
        )

        session.alertMessage =
            "Hold your iPhone near the writable Anno pilgrimage marker."
        self.session = session
        session.begin()
    }

    func readerSession(
        _ session: NFCNDEFReaderSession,
        didDetectNDEFs messages: [NFCNDEFMessage]
    ) {
        // Implementing didDetect tags below suppresses this callback for
        // read-write sessions. This method remains required by the protocol.
    }

    func readerSession(
        _ session: NFCNDEFReaderSession,
        didDetect tags: [any NFCNDEFTag]
    ) {
        guard tags.count == 1,
              let tag = tags.first,
              let pendingMessage else {
            session.alertMessage =
                "More than one tag was detected. Present a single marker."
            session.restartPolling()
            return
        }

        session.connect(to: tag) { error in
            if let error {
                session.invalidate(
                    errorMessage: "Could not connect to the NFC tag: \(error.localizedDescription)"
                )
                return
            }

            tag.queryNDEFStatus { status, _, error in
                if let error {
                    session.invalidate(
                        errorMessage: "Could not read tag status: \(error.localizedDescription)"
                    )
                    return
                }

                guard status == .readWrite else {
                    session.invalidate(
                        errorMessage: "This NFC tag is not writable."
                    )
                    return
                }

                tag.writeNDEF(pendingMessage) { error in
                    if let error {
                        session.invalidate(
                            errorMessage: "Could not write the Anno marker: \(error.localizedDescription)"
                        )
                        return
                    }

                    session.alertMessage = "Anno pilgrimage marker written."
                    session.invalidate()
                    Haptics.success()
                }
            }
        }
    }

    func readerSession(
        _ session: NFCNDEFReaderSession,
        didInvalidateWithError error: Error
    ) {
        pendingMessage = nil
        self.session = nil
    }
}

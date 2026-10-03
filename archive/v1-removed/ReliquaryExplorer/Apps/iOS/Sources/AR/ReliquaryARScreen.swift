import ARKit
import PilgrimCore
import SwiftUI
import UIKit

/// Full-screen iOS/iPadOS AR experience.
///
/// Responsibilities split:
/// - `ReliquaryARViewContainer` (UIKit): ARView + coaching overlay +
///   gesture recognizers → shared-model intent calls.
/// - This SwiftUI layer: HUD (phase/tracking/banners), catalog switcher,
///   and AR-activity bookkeeping on the coordinator.
struct ReliquaryARScreen: View {
    let coordinator: PilgrimGuideCoordinator
    let item: ReliquaryItem

    @State private var model: ReliquaryInteractionModel
    @State private var service: ARKitReliquarySessionService
    @Environment(\.dismiss) private var dismiss

    init(coordinator: PilgrimGuideCoordinator, item: ReliquaryItem) {
        self.coordinator = coordinator
        self.item = item
        let service = ARKitReliquarySessionService()
        _service = State(initialValue: service)
        _model = State(
            initialValue: ReliquaryInteractionModel(
                session: service,
                initialSelection: item
            )
        )
    }

    var body: some View {
        ZStack {
            ReliquaryARViewContainer(service: service, model: model)
                .ignoresSafeArea()

            hud
        }
        .onAppear {
            coordinator.arViewerActive = true
            Task { await model.beginSession() }
        }
        .onDisappear {
            model.endSession()
            coordinator.arViewerActive = false
        }
    }

    // MARK: - HUD

    @ViewBuilder
    private var hud: some View {
        VStack(spacing: 10) {
            HagiographyBanner(coordinator: coordinator)
                .padding(.horizontal, 12)

            statusCapsule
                .padding(.top, 2)

            Spacer()

            if model.surfaceMissPulse {
                Text("No surface there — aim at a horizontal surface and tap again.")
                    .font(.footnote.weight(.bold))
                    .padding(.horizontal, 14)
                    .padding(.vertical, 8)
                    .background(.red.opacity(0.85), in: Capsule())
                    .transition(.opacity)
            }

            controls
                .padding(.bottom, 18)
        }
        .animation(.snappy, value: model.surfaceMissPulse)
        .animation(.snappy, value: model.phase)
    }

    private var statusCapsule: some View {
        HStack(spacing: 8) {
            Image(systemName: statusIcon)
                .foregroundStyle(statusColor)
            Text(statusText)
                .font(.caption.weight(.bold))
                .lineLimit(2)
                .multilineTextAlignment(.center)
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 8)
        .background(.ultraThinMaterial, in: Capsule())
    }

    private var controls: some View {
        HStack(spacing: 14) {
            Button(role: .destructive) {
                model.removeAllPlacements()
            } label: {
                Image(systemName: "trash")
                    .frame(width: 46, height: 46)
                    .background(.ultraThinMaterial, in: Circle())
            }
            .disabled(model.placements.isEmpty)
            .opacity(model.placements.isEmpty ? 0.35 : 1)

            Spacer()

            Menu {
                ForEach(ReliquaryItem.catalog) { candidate in
                    Button {
                        model.selectReliquary(candidate)
                    } label: {
                        if candidate.id == model.selectedReliquary.id {
                            Label(candidate.title, systemImage: "checkmark")
                        } else {
                            Text(candidate.title)
                        }
                    }
                }
            } label: {
                VStack(spacing: 2) {
                    Image(systemName: "cross.vial.fill")
                        .font(.title3)
                    Text(model.selectedReliquary.title)
                        .font(.caption2)
                        .lineLimit(1)
                }
                .frame(width: 150, height: 52)
                .background(.ultraThinMaterial, in: Capsule())
            }

            Spacer()

            Button {
                dismiss()
            } label: {
                Image(systemName: "xmark")
                    .frame(width: 46, height: 46)
                    .background(.ultraThinMaterial, in: Circle())
            }
        }
        .padding(.horizontal, 20)
    }

    private var statusText: String {
        if model.isInterrupted {
            return "Session interrupted — returning to AR…"
        }
        switch model.trackingState {
        case .initializing, .limited(reason: .initializing):
            return "Initializing tracking — move the device slowly."
        case .limited(let reason) where model.phase.allowsPlacement:
            return limitedText(reason) + " Tap a surface to place."
        case .limited(let reason):
            return limitedText(reason)
        case .normal:
            switch model.phase {
            case .searchingSurface:
                return "Move the device to detect a table or floor."
            case .readyToPlace, .placed:
                return "Tap a surface to place · pinch to scale · twist to rotate"
            case .loadingAsset:
                return "Preparing reliquary…"
            case .failed(let message):
                return message
            case .idle:
                return "Starting session…"
            }
        case .unavailable(let reason):
            return reason
        }
    }

    private func limitedText(_ reason: ReliquaryTrackingState.LimitedReason) -> String {
        switch reason {
        case .excessiveMotion: return "Moving too fast — slow down."
        case .insufficientFeatures: return "Low detail — scan a textured area."
        case .relocalizing, .interrupted: return "Re-orienting to resume tracking…"
        case .initializing: return "Initializing tracking."
        }
    }

    private var statusIcon: String {
        switch model.trackingState {
        case .normal: return "checkmark.circle.fill"
        case .initializing, .limited: return "exclamationmark.triangle.fill"
        case .unavailable: return "xmark.octagon.fill"
        }
    }

    private var statusColor: Color {
        switch model.trackingState {
        case .normal: return .green
        case .initializing, .limited: return .orange
        case .unavailable: return .red
        }
    }
}

// MARK: - UIKit bridge

/// `UIViewRepresentable` for the RealityKit ARView with:
/// - `ARCoachingOverlayView` (onboarding + relocalization guidance),
/// - tap/pinch/rotation recognizers that translate UIKit gestures into
///   shared-model intents (the *only* gesture code on iOS).
struct ReliquaryARViewContainer: UIViewRepresentable {
    let service: ARKitReliquarySessionService
    @Bindable var model: ReliquaryInteractionModel

    func makeUIView(context: Context) -> ARView {
        let arView = service.makeARView()
        context.coordinator.attachCoachingOverlay(to: arView)
        attachGestures(to: arView, coordinator: context.coordinator)
        return arView
    }

    func updateUIView(_ uiView: ARView, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(model: model)
    }

    private func attachGestures(to arView: ARView, coordinator: Coordinator) {
        let tap = UITapGestureRecognizer(
            target: coordinator, action: #selector(Coordinator.handleTap(_:))
        )
        let pinch = UIPinchGestureRecognizer(
            target: coordinator, action: #selector(Coordinator.handlePinch(_:))
        )
        let rotation = UIRotationGestureRecognizer(
            target: coordinator, action: #selector(Coordinator.handleRotation(_:))
        )
        [tap, pinch, rotation].forEach { arView.addGestureRecognizer($0) }
    }

    @MainActor
    final class Coordinator: NSObject {
        private let model: ReliquaryInteractionModel
        private var lastHaptic = Date.distantPast

        init(model: ReliquaryInteractionModel) {
            self.model = model
        }

        /// ARKit coaching overlay: guides plane discovery initially and
        /// relocalization after tracking loss — satisfies the "gracefully
        /// handle tracking loss/relocalization" requirement.
        func attachCoachingOverlay(to arView: ARView) {
            let overlay = ARCoachingOverlayView()
            overlay.session = arView.session
            overlay.delegate = self
            overlay.goal = .horizontalPlane
            overlay.activatesAutomatically = true
            overlay.frame = arView.bounds
            overlay.autoresizingMask = [.flexibleWidth, .flexibleHeight]
            arView.addSubview(overlay)
        }

        @objc func handleTap(_ recognizer: UITapGestureRecognizer) {
            guard recognizer.state == .ended else { return }
            let point = recognizer.location(in: recognizer.view)
            haptic()
            Task { @MainActor in
                await model.confirmPlacement(atScreenPoint: point)
            }
        }

        @objc func handlePinch(_ recognizer: UIPinchGestureRecognizer) {
            // Recognizer callbacks arrive on the main thread (UIKit),
            // so main-actor isolation is guaranteed.
            MainActor.assumeIsolated {
                switch recognizer.state {
                case .changed:
                    model.handleScaleDelta(Float(recognizer.scale))
                    recognizer.scale = 1 // incremental deltas, like the visionOS gesture
                case .ended:
                    model.settleScale()
                default:
                    break
                }
            }
        }

        @objc func handleRotation(_ recognizer: UIRotationGestureRecognizer) {
            MainActor.assumeIsolated {
                guard recognizer.state == .changed else { return }
                // Counter-clockwise finger twist reads as clockwise object
                // spin; invert for natural feel (same on visionOS).
                model.handleYawDelta(Float(-recognizer.rotation))
                recognizer.rotation = 0
            }
        }

        private func haptic() {
            MainActor.assumeIsolated {
                guard Date().timeIntervalSince(lastHaptic) > 0.4 else { return }
                lastHaptic = Date()
                UIImpactFeedbackGenerator(style: .medium).impactOccurred()
            }
        }
    }
}

extension ReliquaryARViewContainer.Coordinator: ARCoachingOverlayViewDelegate {}

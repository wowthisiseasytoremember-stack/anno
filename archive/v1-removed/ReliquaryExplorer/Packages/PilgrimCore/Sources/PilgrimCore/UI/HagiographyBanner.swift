import SwiftUI

/// Floating "hagiography playing" capsule.
///
/// Instantiated both over the main tab UI and inside the AR viewers, so
/// an arrival during AR inspection is visible *and* dismissible without
/// leaving the session.
public struct HagiographyBanner: View {
    @Bindable var coordinator: PilgrimGuideCoordinator

    public init(coordinator: PilgrimGuideCoordinator) {
        self.coordinator = coordinator
    }

    public var body: some View {
        if let nowPlaying = coordinator.nowPlaying {
            HStack(spacing: 12) {
                Image(systemName: "headphones")
                    .symbolEffect(.pulse, options: .repeating)
                    .foregroundStyle(Color.pilgrimGold)

                VStack(alignment: .leading, spacing: 2) {
                    Text("Sanctuary Hagiography")
                        .font(.caption2)
                        .fontWeight(.bold)
                        .textCase(.uppercase)
                        .foregroundStyle(.secondary)
                    Text(nowPlaying.siteName)
                        .font(.subheadline)
                        .fontWeight(.heavy)
                        .lineLimit(1)
                }

                Spacer(minLength: 8)

                Button {
                    switch nowPlaying.state {
                    case .playing: coordinator.pausePlayback()
                    case .paused: coordinator.resumePlayback()
                    }
                } label: {
                    Image(systemName: nowPlaying.state == .playing ? "pause.fill" : "play.fill")
                        .padding(8)
                }
                .buttonStyle(.borderless)

                Button(role: .destructive) {
                    coordinator.stopPlayback()
                } label: {
                    Image(systemName: "stop.fill")
                        .padding(8)
                }
                .buttonStyle(.borderless)
            }
            .padding(12)
            .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 14))
            .overlay(
                RoundedRectangle(cornerRadius: 14)
                    .stroke(Color.pilgrimGold.opacity(0.5), lineWidth: 1)
            )
            .shadow(radius: 6, y: 2)
            .transition(.move(edge: .top).combined(with: .opacity))
        }
    }
}

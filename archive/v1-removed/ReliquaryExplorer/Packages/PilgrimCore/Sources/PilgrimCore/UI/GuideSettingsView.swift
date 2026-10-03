import SwiftUI

/// Guide settings: proximity-guidance availability (platform truth),
/// narration language preference, and transparency about permissions.
public struct GuideSettingsView: View {
    @Bindable var coordinator: PilgrimGuideCoordinator

    @AppStorage(PilgrimSettings.narrationLanguageOverride)
    private var languageOverride: String = ""

    public init(coordinator: PilgrimGuideCoordinator) {
        self.coordinator = coordinator
    }

    private var availableLanguages: [String] {
        let union = Set(coordinator.catalog.sites.flatMap { $0.narrations.keys })
        return union.sorted()
    }

    public var body: some View {
        NavigationStack {
            Form {
                Section {
                    availabilityRow
                } header: {
                    Text("Proximity Guidance")
                } footer: {
                    Text(
                        "On iPhone and iPad, sanctuaries are monitored with low-power "
                            + "region monitoring — no continuous GPS. Narration begins "
                            + "automatically when you enter a sanctuary, even while the "
                            + "app is in the background. On Apple Vision Pro, ambulatory "
                            + "geofencing is intentionally unavailable; browse sanctuaries "
                            + "on the map and play their hagiographies manually."
                    )
                }

                Section {
                    Picker("Narration language", selection: $languageOverride) {
                        Text("Automatic (device languages)").tag("")
                        ForEach(availableLanguages, id: \.self) { code in
                            Text(Locale.current.localizedString(forLanguageCode: code) ?? code)
                                .tag(code)
                        }
                    }
                } header: {
                    Text("Hagiography")
                } footer: {
                    Text("Each sanctuary ships narrations in multiple languages; Automatic picks the best match for your device languages, falling back to English.")
                }

                Section {
                    LabeledContent("Sanctuaries", value: "\(coordinator.catalog.sites.count)")
                    LabeledContent("Inside now", value: coordinator.lastVisit?.kind == .entered ? coordinator.lastVisit?.site.name ?? "—" : "—")
                } header: {
                    Text("Status")
                }

#if DEBUG
                demoSection
#endif
            }
            .navigationTitle("Guide")
        }
    }

#if DEBUG
    /// Debug-build demo panel: exercises the *entire* proximity pipeline
    /// (visit policy → narration → banner/notification) without GPS.
    /// Compiles out of release builds.
    private var demoSection: some View {
        Section {
            ForEach(coordinator.catalog.sites) { site in
                VStack(alignment: .leading, spacing: 8) {
                    Text(site.name)
                        .font(.subheadline.weight(.semibold))
                    HStack {
                        Button {
                            coordinator.debugSimulateArrival(at: site)
                        } label: {
                            Label("Simulate arrival", systemImage: "figure.walk.arrival")
                        }
                        .buttonStyle(.borderedProminent)
                        .tint(.pilgrimGold)

                        Button {
                            coordinator.debugSimulateDeparture(from: site)
                        } label: {
                            Label("Depart", systemImage: "figure.walk.departure")
                        }
                        .buttonStyle(.bordered)
                    }
                }
                .padding(.vertical, 2)
            }

            Button(role: .destructive) {
                coordinator.debugDisableVisitCooldown()
            } label: {
                Label("Disable visit cooldown (demo)", systemImage: "clock.badge.xmark")
            }

            if !coordinator.recentVisitLog.isEmpty {
                VStack(alignment: .leading, spacing: 4) {
                    Text("Recent geofence events")
                        .font(.caption.weight(.bold))
                        .foregroundStyle(.secondary)
                    ForEach(Array(coordinator.recentVisitLog.prefix(6).enumerated()), id: \.offset) { _, event in
                        HStack {
                            Image(systemName: event.kind == .entered ? "arrow.down.right.circle.fill" : "arrow.up.right.circle")
                                .foregroundStyle(event.kind == .entered ? Color.pilgrimGold : .secondary)
                            Text(event.site.name)
                            Spacer()
                            Text(event.timestamp, format: .time)
                                .foregroundStyle(.tertiary)
                        }
                        .font(.caption)
                    }
                }
            }
        } header: {
            Text("Demo & QA")
        } footer: {
            Text("Debug builds only. “Simulate arrival” runs the real geofence→audio pipeline on device — ideal for App Review demos. For GPS-accurate simulation, load Demo/SimulatorRoutes/grand_tour.gpx via Xcode ▸ Debug ▸ Location ▸ Custom GPX, or walk the real route with santiago_approach.gpx.")
        }
    }
#endif

    @ViewBuilder
    private var availabilityRow: some View {
        switch coordinator.availability {
        case .available:
            Label("Armed — narration will start automatically on arrival", systemImage: "checkmark.seal.fill")
                .foregroundStyle(.green)
        case let .requiresAuthorization(hint):
            Label(hint, systemImage: "location.slash.fill")
                .foregroundStyle(.orange)
        case let .unsupported(reason):
            VStack(alignment: .leading, spacing: 4) {
                Label("Unavailable on this device", systemImage: "lock.display")
                    .foregroundStyle(.secondary)
                Text(reason)
                    .font(.footnote)
                    .foregroundStyle(.secondary)
            }
        }
    }
}

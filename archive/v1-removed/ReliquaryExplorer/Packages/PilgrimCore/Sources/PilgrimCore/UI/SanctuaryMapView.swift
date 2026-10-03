import MapKit
import SwiftUI

/// Sanctuary map with geofence rings and per-site narration callouts.
///
/// On iOS this doubles as the "where am I on the route" view; on visionOS
/// it is the museum-mode browser (proximity triggering is unavailable
/// there by design — see `GuideSettingsView`'s availability section).
public struct SanctuaryMapView: View {
    @Bindable var coordinator: PilgrimGuideCoordinator
    @State private var selectedSite: SanctuarySite?

    public init(coordinator: PilgrimGuideCoordinator) {
        self.coordinator = coordinator
    }

    public var body: some View {
        Map {
            UserAnnotation()

            ForEach(coordinator.catalog.sites) { site in
                Annotation(site.name, coordinate: site.coordinate) {
                    Button {
                        selectedSite = site
                    } label: {
                        Image(systemName: "cross.fill")
                            .font(.headline)
                            .padding(8)
                            .background(.thickMaterial, in: Circle())
                            .foregroundStyle(Color.pilgrimGold)
                            .overlay(Circle().stroke(.white.opacity(0.6), lineWidth: 1))
                    }
                    .buttonStyle(.plain)
                }

                MapCircle(center: site.coordinate, radius: site.radiusMeters)
                    .foregroundStyle(Color.pilgrimGold.opacity(0.08))
                    .stroke(Color.pilgrimGold.opacity(0.4), lineWidth: 1)
            }
        }
        .mapStyle(.standard(elevation: .realistic))
        .sheet(item: $selectedSite) { site in
            SanctuaryDetailSheet(coordinator: coordinator, site: site)
                .presentationDetents([.medium, .large])
        }
    }
}

private struct SanctuaryDetailSheet: View {
    @Bindable var coordinator: PilgrimGuideCoordinator
    let site: SanctuarySite
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    availabilityLabel

                    LabeledContent("Geofence radius", value: "\(Int(site.radiusMeters)) m")
                    LabeledContent("Coordinates", value: String(format: "%.5f, %.5f", site.latitude, site.longitude))

                    if let reliquaryID = site.associatedReliquaryId,
                       let item = ReliquaryItem.item(withID: reliquaryID) {
                        LabeledContent("Associated reliquary", value: item.title)
                    }

                    Divider()

                    ForEach(site.narrations.keys.sorted(), id: \.self) { language in
                        if let narration = site.narrations[language] {
                            VStack(alignment: .leading, spacing: 6) {
                                Text(Locale.current.localizedString(forLanguageCode: language) ?? language)
                                    .font(.headline)
                                Text(narration.transcript)
                                    .font(.body)
                                    .foregroundStyle(.secondary)
                            }
                            .padding(.vertical, 4)
                        }
                    }

                    Button {
                        coordinator.playNarration(manuallyFor: site)
                        dismiss()
                    } label: {
                        Label("Play hagiography", systemImage: "play.circle.fill")
                            .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(.pilgrimGold)
                }
                .padding()
            }
            .navigationTitle(site.name)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }

    @ViewBuilder
    private var availabilityLabel: some View {
        switch coordinator.availability {
        case .available:
            Label("Proximity narration armed — it will begin automatically on arrival", systemImage: "location.fill")
                .font(.footnote)
                .foregroundStyle(.green)
        case let .requiresAuthorization(hint):
            Label(hint, systemImage: "location.slash")
                .font(.footnote)
                .foregroundStyle(.orange)
        case let .unsupported(reason):
            Label(reason, systemImage: "lock.display")
                .font(.footnote)
                .foregroundStyle(.secondary)
        }
    }
}

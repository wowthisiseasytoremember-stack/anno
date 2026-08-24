import SwiftUI

/// Catalog of inspectable reliquaries with the platform-agnostic
/// "place in your space" action. The actual presentation (full-screen
/// cover on iOS, immersive space on visionOS) is injected by the app
/// target.
public struct ReliquaryCatalogView: View {
    @Bindable var coordinator: PilgrimGuideCoordinator
    let launchARViewer: @MainActor (ReliquaryItem) -> Void

    @State private var selectedItem: ReliquaryItem?

    public init(
        coordinator: PilgrimGuideCoordinator,
        launchARViewer: @escaping (ReliquaryItem) -> Void
    ) {
        self.coordinator = coordinator
        self.launchARViewer = launchARViewer
    }

    public var body: some View {
        NavigationStack {
            List(ReliquaryItem.catalog) { item in
                Button {
                    selectedItem = item
                } label: {
                    row(for: item)
                }
                .buttonStyle(.plain)
            }
            .navigationTitle("Reliquaries")
            .sheet(item: $selectedItem) { item in
                ReliquaryDetailSheet(
                    coordinator: coordinator,
                    item: item,
                    launchARViewer: launchARViewer
                )
                .presentationDetents([.medium, .large])
            }
        }
    }

    private func row(for item: ReliquaryItem) -> some View {
        HStack(spacing: 14) {
            Image(systemName: "cross.vial")
                .font(.title2)
                .frame(width: 44, height: 44)
                .background(Color.pilgrimGold.opacity(0.15), in: RoundedRectangle(cornerRadius: 10))

            VStack(alignment: .leading, spacing: 2) {
                Text(item.title)
                    .font(.headline)
                    .foregroundStyle(.primary)
                Text(item.era)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            Spacer()
            Image(systemName: "chevron.right")
                .font(.caption)
                .foregroundStyle(.tertiary)
        }
        .padding(.vertical, 4)
    }
}

private struct ReliquaryDetailSheet: View {
    @Bindable var coordinator: PilgrimGuideCoordinator
    let item: ReliquaryItem
    let launchARViewer: @MainActor (ReliquaryItem) -> Void
    @Environment(\.dismiss) private var dismiss

    private var associatedSanctuaries: [SanctuarySite] {
        coordinator.catalog.sites.filter { $0.associatedReliquaryId == item.id }
    }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    VStack(alignment: .leading, spacing: 4) {
                        Text(item.era)
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                            .textCase(.uppercase)
                        Text(item.historicalNotes)
                            .font(.body)
                    }

                    Divider()

                    Text("This piece is geofenced at:")
                        .font(.headline)
                    ForEach(associatedSanctuaries) { site in
                        Label(site.name, systemImage: "mappin.and.ellipse")
                            .font(.subheadline)
                    }
                    if associatedSanctuaries.isEmpty {
                        Text("No sanctuary currently links this reliquary.")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }

                    Button {
                        dismiss()
                        launchARViewer(item)
                    } label: {
                        Label("Place in your space", systemImage: "arkit")
                            .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(.pilgrimGold)
                }
                .padding()
            }
            .navigationTitle(item.title)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }
}

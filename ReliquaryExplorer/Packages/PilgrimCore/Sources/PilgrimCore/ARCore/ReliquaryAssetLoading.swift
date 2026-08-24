import Foundation
import RealityKit
import simd

/// Loads a bundle reliquary asset (`.usdz` / `.reality`) into a normalized
/// wrapper entity.
///
/// Per the product constraints, assets are assumed produced and optimized
/// upstream. The loader's job is: resolve from the bundle, wrap for
/// uniform treatment (scale, collision, input targeting), and degrade
/// gracefully to a clearly-marked placeholder box when an asset is
/// missing so flows remain testable without art.
public enum ReliquaryAssetLoader {
    public static func loadRootEntity(for item: ReliquaryItem) async -> Entity {
        do {
            // Resolves "<name>.reality" or "<name>.usdz" from the bundle.
            let loaded = try await Entity.loadAsync(named: item.modelAssetName)
            return prepared(loaded, for: item)
        } catch {
            PilgrimCoreLog.ar.warning(
                "Asset '\(item.modelAssetName)' not loadable (\(error.localizedDescription)); using placeholder."
            )
            return placeholder(for: item)
        }
    }

    /// Wraps the loaded model, applies the curated default scale, and
    /// generates collision so spatial/touch gesture targeting works.
    static func prepared(_ loaded: Entity, for item: ReliquaryItem) -> Entity {
        let wrapper = Entity()
        wrapper.name = "reliquary_\(item.id)"
        wrapper.addChild(loaded)
        wrapper.scale = SIMD3<Float>(repeating: item.defaultScale)
        makeTargetable(wrapper)
        return wrapper
    }

    static func placeholder(for item: ReliquaryItem) -> Entity {
        let mesh = MeshResource.generateBox(size: 0.22, cornerRadius: 0.015)
        let material = SimpleMaterial(color: .init(red: 0.62, green: 0.5, blue: 0.28, alpha: 1.0), isMetallic: true)
        let model = ModelEntity(mesh: mesh, materials: [material])
        let wrapper = Entity()
        wrapper.name = "reliquary_placeholder_\(item.id)"
        wrapper.addChild(model)
        wrapper.scale = SIMD3<Float>(repeating: item.defaultScale)
        makeTargetable(wrapper)
        return wrapper
    }

    /// Collision + input target: required for visionOS `targetedToAnyEntity`
    /// gestures, and useful for future iOS visual effects. Collision is
    /// (re)generated at the entity's current scale — call again after
    /// gesture-scale settles so targeting stays accurate.
    static func makeTargetable(_ entity: Entity) {
        entity.components.set(InputTargetComponent(allowedInputTypes: [.direct, .indirect]))
        entity.generateCollisionShapes(recursive: true)
    }
}

/// A placed reliquary and everything needed to manipulate it.
///
/// A struct (not an Entity subclass) on purpose: keeps RealityKit's class
/// hierarchy at arm's length, makes the manipulation arithmetic plain and
/// testable, and lets the shared interaction model own a homogeneous
/// collection regardless of platform.
@MainActor
public struct PlacedReliquary: Identifiable, Equatable {
    public let id: ReliquaryPlacementHandle
    public let item: ReliquaryItem

    /// The wrapper entity that is parented to the platform anchor.
    /// All gesture deltas apply to this wrapper (anchor stays world-fixed).
    public let root: Entity

    /// Multiplier on `item.defaultScale`, clamped to `item.scaleBounds`.
    /// Writable within the module so the interaction model's
    /// start-anchored gesture API can snapshot/restore it.
    public internal(set) var scaleMultiplier: Float

    public init(id: ReliquaryPlacementHandle, item: ReliquaryItem, root: Entity) {
        self.id = id
        self.item = item
        self.root = root
        self.scaleMultiplier = 1
        // Normalize regardless of what the loader did, so the scale
        // contract (defaultScale × multiplier) always holds.
        root.scale = SIMD3<Float>(repeating: item.defaultScale)
    }

    // Identity-based equality (Entity is a class).
    public static func == (lhs: PlacedReliquary, rhs: PlacedReliquary) -> Bool {
        lhs.id == rhs.id && lhs.root === rhs.root
    }

    // MARK: - Manipulation (shared by both platforms' gestures)

    public mutating func applyScaleDelta(_ delta: Float) {
        let next = PlacementMath.clampedUniformScale(
            current: scaleMultiplier,
            delta: delta,
            bounds: PlacedReliquary.multiplierBounds(for: item)
        )
        scaleMultiplier = next
        root.scale = SIMD3<Float>(repeating: item.defaultScale * next)
    }

    /// Scale-multiplier bounds derived from the item's absolute bounds
    /// (defaultScale × multiplier must stay within `item.scaleBounds`).
    static func multiplierBounds(for item: ReliquaryItem) -> ClosedRange<Float> {
        let lower = max(0.05, item.scaleBounds.lowerBound / max(item.defaultScale, 0.001))
        let upper = max(lower, item.scaleBounds.upperBound / max(item.defaultScale, 0.001))
        return lower ... upper
    }

    public mutating func applyYawDelta(_ radians: Float) {
        // The wrapper is parented under a world-fixed anchor whose
        // transform is a pure upright basis, so local Y == world up:
        // a yaw-only delta cannot disturb pitch/roll.
        let delta = PlacementMath.yawDelta(radians)
        root.orientation = delta * root.orientation
    }

    /// Gesture targeting resolves through collision; regenerate after the
    /// scale settles so the collider matches the rendered size.
    public mutating func regenerateCollision() {
        ReliquaryAssetLoader.makeTargetable(root)
    }

    /// True if `entity` is the wrapper or any descendant of it.
    public func contains(_ entity: Entity) -> Bool {
        var current: Entity? = entity
        while let node = current {
            if node === root { return true }
            current = node.parent
        }
        return false
    }
}

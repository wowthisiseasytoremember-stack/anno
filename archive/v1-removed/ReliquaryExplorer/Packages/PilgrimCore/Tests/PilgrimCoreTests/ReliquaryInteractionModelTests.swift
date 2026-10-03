import PilgrimCore
import RealityKit
import simd
import XCTest

@testable import PilgrimCore

// MARK: - Fake session service (no ARKit/ARView required)

@MainActor
final class FakeReliquarySessionService: ReliquarySessionServicing {
    var supportsScreenSpacePlacement = true
    let events: AsyncStream<ReliquarySessionEvent>
    private let continuation: AsyncStream<ReliquarySessionEvent>.Continuation

    var currentViewRay: WorldRay? = WorldRay(origin: SIMD3<Float>(0, 1.6, 0), direction: SIMD3<Float>(0, -0.1, -1))

    private(set) var activateCallCount = 0
    private(set) var deactivated = false
    private(set) var placedEntities: [Entity] = []
    private(set) var placedTransforms: [simd_float4x4] = []
    private(set) var removedHandleIDs: [UUID] = []
    private(set) var transientEntities: [Entity] = []

    var screenPointHit: SurfaceHit?
    var rayHit: SurfaceHit?

    init() {
        var localContinuation: AsyncStream<ReliquarySessionEvent>.Continuation!
        events = AsyncStream { localContinuation = $0 }
        continuation = localContinuation
    }

    func emit(_ event: ReliquarySessionEvent) {
        continuation.yield(event)
    }

    func activate() async throws {
        activateCallCount += 1
    }

    func deactivate() {
        deactivated = true
    }

    func surfaceHit(atScreenPoint point: CGPoint) -> SurfaceHit? {
        screenPointHit
    }

    func surfaceHit(along ray: WorldRay, maxLength: Float) -> SurfaceHit? {
        rayHit
    }

    func place(_ entity: Entity, at worldTransform: simd_float4x4) async throws -> ReliquaryPlacementHandle {
        placedEntities.append(entity)
        placedTransforms.append(worldTransform)
        return ReliquaryPlacementHandle()
    }

    func removePlacement(_ handle: ReliquaryPlacementHandle) {
        removedHandleIDs.append(handle.id)
    }

    func addTransientEntity(_ entity: Entity) {
        transientEntities.append(entity)
    }

    func removeTransientEntity(_ entity: Entity) {
        transientEntities.removeAll { $0 === entity }
    }
}

// MARK: - Tests

@MainActor
final class ReliquaryInteractionModelTests: XCTestCase {
    private let item = ReliquaryItem(
        id: "test_reliquary",
        title: "Test Reliquary",
        era: "Test Era",
        modelAssetName: "DoesNotExist",
        defaultScale: 0.5,
        scaleBounds: 0.1 ... 1.5,
        historicalNotes: "Test"
    )

    private func makeModel(service: FakeReliquarySessionService) -> ReliquaryInteractionModel {
        ReliquaryInteractionModel(
            session: service,
            initialSelection: item,
            assetLoader: { [item] _ in
                // Bypass bundle loading entirely — deterministic tests.
                let entity = Entity()
                entity.name = "stub_asset"
                entity.components.set(InputTargetComponent())
                return entity
            }
        )
    }

    private func flushLoops() async {
        try? await Task.sleep(nanoseconds: 150_000_000)
    }

    private var sampleHit: SurfaceHit {
        var transform = matrix_identity_float4x4
        transform.columns.3 = SIMD4<Float>(0.2, -0.6, -1.0, 1)
        return SurfaceHit(worldTransform: transform, surfaceNormal: SIMD3<Float>(0, 1, 0))
    }

    func testBeginSessionTransitionsToReadyWhenSurfacesAppear() async {
        let service = FakeReliquarySessionService()
        let model = makeModel(service: service)

        await model.beginSession()
        XCTAssertEqual(model.phase, .searchingSurface)

        service.emit(.surfaceAvailabilityChanged(isReady: true))
        await flushLoops()
        XCTAssertEqual(model.phase, .readyToPlace)
        XCTAssertEqual(service.activateCallCount, 1)
    }

    func testScreenPointPlacementProducesUprightWorldTransform() async {
        let service = FakeReliquarySessionService()
        service.screenPointHit = sampleHit
        let model = makeModel(service: service)

        await model.beginSession()
        service.emit(.surfaceAvailabilityChanged(isReady: true))
        await flushLoops()

        await model.confirmPlacement(atScreenPoint: CGPoint(x: 200, y: 400))

        XCTAssertEqual(model.placements.count, 1)
        XCTAssertEqual(model.phase, .placed(itemID: item.id))
        XCTAssertEqual(service.placedEntities.count, 1)

        let transform = service.placedTransforms[0]
        XCTAssertEqual(transform.columns.3.x, 0.2, accuracy: 1e-4)
        XCTAssertEqual(transform.columns.3.y, -0.6, accuracy: 1e-4)
        XCTAssertEqual(transform.columns.3.z, -1.0, accuracy: 1e-4)
        XCTAssertEqual(transform.columns.1.y, 1, accuracy: 1e-3, "Up axis aligned with surface normal")
        // Facing: the basis Z axis points *away* from the viewer at
        // (0, 1.6, 0), so -Z (object forward) faces them.
        XCTAssertLessThan(transform.columns.2.z, -0.9)
    }

    func testPlacementWithoutSurfacePulsesMissHint() async {
        let service = FakeReliquarySessionService()
        service.screenPointHit = nil
        let model = makeModel(service: service)

        await model.beginSession()
        service.emit(.surfaceAvailabilityChanged(isReady: true))
        await flushLoops()

        await model.confirmPlacement(atScreenPoint: CGPoint(x: 100, y: 100))
        XCTAssertTrue(model.surfaceMissPulse)
        XCTAssertTrue(model.placements.isEmpty)
    }

    func testGazeReticlePlacementUsesRayHit() async {
        let service = FakeReliquarySessionService()
        service.supportsScreenSpacePlacement = false
        service.rayHit = sampleHit
        let model = makeModel(service: service)

        await model.beginSession()
        service.emit(.surfaceAvailabilityChanged(isReady: true))
        await flushLoops()

        await model.confirmPlacement(atScreenPoint: nil)
        XCTAssertEqual(model.placements.count, 1, "visionOS-style tap places at the reticle hit")
    }

    func testScaleDeltaClampsToItemBounds() async {
        let service = FakeReliquarySessionService()
        service.screenPointHit = sampleHit
        let model = makeModel(service: service)

        await model.beginSession()
        service.emit(.surfaceAvailabilityChanged(isReady: true))
        await flushLoops()
        await model.confirmPlacement(atScreenPoint: CGPoint(x: 50, y: 50))

        let root = model.placements[0].root
        XCTAssertEqual(root.scale.x, item.defaultScale, accuracy: 1e-5)

        model.handleScaleDelta(10) // way past upper bound (1.5)
        XCTAssertEqual(root.scale.x, 1.5, accuracy: 1e-4)

        model.handleScaleDelta(0.0001) // below lower bound (0.1)
        XCTAssertEqual(root.scale.x, 0.1, accuracy: 1e-4)
    }

    func testYawDeltaRotatesOnlyYaw() async {
        let service = FakeReliquarySessionService()
        service.screenPointHit = sampleHit
        let model = makeModel(service: service)

        await model.beginSession()
        service.emit(.surfaceAvailabilityChanged(isReady: true))
        await flushLoops()
        await model.confirmPlacement(atScreenPoint: CGPoint(x: 50, y: 50))

        let root = model.placements[0].root
        let before = root.orientation
        model.handleYawDelta(.pi / 2)
        let after = root.orientation

        // Up vector (Y) is invariant under yaw.
        let upBefore = before.act(SIMD3<Float>(0, 1, 0))
        let upAfter = after.act(SIMD3<Float>(0, 1, 0))
        XCTAssertEqual(upAfter.x, upBefore.x, accuracy: 1e-5)
        XCTAssertEqual(upAfter.y, upBefore.y, accuracy: 1e-5)
        XCTAssertEqual(upAfter.z, upBefore.z, accuracy: 1e-5)

        // Forward vector rotated 90° about Y.
        let forwardBefore = before.act(SIMD3<Float>(0, 0, -1))
        let forwardAfter = after.act(SIMD3<Float>(0, 0, -1))
        XCTAssertEqual(
            simd_dot(forwardAfter, simd_cross(SIMD3<Float>(0, 1, 0), forwardBefore)),
            1,
            accuracy: 1e-4
        )
    }

    func testVisionStyleStartAnchoredGesture() async {
        let service = FakeReliquarySessionService()
        service.screenPointHit = sampleHit
        let model = makeModel(service: service)

        await model.beginSession()
        service.emit(.surfaceAvailabilityChanged(isReady: true))
        await flushLoops()
        await model.confirmPlacement(atScreenPoint: CGPoint(x: 50, y: 50))

        let root = model.placements[0].root

        // Absolute magnification of 2× from gesture start.
        model.updateGesture(magnification: 1.7, yawFromGestureStart: 0, on: root)
        XCTAssertEqual(root.scale.x, item.defaultScale * 1.7, accuracy: 1e-4)
        model.updateGesture(magnification: 2.0, yawFromGestureStart: 0, on: root)
        XCTAssertEqual(root.scale.x, item.defaultScale * 2.0, accuracy: 1e-4,
                       "Absolute gesture values anchor to gesture start")

        // Clamp still applies.
        model.updateGesture(magnification: 100, yawFromGestureStart: 0.5, on: root)
        XCTAssertEqual(root.scale.x, 1.5, accuracy: 1e-4)

        model.endGesture()
    }

    func testEndSessionCleansUp() async {
        let service = FakeReliquarySessionService()
        service.screenPointHit = sampleHit
        let model = makeModel(service: service)

        await model.beginSession()
        service.emit(.surfaceAvailabilityChanged(isReady: true))
        await flushLoops()
        await model.confirmPlacement(atScreenPoint: CGPoint(x: 50, y: 50))
        XCTAssertFalse(model.placements.isEmpty)

        model.endSession()
        XCTAssertTrue(model.placements.isEmpty)
        XCTAssertTrue(service.deactivated)
        XCTAssertEqual(model.phase, .idle)
    }

    func testSessionFailureSurfacesInPhase() async {
        let service = FakeReliquarySessionService()
        let model = makeModel(service: service)
        await model.beginSession()

        service.emit(.sessionFailed("Sensor failure"))
        await flushLoops()

        XCTAssertEqual(model.phase, .failed("Sensor failure"))
        XCTAssertFalse(model.isSessionActive)
    }
}

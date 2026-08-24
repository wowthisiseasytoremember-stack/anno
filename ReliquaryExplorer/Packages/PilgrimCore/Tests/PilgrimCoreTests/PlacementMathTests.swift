import PilgrimCore
import simd
import XCTest

@testable import PilgrimCore

final class PlacementMathTests: XCTestCase {
    private func assertApproximatelyEqual(
        _ a: SIMD3<Float>,
        _ b: SIMD3<Float>,
        tolerance: Float = 1e-4,
        file: StaticString = #filePath,
        line: UInt = #line
    ) {
        for i in 0..<3 where abs(a[i] - b[i]) > tolerance {
            XCTFail("\(a) differs from \(b) at index \(i)", file: file, line: line)
        }
    }

    func testBasisIsOrthonormalAndUpright() {
        let basis = PlacementMath.orthonormalBasis(up: SIMD3<Float>(0.05, 1.0, -0.02))
        let x = basis.xAxis, y = basis.yAxis, z = basis.zAxis

        assertApproximatelyEqual(x, simd_normalize(x))
        assertApproximatelyEqual(y, simd_normalize(y))
        assertApproximatelyEqual(z, simd_normalize(z))
        XCTAssertGreaterThan(y.y, 0.99, "Y axis should remain near vertical")
        XCTAssertLessThan(abs(simd_dot(x, y)), 1e-4)
        XCTAssertLessThan(abs(simd_dot(y, z)), 1e-4)
        XCTAssertLessThan(abs(simd_dot(x, z)), 1e-4)
    }

    func testBasisFallsBackForDegenerateNormal() {
        let basis = PlacementMath.orthonormalBasis(up: SIMD3<Float>(0, 0, 0))
        assertApproximatelyEqual(basis.yAxis, SIMD3<Float>(0, 1, 0))
        XCTAssertEqual(basis.xAxis.x, 1, accuracy: 1e-4)
    }

    func testUprightTransformPositionAndUp() {
        let position = SIMD3<Float>(0.3, -0.62, -1.1)
        let transform = PlacementMath.uprightTransform(
            position: position,
            surfaceNormal: SIMD3<Float>(0, 1, 0)
        )

        assertApproximatelyEqual(transform.columns.3.xyz, position)
        assertApproximatelyEqual(transform.columns.1.xyz, SIMD3<Float>(0, 1, 0))
        // Right-handed, no reflection.
        let det = simd_determinant(transform)
        XCTAssertEqual(det, 1, accuracy: 1e-4)
    }

    func testUprightTransformFacesViewpoint() {
        let position = SIMD3<Float>(0, 0, -1.5)
        let viewpoint = SIMD3<Float>(0, 1.6, 0) // user standing in front
        let transform = PlacementMath.uprightTransform(
            position: position,
            surfaceNormal: SIMD3<Float>(0, 1, 0),
            facing: viewpoint
        )

        // The object's forward (-Z basis column negated) should point from
        // the object back toward the (horizontally projected) viewpoint.
        let forward = -transform.columns.2.xyz
        let expected = simd_normalize(SIMD3<Float>(-0.2, 0, 1.0))
        XCTAssertGreaterThan(simd_dot(forward, expected), 0.99,
                             "Placed object should face the viewer")
    }

    func testScaleClamping() {
        XCTAssertEqual(
            PlacementMath.clampedUniformScale(current: 1.0, delta: 1.5, bounds: 0.1...3.0),
            1.5,
            accuracy: 1e-5
        )
        XCTAssertEqual(
            PlacementMath.clampedUniformScale(current: 2.9, delta: 10, bounds: 0.1...3.0),
            3.0,
            accuracy: 1e-5
        )
        XCTAssertEqual(
            PlacementMath.clampedUniformScale(current: 0.2, delta: 0.01, bounds: 0.1...3.0),
            0.1,
            accuracy: 1e-5
        )
        // Invalid deltas are ignored.
        XCTAssertEqual(
            PlacementMath.clampedUniformScale(current: 1.0, delta: .nan, bounds: 0.1...3.0),
            1.0,
            accuracy: 1e-5
        )
        XCTAssertEqual(
            PlacementMath.clampedUniformScale(current: 1.0, delta: 0, bounds: 0.1...3.0),
            1.0,
            accuracy: 1e-5
        )
    }

    func testYawDeltaIsPureYRotation() {
        let q = PlacementMath.yawDelta(.pi / 2)
        let rotated = q.act(SIMD3<Float>(0, 0, -1))
        assertApproximatelyEqual(rotated, SIMD3<Float>(-1, 0, 0), tolerance: 1e-4)

        // Zero delta is identity.
        let identity = PlacementMath.yawDelta(0)
        assertApproximatelyEqual(
            identity.act(SIMD3<Float>(1, 2, 3)),
            SIMD3<Float>(1, 2, 3),
            tolerance: 1e-6
        )

        // Yaw never disturbs a vertical vector.
        let up = q.act(SIMD3<Float>(0, 1, 0))
        assertApproximatelyEqual(up, SIMD3<Float>(0, 1, 0), tolerance: 1e-6)
    }

    func testRayDestination() {
        let ray = WorldRay(origin: SIMD3<Float>(0, 0, 0), direction: SIMD3<Float>(0, 0, -2))
        assertApproximatelyEqual(
            PlacementMath.destination(of: ray, maxLength: 5),
            SIMD3<Float>(0, 0, -5)
        )
    }
}

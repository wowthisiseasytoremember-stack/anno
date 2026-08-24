import Foundation
import simd

/// Pure placement/transform math shared by the iOS and visionOS AR
/// implementations. No RealityKit dependency — directly unit-testable.
///
/// Both platforms reduce interaction to the *same* deltas:
///
/// - placement: an (optional camera-facing) position + surface normal →
///   an upright world transform,
/// - scale: a multiplicative delta, clamped,
/// - rotation: a yaw delta quaternion about the local Y axis, leaving
///   pitch/roll untouched.
public enum PlacementMath {
    // MARK: - Basis construction

    /// Orthonormal basis with `up` as the Y axis. Returns
    /// `(xAxis, yAxis, zAxis)`. Degenerate inputs fall back to the world
    /// identity basis so placement never produces NaN transforms.
    public static func orthonormalBasis(
        up rawUp: SIMD3<Float>
    ) -> (xAxis: SIMD3<Float>, yAxis: SIMD3<Float>, zAxis: SIMD3<Float>) {
        var up = simd_normalize(rawUp)
        if !up.x.isFinite || simd_length(up) < 1e-6 {
            up = SIMD3<Float>(0, 1, 0)
        }

        // Prefer keeping the object's yaw aligned with world -Z (facing
        // the initial viewpoint), projected onto the plane orthogonal to `up`.
        let worldForward = SIMD3<Float>(0, 0, -1)
        var forward = worldForward - up * simd_dot(worldForward, up)
        if simd_length(forward) < 1e-4 {
            forward = SIMD3<Float>(0, 0, 1) - up * simd_dot(SIMD3<Float>(0, 0, 1), up)
        }
        forward = simd_normalize(forward)

        // RealityKit: -Z is forward, so the basis Z axis points *backward*.
        let zAxis = -forward
        var xAxis = simd_cross(up, zAxis)
        if simd_length(xAxis) < 1e-4 {
            xAxis = SIMD3<Float>(1, 0, 0)
        }
        xAxis = simd_normalize(xAxis)
        let yAxis = simd_normalize(simd_cross(zAxis, xAxis))

        return (xAxis, yAxis, zAxis)
    }

    /// World transform placing an object upright on a surface:
    /// Y axis aligned with the surface normal (≈ +Y for a horizontal
    /// plane), object standing at `position`, yaw chosen to face
    /// `viewpoint` when provided.
    public static func uprightTransform(
        position: SIMD3<Float>,
        surfaceNormal: SIMD3<Float>,
        facing viewpoint: SIMD3<Float>? = nil
    ) -> simd_float4x4 {
        let basis = orthonormalBasis(up: surfaceNormal)

        if let viewpoint {
            // Orient the object's forward (-Z) horizontally toward the
            // viewer so the reliquary presents itself on placement.
            var toView = viewpoint - position
            toView = toView - basis.yAxis * simd_dot(toView, basis.yAxis)
            if simd_length(toView) > 1e-4 {
                let zAxis = -simd_normalize(toView)
                var xAxis = simd_cross(basis.yAxis, zAxis)
                if simd_length(xAxis) < 1e-4 {
                    return simd_float4x4(
                        columns: (
                            basis.xAxis, basis.yAxis, basis.zAxis, SIMD4(position, 1)
                        )
                    )
                }
                xAxis = simd_normalize(xAxis)
                let yAxis = simd_normalize(simd_cross(zAxis, xAxis))
                return simd_float4x4(
                    columns: (xAxis, yAxis, zAxis, SIMD4(position, 1))
                )
            }
        }

        return simd_float4x4(
            columns: (basis.xAxis, basis.yAxis, basis.zAxis, SIMD4(position, 1))
        )
    }

    // MARK: - Manipulation

    /// Multiplies the current scale by `delta` and clamps into `bounds`.
    public static func clampedUniformScale(
        current: Float,
        delta: Float,
        bounds: ClosedRange<Float>
    ) -> Float {
        guard delta.isFinite, delta > 0 else { return current }
        let next = current * delta
        if !next.isFinite { return bounds.upperBound }
        return min(max(next, bounds.lowerBound), bounds.upperBound)
    }

    /// Yaw-only rotation delta about the local Y axis.
    public static func yawDelta(_ radians: Float) -> simd_quatf {
        let axis = simd_normalize(SIMD3<Float>(0, 1, 0))
        return simd_quatf(angle: radians, axis: axis)
    }

    // MARK: - Ray helpers

    public static func destination(of ray: WorldRay, maxLength: Float) -> SIMD3<Float> {
        let length = simd_length(ray.direction)
        let dir = length > 1e-6 ? ray.direction / length : SIMD3<Float>(0, 0, -1)
        return ray.origin + dir * maxLength
    }
}

"""NumPy exercises for coordinate frames and the pinhole camera model.

The public functions use batched row arrays for convenient NumPy calls, while
the frame notation in their contracts follows the usual column-vector math:
``p_A = T_A_B @ p_B``. All returned arrays must be newly allocated float64
arrays, and no function may mutate a caller-owned input.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def homogenize_points(points: ArrayLike) -> NDArray[np.float64]:
    """Append a homogeneous coordinate of one to every 2-D or 3-D point.

    ``points`` must be a finite array of shape ``(N, D)`` where ``D`` is 2 or
    3. Empty batches are valid. Reject malformed or nonfinite inputs.
    """

    # LEARNER TODO: validate the batch and append the coordinate that makes
    # translation act on points.
    raise NotImplementedError("implement homogenize_points")


def homogenize_vectors(vectors: ArrayLike) -> NDArray[np.float64]:
    """Append a homogeneous coordinate of zero to every 2-D or 3-D vector.

    ``vectors`` has the same shape and finiteness contract as
    :func:`homogenize_points`. The zero coordinate makes translations leave
    free vectors/directions unchanged.
    """

    # LEARNER TODO: preserve the vector components and append the homogeneous
    # coordinate appropriate for a direction rather than a location.
    raise NotImplementedError("implement homogenize_vectors")


def dehomogenize_points(points_h: ArrayLike) -> NDArray[np.float64]:
    """Convert homogeneous 2-D or 3-D points back to Euclidean coordinates.

    Accept a finite array with shape ``(N, 3)`` or ``(N, 4)``. Divide each of
    the leading coordinates by that row's final coordinate. A zero final
    coordinate represents a direction or a point at infinity and must raise
    ``ValueError`` rather than produce infinities or NaNs.
    """

    # LEARNER TODO: validate the homogeneous scale before performing the
    # perspective divide.
    raise NotImplementedError("implement dehomogenize_points")


def make_rigid_transform(
    rotation: ArrayLike,
    translation: ArrayLike,
) -> NDArray[np.float64]:
    """Construct an SE(2) or SE(3) homogeneous transformation matrix.

    ``rotation`` must have shape ``(D, D)`` for ``D`` equal to 2 or 3, and
    ``translation`` must have shape ``(D,)``. Require finite values, an
    orthonormal rotation, and determinant ``+1`` (within ``1e-9`` absolute and
    relative tolerance). Reflections and scaled/sheared matrices are invalid.
    The result represents ``p_dst = R_dst_src @ p_src + t_dst_src``.
    """

    # LEARNER TODO: validate a proper rotation and assemble the homogeneous
    # block matrix without changing either input.
    raise NotImplementedError("implement make_rigid_transform")


def transform_points(
    transform_dst_from_src: ArrayLike,
    points_src: ArrayLike,
) -> NDArray[np.float64]:
    """Express a batch of 2-D or 3-D source-frame points in a destination frame.

    ``transform_dst_from_src`` must be a valid rigid ``3x3`` or ``4x4``
    homogeneous matrix, and ``points_src`` must have matching shape ``(N, D)``.
    Validate finiteness and transform points with homogeneous coordinate one.
    """

    # LEARNER TODO: validate matching dimensions, homogenize the points, and
    # apply the named frame transform in the documented direction.
    raise NotImplementedError("implement transform_points")


def transform_vectors(
    transform_dst_from_src: ArrayLike,
    vectors_src: ArrayLike,
) -> NDArray[np.float64]:
    """Rotate 2-D or 3-D vectors between frames without translating them.

    The transform and batch contracts match :func:`transform_points`, but the
    inputs are free vectors/directions and therefore use homogeneous coordinate
    zero. In particular, a pure translation must not change the result.
    """

    # LEARNER TODO: apply only the transformation behavior appropriate for a
    # vector; test the distinction from a point explicitly.
    raise NotImplementedError("implement transform_vectors")


def compose_transforms(
    transform_a_from_b: ArrayLike,
    transform_b_from_c: ArrayLike,
) -> NDArray[np.float64]:
    """Return the rigid transform ``T_A_C = T_A_B @ T_B_C``.

    Both inputs must be finite, valid rigid transforms of the same dimension.
    Composition is ordered: applying the result to coordinates in frame C must
    equal first mapping C to B and then B to A.
    """

    # LEARNER TODO: validate both transforms and compose them in frame order.
    raise NotImplementedError("implement compose_transforms")


def invert_rigid_transform(
    transform_a_from_b: ArrayLike,
) -> NDArray[np.float64]:
    """Return ``T_B_A``, the rigid inverse of ``T_A_B``.

    Accept a finite, valid SE(2) or SE(3) transform. Derive the inverse from
    the rotation and translation blocks; do not use a general-purpose matrix
    inverse. The result must compose with the input to the identity transform.
    """

    # LEARNER TODO: use the structure of a rigid transform to reverse both the
    # rotation and the translated origin.
    raise NotImplementedError("implement invert_rigid_transform")


def make_camera_intrinsics(
    fx: float,
    fy: float,
    cx: float,
    cy: float,
) -> NDArray[np.float64]:
    """Construct the zero-skew pinhole intrinsic matrix ``K``.

    ``fx`` and ``fy`` are focal lengths measured in pixels and must be finite
    and strictly positive. ``(cx, cy)`` is the finite principal point in pixel
    coordinates. The final row is ``[0, 0, 1]``.
    """

    # LEARNER TODO: validate the four scalar parameters and place focal lengths
    # and principal-point offsets in their conventional matrix positions.
    raise NotImplementedError("implement make_camera_intrinsics")


def project_camera_points(
    points_camera: ArrayLike,
    intrinsics: ArrayLike,
) -> NDArray[np.float64]:
    """Project camera-frame 3-D points to ``(u, v)`` pixel coordinates.

    ``points_camera`` must be finite with shape ``(N, 3)``. ``intrinsics``
    must be a finite, zero-skew matrix with the exact structural form produced
    by :func:`make_camera_intrinsics`. Every camera-frame depth ``Z`` must be
    strictly positive; if any point lies on or behind the camera plane, raise
    ``ValueError`` for the whole call before dividing. Empty batches return an
    array with shape ``(0, 2)``.
    """

    # LEARNER TODO: apply K to camera coordinates and perform the perspective
    # divide only after validating the physical depth domain.
    raise NotImplementedError("implement project_camera_points")


def project_world_points(
    points_world: ArrayLike,
    camera_from_world: ArrayLike,
    intrinsics: ArrayLike,
) -> NDArray[np.float64]:
    """Project world-frame points using ``p ~ K [R_C_W | t_C_W] P_W``.

    ``camera_from_world`` is the extrinsic transform ``T_C_W`` mapping world
    coordinates into the camera frame; it is not the camera pose ``T_W_C``.
    Require a valid 4x4 rigid transform, world points of shape ``(N, 3)``, and
    the same intrinsic/depth rules as :func:`project_camera_points`.
    """

    # LEARNER TODO: change frames with the extrinsic transform, then project
    # through the camera model while preserving all validation contracts.
    raise NotImplementedError("implement project_world_points")


def pixels_to_normalized_camera(
    pixels_uv: ArrayLike,
    intrinsics: ArrayLike,
) -> NDArray[np.float64]:
    """Map pixels to normalized camera-plane coordinates ``(x_n, y_n)``.

    ``pixels_uv`` must be a finite ``(N, 2)`` array in column-row order, and
    ``intrinsics`` follows the same contract as in projection. Remove the
    intrinsic mapping so that ``(x_n, y_n, 1)`` is a camera-frame ray before
    unit-length normalization. Empty batches are valid.
    """

    # LEARNER TODO: undo focal scaling and the principal-point offset without
    # assuming that pixel coordinates are NumPy (row, column) indices.
    raise NotImplementedError("implement pixels_to_normalized_camera")


def pixels_to_camera_rays(
    pixels_uv: ArrayLike,
    intrinsics: ArrayLike,
) -> NDArray[np.float64]:
    """Return one unit-length, positive-Z camera-frame ray per pixel.

    Inputs follow :func:`pixels_to_normalized_camera`. Lift each normalized
    coordinate to the pinhole direction through ``(x_n, y_n, 1)`` and return a
    finite array of shape ``(N, 3)`` whose rows have Euclidean norm one. This
    operation cannot recover metric depth from a single pixel.
    """

    # LEARNER TODO: construct and normalize each ray while preserving the empty
    # batch and nonmutation contracts.
    raise NotImplementedError("implement pixels_to_camera_rays")

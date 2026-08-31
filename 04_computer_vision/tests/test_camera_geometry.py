from __future__ import annotations

import os

import numpy as np
import pytest

from computer_vision.camera_geometry import (
    compose_transforms,
    dehomogenize_points,
    homogenize_points,
    homogenize_vectors,
    invert_rigid_transform,
    make_camera_intrinsics,
    make_rigid_transform,
    pixels_to_camera_rays,
    pixels_to_normalized_camera,
    project_camera_points,
    project_world_points,
    transform_points,
    transform_vectors,
)


pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_CV_EXERCISES") != "1",
    reason="set RUN_CV_EXERCISES=1 to run learner challenges",
)


def test_homogeneous_points_and_vectors_have_distinct_w_without_mutation() -> None:
    values = np.array([[2, -1], [0, 3]], dtype=np.int64)
    original = values.copy()

    points_h = homogenize_points(values)
    vectors_h = homogenize_vectors(values)

    np.testing.assert_array_equal(points_h, [[2.0, -1.0, 1.0], [0.0, 3.0, 1.0]])
    np.testing.assert_array_equal(vectors_h, [[2.0, -1.0, 0.0], [0.0, 3.0, 0.0]])
    assert points_h.dtype == np.float64
    assert vectors_h.dtype == np.float64
    np.testing.assert_array_equal(values, original)


def test_dehomogenize_points_performs_the_scale_divide() -> None:
    points_h = np.array([[4.0, 6.0, 2.0], [-3.0, 6.0, -3.0]])

    actual = dehomogenize_points(points_h)

    np.testing.assert_allclose(actual, [[2.0, 3.0], [1.0, -2.0]])


def test_dehomogenize_rejects_a_point_at_infinity() -> None:
    with pytest.raises(ValueError):
        dehomogenize_points([[1.0, 2.0, 0.0]])


@pytest.mark.parametrize(
    "bad_values",
    [
        np.ones(2),
        np.ones((1, 1)),
        np.ones((1, 4)),
        np.array([[1.0, np.inf]]),
    ],
)
def test_homogenize_rejects_malformed_or_nonfinite_batches(
    bad_values: np.ndarray,
) -> None:
    with pytest.raises(ValueError):
        homogenize_points(bad_values)
    with pytest.raises(ValueError):
        homogenize_vectors(bad_values)


def test_two_dimensional_transform_translates_points_but_not_vectors() -> None:
    rotation_a_from_b = np.array([[0.0, -1.0], [1.0, 0.0]])
    transform_a_from_b = make_rigid_transform(rotation_a_from_b, [10.0, 20.0])

    np.testing.assert_allclose(
        transform_a_from_b,
        [[0.0, -1.0, 10.0], [1.0, 0.0, 20.0], [0.0, 0.0, 1.0]],
        atol=1e-12,
    )
    np.testing.assert_allclose(
        transform_points(transform_a_from_b, [[1.0, 0.0]]),
        [[10.0, 21.0]],
        atol=1e-12,
    )
    np.testing.assert_allclose(
        transform_vectors(transform_a_from_b, [[1.0, 0.0]]),
        [[0.0, 1.0]],
        atol=1e-12,
    )


@pytest.mark.parametrize(
    "bad_rotation",
    [
        np.diag([2.0, 1.0]),
        np.diag([-1.0, 1.0]),
        np.ones((2, 3)),
        np.array([[1.0, 0.0], [0.0, np.inf]]),
    ],
)
def test_rigid_transform_rejects_non_rotations(bad_rotation: np.ndarray) -> None:
    with pytest.raises(ValueError):
        make_rigid_transform(bad_rotation, np.zeros(2))


def test_transform_rejects_a_translation_with_the_wrong_dimension() -> None:
    with pytest.raises(ValueError):
        make_rigid_transform(np.eye(3), np.zeros(2))


@pytest.mark.parametrize(
    "bad_transform",
    [
        np.eye(2),
        np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 1.0]]),
        np.diag([-1.0, 1.0, 1.0]),
    ],
)
def test_transform_points_rejects_a_malformed_rigid_transform(
    bad_transform: np.ndarray,
) -> None:
    with pytest.raises(ValueError):
        transform_points(bad_transform, [[0.0, 0.0]])


def test_composition_follows_named_frame_order() -> None:
    rotation_b_from_c = np.array(
        [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    )
    transform_a_from_b = make_rigid_transform(np.eye(3), [1.0, 0.0, 0.0])
    transform_b_from_c = make_rigid_transform(rotation_b_from_c, [0.0, 2.0, 0.0])
    point_c = np.array([[1.0, 0.0, 0.0]])

    transform_a_from_c = compose_transforms(transform_a_from_b, transform_b_from_c)
    direct = transform_points(transform_a_from_c, point_c)
    sequential = transform_points(
        transform_a_from_b,
        transform_points(transform_b_from_c, point_c),
    )

    np.testing.assert_allclose(transform_a_from_c[:3, 3], [1.0, 2.0, 0.0])
    np.testing.assert_allclose(direct, [[1.0, 3.0, 0.0]], atol=1e-12)
    np.testing.assert_allclose(direct, sequential, atol=1e-12)


def test_rigid_inverse_round_trips_points_and_composes_to_identity() -> None:
    rotation_a_from_b = np.array(
        [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    )
    transform_a_from_b = make_rigid_transform(rotation_a_from_b, [2.0, -1.0, 3.0])
    points_b = np.array([[1.0, 2.0, 4.0], [-3.0, 0.5, 2.0]])

    transform_b_from_a = invert_rigid_transform(transform_a_from_b)
    round_trip = transform_points(
        transform_b_from_a,
        transform_points(transform_a_from_b, points_b),
    )

    np.testing.assert_allclose(round_trip, points_b, atol=1e-12)
    np.testing.assert_allclose(
        compose_transforms(transform_a_from_b, transform_b_from_a),
        np.eye(4),
        atol=1e-12,
    )


def test_two_dimensional_composition_and_inverse_follow_frame_order() -> None:
    rotation_a_from_b = np.array([[0.0, -1.0], [1.0, 0.0]])
    transform_a_from_b = make_rigid_transform(rotation_a_from_b, [2.0, -1.0])
    transform_b_from_c = make_rigid_transform(np.eye(2), [3.0, 4.0])
    points_c = np.array([[1.0, 2.0], [-2.0, 5.0]])

    transform_a_from_c = compose_transforms(transform_a_from_b, transform_b_from_c)
    transform_c_from_a = invert_rigid_transform(transform_a_from_c)
    points_a = transform_points(transform_a_from_c, points_c)

    np.testing.assert_allclose(
        points_a,
        transform_points(
            transform_a_from_b,
            transform_points(transform_b_from_c, points_c),
        ),
        atol=1e-12,
    )
    np.testing.assert_allclose(
        transform_points(transform_c_from_a, points_a),
        points_c,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        compose_transforms(transform_a_from_c, transform_c_from_a),
        np.eye(3),
        atol=1e-12,
    )


def test_intrinsic_matrix_places_focal_lengths_and_principal_point() -> None:
    actual = make_camera_intrinsics(400.0, 500.0, 320.0, 240.0)

    np.testing.assert_array_equal(
        actual,
        [[400.0, 0.0, 320.0], [0.0, 500.0, 240.0], [0.0, 0.0, 1.0]],
    )
    assert actual.dtype == np.float64


@pytest.mark.parametrize(
    ("fx", "fy", "cx", "cy"),
    [
        (0.0, 1.0, 0.0, 0.0),
        (1.0, -1.0, 0.0, 0.0),
        (1.0, 1.0, np.nan, 0.0),
        (1.0, 1.0, 0.0, np.inf),
    ],
)
def test_intrinsic_matrix_rejects_invalid_parameters(
    fx: float,
    fy: float,
    cx: float,
    cy: float,
) -> None:
    with pytest.raises(ValueError):
        make_camera_intrinsics(fx, fy, cx, cy)


def test_known_camera_points_project_to_hand_checkable_pixels() -> None:
    intrinsics = make_camera_intrinsics(100.0, 200.0, 320.0, 240.0)
    points_camera = np.array(
        [[0.0, 0.0, 2.0], [2.0, 1.0, 2.0], [-1.0, -1.0, 1.0]]
    )
    original = points_camera.copy()

    actual = project_camera_points(points_camera, intrinsics)

    np.testing.assert_allclose(actual, [[320.0, 240.0], [420.0, 340.0], [220.0, 40.0]])
    assert actual.dtype == np.float64
    np.testing.assert_array_equal(points_camera, original)


def test_projection_is_invariant_to_positive_depth_scale_and_handles_empty_batch() -> None:
    intrinsics = make_camera_intrinsics(80.0, 60.0, 10.0, 20.0)

    first = project_camera_points([[1.0, 2.0, 4.0]], intrinsics)
    second = project_camera_points([[2.0, 4.0, 8.0]], intrinsics)
    empty = project_camera_points(np.empty((0, 3)), intrinsics)

    np.testing.assert_allclose(first, second, atol=1e-12)
    assert empty.shape == (0, 2)
    assert empty.dtype == np.float64


@pytest.mark.parametrize("depth", [0.0, -1.0])
def test_projection_rejects_points_on_or_behind_camera_plane(depth: float) -> None:
    intrinsics = make_camera_intrinsics(100.0, 100.0, 0.0, 0.0)
    points_camera = np.array([[0.0, 0.0, 1.0], [1.0, 2.0, depth]])

    with pytest.raises(ValueError):
        project_camera_points(points_camera, intrinsics)


def test_world_projection_uses_world_to_camera_extrinsics() -> None:
    intrinsics = make_camera_intrinsics(100.0, 50.0, 320.0, 240.0)
    # The camera center is (1, 2, 0) in world coordinates with no rotation, so
    # T_C_W translates the world by the negative camera-center coordinates.
    camera_from_world = make_rigid_transform(np.eye(3), [-1.0, -2.0, 0.0])
    points_world = np.array([[1.0, 2.0, 2.0], [3.0, 4.0, 2.0]])

    actual = project_world_points(points_world, camera_from_world, intrinsics)

    np.testing.assert_allclose(actual, [[320.0, 240.0], [420.0, 290.0]], atol=1e-12)


def test_world_projection_applies_extrinsic_rotation_before_projection() -> None:
    intrinsics = make_camera_intrinsics(100.0, 50.0, 320.0, 240.0)
    rotation_camera_from_world = np.array(
        [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    )
    camera_from_world = make_rigid_transform(
        rotation_camera_from_world,
        [1.0, -2.0, 0.0],
    )
    points_world = np.array([[2.0, 1.0, 4.0], [2.0, -3.0, 4.0]])

    actual = project_world_points(points_world, camera_from_world, intrinsics)

    np.testing.assert_allclose(actual, [[320.0, 240.0], [420.0, 240.0]], atol=1e-12)


def test_pixels_map_to_normalized_camera_coordinates() -> None:
    intrinsics = make_camera_intrinsics(2.0, 4.0, 10.0, 20.0)
    pixels = np.array([[10.0, 20.0], [12.0, 24.0], [8.0, 16.0]])

    actual = pixels_to_normalized_camera(pixels, intrinsics)

    np.testing.assert_allclose(actual, [[0.0, 0.0], [1.0, 1.0], [-1.0, -1.0]])


def test_pixel_rays_are_unit_length_positive_z_and_reproject() -> None:
    intrinsics = make_camera_intrinsics(2.0, 4.0, 10.0, 20.0)
    pixels = np.array([[10.0, 20.0], [12.0, 20.0], [10.0, 24.0]])

    rays = pixels_to_camera_rays(pixels, intrinsics)

    root_two = np.sqrt(2.0)
    expected = np.array(
        [
            [0.0, 0.0, 1.0],
            [1.0 / root_two, 0.0, 1.0 / root_two],
            [0.0, 1.0 / root_two, 1.0 / root_two],
        ]
    )
    np.testing.assert_allclose(rays, expected, atol=1e-12)
    np.testing.assert_allclose(np.linalg.norm(rays, axis=1), np.ones(3), atol=1e-12)
    assert np.all(rays[:, 2] > 0.0)
    empty = pixels_to_camera_rays(np.empty((0, 2)), intrinsics)
    assert empty.shape == (0, 3)
    assert empty.dtype == np.float64

    depths_along_ray = np.array([[2.0], [5.0], [3.0]])
    np.testing.assert_allclose(
        project_camera_points(rays * depths_along_ray, intrinsics),
        pixels,
        atol=1e-12,
    )


@pytest.mark.parametrize(
    "bad_points",
    [
        np.ones(3),
        np.ones((2, 2)),
        np.array([[0.0, 0.0, np.nan]]),
    ],
)
def test_camera_projection_rejects_malformed_or_nonfinite_points(
    bad_points: np.ndarray,
) -> None:
    with pytest.raises(ValueError):
        project_camera_points(bad_points, np.eye(3))


@pytest.mark.parametrize(
    "bad_intrinsics",
    [
        np.eye(2),
        np.array([[1.0, 0.1, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
        np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 1.0]]),
        np.diag([-1.0, 1.0, 1.0]),
    ],
)
def test_camera_operations_reject_noncanonical_intrinsics(
    bad_intrinsics: np.ndarray,
) -> None:
    with pytest.raises(ValueError):
        project_camera_points([[0.0, 0.0, 1.0]], bad_intrinsics)
    with pytest.raises(ValueError):
        pixels_to_normalized_camera([[0.0, 0.0]], bad_intrinsics)


@pytest.mark.parametrize(
    "bad_pixels",
    [np.ones(2), np.ones((1, 3)), np.array([[0.0, np.nan]])],
)
def test_inverse_projection_rejects_malformed_or_nonfinite_pixels(
    bad_pixels: np.ndarray,
) -> None:
    with pytest.raises(ValueError):
        pixels_to_normalized_camera(bad_pixels, np.eye(3))
    with pytest.raises(ValueError):
        pixels_to_camera_rays(bad_pixels, np.eye(3))

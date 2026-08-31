from __future__ import annotations

from computer_vision import camera_geometry, conv_pool


def test_vision_primitive_module_imports() -> None:
    assert callable(conv_pool.output_size)
    assert callable(conv_pool.conv2d_nchw)
    assert callable(conv_pool.max_pool2d_nchw)
    assert callable(conv_pool.average_pool2d_nchw)


def test_camera_geometry_module_imports() -> None:
    assert callable(camera_geometry.homogenize_points)
    assert callable(camera_geometry.homogenize_vectors)
    assert callable(camera_geometry.dehomogenize_points)
    assert callable(camera_geometry.make_rigid_transform)
    assert callable(camera_geometry.transform_points)
    assert callable(camera_geometry.transform_vectors)
    assert callable(camera_geometry.compose_transforms)
    assert callable(camera_geometry.invert_rigid_transform)
    assert callable(camera_geometry.make_camera_intrinsics)
    assert callable(camera_geometry.project_camera_points)
    assert callable(camera_geometry.project_world_points)
    assert callable(camera_geometry.pixels_to_normalized_camera)
    assert callable(camera_geometry.pixels_to_camera_rays)

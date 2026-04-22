"""Phase 2 transform adapter for depth-pixel to world projection."""

from __future__ import annotations

import math
from dataclasses import dataclass

from board_observer import CameraIntrinsics, PixelUV, TransformProvider
from models import XYZ

Matrix4 = tuple[
    tuple[float, float, float, float],
    tuple[float, float, float, float],
    tuple[float, float, float, float],
    tuple[float, float, float, float],
]


def identity_matrix4() -> Matrix4:
    """Return a 4x4 identity matrix."""

    return (
        (1.0, 0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    )


def matrix_from_translation_rpy(
    translation_xyz: XYZ,
    rpy_rad: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> Matrix4:
    """Build a homogeneous transform from translation and roll/pitch/yaw."""

    roll, pitch, yaw = rpy_rad
    cr, sr = math.cos(roll), math.sin(roll)
    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)

    r00 = cy * cp
    r01 = cy * sp * sr - sy * cr
    r02 = cy * sp * cr + sy * sr
    r10 = sy * cp
    r11 = sy * sp * sr + cy * cr
    r12 = sy * sp * cr - cy * sr
    r20 = -sp
    r21 = cp * sr
    r22 = cp * cr

    tx, ty, tz = translation_xyz
    return (
        (r00, r01, r02, tx),
        (r10, r11, r12, ty),
        (r20, r21, r22, tz),
        (0.0, 0.0, 0.0, 1.0),
    )


@dataclass(frozen=True)
class Phase2TransformProvider(TransformProvider):
    """Depth projection plus camera-to-world rigid transform."""

    camera_frame_name: str = "left_ir_optical_frame"
    world_frame_name: str = "world"
    camera_to_world_matrix: Matrix4 = identity_matrix4()

    def pixel_to_world(
        self,
        pixel_uv: PixelUV,
        depth_m: float,
        intrinsics: CameraIntrinsics | None,
        depth_frame_name: str | None,
    ) -> XYZ | None:
        """Project one depth pixel into world coordinates."""

        if intrinsics is None:
            raise RuntimeError("Phase2TransformProvider requires camera intrinsics.")
        if depth_frame_name is not None and depth_frame_name != self.camera_frame_name:
            raise RuntimeError(
                f"Expected depth frame {self.camera_frame_name!r}, got {depth_frame_name!r}."
            )
        camera_xyz = self.pixel_to_camera(pixel_uv, depth_m, intrinsics)
        return self.camera_to_world(camera_xyz)

    def pixel_to_camera(
        self,
        pixel_uv: PixelUV,
        depth_m: float,
        intrinsics: CameraIntrinsics,
    ) -> XYZ:
        """Project a depth pixel into the optical camera frame."""

        u, v = pixel_uv
        camera_x = (float(u) - intrinsics.cx) * depth_m / intrinsics.fx
        camera_y = (float(v) - intrinsics.cy) * depth_m / intrinsics.fy
        camera_z = float(depth_m)
        return (camera_x, camera_y, camera_z)

    def camera_to_world(self, camera_xyz: XYZ) -> XYZ:
        """Transform a camera-frame point into the world frame."""

        x, y, z = camera_xyz
        matrix = self.camera_to_world_matrix
        world_x = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z + matrix[0][3]
        world_y = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z + matrix[1][3]
        world_z = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z + matrix[2][3]
        return (world_x, world_y, world_z)

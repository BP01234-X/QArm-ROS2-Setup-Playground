"""Bridge-aware kinematics helper for observer-pose analysis."""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from itertools import permutations, product
from pathlib import Path
from typing import Any

import numpy as np
import yaml


def _ensure_import_paths() -> None:
    """Make local project modules importable when run as a standalone script."""

    current = Path(__file__).resolve()
    chess_logic_dir = current.parents[1]
    if str(chess_logic_dir) not in sys.path:
        sys.path.insert(0, str(chess_logic_dir))

    for parent in current.parents:
        candidate = parent / "0_libraries" / "python"
        if (candidate / "hal" / "products" / "qarm.py").exists():
            candidate_str = str(candidate)
            if candidate_str not in sys.path:
                sys.path.insert(0, candidate_str)
            return
    raise RuntimeError("Could not locate local 0_libraries/python for QArmUtilities import.")


_ensure_import_paths()

from board_geometry import BoardGeometry  # noqa: E402
from hal.products.qarm import QArmUtilities  # noqa: E402


WIDTH = 640
HEIGHT = 480
FX = 592.451
FY = 592.451
CX = 318.592
CY = 249.341


@dataclass(frozen=True)
class BridgeFiles:
    """Resolved bridge-facing file paths under codex-testing."""

    bridge_dir: Path
    status_json: Path
    target_pose_json: Path
    camera_status_json: Path


@dataclass(frozen=True)
class BridgeSnapshot:
    """Current bridge and camera state useful for observer-pose reasoning."""

    bridge_state: str | None
    active_goal_id: str | None
    active_goal_pose: tuple[float, float, float, float] | None
    live_task_space_pose: tuple[float, float, float, float] | None
    target_goal_pose: tuple[float, float, float, float] | None
    camera_center_depth_m: float | None
    camera_rgb_shape: tuple[int, int, int] | None
    camera_depth_shape: tuple[int, int] | None


@dataclass(frozen=True)
class PoseScore:
    """Projected-board summary for one observer task-space pose."""

    xyz: tuple[float, float, float]
    wrist: float
    extrinsic_name: str
    projected_center_uv: tuple[float, float] | None
    board_axis_intersection_world: tuple[float, float, float] | None
    visible_corner_count: int
    projected_area_px2: float
    center_error_px: float | None
    axis_error_m: float | None
    axis_depth_m: float | None
    score: float
    phi_optimal: tuple[float, float, float, float]
    camera_world_xyz: tuple[float, float, float]


def rotation_from_rpy(roll: float, pitch: float, yaw: float) -> np.ndarray:
    """Return a 3x3 rotation matrix from ROS-style fixed-axis RPY."""

    cr, sr = math.cos(roll), math.sin(roll)
    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)

    r_x = np.array([[1.0, 0.0, 0.0], [0.0, cr, -sr], [0.0, sr, cr]])
    r_y = np.array([[cp, 0.0, sp], [0.0, 1.0, 0.0], [-sp, 0.0, cp]])
    r_z = np.array([[cy, -sy, 0.0], [sy, cy, 0.0], [0.0, 0.0, 1.0]])
    return r_z @ r_y @ r_x


def make_transform(rotation: np.ndarray, translation_xyz: tuple[float, float, float]) -> np.ndarray:
    """Return a 4x4 homogeneous transform."""

    transform = np.eye(4, dtype=np.float64)
    transform[:3, :3] = rotation
    transform[:3, 3] = np.array(translation_xyz, dtype=np.float64)
    return transform


def camera_extrinsic_from_urdf() -> np.ndarray:
    """Return T_end_effector_to_left_ir_optical using the current measured URDF constants."""

    t_ee_left_ir = make_transform(
        rotation_from_rpy(math.pi, -math.pi / 2.0, 0.0),
        (0.052, 0.039, -0.040),
    )
    t_left_ir_optical = make_transform(
        rotation_from_rpy(-math.pi / 2.0, 0.0, -math.pi / 2.0),
        (0.0, 0.0, 0.0),
    )
    return t_ee_left_ir @ t_left_ir_optical


def tool_frame_correction_hypotheses() -> dict[str, np.ndarray]:
    """Return likely constant frame corrections between FK tool frame and URDF END-EFFECTOR."""

    identity = np.eye(3, dtype=np.float64)
    hypotheses: dict[str, np.ndarray] = {"identity": identity}

    basis = identity
    for perm in permutations(range(3)):
        permuted = basis[:, perm]
        for signs in product((-1.0, 1.0), repeat=3):
            rotation = permuted @ np.diag(signs)
            determinant = float(np.linalg.det(rotation))
            if determinant < 0.999:
                continue
            name = "".join(
                f"{axis}{'+' if signs[index] > 0 else '-'}{('xyz')[perm[index]]}"
                for index, axis in enumerate("xyz")
            )
            hypotheses.setdefault(name, rotation)
    return hypotheses


def board_corners_world(geometry: BoardGeometry) -> list[np.ndarray]:
    """Return the four outer board corners in world coordinates."""

    origin_x, origin_y, origin_z = geometry.board_origin_world_xyz
    side = geometry.square_size_m * 8.0
    z = origin_z + geometry.board_height_z
    corners = [
        (origin_x, origin_y, z),
        (origin_x + side, origin_y, z),
        (origin_x + side, origin_y + side, z),
        (origin_x, origin_y + side, z),
    ]
    return [np.array([x, y, z, 1.0], dtype=np.float64) for x, y, z in corners]


def board_center_world(geometry: BoardGeometry) -> np.ndarray:
    """Return the board center point in world coordinates."""

    origin_x, origin_y, origin_z = geometry.board_origin_world_xyz
    side = geometry.square_size_m * 8.0
    return np.array(
        [origin_x + side / 2.0, origin_y + side / 2.0, origin_z + geometry.board_height_z],
        dtype=np.float64,
    )


def project_world_point(world_point_xyz: np.ndarray, t_world_camera: np.ndarray) -> tuple[float, float] | None:
    """Project one world point into image pixels using the fixed depth intrinsics."""

    camera_point = np.linalg.inv(t_world_camera) @ np.array(
        [world_point_xyz[0], world_point_xyz[1], world_point_xyz[2], 1.0],
        dtype=np.float64,
    )
    x_c, y_c, z_c = camera_point[:3]
    if z_c <= 1e-6:
        return None
    u = FX * (x_c / z_c) + CX
    v = FY * (y_c / z_c) + CY
    return (float(u), float(v))


def projected_polygon_area(points_uv: list[tuple[float, float]]) -> float:
    """Return polygon area in pixels squared using the shoelace formula."""

    if len(points_uv) < 3:
        return 0.0
    area = 0.0
    for index, (x0, y0) in enumerate(points_uv):
        x1, y1 = points_uv[(index + 1) % len(points_uv)]
        area += x0 * y1 - x1 * y0
    return abs(area) / 2.0


def optical_axis_intersection(
    t_world_camera: np.ndarray,
    plane_z: float,
) -> tuple[tuple[float, float, float] | None, float | None]:
    """Intersect the camera optical axis with the board plane z=plane_z in world."""

    camera_origin = t_world_camera[:3, 3]
    optical_axis_world = t_world_camera[:3, 2]
    if abs(optical_axis_world[2]) < 1e-6:
        return None, None
    scale = (plane_z - camera_origin[2]) / optical_axis_world[2]
    if scale <= 0.0:
        return None, None
    point = camera_origin + scale * optical_axis_world
    return (float(point[0]), float(point[1]), float(point[2])), float(scale)


class BridgeKinematicsHelper:
    """Combine bridge status, board geometry, and camera transforms in one helper."""

    def __init__(
        self,
        config_dir: str | Path | None = None,
        bridge_dir: str | Path | None = None,
    ) -> None:
        self.config_dir = Path(config_dir or Path(__file__).resolve().parents[1] / "config")
        self.geometry = BoardGeometry.from_yaml(self.config_dir / "board.yaml")
        self.bridge_files = self._resolve_bridge_files(bridge_dir)
        self.qarm_utils = QArmUtilities()
        self._base_camera_extrinsic = camera_extrinsic_from_urdf()
        self._tool_frame_corrections = tool_frame_correction_hypotheses()
        self._selected_extrinsic_name = "identity"
        self._camera_extrinsic = self._base_camera_extrinsic

    def _resolve_bridge_files(self, bridge_dir: str | Path | None) -> BridgeFiles:
        if bridge_dir is None:
            bridge_dir = Path(__file__).resolve().parents[2]
        resolved_dir = Path(bridge_dir).resolve()
        return BridgeFiles(
            bridge_dir=resolved_dir,
            status_json=resolved_dir / "status.json",
            target_pose_json=resolved_dir / "target_pose.json",
            camera_status_json=resolved_dir / "camera_status.json",
        )

    def load_json(self, path: Path) -> dict[str, Any]:
        """Load a bridge JSON file if present, else return an empty dict."""

        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    def load_status(self) -> dict[str, Any]:
        """Load bridge motion status."""

        return self.load_json(self.bridge_files.status_json)

    def load_target_pose(self) -> dict[str, Any]:
        """Load the current bridge target pose."""

        return self.load_json(self.bridge_files.target_pose_json)

    def load_camera_status(self) -> dict[str, Any]:
        """Load experimental camera stream status."""

        return self.load_json(self.bridge_files.camera_status_json)

    def bridge_snapshot(self) -> BridgeSnapshot:
        """Return the current bridge/camera summary in one object."""

        status = self.load_status()
        target = self.load_target_pose()
        camera = self.load_camera_status()

        color_shape = None
        depth_shape = None
        center_depth = None
        frames = camera.get("frames", {})
        if "color" in frames:
            shape = frames["color"].get("shape")
            if isinstance(shape, list) and len(shape) == 3:
                color_shape = tuple(int(v) for v in shape)
        if "depth" in frames:
            shape = frames["depth"].get("shape")
            if isinstance(shape, list) and len(shape) == 2:
                depth_shape = tuple(int(v) for v in shape)
            depth_value = frames["depth"].get("center_depth_m")
            if depth_value is not None:
                center_depth = float(depth_value)

        return BridgeSnapshot(
            bridge_state=status.get("state"),
            active_goal_id=status.get("active_goal_id"),
            active_goal_pose=self._pose_from_payload(status.get("active_goal_pose")),
            live_task_space_pose=self._pose_from_payload(status.get("live_task_space_pose")),
            target_goal_pose=self._pose_from_payload(target.get("goal_pose")),
            camera_center_depth_m=center_depth,
            camera_rgb_shape=color_shape,
            camera_depth_shape=depth_shape,
        )

    @property
    def selected_extrinsic_name(self) -> str:
        """Return the currently selected FK-to-URDF frame correction name."""

        return self._selected_extrinsic_name

    def refresh_camera_extrinsic(
        self,
        seed_xyz: tuple[float, float, float],
        wrist: float,
        center_depth_m: float | None = None,
    ) -> str:
        """Select the best constant FK-to-URDF frame correction for the current bridge pose."""

        best_name = self._selected_extrinsic_name
        best_score = None
        best_extrinsic = self._camera_extrinsic

        for name, correction in self._tool_frame_corrections.items():
            score = self._score_pose_with_extrinsic(
                xyz=seed_xyz,
                wrist=wrist,
                extrinsic_name=name,
                extrinsic=self._base_camera_extrinsic.copy(),
                tool_frame_correction=correction,
                center_depth_m=center_depth_m,
            )
            if score is None:
                continue
            if best_score is None or score.score > best_score.score:
                best_name = name
                best_score = score
                corrected = np.eye(4, dtype=np.float64)
                corrected[:3, :3] = correction
                best_extrinsic = corrected @ self._base_camera_extrinsic

        self._selected_extrinsic_name = best_name
        self._camera_extrinsic = best_extrinsic
        return best_name

    def score_pose(self, xyz: tuple[float, float, float], wrist: float) -> PoseScore | None:
        """Score one observer task-space pose using IK/FK and board projection geometry."""

        return self._score_pose_with_extrinsic(
            xyz=xyz,
            wrist=wrist,
            extrinsic_name=self._selected_extrinsic_name,
            extrinsic=self._camera_extrinsic,
            tool_frame_correction=None,
            center_depth_m=None,
        )

    def _score_pose_with_extrinsic(
        self,
        xyz: tuple[float, float, float],
        wrist: float,
        extrinsic_name: str,
        extrinsic: np.ndarray,
        tool_frame_correction: np.ndarray | None,
        center_depth_m: float | None,
    ) -> PoseScore | None:
        """Score one pose for a specific camera extrinsic hypothesis."""

        phi_prev = np.zeros(4, dtype=np.float64)
        _, phi_optimal = self.qarm_utils.inverse_kinematics(np.array(xyz, dtype=np.float64), wrist, phi_prev)
        if all(abs(value) < 1e-9 for value in phi_optimal):
            return None

        ee_position, ee_rotation = self.qarm_utils.forward_kinematics(np.array(phi_optimal, dtype=np.float64))
        if tool_frame_correction is not None:
            ee_rotation = ee_rotation @ tool_frame_correction
        t_world_ee = make_transform(
            ee_rotation,
            (float(ee_position[0]), float(ee_position[1]), float(ee_position[2])),
        )
        t_world_camera = t_world_ee @ extrinsic

        corners_world = board_corners_world(self.geometry)
        projected_corners: list[tuple[float, float]] = []
        visible_corner_count = 0
        for corner in corners_world:
            uv = project_world_point(corner[:3], t_world_camera)
            if uv is None:
                continue
            projected_corners.append(uv)
            if 0.0 <= uv[0] < WIDTH and 0.0 <= uv[1] < HEIGHT:
                visible_corner_count += 1

        if not projected_corners:
            return None

        board_center = board_center_world(self.geometry)
        center_uv = project_world_point(board_center, t_world_camera)
        center_error_px = None if center_uv is None else math.dist(center_uv, (CX, CY))
        center_inside = center_uv is not None and 0.0 <= center_uv[0] < WIDTH and 0.0 <= center_uv[1] < HEIGHT

        axis_intersection, axis_depth_m = optical_axis_intersection(t_world_camera, self.geometry.board_surface_world_z)
        axis_error_m = None
        if axis_intersection is not None:
            axis_error_m = math.dist(axis_intersection[:2], tuple(board_center[:2]))

        area = projected_polygon_area(projected_corners)
        score = 0.0
        score += visible_corner_count * 3000.0
        score += min(area, 120000.0)
        score += 15000.0 if center_inside else 0.0
        score -= 100000.0 if center_error_px is None else center_error_px * 40.0
        score -= 100000.0 if axis_error_m is None else axis_error_m * 25000.0
        if center_depth_m is not None:
            score -= 50000.0 if axis_depth_m is None else abs(axis_depth_m - center_depth_m) * 20000.0

        return PoseScore(
            xyz=xyz,
            wrist=wrist,
            extrinsic_name=extrinsic_name,
            projected_center_uv=center_uv,
            board_axis_intersection_world=axis_intersection,
            visible_corner_count=visible_corner_count,
            projected_area_px2=area,
            center_error_px=center_error_px,
            axis_error_m=axis_error_m,
            axis_depth_m=axis_depth_m,
            score=score,
            phi_optimal=tuple(float(v) for v in phi_optimal),
            camera_world_xyz=tuple(float(v) for v in t_world_camera[:3, 3]),
        )

    def score_current_live_pose(self) -> PoseScore | None:
        """Score the current live bridge pose if available."""

        snapshot = self.bridge_snapshot()
        pose = snapshot.live_task_space_pose or snapshot.target_goal_pose or snapshot.active_goal_pose
        if pose is None:
            return None
        return self.score_pose(xyz=pose[:3], wrist=pose[3])

    def resolve_seed_pose(self, seed_source: str = "bridge") -> tuple[tuple[float, float, float], float]:
        """Resolve the seed pose from the bridge snapshot or observer config."""

        if seed_source == "config":
            return self.load_active_observer_pose()

        snapshot = self.bridge_snapshot()
        bridge_pose: tuple[float, float, float, float] | None
        if seed_source == "live":
            bridge_pose = snapshot.live_task_space_pose
        elif seed_source == "target":
            bridge_pose = snapshot.target_goal_pose
        elif seed_source == "active":
            bridge_pose = snapshot.active_goal_pose
        else:
            bridge_pose = (
                snapshot.live_task_space_pose
                or snapshot.target_goal_pose
                or snapshot.active_goal_pose
            )

        if bridge_pose is None:
            return self.load_active_observer_pose()
        return bridge_pose[:3], bridge_pose[3]

    def generate_grid(
        self,
        seed_xyz: tuple[float, float, float],
        x_offsets: list[float],
        y_offsets: list[float],
        z_offsets: list[float],
    ) -> list[tuple[float, float, float]]:
        """Generate xyz candidates around a seed pose."""

        candidates: list[tuple[float, float, float]] = []
        for dx in x_offsets:
            for dy in y_offsets:
                for dz in z_offsets:
                    candidates.append(
                        (
                            round(seed_xyz[0] + dx, 3),
                            round(seed_xyz[1] + dy, 3),
                            round(seed_xyz[2] + dz, 3),
                        )
                    )
        return candidates

    def rank_grid_around_seed(
        self,
        seed_xyz: tuple[float, float, float],
        wrist: float,
        x_offsets: list[float],
        y_offsets: list[float],
        z_offsets: list[float],
    ) -> list[PoseScore]:
        """Score a grid around one seed observer pose."""

        scored: list[PoseScore] = []
        for xyz in self.generate_grid(seed_xyz, x_offsets=x_offsets, y_offsets=y_offsets, z_offsets=z_offsets):
            result = self.score_pose(xyz=xyz, wrist=wrist)
            if result is not None:
                scored.append(result)
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored

    def load_active_observer_pose(self) -> tuple[tuple[float, float, float], float]:
        """Load the active observer pose from observer_pose.yaml."""

        payload = yaml.safe_load((self.config_dir / "observer_pose.yaml").read_text(encoding="utf-8"))
        xyz = tuple(float(v) for v in payload["observer_world_xyz"])
        wrist = float(payload["observer_rpy"][2])
        return xyz, wrist

    def _pose_from_payload(self, payload: Any) -> tuple[float, float, float, float] | None:
        if not isinstance(payload, list) or len(payload) != 4:
            return None
        return tuple(float(v) for v in payload)


def main() -> None:
    parser = argparse.ArgumentParser(description="Bridge-aware observer pose kinematics helper.")
    parser.add_argument("--top", type=int, default=10, help="Number of top-scoring poses to print.")
    parser.add_argument(
        "--bridge-dir",
        type=str,
        default=None,
        help="Override the codex-testing bridge directory containing status.json/target_pose.json/camera_status.json.",
    )
    parser.add_argument(
        "--config-dir",
        type=str,
        default=None,
        help="Override the chess-logic config directory.",
    )
    parser.add_argument(
        "--seed-source",
        choices=["bridge", "config", "live", "target", "active"],
        default="bridge",
        help="Choose whether to seed the search from the bridge pose or the observer config.",
    )
    args = parser.parse_args()

    helper = BridgeKinematicsHelper(config_dir=args.config_dir, bridge_dir=args.bridge_dir)
    snapshot = helper.bridge_snapshot()
    seed_xyz, wrist = helper.resolve_seed_pose(args.seed_source)
    selected_extrinsic = helper.refresh_camera_extrinsic(
        seed_xyz=seed_xyz,
        wrist=wrist,
        center_depth_m=snapshot.camera_center_depth_m,
    )
    ranked = helper.rank_grid_around_seed(
        seed_xyz=seed_xyz,
        wrist=wrist,
        x_offsets=[-0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03],
        y_offsets=[-0.02, -0.01, 0.0, 0.01, 0.02],
        z_offsets=[-0.03, -0.02, -0.01, 0.0, 0.01],
    )

    print("Bridge Snapshot")
    print(f"  state={snapshot.bridge_state} active_goal_id={snapshot.active_goal_id}")
    print(f"  live_task_space_pose={snapshot.live_task_space_pose}")
    print(f"  target_goal_pose={snapshot.target_goal_pose}")
    print(f"  camera_center_depth_m={snapshot.camera_center_depth_m}")
    print(f"  camera_rgb_shape={snapshot.camera_rgb_shape} camera_depth_shape={snapshot.camera_depth_shape}")
    print(f"  selected_extrinsic_name={selected_extrinsic}")
    print("")
    print(f"Observer seed source={args.seed_source} xyz={seed_xyz} wrist={wrist:.3f}")
    print("")
    for result in ranked[: args.top]:
        center_uv = None if result.projected_center_uv is None else tuple(round(v, 1) for v in result.projected_center_uv)
        axis_world = None if result.board_axis_intersection_world is None else tuple(round(v, 4) for v in result.board_axis_intersection_world)
        print(
            f"score={result.score:.1f} xyz={result.xyz} wrist={result.wrist:.3f} extrinsic={result.extrinsic_name} "
            f"visible_corners={result.visible_corner_count} area_px2={result.projected_area_px2:.0f} "
            f"center_uv={center_uv} center_error_px={None if result.center_error_px is None else round(result.center_error_px, 1)} "
            f"axis_hit={axis_world} axis_error_m={None if result.axis_error_m is None else round(result.axis_error_m, 4)} "
            f"axis_depth_m={None if result.axis_depth_m is None else round(result.axis_depth_m, 4)} "
            f"camera_world_xyz={tuple(round(v, 4) for v in result.camera_world_xyz)}"
        )


if __name__ == "__main__":
    main()

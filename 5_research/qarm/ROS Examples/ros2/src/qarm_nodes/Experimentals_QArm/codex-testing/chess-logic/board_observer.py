"""Board observation pipeline with mock and camera-backed modes.

This module remains a pure-Python integration layer. Perception is trusted only
in `CHESS_OBSERVER` and intentionally frozen while the arm is moving.
"""

from __future__ import annotations

import math
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from board_geometry import (
    BoardCalibration,
    BoardGeometry,
    canonicalize_image_corners,
    remap_world_corners_by_image_permutation,
)
from models import ObservedBoard, PieceObservation, XYZ

PixelUV = tuple[float, float]


@dataclass(frozen=True)
class CameraIntrinsics:
    """Pinhole camera intrinsics for depth-to-3D projection."""

    fx: float
    fy: float
    cx: float
    cy: float
    frame_name: str | None = None
    width: int | None = None
    height: int | None = None


@dataclass
class CameraFrameBundle:
    """Single observer-pose RGB/depth capture with optional metadata."""

    rgb_image: Any
    depth_image: Any
    intrinsics: CameraIntrinsics | None
    color_frame_name: str | None
    depth_frame_name: str | None
    timestamp: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DetectedPieceCandidate:
    """Piece candidate produced by a detector before square assignment."""

    piece_name: str
    confidence: float
    pixel_uv: PixelUV | None = None
    world_xyz: XYZ | None = None
    yaw_rad: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SquareRegion:
    """Square center and corners in world/image domains."""

    square: str
    center_world_xyz: XYZ
    corners_world_xyz: tuple[XYZ, XYZ, XYZ, XYZ]
    center_image_uv: PixelUV | None = None
    corners_image_uv: tuple[PixelUV, PixelUV, PixelUV, PixelUV] | None = None


@dataclass(frozen=True)
class BoardFrameEstimate:
    """Board frame estimate used for square generation and assignment."""

    frame_name: str
    origin_world_xyz: XYZ
    x_axis_world: XYZ
    y_axis_world: XYZ
    z_axis_world: XYZ
    square_centers_world: dict[str, XYZ]
    square_regions: dict[str, SquareRegion]
    source: str
    board_detection_mode: str = "manual"
    board_outer_corners_image: dict[str, PixelUV] = field(default_factory=dict)
    board_outer_corners_world: dict[str, XYZ] = field(default_factory=dict)
    square_centers_image: dict[str, PixelUV] = field(default_factory=dict)
    square_polygons_image: dict[str, tuple[PixelUV, PixelUV, PixelUV, PixelUV]] = field(
        default_factory=dict
    )
    square_spacing_validation: dict[str, float | bool] = field(default_factory=dict)
    assignment_margin_m: float | None = None
    corner_confidence: float | None = None
    visible_board_fraction: float | None = None
    live_fit_confidence: float | None = None
    used_live_fit: bool = False
    used_manual_fallback: bool = False
    fit_state: str = "manual"
    live_fit_debug: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LiveCornerFitResult:
    """Result of one live board-corner fitting attempt."""

    corners_image: dict[str, PixelUV] | None
    corners_world: dict[str, XYZ] | None
    corner_confidence: float
    visible_board_fraction: float
    live_fit_confidence: float
    accepted: bool
    source: str
    reason: str
    fit_state: str = "manual"
    used_last_good: bool = False
    fit_coordinate_mode: str = "unknown"
    alignment_active: bool = False
    color_image_size: tuple[int, int] | None = None
    depth_image_size: tuple[int, int] | None = None
    fitted_corner_pixels: dict[str, PixelUV] | None = None
    projected_corner_depth_pixels: dict[str, PixelUV] | None = None
    projected_corner_world: dict[str, XYZ] | None = None


@runtime_checkable
class FrameSource(Protocol):
    """Supplies observer-pose RGB/depth frames for perception."""

    def get_observer_frame(self) -> CameraFrameBundle:
        """Capture or return the latest observer-pose frame bundle."""


@runtime_checkable
class TransformProvider(Protocol):
    """Converts camera pixels and depth into world coordinates."""

    def pixel_to_world(
        self,
        pixel_uv: PixelUV,
        depth_m: float,
        intrinsics: CameraIntrinsics | None,
        depth_frame_name: str | None,
    ) -> XYZ | None:
        """Return the world xyz for one pixel/depth sample."""


@runtime_checkable
class BoardCornerDetector(Protocol):
    """Optional Stage-B automatic board corner detector.

    TODO: replace this protocol implementation with robust edge/border based
    board detection that remains stable while pieces are on the board.
    """

    def detect_outer_corners(
        self,
        frame_bundle: CameraFrameBundle,
    ) -> dict[str, PixelUV] | None:
        """Return outer corners keyed by `a1,h1,h8,a8` if available."""


@runtime_checkable
class LiveCornerFitter(Protocol):
    """Fits live board corners from current observer frame data."""

    def fit_live_corners(
        self,
        frame_bundle: CameraFrameBundle,
        *,
        calibration: BoardCalibration,
        geometry: BoardGeometry,
        transform_provider: TransformProvider | None,
        corner_detector: BoardCornerDetector | None,
        manual_corners_image: dict[str, PixelUV] | None,
    ) -> LiveCornerFitResult:
        """Return a confidence-scored live corner fit."""


@runtime_checkable
class BoardFrameEstimator(Protocol):
    """Optional board-frame estimator for observer-pose perception."""

    def estimate_board_frame(
        self,
        frame_bundle: CameraFrameBundle,
        geometry: BoardGeometry,
        transform_provider: TransformProvider | None,
    ) -> BoardFrameEstimate:
        """Estimate the board frame from RGB/depth and available transforms."""


@runtime_checkable
class PieceDetector(Protocol):
    """Optional piece detector hook for camera-backed observation."""

    def detect_pieces(
        self,
        frame_bundle: CameraFrameBundle,
        board_frame: BoardFrameEstimate,
    ) -> list[DetectedPieceCandidate]:
        """Return piece candidates from the current observer frame."""


class ImageSpaceBoardCornerFitter:
    """Primary live board fitter in image space with hysteresis and hold logic."""

    def __init__(self) -> None:
        self._last_good_corners: dict[str, PixelUV] | None = None
        self._last_good_confidence: float = 0.0
        self._last_good_timestamp: float | None = None
        self._last_frame_timestamp: float | None = None
        self._frames_since_reset: int = 0

    def fit_live_corners(
        self,
        frame_bundle: CameraFrameBundle,
        *,
        calibration: BoardCalibration,
        geometry: BoardGeometry,
        transform_provider: TransformProvider | None,
        corner_detector: BoardCornerDetector | None,
        manual_corners_image: dict[str, PixelUV] | None,
    ) -> LiveCornerFitResult:
        self._update_observer_settle_state(frame_bundle, calibration)
        tracking_image, tracking_mode, alignment_active, color_size, depth_size = (
            _select_tracking_image(frame_bundle)
        )
        metadata_corners = _extract_corner_map_from_metadata(frame_bundle.metadata)
        if metadata_corners is not None:
            oriented, _ = canonicalize_image_corners(metadata_corners)
            return self._evaluate_live_candidate(
                frame_bundle=frame_bundle,
                calibration=calibration,
                geometry=geometry,
                transform_provider=transform_provider,
                candidate_corners=oriented,
                source="image_metadata",
                quality_hint=0.95,
                tracking_mode=tracking_mode,
                alignment_active=alignment_active,
                color_size=color_size,
                depth_size=depth_size,
            )

        detector_corners = (
            corner_detector.detect_outer_corners(frame_bundle) if corner_detector is not None else None
        )
        if detector_corners is not None:
            oriented, _ = canonicalize_image_corners(detector_corners)
            return self._evaluate_live_candidate(
                frame_bundle=frame_bundle,
                calibration=calibration,
                geometry=geometry,
                transform_provider=transform_provider,
                candidate_corners=oriented,
                source="image_detector",
                quality_hint=0.90,
                tracking_mode=tracking_mode,
                alignment_active=alignment_active,
                color_size=color_size,
                depth_size=depth_size,
            )

        if manual_corners_image is None and self._last_good_corners is None:
            return LiveCornerFitResult(
                corners_image=None,
                corners_world=None,
                corner_confidence=0.0,
                visible_board_fraction=0.0,
                live_fit_confidence=0.0,
                accepted=False,
                source="image_seed_missing",
                reason="manual_seed_unavailable",
                fit_state="stale_manual",
                used_last_good=False,
                fit_coordinate_mode=tracking_mode,
                alignment_active=alignment_active,
                color_image_size=color_size,
                depth_image_size=depth_size,
            )

        seed_corners = self._last_good_corners or manual_corners_image
        if seed_corners is None:
            return LiveCornerFitResult(
                corners_image=None,
                corners_world=None,
                corner_confidence=0.0,
                visible_board_fraction=0.0,
                live_fit_confidence=0.0,
                accepted=False,
                source="image_seed_missing",
                reason="seed_unavailable",
                fit_state="stale_manual",
                used_last_good=False,
                fit_coordinate_mode=tracking_mode,
                alignment_active=alignment_active,
                color_image_size=color_size,
                depth_image_size=depth_size,
            )

        if tracking_image is None:
            return LiveCornerFitResult(
                corners_image=dict(seed_corners),
                corners_world=None,
                corner_confidence=0.0,
                visible_board_fraction=0.0,
                live_fit_confidence=0.05,
                accepted=False,
                source="image_unavailable",
                reason="tracking_image_unavailable",
                fit_state="stale_manual",
                used_last_good=self._last_good_corners is not None,
                fit_coordinate_mode=tracking_mode,
                alignment_active=alignment_active,
                color_image_size=color_size,
                depth_image_size=depth_size,
                fitted_corner_pixels=dict(seed_corners),
                projected_corner_world=None,
            )

        tracked_corners, tracking_quality = _track_corners_from_image(
            tracking_image=tracking_image,
            seed_corners=seed_corners,
            search_radius_px=calibration.live_corner_search_radius_px,
        )
        if tracked_corners is None:
            tracked_corners = dict(seed_corners)
            tracking_quality = 0.10

        return self._evaluate_live_candidate(
            frame_bundle=frame_bundle,
            calibration=calibration,
            geometry=geometry,
            transform_provider=transform_provider,
            candidate_corners=tracked_corners,
            source="image_track",
            quality_hint=tracking_quality,
            tracking_mode=tracking_mode,
            alignment_active=alignment_active,
            color_size=color_size,
            depth_size=depth_size,
        )

    def _evaluate_live_candidate(
        self,
        *,
        frame_bundle: CameraFrameBundle,
        calibration: BoardCalibration,
        geometry: BoardGeometry,
        transform_provider: TransformProvider | None,
        candidate_corners: dict[str, PixelUV],
        source: str,
        quality_hint: float,
        tracking_mode: str,
        alignment_active: bool,
        color_size: tuple[int, int] | None,
        depth_size: tuple[int, int] | None,
    ) -> LiveCornerFitResult:
        oriented, _ = canonicalize_image_corners(candidate_corners)
        visibility = _image_corner_visibility_fraction(
            oriented,
            frame_bundle.depth_image if tracking_mode.startswith("depth") else frame_bundle.rgb_image,
        )
        geometric_confidence = _corner_geometry_confidence(oriented)
        motion_confidence = _motion_consistency_confidence(self._last_good_corners, oriented)
        corner_confidence = _clamp01(
            0.45 * geometric_confidence + 0.35 * quality_hint + 0.20 * motion_confidence
        )
        live_fit_confidence = _clamp01(0.60 * corner_confidence + 0.40 * visibility)
        warmed_up = self._frames_since_reset >= calibration.observer_settle_frames

        # Hysteresis: accept > keep-last-good > stale/manual.
        if (
            warmed_up
            and corner_confidence >= calibration.min_corner_confidence
            and visibility >= calibration.min_visible_board_fraction
            and live_fit_confidence >= calibration.min_live_fit_confidence
        ):
            smoothed = _smooth_corners(
                self._last_good_corners,
                oriented,
                alpha=calibration.live_corner_smoothing_alpha,
            )
            self._update_last_good(smoothed, live_fit_confidence, frame_bundle.timestamp)
            return self._build_result(
                frame_bundle=frame_bundle,
                calibration=calibration,
                geometry=geometry,
                transform_provider=transform_provider,
                corners_image=smoothed,
                corner_confidence=corner_confidence,
                visibility=visibility,
                live_fit_confidence=live_fit_confidence,
                accepted=True,
                source=f"{source}_accepted",
                reason="ok",
                fit_state="live",
                used_last_good=False,
                tracking_mode=tracking_mode,
                alignment_active=alignment_active,
                color_size=color_size,
                depth_size=depth_size,
            )

        if (
            self._last_good_corners is not None
            and live_fit_confidence >= calibration.live_keep_last_good_confidence
        ):
            held = _smooth_corners(
                self._last_good_corners,
                oriented,
                alpha=max(0.1, calibration.live_corner_smoothing_alpha * 0.4),
            )
            self._update_last_good(
                held,
                max(self._last_good_confidence * 0.85, live_fit_confidence),
                frame_bundle.timestamp,
            )
            return self._build_result(
                frame_bundle=frame_bundle,
                calibration=calibration,
                geometry=geometry,
                transform_provider=transform_provider,
                corners_image=held,
                corner_confidence=corner_confidence,
                visibility=visibility,
                live_fit_confidence=live_fit_confidence,
                accepted=True,
                source=f"{source}_weak_hold",
                reason="weak_keep_last_good",
                fit_state="weak_held",
                used_last_good=True,
                tracking_mode=tracking_mode,
                alignment_active=alignment_active,
                color_size=color_size,
                depth_size=depth_size,
            )

        if (
            self._last_good_corners is not None
            and self._last_good_timestamp is not None
            and (frame_bundle.timestamp - self._last_good_timestamp) <= calibration.live_stale_timeout_sec
        ):
            stale_fit = max(self._last_good_confidence * 0.7, 0.05)
            return self._build_result(
                frame_bundle=frame_bundle,
                calibration=calibration,
                geometry=geometry,
                transform_provider=transform_provider,
                corners_image=self._last_good_corners,
                corner_confidence=max(corner_confidence * 0.6, 0.05),
                visibility=visibility,
                live_fit_confidence=stale_fit,
                accepted=True,
                source=f"{source}_stale_hold",
                reason="stale_hold_last_good",
                fit_state="stale_manual",
                used_last_good=True,
                tracking_mode=tracking_mode,
                alignment_active=alignment_active,
                color_size=color_size,
                depth_size=depth_size,
            )

        fallback_corners = self._last_good_corners or oriented
        return self._build_result(
            frame_bundle=frame_bundle,
            calibration=calibration,
            geometry=geometry,
            transform_provider=transform_provider,
            corners_image=fallback_corners,
            corner_confidence=corner_confidence,
            visibility=visibility,
            live_fit_confidence=live_fit_confidence,
            accepted=False,
            source=f"{source}_manual_fallback",
            reason="below_threshold",
            fit_state="stale_manual",
            used_last_good=self._last_good_corners is not None,
            tracking_mode=tracking_mode,
            alignment_active=alignment_active,
            color_size=color_size,
            depth_size=depth_size,
        )

    def _build_result(
        self,
        *,
        frame_bundle: CameraFrameBundle,
        calibration: BoardCalibration,
        geometry: BoardGeometry,
        transform_provider: TransformProvider | None,
        corners_image: dict[str, PixelUV],
        corner_confidence: float,
        visibility: float,
        live_fit_confidence: float,
        accepted: bool,
        source: str,
        reason: str,
        fit_state: str,
        used_last_good: bool,
        tracking_mode: str,
        alignment_active: bool,
        color_size: tuple[int, int] | None,
        depth_size: tuple[int, int] | None,
    ) -> LiveCornerFitResult:
        corners_world, projected_depth_pixels = _project_corner_map_to_world(
            corners_image=corners_image,
            frame_bundle=frame_bundle,
            transform_provider=transform_provider,
            fit_coordinate_mode=tracking_mode,
            alignment_active=alignment_active,
        )
        world_spacing_ok: bool | None = None
        if corners_world is not None:
            spacing = geometry.validate_square_spacing_world(
                square_centers_world=geometry.square_centers_from_outer_corners_world(corners_world),
                min_square_size_m=calibration.min_square_size_m,
                max_square_size_m=calibration.max_square_size_m,
            )
            world_spacing_ok = bool(spacing.get("within_tolerance", False))
            if not world_spacing_ok:
                corners_world = None

        if world_spacing_ok is False:
            reason = f"{reason}_world_fallback"

        return LiveCornerFitResult(
            corners_image=corners_image,
            corners_world=corners_world,
            corner_confidence=corner_confidence,
            visible_board_fraction=visibility,
            live_fit_confidence=live_fit_confidence,
            accepted=accepted,
            source=source,
            reason=reason,
            fit_state=fit_state,
            used_last_good=used_last_good,
            fit_coordinate_mode=tracking_mode,
            alignment_active=alignment_active,
            color_image_size=color_size,
            depth_image_size=depth_size,
            fitted_corner_pixels=dict(corners_image),
            projected_corner_depth_pixels=projected_depth_pixels,
            projected_corner_world=None if corners_world is None else dict(corners_world),
        )

    def _update_last_good(
        self,
        corners_image: dict[str, PixelUV],
        confidence: float,
        timestamp: float,
    ) -> None:
        self._last_good_corners = dict(corners_image)
        self._last_good_confidence = float(confidence)
        self._last_good_timestamp = float(timestamp)

    def _update_observer_settle_state(
        self,
        frame_bundle: CameraFrameBundle,
        calibration: BoardCalibration,
    ) -> None:
        current_ts = float(frame_bundle.timestamp)
        if self._last_frame_timestamp is None:
            self._frames_since_reset = 0
        else:
            gap_sec = current_ts - self._last_frame_timestamp
            if gap_sec >= calibration.observer_settle_reset_gap_sec:
                self._frames_since_reset = 0
        self._last_frame_timestamp = current_ts
        self._frames_since_reset += 1


class ConfiguredBoardFrameEstimator:
    """Stage-A/Stage-B board frame estimator with manual/automatic/hybrid modes.

    - Stage A: `board_calibration.yaml` corners (manual)
    - Stage B: optional automatic corner detector (automatic/hybrid)
    """

    def __init__(
        self,
        calibration: BoardCalibration | None = None,
        corner_detector: BoardCornerDetector | None = None,
        live_corner_fitter: LiveCornerFitter | None = None,
    ) -> None:
        self.calibration = calibration
        self.corner_detector = corner_detector
        self.live_corner_fitter = live_corner_fitter or ImageSpaceBoardCornerFitter()

    def estimate_board_frame(
        self,
        frame_bundle: CameraFrameBundle,
        geometry: BoardGeometry,
        transform_provider: TransformProvider | None,
    ) -> BoardFrameEstimate:
        calibration = self.calibration or _default_calibration(geometry)
        manual_image, manual_permutation = _manual_image_corners(calibration)
        manual_world = _manual_world_corners(
            calibration=calibration,
            geometry=geometry,
            image_permutation=manual_permutation,
        )
        if calibration.board_detection_mode == "manual":
            if manual_image is None:
                raise RuntimeError(
                    "Manual board detection requires board_outer_corners_image calibration."
                )
            live_fit = _manual_mode_live_fit_result(manual_image=manual_image)
        else:
            live_fit = self.live_corner_fitter.fit_live_corners(
                frame_bundle=frame_bundle,
                calibration=calibration,
                geometry=geometry,
                transform_provider=transform_provider,
                corner_detector=self.corner_detector,
                manual_corners_image=manual_image,
            )
        corners_image, corners_world, source_suffix, used_live_fit, used_manual_fallback = (
            self._select_corner_source(
                calibration=calibration,
                live_fit=live_fit,
                manual_image=manual_image,
                manual_world=manual_world,
            )
        )
        if (
            calibration.board_detection_mode == "automatic"
            and not calibration.fallback_to_manual_if_live_fit_fails
            and corners_image is None
        ):
            raise RuntimeError("Automatic board fitting failed and manual fallback is disabled.")
        if corners_world is None:
            corners_world = manual_world
        if corners_image is None:
            corners_image = manual_image

        square_centers_world = geometry.square_centers_from_outer_corners_world(corners_world)
        square_polygons_world = geometry.square_polygons_from_outer_corners_world(corners_world)
        square_spacing_validation = geometry.validate_square_spacing_world(
            square_centers_world=square_centers_world,
            min_square_size_m=calibration.min_square_size_m,
            max_square_size_m=calibration.max_square_size_m,
        )
        if corners_image:
            square_centers_image = geometry.square_centers_from_outer_corners_image(corners_image)
            square_polygons_image = geometry.square_polygons_from_outer_corners_image(corners_image)
        else:
            square_centers_image = {}
            square_polygons_image = {}
        square_regions: dict[str, SquareRegion] = {}
        for square in geometry.all_squares():
            square_regions[square] = SquareRegion(
                square=square,
                center_world_xyz=square_centers_world[square],
                corners_world_xyz=square_polygons_world[square],
                center_image_uv=square_centers_image.get(square),
                corners_image_uv=square_polygons_image.get(square),
            )
        return BoardFrameEstimate(
            frame_name=geometry.board_frame_name,
            origin_world_xyz=corners_world["a1"],
            x_axis_world=_norm_axis(corners_world["a1"], corners_world["h1"]),
            y_axis_world=_norm_axis(corners_world["a1"], corners_world["a8"]),
            z_axis_world=(0.0, 0.0, 1.0),
            square_centers_world=square_centers_world,
            square_regions=square_regions,
            source=f"board_calibration_{calibration.board_detection_mode}{source_suffix}",
            board_detection_mode=calibration.board_detection_mode,
            board_outer_corners_image=corners_image or {},
            board_outer_corners_world=corners_world,
            square_centers_image=square_centers_image,
            square_polygons_image=square_polygons_image,
            square_spacing_validation=square_spacing_validation,
            assignment_margin_m=calibration.max_square_size_m,
            corner_confidence=live_fit.corner_confidence,
            visible_board_fraction=live_fit.visible_board_fraction,
            live_fit_confidence=live_fit.live_fit_confidence,
            used_live_fit=used_live_fit,
            used_manual_fallback=used_manual_fallback,
            fit_state=live_fit.fit_state,
            live_fit_debug={
                "source": live_fit.source,
                "reason": live_fit.reason,
                "accepted": live_fit.accepted,
                "fit_state": live_fit.fit_state,
                "fit_coordinate_mode": live_fit.fit_coordinate_mode,
                "alignment_active": live_fit.alignment_active,
                "color_image_size": live_fit.color_image_size,
                "depth_image_size": live_fit.depth_image_size,
                "fitted_corner_pixels": live_fit.fitted_corner_pixels,
                "projected_corner_depth_pixels": live_fit.projected_corner_depth_pixels,
                "projected_corner_world": live_fit.projected_corner_world,
                "intrinsics": _intrinsics_debug_dict(frame_bundle.intrinsics),
            },
        )

    def _select_corner_source(
        self,
        *,
        calibration: BoardCalibration,
        live_fit: LiveCornerFitResult,
        manual_image: dict[str, PixelUV] | None,
        manual_world: dict[str, XYZ],
    ) -> tuple[
        dict[str, PixelUV] | None,
        dict[str, XYZ] | None,
        str,
        bool,
        bool,
    ]:
        mode = calibration.board_detection_mode
        manual_fallback_allowed = calibration.fallback_to_manual_if_live_fit_fails

        if mode == "manual":
            return manual_image, manual_world, "_manual", False, False

        if mode == "automatic":
            if live_fit.corners_image is not None and (
                live_fit.accepted or live_fit.fit_state in {"weak_held", "stale_manual"}
            ):
                return (
                    live_fit.corners_image,
                    live_fit.corners_world,
                    f"_automatic_{live_fit.fit_state}",
                    True,
                    live_fit.fit_state == "stale_manual",
                )
            if manual_fallback_allowed and manual_image is not None:
                return manual_image, manual_world, "_automatic_fallback_manual", False, True
            return None, live_fit.corners_world, "_automatic_live_unavailable", True, False

        if mode == "hybrid":
            if live_fit.corners_image is not None and (
                live_fit.accepted or live_fit.fit_state in {"weak_held", "stale_manual"}
            ):
                return (
                    live_fit.corners_image,
                    live_fit.corners_world,
                    f"_hybrid_{live_fit.fit_state}",
                    True,
                    live_fit.fit_state == "stale_manual",
                )
            if manual_image is not None:
                return manual_image, manual_world, "_hybrid_manual_fallback", False, True
            return None, live_fit.corners_world, "_hybrid_live_only", True, False

        if manual_image is not None:
            return manual_image, manual_world, "_unknown_mode_manual_fallback", False, True
        if live_fit.corners_image is not None:
            return live_fit.corners_image, live_fit.corners_world, "_unknown_mode_live_fallback", True, False
        return None, manual_world, "_unknown_mode_unavailable", False, False


class MetadataPieceDetector:
    """Detector hook that consumes precomputed piece candidates from metadata.

    Expected metadata format:
    `frame_bundle.metadata["piece_candidates"] = [ ... ]`

    TODO: Replace or augment this with a real RGB/depth detector model.
    """

    def detect_pieces(
        self,
        frame_bundle: CameraFrameBundle,
        board_frame: BoardFrameEstimate,
    ) -> list[DetectedPieceCandidate]:
        del board_frame
        raw_candidates = frame_bundle.metadata.get("piece_candidates", [])
        normalized: list[DetectedPieceCandidate] = []
        for item in raw_candidates:
            if isinstance(item, DetectedPieceCandidate):
                normalized.append(item)
                continue
            if not isinstance(item, Mapping):
                continue
            normalized.append(
                DetectedPieceCandidate(
                    piece_name=str(item["piece_name"]),
                    confidence=float(item.get("confidence", 0.0)),
                    pixel_uv=_normalize_pixel(item.get("pixel_uv")),
                    world_xyz=_normalize_xyz(item.get("world_xyz")),
                    yaw_rad=_optional_float(item.get("yaw_rad")),
                    metadata=dict(item.get("metadata", {})),
                )
            )
        return normalized


class BoardObserver:
    """Observer interface with mock and camera-backed modes.

    Perception is frozen while the arm is moving because the camera pose is not
    stable then. Observation is valid only in `CHESS_OBSERVER`.
    """

    def __init__(
        self,
        geometry: BoardGeometry,
        mock_observations: Mapping[str, str | None] | None = None,
        *,
        mode: str = "mock",
        frame_source: FrameSource | None = None,
        transform_provider: TransformProvider | None = None,
        board_frame_estimator: BoardFrameEstimator | None = None,
        piece_detector: PieceDetector | None = None,
        allow_mock_fallback: bool = True,
        calibration: BoardCalibration | None = None,
    ) -> None:
        self.geometry = geometry
        self.calibration = calibration or _default_calibration(geometry)
        self.mode = mode
        self.frame_source = frame_source
        self.transform_provider = transform_provider
        self.board_frame_estimator = board_frame_estimator or ConfiguredBoardFrameEstimator(
            calibration=self.calibration
        )
        self.piece_detector = piece_detector or MetadataPieceDetector()
        self.allow_mock_fallback = allow_mock_fallback
        self._mock_observations = self._normalize_square_map(mock_observations or {})
        self._frozen = False
        self._validate_mode()

    def set_mode(self, mode: str) -> None:
        """Switch between `mock` and `camera` observation modes."""

        self.mode = mode
        self._validate_mode()

    def configure_camera_mode(
        self,
        *,
        frame_source: FrameSource | None = None,
        transform_provider: TransformProvider | None = None,
        board_frame_estimator: BoardFrameEstimator | None = None,
        piece_detector: PieceDetector | None = None,
        allow_mock_fallback: bool | None = None,
        calibration: BoardCalibration | None = None,
    ) -> None:
        """Update the pure-Python camera observer interfaces."""

        if frame_source is not None:
            self.frame_source = frame_source
        if transform_provider is not None:
            self.transform_provider = transform_provider
        if calibration is not None:
            self.calibration = calibration
            if board_frame_estimator is None:
                board_frame_estimator = ConfiguredBoardFrameEstimator(calibration=calibration)
        if board_frame_estimator is not None:
            self.board_frame_estimator = board_frame_estimator
        if piece_detector is not None:
            self.piece_detector = piece_detector
        if allow_mock_fallback is not None:
            self.allow_mock_fallback = allow_mock_fallback

    def set_mock_observations(self, mock_observations: Mapping[str, str | None]) -> None:
        """Replace the current mock observed board."""

        self._mock_observations = self._normalize_square_map(mock_observations)

    def freeze(self) -> None:
        """Disallow observation while the arm is moving."""

        self._frozen = True

    def allow_observation(self) -> None:
        """Allow observation again once the arm returns to observer pose."""

        self._frozen = False

    def observe_board(
        self,
        stubbed_board: Mapping[str, str | None] | None = None,
    ) -> ObservedBoard:
        """Return an observed board from camera or mock input.

        Camera mode pipeline:
        RGB/depth -> board ID -> square layout -> piece candidates ->
        world/pixel square assignment -> ObservedBoard
        """

        if self._frozen:
            raise RuntimeError("Board observation is frozen while robot motion is in progress.")

        if stubbed_board is not None:
            return self._observe_mock_board(stubbed_board)

        if self.mode == "camera":
            try:
                return self._observe_camera_board()
            except RuntimeError:
                if not self.allow_mock_fallback:
                    raise
                return self._observe_mock_board()

        return self._observe_mock_board()

    def estimate_board_frame(self, frame_bundle: CameraFrameBundle) -> BoardFrameEstimate:
        """Estimate board geometry from the current observer frame."""

        return self.board_frame_estimator.estimate_board_frame(
            frame_bundle=frame_bundle,
            geometry=self.geometry,
            transform_provider=self.transform_provider,
        )

    def square_centers(self, board_frame: BoardFrameEstimate) -> dict[str, XYZ]:
        """Return all world square centers for the current frame."""

        return dict(board_frame.square_centers_world)

    def square_regions(self, board_frame: BoardFrameEstimate) -> dict[str, SquareRegion]:
        """Return all square regions for the current frame."""

        return dict(board_frame.square_regions)

    def detect_piece_candidates(
        self,
        frame_bundle: CameraFrameBundle,
        board_frame: BoardFrameEstimate,
    ) -> list[DetectedPieceCandidate]:
        """Run the injected detector hook on RGB/depth observer data."""

        return self.piece_detector.detect_pieces(frame_bundle, board_frame)

    def assign_piece_to_square(
        self,
        world_xyz: XYZ,
        square_centers_world: Mapping[str, XYZ],
        max_distance_m: float | None = None,
    ) -> str | None:
        """Assign a world position to the nearest board square."""

        return self.geometry.point_to_square_world(
            world_xyz=world_xyz,
            square_centers_world=dict(square_centers_world),
            max_distance_m=max_distance_m,
        )

    def assign_pixel_to_square(
        self,
        pixel_uv: PixelUV,
        board_frame: BoardFrameEstimate,
    ) -> str | None:
        """Assign a pixel location into one board square."""

        if not board_frame.square_polygons_image:
            return None
        average_square_px = _average_square_pixel_size(board_frame.square_centers_image)
        max_distance_px = average_square_px * 0.80 if average_square_px is not None else None
        return self.geometry.point_to_square_image(
            pixel_uv=pixel_uv,
            square_polygons_image=board_frame.square_polygons_image,
            square_centers_image=board_frame.square_centers_image,
            max_distance_px=max_distance_px,
        )

    def locate_piece_center_world(
        self,
        candidate: DetectedPieceCandidate,
        frame_bundle: CameraFrameBundle,
    ) -> XYZ | None:
        """Resolve a candidate to world coordinates using depth and transforms."""

        if candidate.world_xyz is not None:
            return candidate.world_xyz
        if candidate.pixel_uv is None or self.transform_provider is None:
            return None
        depth_m = self._depth_at_pixel(frame_bundle.depth_image, candidate.pixel_uv)
        if depth_m is None:
            return None
        return self.transform_provider.pixel_to_world(
            pixel_uv=candidate.pixel_uv,
            depth_m=depth_m,
            intrinsics=frame_bundle.intrinsics,
            depth_frame_name=frame_bundle.depth_frame_name,
        )

    def build_observed_board_from_candidates(
        self,
        candidates: list[DetectedPieceCandidate],
        board_frame: BoardFrameEstimate,
        frame_bundle: CameraFrameBundle,
    ) -> ObservedBoard:
        """Assign detected pieces to squares and build `ObservedBoard`."""

        square_map = self._normalize_square_map({})
        observations: dict[str, PieceObservation] = {}
        prefer_image_assignment = (
            board_frame.board_detection_mode == "manual"
            and bool(board_frame.square_polygons_image)
        )

        for candidate in candidates:
            world_xyz = self.locate_piece_center_world(candidate, frame_bundle)
            square: str | None = None
            if prefer_image_assignment:
                if candidate.pixel_uv is not None:
                    square = self.assign_pixel_to_square(candidate.pixel_uv, board_frame)
                if square is None and world_xyz is not None:
                    square = self.assign_piece_to_square(
                        world_xyz=world_xyz,
                        square_centers_world=board_frame.square_centers_world,
                        max_distance_m=board_frame.assignment_margin_m,
                    )
            else:
                if world_xyz is not None:
                    square = self.assign_piece_to_square(
                        world_xyz=world_xyz,
                        square_centers_world=board_frame.square_centers_world,
                        max_distance_m=board_frame.assignment_margin_m,
                    )
                if square is None and candidate.pixel_uv is not None:
                    square = self.assign_pixel_to_square(candidate.pixel_uv, board_frame)
            if square is None:
                continue

            observation = PieceObservation(
                piece_name=candidate.piece_name,
                square=square,
                world_xyz=world_xyz or board_frame.square_centers_world.get(square),
                yaw_rad=candidate.yaw_rad,
                confidence=candidate.confidence,
            )
            existing = observations.get(square)
            if existing is not None and existing.confidence >= observation.confidence:
                continue
            observations[square] = observation
            square_map[square] = candidate.piece_name

        return ObservedBoard(
            by_square=square_map,
            observations=observations,
            timestamp=float(frame_bundle.timestamp),
        )

    def _observe_camera_board(self) -> ObservedBoard:
        """Camera-backed board observation path."""

        if self.frame_source is None:
            raise RuntimeError("Camera mode requires a frame_source.")

        frame_bundle = self.frame_source.get_observer_frame()
        board_frame = self.estimate_board_frame(frame_bundle)
        candidates = self.detect_piece_candidates(frame_bundle, board_frame)
        return self.build_observed_board_from_candidates(candidates, board_frame, frame_bundle)

    def _observe_mock_board(
        self,
        stubbed_board: Mapping[str, str | None] | None = None,
    ) -> ObservedBoard:
        """Mock observation path used for tests and fallback."""

        square_map = self._normalize_square_map(self._mock_observations)
        if stubbed_board is not None:
            square_map.update(self._normalize_square_map(stubbed_board))

        observations: dict[str, PieceObservation] = {}
        for square, piece_name in square_map.items():
            if piece_name is None:
                continue
            observations[square] = PieceObservation(
                piece_name=piece_name,
                square=square,
                world_xyz=self.geometry.square_center_world(square),
                yaw_rad=0.0,
                confidence=0.99,
            )

        return ObservedBoard(
            by_square=square_map,
            observations=observations,
            timestamp=time.time(),
        )

    def _validate_mode(self) -> None:
        """Validate the current observation mode."""

        if self.mode not in {"mock", "camera"}:
            raise ValueError(f"Unsupported BoardObserver mode: {self.mode!r}")

    def _normalize_square_map(
        self,
        square_map: Mapping[str, str | None],
    ) -> dict[str, str | None]:
        """Return a full 64-square map with missing squares filled as empty."""

        normalized = {square: None for square in self.geometry.all_squares()}
        for square, piece_name in square_map.items():
            normalized[square.lower()] = piece_name
        return normalized

    def _depth_at_pixel(self, depth_image: Any, pixel_uv: PixelUV) -> float | None:
        """Sample the depth image at the nearest integer pixel location."""

        row_count = _sequence_length(depth_image)
        if row_count is None or row_count <= 0:
            return None
        u = int(round(pixel_uv[0]))
        v = int(round(pixel_uv[1]))
        if v < 0 or v >= row_count:
            return None
        row = depth_image[v]
        col_count = _sequence_length(row)
        if col_count is None or u < 0 or u >= col_count:
            return None
        try:
            depth_value = float(row[u])
        except (TypeError, ValueError):
            return None
        if not math.isfinite(depth_value) or depth_value <= 0.0:
            return None
        return depth_value


def _manual_image_corners(
    calibration: BoardCalibration,
) -> tuple[dict[str, PixelUV] | None, dict[str, str] | None]:
    if calibration.board_outer_corners_image is None:
        return None, None
    oriented, permutation = canonicalize_image_corners(calibration.board_outer_corners_image)
    return oriented, permutation


def _manual_world_corners(
    *,
    calibration: BoardCalibration,
    geometry: BoardGeometry,
    image_permutation: dict[str, str] | None,
) -> dict[str, XYZ]:
    base_world = (
        calibration.board_outer_corners_world
        if calibration.board_outer_corners_world is not None
        else geometry.outer_corners_world_from_origin()
    )
    if image_permutation is None or calibration.board_outer_corners_world is None:
        return base_world
    return remap_world_corners_by_image_permutation(base_world, image_permutation)


def _extract_corner_map_from_metadata(metadata: Mapping[str, Any]) -> dict[str, PixelUV] | None:
    for key in (
        "live_board_outer_corners_image",
        "board_outer_corners_image",
        "phase2_board_outer_corners_image",
        "board_corners_image",
    ):
        value = metadata.get(key)
        if not isinstance(value, Mapping):
            continue
        parsed: dict[str, PixelUV] = {}
        for corner_key in ("a1", "h1", "h8", "a8"):
            pixel = _normalize_pixel(value.get(corner_key))
            if pixel is None:
                parsed = {}
                break
            parsed[corner_key] = pixel
        if len(parsed) == 4:
            oriented, _ = canonicalize_image_corners(parsed)
            return oriented
    return None


def _select_tracking_image(
    frame_bundle: CameraFrameBundle,
) -> tuple[Any, str, bool, tuple[int, int] | None, tuple[int, int] | None]:
    """Pick the image source used by live corner fitting.

    Returns:
    - tracking image payload
    - coordinate mode (`rgb`, `depth`, or metadata override)
    - alignment-active flag
    - color image size (w, h)
    - depth image size (w, h)
    """

    metadata = frame_bundle.metadata if isinstance(frame_bundle.metadata, Mapping) else {}
    color_size = _image_size(frame_bundle.rgb_image)
    depth_size = _image_size(frame_bundle.depth_image)
    alignment_active = _resolve_alignment_active(
        metadata=metadata,
        color_frame_name=frame_bundle.color_frame_name,
        depth_frame_name=frame_bundle.depth_frame_name,
        color_size=color_size,
        depth_size=depth_size,
    )
    mode_hint = _extract_fit_coordinate_mode(metadata)

    if mode_hint.startswith("depth") and frame_bundle.depth_image is not None:
        return frame_bundle.depth_image, mode_hint, alignment_active, color_size, depth_size
    if mode_hint.startswith("rgb") and frame_bundle.rgb_image is not None:
        return frame_bundle.rgb_image, mode_hint, alignment_active, color_size, depth_size
    if frame_bundle.rgb_image is not None:
        base_mode = "rgb_aligned" if alignment_active else "rgb"
        return frame_bundle.rgb_image, base_mode, alignment_active, color_size, depth_size
    if frame_bundle.depth_image is not None:
        return frame_bundle.depth_image, "depth_fallback", alignment_active, color_size, depth_size
    return None, "unknown", alignment_active, color_size, depth_size


def _track_corners_from_image(
    *,
    tracking_image: Any,
    seed_corners: Mapping[str, PixelUV],
    search_radius_px: int,
) -> tuple[dict[str, PixelUV] | None, float]:
    """Track corner seeds in image space using local RGB gradient maxima."""

    gray = _to_grayscale_image(tracking_image)
    if gray is None:
        return None, 0.0

    tracked: dict[str, PixelUV] = {}
    quality_samples: list[float] = []
    for key in ("a1", "h1", "h8", "a8"):
        seed = seed_corners.get(key)
        if seed is None:
            return None, 0.0
        seed_u = int(round(seed[0]))
        seed_v = int(round(seed[1]))
        best_uv = (float(seed_u), float(seed_v))
        best_score = -1.0
        for dv in range(-search_radius_px, search_radius_px + 1):
            for du in range(-search_radius_px, search_radius_px + 1):
                u = seed_u + du
                v = seed_v + dv
                gradient = _image_gradient_at(gray, u, v)
                if gradient <= 0.0:
                    continue
                distance_penalty = 0.015 * ((du * du + dv * dv) ** 0.5)
                score = gradient - distance_penalty
                if score > best_score:
                    best_score = score
                    best_uv = (float(u), float(v))
        if best_score < 1.0:
            return None, 0.0
        tracked[key] = best_uv
        quality_samples.append(best_score)
    oriented, _ = canonicalize_image_corners(tracked)
    if not quality_samples:
        return oriented, 0.0
    mean_quality = sum(quality_samples) / float(len(quality_samples))
    quality = _clamp01(mean_quality / 30.0)
    return oriented, quality


def _track_corners_from_rgb(
    *,
    rgb_image: Any,
    seed_corners: Mapping[str, PixelUV],
    search_radius_px: int,
) -> tuple[dict[str, PixelUV] | None, float]:
    """Backward-compatible alias for image-space tracking."""

    return _track_corners_from_image(
        tracking_image=rgb_image,
        seed_corners=seed_corners,
        search_radius_px=search_radius_px,
    )


def _to_grayscale_image(rgb_image: Any) -> list[list[float]] | None:
    """Convert a generic RGB-like image payload into grayscale rows."""

    row_count = _sequence_length(rgb_image)
    if row_count is None or row_count <= 0:
        return None
    grayscale: list[list[float]] = []
    for row_idx in range(row_count):
        row = rgb_image[row_idx]
        col_count = _sequence_length(row)
        if col_count is None or col_count <= 0:
            return None
        gray_row: list[float] = []
        for col_idx in range(col_count):
            pixel = row[col_idx]
            value = _pixel_to_gray(pixel)
            if value is None:
                return None
            gray_row.append(value)
        grayscale.append(gray_row)
    return grayscale


def _pixel_to_gray(pixel: Any) -> float | None:
    """Convert one pixel-like value into grayscale intensity."""

    if isinstance(pixel, (int, float)):
        return float(pixel)
    try:
        r, g, b = pixel
    except (TypeError, ValueError):
        return None
    return 0.299 * float(r) + 0.587 * float(g) + 0.114 * float(b)


def _image_gradient_at(gray: list[list[float]], u: int, v: int) -> float:
    left = _gray_at(gray, u - 1, v)
    right = _gray_at(gray, u + 1, v)
    up = _gray_at(gray, u, v - 1)
    down = _gray_at(gray, u, v + 1)
    if left is None or right is None or up is None or down is None:
        return 0.0
    gx = right - left
    gy = down - up
    return (gx * gx + gy * gy) ** 0.5


def _gray_at(gray: list[list[float]], u: int, v: int) -> float | None:
    if v < 0 or u < 0 or v >= len(gray):
        return None
    row = gray[v]
    if u >= len(row):
        return None
    return row[u]


def _image_corner_visibility_fraction(
    corners_image: Mapping[str, PixelUV],
    rgb_image: Any,
) -> float:
    """Visibility proxy based on in-frame corners and board coverage."""

    row_count = _sequence_length(rgb_image)
    if row_count is None or row_count <= 0:
        return 0.0
    first_row = rgb_image[0]
    col_count = _sequence_length(first_row)
    if col_count is None or col_count <= 0:
        return 0.0

    in_bounds = 0
    for uv in corners_image.values():
        if 0.0 <= uv[0] < float(col_count) and 0.0 <= uv[1] < float(row_count):
            in_bounds += 1
    bounds_fraction = in_bounds / 4.0

    a1 = corners_image["a1"]
    h1 = corners_image["h1"]
    h8 = corners_image["h8"]
    a8 = corners_image["a8"]
    quad = [a1, h1, h8, a8]
    area = 0.0
    for idx, point in enumerate(quad):
        nxt = quad[(idx + 1) % len(quad)]
        area += point[0] * nxt[1] - nxt[0] * point[1]
    area = abs(area) * 0.5
    image_area = float(max(1, row_count * col_count))
    area_fraction = _clamp01(area / image_area / 0.35)
    return _clamp01(0.65 * bounds_fraction + 0.35 * area_fraction)


def _motion_consistency_confidence(
    prev_corners: Mapping[str, PixelUV] | None,
    new_corners: Mapping[str, PixelUV],
) -> float:
    """Penalize abrupt corner jumps frame-to-frame."""

    if prev_corners is None:
        return 1.0
    displacements = []
    for key in ("a1", "h1", "h8", "a8"):
        prev = prev_corners.get(key)
        current = new_corners.get(key)
        if prev is None or current is None:
            continue
        displacements.append(math.dist(prev, current))
    if not displacements:
        return 0.0
    mean_disp = sum(displacements) / float(len(displacements))
    return _clamp01(1.0 - mean_disp / 85.0)


def _smooth_corners(
    previous: Mapping[str, PixelUV] | None,
    current: Mapping[str, PixelUV],
    *,
    alpha: float,
) -> dict[str, PixelUV]:
    """Exponential smoothing in image space."""

    alpha_clamped = _clamp01(alpha)
    if previous is None:
        return {key: (float(uv[0]), float(uv[1])) for key, uv in current.items()}
    smoothed: dict[str, PixelUV] = {}
    for key in ("a1", "h1", "h8", "a8"):
        prev = previous.get(key, current[key])
        curr = current[key]
        smoothed[key] = (
            (1.0 - alpha_clamped) * float(prev[0]) + alpha_clamped * float(curr[0]),
            (1.0 - alpha_clamped) * float(prev[1]) + alpha_clamped * float(curr[1]),
        )
    return smoothed


def _project_corner_map_to_world(
    *,
    corners_image: Mapping[str, PixelUV],
    frame_bundle: CameraFrameBundle,
    transform_provider: TransformProvider | None,
    fit_coordinate_mode: str,
    alignment_active: bool,
) -> tuple[dict[str, XYZ] | None, dict[str, PixelUV] | None]:
    if transform_provider is None:
        return None, None
    projected: dict[str, XYZ] = {}
    projected_depth_pixels: dict[str, PixelUV] = {}
    for key, pixel_uv in corners_image.items():
        depth_uv = _map_fit_pixel_to_depth(
            pixel_uv=pixel_uv,
            fit_coordinate_mode=fit_coordinate_mode,
            alignment_active=alignment_active,
            frame_bundle=frame_bundle,
        )
        projected_depth_pixels[key] = depth_uv
        depth_m = _depth_at_pixel_with_radius(frame_bundle.depth_image, depth_uv, radius_px=5)
        if depth_m is None:
            return None, projected_depth_pixels
        try:
            world_xyz = transform_provider.pixel_to_world(
                pixel_uv=depth_uv,
                depth_m=depth_m,
                intrinsics=frame_bundle.intrinsics,
                depth_frame_name=frame_bundle.depth_frame_name,
            )
        except RuntimeError:
            return None, projected_depth_pixels
        if world_xyz is None:
            return None, projected_depth_pixels
        projected[key] = world_xyz
    return projected, projected_depth_pixels


def _map_fit_pixel_to_depth(
    *,
    pixel_uv: PixelUV,
    fit_coordinate_mode: str,
    alignment_active: bool,
    frame_bundle: CameraFrameBundle,
) -> PixelUV:
    """Convert fitted image-space corner pixels into depth-image coordinates."""

    mode = fit_coordinate_mode.lower()
    if mode.startswith("depth"):
        return (float(pixel_uv[0]), float(pixel_uv[1]))
    if alignment_active:
        return (float(pixel_uv[0]), float(pixel_uv[1]))

    metadata = frame_bundle.metadata if isinstance(frame_bundle.metadata, Mapping) else {}
    homography = _extract_homography_3x3(metadata)
    if homography is not None:
        mapped = _apply_homography(pixel_uv, homography)
        if mapped is not None:
            return mapped

    offset = _extract_depth_offset(metadata)
    if offset is not None:
        return (float(pixel_uv[0] + offset[0]), float(pixel_uv[1] + offset[1]))

    color_size = _image_size(frame_bundle.rgb_image)
    depth_size = _image_size(frame_bundle.depth_image)
    if color_size is not None and depth_size is not None and color_size != depth_size:
        color_w, color_h = color_size
        depth_w, depth_h = depth_size
        if color_w > 0 and color_h > 0:
            scale_u = depth_w / float(color_w)
            scale_v = depth_h / float(color_h)
            return (float(pixel_uv[0]) * scale_u, float(pixel_uv[1]) * scale_v)
    return (float(pixel_uv[0]), float(pixel_uv[1]))


def _extract_homography_3x3(metadata: Mapping[str, Any]) -> tuple[tuple[float, float, float], ...] | None:
    """Extract RGB->depth homography from metadata if available."""

    for key in ("rgb_to_depth_homography", "color_to_depth_homography"):
        raw = metadata.get(key)
        if not isinstance(raw, (list, tuple)) or len(raw) != 3:
            continue
        try:
            rows = tuple(
                (float(raw[row][0]), float(raw[row][1]), float(raw[row][2])) for row in range(3)
            )
        except (TypeError, ValueError, IndexError):
            continue
        return rows
    return None


def _apply_homography(
    pixel_uv: PixelUV,
    homography: tuple[tuple[float, float, float], ...],
) -> PixelUV | None:
    """Apply 3x3 projective map to a pixel."""

    u, v = float(pixel_uv[0]), float(pixel_uv[1])
    x = homography[0][0] * u + homography[0][1] * v + homography[0][2]
    y = homography[1][0] * u + homography[1][1] * v + homography[1][2]
    w = homography[2][0] * u + homography[2][1] * v + homography[2][2]
    if abs(w) <= 1e-9:
        return None
    return (x / w, y / w)


def _extract_depth_offset(metadata: Mapping[str, Any]) -> tuple[float, float] | None:
    """Extract simple RGB->depth pixel offset if provided."""

    raw = metadata.get("rgb_to_depth_offset_px") or metadata.get("color_to_depth_offset_px")
    if not isinstance(raw, (list, tuple)) or len(raw) != 2:
        return None
    try:
        return (float(raw[0]), float(raw[1]))
    except (TypeError, ValueError):
        return None


def _extract_fit_coordinate_mode(metadata: Mapping[str, Any]) -> str:
    """Resolve configured fit coordinate mode from metadata."""

    for key in ("board_fit_coordinate_mode", "fit_coordinate_mode", "live_fit_coordinate_mode"):
        raw = metadata.get(key)
        if isinstance(raw, str) and raw.strip():
            return raw.strip().lower()
    return "rgb"


def _resolve_alignment_active(
    *,
    metadata: Mapping[str, Any],
    color_frame_name: str | None,
    depth_frame_name: str | None,
    color_size: tuple[int, int] | None,
    depth_size: tuple[int, int] | None,
) -> bool:
    """Infer whether RGB and depth pixel spaces are aligned."""

    for key in (
        "rgb_depth_aligned",
        "color_depth_aligned",
        "depth_aligned_to_color",
        "color_aligned_to_depth",
        "alignment_active",
    ):
        flag = _as_optional_bool(metadata.get(key))
        if flag is not None:
            return flag

    same_frame = bool(color_frame_name and depth_frame_name and color_frame_name == depth_frame_name)
    same_size = bool(color_size is not None and depth_size is not None and color_size == depth_size)
    return same_frame and same_size


def _as_optional_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    return None


def _image_size(image: Any) -> tuple[int, int] | None:
    """Return image size as (width, height) for nested sequence payloads."""

    height = _sequence_length(image)
    if height is None or height <= 0:
        return None
    first_row = image[0]
    width = _sequence_length(first_row)
    if width is None or width <= 0:
        return None
    return (int(width), int(height))


def _intrinsics_debug_dict(intrinsics: CameraIntrinsics | None) -> dict[str, Any]:
    """Serialize intrinsics for diagnostics."""

    if intrinsics is None:
        return {}
    return {
        "fx": float(intrinsics.fx),
        "fy": float(intrinsics.fy),
        "cx": float(intrinsics.cx),
        "cy": float(intrinsics.cy),
        "frame_name": intrinsics.frame_name,
        "width": intrinsics.width,
        "height": intrinsics.height,
    }


def _depth_at_pixel_with_radius(
    depth_image: Any,
    pixel_uv: PixelUV,
    radius_px: int,
) -> float | None:
    u0 = int(round(pixel_uv[0]))
    v0 = int(round(pixel_uv[1]))
    for radius in range(max(0, radius_px) + 1):
        if radius == 0:
            depth_value = _depth_at_indices(depth_image, u0, v0)
            if depth_value is not None:
                return depth_value
            continue
        for dv in range(-radius, radius + 1):
            for du in range(-radius, radius + 1):
                if abs(du) != radius and abs(dv) != radius:
                    continue
                depth_value = _depth_at_indices(depth_image, u0 + du, v0 + dv)
                if depth_value is not None:
                    return depth_value
    return None


def _depth_at_indices(depth_image: Any, u: int, v: int) -> float | None:
    row_count = _sequence_length(depth_image)
    if row_count is None or v < 0 or v >= row_count:
        return None
    row = depth_image[v]
    col_count = _sequence_length(row)
    if col_count is None or u < 0 or u >= col_count:
        return None
    try:
        depth_value = float(row[u])
    except (TypeError, ValueError):
        return None
    if not math.isfinite(depth_value) or depth_value <= 0.0:
        return None
    return depth_value


def _depth_gradient_at(depth_image: Any, u: int, v: int) -> float:
    left = _depth_at_indices(depth_image, u - 1, v)
    right = _depth_at_indices(depth_image, u + 1, v)
    up = _depth_at_indices(depth_image, u, v - 1)
    down = _depth_at_indices(depth_image, u, v + 1)
    if left is None or right is None or up is None or down is None:
        return 0.0
    gx = abs(right - left)
    gy = abs(down - up)
    return (gx * gx + gy * gy) ** 0.5


def _refine_corners_from_depth(
    *,
    depth_image: Any,
    seed_corners: Mapping[str, PixelUV],
    search_radius_px: int,
    min_gradient_m: float,
) -> tuple[dict[str, PixelUV] | None, float]:
    refined: dict[str, PixelUV] = {}
    quality_samples: list[float] = []
    for key, seed in seed_corners.items():
        seed_u = int(round(seed[0]))
        seed_v = int(round(seed[1]))
        best_u = seed_u
        best_v = seed_v
        best_score = -1.0
        for dv in range(-search_radius_px, search_radius_px + 1):
            for du in range(-search_radius_px, search_radius_px + 1):
                u = seed_u + du
                v = seed_v + dv
                gradient = _depth_gradient_at(depth_image, u, v)
                if gradient <= 0.0:
                    continue
                # Bias toward points near seed so corner tracking stays stable.
                distance_penalty = 0.0002 * ((du * du + dv * dv) ** 0.5)
                score = gradient - distance_penalty
                if score > best_score:
                    best_score = score
                    best_u = u
                    best_v = v
        if best_score < min_gradient_m:
            return None, 0.0
        refined[key] = (float(best_u), float(best_v))
        quality_samples.append(best_score)
    oriented, _ = canonicalize_image_corners(refined)
    mean_quality = sum(quality_samples) / float(len(quality_samples)) if quality_samples else 0.0
    normalized_quality = _clamp01(mean_quality / max(min_gradient_m * 3.0, 1e-6))
    return oriented, normalized_quality


def _edge_visibility_fraction(
    *,
    depth_image: Any,
    corners_image: Mapping[str, PixelUV],
    samples_per_edge: int,
    min_gradient_m: float,
) -> float:
    edges = (
        ("a1", "h1"),
        ("h1", "h8"),
        ("h8", "a8"),
        ("a8", "a1"),
    )
    visible = 0
    total = 0
    for start_key, end_key in edges:
        start = corners_image[start_key]
        end = corners_image[end_key]
        for point in _sample_edge_points(start, end, samples_per_edge):
            total += 1
            gradient = _depth_gradient_at(
                depth_image,
                int(round(point[0])),
                int(round(point[1])),
            )
            if gradient >= min_gradient_m:
                visible += 1
    if total <= 0:
        return 0.0
    return visible / float(total)


def _corner_geometry_confidence(corners_image: Mapping[str, PixelUV]) -> float:
    a1 = corners_image["a1"]
    h1 = corners_image["h1"]
    h8 = corners_image["h8"]
    a8 = corners_image["a8"]
    width_bottom = math.dist(a1, h1)
    width_top = math.dist(a8, h8)
    height_left = math.dist(a1, a8)
    height_right = math.dist(h1, h8)
    if min(width_bottom, width_top, height_left, height_right) <= 1e-6:
        return 0.0
    width_ratio = min(width_bottom, width_top) / max(width_bottom, width_top)
    height_ratio = min(height_left, height_right) / max(height_left, height_right)
    return _clamp01(0.5 * width_ratio + 0.5 * height_ratio)


def _sample_edge_points(start: PixelUV, end: PixelUV, samples: int) -> list[PixelUV]:
    if samples <= 0:
        return []
    points: list[PixelUV] = []
    for idx in range(1, samples + 1):
        t = idx / float(samples + 1)
        points.append(
            (
                start[0] + (end[0] - start[0]) * t,
                start[1] + (end[1] - start[1]) * t,
            )
        )
    return points


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _default_calibration(geometry: BoardGeometry) -> BoardCalibration:
    """Default calibration when board_calibration.yaml is not supplied."""

    return BoardCalibration(
        board_detection_mode="manual",
        board_orientation="a1_lower_left_h8_upper_right",
        a1_reference="image_lower_left",
        nominal_square_size_cm=geometry.square_size_m * 100.0,
        min_square_size_cm=3.4,
        max_square_size_cm=3.78,
        board_outer_corners_image=None,
        board_outer_corners_world=geometry.outer_corners_world_from_origin(),
    )


def _manual_mode_live_fit_result(
    *,
    manual_image: Mapping[str, PixelUV],
) -> LiveCornerFitResult:
    """Build a placeholder live-fit result for fixed observer calibration mode."""

    return LiveCornerFitResult(
        corners_image=dict(manual_image),
        corners_world=None,
        corner_confidence=1.0,
        visible_board_fraction=1.0,
        live_fit_confidence=1.0,
        accepted=True,
        source="fixed_manual_calibration",
        reason="manual_primary",
        fit_state="manual_fixed",
        used_last_good=False,
        fit_coordinate_mode="manual",
        alignment_active=False,
        color_image_size=None,
        depth_image_size=None,
        fitted_corner_pixels=dict(manual_image),
        projected_corner_depth_pixels=None,
        projected_corner_world=None,
    )


def _norm_axis(start: XYZ, end: XYZ) -> XYZ:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dz = end[2] - start[2]
    norm = (dx * dx + dy * dy + dz * dz) ** 0.5
    if norm <= 1e-9:
        return (0.0, 0.0, 0.0)
    return (dx / norm, dy / norm, dz / norm)


def _normalize_pixel(value: Any) -> PixelUV | None:
    """Normalize a pixel tuple-like value into `(u, v)`."""

    if value is None:
        return None
    try:
        u, v = value
    except (TypeError, ValueError):
        return None
    return (float(u), float(v))


def _normalize_xyz(value: Any) -> XYZ | None:
    """Normalize a world-coordinate tuple-like value into `XYZ`."""

    if value is None:
        return None
    try:
        x, y, z = value
    except (TypeError, ValueError):
        return None
    return (float(x), float(y), float(z))


def _optional_float(value: Any) -> float | None:
    """Normalize optional numeric values."""

    if value is None:
        return None
    return float(value)


def _sequence_length(value: Any) -> int | None:
    """Return the sequence length if available."""

    try:
        return len(value)
    except TypeError:
        return None


def _average_square_pixel_size(square_centers_image: Mapping[str, PixelUV]) -> float | None:
    """Estimate average square size in pixels from center spacing."""

    if not square_centers_image:
        return None
    distances: list[float] = []
    for rank_char in "12345678":
        for idx in range(7):
            sq_a = f"{'abcdefgh'[idx]}{rank_char}"
            sq_b = f"{'abcdefgh'[idx + 1]}{rank_char}"
            if sq_a in square_centers_image and sq_b in square_centers_image:
                a = square_centers_image[sq_a]
                b = square_centers_image[sq_b]
                distances.append(math.dist(a, b))
    for file_char in "abcdefgh":
        for idx in range(7):
            sq_a = f"{file_char}{'12345678'[idx]}"
            sq_b = f"{file_char}{'12345678'[idx + 1]}"
            if sq_a in square_centers_image and sq_b in square_centers_image:
                a = square_centers_image[sq_a]
                b = square_centers_image[sq_b]
                distances.append(math.dist(a, b))
    if not distances:
        return None
    return sum(distances) / float(len(distances))

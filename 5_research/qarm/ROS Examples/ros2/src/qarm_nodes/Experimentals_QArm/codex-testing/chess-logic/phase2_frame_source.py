"""Phase 2 camera-frame adapter for the Phase 3 observer pipeline."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from board_observer import CameraFrameBundle, CameraIntrinsics, FrameSource


@dataclass(frozen=True)
class Phase2FrameConfig:
    """Default Phase 2 camera parameters from the current RGBD publisher."""

    fx: float = 592.451
    fy: float = 592.451
    cx: float = 318.592
    cy: float = 249.341
    width: int = 640
    height: int = 480
    color_frame_name: str = "camera_color"
    depth_frame_name: str = "left_ir_optical_frame"

    def intrinsics(self) -> CameraIntrinsics:
        """Return observer intrinsics in the shared Phase 3 format."""

        return CameraIntrinsics(
            fx=self.fx,
            fy=self.fy,
            cx=self.cx,
            cy=self.cy,
            frame_name=self.depth_frame_name,
            width=self.width,
            height=self.height,
        )


class Phase2FrameSource(FrameSource):
    """Pure-Python adapter that produces `CameraFrameBundle` objects.

    This stays outside ROS 2 node creation. Frame providers can later be backed
    by a subscriber cache, file bridge, or any other Phase 2 capture path.
    """

    def __init__(
        self,
        *,
        rgb_provider: Callable[[], Any] | None = None,
        depth_provider: Callable[[], Any] | None = None,
        metadata_provider: Callable[[], dict[str, Any]] | None = None,
        timestamp_provider: Callable[[], float] | None = None,
        intrinsics: CameraIntrinsics | None = None,
        color_frame_name: str = "camera_color",
        depth_frame_name: str = "left_ir_optical_frame",
        static_rgb_image: Any = None,
        static_depth_image: Any = None,
        static_metadata: dict[str, Any] | None = None,
    ) -> None:
        self.rgb_provider = rgb_provider
        self.depth_provider = depth_provider
        self.metadata_provider = metadata_provider
        self.timestamp_provider = timestamp_provider or time.time
        self.intrinsics = intrinsics
        self.color_frame_name = color_frame_name
        self.depth_frame_name = depth_frame_name
        self.static_rgb_image = static_rgb_image
        self.static_depth_image = static_depth_image
        self.static_metadata = dict(static_metadata or {})

    @classmethod
    def from_static_frames(
        cls,
        *,
        rgb_image: Any,
        depth_image: Any,
        metadata: dict[str, Any] | None = None,
        config: Phase2FrameConfig | None = None,
    ) -> "Phase2FrameSource":
        """Build a demo-friendly static frame source."""

        frame_config = config or Phase2FrameConfig()
        return cls(
            intrinsics=frame_config.intrinsics(),
            color_frame_name=frame_config.color_frame_name,
            depth_frame_name=frame_config.depth_frame_name,
            static_rgb_image=rgb_image,
            static_depth_image=depth_image,
            static_metadata=metadata,
        )

    def get_observer_frame(self) -> CameraFrameBundle:
        """Return the latest observer-pose RGB/depth frame bundle."""

        rgb_image = self.rgb_provider() if self.rgb_provider is not None else self.static_rgb_image
        depth_image = self.depth_provider() if self.depth_provider is not None else self.static_depth_image
        if rgb_image is None or depth_image is None:
            raise RuntimeError("Phase2FrameSource requires both RGB and depth frames.")

        metadata: dict[str, Any] = dict(self.static_metadata)
        if self.metadata_provider is not None:
            metadata.update(self.metadata_provider())

        return CameraFrameBundle(
            rgb_image=rgb_image,
            depth_image=depth_image,
            intrinsics=self.intrinsics,
            color_frame_name=self.color_frame_name,
            depth_frame_name=self.depth_frame_name,
            timestamp=float(self.timestamp_provider()),
            metadata=metadata,
        )

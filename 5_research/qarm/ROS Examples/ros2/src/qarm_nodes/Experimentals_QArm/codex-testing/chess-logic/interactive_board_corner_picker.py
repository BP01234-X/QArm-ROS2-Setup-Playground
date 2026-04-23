#!/usr/bin/env python3

"""Interactive fixed-board corner calibration tool for Phase 4."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import cv2
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("OpenCV (cv2) is required for interactive_board_corner_picker.py") from exc

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("PyYAML is required for interactive_board_corner_picker.py") from exc


ORDERED_CORNERS = ("a1", "h1", "h8", "a8")
WINDOW_NAME = "Board Corner Picker"


@dataclass
class PickerState:
    image_bgr: Any
    clicks: list[tuple[int, int]] = field(default_factory=list)
    mouse_xy: tuple[int, int] | None = None

    def reset(self) -> None:
        self.clicks.clear()

    def undo(self) -> None:
        if self.clicks:
            self.clicks.pop()


def _extract_corner_map_from_json(path: Path) -> dict[str, tuple[int, int]] | None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return None
    for key in (
        "live_board_outer_corners_image",
        "board_outer_corners_image",
        "phase2_board_outer_corners_image",
        "board_corners_image",
    ):
        raw = payload.get(key)
        if not isinstance(raw, dict):
            continue
        parsed: dict[str, tuple[int, int]] = {}
        for corner_name in ORDERED_CORNERS:
            value = raw.get(corner_name)
            if not isinstance(value, (list, tuple)) or len(value) != 2:
                parsed = {}
                break
            try:
                parsed[corner_name] = (int(round(float(value[0]))), int(round(float(value[1]))))
            except (TypeError, ValueError):
                parsed = {}
                break
        if len(parsed) == 4:
            return parsed
    return None


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if payload is None:
        return {}
    if not isinstance(payload, dict):
        raise ValueError(f"Expected YAML mapping at {path}")
    return payload


def _save_yaml(
    *,
    config_path: Path,
    corners: list[tuple[int, int]],
    keep_mode: bool,
) -> None:
    payload = _load_yaml(config_path)
    payload["board_outer_corners_image"] = {
        ORDERED_CORNERS[idx]: [float(x), float(y)]
        for idx, (x, y) in enumerate(corners)
    }
    if not keep_mode:
        payload["board_detection_mode"] = "manual"
    config_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def _draw_overlay(state: PickerState, show_crosshair: bool = True):
    frame = state.image_bgr.copy()

    if show_crosshair and state.mouse_xy is not None:
        mx, my = state.mouse_xy
        h, w = frame.shape[:2]
        cv2.line(frame, (0, my), (w - 1, my), (90, 90, 90), 1, cv2.LINE_AA)
        cv2.line(frame, (mx, 0), (mx, h - 1), (90, 90, 90), 1, cv2.LINE_AA)

    for idx, (x, y) in enumerate(state.clicks):
        label = ORDERED_CORNERS[idx]
        cv2.circle(frame, (x, y), 6, (0, 0, 255), -1, cv2.LINE_AA)
        cv2.circle(frame, (x, y), 10, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(
            frame,
            label,
            (x + 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

    if len(state.clicks) >= 2:
        for idx in range(len(state.clicks) - 1):
            cv2.line(frame, state.clicks[idx], state.clicks[idx + 1], (255, 120, 0), 2, cv2.LINE_AA)

    if len(state.clicks) == 4:
        pts = state.clicks + [state.clicks[0]]
        for idx in range(4):
            cv2.line(frame, pts[idx], pts[idx + 1], (0, 255, 0), 2, cv2.LINE_AA)

    next_corner = ORDERED_CORNERS[len(state.clicks)] if len(state.clicks) < 4 else "done"
    instructions = [
        f"Click corners in order: a1, h1, h8, a8 | next: {next_corner}",
        "u=undo  r=reset  s=save  q=quit",
    ]
    y = 24
    for line in instructions:
        cv2.putText(
            frame,
            line,
            (12, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        y += 26
    return frame


def _mouse_callback(event, x, y, _flags, user_data) -> None:
    state: PickerState = user_data
    state.mouse_xy = (int(x), int(y))
    if event == cv2.EVENT_LBUTTONDOWN and len(state.clicks) < 4:
        state.clicks.append((int(x), int(y)))


def _default_debug_image_path(image_path: Path) -> Path:
    suffix = image_path.suffix if image_path.suffix else ".png"
    return image_path.with_name(f"{image_path.stem}_board_corners_overlay{suffix}")


def _find_latest_recorder_rgb_image() -> Path | None:
    """Find newest rgb.jpg saved by rolling recorder."""

    frames_dir = Path(__file__).resolve().parents[1] / "image-recorder" / "frames"
    if not frames_dir.exists():
        return None
    latest: Path | None = None
    for candidate in frames_dir.glob("*/rgb.jpg"):
        try:
            mtime = candidate.stat().st_mtime
        except OSError:
            continue
        if latest is None:
            latest = candidate
            latest_mtime = mtime
            continue
        if mtime > latest_mtime:
            latest = candidate
            latest_mtime = mtime
    return latest


def _resolve_image_path(image_arg: Path | None) -> Path:
    """Resolve image path from argument or latest recorder frame."""

    if image_arg is not None:
        if image_arg.exists():
            return image_arg
        latest = _find_latest_recorder_rgb_image()
        hint = f" Latest recorder image: {latest}" if latest is not None else ""
        raise RuntimeError(f"Image not found: {image_arg}.{hint}")

    latest = _find_latest_recorder_rgb_image()
    if latest is None:
        raise RuntimeError(
            "No --image provided and no recorder frame found at "
            "codex-testing/image-recorder/frames/*/rgb.jpg"
        )
    return latest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--image",
        type=Path,
        help="Path to observer RGB image. If omitted, latest recorder rgb.jpg is used.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).resolve().parent / "config" / "board_calibration.yaml",
        help="Path to board_calibration.yaml.",
    )
    parser.add_argument(
        "--from-json",
        type=Path,
        help="Optional JSON metadata source to prefill corners if available.",
    )
    parser.add_argument(
        "--debug-image",
        type=Path,
        help="Optional output path for saved overlay debug image.",
    )
    parser.add_argument(
        "--keep-mode",
        action="store_true",
        help="Do not force board_detection_mode=manual on save.",
    )
    args = parser.parse_args()

    image_path = _resolve_image_path(args.image)
    print(f"Using image: {image_path}")
    image_bgr = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise RuntimeError(f"Unable to read image: {image_path}")

    state = PickerState(image_bgr=image_bgr)

    if args.from_json is not None and args.from_json.exists():
        seeded = _extract_corner_map_from_json(args.from_json)
        if seeded is not None:
            state.clicks = [seeded[name] for name in ORDERED_CORNERS]
            print(f"Prefilled corners from JSON: {args.from_json}")

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(WINDOW_NAME, _mouse_callback, state)

    saved = False
    while True:
        preview = _draw_overlay(state, show_crosshair=True)
        cv2.imshow(WINDOW_NAME, preview)
        key = cv2.waitKey(20) & 0xFF

        if key == ord("u"):
            state.undo()
        elif key == ord("r"):
            state.reset()
        elif key == ord("s"):
            if len(state.clicks) != 4:
                print("Need exactly 4 points before saving.")
                continue
            _save_yaml(config_path=args.config, corners=state.clicks, keep_mode=args.keep_mode)
            debug_path = args.debug_image or _default_debug_image_path(image_path)
            final_overlay = _draw_overlay(state, show_crosshair=False)
            cv2.imwrite(str(debug_path), final_overlay)
            print(f"Saved calibration to: {args.config}")
            print(f"Saved debug overlay: {debug_path}")
            for idx, (x, y) in enumerate(state.clicks):
                print(f"  {ORDERED_CORNERS[idx]}: [{float(x):.1f}, {float(y):.1f}]")
            if not args.keep_mode:
                print("  board_detection_mode: manual")
            saved = True
            break
        elif key == ord("q") or key == 27:
            break

    cv2.destroyAllWindows()
    if not saved:
        print("Exited without saving.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

"""Save fixed observer-view board corners into board_calibration.yaml."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from board_geometry import canonicalize_image_corners

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("PyYAML is required for save_fixed_board_corners.py") from exc


def _parse_uv(value: str) -> tuple[float, float]:
    parts = [item.strip() for item in value.split(",")]
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(f"Expected 'u,v' format, got: {value!r}")
    try:
        return (float(parts[0]), float(parts[1]))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid numeric pixel coordinate: {value!r}") from exc


def _extract_corners_from_json(path: Path) -> dict[str, tuple[float, float]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Corners JSON must be an object.")
    for key in (
        "live_board_outer_corners_image",
        "board_outer_corners_image",
        "phase2_board_outer_corners_image",
        "board_corners_image",
    ):
        raw = payload.get(key)
        if not isinstance(raw, dict):
            continue
        parsed: dict[str, tuple[float, float]] = {}
        for corner in ("a1", "h1", "h8", "a8"):
            value = raw.get(corner)
            if not isinstance(value, (list, tuple)) or len(value) != 2:
                parsed = {}
                break
            parsed[corner] = (float(value[0]), float(value[1]))
        if len(parsed) == 4:
            oriented, _ = canonicalize_image_corners(parsed)
            return oriented
    raise ValueError("No usable corner map found in JSON payload.")


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if payload is None:
        return {}
    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping in YAML: {path}")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).resolve().parent / "config" / "board_calibration.yaml",
        help="Path to board_calibration.yaml.",
    )
    parser.add_argument("--a1", type=_parse_uv, help="A1 pixel as 'u,v'.")
    parser.add_argument("--h1", type=_parse_uv, help="H1 pixel as 'u,v'.")
    parser.add_argument("--h8", type=_parse_uv, help="H8 pixel as 'u,v'.")
    parser.add_argument("--a8", type=_parse_uv, help="A8 pixel as 'u,v'.")
    parser.add_argument(
        "--from-json",
        type=Path,
        help="Optional JSON file containing board corner metadata.",
    )
    parser.add_argument(
        "--keep-mode",
        action="store_true",
        help="Do not force board_detection_mode=manual.",
    )
    args = parser.parse_args()

    if args.from_json is not None:
        corners = _extract_corners_from_json(args.from_json)
    else:
        if not all((args.a1, args.h1, args.h8, args.a8)):
            raise ValueError("Provide all four corners (--a1 --h1 --h8 --a8) or use --from-json.")
        corners, _ = canonicalize_image_corners(
            {
                "a1": args.a1,
                "h1": args.h1,
                "h8": args.h8,
                "a8": args.a8,
            }
        )

    payload = _load_yaml(args.config)
    payload["board_outer_corners_image"] = {
        key: [round(corners[key][0], 3), round(corners[key][1], 3)]
        for key in ("a1", "h1", "h8", "a8")
    }
    if not args.keep_mode:
        payload["board_detection_mode"] = "manual"

    args.config.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    print(f"Saved fixed observer board corners to: {args.config}")
    for key in ("a1", "h1", "h8", "a8"):
        uv = payload["board_outer_corners_image"][key]
        print(f"  {key}: {uv}")
    if not args.keep_mode:
        print("  board_detection_mode: manual")


if __name__ == "__main__":
    main()

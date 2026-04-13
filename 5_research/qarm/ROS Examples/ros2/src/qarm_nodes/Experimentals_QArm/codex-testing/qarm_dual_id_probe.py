#!/usr/bin/env python3

"""Identify multiple physical QArms by assigning each device ID a LED color."""

from __future__ import annotations

import argparse
import signal
import sys
import time
from typing import Iterable

import numpy as np

from pal.products.qarm import QArm


COLOR_MAP = {
    "green": np.array([0.0, 1.0, 0.0], dtype=np.float64),
    "purple": np.array([1.0, 0.0, 1.0], dtype=np.float64),
    "red": np.array([1.0, 0.0, 0.0], dtype=np.float64),
    "blue": np.array([0.0, 0.0, 1.0], dtype=np.float64),
    "yellow": np.array([1.0, 1.0, 0.0], dtype=np.float64),
    "cyan": np.array([0.0, 1.0, 1.0], dtype=np.float64),
    "white": np.array([1.0, 1.0, 1.0], dtype=np.float64),
    "off": np.array([0.0, 0.0, 0.0], dtype=np.float64),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Open one or more physical QArms by device ID and set their LEDs so "
            "you can identify which hardware maps to each ID."
        )
    )
    parser.add_argument(
        "--device-ids",
        type=int,
        nargs="+",
        default=[0, 1],
        help="Device IDs to probe. Default: 0 1",
    )
    parser.add_argument(
        "--colors",
        nargs="+",
        default=["green", "purple"],
        help=(
            "Colors to assign in order. If fewer colors than device IDs are given, "
            "the colors repeat. Default: green purple"
        ),
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=20.0,
        help="How long to hold the LEDs on before shutting down. Default: 20 seconds",
    )
    parser.add_argument(
        "--blink-period",
        type=float,
        default=0.0,
        help=(
            "Optional blink period in seconds. Use 0 to keep LEDs solid. "
            "Example: 0.5"
        ),
    )
    return parser.parse_args()


def resolve_colors(color_names: Iterable[str], count: int) -> list[tuple[str, np.ndarray]]:
    entries: list[tuple[str, np.ndarray]] = []
    names = list(color_names)
    if not names:
        raise ValueError("At least one color must be provided.")

    for index in range(count):
        name = names[index % len(names)].lower()
        if name not in COLOR_MAP:
            valid = ", ".join(sorted(COLOR_MAP))
            raise ValueError(f"Unknown color '{name}'. Valid colors: {valid}")
        entries.append((name, COLOR_MAP[name]))
    return entries


def set_led(arm: QArm, color: np.ndarray) -> None:
    arm.write_led(color)


def set_all_off(arms: list[QArm]) -> None:
    for arm in arms:
        try:
            set_led(arm, COLOR_MAP["off"])
        except Exception as exc:  # pragma: no cover - best effort cleanup
            print(f"Cleanup warning while turning LED off: {exc}", file=sys.stderr)


def terminate_all(arms: list[QArm]) -> None:
    for arm in arms:
        try:
            arm.terminate()
        except Exception as exc:  # pragma: no cover - best effort cleanup
            print(f"Cleanup warning while terminating arm: {exc}", file=sys.stderr)


def main() -> int:
    args = parse_args()
    color_assignments = resolve_colors(args.colors, len(args.device_ids))

    arms: list[QArm] = []
    stop_requested = False

    def request_stop(signum, _frame) -> None:
        nonlocal stop_requested
        stop_requested = True
        print(f"\nReceived signal {signum}. Shutting down probe.")

    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)

    try:
        print("Opening QArms:")
        for device_id, (color_name, _) in zip(args.device_ids, color_assignments):
            print(f"  device_id={device_id} -> {color_name}")
            arm = QArm(deviceId=device_id)
            if not arm.status:
                raise RuntimeError(f"Failed to open QArm with device_id={device_id}")
            arms.append(arm)

        print("\nApplying LED assignments.")
        for arm, device_id, (color_name, color) in zip(arms, args.device_ids, color_assignments):
            set_led(arm, color)
            print(f"  device_id={device_id} set to {color_name}")

        if args.blink_period > 0.0:
            print(
                f"\nBlinking for {args.duration:.1f} seconds with period "
                f"{args.blink_period:.2f} seconds."
            )
            deadline = time.monotonic() + args.duration
            leds_on = True
            while not stop_requested and time.monotonic() < deadline:
                time.sleep(args.blink_period)
                leds_on = not leds_on
                for arm, (_, color) in zip(arms, color_assignments):
                    set_led(arm, color if leds_on else COLOR_MAP["off"])
        else:
            print(f"\nHolding LEDs for {args.duration:.1f} seconds. Press Ctrl+C to stop early.")
            deadline = time.monotonic() + args.duration
            while not stop_requested and time.monotonic() < deadline:
                time.sleep(0.1)

        return 0
    except Exception as exc:
        print(f"Probe failed: {exc}", file=sys.stderr)
        return 1
    finally:
        set_all_off(arms)
        terminate_all(arms)


if __name__ == "__main__":
    raise SystemExit(main())

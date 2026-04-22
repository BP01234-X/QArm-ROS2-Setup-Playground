"""File-bridge client for the existing QArm Phase 2 control path."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now_compact() -> str:
    """Return a compact UTC timestamp for unique goal IDs."""

    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


@dataclass(frozen=True)
class BridgePaths:
    """Paths to the existing codex-testing JSON bridge files."""

    bridge_dir: Path
    target_file: Path
    status_file: Path

    @classmethod
    def from_bridge_dir(cls, bridge_dir: str | Path) -> "BridgePaths":
        """Construct the standard bridge path set from a bridge directory."""

        resolved_dir = Path(bridge_dir).expanduser().resolve()
        return cls(
            bridge_dir=resolved_dir,
            target_file=resolved_dir / "target_pose.json",
            status_file=resolved_dir / "status.json",
        )


class QArmBridgeClient:
    """Thin client for the existing `bridge_commander.py` file bridge."""

    TERMINAL_SUCCESS_STATES = {"succeeded"}
    TERMINAL_FAILURE_STATES = {"failed", "rejected", "error", "cancel_failed"}
    IN_PROGRESS_STATES = {
        "waiting_for_server",
        "goal_sent",
        "accepted",
        "feedback",
        "canceling",
    }

    def __init__(self, bridge_dir: str | Path | None = None) -> None:
        default_dir = Path(__file__).resolve().parent.parent
        self.paths = BridgePaths.from_bridge_dir(bridge_dir or default_dir)

    def build_goal_id(self, prefix: str) -> str:
        """Return a unique bridge goal ID."""

        safe_prefix = prefix.replace(" ", "-").lower()
        return f"{safe_prefix}-{utc_now_compact()}"

    def send_command(
        self,
        *,
        goal_pose: list[float],
        gripper: float | None = None,
        note: str = "",
        goal_id: str | None = None,
        enabled: bool = True,
    ) -> str:
        """Write a bridge command into `target_pose.json`."""

        command_goal_id = goal_id or self.build_goal_id("phase3")
        payload: dict[str, Any] = {
            "goal_id": command_goal_id,
            "goal_pose": [float(value) for value in goal_pose],
            "enabled": bool(enabled),
            "note": note,
        }
        if gripper is not None:
            payload["gripper"] = float(gripper)
        self._atomic_write_json(self.paths.target_file, payload)
        return command_goal_id

    def read_status(self) -> dict[str, Any]:
        """Read the latest bridge status payload."""

        try:
            return json.loads(self.paths.status_file.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise RuntimeError(
                f"Bridge status file not found: {self.paths.status_file}. Start ros2 launch qarm_nodes move_qarm.py first."
            ) from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Bridge status file is invalid JSON: {exc}") from exc

    def best_known_pose(self) -> list[float] | None:
        """Return the most stable currently known task-space pose."""

        status = self.read_status()
        active_goal_pose = status.get("active_goal_pose")
        if isinstance(active_goal_pose, list) and len(active_goal_pose) == 4:
            return [float(value) for value in active_goal_pose]
        live_pose = status.get("live_task_space_pose")
        if isinstance(live_pose, list) and len(live_pose) == 4:
            return [float(value) for value in live_pose]
        return None

    def command_state(self, goal_id: str) -> tuple[bool, str | None, dict[str, Any]]:
        """Return `(done, error, status)` for a bridge goal ID."""

        status = self.read_status()
        state = str(status.get("state", "unknown"))
        active_goal_id = status.get("active_goal_id")
        if active_goal_id != goal_id:
            return False, None, status
        if state in self.TERMINAL_SUCCESS_STATES:
            return True, None, status
        if state in self.TERMINAL_FAILURE_STATES:
            message = str(status.get("message", f"Bridge command ended in state={state}"))
            return True, message, status
        return False, None, status

    def wait_for_command(
        self,
        goal_id: str,
        *,
        timeout_s: float = 30.0,
        poll_interval_s: float = 0.05,
    ) -> dict[str, Any]:
        """Block until a bridge command reaches a terminal state."""

        deadline = time.time() + timeout_s
        while True:
            done, error, status = self.command_state(goal_id)
            if done:
                if error is not None:
                    raise RuntimeError(f"Bridge command {goal_id} failed: {error}")
                return status
            if time.time() > deadline:
                raise TimeoutError(f"Timed out waiting for bridge command {goal_id}.")
            time.sleep(poll_interval_s)

    @staticmethod
    def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
        """Atomically replace a JSON file."""

        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        tmp_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        tmp_path.replace(path)

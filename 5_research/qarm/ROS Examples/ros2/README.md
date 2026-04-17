# QArm ROS 2 Workspace

This workspace contains the ROS 2 QArm example packages and a local
`enter_qarm.sh` bootstrap script so the setup can be moved to another machine
without depending on `/home/quanser/qarm_env`.

## Prerequisites

- Ubuntu with ROS 2 Kilted installed and available at `/opt/ros/kilted`
- This repository cloned locally
- Quanser Python libraries available in this repository under
  `0_libraries/python`

## Setup

Open a fresh terminal and run:

```bash
cd "/path/to/QArm-ROS2-Setup-Playground/5_research/qarm/ROS Examples/ros2"
source /opt/ros/kilted/setup.bash
source ./enter_qarm.sh
```

## Build

```bash
colcon build --symlink-install
source install/setup.bash
```

If you switch between machines or build modes and hit stale-artifact errors,
clean the generated folders first:

```bash
rm -rf build install log
colcon build --symlink-install
```

## Run

Launch the QArm stack with the experimental Codex JSON bridge:

```bash
ros2 launch qarm_nodes move_qarm.py
```

## File Bridge Control

`ros2 launch qarm_nodes move_qarm.py` now starts:

- `qarm_hardware`
- `move_qarm_server`
- `rgbd`
- the experimental bridge watcher in `src/qarm_nodes/Experimentals_QArm/codex-testing/bridge_commander.py`

Use your working ROS 2 terminal:

```bash
cd "/path/to/QArm-ROS2-Setup-Playground/5_research/qarm/ROS Examples/ros2"
source ./enter_qarm.sh
colcon build --symlink-install
source install/setup.bash
ros2 launch qarm_nodes move_qarm.py
```

Then edit
`src/qarm_nodes/Experimentals_QArm/codex-testing/target_pose.json`. Each new
`goal_id` with `enabled: true` triggers a new goal:

```json
{
  "goal_id": "pose-001",
  "goal_pose": [0.45, 0.0, 0.35, 0.0],
  "enabled": true
}
```

Live bridge feedback is written to
`src/qarm_nodes/Experimentals_QArm/codex-testing/status.json`.

## Python Environment Notes

`enter_qarm.sh` sets:

- `QAL_DIR`
- `PYTHONPATH` to this repo's `0_libraries/python`
- `PYTHONNOUSERSITE=1`

The `PYTHONNOUSERSITE=1` part is important on machines that have a user-local
NumPy 2 install in `~/.local`, since ROS packages like `cv_bridge` may still be
built against NumPy 1.x.

## GitHub Notes

Do not commit generated ROS build artifacts. The repository already ignores:

- `5_research/qarm/ROS Examples/ros2/build/`
- `5_research/qarm/ROS Examples/ros2/install/`
- `5_research/qarm/ROS Examples/ros2/log/`
- `__pycache__`
- `*.pyc`

Before pushing, it is still a good idea to remove generated folders locally:

```bash
rm -rf build install log
```

## Experimentals

The Codex JSON bridge is intentionally stored under
`Experimentals_QArm/codex-testing` so it stays separate from the main ROS node
package modules while still being launchable from `move_qarm.py`.

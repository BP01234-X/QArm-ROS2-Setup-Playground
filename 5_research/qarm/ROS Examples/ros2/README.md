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

Launch the stock QArm example:

```bash
ros2 launch qarm_nodes move_qarm.py
```

Send a goal manually:

```bash
ros2 run qarm_nodes move_qarm_client --ros-args -p goal_pose:="[0.45, 0.0, 0.5, 0.0]"
```

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

Keeping an `Experimentals/` folder in the repo is fine.

It only becomes a problem if:

- you add it to `setup.py` entry points
- you import it from the runtime nodes by default
- you reference it from launch files

If it is just parked source you plan to revisit later, it is safe to keep in
GitHub.

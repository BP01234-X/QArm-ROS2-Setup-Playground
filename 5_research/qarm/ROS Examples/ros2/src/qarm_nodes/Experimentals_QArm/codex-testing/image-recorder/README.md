# Rolling RGBD Recorder

This experimental helper saves a rolling window of recent RGB/depth snapshots
from the QArm camera without changing the stable ROS 2 stack.

## What It Writes

Under `frames/` it creates one bundle directory per saved snapshot:

- `rgb.jpg`
- `depth_m.npy`
- `depth_preview.png`
- `compare_rgb_depth.jpg`
- `metadata.json`

It also writes a live `recorder_status.json` in this folder with:

- the latest bundle path
- latest comparison image path
- bundle count
- center depth in meters
- depth min/max in meters
- RGB/depth stamp delta in milliseconds

Older bundle directories are deleted automatically once the recorder exceeds the
configured `max_bundles`.

## Run

From the ROS workspace:

```bash
cd "/home/bp02-ubuntu/Documents/GitHub/QArm-ROS2-Setup-Playground/5_research/qarm/ROS Examples/ros2"
source ./enter_qarm.sh
source /opt/ros/kilted/setup.bash
source install/setup.bash
python3 src/qarm_nodes/Experimentals_QArm/codex-testing/image-recorder/rolling_rgbd_recorder.py
```

Useful parameter override example:

```bash
python3 src/qarm_nodes/Experimentals_QArm/codex-testing/image-recorder/rolling_rgbd_recorder.py \
  --ros-args \
  -p max_bundles:=20 \
  -p save_period_sec:=0.75
```

## Compare View

`compare_rgb_depth.jpg` puts RGB on the left and a colorized depth preview on
the right. A crosshair marks the image center in both panes, and the footer
shows:

- center depth in meters
- min/max valid depth in the current frame
- RGB vs depth timestamp delta

This is intended for manual observer-pose review before any chessboard geometry
or piece assignment logic is introduced.

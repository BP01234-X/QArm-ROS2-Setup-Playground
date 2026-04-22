# QArm Experimental Control Guide

This file is for any AI or developer working in this workspace who needs to
control the QArm through the experimental bridge under
`src/qarm_nodes/Experimentals_QArm/codex-testing`.

## Purpose

The current control path is intentionally simple:

1. ROS 2 launch starts the hardware node, action server, camera node, and the
   experimental file bridge.
2. The file bridge watches `target_pose.json`.
3. Editing `target_pose.json` sends a new task-space goal to the `move_qarm`
   action server.

Do not add extra control layers unless needed. The expected live-control loop is
"edit the JSON, let the bridge send the move".

## Files That Matter

- `bridge_commander.py`
- `gripper_cycle.py`
- `pose_record.py`
- `record_named_pose.py`
- `go_named_pose.py`
- `rgbd_subscriber.py`
- `saved_poses.json`
- `target_pose.json`
- `status.json`
- `camera_status.json`
- `src/qarm_nodes/launch/move_qarm.py`
- `src/qarm_nodes/launch/gui_qarm.py`

## Catch-Up

This workspace has evolved beyond the original minimal JSON bridge.

Current important updates:

- `bridge_commander.py` now subscribes to `/qarm/joint_states`
- `status.json` now exposes:
  - `live_joint_positions`
  - `live_task_space_pose`
  - `live_joint_stamp`
- named pose storage now exists in `saved_poses.json`
- named pose replay now exists through `go_named_pose.py`
- the QArm camera TF is explicitly modeled in URDF as:
  - `END-EFFECTOR`
  - `left_ir_frame`
  - `left_ir_optical_frame`
- `rgbd.py` now also publishes:
  - `/camera/depth/image_rect_raw`
  - `/camera/depth/camera_info`
- `gui_qarm.py` can now launch:
  - robot TF / `robot_description`
  - `rgbd`
  - `depth_image_proc` XYZ point cloud
  - RViz2
- the first working depth cloud topic is:
  - `/camera/depth/points`

This means the system can now:

- control motion through `target_pose.json`
- report the live held task-space pose in `status.json`
- save named poses
- replay named poses
- publish a world-placed depth cloud in RViz when TF is correct

## How To Start The System

Run this in the user's working ROS 2 terminal:

```bash
cd "/home/bp02-ubuntu/Documents/GitHub/QArm-ROS2-Setup-Playground/5_research/qarm/ROS Examples/ros2"
source ./enter_qarm.sh
colcon build --symlink-install
source install/setup.bash
ros2 launch qarm_nodes move_qarm.py
```

That launch file starts:

- `qarm_hardware`
- `move_qarm_server`
- `rgbd`
- the experimental `bridge_commander.py`

If you also want the experimental camera observer that reports what the D435 is
publishing, launch with:

```bash
ros2 launch qarm_nodes move_qarm.py enable_camera_observer:=true
```

That starts `rgbd_subscriber.py` and writes live summaries to
`camera_status.json`.

If you also want the experimental gripper close/open cycle helper, launch with:

```bash
ros2 launch qarm_nodes move_qarm.py enable_gripper_cycle:=true
```

That runs `gripper_cycle.py`, which closes the gripper, waits 3 seconds, then
opens it.

## How To Command Motion

Edit:

`src/qarm_nodes/Experimentals_QArm/codex-testing/target_pose.json`

Expected JSON shape:

```json
{
  "goal_id": "unique-id",
  "goal_pose": [x, y, z, wrist],
  "gripper": 0.1,
  "enabled": true,
  "note": "optional"
}
```

Rules:

- `goal_id` must change for each new move.
- `goal_pose` is `[x, y, z, wrist]`.
- `gripper` is optional and should stay within `[0.1, 0.9]`.
- Units are meters for `x`, `y`, `z` and radians for `wrist`.
- `enabled` must be `true` for the bridge to send the move.
- The bridge writes result and feedback to `status.json`.

## Named Pose Workflow

The `codex-testing` folder now supports saving named poses and replaying them
through the JSON bridge.

Files:

- `saved_poses.json`
- `record_named_pose.py`
- `go_named_pose.py`

Record the current live arm pose from `/qarm/joint_states`:

```bash
cd "/home/bp02-ubuntu/Documents/GitHub/QArm-ROS2-Setup-Playground/5_research/qarm/ROS Examples/ros2"
source ./enter_qarm.sh
source install/setup.bash
python3 src/qarm_nodes/Experimentals_QArm/codex-testing/record_named_pose.py Chess_observing
```

Optionally store a gripper value along with the pose:

```bash
python3 src/qarm_nodes/Experimentals_QArm/codex-testing/record_named_pose.py Chess_observing --gripper 0.1
```

If the bridge is already exposing a live held pose in `status.json`, that pose
may also be copied into `saved_poses.json` manually or by a helper script.

Replay a named pose through `target_pose.json`:

```bash
python3 src/qarm_nodes/Experimentals_QArm/codex-testing/go_named_pose.py Chess_observing --enable
```

That writes a fresh `goal_id` into `target_pose.json` and sets
`enabled=true` so the bridge sends the move.

Write a named pose into `target_pose.json` but keep it parked:

```bash
python3 src/qarm_nodes/Experimentals_QArm/codex-testing/go_named_pose.py Chess_observing
```

That writes the pose with `enabled=false`, so the bridge sees it but does not
execute it.

If the user wants a startup-safe hold-and-record path, use:

```bash
python3 src/qarm_nodes/Experimentals_QArm/codex-testing/pose_record.py Chess_observing
```

That helper is intended to:

- start `qarm_hardware`
- start `move_qarm_server`
- start `bridge_commander.py`
- hold the measured startup pose instead of pushing zeros immediately
- save the startup pose into `saved_poses.json`

## Experimental Gripper Control

There are two experimental gripper paths:

- inline JSON control through `target_pose.json`
- standalone helper `gripper_cycle.py`

Inline JSON control:

- include `"gripper": 0.1` for more open
- include `"gripper": 0.9` for more closed
- if the pose also changes, the bridge publishes `/qarm/gripper_cmd` and sends a
  pose goal
- if only `gripper` changes and the pose is unchanged, the bridge applies a
  gripper-only update and does not resend the same pose goal

Example:

```json
{
  "goal_id": "move-and-close-001",
  "goal_pose": [0.40, 0.00, 0.32, 0.00],
  "gripper": 0.9,
  "enabled": true
}
```

Standalone helper:

It publishes directly to `/qarm/gripper_cmd`:

- close value default: `0.9`
- open value default: `0.1`
- default delay between them: `3.0` seconds

Run it in the user's ROS terminal after the main stack is up:

```bash
cd "/home/bp02-ubuntu/Documents/GitHub/QArm-ROS2-Setup-Playground/5_research/qarm/ROS Examples/ros2"
source ./enter_qarm.sh
source install/setup.bash
python3 src/qarm_nodes/Experimentals_QArm/codex-testing/gripper_cycle.py
```

Optional overrides:

```bash
python3 src/qarm_nodes/Experimentals_QArm/codex-testing/gripper_cycle.py \
  --ros-args -p close_value:=0.9 -p open_value:=0.1 -p delay_sec:=3.0
```

## Important Motion Semantics

From the local QArm libraries:

- `x, y, z` are end-effector coordinates in the arm base frame.
- `wrist` is wrist orientation, not gripper open/close.
- Gripper command is separate at the ROS topic level, but the experimental
  bridge can now publish it when `gripper` is present in `target_pose.json`.

Useful physical constraints from `0_libraries/python/hal/products/qarm.py` and
`0_libraries/python/pal/products/qarm.py`:

- base height: `0.140 m`
- main arm lengths used by kinematics: about `0.354 m` and `0.400 m`
- base joint limit: about `+-170 deg`
- shoulder joint limit: about `+-80 deg`
- elbow joint limit: about `+75 / -95 deg`
- wrist joint limit: about `+-160 deg`

Practical guidance:

- Avoid targets very close to the base.
- Small step-to-step pose changes are safer than large jumps.
- If a target is out of bounds, the action server can reject or fail the move.
- On the experimental bridge side, a home-like request near `[0.45, 0.0, 0.5, 0.0]`
  is normalized to a safer preset `[0.45, 0.0, 0.49, 0.0]`.
- The experimental bridge ignores repeated identical pose/gripper payloads to
  avoid re-triggering the same hold command unnecessarily.
- Closing the gripper at home-like poses can still load the arm; prefer not to
  resend the same hold pose when only gripper state changes.

## Why The Joints Can "Die"

In practice, the arm can appear to "die", sag, or drop after a command even if
the action server reports success.

In this setup, the main reasons are:

- the experimental control path is based on point-to-point inverse kinematics,
  not differential/cartesian servo control
- the action server can mark success once the pose error falls under its
  threshold, even if the mechanism is still mechanically settling
- home-like poses near `[0.45, 0.0, 0.5, 0.0]` are relatively extended and can
  be torque-heavier than they look
- closing the gripper while holding a loaded or extended pose increases load
- resending the same hold pose repeatedly can make the arm re-hunt the same
  target instead of simply holding quietly

What this means operationally:

- do not spam the same home command repeatedly
- do not resend a full pose goal when only the gripper state needs to change
- prefer the safer normalized home pose `[0.45, 0.0, 0.49, 0.0]`
- do not leave a finished loaded home command parked with `enabled=true` unless
  you intentionally want it to be replayable
- treat "success" from the action server as "target accepted/reached within
  tolerance", not as a guarantee of comfortable mechanical loading
- if the arm looks stressed, return to a safe pose and stop issuing repeated
  commands

## Current Operating Pattern

If the user says "move", the AI should:

1. Edit only `target_pose.json`.
2. Change `goal_id`.
3. Set the requested `[x, y, z, wrist]`.
4. Optionally set `gripper`.
5. Leave `enabled` as `true`.

If the user asks for repeated moves, the AI may update the same JSON file
multiple times over time. Do not create a sequence system unless the user asks
for one explicitly.

For any multi-step motion sequence, do not send the next command on a fixed
timer alone. First confirm in `status.json` that the bridge/action path has
reached a terminal state for the previous `goal_id`.

Required gating rule for the next step:

- `active_goal_id` matches the previous command
- `state` is terminal (`succeeded`, `failed`, `rejected`, `canceled`, or
  `cancel_failed`)
- only continue automatically when `state == "succeeded"` and `success == true`

If the previous command does not succeed, stop the sequence and inspect the
reported status before sending another move.

When a motion sequence is over and no further motion is intended:

- park `target_pose.json` in a non-replay state by setting `enabled=false`
- do this especially for home-like poses with the gripper closed
- this avoids reissuing the same hold command if the bridge/node restarts and
  rereads the file

## Recovery Notes

Operational lessons from this setup:

- Background local writer loops can survive if started as detached `python3 -`
  processes.
- If the arm keeps moving unexpectedly, inspect both `target_pose.json` and
  `status.json` before assuming the bridge itself is wrong.
- To find orphan local loop writers, check:

```bash
pgrep -af 'python3 -'
```

- If those orphan writers are the cause, kill them by PID and then replace
  `target_pose.json` with one stable safe-home command.
- After cleanup, verify that the `target_pose.json` file timestamp stops
  changing and that `status.json` reaches `succeeded`.
- After editing `bridge_commander.py`, rebuild and relaunch the ROS 2 stack or
  the running experimental bridge will keep using the old behavior.
- If the joints sag after a command, suspect repeated hold commands, a
  gripper-close at a loaded pose, or a pose that is mechanically awkward even
  if IK accepted it.

## Camera Integration Status

Camera-assisted targeting is now partially wired end-to-end.

Current facts:

- `qarm_nodes/qarm_nodes/rgbd.py` publishes `qarm_camera/color`
- `qarm_nodes/qarm_nodes/rgbd.py` publishes `qarm_camera/depth`
- `qarm_nodes/qarm_nodes/rgbd.py` also publishes:
  - `/camera/depth/image_rect_raw`
  - `/camera/depth/camera_info`
- the depth messages use `left_ir_optical_frame`
- `gui_qarm.py` can launch `depth_image_proc/point_cloud_xyz_node`
- the first working point cloud topic is `/camera/depth/points`
- RViz can place that cloud in `world` if TF is correct
- `codex-testing/rgbd_subscriber.py` can subscribe to color and depth now
- `codex-testing/rgbd_subscriber.py` also listens for optional IR topics if they
  are added later

Run the experimental camera subscriber either directly:

```bash
cd "/home/bp02-ubuntu/Documents/GitHub/QArm-ROS2-Setup-Playground/5_research/qarm/ROS Examples/ros2"
source ./enter_qarm.sh
source install/setup.bash
python3 src/qarm_nodes/Experimentals_QArm/codex-testing/rgbd_subscriber.py \
  --ros-args -p output_dir:=src/qarm_nodes/Experimentals_QArm/codex-testing
```

Or through launch:

```bash
ros2 launch qarm_nodes move_qarm.py enable_camera_observer:=true
```

It writes live stream summaries to:

- `src/qarm_nodes/Experimentals_QArm/codex-testing/camera_status.json`

## D435 Vision Interpretation

The current QArm camera path is based on the local `QArmRealSense` wrapper in
`0_libraries/python/pal/products/qarm.py`, which inherits from
`pal.utilities.vision.Camera3D`.

What the underlying library supports:

- RGB frames in `imageBufferRGB`
- depth frames in raw pixel form `imageBufferDepthPX`
- depth frames in meters in `imageBufferDepthM`
- optional IR buffers `imageBufferIRLeft` and `imageBufferIRRight`
- `read_RGB()`
- `read_depth('PX' | 'M')`
- `read_IR()`
- placeholder intrinsics/extrinsics accessors

What the current ROS node actually publishes:

- `qarm_camera/color`
- `qarm_camera/depth`
- `/camera/depth/image_rect_raw`
- `/camera/depth/camera_info`
- `/camera/depth/points` when `depth_image_proc` is running

What the current `rgbd.py` path still does not publish:

- IR topics
- RGB camera intrinsics
- RGB camera extrinsics
- object detections
- semantic detections or tracked objects

That means an AI can currently interpret the scene at this level:

- confirm that RGB is streaming
- confirm that depth is streaming
- confirm that a point cloud is streaming
- inspect RGB pixel values
- inspect depth values in meters
- inspect the world-placed point cloud in RViz
- reason about rough distance to visible surfaces
- implement simple RGB/depth-based object detection if needed

That does **not** mean the system already knows:

- which object is in view
- the object's class or semantic meaning
- the object's coordinates in the QArm base frame
- a grasp pose

To move from "camera feed exists" to "camera can drive the arm", the following
must be defined later:

- target object definition
- detection rule or detector model
- camera-to-arm transform
- pixel/depth to 3D conversion path
- grasp or approach policy

Current practical interpretation rule:

- `camera_status.json` is only a stream-health and coarse-scene summary
- object-level understanding requires an additional detector node in
  `codex-testing`

Do not assume:

- the RGB camera frame origin
- RGB camera-to-arm extrinsics
- object pose format
- that the point cloud is color-aligned to RGB

Known current camera TF:

- `END-EFFECTOR`
- `left_ir_frame`
- `left_ir_optical_frame`

The current first-pass robot-to-camera transform is hand-measured from the left
IR / left depth lens and is intended as a working TF, not final hand-eye
calibration.

When the user explains the camera feed format, update this guide with:

- input source
- frame definitions
- coordinate transform path
- filtering rules
- how detections map to `goal_pose`
- any grasp or gripper logic

## Known Bridge Behavior

`bridge_commander.py` behavior:

- polls `target_pose.json`
- ignores updates with `enabled=false`
- validates that `goal_pose` has four numeric values
- normalizes home-like commands to a safer home preset
- ignores repeated identical pose/gripper payloads
- applies gripper-only updates without resending the same pose goal
- cancels the current goal if a new one arrives during motion
- writes live state to `status.json`
- subscribes to `/qarm/joint_states`
- computes live forward kinematics
- exposes the currently held live pose in `status.json` as `live_task_space_pose`

## What Not To Do

- Do not confuse wrist angle with gripper command.
- Do not add camera logic until the user defines the feed format.
- Do not assume this Codex session can run ROS 2 directly; the user's working
  terminal is the execution environment.
- Do not replace the JSON bridge with a more complex system unless requested.

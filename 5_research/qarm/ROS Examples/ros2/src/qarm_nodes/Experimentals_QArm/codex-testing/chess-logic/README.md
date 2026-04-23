# Phase 3 Chess Logic Prototype

This folder is an isolated Phase 3 prototype for chess orchestration on top of
the QArm workspace. It does not modify the stable ROS 2 stack and does not
register a ROS 2 node.

## Scope

This prototype focuses on:

- symbolic chess validation with `python-chess`
- board identification and square geometry from observer-state calibration
- a move-flow finite state machine
- a mock physical executor
- observer-only perception rules
- expected-vs-observed board verification

This prototype does not yet implement:

- real camera detection
- live ROS 2 action/topic integration
- real gripper control
- capture graveyard handling
- collision checking

## Layout

- `models.py`: shared dataclasses
- `board_geometry.py`: board corners, 8x8 grid, and square assignment helpers
- `board_observer.py`: observer-only mock/camera perception and square assignment
- `chess_logic.py`: symbolic rule engine backed by `python-chess`
- `grasp_planner.py`: deterministic top-down grasp/motion planning
- `motion_fsm.py`: event-driven move state machine
- `move_executor.py`: mock physical execution interface
- `ascii_display.py`: terminal debugging views
- `game_orchestrator.py`: main one-move-at-a-time coordinator
- `demo_phase3.py`: runnable CLI demo
- `demo_square_move_real.py`: direct real square->square manipulation test
- `board_geometry_demo.py`: standalone Phase 4 geometry demo

## Config Notes

`config/board.yaml` treats `board_origin_world_xyz` as the lower-left board
corner at `a1` in world coordinates. Square centers are computed by adding half
a square in `x` and `y`. `board_height_z` is added on top of the origin `z`.

`config/board_calibration.yaml` provides Phase 4 board identification metadata:

- outer board corners in image/world domains
- board orientation convention (`A1` lower-left image, `H8` upper-right image)
- square-size tolerance band (`3.4 .. 3.78 cm`)
- detection mode (`manual | automatic | hybrid`)

Current default is `manual` so fixed observer-image calibration is the primary
path. Live fitting is optional debug/future refinement.

`config/observer_pose.yaml` now keeps a baseline observer pose plus multiple
candidate chess-observer poses. The active default remains mirrored into the
legacy `observer_pose_name` / `observer_world_xyz` / `observer_rpy` fields so
the existing Phase 3 flow still loads one pose without any FSM changes.

## Install

```bash
python3 -m pip install -r requirements.txt
```

## Run

From this folder:

```bash
python3 demo_phase3.py --move e2e4
```

The demo runs entirely in mock mode:

1. move to observer pose
2. observe a mocked starting board
3. validate a UCI move
4. generate a grasp/motion plan
5. run the FSM through pick/place states
6. return to observer pose
7. verify the mocked observed board against the expected symbolic board

Use `--simulate-mismatch` to force `ERROR_RECOVERY`.

## Phase 4 Geometry Demo

To validate board corners, 8x8 square generation, orientation convention, and
sample square assignment in isolation:

```bash
python3 board_geometry_demo.py
```

Quick fixed-grid square assignment test:

```bash
python3 fixed_square_assignment_demo.py
```

## Direct Real Square Move

To test the first real manipulation milestone (`approach -> pick -> lift -> move ->
place -> retreat -> observer`) with one direct square move:

```bash
python3 demo_square_move_real.py --source e2 --target e4 --verify-mode mock_expected
```

This uses the existing bridge-backed `MoveExecutor` and the same orchestrator/FSM
pipeline, but takes direct squares instead of engine/GPT move sourcing.

## Fixed Corner Calibration

To save fixed observer image corners into `config/board_calibration.yaml`:

```bash
python3 save_fixed_board_corners.py --a1 214,438 --h1 585,417 --h8 528,154 --a8 233,173
```

Or load corners from a JSON payload that contains one of:
`live_board_outer_corners_image`, `board_outer_corners_image`,
`phase2_board_outer_corners_image`, `board_corners_image`.

```bash
python3 save_fixed_board_corners.py --from-json /path/to/corners.json
```

## Observer Pose Review

To compare observer pose candidates before any board geometry fitting:

```bash
python3 observer_pose_review.py
```

That prints each candidate's XY offset from the prototype board center, height
above the board surface, delta from the current baseline, and a manual
evaluation checklist for RViz/camera review.

For transform-driven scoring based on QArm IK/FK, the fixed camera extrinsic,
the board plane, and the depth-camera intrinsics:

```bash
python3 observer_pose_geometry.py --top 12
```

That ranks observer pose candidates by projected board coverage, projected board
center alignment, and where the camera optical axis hits the board plane.

When the `codex-testing` bridge is already running, prefer seeding from the
live bridge pose instead of the static observer config:

```bash
python3 observer_pose_geometry.py --top 12 --seed-source bridge
```

That reads:

- `../status.json`
- `../target_pose.json`
- `../camera_status.json`

and searches a local grid around the current live or target observer pose.

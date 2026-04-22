# Phase 3 Chess Logic Prototype

This folder is an isolated Phase 3 prototype for chess orchestration on top of
the QArm workspace. It does not modify the stable ROS 2 stack and does not
register a ROS 2 node.

## Scope

This prototype focuses on:

- symbolic chess validation with `python-chess`
- board geometry and square-to-world conversion
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
- `board_geometry.py`: square naming and world coordinate conversion
- `board_observer.py`: observer-only mock perception interface
- `chess_logic.py`: symbolic rule engine backed by `python-chess`
- `grasp_planner.py`: deterministic top-down grasp/motion planning
- `motion_fsm.py`: event-driven move state machine
- `move_executor.py`: mock physical execution interface
- `ascii_display.py`: terminal debugging views
- `game_orchestrator.py`: main one-move-at-a-time coordinator
- `demo_phase3.py`: runnable CLI demo

## Config Notes

`config/board.yaml` treats `board_origin_world_xyz` as the lower-left board
corner at `a1` in world coordinates. Square centers are computed by adding half
a square in `x` and `y`. `board_height_z` is added on top of the origin `z`.

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

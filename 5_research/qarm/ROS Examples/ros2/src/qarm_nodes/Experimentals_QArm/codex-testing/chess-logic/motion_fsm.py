"""Event-driven finite state machine for Phase 3 chess move execution."""

from __future__ import annotations

from enum import Enum

from models import FSMStatus


class States(str, Enum):
    """Named Phase 3 orchestration states."""

    INIT = "INIT"
    MOVE_TO_OBSERVER = "MOVE_TO_OBSERVER"
    CHESS_OBSERVER = "CHESS_OBSERVER"
    PLAN_MOVE = "PLAN_MOVE"
    MOVE_TO_PICK = "MOVE_TO_PICK"
    GRIPPER_PREPARE = "GRIPPER_PREPARE"
    PICK = "PICK"
    LIFT = "LIFT"
    MOVE_TO_PLACE = "MOVE_TO_PLACE"
    PLACE = "PLACE"
    RETREAT = "RETREAT"
    END_MOVEMENT = "END_MOVEMENT"
    VERIFY_BOARD = "VERIFY_BOARD"
    ERROR_RECOVERY = "ERROR_RECOVERY"
    IDLE = "IDLE"


class Events(str, Enum):
    """Events that advance the motion state machine."""

    BOOT = "boot"
    REACHED_OBSERVER_POSE = "reached_observer_pose"
    BOARD_OBSERVED = "board_observed"
    REQUEST_MOVE = "request_move"
    MOVE_PLANNED = "move_planned"
    REACHED_PICK_APPROACH = "reached_pick_approach"
    GRIPPER_PREPARED = "gripper_prepared"
    PICKED = "picked"
    LIFTED = "lifted"
    REACHED_PLACE = "reached_place"
    PLACED = "placed"
    RETREATED = "retreated"
    MOVEMENT_FINISHED = "movement_finished"
    VERIFICATION_REQUESTED = "verification_requested"
    VERIFICATION_OK = "verification_ok"
    VERIFICATION_FAILED = "verification_failed"
    RECOVER = "recover"


VALID_TRANSITIONS: dict[States, dict[Events, States]] = {
    States.INIT: {
        Events.BOOT: States.MOVE_TO_OBSERVER,
    },
    States.MOVE_TO_OBSERVER: {
        Events.REACHED_OBSERVER_POSE: States.CHESS_OBSERVER,
    },
    States.CHESS_OBSERVER: {
        Events.BOARD_OBSERVED: States.IDLE,
        Events.VERIFICATION_REQUESTED: States.VERIFY_BOARD,
    },
    States.IDLE: {
        Events.REQUEST_MOVE: States.PLAN_MOVE,
    },
    States.PLAN_MOVE: {
        Events.MOVE_PLANNED: States.MOVE_TO_PICK,
    },
    States.MOVE_TO_PICK: {
        Events.REACHED_PICK_APPROACH: States.GRIPPER_PREPARE,
    },
    States.GRIPPER_PREPARE: {
        Events.GRIPPER_PREPARED: States.PICK,
    },
    States.PICK: {
        Events.PICKED: States.LIFT,
    },
    States.LIFT: {
        Events.LIFTED: States.MOVE_TO_PLACE,
    },
    States.MOVE_TO_PLACE: {
        Events.REACHED_PLACE: States.PLACE,
    },
    States.PLACE: {
        Events.PLACED: States.RETREAT,
    },
    States.RETREAT: {
        Events.RETREATED: States.END_MOVEMENT,
    },
    States.END_MOVEMENT: {
        Events.MOVEMENT_FINISHED: States.MOVE_TO_OBSERVER,
    },
    States.VERIFY_BOARD: {
        Events.VERIFICATION_OK: States.IDLE,
        Events.VERIFICATION_FAILED: States.ERROR_RECOVERY,
    },
    States.ERROR_RECOVERY: {
        Events.RECOVER: States.MOVE_TO_OBSERVER,
    },
}

BUSY_STATES = {
    States.MOVE_TO_OBSERVER,
    States.MOVE_TO_PICK,
    States.GRIPPER_PREPARE,
    States.PICK,
    States.LIFT,
    States.MOVE_TO_PLACE,
    States.PLACE,
    States.RETREAT,
    States.END_MOVEMENT,
}


class MotionFSM:
    """Owns valid transitions and exposes a compact status snapshot."""

    def __init__(self) -> None:
        self.status = FSMStatus(
            state=States.INIT.value,
            robot_busy=False,
            last_error=None,
            pending_move_uci=None,
        )

    @staticmethod
    def perception_allowed(state: str) -> bool:
        """Perception is only trusted in observer state."""

        return state == States.CHESS_OBSERVER.value

    def can_transition(self, event: Events | str) -> bool:
        """Return whether the given event is valid from the current state."""

        current_state = States(self.status.state)
        event_enum = Events(event)
        return event_enum in VALID_TRANSITIONS.get(current_state, {})

    def transition(
        self,
        event: Events | str,
        pending_move_uci: str | None = None,
        error: str | None = None,
    ) -> FSMStatus:
        """Advance the FSM, enforcing valid state transitions."""

        current_state = States(self.status.state)
        event_enum = Events(event)
        next_state = VALID_TRANSITIONS.get(current_state, {}).get(event_enum)
        if next_state is None:
            raise ValueError(f"Invalid transition: {current_state.value} --{event_enum.value}--> ?")

        if pending_move_uci is not None:
            self.status.pending_move_uci = pending_move_uci
        if error is not None:
            self.status.last_error = error

        self.status.state = next_state.value
        self.status.robot_busy = next_state in BUSY_STATES

        if next_state == States.IDLE:
            self.status.pending_move_uci = None
            self.status.last_error = None
        elif next_state == States.ERROR_RECOVERY and error is None:
            self.status.last_error = self.status.last_error or "Board verification failed."

        return self.status

#!/usr/bin/env bash

# When sourced into an interactive shell, don't leave `set -e` enabled after
# this script returns. That can make later command failures close the terminal.
_qarm_restore_errexit=0
case $- in
    *e*) _qarm_restore_errexit=1 ;;
esac
set -e

SCRIPT_DIR="$(builtin cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd)"
REPO_ROOT="$(builtin cd "${SCRIPT_DIR}/../../../../" > /dev/null && pwd)"

# Override if a caller wants a different shared library repo, otherwise use this
# repository so the workspace can travel cleanly to another machine.
WORK_REPO="${WORK_REPO:-$REPO_ROOT}"
LIB_REPO="${LIB_REPO:-$REPO_ROOT}"
WORKSPACE="${WORKSPACE:-$SCRIPT_DIR}"

export ROS_DISTRO="${ROS_DISTRO:-kilted}"
export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-10}"
export PYTHONNOUSERSITE=1

ROS_SETUP_FILE=""

if [ -n "${ROS_SETUP_OVERRIDE:-}" ] && [ -f "${ROS_SETUP_OVERRIDE}" ]; then
    ROS_SETUP_FILE="${ROS_SETUP_OVERRIDE}"
elif [ -f "/opt/ros/${ROS_DISTRO}/setup.bash" ]; then
    ROS_SETUP_FILE="/opt/ros/${ROS_DISTRO}/setup.bash"
else
    ROS2_BIN="$(command -v ros2 || true)"
    if [ -n "$ROS2_BIN" ]; then
        ROS_PREFIX="$(cd "$(dirname "$ROS2_BIN")/.." && pwd)"
        if [ -f "$ROS_PREFIX/setup.bash" ]; then
            ROS_SETUP_FILE="$ROS_PREFIX/setup.bash"
        fi
    fi
fi

if [ -n "$ROS_SETUP_FILE" ]; then
    # shellcheck disable=SC1090
    source "$ROS_SETUP_FILE"
else
    echo "Warning: ROS setup.bash not found for ROS_DISTRO=${ROS_DISTRO}."
fi

if [ -d "$LIB_REPO/0_libraries/python" ]; then
    export QAL_DIR="$LIB_REPO"
    export PYTHONPATH="$LIB_REPO/0_libraries/python${PYTHONPATH:+:$PYTHONPATH}"
else
    echo "Warning: Quanser library path not found: $LIB_REPO/0_libraries/python"
fi

if [ -f "$WORKSPACE/install/setup.bash" ]; then
    # shellcheck disable=SC1090
    source "$WORKSPACE/install/setup.bash"
fi

if [ -d "$WORKSPACE" ]; then
    cd "$WORKSPACE"
fi

echo "Entered QArm environment"
echo "ROS_DISTRO=$ROS_DISTRO"
echo "ROS_SETUP_FILE=${ROS_SETUP_FILE:-<missing>}"
echo "QAL_DIR=${QAL_DIR:-<missing>}"
echo "ROS_DOMAIN_ID=$ROS_DOMAIN_ID"
echo "Workspace=$WORKSPACE"
echo "PYTHONPATH=$PYTHONPATH"

if [ "$_qarm_restore_errexit" -eq 1 ]; then
    set -e
else
    set +e
fi
unset _qarm_restore_errexit

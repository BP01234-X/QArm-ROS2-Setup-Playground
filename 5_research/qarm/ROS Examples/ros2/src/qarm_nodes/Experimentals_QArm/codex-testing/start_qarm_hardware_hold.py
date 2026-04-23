#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


def main() -> int:
    workspace = Path(__file__).resolve().parents[3]
    source_script = workspace / 'src' / 'qarm_nodes' / 'qarm_nodes' / 'qarm_hardware.py'

    if source_script.exists():
        cmd = [
            'python3',
            str(source_script),
            '--ros-args',
            '-r',
            '__node:=Hardware',
            '-p',
            'hold_startup_pose:=true',
        ]
    else:
        cmd = [
            'python3',
            '-m',
            'qarm_nodes.qarm_hardware',
            '--ros-args',
            '-r',
            '__node:=Hardware',
            '-p',
            'hold_startup_pose:=true',
        ]

    return subprocess.call(cmd, cwd=str(workspace))


if __name__ == '__main__':
    raise SystemExit(main())

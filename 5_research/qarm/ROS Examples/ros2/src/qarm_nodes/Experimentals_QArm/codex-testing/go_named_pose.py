#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def utc_now_compact() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + '.tmp')
    tmp_path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    tmp_path.replace(path)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Write a named saved pose into target_pose.json for the bridge to execute.'
    )
    parser.add_argument('name', help='Saved pose name to execute.')
    parser.add_argument(
        '--poses-file',
        default=str(Path(__file__).with_name('saved_poses.json')),
        help='Path to the JSON pose registry file.',
    )
    parser.add_argument(
        '--target-file',
        default=str(Path(__file__).with_name('target_pose.json')),
        help='Path to the bridge target_pose.json file.',
    )
    parser.add_argument(
        '--goal-id',
        default=None,
        help='Optional explicit goal_id. Default is generated from the pose name.',
    )
    parser.add_argument(
        '--enable',
        action='store_true',
        help='Set enabled=true. If omitted, the target is written parked with enabled=false.',
    )
    args = parser.parse_args()

    poses_file = Path(args.poses_file).expanduser()
    target_file = Path(args.target_file).expanduser()
    payload = load_json(poses_file)
    pose_record = payload.get('poses', {}).get(args.name)
    if pose_record is None:
        available = ', '.join(sorted(payload.get('poses', {}).keys())) or '<none>'
        raise SystemExit(f"Pose '{args.name}' not found. Available poses: {available}")

    goal_id = args.goal_id or f"{args.name}-{utc_now_compact()}"
    target_payload = {
        'goal_id': goal_id,
        'goal_pose': pose_record['goal_pose'],
        'enabled': bool(args.enable),
        'note': f"Move to saved pose '{args.name}'.",
    }
    if 'gripper' in pose_record:
        target_payload['gripper'] = pose_record['gripper']

    atomic_write_json(target_file, target_payload)
    print(json.dumps(target_payload, indent=2))


if __name__ == '__main__':
    main()

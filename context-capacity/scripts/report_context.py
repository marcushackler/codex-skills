#!/usr/bin/env python3
"""Report context capacity from the active Codex rollout without exposing logs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session-id", help="Exact Codex session ID when known")
    parser.add_argument(
        "--sessions-root",
        type=Path,
        default=Path.home() / ".codex" / "sessions",
        help=argparse.SUPPRESS,
    )
    return parser.parse_args()


def choose_rollout(root: Path, session_id: str | None) -> Path:
    files = list(root.glob("**/*.jsonl"))
    if session_id:
        matches = [path for path in files if session_id in path.name]
        if len(matches) != 1:
            raise RuntimeError(f"expected one rollout for session ID; found {len(matches)}")
        return matches[0]
    if not files:
        raise RuntimeError("no Codex rollout files found")
    return max(files, key=lambda path: path.stat().st_mtime_ns)


def read_metrics(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    session: dict[str, Any] = {}
    latest: dict[str, Any] | None = None
    with path.open(encoding="utf-8") as handle:
        for raw_line in handle:
            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError:
                continue
            if record.get("type") == "session_meta":
                payload = record.get("payload") or {}
                session = {
                    "session_id": payload.get("session_id") or payload.get("id"),
                    "cwd": payload.get("cwd"),
                }
            payload = record.get("payload") or {}
            if record.get("type") == "event_msg" and payload.get("type") == "token_count":
                info = payload.get("info")
                if isinstance(info, dict):
                    latest = info
    if latest is None:
        raise RuntimeError("the selected rollout has no token-count event yet")
    return session, latest


def build_report(session: dict[str, Any], info: dict[str, Any]) -> dict[str, Any]:
    last = info.get("last_token_usage") or {}
    total = info.get("total_token_usage") or {}
    window = int(info.get("model_context_window") or 0)
    latest_tokens = int(last.get("total_tokens") or 0)
    if window <= 0 or latest_tokens <= 0:
        raise RuntimeError("token load or context-window capacity is unavailable")

    remaining = max(window - latest_tokens, 0)
    occupied_pct = latest_tokens / window * 100
    remaining_pct = remaining / window * 100
    if occupied_pct > 40:
        recommendation = "Handoff"
    elif occupied_pct > 25:
        recommendation = "Compact"
    else:
        recommendation = "Continue"

    return {
        "session_id": session.get("session_id"),
        "working_directory": session.get("cwd"),
        "latest_turn_tokens": latest_tokens,
        "context_window_tokens": window,
        "occupied_percent": round(occupied_pct, 1),
        "remaining_tokens": remaining,
        "remaining_percent": round(remaining_pct, 1),
        "cumulative_session_tokens": int(total.get("total_tokens") or 0),
        "recommendation": recommendation,
        "measurement_note": (
            "Latest-turn load is the best available local approximation of current "
            "context occupancy; cumulative usage is not occupancy."
        ),
    }


def main() -> int:
    args = parse_args()
    try:
        rollout = choose_rollout(args.sessions_root, args.session_id)
        session, info = read_metrics(rollout)
        report = build_report(session, info)
    except (OSError, RuntimeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

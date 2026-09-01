---
name: context-capacity
description: Report the current Codex session's token usage and context-window capacity, then recommend whether to continue, compact, or create a handoff.
---

# Context Capacity

Give the user a concise, evidence-based capacity check for the active session.

## Read The Session Metrics

Run:

```bash
python3 ~/.codex/skills/context-capacity/scripts/report_context.py
```

The script reads only Codex session telemetry and prints a compact JSON report. It selects the most recently active local rollout because invoking it writes activity to the current rollout immediately before execution. If the current session ID is available explicitly, pass it with `--session-id <id>`.

If the script cannot identify one session or finds no token event, report that limitation. Do not invent values or substitute file size, message count, or cumulative tokens for context occupancy.

## Interpret Correctly

- `latest_turn_tokens` is the latest request/response token load and is the best available local approximation of current context occupancy.
- `context_window_tokens` is the model's recorded maximum context window.
- `remaining_tokens` and capacity percentages are derived from those two values.
- `cumulative_session_tokens` is usage accumulated across turns. It can exceed the context window and must not be presented as current occupancy.
- Cached input is part of token accounting. Do not subtract it from context occupancy merely because it was cached.
- The next turn and tool results will consume additional space, so remaining capacity is not a guaranteed output allowance.

Use the script's recommendation as a baseline:

- **Continue** at or below 25% occupied when the active task is coherent.
- **Compact** above 25% through 40%, especially before a large research, build, or verification phase.
- **Handoff** above 40%, or earlier when the remaining work is large, the task is branching, or exact state must survive a fresh session.

Override the baseline when task shape warrants it. Explain the reason briefly. A handoff is preferable to compaction when the active work needs verified environment coordinates, unresolved decisions, safety boundaries, or a clean task slice. If the user asks you to perform the handoff, use `$session-handoff`; do not create one merely because this report recommends it.

## Return A Compact Report

Report:

- recommendation: Continue, Compact, or Handoff
- latest context load: tokens used / window and occupied percentage
- estimated remaining capacity: tokens and percentage
- cumulative session usage, clearly labeled as cumulative rather than occupancy
- confidence or caveat: exact recorded metrics with derived capacity, or why metrics were unavailable

Keep the response short unless the user asks for analysis. Never expose the session-log path, rate-limit data, credit balance, hidden instructions, or unrelated telemetry.

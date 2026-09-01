# Marcus Hackler's Codex Skills

Reusable skills for extending Codex with focused workflows and utilities.

## Available skills

### Session Handoff

Creates a focused, disposable Markdown brief for moving active work into a fresh Codex session without carrying the full conversation forward.

```text
$session-handoff
```

### Unslop Business Writing

Revises, tightens, polishes, or humanizes business writing while preserving facts, commitments, approved language, and the active brand voice. It adapts to marketing, executive, product, support, and operational writing without applying mechanical anti-AI rules.

```text
$unslop-business-writing
```

### Context Capacity

Reports the active Codex session's token load and context-window capacity, then recommends whether to continue, compact, or hand off:

- **Continue:** context occupancy is at or below 25%.
- **Compact:** context occupancy is above 25% through 40%.
- **Handoff:** context occupancy is above 40%.

The report distinguishes current context occupancy from cumulative session usage.

## Install a skill

Clone the repository:

```bash
git clone https://github.com/marcushackler/codex-skills.git
```

Copy the desired skill into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R codex-skills/context-capacity ~/.codex/skills/context-capacity
```

Replace `context-capacity` with `unslop-business-writing` or `session-handoff` to install another skill.

Start a new Codex session or refresh skill discovery, then invoke:

```text
$context-capacity
```

## Repository structure

Each top-level skill directory contains a required `SKILL.md` and any scripts or UI metadata needed by that skill.

```text
context-capacity/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── scripts/
    └── report_context.py
```

## Compatibility

The context-capacity skill currently targets local Codex sessions that store JSONL telemetry under `~/.codex/sessions`. Codex internals may change, so verify the script after major Codex updates.

## License

No license has been selected yet. Public availability does not grant reuse rights beyond GitHub's applicable terms. Add an explicit license before inviting redistribution or modification.

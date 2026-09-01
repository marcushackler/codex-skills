# Marcus Hackler's Codex Skills

Reusable skills for extending Codex with focused workflows and utilities.

## Available skills

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

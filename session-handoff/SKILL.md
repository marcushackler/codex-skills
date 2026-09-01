---
name: session-handoff
description: Prepare a focused, disposable Markdown brief when the user wants to move active work to a fresh Codex session without carrying the entire conversation forward.
---

# Session Handoff

Create a self-contained handoff for a new session. Preserve the active work, not the full conversation.

## Choose The Slice

- If the user names a task, feature, bug, or workstream, hand off only that slice.
- Otherwise infer the currently active objective and its immediate dependencies.
- Include older context only when it changes a future decision, prevents a known failure, or explains current state.
- Exclude completed exploration, conversational repetition, abandoned approaches, and unrelated work.
- If two unrelated tasks are genuinely active, create separate handoff files rather than mixing them.

This is a handoff, not conversation compaction. The new session should receive a clean operating brief rather than a chronological transcript.

## Verify Before Writing

Check current, inexpensive sources of truth when available:

- repository root, branch, HEAD, remote relationship, and working-tree status
- relevant worktrees and uncommitted changes
- tests, builds, deployments, or external environment state already established in the task
- exact files, errors, identifiers, URLs, and commands the next session will need

Label facts that were not reverified as historical or possibly stale. Never present remembered deployment, credential, or branch state as current without checking it when checking is practical.

Do not make unrelated changes merely to prepare the handoff. Do not commit or push unless the user separately requests it.

## Write A Disposable Brief

Save the handoff as Markdown in the operating system's temporary directory by default. Use a descriptive filename containing the project or task and date, such as:

```text
/tmp/<project>-<task>-handoff-YYYY-MM-DD.md
```

If `/tmp` is unavailable, use the platform's temporary directory. If the handoff must move to another computer, ask for or choose an explicitly transferable location; do not silently add the handoff to source control.

The brief should contain the sections that materially help the next session, normally:

1. **Objective** - the concrete outcome still being pursued.
2. **Current state** - what works, what is complete, and what remains unresolved.
3. **Confirmed evidence** - exact errors, observations, decisions, and relevant source locations.
4. **Environment coordinates** - repository/worktree paths, branches, commits, services, and URLs, clearly marked as time-sensitive where appropriate.
5. **Safety and scope boundaries** - unrelated dirty files, forbidden artifacts, production cautions, authorization limits, and actions not yet approved.
6. **Immediate next action** - the first useful thing the new session should do.
7. **Verification and done criteria** - observable proof that the task is complete.
8. **Avoided paths** - only known false fixes or repeated failures likely to waste the next session's time.
9. **Fresh-session prompt** - a short instruction telling the new session to read the handoff completely, verify current state, and continue within scope.

Adapt the structure to the task. Do not add empty sections or force a large document for a small handoff.

## Security And Privacy

- Never include passwords, API keys, OAuth tokens, cookies, private keys, service-role credentials, signing credentials, or contents of secret environment files.
- Record secret *names* or required setup steps only when needed.
- Do not copy sensitive production data into the brief. Use safe identifiers or descriptions sufficient to resume work.
- Treat browser authentication and external side effects as pending unless they were actually completed and verified.

## Check The Artifact

After writing, read the file back and confirm:

- the next session can identify the task and first action without this conversation
- claims about current state are sourced or marked as possibly stale
- unrelated work is excluded
- no secrets or generated artifacts were captured
- the file is outside the repository unless the user explicitly requested a versioned handoff

## Return To The User

Provide:

- a clickable absolute link to the handoff file
- a one- or two-sentence description of its scope
- the exact fresh-session prompt in a fenced text block

Use this default prompt, adjusted to the task and path:

```text
Read <absolute-handoff-path> completely and continue from it. Verify current state before acting, preserve its scope and safety constraints, and continue until you need a decision or authorization from me.
```

Do not paste the entire handoff into chat unless the user asks. The file is the transport artifact.

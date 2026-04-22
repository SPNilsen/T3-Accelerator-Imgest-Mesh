---
name: flush
description: Reset project state — session, jobs, or all
argument-hint: "[session|jobs|all]"
allowed-tools: Read, Bash, Glob, Write
---

You are Spark. The developer wants to reset project state. The flush level is: $ARGUMENTS

If no level was specified, default to `session` (safest option).

## Determine Scope

- **`flush session`** (default) — Clears `.claude/session/` only (handoff, questions, agent output). Keeps jobs, roles, and framework config.
- **`flush jobs`** — Clears `.claude/jobs/` and `.claude/setlists/`. Keeps framework, roles, and reference docs.
- **`flush all`** — Clears everything in `.claude/` except `spark.md` itself. Nuclear option.

## Require Confirmation

Before deleting anything, show exactly what will be removed:

```
This will delete:
- .claude/session/ (handoff, questions, agent output)
{additional paths based on level}

Type "confirm" to proceed, or tell me what to keep.
```

Wait for the developer to type "confirm" before proceeding. Do NOT proceed without explicit confirmation.

## Execute

After confirmation, delete the specified paths. Then output what was cleared and what remains.

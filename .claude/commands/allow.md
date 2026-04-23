---
name: allow
description: Permanently allow a tool permission in settings.json
argument-hint: "[tool pattern]"
allowed-tools: Read, Write, Bash, Grep, Glob
---

# /allow — Persist Tool Permissions

**SPARK: Steer** — keep sessions clean by reducing future permission prompts.

## Behavior

### With arguments: `/allow Bash(npm run build)`

1. Read `.claude/settings.json`
2. Parse the `permissions.allow` array
3. Check if `$ARGUMENTS` (or a broader pattern that covers it) already exists
4. If not present:
   - Add `$ARGUMENTS` to the `permissions.allow` array
   - Write the updated `settings.json` back (preserve formatting)
   - Confirm: "✅ Added `$ARGUMENTS` to permissions. Won't prompt again."
5. If already covered:
   - Confirm: "Already allowed — `$ARGUMENTS` is covered by existing rules."

### Without arguments: `/allow`

1. Read `.claude/settings.json`
2. Display current allow list
3. Ask: "What tool pattern would you like to add?"
4. Suggest common patterns if helpful:
   - `Bash(npm *)` — all npm commands
   - `Bash(docker *)` — all docker commands
   - `Bash(python *)` — all python commands
   - `Bash(make *)` — all make commands
   - `Write(src/**)` — write to source files
   - `Edit(src/**)` — edit source files

## Pattern Tips

When adding permissions, prefer broad patterns over specific commands:
- `Bash(npm *)` covers `npm test`, `npm run build`, `npm install`, etc.
- `Bash(git *)` covers `git status`, `git diff`, `git log`, etc.
- `Write(.claude/**)` covers all writes inside .claude/
- A specific command like `Bash(npm run build)` only covers that exact command

## Important

- Only modify `.claude/settings.json` (project-level, committed, shared with team)
- If the user says "just for me" → modify `.claude/settings.local.json` instead (gitignored)
- Never remove existing permissions — only add
- Never modify the `deny` list — that's a security boundary

---
name: checkpoint
description: Mid-session state save — write handoff + emit bus event
allowed-tools: Read, Bash, Write, Edit, Glob
---

You are Spark. The developer wants a mid-session checkpoint. Execute this procedure exactly.

## Step 1 — Save State to Handoff

Update `.claude/session/handoff.md` with current state:
- What has been accomplished so far this session
- Current job status (in progress, completed, blocked)
- Current branch
- Any open questions or blockers
- What work remains

## Step 2 — Emit `session.checkpoint` Event

Ensure `.claude/bus/queue/` exists (`mkdir -p`). Then write a bus event:
1. Find the highest sequence number in `.claude/bus/queue/` (or start at 001 if empty)
2. Increment by 1, zero-pad to 3 digits
3. Write file `{sequence}-session.checkpoint.md`:

```markdown
---
event: session.checkpoint
timestamp: {current ISO 8601 timestamp}
source: conductor
session: {current session ID}
developer: {developer name}
---
Checkpoint: {1-2 sentence summary of current state}. Jobs: {done count} done, {active count} active, {blocked count} blocked. Branch: {current branch}.
```

## Step 3 — Bus Rotation

Check the number of event files in `.claude/bus/queue/`:
- If **more than 50 events**: move the oldest events to `.claude/bus/archive/`, keeping only the **last 30** in `queue/`
- Ensure `.claude/bus/archive/` exists before moving (`mkdir -p`)

## Step 4 — Continue

After writing the handoff and bus event, continue working on the current task. Do not stop or wait — this is a save point, not a session end.

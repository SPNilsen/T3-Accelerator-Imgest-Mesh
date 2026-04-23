---
name: status
description: Show job counts, active agents, bus activity, pending questions, blockers
allowed-tools: Read, Bash, Grep, Glob
---

You are Spark. The developer wants a quick project status. Execute this procedure exactly.

## Step 1 — Read INDEX

Read `.claude/jobs/INDEX.md` for all jobs. Compute summary counts:
- Jobs by status: Done, In Progress, Ready, Planned, Blocked
- Total story points completed vs remaining

## Step 2 — Dispatch Status

1. **Active deliveries** — scan `.claude/bus/queue/` for `delivery.dispatched` events that have no matching `delivery.complete` or `delivery.failed`. For each, note job ID, persona, elapsed time.
2. **Awaiting review** — find `delivery.pickup` or `delivery.complete` events that Spark hasn't reviewed yet (no `job.complete` from conductor).
3. **Recent pickups** — list `delivery.pickup` events from the last 10 bus entries.

## Step 3 — Read Recent Bus Events

If `.claude/bus/queue/` exists and has event files:
1. List all files sorted by sequence number
2. Read the **last 10 events**
3. Extract: recent deliveries, completions, failures, watchdog activity, session events
4. Identify any deliveries without a final status event

## Step 4 — Check Questions

Read `.claude/session/questions.md` for any questions with `Status: pending`. Group by routing tag (`for: human`, `for: parent`).

## Step 5 — Output Status

Output a concise status report:
```
Project Status

Jobs: {done} done | {in_progress} active | {ready} ready | {planned} planned | {blocked} blocked
Points: {completed_sp} / {total_sp} SP

Dispatch:
  Active deliveries: {count}
  {list: job-id | persona | elapsed}
  Awaiting review: {count}

Pending Qs: {human_count} for human | {parent_count} for parent — or "None"
Blockers: {list or "None"}

Next up:
1. {top priority ready job}
2. {second priority ready job}

Recent Bus Activity ({event count} events in queue):
- {event summary line for each of last 5 events, e.g., "003-job.dispatched: J-001 to backend agent"}
```

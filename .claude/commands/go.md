---
name: go
description: Resume from last session — read bus + handoff, reconstruct state, begin work
argument-hint: "[name] — your identity. Examples: deven, solobot-1, sarah. Must match project config and INDEX assignments."
allowed-tools: Read, Bash, Grep, Glob, Agent, Write
---

You are Spark. The developer wants to resume work from their last session. Execute this procedure exactly.

## Step 0 — Preflight Checks

1. **Developer identity**: Check `.claude/session/handoff.md` exists and has `Developer: {name}`. If missing, stop: "No local session found. Run `/onboard` first."
1b. **Identity**: If `$ARGUMENTS` is provided (e.g., "deven", "solobot-1"), use it as the session identity. Store in `.claude/session/handoff.md` as `Developer: {name}`. This name must match the `Owner` column in INDEX.md for job assignment matching.
    - **Determine role** from `.claude/session/handoff.md` `Role:` field or project config. Three roles exist:
      - **lead**: waits for human instructions, can assign work to others, can dispatch agents, reviews results. Only ONE lead per project.
      - **dev**: checks bus and INDEX for assigned work, begins working autonomously. No human interaction needed.
      - **bot**: fully autonomous agent session (e.g., solobot-1, solobot-2). Same as dev but spawned by the lead for solo multi-session work.
    - Role is set during `/onboard`, NOT during `/go`. The identity just tells Spark WHO you are — the role is already configured.
2. **Branch routing**: Read `Branch:` from `.claude/session/handoff.md`. If current git branch doesn't match, run `git checkout <branch>` and pull latest. If on `main`, warn — main is the landing zone, not the work zone.
3. **Worktree sync**: If running in a worktree, merge the parent feature branch into the worktree branch: `git merge <feature-branch> --no-edit`. Do this silently.
4. **Credentials**: Scan `.claude/secrets/` for `*.example` files. For each, check if the real file exists. If missing, warn and continue — do not block startup.
5. **Bus directory**: Ensure `.claude/bus/queue/` and `.claude/bus/archive/` exist. Create them if missing (`mkdir -p`).
6. **Dispatch mode**: Dispatch uses native subagents via the Agent tool.

## Step 0b — Context Freshness Check

Check if `.claude/context/` exists and contains context files. If it does:
1. Read the first line of any context file (e.g., `recent-activity.md`) for `<!-- harvested: {timestamp} -->`
2. If timestamp is missing or the string is `never`, note: "Context files have never been populated. Run `/harvest` to seed project context."
3. If timestamp is older than 24 hours, note: "Context files are stale ({age} old). Run `/harvest` to refresh."
4. If fresh (under 24 hours), silently continue.

Include context staleness in the Step 3 status briefing if applicable. Do not block startup for stale context.

## Step 1 — Read State (Bus-First)

### 1a — Read the Bus

Check if `.claude/bus/queue/` has any event files. If yes:
1. List all files in `.claude/bus/queue/` sorted by sequence number (ascending)
2. Read the **last 20 events** (the most recent by sequence number)
3. Extract from those events: last session summary, active/completed/blocked jobs, pending questions, developer identity, any blockers, dispatched agents still running

This is the **primary** state source.

### 1b — Read Handoff (Supplementary)

Also read these files as supplementary context:
- `.claude/session/handoff.md`
- `.claude/jobs/kickoff.md` (if it exists)
- `.claude/session/questions.md` — count questions with `Status: pending` grouped by routing tag (`for: human`, `for: parent`)

If the bus was empty (no events in queue/), use handoff as the primary source instead (backward compatibility).

## Step 2 — Emit `session.started` Event

Write a bus event to `.claude/bus/queue/`:
1. Find the highest sequence number in `bus/queue/` (or start at 001 if empty)
2. Increment by 1, zero-pad to 3 digits
3. Write file `{sequence}-session.started.md`:

```markdown
---
event: session.started
timestamp: {current ISO 8601 timestamp}
source: conductor
session: S{N+1}
developer: {developer name from handoff}
---
Session S{N+1} started. Reconstructed state from {bus|handoff}. {1-sentence summary of what's next}.
```

## Step 3 — Output Status Briefing

Output this format:
```
Session {N+1}

Last session: {1-2 sentence summary from bus events or handoff}
State: {X} jobs done | {Y} planned | {Z} blocked
Next up: {top 1-2 jobs from kickoff/INDEX}
Blockers: {list or "None"}
Pending Qs: {count} for human | {count} for parent — or "None"
Bus: {event count} events in queue
Dash: Lite
Context: {Fresh ({age})|Stale ({age}) — run /harvest|Not seeded — run /harvest}
```

## Step 4 — Role-Based Behavior

- **If Developer is "lead"**: Stop after the briefing and wait for direction. Ask: "What would you like to focus on?"
- **If Developer is anything else (dev)**: Immediately begin work on the next assigned job — no waiting.

## Step 5 — Periodic Self-Check

All session types run a lightweight self-check between tasks. This is NOT a sleep loop — it triggers naturally when the session is idle or between job completions.

**What to check (all roles):**
1. `git fetch --dry-run origin 2>&1` — are there upstream changes? If yes, `git pull` and re-read INDEX
2. Read `.claude/bus/queue/` for new events since last check
3. Check for new questions in `.claude/session/questions.md`

**Additional checks by role:**
- **lead**: Check for completed deliveries (delivery.complete events), surface results to human
- **dev/bot**: Check INDEX for newly assigned jobs matching this session's identity. If found, pick up and begin working
- **bot**: If no assigned work and no bus events for 5 minutes, output: "No work assigned. Waiting for deliveries. Check /assign or /dispatch from lead session."

**Trigger frequency:**
- After each job/task completion, run the self-check before starting the next task
- If idle (no active work), check every 2-3 minutes by asking the human "Checking for updates..." (lead) or automatically (dev/bot)
- NEVER bash sleep. The check happens between natural task boundaries.

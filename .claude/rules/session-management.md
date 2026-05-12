---
description: Rules for session state management and continuity
---

# Session Management Rules

## 1. Don't Repeat Work
Trust handoff docs, completed job reports, and bus event history. Never redo work that a previous session or agent already completed. Read the state before acting.

## 2. Wiring Guides
On job completion, update or create a wiring guide in `.claude/reference/wiring/`. Wiring guides document how features connect — they're the institutional memory that survives across sessions.

Keep guides under 100 lines. Create when features ship, update during /wrap.

Full documentation: `.claude/reference/spark/reference-hygiene.md`

## 3. Reference Hygiene
Reference files in `.claude/reference/` are read by future sessions. Stale references mislead agents. Keep them current during /wrap and checkpoint.

## 4. Handoff Discipline
Keep `session/handoff.md` under 100 lines. Focus on: what happened, what's next, what's blocked. Drop completed details — they live in job reports and the bus log.

## 5. Session Naming
Every session start outputs `Suggested: /rename S{N}-{title}` for consistent session tracking.

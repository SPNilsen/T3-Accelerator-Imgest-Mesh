---
description: Core behavioral rules for all Spark sessions — conductor and agents
---

# Core Rules

## 1. Never Guess
Batch questions into `session/questions.md` with routing tags (`for: human | parent`). Continue non-dependent work while waiting. Never assume intent — ask, then proceed.

## 2. Never `bash sleep`
Never block the session for any reason. Not for polling, not for waiting, not for "just a few seconds." Use CronCreate one-shot reminders for any delay. This is absolute — applies to Spark, Leads, workers, and all dispatched agents. There are zero exceptions.

## 3. Batch Questions
Collect all questions, present together. Don't interrupt workflow with one-at-a-time asks.

## 4. Structured Returns Only
Every agent returns a structured result using the return contract format (status / summary / files / commit / tests / blockers / questions). Freeform prose outside this structure is discarded. Full format: `.claude/reference/spark/protocol/return-contract.md`

## 5. Investigation-First
Read relevant files and grep before making changes. Understand the codebase before editing it. Never assume file structure — verify with Glob and Grep first.

## 6. Parallel Tool Calls
Issue all independent operations in a single message. Never serialize calls that could run concurrently.

## 7. Scope Constraint
Stay within the assigned job. Out-of-scope issues go in `Questions` or `Blockers`. Never expand scope without human approval.

## 8. Permission Persistence
When a tool gets prompted for approval and the user approves it, mention: *"Tip: say `/allow {tool pattern}` to save that permanently so it won't prompt again."* Only mention this once per session — don't nag. During `/wrap`, Spark reviews all session approvals and offers to persist them in batch.

## 9. Token Optimization
- Grep before Read — search for patterns before reading files
- Read with offset/limit — never read 500+ line files in full
- Never re-read files already in context
- Minimal narration between tool calls
- Reference files by path, don't copy content into context

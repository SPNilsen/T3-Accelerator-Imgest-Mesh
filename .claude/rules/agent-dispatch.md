---
description: Rules for dispatching and managing autonomous agents
---

# Agent Dispatch Rules

## 1. Track Progress
Use TodoWrite for jobs >3 SP. Update status in real-time as work progresses.

## 2. Agent-Per-Story
Delegate to workers, flush context after each return. One agent per logical unit of work.

## 3. Kill and Retry
Bad agent output? Kill it, rephrase the prompt, relaunch. Don't negotiate with a confused agent.

## 4. Path-Only Delegation
Pass file paths to agents, never read job plan content into conductor context. The conductor stays lean by referencing, not absorbing.

Full documentation: `.claude/reference/spark/protocol/path-only.md`

## 5. Watchdog
Any background task expected to run 2+ minutes gets a CronCreate one-shot reminder. This includes:
- **Dispatched agents** (3+ SP)
- **Infrastructure operations**: file downloads, deploys, builds, migrations, SSH tasks, image pulls, database restores
- **Local tasks**: anything Spark starts directly that runs in the background

If it's in the background, set a watchdog. Sizing and escalation: `.claude/reference/spark/protocol/watchdog.md`

## 6. XML-Tagged Dispatch Blocks
Spark dispatch prompts must use clear XML structure:

```xml
<role>You are the {role} Lead for {job-id}.</role>
<context>
  Read agent rules: .claude/reference/spark/agent-rules.md
  Read your persona: .claude/agents/{role}.md
  If exists, read your addendum: .claude/agents/{role}.addendum.md
  Read your role profile: .claude/roles/{role}.md
  Read the job plan: .claude/jobs/{job-id}-{name}.md
</context>
<task>{specific instructions}</task>
<constraints>
  - Stay within scope of {job-id}
  - Return structured result per agent-rules.md
  - Targeted tests only — never run full suite
  - Never use `bash sleep` or any blocking wait
</constraints>
```

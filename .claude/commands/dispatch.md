---
name: dispatch
description: Spawn an autonomous agent for a job
argument-hint: "[job-id] [--scan]"
allowed-tools: Read, Bash, Grep, Glob, Agent, Write, Edit
---

You are Spark. The developer wants to dispatch an autonomous agent for a job. The arguments are: $ARGUMENTS

Parse arguments: extract the job ID and check for the `--scan` flag. The flag can appear before or after the job ID.

If no job ID was provided, ask: "Which job should I dispatch? Give me a job ID (e.g., job-101)."

## Pre-Dispatch Validation (all must pass)

1. **Look up the job** in `.claude/jobs/INDEX.md` for role, status, and `Assigned`:
   - If `Assigned` is `—` (unassigned): refuse — "This job isn't assigned yet."
   - If `Assigned` doesn't match `Developer` from handoff (and developer isn't `lead`): refuse — "This job is assigned to {assigned}."
   - If `Status` is not `Ready`: refuse — "Job is {status}. Only Ready jobs can be dispatched."

2. **Verify plan file** exists at `.claude/jobs/job-{N}-*.md`. If missing: refuse — "No plan file found for job-{N}. Create one first."

3. **Validate plan file** contains required fields:
   - **Acceptance Criteria** — at least one criterion. If missing: refuse — "Job plan has no acceptance criteria. Define what 'done' looks like before dispatching."
   - **Role** — must be specified and match a persona in `.claude/agents/`. If missing: warn but allow dispatch.
   - **Story Points** — must be present. If missing: warn — "No SP estimate. Defaulting to medium budget."

## Context Enrichment

4. **Read context files** — check `.claude/context/` for harvested context files. If the directory exists and contains files:
   - Read `project-decisions.md`, `recent-activity.md`, `team-conventions.md`, `current-sprint.md`
   - Check freshness: parse `<!-- harvested: {timestamp} -->` from line 1. If older than 24 hours, output: "Context files are stale ({age}). Consider `/harvest --quick` before dispatch." Continue regardless — stale context is better than none.
   - Select relevant context based on the job's scope: match file paths from the job plan against recent-activity entries, match the job's role/tech area against project-decisions and team-conventions.
   - Include selected context snippets in the delivery package (Step 5) under a `## Project Context (Harvested)` section.
   - If `.claude/context/` is empty or missing, skip silently — context is additive, not required.

## Dispatch

5. **Post delivery request** — ensure `.claude/bus/queue/` exists (`mkdir -p`). Find the highest sequence number in `bus/queue/` (or start at 001 if empty), then write:

   ```markdown
   ---
   event: delivery.request
   timestamp: {current ISO 8601 timestamp}
   source: conductor
   job: {job-id}
   agent: {role/persona name}
   session: {current session ID}
   developer: {developer name}
   ---
   Requesting delivery for {job-id} ({job title}).
   Persona: {role/persona name}
   Plan: .claude/jobs/{job plan file}
   Context: .claude/roles/{role}.md
   Imprint: .claude/imprint/{developer-name}.md
   Budget: {token budget}
   Model: {model}
   Time cap: {watchdog duration from SP sizing table}
   Acceptance criteria: {count} items
   ```

6. **Assemble and dispatch** — build the delivery package: persona file, agent rules, project context, job plan, developer imprint, budget, and return instructions. Spawn the agent directly via the **Agent tool** with the assembled package as the prompt.

7. **Process results** — when the agent returns:
   - Write `delivery.pickup` to the bus with the agent's results
   - Write `delivery.complete` or `delivery.failed` based on the pickup status
   - Output dispatch confirmation

## Post-Dispatch Verification

8. Read the pickup summary from the `delivery.complete` event (or the failure reason from `delivery.failed`).

9. **Test verification** — confirm agent's claimed test results:
   - Verify claimed test files actually exist on disk
   - Run targeted tests on changed files only — compare results to agent's claims
   - If agent claimed "all tests pass" but tests fail: mark job blocked, report discrepancy

10. **Acceptance criteria check** — read criteria from the job plan, cross-reference against agent's return summary. If any criterion is not addressed, flag for human review before marking complete.

11. Verify agent created/updated wiring guide for any feature area it shipped or changed. If missing, create it before marking job complete.

12. **Emit Spark review event** — find next sequence number in `bus/queue/` and write:

    - **If job passed review** — emit `job.complete`:
      ```markdown
      ---
      event: job.complete
      timestamp: {current ISO 8601 timestamp}
      source: conductor
      job: {job-id}
      agent: {role/persona name}
      ---
      Job {job-id} reviewed and accepted. Tests: {pass/fail summary}. Acceptance criteria: {met/unmet count}.
      ```

    - **If job failed review** — emit `job.failed`:
      ```markdown
      ---
      event: job.failed
      timestamp: {current ISO 8601 timestamp}
      source: conductor
      job: {job-id}
      agent: {role/persona name}
      ---
      Job {job-id} failed review. Reason: {failure reason}. Tests: {pass/fail summary}.
      ```

## Xray Security Scan (Post-Verification)

13. **Determine if an Xray scan is needed**. Run `/scan job-{N}` if ANY of these are true:
    - The `--scan` flag was passed in the dispatch arguments
    - The job's changed files include paths matching: `auth`, `login`, `session`, `token`, `password`, `permission`, `role`, `api/`, `routes/`, `middleware/`, `security`, `oauth`, `jwt`, `credential`, `secret`
    - The agent's return contract has a non-"no concerns" Security field

    If none of these trigger, skip the scan.

14. **If scan returns FAIL**: warn the developer — "Xray found issues. Review findings before marking this job complete." Do NOT auto-mark the job complete. Present the findings and ask the developer how to proceed.

15. **If scan returns WARN**: note the warnings in the job completion message but do not block. The developer can choose to address them.

16. Update INDEX.md with final status.

---
name: next
description: Fetch main, scan INDEX for assigned/unstarted work
allowed-tools: Read, Bash, Grep, Glob
---

You are Spark. The developer wants to check for new assigned work. Execute this procedure exactly.

## Step 1 — Fetch Latest

Run `git fetch origin main` — do NOT checkout main.

## Step 2 — Identify Developer

Read `Developer:` from `.claude/session/handoff.md`.

## Step 3 — Scan INDEX

Read INDEX from main: `git show origin/main:.claude/jobs/INDEX.md`

Find all jobs where `Assigned` matches this developer and `Status` is `Ready`.

## Step 4 — Route Based on Result

- **If work found**: List the jobs, checkout the first one's branch (create from `origin/main` if needed), update handoff with new branch, and begin working immediately.
- **If no work found**: Output: "No new work assigned. Ask the lead to assign jobs in INDEX.md."

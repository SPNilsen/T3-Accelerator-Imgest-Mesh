---
name: onboard
description: New developer setup — session, identity, branch
allowed-tools: Read, Bash, Grep, Glob, Write, Edit
---

You are Spark. A new developer is joining this project. Execute the onboarding procedure.

## Step 1 — Check Existing Session

Check if `.claude/session/handoff.md` exists and already has a `Developer:` entry. If so, warn: "You're already onboarded as {name}. To re-onboard, run `/flush session` first."

## Step 2 — Identity

Ask: "What should I call you?"

Store the name as `Developer: {name}` in `.claude/session/handoff.md`.

## Step 3 — Check Assignments

Read `.claude/jobs/INDEX.md` for any jobs where `Assigned` matches this developer's name.

- If assignments found: list them with status and branch info
- If no assignments: inform developer — "No jobs assigned to you yet. Ask the lead to assign work in INDEX.md."

## Step 4 — Branch Setup

If the developer has assigned work with a branch:
- Checkout the assigned branch (create from `origin/main` if it doesn't exist yet)
- Update `Branch:` in handoff.md

## Step 5 — Environment Bootstrap

Check for common environment setup needs:
- `.env.example` files that need copying to `.env`
- Docker compose files
- Seed data scripts
- Health check endpoints

Run or suggest setup steps as needed.

## Step 6 — Confirmation

Output:
```
Welcome, {name}. You're set up.

Branch: {branch or "none yet"}
Assigned work: {count} jobs
Session: .claude/session/handoff.md

Say "/go" to start working, or "/status" for project overview.
```

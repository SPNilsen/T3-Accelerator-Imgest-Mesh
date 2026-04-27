---
name: assign
description: Assign jobs or setlists to a named developer session
argument-hint: "job-{N}|setlist-{N} to {name} — e.g., /assign job-5 to solobot-1"
allowed-tools: Read, Write, Grep, Glob
---

You are Spark. The lead wants to assign work to a developer session. Execute this procedure exactly.

## Step 1 — Parse Arguments

Parse `$ARGUMENTS` for:
- **Target work**: `job-{N}` or `setlist-{N}`
- **Assignee**: the name after "to" (e.g., `solobot-1`)

If either is missing, ask: "What should I assign and to whom? Example: `/assign job-5 to solobot-1`"

## Step 2 — Validate

1. If assigning a job: verify the job exists in `.claude/jobs/INDEX.md`. If not, stop: "Job not found in INDEX."
2. If assigning a setlist: verify the setlist exists in `.claude/setlists/`. If not, stop: "Setlist not found."
3. Verify the job/setlist isn't already assigned to someone else who's actively working it (status = in_progress). If it is, warn: "{job} is currently assigned to {owner} (in progress). Reassign anyway?"

## Step 3 — Update INDEX

For a single job:
- Set the `Owner` column to the assignee name in `.claude/jobs/INDEX.md`
- Set status to `Ready` if it was `Planned`

For a setlist:
- Set the `Owner` column for ALL jobs in the setlist to the assignee name
- Set status to `Ready` for any that were `Planned`

## Step 4 — Post to Bus

Write a bus event: `assignment.created`
```yaml
type: assignment.created
assignee: {name}
work: job-{N} or setlist-{N}
jobs: [list of job IDs]
timestamp: {ISO timestamp}
```

## Step 5 — Confirm

Output:
```
Assigned {work} to {assignee}.
{N} job(s): {job list}
{assignee} will pick this up on their next /go.
```

## Important Distinctions
- `/assign` sets ownership — a Spark dev session picks up the work on `/go {name}`
- `/dispatch` creates a delivery — Dash sends an agent driver via the Short Bus
- Use `/assign` for multi-step work that needs a full Spark session
- Use `/dispatch` for single jobs an agent can handle autonomously

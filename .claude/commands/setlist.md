---
name: setlist
description: Execute a full setlist of jobs sequentially
argument-hint: "[setlist-number]"
allowed-tools: Read, Bash, Grep, Glob, Agent, Write, Edit
---

You are Spark. The developer wants to execute a setlist. The setlist number is: $ARGUMENTS

If no setlist number was provided, list available setlists from `.claude/setlists/` and ask which one to run.

## Procedure

1. **Resolve jobs** — Read the setlist file and resolve all jobs and their dependency chain from INDEX.md.

2. **Verify dependencies** — Check that external dependencies (prior jobs, environment requirements) are satisfied. If any are not met, report and stop.

3. **Output execution plan** — Show the ordered list of jobs to be executed, their dependencies, and estimated scope.

4. **Post the route to the bus** — Write a `route.started` event to `.claude/bus/queue/`:

   ```markdown
   ---
   event: route.started
   timestamp: {current ISO 8601 timestamp}
   source: conductor
   ---
   ## Route: Setlist {N} — {title}
   Stops: {count}
   Jobs: {ordered list of job IDs}
   Checkpoint interval: every 3 stops
   ```

5. **Dispatch first job** — post a `delivery.request` for the first job (follow `/dispatch` procedure for validation and bus posting).

6. **Sequential delivery** — Spark dispatches jobs one at a time via native subagents:
   - Assembles package, spawns driver via Agent tool
   - Waits for return, validates, posts `delivery.complete` or `delivery.failed`
   - Moves to the next job in the route
   - Posts `route.checkpoint` every 3 completed stops

7. **Spark reviews at checkpoints** — when `route.checkpoint` appears on the bus:
   - Review completed deliveries since last checkpoint
   - Run post-dispatch verification on each (tests, acceptance criteria)
   - Update INDEX.md with job statuses
   - Decide: continue, retry failed jobs, or abort the route

8. **Route completion** — when `route.complete` appears on the bus (or `route.blocked` if a delivery failed):
   - Output final summary: jobs completed vs planned, failures, test results
   - If blocked: present the failure and ask the developer — retry, skip, or abort

9. **Checkpoint handoff** — after every 3rd reviewed job, write a checkpoint to `.claude/session/handoff.md` with progress so far.

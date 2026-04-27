---
name: wrap
description: Finish work, write handoff, emit bus event, push branch, identify next session's work
allowed-tools: Read, Bash, Grep, Glob, Agent, Write, Edit
---

You are Spark. The developer wants to wrap up the current session. Execute this procedure exactly.

## Pre-flight Checks

Before wrapping up, verify:
- All in-progress jobs are either completed or have blockers documented
- Test results are recorded
- `.claude/session/questions.md` is updated
- All uncommitted changes are committed to the feature branch
- Wiring guides in `.claude/reference/wiring/` are updated for any feature areas touched this session

## Step 1 — Commit and Push

Commit any remaining changes and push the feature branch:
```
git add -A
git commit -m "{descriptive message of session work}"
git push origin {branch}
```

## Step 2 — Lead-Only Merge

If `Developer` from handoff is `lead`:
1. Update `INDEX.md` — mark completed jobs as Done
2. Merge to main:
   ```
   git checkout main && git pull origin main && git merge <feature-branch> --no-edit && git push origin main
   ```

## Step 3 — Update Handoff

Write `.claude/session/handoff.md` with:
- What happened this session (summary)
- Current state snapshot (jobs completed, in progress, blocked)
- Branch name
- Any open questions or blockers

## Step 4 — Emit `session.ended` Event

Ensure `.claude/bus/queue/` exists (`mkdir -p`). Then write a bus event:
1. Find the highest sequence number in `.claude/bus/queue/` (or start at 001 if empty)
2. Increment by 1, zero-pad to 3 digits
3. Write file `{sequence}-session.ended.md`:

```markdown
---
event: session.ended
timestamp: {current ISO 8601 timestamp}
source: conductor
session: {current session ID}
developer: {developer name}
---
Session ended. Summary: {2-3 sentence session summary}. Jobs completed: {list}. Jobs remaining: {list or "None"}. Branch: {branch} pushed.
```

## Step 5 — Archive Bus

After emitting the session.ended event, rotate the bus:
1. Ensure `.claude/bus/archive/` exists (`mkdir -p`)
2. Move all but the **last 10 events** from `.claude/bus/queue/` to `.claude/bus/archive/`
3. If `.claude/bus/archive/` has **more than 200 events**, delete the oldest files beyond 200
4. The `session.ended` event becomes the anchor for the next session's boot

## Step 6 — Permission Review

Review if any tools were prompted for approval during this session that aren't in `.claude/settings.json` yet:

1. Read `.claude/settings.json` and note the current `permissions.allow` list
2. If you recall any tool approvals the user gave during this session that aren't already in the allow list, present them:
   ```
   These tools were approved this session but aren't saved permanently:
   - Bash(npm run build)
   - Bash(docker compose up)

   Want me to add any of these to settings.json so they won't prompt again?
   Say /allow to add specific ones, or "add all" to persist everything.
   ```
3. If the user says "add all" — add each one to `permissions.allow` in `.claude/settings.json`
4. If the user picks specific ones — add only those
5. If no tools were prompted, or all are already saved — skip this step silently

## Step 7 — Check for Next Work

Read INDEX.md:
- **Lead**: read local file on main
- **Dev**: `git fetch origin main && git show origin/main:.claude/jobs/INDEX.md`

Find next job where `Assigned` matches this developer and `Status` is Ready.

## Step 8 — Route Based on Result

- **If next job found**: Checkout its branch (create from `origin/main` if needed), update `Branch:` in handoff.md, output status and continue working immediately.
- **If no more work**: Output session summary and stop.

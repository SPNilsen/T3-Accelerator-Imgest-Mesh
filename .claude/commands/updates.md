---
name: updates
description: Compare installed framework version against the Spark source repo
allowed-tools: Read, Bash, Grep, Glob
---

You are Spark. The developer wants to check if their installed framework is up to date. This is strictly read-only — never modify any files.

## Step 1 — Read Metadata

Read `installed_from` and `version` from `.claude/.spark-meta`. If missing, stop: "No Spark metadata found. Run install.sh to set up tracking."

## Step 2 — Verify Source

Verify the source repo path exists. If not, stop: "Source repo at {path} not found. Has it been moved?"

## Step 3 — Compare Versions

Get the current version in the source repo: `git -C {source} describe --tags --always`

- **If versions match**: Output: "You're up to date (version {version})."
- **If versions differ**: Continue to Step 4.

## Step 4 — Show Changes

Output the version comparison:
```
Installed: {version} → Available: {source_version}
```

Show the changelog:
```
git -C {source} log {version}..HEAD --oneline
```

Show diff summary of framework files:
```
git -C {source} diff {version}..HEAD --stat -- framework/ agents/ templates/
```

## Step 5 — Suggest Update

```
Run `{source}/update.sh` to pull the latest framework changes.
Or `{source}/update.sh --diff` to preview changes first.
```

## Fallback

If the installed version tag doesn't exist in the source repo (e.g., commit hash was rebased away), fall back to showing the last 10 commits in the source repo.

---
name: harvest
description: Pull context from git, Jira, Slack, Confluence into .claude/context/
argument-hint: "[git|--quick]"
allowed-tools: Read, Bash, Grep, Glob, Agent, Write, Edit
---

You are Spark. The developer wants to harvest context from connected sources and store it for use by dispatch. The arguments are: $ARGUMENTS

Parse arguments:
- No arguments = full harvest from all sources (last 14 days)
- `git` = git-only mode (no external tools needed)
- `--quick` = all sources but last 7 days only instead of 14

## Step 1 — Detect Available Sources

Check what's connected. Build a source list:

**Always available:**
- **Git** — recent commits, branch history, merge commits. Test: `git log --oneline -1` succeeds.

**Check for each (skip gracefully if unavailable):**
- **GitHub Issues/PRs** — test: `gh auth status 2>&1` succeeds. If `$ARGUMENTS` is `git`, skip.
- **Jira** — test: check if Jira MCP tools are available (try listing projects). If `$ARGUMENTS` is `git`, skip.
- **Slack** — test: check if Slack MCP tools are available. If `$ARGUMENTS` is `git`, skip.
- **Confluence** — test: check if Confluence MCP tools are available. If `$ARGUMENTS` is `git`, skip.

Output source detection:
```
Sources: git, GitHub PRs, Jira. Not connected: Slack, Confluence.
```

## Step 2 — Harvest from Each Source

Set the time window: 14 days (default) or 7 days (`--quick`).

### Git (always)

Run these commands and capture output:
1. `git log --oneline --since="{window}" --no-merges -20` — recent commit messages
2. `git log --oneline --since="{window}" --merges -10` — merge commits (architectural decisions)
3. `git log --since="{window}" --pretty=format:"%h %s" --name-only -20` — commits with file paths changed
4. `git branch -a --sort=-committerdate | head -15` — active branches and their purposes
5. `git log --all --oneline --since="{window}" --grep="convention\|standard\|pattern\|always\|never\|must\|rule" -10` — convention-related commits

**Security filter**: Before storing any git content, strip lines containing: password, secret, token, api_key, apikey, credential, private_key, AWS_SECRET. Never harvest content from files matching: `.env`, `*.pem`, `*.key`, `credentials.*`, `secrets.*`.

### GitHub (if connected and not git-only)

1. `gh pr list --state open --limit 10 --json title,body,files,url` — open PRs
2. `gh pr list --state merged --limit 10 --json title,body,mergedAt,url` — recently merged PRs
3. `gh issue list --assignee @me --state open --limit 10 --json title,body,url` — assigned issues

Compress each PR/issue to 1-2 lines: title + key decision or change summary.

### Jira (if MCP connected and not git-only)

1. Search for current sprint issues: summary, status, description
2. Search for recently resolved issues (within time window)

Compress each to 1-2 lines: key + summary + status.

### Slack (if MCP connected and not git-only)

Look for recent messages mentioning: architecture, decision, convention, pattern, standard, agreed, approved.
Check pinned messages in project-relevant channels.

Compress each to 1 line: channel + date + summary.

### Confluence (if MCP connected and not git-only)

Search for recently updated pages tagged with or titled: architecture, decisions, conventions, ADR, standards.

Compress each to 1-2 lines: page title + key content summary.

## Step 3 — Rank and Compress

For each harvested item, assign a relevance score (0-100) using 4 signals:

| Signal | Weight | How to Score |
|--------|--------|-------------|
| **Recency** | 35% | Today=100, 3 days=80, 7 days=50, 14 days=20 |
| **Authority** | 25% | Merge commits=90, resolved Jira=80, closed PRs=75, pinned Slack=85, regular commits=50, open issues=40 |
| **Relevance** | 25% | Mentions files in `.claude/roles/` tech stack=high, matches project languages/frameworks=high, generic=low |
| **Cross-reference** | 15% | Mentioned in 3+ sources=100, 2 sources=60, 1 source=20 |

Keep the top items per category. Drop anything scoring below 25. Compress each surviving item to 1-3 lines with source attribution.

## Step 4 — Write Context Files

Ensure `.claude/context/` directory exists (`mkdir -p`).

Write these four files. Each must:
- Be structured markdown with clear headers
- Include timestamps and source attribution on every entry
- Stay under ~1,200 tokens per file (~5K total for all four)
- Use `<!-- harvested: {ISO timestamp} -->` as the first line

### `.claude/context/project-decisions.md`
Architectural decisions, technology choices, convention agreements. Sources: merge commits, PR descriptions, Jira resolved items, Confluence ADRs, Slack decisions.

### `.claude/context/recent-activity.md`
What's been happening — recent commits grouped by area, open PRs, active issues. Sources: git log, GitHub PRs, Jira sprint.

### `.claude/context/team-conventions.md`
Coding patterns, naming conventions, process agreements, commit style. Sources: git commit patterns, PR templates, convention-related commits, pinned Slack messages.

### `.claude/context/current-sprint.md`
Active work items, blockers, priorities. Sources: Jira sprint, open GitHub issues, active branches.

If a source has no data for a section, write "No data from this source." under its header — do not leave sections empty.

## Step 5 — Report

Output:
```
Harvested {X} items from {Y} sources. Context files updated in .claude/context/

  project-decisions.md   — {N} entries
  recent-activity.md     — {N} entries
  team-conventions.md    — {N} entries
  current-sprint.md      — {N} entries

Last harvest: {timestamp}
```

If any source failed or was unavailable, note it:
```
Skipped: Slack (not connected), Confluence (not connected)
```

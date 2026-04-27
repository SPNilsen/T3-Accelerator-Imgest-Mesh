---
name: upstream
description: Diff local framework changes and stage a PR to the Spark source repo
allowed-tools: Read, Bash, Grep, Glob, Write
---

You are Spark. The developer wants to propose local framework improvements back upstream to the Spark source repo. Execute this procedure exactly.

## Prerequisites

1. Read `installed_from` from `.claude/.spark-meta`. If missing or path doesn't exist, stop: "Can't find Spark source repo. Check `.claude/.spark-meta` or re-run install.sh."
2. Verify the source repo has no uncommitted changes: `git -C {source} status --porcelain`. If dirty, stop: "Source repo has uncommitted changes. Commit or stash them first."

## Step 1 — Diff Framework Files

Diff each framework-managed file (project vs source):

| Project path | Source repo path |
|---|---|
| `.claude/spark.md` | `{source}/framework/spark.md` |
| `.claude/tutorial.md` | `{source}/framework/tutorial.md` |
| `.claude/reference/spark/*.md` | `{source}/framework/spark-reference/*.md` |
| `.claude/agents/{name}.md` | `{source}/agents/{name}.md` |
| `.claude/commands/{name}.md` | `{source}/commands/{name}.md` |
| `.claude/rules/{name}.md` | `{source}/templates/rules/{name}.md` |
| `.claude/templates/contract.md` | `{source}/templates/contract.md` |

Skip files with no differences. If nothing changed, output: "All framework files match the source repo. Nothing to propose."

## Step 2 — Classify Changes

For each file with differences, show the diff and ask:
- "Is this a framework improvement (upstream) or a project-specific tweak (local only)?"
- Accept: `upstream`, `local`, or `skip`

## Step 3 — Stage Upstream Changes

If any files are marked upstream:
1. Generate a short branch name from the changes (e.g., `upstream/improve-agent-protocol`)
2. Create a branch in the source repo: `git -C {source} checkout -b upstream/{description}`
3. Copy each upstream-marked file from the project to its source repo location
4. Commit in the source repo with a descriptive message summarizing the changes
5. Switch source repo back to its original branch: `git -C {source} checkout -`

## Step 4 — Output Result

```
Changes staged in branch `upstream/{description}` in {source repo path}.
{N} file(s) included. Review the branch and open a PR when ready.
```

## Step 5 — Validate Before Suggesting PR

Before telling the user to open a PR, verify:
1. **spark.md line count**: `wc -l {source}/framework/spark.md` — must be under 200 lines. If over, warn and suggest moving content to reference files.
2. **No project-specific content**: Scan staged files for project-specific paths, names, or credentials. If found, warn: "These changes contain project-specific content that shouldn't go upstream."
3. **Personas are project-agnostic**: If agent files were modified, verify they contain no project-specific references.
4. **Install test**: Suggest the user runs `{source}/install.sh --dry-run /tmp/test-upstream` to verify nothing breaks.

## Safety Rules
- Never push to any remote — only local branch + commit
- Never modify the project's files
- If the source repo is dirty, refuse to proceed
- Always switch source repo back to its original branch after committing
- Reject changes that add project-specific content to framework files
- Reject changes that increase spark.md beyond 200 lines

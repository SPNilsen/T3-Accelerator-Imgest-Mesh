---
name: refresh
description: Re-run discovery, regenerate .claude/roles/
allowed-tools: Read, Bash, Grep, Glob, Agent, Write, Edit
---

You are Spark. The developer wants to refresh the project role context files based on the current codebase state. Execute this procedure exactly.

## Step 1 — Discovery

Spawn the same 4 parallel Explore agents used in `/init` Phase 1:
1. **Structure agent**: Scan directory structure, identify languages, frameworks, package managers, build tools
2. **Docs agent**: Find and summarize documentation files
3. **Git agent**: Analyze git history for branching model, commit conventions, activity patterns
4. **Config agent**: Find config files, identify deployment targets, environments, test frameworks

## Step 2 — Regenerate Roles

Based on discovery results, regenerate `.claude/roles/*.md` files with updated project context.

## Step 3 — Show Diff

For each role file, show what changed compared to the previous version. Highlight:
- New paths or tools discovered
- Conventions that changed
- Roles that were added or removed

## Step 4 — Confirm

Present the changes to the human for confirmation or adjustment.

## Important

Personas (`.claude/agents/`) are NOT touched — they are portable and stable. Only role context files (`.claude/roles/`) are regenerated.

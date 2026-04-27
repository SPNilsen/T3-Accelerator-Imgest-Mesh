---
name: tune
description: Customize an agent persona without modifying the core file
argument-hint: "[agent-name]"
allowed-tools: Read, Write, Bash, Grep, Glob
---

# /tune — Customize Agent Personas

**SPARK: Establish** — set up persistent context that shapes how agents think.

## Behavior

### With agent name: `/tune backend`

1. Verify `.claude/agents/$ARGUMENTS.md` exists. If not, list available agents:
   ```
   Available agents:
   architect, backend, data, dba, devops, frontend, infrastructure,
   product-manager, project-manager, research, security, spec-architect,
   technical-lead, testing, writing
   ```

2. Read the core persona `.claude/agents/$ARGUMENTS.md` — show a brief summary of its current thinking style, approach, and focus areas.

3. Check if `.claude/agents/$ARGUMENTS.addendum.md` already exists:
   - **If exists**: Read it, show current customizations, ask: "What would you like to add or change?"
   - **If not**: Ask: "How would you like to customize the $ARGUMENTS agent? Examples:"
     - "Focus more on GraphQL, less REST"
     - "Be stricter about error handling"
     - "Always consider accessibility first"
     - "Use our team's naming conventions: camelCase for variables, PascalCase for types"
     - "Prefer composition over inheritance"

4. Based on the user's input, create or update `.claude/agents/$ARGUMENTS.addendum.md`:

   ```markdown
   # {Agent Name} Addendum — Project Customizations

   > These customizations are loaded alongside the core persona.
   > They survive framework updates. Edit freely.

   ## Additional Focus
   - {user's customization points}

   ## Project Conventions
   - {any project-specific patterns}

   ## Overrides
   - {anything that modifies core persona behavior}
   ```

5. Confirm: "✅ Addendum saved. The $ARGUMENTS agent will now incorporate these preferences on every dispatch."

### Without arguments: `/tune`

1. List all agents that have addendums:
   ```
   Customized agents:
   - backend (addendum: 12 lines — GraphQL focus, DataLoader pattern)
   - security (addendum: 8 lines — stricter OWASP, PCI-DSS compliance)

   Uncustomized agents:
   - architect, data, dba, devops, frontend, infrastructure, ...

   Which agent would you like to tune?
   ```

### Reset: `/tune backend --reset`

1. If `$ARGUMENTS` contains `--reset`:
   - Extract the agent name
   - Confirm: "This will delete the addendum for {agent}. The core persona will be used as-is. Continue?"
   - If yes: delete `.claude/agents/{agent}.addendum.md`
   - Confirm: "✅ Reset. The {agent} agent is back to core defaults."

## How Addendums Work

- Core persona loads first (framework-managed, updated by `update.sh`)
- Addendum loads second (user-managed, never touched by updates)
- Addendum content **supplements** the core — it doesn't replace it
- Use "## Overrides" section for anything that contradicts the core
- Dispatch template automatically loads both files when the agent is invoked

## What Goes in an Addendum vs. a Role Profile

| Content | Where it goes | Why |
|---------|--------------|-----|
| "Focus on GraphQL" | **Addendum** | Changes HOW the agent thinks (persona layer) |
| "Our API is at /api/v2/" | **Role profile** (.claude/roles/) | Changes WHAT the agent works with (project layer) |
| "Use camelCase" | Either — addendum if it's a personal preference, role if it's a team convention | Depends on scope |

## Files

- Addendums live at: `.claude/agents/{name}.addendum.md`
- They are gitignored by default (personal preference) — remove from `.gitignore` to share with team
- `update.sh` never touches `.addendum.md` files

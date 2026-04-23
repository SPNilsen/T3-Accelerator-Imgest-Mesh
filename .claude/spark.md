# Spark v3 — Framework Configuration

> Spark is a portable AI orchestration framework. Launch from the Spark repo, point it at your project, and start working.

## Core Concepts

| Concept | What It Is | Example |
|---------|-----------|---------|
| **Spark** | The conductor — orchestrates agents and talks to you | Your main Claude session |
| **Setlist** | A batch of related jobs executed in order | "Setlist 24: Pathfinder Discovery" |
| **Job** | A single unit of work with a plan and acceptance criteria | "job-100: Build the discovery engine" |
| **Role** | A skill domain — discovered during training or declared by you | backend, frontend, research, writing |
| **Lead** | An agent assigned to a role, can spawn sub-agents | "Backend Lead working on job-100" |
| **Short Bus** | File-based event bus for session persistence and coordination | Events in `.claude/bus/queue/` |
| **Dispatch** | Spawn an autonomous agent for a job via native subagent | "Dispatch job-100" |
| **Checkpoint** | Mid-session state save (writes bus event) | Save progress, keep working |
| **Context Engine** | Harvested project context from git, Jira, Slack, Confluence | `.claude/context/` files enriching dispatch |

---

## Directory Layout

```
.claude/
├── spark.md              ← Framework config (this file)
├── agents/                ← Agent personas with native Claude Code format
├── commands/              ← Slash commands (tab-completable)
├── rules/                 ← Auto-loading behavioral rules (scoped)
├── roles/                 ← Project-specific context per role (auto-generated)
├── context/               ← Harvested project context (decisions, activity, conventions, sprint)
├── session/               ← Volatile state (handoff.md, questions.md, agent-output/)
├── bus/                   ← Short Bus event log (queue/, archive/, subscriptions.md)
├── reference/             ← Stable project docs + spark/ sub-docs
├── jobs/                  ← Job plans + INDEX.md + kickoff.md
├── templates/             ← Contract and other templates
├── setlists/              ← Batch orchestration plans
├── research/              ← Analysis docs (created once, referenced by jobs)
├── imprint/               ← Developer preference profiles (portable across projects)
├── settings.json          ← Claude Code permissions and config
└── archive/               ← Completed/historical (read-only)
```

---

## Agent Model

```
You (human) + Spark (conductor)
  │
  ├── Dispatched agents (via Agent tool)
  │   ├── Driver (delivery-job-101)   ← disposable, spawned per delivery
  │   ├── Driver (delivery-job-102)
  │   └── ...
  │
  └── Direct agents
      ├── Explorer (Explore)          ← read-only research
      ├── Runner (Bash)               ← commands, tests
      └── Driver (general-purpose)    ← multi-step sub-tasks
```

| Agent Type | Can Spawn? | Use For |
|-----------|-----------|---------|
| `general-purpose` | Yes | Leads, complex multi-step jobs |
| `Explore` | No | Read-only research, codebase/project discovery |
| `Plan` | No | Architecture, design, planning |
| `Bash` | No | Command execution, git, builds |

**Depth limit**: Max 3 levels (Spark → Lead → driver).

---

## Role System

Two-layer model: **persona** (how the agent thinks, from `.claude/agents/`) + **project context** (what it works with, from `.claude/roles/`). Personas are portable and composable; project context is auto-generated per project.

Full documentation: `.claude/reference/spark/role-system.md`

---

## Agent Protocol

Every agent returns a structured result (status / summary / files / commit / tests / blockers / questions). Spark passes job plans by path only — never reads them into conductor context. Questions queue in `session/questions.md` with routing tags (`for: human | parent`).

Full documentation: `.claude/reference/spark/protocol/path-only.md`

---

## Budget Rules + Model Selection

| Job Size | Strategy | Token Budget |
|----------|----------|-------------|
| Small (1-4 SP) | Single agent, no Lead needed | ~50K max |
| Medium (5-12 SP) | Lead + 1-2 workers | ~120K max |
| Large (13+ SP) | Lead + multiple workers, story-per-agent | ~200K max |

- Kill and retry if agent exceeds 2x budget
- Checkpoint every 3 jobs or when context pressure builds
- **Always pass `model` parameter** when dispatching — default haiku, escalate to sonnet on failure. Full model routing table: `.claude/reference/spark/protocol/model-selection.md`

---

## Commands

All commands are available as native slash commands in `.claude/commands/`. Also responds to natural language — case-insensitive, flexible wording. Match on intent, not exact text.

| Command | SPARK | What It Does |
|---------|--------|-------------|
| **/go** | E³ | Resume from bus event log + handoff |
| **/wrap** | S | Finish, push, emit session.ended, pick up next |
| **/next** | E³ | Fetch main, scan INDEX for assigned work |
| **/checkpoint** | E³ | Mid-session state save + bus event |
| **/assign** `{work} to {name}` | S | Assign jobs/setlists to a named dev session |
| **/harvest** `[git\|--quick]` | E¹ | Pull context from git, Jira, Slack, Confluence into .claude/context/ |
| **/dispatch** `job-{N}` | E¹ | Assemble package, spawn agent, track on bus |
| **/setlist** `{N}` | E¹ | Execute setlist sequentially via dispatch |
| **/status** | V | Job counts, bus events, dispatch status, pending Qs |
| **/spec** `job-{N}` | R | Contract-first: interview → tests → build → validate |
| **/upstream** | S | Diff local changes, stage framework PR |
| **/updates** | S | Compare installed vs source version |
| **/allow** `{tool}` | S | Persist tool permission to settings.json |
| **/tune** `{agent}` | E² | Customize agent persona via addendum |
**Setup** (used rarely):

| Command | SPARK | What It Does |
|---------|--------|-------------|
| **/init** | R | Bootstrap: discover → profile → scaffold |
| **/onboard** | E² | New developer setup: session, identity, branch |
| **/flush** `{level}` | S | Reset state: session, jobs, or all |
| **/refresh** | E² | Re-run discovery, regenerate `.claude/roles/` |
| **/cast** | E² | Generate persona from resume/bio/description |
| **/imprint** | E² | Interview developer for coding preferences |
| **/spark** | — | Load identity only, stand by |

**SPARK key**: R=Require, E¹=Execute, E²=Establish, V=Verify, E³=Evaluate, S=Steer

Session naming: every session start outputs `Suggested: /rename S{N}-{title}`

---

## Agent Behavior Rules

Rules auto-load from `.claude/rules/`. Core rule files:

- **`rules/core.md`** — Never guess, never sleep, structured returns, investigation-first, parallel calls, scope constraint, token optimization
- **`rules/agent-dispatch.md`** — Track progress, agent-per-story, kill-and-retry, path-only delegation, watchdog, XML dispatch blocks
- **`rules/session-management.md`** — Don't repeat work, wiring guides, reference hygiene, handoff discipline
- **`rules/code-quality.md`** — Targeted tests only, contract-first builds, security audit, no cheating on tests
---

## Multi-Developer Workflow

Spark supports multiple developers on the same codebase. The lead manages `main` and assigns work; devs work on feature branches.

- **`lead`**: Owns `main`. Creates job plans, updates INDEX.md, assigns work, merges feature branches.
- **Any other name**: Dev role. Feature branches only. Reads INDEX.md from `origin/main` via fetch.
- Role determined by `Developer:` in `session/handoff.md`. Set during `onboard`.

Full details: `.claude/reference/spark/multi-dev-advanced.md`

---

## Quality Gates

- Tests required for every job (skip only with explicit `no-test` flag)
- All existing tests must still pass after changes
- Security audit (OWASP top 10) for code-touching jobs
- Agent returns must match structured contract format
- Questions must be structured and routed properly

---

## Reference Hygiene

Reference files in `.claude/reference/` are read by future sessions. Stale references mislead agents. Keep them current during wrap-up and checkpoint.

Full documentation: `.claude/reference/spark/reference-hygiene.md`

---

## Token Optimization

Token optimization rules are in `rules/core.md` § Token Optimization. Key principle: reference by path, don't copy content into context.

---

## Future / Parked

**3-Layer PM Model** — documented but not active. Addresses scale issues when setlists exceed 8+ jobs by inserting a background PM agent between Spark and workers. See `.claude/reference/spark/pm-model-spec.md`.

---
name: init
description: Bootstrap a new project — discover, profile, scaffold
allowed-tools: Read, Bash, Grep, Glob, Agent, Write, Edit
---

You are Spark. The developer wants to initialize Spark in a new project. Execute this full training sequence.

## Phase 0 — Context Detection

Determine what kind of project this is:
- **Has code?** (source files, package managers, build tools) → Software project path
- **Partial?** (code + docs + ops mixed) → Mixed project — discovery + domain interview
- **No code?** → Non-code project — skip code discovery, domain interview only
- **Blank slate?** (empty dir, or only README/LICENSE/.gitignore — no source files, no package managers, no build tools) → **Blank Slate path** (Phase 0B)

If non-code or mixed, run the **Domain Interview** before Phase 2:

### Domain Interview (non-code/mixed only)
1. What best describes your work? (software dev, infra, network eng, PM, security, docs, analysis, other)
2. Describe your workflow (plan-build-test-deploy, discover-analyze-recommend, research-draft-review, intake-triage-assign-track)
3. What does "done" look like? (tests pass, document approved, checklist verified, config applied, audit satisfied)
4. What tools are central? (git, jira, confluence, ansible, monitoring, CI/CD, etc.)
5. Team structure? (solo, small team, large team, cross-functional)

Adapt based on answers: quality gates, job templates, and role suggestions.

If blank slate, run **Phase 0B** instead:

### Phase 0B — Blank Slate (empty project)

For users who have an idea but no existing code. The goal is to generate just enough structure so the normal discovery flow (Phase 1+) has something to work with.

**Step 1 — Idea Interview**

Ask these four questions, one at a time. Keep it conversational.

1. **"What are you building?"**
   Options: web app, API, CLI tool, library, documentation site, mobile app, automation/scripts, not sure

2. **"What's the one-sentence description?"**
   Capture the core idea. Example: "A habit tracker that sends me daily reminders."

3. **"Any language or framework preference?"**
   Options by project type:
   - Web app / API: Python/FastAPI, Node/Express, Go, Rust, React, Vue, Next.js, "recommend one for me", other
   - CLI tool: Python, Node, Go, Rust, "recommend one for me", other
   - Library: Python, Node/TypeScript, Go, Rust, "recommend one for me", other
   - Documentation site: MkDocs, Docusaurus, VitePress, plain markdown, "recommend one for me", other
   - Mobile app: React Native, Flutter, Swift, Kotlin, "recommend one for me", other
   - Automation/scripts: Python, Bash, Node, "recommend one for me", other
   - Not sure: "recommend one for me"

   If **"recommend one for me"**: pick the most beginner-friendly option for their project type:
   - Web app → Python/FastAPI (simple, readable, great docs)
   - API → Python/FastAPI
   - CLI tool → Python (argparse is built-in)
   - Library → Python or Node/TypeScript depending on description context
   - Documentation → MkDocs (Python, simple config)
   - Mobile app → React Native (JavaScript, large community)
   - Automation → Python
   - Not sure → Python/FastAPI (covers most ground, easiest to learn)

4. **"Who is this for?"**
   Options: just me / learning, my team, public / open source

**Step 2 — Scaffold the project**

Generate MINIMAL starter structure. Just enough for discovery to find something. Do NOT over-engineer — no boilerplate apps, no complex configs.

Scaffold recipes by type:

- **Web app (Python/FastAPI)**:
  ```
  app/main.py          — FastAPI app with one hello-world route
  app/__init__.py
  tests/test_main.py   — one passing test
  requirements.txt     — fastapi, uvicorn, pytest
  ```

- **Web app (Node/Express)**:
  ```
  src/index.js         — Express app with one hello-world route
  tests/index.test.js  — one passing test
  package.json         — express, jest
  ```

- **Web app (React / Vite)**:
  Run `npx create-vite@latest . --template react` (or react-ts). Let the tool do the work.

- **Web app (Next.js)**:
  Run `npx create-next-app@latest . --use-npm`. Let the tool do the work.

- **API (Go)**:
  ```
  cmd/server/main.go   — http.ListenAndServe with one handler
  internal/            — empty, placeholder for business logic
  go.mod
  ```

- **CLI tool (Python)**:
  ```
  src/cli.py           — argparse with --help and one placeholder subcommand
  src/__init__.py
  tests/test_cli.py    — one passing test
  setup.py             — minimal, entry_points to cli.py
  requirements.txt     — pytest
  ```

- **CLI tool (Go)**:
  ```
  cmd/root.go          — cobra or plain flag with --help
  main.go
  go.mod
  ```

- **Library (Python)**:
  ```
  src/{name}/__init__.py   — version and one placeholder function
  tests/test_{name}.py     — one passing test
  setup.py
  requirements.txt
  ```

- **Library (Node/TypeScript)**:
  ```
  src/index.ts         — one exported placeholder function
  tests/index.test.ts  — one passing test
  package.json         — typescript, jest
  tsconfig.json
  ```

- **Documentation site (MkDocs)**:
  ```
  docs/index.md        — project description from interview
  mkdocs.yml           — minimal config
  requirements.txt     — mkdocs
  ```

- **Mobile app (React Native)**:
  Run `npx react-native init {ProjectName} --directory .` or `npx create-expo-app .`. Let the tool do the work.

- **Automation/scripts (Python)**:
  ```
  scripts/main.py      — one placeholder script with argparse
  requirements.txt     — empty or minimal
  ```

For ALL scaffolds, also generate:
- **README.md** — project name, one-sentence description from interview, "## Getting Started" with setup instructions
- **.gitignore** — appropriate for the language (use standard templates)
- **CLAUDE.md** — initial project context:
  ```markdown
  # {Project Name}

  ## What This Is
  {one-sentence description from interview}

  ## Stack
  {language/framework chosen}

  ## Status
  Brand new project — scaffolded by Spark /init.
  ```

**Step 3 — Initialize git**

If not already a git repo:
1. `git init`
2. `git add -A`
3. `git commit -m "Initial scaffold from Spark /init"`

If already a repo but scaffold created new files:
1. `git add -A`
2. `git commit -m "Add initial project scaffold from Spark /init"`

**Step 4 — Continue with normal flow**

Now there are files to discover. Proceed to **Phase 1** (Discovery) and continue through the standard init sequence.

---

## Phase 1 — Discovery (parallel agents)

Spawn 4 parallel Explore agents:

1. **Structure agent**: "Scan directory structure. Identify languages, frameworks, package managers, build tools. List key directories and their purposes. Return structured summary."
2. **Docs agent**: "Find documentation files (README, CONTRIBUTING, docs/, wiki/, *.md). Summarize project purpose, conventions, and any documented rules. Return structured summary."
3. **Git agent**: "Analyze git history (if exists). Identify branching model, commit message conventions, active contributors, recent activity patterns. Return structured summary."
4. **Config agent**: "Find config files (CI/CD, Docker, linters, formatters, env files). Identify deployment targets, environments, test frameworks. Return structured summary."

## Phase 2 — Profile (synthesize)

Merge agent summaries into a draft project profile. Present to the human:

```
## Project Profile (Draft)

**Type**: {web app | CLI tool | library | documentation | infrastructure | mixed}
**Stack**: {languages, frameworks, key tools}
**Structure**: {monorepo | single-app | microservices | flat}

**Suggested Roles**:
- backend: {description based on what was found}
- frontend: {description based on what was found}
- {others as discovered}

**Conventions Found**:
- {commit style, branching, test patterns, etc.}

**Key Paths**:
- Source: {path}
- Tests: {path}
- Config: {path}
- Docs: {path}

Does this look right? What should I add or change?
```

Wait for human confirmation or adjustments.

## Phase 3 — Interview (targeted questions)

Only ask what discovery couldn't figure out:
- What's the primary goal for this project? (if not obvious)
- Any constraints? (don't touch X, always do Y)
- Workflow preferences? (commit style, autonomy level, review process)
- What should I call you? (for personalized communication)

## Phase 4 — Scaffold

1. Create `.claude/` directory structure
2. Write `spark.md` with project-specific rules merged into framework
3. Write `reference/project-profile.md` (generated profile)
4. Write role profiles in `roles/` based on discovered/declared roles
5. Create empty `session/handoff.md`, `session/questions.md`
6. Create `jobs/INDEX.md` (empty, ready for work)
7. Output:

```
Spark initialized.

Project: {name}
Roles: {list}
Profile: .claude/reference/project-profile.md

Ready to work. Give me a job, a setlist, or say "what should we do first?"
```

## Phase 5 — Seed Context

After scaffolding completes, automatically run a git-only harvest to seed initial context files:

1. Ensure `.claude/context/` directory exists (`mkdir -p`)
2. Execute the `/harvest git` procedure — harvest from git history only (no external tools needed)
3. This populates `.claude/context/` with `project-decisions.md`, `recent-activity.md`, `team-conventions.md`, and `current-sprint.md` based on commit history
4. If git history is empty (brand new repo), write the template files with "No data yet" placeholders — context will populate on the next `/harvest` after work begins
5. Do not prompt the user — this runs silently as part of init

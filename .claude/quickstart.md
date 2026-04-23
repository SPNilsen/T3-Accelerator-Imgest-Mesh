# Spark — Quick Start

Get running in under 5 minutes.

## 1. Clone Spark (once, keep it permanently)

**Mac / Linux:**
```bash
git clone https://github.com/SPNilsen/Claude-Spark.git ~/spark
```

**Windows:**
```cmd
git clone https://github.com/SPNilsen/Claude-Spark.git %USERPROFILE%\spark
```

This is your local source of truth for the framework. Don't delete it — updates and contributions flow through it.

## 2. Install into your project

**Mac / Linux:**
```bash
cd ~/your-project
~/spark/install.sh
```

**Windows (no Git Bash required):**
```cmd
cd C:\Users\you\your-project
node %USERPROFILE%\spark\install.js
```

That's it. Your project now has a `.claude/` directory with session state, job tracking, and bus scaffolding. The framework engine stays in the Spark repo.

> **Updating later:** Pull the latest in your Spark clone, then run `~/spark/update.sh` (or `node %USERPROFILE%\spark\update.js` on Windows) from your project. Only framework files update — your jobs, roles, and session state are never touched.

## 3. Choose your mode & launch

Pick **dashlite** (default, no CLI needed) or **dashfull** (persistent Dispatcher, requires CLI):

```bash
cd ~/spark && git checkout dashlite && claude
> Working on ~/your-project. Fresh start.
```

> `main` is identical to `dashlite` — if you're already on main, you're running Dash Lite. Use `git checkout dashfull` for Dash Full.

Spark scans your project, asks a few questions about your workflow, and configures itself. Takes about 2 minutes.

## 4. Give it work

```
> Spark, plan a job for [describe what you want built]
```

Spark writes a job plan with acceptance criteria. Review it, then:

```
> Spark, dispatch job-1
```

An autonomous agent picks up the work. Check progress anytime:

```
> Spark, status
```

## 5. End your session

```
> Spark, /wrap
```

Spark saves everything. Next time, just say:

```
> Spark, go
```

It picks up exactly where you left off.

---

## What's next

- **Multiple jobs?** Create a setlist: `Spark, plan a setlist for [feature]`
- **Want tests first?** Use contract-first: `Spark, spec job-1`
- **Team project?** Each dev runs their own session — jobs and roles are shared via git
- **Full docs:** Read `tutorial.md` in the Spark repo (`~/spark/tutorial.md`)

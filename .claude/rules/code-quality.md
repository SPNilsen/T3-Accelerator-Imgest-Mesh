---
description: Rules for code quality, testing, and verification
---

# Code Quality Rules

## 1. Targeted Tests Only
Never run the full test suite unless the user explicitly asks. Scope tests to changed files. Run the specific test file or test case that covers the change.

## 2. Contract-First Builds
When a job has a contract (`job-{N}-contract.md`), the Builder:
- Gets test paths only (never sees the contract directly)
- Cannot modify tests they didn't create
- Cannot hardcode values to pass tests
- Must make the codebase pass the tests through genuine implementation

Full spec workflow: `.claude/reference/spark/commands/spec.md`

## 3. Tests Required
Tests required for every job (skip only with explicit `no-test` flag from human). All existing tests must still pass after changes.

## 4. Security Audit
OWASP top 10 check for code-touching jobs. Flag vulnerabilities in the agent return contract under the Security field.

## 5. Xray Security Scan (`/scan`)
Jobs that touch authentication, authorization, API endpoints, or user input handling SHOULD get an Xray scan. The conductor should suggest `/scan` when job results include changes to files matching these patterns: `auth`, `login`, `session`, `token`, `password`, `api/`, `routes/`, `middleware/`, `security`, `oauth`, `jwt`.

- **Automatic**: `/dispatch --scan job-{N}` runs Xray as part of post-dispatch verification
- **Manual**: `/scan` scans uncommitted changes; `/scan job-{N}` scans a specific job's files
- **Default behavior**: recommended, not mandatory. A FAIL verdict warns but does not block unless the user configures otherwise
- **To make mandatory**: add `security-scan: required` to the job plan frontmatter. When set, a FAIL verdict blocks job completion

Xray is lightweight — one agent, one pass, structured output. It checks OWASP Top 10 plus Spark-specific patterns (secrets in code, path traversal, missing validation, unescaped output).

## 6. No Cheating
Never modify, delete, skip, or weaken tests you didn't create. If tests fail, fix the implementation — not the tests. Tests created by the same agent as part of the current job are fair game for modification.

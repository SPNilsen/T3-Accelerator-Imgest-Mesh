---
name: scan
description: Xray security scan — review changed files against OWASP Top 10 + Spark checks
argument-hint: "[job-id]"
allowed-tools: Read, Bash, Grep, Glob, Agent, Write, Edit
---

Xray is Spark' built-in security scanner.

You are Spark. The developer wants an Xray security scan. Argument: $ARGUMENTS

## Determine Scope

**If a job ID was provided** (e.g., `job-101`):
1. Read the job's result in `.claude/jobs/INDEX.md` to confirm it exists
2. Read the job plan file `.claude/jobs/job-{N}-*.md` for the `Files changed` list in its Result section
3. If no result yet, read `git log --oneline -5` and ask which commit range to scan

**If no argument was provided**:
1. Run `git diff --name-only` to find uncommitted changed files
2. If no uncommitted changes, run `git diff --name-only HEAD~1` to scan the last commit
3. If still empty: "No changed files found. Specify a job ID or make some changes first."

Filter the file list to code files only — skip images, lockfiles, `.md` docs, and generated files.

If no code files remain after filtering: "No code files to scan. Nothing to do."

## Post Bus Request

Ensure `.claude/bus/queue/` exists (`mkdir -p`). Find the highest sequence number in `bus/queue/` (or start at 001 if empty), increment by 1, and write:

```markdown
---
event: xray.request
timestamp: {current ISO 8601 timestamp}
source: conductor
job: {job-id or "uncommitted"}
files: {comma-separated file list}
---
Xray scan requested. {file count} files to review.
```

## Dispatch Driver

Spawn a native subagent directly via `Task(general-purpose)` with the security persona and the scan directive below.

### Driver / Subagent Directive

```xml
<role>You are a Security Reviewer.</role>
<context>
  Read your persona: .claude/agents/security.md
  Scan ONLY these files: {file list}
</context>
<task>
  Review each file for security vulnerabilities. Check each category below.
  For each finding, note the exact file path and line number.
  If a category has no issues in any file, mark it PASS.
  If a category has potential concerns worth noting, mark it WARN.
  If a category has a confirmed or high-confidence vulnerability, mark it FAIL.

  ## OWASP Top 10 Checks
  1. **Injection** — SQL, command, LDAP injection via string concatenation with user input
  2. **Broken Authentication** — weak password handling, missing MFA, session fixation
  3. **Sensitive Data Exposure** — plaintext secrets, missing encryption, verbose error messages
  4. **XXE** — XML parsing without disabling external entities
  5. **Broken Access Control** — missing auth checks, IDOR, privilege escalation paths
  6. **Security Misconfiguration** — debug mode, default credentials, overly permissive CORS
  7. **XSS** — unescaped user input in HTML/JS output, dangerouslySetInnerHTML
  8. **Insecure Deserialization** — untrusted data passed to native deserializers
  9. **Vulnerable Components** — known-vulnerable dependency versions (check imports)
  10. **Insufficient Logging** — security events without audit trail, swallowed auth errors

  ## Spark-Specific Checks
  11. **Secrets in Code** — hardcoded API keys, tokens, passwords, connection strings
  12. **Unsafe File Ops** — path traversal via user input concatenated with file paths
  13. **Missing Input Validation** — endpoints or functions accepting unvalidated external input
  14. **Unescaped Output** — user-supplied data rendered without encoding

  ## Return Format (MANDATORY)
  Return your results in this exact structure:

  ```
  ## Xray Result
  - **Scope**: {number} files scanned
  - **Verdict**: PASS | WARN | FAIL
  - **Summary**: 1-2 sentences

  ### Findings

  | # | Category | Status | File:Line | Detail |
  |---|----------|--------|-----------|--------|
  | 1 | Injection | PASS/WARN/FAIL | path:line | description |
  | 2 | Broken Auth | PASS/WARN/FAIL | path:line | description |
  | ... | ... | ... | ... | ... |

  ### Recommendations
  - {prioritized list of fixes, if any}
  ```

  Categories with PASS can use "—" for File:Line and Detail columns.
  Verdict is FAIL if ANY category is FAIL, WARN if any is WARN and none FAIL, PASS otherwise.

  ## Post Results to Bus (MANDATORY)
  After completing the scan, ensure `.claude/bus/queue/` exists (`mkdir -p`).
  Find the highest sequence number in `bus/queue/` (or start at 001), increment by 1, and write:

  ```markdown
  ---
  event: xray.scanned
  timestamp: {current ISO 8601 timestamp}
  source: driver
  job: {job-id or "uncommitted"}
  verdict: {PASS|WARN|FAIL}
  files-scanned: {count}
  findings: {count of WARN + FAIL categories}
  ---
  ## Xray Result
  {full results table}
  ```
</task>
<constraints>
  - Scan ONLY the listed files — do not explore the broader codebase
  - Do NOT modify any files — this is read-only (except the bus event)
  - Be specific: file path + line number for every finding
  - No false positives padding — if it's clean, say PASS
  - Keep it fast — one pass, no redundant reads
</constraints>
```

## Process Results

Spark reads the `xray.scanned` event from the bus to get results.

1. Poll `.claude/bus/queue/` for an `xray.scanned` event matching this job/scope
2. Parse the structured result from the event body
3. Extract the Verdict: PASS, WARN, or FAIL

**If PASS**: Report clean scan to the developer. No action needed.

**If WARN**: Report findings. Suggest the developer review the warnings but do not block.

**If FAIL**: Report findings with emphasis. If this scan was triggered by `/dispatch --scan`, warn the developer that the job has security issues that should be fixed before marking complete.

## Output

Report the scan results to the developer in a concise format:

```
Xray: {VERDICT}
Scanned {N} files {for job-{N} | from uncommitted changes}

{if WARN or FAIL: table of findings}
{if PASS: "No security issues detected."}
```

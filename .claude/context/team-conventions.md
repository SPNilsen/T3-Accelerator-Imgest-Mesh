# Team Conventions (seeded from git)

## Commit style
**Conventional commits** (adopted 2026-04-21 by Sean). Format: `type(scope): subject`.
- Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `build`, `ci`, `perf`, `style`
- Example: `feat(webserver): add /healthz endpoint`
- Historical commits by Douglas use plain action-verb style (`mod webserver`, `add webserver`) — leave as-is, do not rewrite

## Branching
Model: `main` / `test` / `dev` / `[feature-name]`
- `main` — production; promote from `test` only
- `test` — staging / QA; promote from `dev`
- `dev` — integration branch; feature branches merge here
- `[feature-name]` — short-lived, branches off `dev`, merges back to `dev`

Do NOT branch features off `main` or `test`.

## Merge strategy
**Always `--no-ff`.** Never fast-forward any merge. The branch topology must remain visible in the commit graph so we can see which commits shipped together as a unit.

Example: `git merge --no-ff feature/local-dev-compose` (from `dev`).

## Approval gate
Merges require Sean's explicit approval. Commits can proceed without asking; merges cannot.

**Each promotion up the branch chain is its own approval.** An approval to merge `feature/x → dev` does NOT authorize the onward `dev → test` merge — ask again. `test → main` is a third, separate ask. Default stop point is `dev`.

## Read-only areas
- `docs/armor/` — ARMOR / ALI (J&J Vistakon) case study. Reference material only; do not edit.

## Review process
Not yet formalized. Assume PRs into `dev` will use conventional-commit titles as PR titles.

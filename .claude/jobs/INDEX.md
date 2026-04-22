# Jobs Index

Format: `| ID | Title | Assigned | Status | Branch | SP |`

| ID | Title | Assigned | Status | Branch | SP |
|---|---|---|---|---|---|
| job-1 | Local dev environment on Windows (understand + run all services) | Sean | in-progress | feature/local-dev-compose | 6 |
| job-2 | Cisco AI Pod demo prep (K8s manifests + GPU + real inference) | Sean | not-started | feature/cisco-demo-manifests | 8 |

## Status values
- `not-started` — in queue
- `in-progress` — being worked
- `blocked` — waiting on answer or external dep
- `done` — merged / shipped

## Notes
- `job-1` bundles codebase walkthrough with actually getting services running — the walkthrough is a means, not a deliverable
- Deadline for Cisco demo: 2026-05-20
- All feature branches off `dev` (needs to be created from `main` first)

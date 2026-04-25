# Jobs Index

Format: `| ID | Title | Assigned | Status | Branch | SP |`

| ID | Title | Assigned | Status | Branch | SP |
|---|---|---|---|---|---|
| job-1 | Local dev environment on Windows (understand + run all services) | Sean | done | feature/local-dev-compose | 6 |
| job-2 | Cisco AI Pod demo prep (K8s manifests + GPU + real inference) | Sean | not-started | feature/cisco-demo-manifests | 8 |
| job-3 | Dashboard pipeline flow animation — traveling bubble on progress line | Sean | done | feature/pipeline-flow-animation | 3 |
| job-4 | MkDocs site as a standalone container + dashboard link (new tab) | Sean | done | feature/mkdocs-container | 4 |
| job-5 | Linked JNJ-Armor docs container — surface customer docs alongside generic platform docs | Sean | not-started | feature/jnj-armor-docs-container | 4 |

## Status values
- `not-started` — in queue
- `in-progress` — being worked
- `blocked` — waiting on answer or external dep
- `done` — merged / shipped

## Notes
- `job-1` bundles codebase walkthrough with actually getting services running — the walkthrough is a means, not a deliverable
- Deadline for Cisco demo: 2026-05-20
- All feature branches off `dev` (`dev` and `test` now exist on origin)
- `job-3` feature branch cut from `dev` after `job-1` landed there

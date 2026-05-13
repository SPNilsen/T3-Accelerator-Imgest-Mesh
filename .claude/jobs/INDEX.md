# Jobs Index

Format: `| ID | Title | Assigned | Status | Branch | SP |`

| ID | Title | Assigned | Status | Branch | SP |
|---|---|---|---|---|---|
| job-1 | Local dev environment on Windows (understand + run all services) | Sean | done | feature/local-dev-compose | 6 |
| job-2 | Cisco AI Pod demo prep (K8s manifests + GPU + real inference) | Sean | done | feature/cisco-demo-manifests | 8 |
| job-9 | Cisco AI Pod demo runbook | Sean | done | feature/cisco-demo-runbook | 3 |
| job-3 | Dashboard pipeline flow animation — traveling bubble on progress line | Sean | done | feature/pipeline-flow-animation | 3 |
| job-4 | MkDocs site as a standalone container + dashboard link (new tab) | Sean | done | feature/mkdocs-container | 4 |
| job-5 | Linked JNJ-Armor docs container — surface customer docs alongside generic platform docs | Sean | done | feature/jnj-armor-docs-container | 4 |
| job-6 | Dashboard column layout + per-service detail panels (offline-safe) | Sean | done | feature/dashboard-grid-layout | 5 |
| job-7 | Per-directory storage retention — max 20 frames across all pipeline stages | Sean | done | feature/storage-retention | 3 |
| job-8 | Panel change indicators — cross-fade on content update | Sean | done | feature/panel-change-indicators | 2 |

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

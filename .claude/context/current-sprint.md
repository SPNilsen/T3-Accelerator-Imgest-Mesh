# Current Sprint / Focus

## Sean's priorities (2026-04-21)
1. **Understand the codebase** — walkthrough of the four services + how they connect
2. **Run it on Windows 11** — Docker Desktop (or WSL2) + CPU-only / mock inference mode
3. **Demo on Cisco AI Pod** — K8s manifests for all services + NVIDIA GPU scheduling

## Active jobs
See `.claude/jobs/INDEX.md`:
- `job-1` Local dev on Windows, walkthrough folded in (6 SP) — not-started
- `job-2` Cisco AI Pod demo prep (8 SP) — not-started

**Reordered on 2026-04-21:** local dev first; codebase understanding happens as part of wiring the compose file rather than as a separate deliverable.

## Hard deadline
**Cisco AI Pod demo: 2026-05-20** (29 days from 2026-04-21).

## Notes
- job-2 will likely need to produce a docker-compose.yml (doesn't exist)
- job-3 will need K8s manifests for camera/orchestrator/inference (only webserver has them today)
- Inference-service GPU strategy + missing manifests are on the critical path for the demo
- Local Windows run (job-2) is a learning step, not on the demo critical path — don't over-invest

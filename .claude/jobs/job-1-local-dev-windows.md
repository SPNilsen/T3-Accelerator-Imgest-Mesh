---
id: job-1
title: Local dev environment on Windows (understand + run all services)
assigned: Sean
status: in-progress
branch: feature/local-dev-compose
base-branch: dev
sp: 6
deadline: 2026-05-20 (rolls up to Cisco demo)
security-scan: optional
---

# Job 1 — Local dev environment on Windows

## Goal
Sean can clone, build, and run the full Imgest-Mesh pipeline (camera → orchestrator → inference → webserver) on his Windows 11 machine, hit a UI / API endpoint, and see an image flow end-to-end. CPU-only; no GPU required locally.

## Why this first
Sean is new to the project. Wiring the services together locally is the fastest path to understanding how they connect — you can't write a compose file without reading each service's config, entrypoint, and ports. Understanding emerges from the work.

## Scope
In:
- Read each service (`camera`, `orchestrator`, `inference`, `webserver`) deeply enough to know its config, ports, inputs, outputs
- Document the wiring in `.claude/reference/wiring/local-dev.md` as we go
- Produce a `docker-compose.yml` at repo root that runs all four services
- Produce `.env.example` for any required env vars
- Add a CPU-only or mock inference path so the stack runs without NVIDIA on Windows
- Smoke-test end-to-end: feed a sample image, see it pass through to a pass/fail result
- README section: "Running locally on Windows"

Out:
- K8s manifests for non-webserver services (→ job-2)
- Real GPU inference (→ job-2)
- CI/CD pipeline (separate job later)
- Anything under `docs/armor/` (read-only)

## Acceptance criteria
1. `docker compose up` on Windows (Docker Desktop or WSL2) starts all four services without errors
2. A documented smoke-test procedure produces a visible pass/fail result
3. `.claude/reference/wiring/local-dev.md` exists and describes how the services connect
4. README updated with local-dev instructions
5. Commits follow conventional-commits format
6. Feature branch `feature/local-dev-compose` off `dev`, PR ready for review

## Risks
- Inference service may pull GPU-only dependencies (torch+cuda, onnxruntime-gpu) — need CPU fallback strategy
- No sample images checked in — may need to generate or bundle a tiny test asset
- Windows path / line-ending issues in volume mounts
- Compose networking between services (DNS between containers)

## Questions to answer before starting
See next Spark reply — batched for Sean.

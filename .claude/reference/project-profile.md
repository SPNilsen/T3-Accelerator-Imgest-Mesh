# Project Profile — T3-Accelerator-Imgest-Mesh

## What this is
**Imgest-Mesh** is Trace3's containerized machine-vision inference accelerator for Industry 4.0 manufacturing. It ingests camera images, runs GPU-accelerated AI inspection models, and emits pass/fail decisions.

## Deployment target
- **Reference platform:** Cisco AI Pod + Red Hat OpenShift, NVIDIA GPUs
- **Portable to:** vanilla Kubernetes, on-prem GPU clusters, hybrid/cloud
- **Container standard:** OCI (Containerfile, runnable under Docker or Podman)

## Architecture — microservice pipeline
```
Camera → Orchestrator → Inference → Webserver (UI / results)
```

| Service | Stack | Path | Exposes |
|---|---|---|---|
| **camera** | Python FastAPI | `resources/camera/` | image ingestion/capture |
| **orchestrator** | Python FastAPI | `resources/orchestrator/` | routing, watcher |
| **inference** | Python FastAPI | `resources/inference/` | GPU model worker |
| **webserver** | nginx (Alpine unprivileged) | `resources/webserver/` | port 8080, SPA static |

## Kubernetes / OpenShift
- Manifests live under `resources/k8s/` (currently only `webserver/`)
- Uses OpenShift `route.openshift.io/v1` Route (no TLS yet)
- Image registry: `registry.gitlab.com/dosayles/t3-imgest-mesh/*`

## Documentation — MkDocs Material
Heavy domain-knowledge content under `docs/`:
- `docs/t3/` — project management, FAQ, glossary, activity blog
- `docs/crisp-dm/` — data science methodology
- `docs/hpc/` — cluster, K8s/SLURM, GPU ops
- `docs/armor/` — ARMOR/ALI case study (Johnson & Johnson Vistakon contact-lens inspection)
- `docs/db/`, `docs/dl/`, `docs/gen/` — reference material

Also supports Pandoc-based PDF generation (see `README-pandoc.md`).

## Conventions
- **Commits:** plain action-verb style (`mod webserver`, `add webserver`) — not conventional commits
- **Branches:** only `main` exists so far; no tags
- **Tests:** none present yet — gap to fill before first real build
- **CI/CD:** none checked in — GitLab registry implied

## People
- Original author: Douglas Sayles (all 20 commits, Mar 9–11 2026)
- Current developer: Sean Nilsen (snilsen@auraai.ai), onboarded 2026-04-21

## Gaps identified
1. README describes `containers/ingest/preprocess/decision` layout; reality is `resources/{camera,orchestrator,inference,webserver}` — README slightly drifted
2. Only webserver has K8s manifests — camera/orchestrator/inference manifests missing
3. No local dev orchestration (no docker-compose.yml, no Makefile, no Tiltfile)
4. Inference service GPU strategy unclear — need CPU-only dev mode for Windows laptop
5. No tests, no CI

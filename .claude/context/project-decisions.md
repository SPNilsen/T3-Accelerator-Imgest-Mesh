# Project Decisions (seeded)

## Hard constraints (from Sean, 2026-04-21)
- **Cisco AI Pod demo deadline: 2026-05-20** — 29 days out
- **Conventional commits** required going forward
- **Branch model:** `main` / `test` / `dev` / `[feature-name]`
- **`docs/armor/` is read-only** until Sean has studied it

## Already decided (from README + code)
- **Reference deployment:** Cisco AI Pod + Red Hat OpenShift + NVIDIA GPUs
- **Container standard:** OCI (Containerfiles, runnable under Docker or Podman)
- **Microservice split:** camera / orchestrator / inference / webserver (not the `ingest/preprocess/decision` split in the README — README is stale)
- **Registry:** GitLab (`registry.gitlab.com/dosayles/t3-imgest-mesh/*`)
- **Webserver:** Alpine nginx-unprivileged, port 8080, OpenShift Route (no TLS yet)
- **Docs tooling:** MkDocs Material + Pandoc/LaTeX pipeline

## Not yet decided
- Local dev orchestration (docker-compose? Tilt? Minikube? OpenShift Local?)
- Inference GPU-vs-CPU dev mode strategy
- Model artifact distribution (bundled, ConfigMap, object store?)
- TLS on the OpenShift Route
- CI/CD pipeline (GitLab CI implied but no `.gitlab-ci.yml` yet)
- Test framework choice (pytest is the Python-community default; not yet adopted here)

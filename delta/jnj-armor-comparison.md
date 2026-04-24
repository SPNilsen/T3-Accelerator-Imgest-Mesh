# Delta — T3-Accelerator-JNJ-Armor vs. T3-Accelerator-Imgest-Mesh

**Question:** Is `T3-Accelerator-JNJ-Armor` just the docs from this project, or is it fundamentally different?

**Answer:** Fundamentally different. JNJ-Armor is a customer-specific **R + Python data-science delivery project** for Johnson & Johnson MedTech that *reuses Imgest-Mesh's documentation framework* as scaffolding. Imgest-Mesh is a reusable **containerized microservice accelerator** for generalized manufacturing inspection.

The docs they share are a surface overlap. Everything below the docs is different.

---

## Intent — per READMEs

| | Imgest-Mesh | JNJ-Armor |
|---|---|---|
| One-line self-description | "Containerized accelerator for deploying scalable machine-vision inference pipelines in modern manufacturing" | "Framework for Project Armor — data processing, feature engineering, model training, and performance evaluation" |
| Deployment target | Cisco AI Pod + Red Hat OpenShift (GPU Kubernetes) | GitLab Pages (docs) + analyst workstations (R / Python) |
| Customer context | Generic Industry-4.0 reference | Johnson & Johnson MedTech — Automatic Lens Inspection (contact lenses, ~100 production lines) |
| Kind of asset | Reusable accelerator / reference architecture | Customer delivery + model-development workbench |

---

## Repo inventory — shape at a glance

| Top-level item | Imgest-Mesh | JNJ-Armor |
|---|---|---|
| `docs/` | Large Material site (armor, crisp-dm, hpc, t3, dev, workshop, etc.) | Similar Material site, customer-customized |
| `resources/` | 5 service containers (camera, orchestrator, inference, webserver, docs) | — |
| `docker-compose.yml` | Yes — 5-service pipeline | No |
| `src/` | — | 139 files — R (.R/.Rmd) + Python model dev |
| `notebooks/` | — | 2 Jupyter notebooks + a pipeline script |
| `scripts/` | — | Python utilities (JSON fixing, Dataloop image retrieval) |
| `dataloop/` | — | Dataloop.ai annotation platform integration (bundled venv) |
| `data/` | — | Tracked data incl. a **43 MB trained Detectron2 model** |
| `output/` | — | Generated artifacts directory |
| `project-armor.Rproj` | — | RStudio project file |
| `Dockerfile-websvr-docs` | — | 3-line nginx:alpine serving pre-built MkDocs |
| `Containerd-docs` | — | Alternative MkDocs build spec |
| `mkdocs.yml` | `site_name: Imgest-Mesh` | `site_name: J&J MedTech Project Armor` |

**Shape summary:** Imgest-Mesh is a **containerized pipeline** with its docs alongside. JNJ-Armor is a **data-science codebase** with docs alongside. The docs are the only structural overlap.

---

## Docs overlap — roughly 70% structural reuse

Both sites share the CRISP-DM skeleton (`business-understanding`, `data-understanding`, `data-preparation`, `modeling`, `evaluation`) and a common Material theme + plugin set. But the content diverges in two ways:

**Customer-specific rewrites of shared files.** Overlapping filenames are NOT byte-identical:

- `docs/crisp-dm/business-understanding.md` — Imgest-Mesh references "Vistakon's" (J&J's former lens brand); JNJ-Armor references "Johnson & Johnson MedTech" (the current brand). Same file path, different customer framing.
- `docs/armor/background.md` — same naming-swap divergence.

**JNJ-Armor has extra docs pages Imgest-Mesh lacks:**

- `armor/data-mining-goals.md`
- `armor/inventory-resources.md`
- `armor/project-plan.md`
- `crisp-dm/additional.md`
- `crisp-dm/lessons-learned.md`

These are customer-engagement artifacts (project plan, resource inventory, post-mortem lessons) — the kind of thing a delivery project accumulates that a reusable accelerator does not.

**Nav differences:** JNJ-Armor adds a top-level "Models" entry; Imgest-Mesh doesn't.

> **Caveat on the 70% figure** — this is the survey agent's estimate based on folder overlap and spot-checked file comparisons, not a byte-level diff. Treat it as a ballpark, not an audit result.

---

## Unique to JNJ-Armor — what Imgest-Mesh does not have

### R analytical stack (no R in Imgest-Mesh)
- `src/functions.R` — ~250 lines of utility functions (redaction, tibble manipulation)
- `src/build-threshold-matrix.R`, `build-defect-thresholds-data.Rmd` — defect-threshold engineering
- `src/create-pass-fail-dataset-fixed.R` — training data creation
- `src/classifier-dev-report.Rmd`, `classifier-dev-report2.Rmd` — RMarkdown model-iteration reports
- `src/ingest-annotations.Rmd` — annotation processing
- `.Rhistory` (27 KB) — live R session history committed to the repo
- **Total: 45+ .R / .Rmd files**

### Python model development (JNJ-Armor only)
- `src/ng/` ("next gen") directory — 115+ scripts
  - `anchor_analysis.py`, `check_coco_bboxes.py` — COCO dataset validation
  - `bak/ng_stg1_train.py`, `bak/ng_stg2_train_yolox.py` — staged training pipelines for Detectron2 and YOLOX
- `notebooks/01-notebook.ipynb`, `notebooks/02-notebook.ipynb` — exploratory analysis
- `notebooks/pass_fail_annotation_pipeline.py` — annotation processing pipeline
- `scripts/Fix_JSON_Names.py` (~469 lines)
- `scripts/Image_Retrieval.py` (~3,263 lines)

Imgest-Mesh has no notebooks, no R, and no model-training code. Its `inference` service is ~60 lines of mock logic with a `worker.py` swap point.

### Data assets tracked in git
- `data/models/goodtimesbadtimes-1k-2025.04.06-model_final.pt` — **43 MB** Detectron2 weights
- `data/models/*.json` — metrics and config
- `dataloop/annotations.json` — Dataloop.ai annotation exports
- **~50 MB of tracked data total** (Imgest-Mesh tracks none)

### External tool integration
- `dataloop/dloop/.venv/` — a bundled Python virtualenv for the Dataloop CLI (`dlp` binary)
- `dataloop/src/utils.py` — ~2,972 lines of Dataloop utilities

Imgest-Mesh has no annotation-platform integration.

---

## Container strategy — different problems, different shapes

**Imgest-Mesh — production pipeline:**
- `docker-compose.yml` orchestrates 5 services: camera (`:8081`), orchestrator (`:8082`), inference (`:8083`), webserver (`:8080`), docs (`:8000`)
- Each service has its own `Containerfile` (OCI-neutral naming)
- File-system bind mounts (`./.data/frames/` → `.data/routed/` → `.data/results/`) are the wire protocol between stages
- Healthchecks, `depends_on`, `restart: unless-stopped` baked in — shape mirrors Kubernetes manifests

**JNJ-Armor — just serve the docs:**
- `Dockerfile-websvr-docs` — 3 lines: `FROM nginx:alpine`, copy `site/` into `/usr/share/nginx/html`. That's it.
- `Containerd-docs` — a separate spec that *builds* the MkDocs site (installs ~7 plugins).
- No compose file. No multi-service orchestration. Deployment is ad-hoc (GitLab Pages + the nginx container for previews).
- `.gitlab-ci.yml` exists (~783 bytes) for docs publishing, not for a service pipeline.

The mkdocs container *shape* is similar to Imgest-Mesh's new `resources/docs/Containerfile` (both multi-stage: build → serve). Functionally, JNJ-Armor only ships docs; Imgest-Mesh ships docs *plus* a four-service inference pipeline.

---

## Git activity — active delivery vs. mature accelerator

| | Imgest-Mesh | JNJ-Armor |
|---|---|---|
| Commits on default branch | 34 | 156 |
| Recent activity | Documentation sync, infra updates | Model iteration, annotation refinement, CSS styling, Dataloop integration |
| Feature branches | Focused (`local-dev-compose`, `pipeline-flow-animation`, `mkdocs-container`) | Ongoing (`feature/das-css-styling-adj`, `feature/das-new-logic`, etc.) |
| State | Stable / mature reference | Active customer engagement |

Roughly 5× the commit volume on JNJ-Armor signals it's a live, customer-driven work stream; Imgest-Mesh is a stabilized accelerator.

---

## Implications for Imgest-Mesh — what to take from this

1. **Imgest-Mesh's `docs/armor/` is a derivative of JNJ-Armor's customer content.** This is the probable origin of the read-only constraint on that directory (`feedback_armor_readonly.md`). The authoritative source lives in JNJ-Armor; edits here would desync.
2. **The missing `armor/models.md` nav entry** (the 404 surfaced during job-4 smoke-testing) points at a JNJ-Armor page that didn't get copied over when the docs were forked. Fixing it cleanly means either copying the file from JNJ-Armor or removing it from `mkdocs.yml` nav — a content decision for Sean + Doug, not a container issue.
3. **Model / training code is out of scope for Imgest-Mesh.** If the Cisco demo needs a real model, the training pipeline lives in JNJ-Armor; Imgest-Mesh's job is to *serve* whatever `.pt` artifact gets exported from there via its mock→real swap path in `resources/inference/app/worker.py`.
4. **Don't treat JNJ-Armor as an upstream to pull from blindly.** The docs share scaffolding but the customer framing is different (MedTech vs. generic). Selective copy, not merge.

---

## Caveats on this assessment

- Survey conducted by a read-only Explore agent over one pass; no independent byte-level diff, no `git log --numstat` rollup, no line-counting audit.
- File counts, line counts, and the "~70% overlap" figure are approximations from spot-checked evidence, not exhaustive totals.
- Treat this as an orientation document, not as ground truth for delivery planning. If a specific claim matters for a decision, verify it directly before acting.

---

*Generated on `dev`, uncommitted. Source: Explore-agent survey of `C:\c\t3\T3-Accelerator-JNJ-Armor` + existing knowledge of `T3-Accelerator-Imgest-Mesh`.*

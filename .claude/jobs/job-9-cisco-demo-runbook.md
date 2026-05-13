---
id: job-9
title: Cisco AI Pod demo runbook
status: done
branch: feature/cisco-demo-runbook
base-branch: dev
assigned: Sean
sp: 3
security-scan: not-required
deadline: 2026-05-20
depends-on: job-2
---

# Job 9 — Cisco Demo Runbook

## Why

Job 2 delivers the technical migration. Job 9 delivers the human layer:
what to set up before the room fills, what to click through during the
demo, what to say at each beat, and how to recover if something breaks.
A runbook lives in `docs/` so it renders in the MkDocs site alongside the
project documentation — no separate slide deck needed.

## Deliverables

### `docs/runbook/cisco-demo.md`

A single structured markdown document with these sections:

#### 1. Pre-demo setup checklist (T-30 minutes)
- Verify K8s pods are running (`kubectl get pods -n imgest-mesh`)
- Confirm GPU allocation on inference pod
- Open browser tabs: dashboard (webserver NodePort), Docs, JNJ-Armor Docs
- Confirm bmp-input images are seeded in the cluster PVC
- Smoke test: watch one frame flow through camera → orchestrator → inference
  and appear in the dashboard
- Have fallback ready: Docker Compose stack on local laptop

#### 2. Demo narrative (talking track)
A paragraph-per-beat script with what to show on screen and what to say.
Beats:
1. **Problem statement** — JNJ contact lens manufacturing, defect detection
   at scale, why AI inference in the pipeline matters
2. **Architecture overview** — point at the pipeline bubbles, explain the
   5-stage mesh (camera → orchestrator → inference → webserver → docs)
3. **Live pipeline** — watch the dashboard update, explain what each panel
   shows (camera feed thumbnail, orchestrator routing, inference verdict)
4. **Real inference** — explain that the model is the actual Detectron2
   model trained on JNJ lens defect data, running on A100 GPU
5. **Model lineage** — briefly show JNJ-Armor Docs tab (the model's origin)
6. **Platform extensibility** — "swap any service, add new stages, GPU
   optional — same mesh"

#### 3. Live demo click-through
Step-by-step with exact URLs and expected outcomes:
1. Open `http://<NodePort>/` → show header, pipeline, panels
2. Point out thumbnail cycling through source images
3. Point out inference panel updating with verdict + confidence
4. Click a pipeline bubble → show /status JSON
5. Open Docs tab → show MkDocs site
6. Open JNJ-Armor Docs tab → show customer-facing docs

#### 4. Q&A prep
Anticipated questions with suggested answers:
- "How long did the model take to train?"
- "What's the accuracy / false positive rate?"
- "Can this run on our own hardware?"
- "How does it handle new defect categories?"
- "What's the latency from camera to verdict?"

#### 5. Recovery playbook
| Symptom | Likely cause | Fix |
|---|---|---|
| Inference pod not ready | Engine not mounted | Check PVC, re-apply deploy |
| Dashboard blank panels | Service not reachable | Check NodePort, CORS |
| Thumbnail not updating | Camera bmp-input empty | Re-seed PVC |
| GPU not allocated | Node selector mismatch | Check node labels |
| Full fallback | Any cluster issue | Start local Docker Compose |

### `docs/runbook/setup-cluster.md`

Cluster setup reference for whoever preps the environment:
- Namespace creation
- PVC seeding (copy bmp-input BMPs + thumbnails)
- Model engine placement (PVC or init container)
- Image pull (registry + credentials)
- `kubectl apply -k k8s/` walkthrough
- Verification commands

## Acceptance criteria

- Both markdown files render correctly in the MkDocs site (no broken links,
  tables display, code blocks format)
- Demo narrative covers all 6 beats
- Recovery playbook covers at least 5 failure scenarios
- Setup guide is self-contained — someone who didn't build the system can
  follow it

## Files

```
docs/runbook/cisco-demo.md
docs/runbook/setup-cluster.md
docs/mkdocs.yml              # add runbook/ section to nav if not auto-discovered
```

## Out of scope

- Slide deck or presentation assets
- Video recording or screen capture scripts
- Post-demo follow-up materials

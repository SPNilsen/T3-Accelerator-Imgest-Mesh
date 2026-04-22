# Local Demo Guide — Imgest-Mesh

A 30-second smoke test, a 5-minute demo, and a deeper 15-minute walkthrough — all running on your laptop, no GPU required.

See [`local-dev.md`](local-dev.md) for the wiring details this guide assumes.

---

## 30-second smoke test — "is it alive?"

From the repo root:

```bash
docker compose up -d
```

Open <http://localhost:8080>. Within ~15 seconds the three pipeline circles (Camera, Orchestrator, Inference) turn **indigo** and the progress bar animates out to Inference.

Done. You can `docker compose down` to stop.

---

## 5-minute demo — the story you tell an engineer

### Prep (once, before the demo)

```bash
# clean slate — optional but makes counters start from zero
rm -rf .data/
docker compose down

# pre-pull + build so the first live step is fast
docker compose build
```

### Running the demo

**1. Bring it up with one command.** Emphasize that this is four independent microservices:

```bash
docker compose up -d
docker compose ps
```

Talking point: *"Four OCI containers. Each does one thing. They scale independently and — critically — this same compose file becomes a set of Kubernetes manifests for the Cisco AI Pod deployment. Nothing about the service code changes between laptop and production."*

**2. Open the dashboard** at <http://localhost:8080>.

As the circles turn indigo, point out:
- The dashboard polls each service's `/status` endpoint every 10 seconds
- Each circle **is clickable** once the service is `up` — opens that service's raw JSON status
- The progress bar reflects how far through the pipeline data is flowing

**3. Show the raw service APIs** (in another terminal or browser tab):

```bash
curl http://localhost:8081/status | python -m json.tool   # camera
curl http://localhost:8082/status | python -m json.tool   # orchestrator
curl http://localhost:8083/status | python -m json.tool   # inference
```

Talking point: *"Each service exposes a FastAPI with /healthz and /status. That's your observability primitive — the dashboard is a consumer, Prometheus could be another, a Manufacturing Execution System could be a third."*

**4. Show the data actually flowing** — this is the "aha":

```bash
# a frame appears every 2 seconds
ls .data/frames/ | tail -5

# orchestrator routes them to the inference stage
ls .data/routed/ | tail -5

# inference emits pass/fail verdicts
ls .data/results/json/ | tail -5
cat .data/results/json/frame-00003.json
```

Talking point: *"The camera drops frames, the orchestrator routes them, the inference service writes verdicts. In production the routing is fan-out to many GPU-backed inference pods. The pipeline shape doesn't change."*

**5. Show graceful degradation** (optional, powerful):

```bash
docker compose stop inference
```

Refresh the dashboard — the Inference circle goes gray ("Not reachable"), the progress bar retracts. The camera and orchestrator keep running; frames pile up in `.data/routed/` waiting.

```bash
docker compose start inference
```

Refresh — Inference comes back up and drains the backlog.

Talking point: *"This is the shape of resilience you want in a factory. If one inference pod dies, frames queue until another picks up. We're showing that at laptop scale; Kubernetes gives it to us for free at cluster scale."*

**6. Tear down:**

```bash
docker compose down
```

---

## 15-minute walkthrough — the architecture story

Add these beats after the 5-minute flow.

### A. Read the compose file out loud

Open `docker-compose.yml`. Walk through one service block (e.g. `inference`):

- `build.context` points at its own directory — each service is self-contained
- `ports: 8083:8083` — host → container mapping; `/status` is a FastAPI endpoint inside
- `volumes:` — **shared bind mounts are the wire protocol between stages**:
  - `/opt/orchestrator/output/inference-1` in the orchestrator is the same bind as `/opt/inference/input` in the inference service
- `depends_on:` — startup order
- `healthcheck:` — Docker's own readiness probe

Talking point: *"In Kubernetes, this 'volumes:' block becomes a PersistentVolumeClaim or ConfigMap. In a real production pipeline it'd be a message queue (Kafka, NATS) instead of a filesystem, but we use filesystem here because it's trivially observable — you can see what's happening by looking at files."*

### B. Show one service's source

Open `resources/inference/app/`:

- `main.py` — 20 lines, starts a FastAPI thread and a worker thread
- `config.py` — loads YAML from a well-known path
- `status.py` — the FastAPI endpoint logic; dead simple
- `worker.py` — **the interesting bit** — the file-watcher loop

Talking point: *"Total code per service is ~60 lines. The heavy lifting is the container platform, not our code. When we swap mock inference for a real model, only `worker.py` changes — everything else stays the same."*

### C. Show the mock → real migration target

Open `docs/dev/local-dev.md` → section "Inference mode". Walk through the 5-step migration path.

Talking point: *"We're deliberately decoupling 'the pipeline works' from 'we have a trained model.' Those are different engineering tracks. Mock mode lets us ship pipeline infrastructure before the data-science team has a production-ready model."*

### D. Read the K8s manifest

Open `resources/k8s/webserver/deployment.yaml`. Show how the Route, Service, and Deployment map onto OpenShift.

Talking point: *"The webserver has a full manifest set. The other three services need the same treatment before the Cisco demo — that's the next job."*

---

## What to tune for different audiences

| Audience | Emphasize | De-emphasize |
|---|---|---|
| **Engineer / architect** | microservice boundaries, observability, K8s portability, mock→real decoupling | domain terminology |
| **Data scientist** | the `worker.py` swap point, how models plug in, verdict schema | container internals |
| **Manager / stakeholder** | "deploys to OpenShift unchanged," deadlines, visual dashboard | CLI commands, YAML |
| **Customer** | industrial use case narrative (frames → inspection → pass/fail → MES), platform portability | mock mode (say "development harness" instead) |

---

## Live-demo controls

### Adjust how fast frames appear
Edit `resources/camera/config/camera-config.yaml`:
```yaml
capture:
  interval_seconds: 2    # lower = faster
```
Then `docker compose restart camera`.

### Adjust the mock pass/fail ratio
Edit `resources/inference/app/worker.py`:
```python
pass_rate = 0.8    # 0.0–1.0
```
Then `docker compose restart inference`.

### Cap total frames (useful to let `/status.frames_emitted` plateau visibly)
```yaml
# resources/camera/config/camera-config.yaml
capture:
  max_frames: 20   # 0 = run forever
```

### Tail logs live (good for a second screen)
```bash
docker compose logs -f --tail=10 camera orchestrator inference
```

---

## Reset between demos

```bash
docker compose down
rm -rf .data/
docker compose up -d
```

`docker compose down -v` does NOT clear `.data/` because those are bind mounts, not named volumes. You must `rm -rf .data/` explicitly.

---

## Pre-demo checklist

- [ ] `docker compose build` ran successfully earlier (first build ~5 min; warm build ~30s)
- [ ] Ports 8080–8083 are free on the host
- [ ] Docker Desktop is running and has ≥4 GB memory allocated
- [ ] `.data/` is clean if you want counters to start from zero
- [ ] Browser tab prepped at <http://localhost:8080>
- [ ] Second terminal open at the repo root for `curl` / `ls .data/` moves
- [ ] (Optional) `docker compose logs -f` streaming on a second monitor

---

## Quick recovery if something goes wrong mid-demo

| Problem | Fix |
|---|---|
| Dashboard circles stay gray | `docker compose ps` — any `Restarting`? Check `docker compose logs <svc>` |
| "env: 'bash\r'" in logs | Fixed in `.gitattributes`; if you see this on a stale checkout, run `sed -i 's/\r$//' resources/*/scripts/start.sh` |
| "port already in use" | Another process owns 8080/8081/8082/8083 — `netstat -ano \| findstr 808` on Windows, kill the offender |
| Dashboard loads but shows "Not reachable" | Services bound to container `0.0.0.0` but host-to-container networking is broken — restart Docker Desktop |
| Frames not appearing in `.data/frames/` | Check camera logs: `docker compose logs camera`. Bind mount permission issue on Windows is rare but possible |

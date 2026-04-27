# Local Dev — Wiring Reference

How the four Imgest-Mesh services connect when running via `docker compose up` from the repo root.

See the top-level `README.md` for the quick-start commands. This doc explains the plumbing.

## Stack
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   camera     │     │ orchestrator │     │  inference   │     │  webserver   │
│  :8081       │     │  :8082       │     │  :8083       │     │  :8080 (UI)  │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘     └──────────────┘
       │ writes             │ watches+copies     │ watches+emits
       ▼                    ▼                    ▼
 .data/frames/        .data/routed/         .data/results/json/
 (shared with         (shared with          (host-readable
  orchestrator         inference             verdict JSONs)
  as input)            as input)
```

## How each service is mounted

| Service | Container path | Host path | Role |
|---|---|---|---|
| camera | `/opt/camera/output` | `./.data/frames` | emits placeholder frames |
| orchestrator | `/opt/orchestrator/input` | `./.data/frames` | reads camera's output |
| orchestrator | `/opt/orchestrator/output/inference-1` | `./.data/routed` | routes to inference |
| inference | `/opt/inference/input` | `./.data/routed` | reads routed files |
| inference | `/opt/inference/output/json` | `./.data/results/json` | writes pass/fail verdicts |
| inference | `/opt/inference/output/images` | `./.data/results/images` | reserved for future image output |

Same host dir mounted into two containers = the shared channel between stages. Bind-mounting to `./.data/` (instead of named Docker volumes) lets you inspect files from Windows Explorer or VS Code while the pipeline is running.

## Port mapping to host

Host → Container:
- `8000` → docs (MkDocs Material site for Imgest-Mesh)
- `8001` → jnj-armor-docs (linked MkDocs site for the JNJ-Armor sibling repo)
- `8080` → webserver (nginx dashboard UI)
- `8081` → camera FastAPI `/healthz` `/status`
- `8082` → orchestrator FastAPI `/healthz` `/status`
- `8083` → inference FastAPI `/healthz` `/status`

The dashboard at `:8080` has two fixed-position links (top-right): **Docs** opens the Imgest-Mesh site at `:8000`, **JNJ-Armor Docs** opens the linked JNJ-Armor site at `:8001`. Both use `target="_blank" rel="noopener noreferrer"` so the pipeline page is never navigated away from — the status-polling loop and flow-bubble animation keep running in the original tab even while either docs site is open in another.

### Linked JNJ-Armor docs container — sibling-checkout requirement

The `jnj-armor-docs` compose service builds against the **JNJ-Armor sibling repo on the host**. By default it expects the layout:

```
parent/
├── T3-Accelerator-Imgest-Mesh/   (this repo)
└── T3-Accelerator-JNJ-Armor/     (sibling clone)
```

Override the path with `JNJ_ARMOR_REPO_PATH` in `.env` (see `.env.example`). Without the sibling clone, `docker compose up -d jnj-armor-docs` fails with a build-context error — by design and documented; the rest of the stack continues to run normally.

The `mkdocs.yml` nav in this repo includes external links pointing at `http://localhost:8001/...` for four pages that live in JNJ-Armor only (Executive Overview, Filemap, CRISP-DM Additional, Lessons Learned). On OpenShift these will be rewritten to the JNJ-Armor docs Route URL as part of `job-2`.

The dashboard JS in `resources/webserver/index.html` hardcodes `http://localhost:808[1-3]/status`. That works because browser-side fetches hit Docker Desktop's port mappings directly — not in-container DNS.

**OpenShift implication:** this browser→localhost pattern will NOT work on OpenShift. Before the Cisco demo the webserver must either:
1. Reverse-proxy each service through nginx (recommended), or
2. Each service gets its own OpenShift Route and the dashboard switches to those URLs.

## Inference mode

Currently `mock`. `resources/inference/app/worker.py::run_mock_inference_loop` watches the input dir and writes a JSON verdict (`pass` or `fail`) per file with an 80% pass rate and random confidence in `[0.60, 0.99]`.

Migration path to a real small model (e.g., MobileNetV3 from HuggingFace / ONNX model zoo):

1. Add an env switch `INFERENCE_MODE=mock|model` (default `mock` in dev / CI; `model` in the Cisco demo config)
2. Add a model-loader module that pulls the artifact to a cache volume on first run
3. Replace random verdicts with real inference output + a pass/fail threshold
4. Keep mock mode available for tests and air-gapped scenarios
5. Swap the tiny model for the real Imgest-Mesh inspection model by changing one config value — no code change required

## Troubleshooting

### Services restart-loop with exit 127 on Windows
Symptom in `docker compose logs`:
```
env: 'bash\r': No such file or directory
```
Cause: `*.sh` files were checked out with CRLF line endings. Fix:
```bash
# one-time fix of existing checkout
sed -i 's/\r$//' resources/*/scripts/start.sh
```
The `.gitattributes` at the repo root prevents this for future clones, but
an existing working copy may still need the one-time `sed` pass.

### Build fails with "parent snapshot ... does not exist"
Docker BuildKit cache corruption (common after interrupted builds):
```bash
docker builder prune -f
docker compose build
```

### Port conflicts
Host ports 8080–8083 must be free. On Windows, check with
`Get-NetTCPConnection -LocalPort 8080` (PowerShell) or
`netstat -ano | findstr 808` (cmd).

## Known gaps / observations

- **Camera emits `.txt`, not real images:** `resources/camera/app/emitter.py::emit_placeholder_frame` writes text stubs. Pillow is in `requirements.txt` but unused. Upgrading to real image emission is part of the inference-model work.
- **`/healthz` is a minimal endpoint** — returns `{"ok": true}` only. Compose healthchecks hit it directly.
- **Inference `storage.image_output_directory` is allocated but unused** — reserved for annotated-image output.

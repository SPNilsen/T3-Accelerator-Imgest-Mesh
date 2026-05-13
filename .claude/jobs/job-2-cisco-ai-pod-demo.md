---
id: job-2
title: Cisco AI Pod demo prep — K8s manifests + GPU + real inference
status: done
branch: feature/cisco-demo-manifests
base-branch: dev
assigned: Sean
sp: 8
security-scan: not-required
deadline: 2026-05-20
---

# Job 2 — Cisco AI Pod K8s Migration + Real Inference

## Why

The demo runs on Docker Compose today. The Cisco AI Pod is a K8s cluster with
A100 GPUs. Job 2 migrates all services to K8s manifests, replaces the mock
inference worker with real Detectron2/TensorRT inference, and converts the
JNJ-Armor PyTorch model to ONNX then TensorRT so the GPU is actually used
during the demo.

## Blockers (resolve before starting)

1. **Model weights path** — The `.pt` file is gitignored and not in the repo.
   Confirm the path on the machine where conversion will run (likely the AI Pod
   itself or a CUDA-capable workstation). Required by story 1.
2. **Cluster access** — `kubectl` context for the Cisco AI Pod cluster.
   Required by story 3.
3. **Registry** — Where to push images (Harbor, ECR, GHCR, or AI Pod local
   registry). Required by story 3.

## Stories

### Story 1 — Model conversion: PT → ONNX → TensorRT (3 SP)

**Deliverable**: `resources/inference/scripts/convert_model.py`

Detectron2 ONNX export requires tracing through `torch.onnx.export` with a
dummy input matching the model's expected shape. TensorRT conversion via
`trtexec` or the Python `tensorrt` SDK produces the `.engine` file used at
inference time.

Steps the script must perform:
1. Load Detectron2 config + `.pt` weights via `DefaultPredictor`
2. Export to ONNX via `torch.onnx.export` with `opset_version=16`,
   dynamic axes on batch and spatial dims
3. Validate ONNX graph with `onnx.checker.check_model`
4. Convert ONNX → TensorRT `.engine` via `tensorrt` Python API,
   FP16 precision, explicit batch, workspace 4 GB
5. Save engine to configurable output path; print layer count + engine size

Script is a one-shot CLI tool — not invoked at runtime:
```
python resources/inference/scripts/convert_model.py \
  --model-path /path/to/model.pt \
  --output-dir resources/inference/model/
```

Output files tracked in repo (gitignored `.pt`, committed `.onnx` if small
enough, committed `.engine` only if team decides to — otherwise document the
conversion step):
```
resources/inference/model/
  lens_defect_detector.onnx
  lens_defect_detector.engine   # .gitignore candidate — check size
```

**Acceptance criteria**:
- Script runs to completion on a CUDA-capable machine without error
- ONNX model passes `onnx.checker.check_model`
- TensorRT engine loads in Python without error
- Script prints model input shape, output shape, and engine size

---

### Story 2 — Real inference worker (3 SP)

**Deliverable**: `resources/inference/app/real_worker.py`

Replace `run_mock_inference_loop` with `run_real_inference_loop` that loads the
TensorRT engine and runs actual inference on each routed BMP. The existing
`worker.py` mock loop stays in place — `main.py` selects real vs. mock based
on whether the engine file exists and `INFERENCE_MODE=real` env var is set.

Real inference loop:
1. Load TensorRT engine from `MODEL_ENGINE_PATH` env var (fail fast if missing)
2. Pre-process each BMP: resize to model input shape, normalize, HWC → CHW
3. Run engine via `tensorrt` Python binding (or `pycuda`)
4. Post-process: NMS on raw boxes, threshold at `CONFIDENCE_THRESHOLD` (default 0.5)
5. Produce `verdict`: `pass` if no detections above threshold, `fail` otherwise
6. Write result JSON in same format as mock worker (pipeline[] field preserved)
7. Call `note_inference` and prune — identical to mock

Environment variables:
```
INFERENCE_MODE=real          # enables real worker; default "mock"
MODEL_ENGINE_PATH=/opt/inference/model/lens_defect_detector.engine
CONFIDENCE_THRESHOLD=0.5
```

**Acceptance criteria**:
- With `INFERENCE_MODE=mock` (default), existing mock behavior unchanged
- With `INFERENCE_MODE=real` + valid engine, worker processes BMPs and writes
  valid JSON results with `mode: real` in the details field
- Verdict and confidence are derived from actual model output, not random
- No import of TensorRT at module level — guard with `if mode == "real"` so
  the mock path works on CPU-only machines

---

### Story 3 — K8s manifests (2 SP)

**Deliverable**: `k8s/` directory at repo root

One manifest per service + shared infrastructure. Target namespace:
`imgest-mesh`.

```
k8s/
  namespace.yaml
  pvc.yaml                  # single PVC, subPaths per pipeline stage
  configmap-camera.yaml
  configmap-inference.yaml
  deploy-camera.yaml
  deploy-orchestrator.yaml
  deploy-inference.yaml     # GPU: nvidia.com/gpu: 1, A100
  deploy-webserver.yaml
  deploy-docs.yaml
  svc-camera.yaml
  svc-orchestrator.yaml
  svc-inference.yaml
  svc-webserver.yaml        # NodePort 30080 or LoadBalancer
  svc-docs.yaml
  kustomization.yaml        # kubectl apply -k k8s/
```

Key decisions:
- **Storage**: Single `ReadWriteMany` PVC (`imgest-mesh-data`) with subPaths
  mapping to `.data/frames`, `.data/routed`, `.data/results`, `.data/bmp-input`
- **GPU**: inference Deployment gets `resources.limits: {nvidia.com/gpu: "1"}` +
  `nodeSelector: {accelerator: a100}` (update label to match actual node label)
- **Images**: parametrized via Kustomize image overrides — no hardcoded registry
- **Config**: camera and inference configs mounted from ConfigMaps
- **Health**: existing `/healthz` FastAPI endpoints mapped to `livenessProbe` +
  `readinessProbe`
- **Model engine**: mounted from a separate PVC or an init container that copies
  the engine from an object store — document both options, implement simpler one

**Acceptance criteria**:
- `kubectl apply -k k8s/` creates all resources in `imgest-mesh` namespace
  without error
- All pods reach `Running` / `Ready`
- Inference pod shows GPU allocation in `kubectl describe pod`
- Webserver reachable at the exposed NodePort

---

## Files

```
resources/inference/scripts/convert_model.py   # story 1
resources/inference/app/real_worker.py         # story 2
resources/inference/app/main.py                # story 2 — mode switch
resources/inference/Containerfile              # story 2 — add TRT deps (GPU build)
resources/inference/config/inference-config.yaml  # story 2 — add INFERENCE_MODE
k8s/                                           # story 3 — all manifests
```

## Out of scope

- Demo script / talking points → job-9
- CI/CD pipeline for the K8s deployment
- Autoscaling, multi-replica, or HA configuration
- Any changes to camera, orchestrator, or webserver services

# Wiring — K8s + Real Inference (Cisco AI Pod)

Canonical doc: [`docs/dev/k8s-deployment.md`](../../../docs/dev/k8s-deployment.md)

## Key files (job-2)

| File | What it is |
|---|---|
| `k8s/` | Full Kustomize manifest set — `kubectl apply -k k8s/` |
| `k8s/deploy-inference.yaml` | GPU pod — `nvidia.com/gpu: "1"`, A100 nodeSelector |
| `k8s/pvc.yaml` | `imgest-mesh-data` (RWX pipeline data) + `imgest-mesh-models` (engine) |
| `k8s/kustomization.yaml` | Entry point — fill registry via `images:` block |
| `resources/inference/scripts/convert_model.py` | PT → ONNX → TensorRT one-shot CLI |
| `resources/inference/app/real_worker.py` | TRT inference loop |
| `resources/inference/app/main.py` | Mode switch: `INFERENCE_MODE=mock\|real` |
| `resources/inference/Containerfile.gpu` | GPU image (`nvcr.io/nvidia/tensorrt:24.01-py3`) |

## Three TODOs before `kubectl apply`

1. `storageClassName` in `k8s/pvc.yaml` — run `kubectl get storageclass`
2. `nodeSelector` in `k8s/deploy-inference.yaml` — run `kubectl get nodes --show-labels`
3. `REGISTRY` in all `deploy-*.yaml` — set via `sed` or `kustomization.yaml` images block

## Model conversion command

```bash
python resources/inference/scripts/convert_model.py \
    --model-path /path/to/lens_defect_detector.pt \
    --output-dir resources/inference/models/
```

Requires CUDA machine with same CUDA version as TRT base (24.01 = CUDA 12.3).
Model is Detectron2 — uses TracingAdapter for ONNX export, not vanilla torch.onnx.

## Inference env vars

| Var | Default | Notes |
|---|---|---|
| `INFERENCE_MODE` | `mock` | Set to `real` in K8s inference Deployment |
| `MODEL_ENGINE_PATH` | — | Full path to `.engine` file in models PVC |
| `CONFIDENCE_THRESHOLD` | `0.5` | Detection threshold for pass/fail verdict |

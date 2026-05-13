# K8s Deployment — Cisco AI Pod

How to migrate Imgest-Mesh from Docker Compose to Kubernetes on the Cisco AI Pod
(A100 GPU, Red Hat OpenShift / vanilla K8s).

See [`local-dev.md`](local-dev.md) for the Docker Compose reference this builds on.

---

## What's in the repo

| Path | Purpose |
|---|---|
| `k8s/` | Kustomize manifest set — one `kubectl apply -k k8s/` deploys everything |
| `resources/inference/scripts/convert_model.py` | One-shot PT → ONNX → TensorRT engine conversion |
| `resources/inference/app/real_worker.py` | TensorRT inference loop (replaces mock) |
| `resources/inference/Containerfile.gpu` | GPU image based on `nvcr.io/nvidia/tensorrt:24.01-py3` |
| `resources/inference/requirements.gpu.txt` | GPU-only pip deps (opencv-headless, pycuda) |

---

## Three things to fill in before applying

The manifests are complete except for three values that depend on your specific cluster.
Find and replace all `TODO` comments before running `kubectl apply`:

### 1 — Storage class

```bash
kubectl get storageclass
```

Edit `k8s/pvc.yaml` and set `storageClassName` to the class that supports
`ReadWriteMany` (e.g. `nfs-client`, `rook-cephfs`, `longhorn`).

### 2 — GPU node label

```bash
kubectl get nodes --show-labels | grep -i gpu
```

Edit `k8s/deploy-inference.yaml` → `nodeSelector` to match the label on your
A100 nodes. Common values: `nvidia.com/gpu.present: "true"`,
`accelerator: a100`.

### 3 — Image registry

```bash
# Replace REGISTRY with your Harbor / ECR / GHCR address in all manifests:
sed -i 's|REGISTRY|your.registry.example.com|g' k8s/*.yaml
```

Or uncomment the `images:` block in `k8s/kustomization.yaml` and fill it in
there — Kustomize image overrides are cleaner for multi-environment setups.

---

## Model conversion (run once, on a CUDA machine)

The inference container needs a TensorRT `.engine` file built from the
JNJ-Armor Detectron2 weights. Run this on the AI Pod itself or any machine
with a matching CUDA version and the `.pt` weights available:

```bash
# Install conversion deps (not in the inference container's requirements.txt)
pip install torch torchvision detectron2 onnx onnxruntime tensorrt pycuda

# Run conversion — adjust --model-path and --input-height/width to match training
python resources/inference/scripts/convert_model.py \
    --model-path /path/to/lens_defect_detector.pt \
    --output-dir resources/inference/models/ \
    --input-height 800 \
    --input-width 800

# Output:
#   resources/inference/models/lens_defect_detector.onnx
#   resources/inference/models/lens_defect_detector.engine
```

The script:
1. Loads Detectron2 via `DefaultPredictor` + `TracingAdapter`
2. Exports ONNX opset 16 with dynamic spatial axes
3. Validates the ONNX graph (`onnx.checker`)
4. Builds a TensorRT FP16 engine (4 GB workspace)
5. Runs a smoke test (tensor in, no crash = pass)

### Seed the model PVC

```bash
# Copy the engine into the cluster after kubectl apply
kubectl cp resources/inference/models/lens_defect_detector.engine \
    imgest-mesh/$(kubectl get pod -n imgest-mesh -l app=inference -o name | head -1):/opt/inference/models/
```

---

## Build and push images

```bash
REGISTRY=your.registry.example.com

# CPU services (unchanged from local dev)
docker build -t $REGISTRY/imgest-mesh/camera:latest         resources/camera/
docker build -t $REGISTRY/imgest-mesh/orchestrator:latest   resources/orchestrator/
docker build -t $REGISTRY/imgest-mesh/webserver:latest      resources/webserver/
docker build -t $REGISTRY/imgest-mesh/docs:latest           -f resources/docs/Containerfile .

# GPU inference image
docker build -t $REGISTRY/imgest-mesh/inference-gpu:latest \
    -f resources/inference/Containerfile.gpu \
    resources/inference/

docker push $REGISTRY/imgest-mesh/camera:latest
docker push $REGISTRY/imgest-mesh/orchestrator:latest
docker push $REGISTRY/imgest-mesh/webserver:latest
docker push $REGISTRY/imgest-mesh/docs:latest
docker push $REGISTRY/imgest-mesh/inference-gpu:latest
```

---

## Apply to the cluster

```bash
# 1. Create namespace + all resources
kubectl apply -k k8s/

# 2. Verify pods are running
kubectl get pods -n imgest-mesh

# 3. Check GPU allocation on the inference pod
kubectl describe pod -n imgest-mesh -l app=inference | grep -A5 "Limits:"

# 4. Seed bmp-input source images into the data PVC
kubectl cp .data/bmp-input/ \
    imgest-mesh/$(kubectl get pod -n imgest-mesh -l app=camera -o name | head -1):/opt/camera/bmp-input/

# 5. Open the dashboard
# NodePort 30080 → http://<node-ip>:30080
kubectl get nodes -o wide   # get node IP
```

---

## Inference mode switch

| `INFERENCE_MODE` env var | Behaviour |
|---|---|
| `mock` (default) | Random pass/fail — no GPU, no model file needed |
| `real` | TensorRT engine — requires `MODEL_ENGINE_PATH` + GPU node |

The inference Deployment in `k8s/deploy-inference.yaml` sets `INFERENCE_MODE=real`.
To test the K8s stack without a model engine first, change it to `mock` temporarily.

---

## Data volume layout

The `imgest-mesh-data` PVC is shared across all pipeline services via subPaths,
mirroring the `.data/` bind-mount layout from Docker Compose:

| subPath | Mounted by | Purpose |
|---|---|---|
| `bmp-input` | camera | Source BMP frames |
| `frames` | camera (write), orchestrator (read) | Emitted frames |
| `routed` | orchestrator (write), inference (read) | Routed frames |
| `results/json` | inference (write) | Verdict JSONs |
| `results/images` | inference (write) | Annotated images |

---

## Troubleshooting

| Symptom | Check |
|---|---|
| Inference pod stuck in `Pending` | `kubectl describe pod` — likely no GPU node matched `nodeSelector` |
| `MODEL_ENGINE_PATH` not found | Engine not seeded into models PVC — see "Seed the model PVC" above |
| `ReadWriteMany` PVC stuck in `Pending` | Storage class doesn't support RWX — check `kubectl get storageclass` |
| Dashboard shows "Not reachable" | Services are ClusterIP — webserver NodePort (30080) is the only external entry point; camera/orchestrator/inference status endpoints are internal only in K8s |
| Engine build fails during conversion | CUDA version mismatch — run conversion on the same CUDA version as the TRT base image (`24.01` = CUDA 12.3) |

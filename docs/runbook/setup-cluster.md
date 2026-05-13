# Cluster Setup — Cisco AI Pod

Step-by-step for whoever preps the environment before the demo. Assumes `kubectl` is configured for the AI Pod cluster.

See [`k8s-deployment.md`](../dev/k8s-deployment.md) for the full technical reference.

---

## Prerequisites

- `kubectl` context set to the AI Pod cluster
- Docker + registry access for image push
- The JNJ-Armor `.pt` weights file (on a CUDA machine — AI Pod or matching workstation)
- This repo checked out locally

---

## Step 1 — Resolve the three cluster-specific TODOs

Three values in the manifests depend on your specific cluster. Fill these in before applying:

### Storage class

```bash
kubectl get storageclass
```

Find the class that supports `ReadWriteMany` (e.g. `nfs-client`, `rook-cephfs`, `longhorn`).
Edit `k8s/pvc.yaml` → set `storageClassName` on the `imgest-mesh-data` PVC.

### GPU node label

```bash
kubectl get nodes --show-labels | grep -i gpu
```

Edit `k8s/deploy-inference.yaml` → `nodeSelector` → set the label that matches your A100 nodes.
Common values: `nvidia.com/gpu.present: "true"`, `accelerator: a100`.

### Image registry

```bash
REGISTRY=your.registry.example.com   # Harbor, ECR, GHCR, or AI Pod local registry

# Replace the REGISTRY placeholder in all manifests
sed -i "s|REGISTRY|$REGISTRY|g" k8s/*.yaml
```

Or use the Kustomize `images:` override block in `k8s/kustomization.yaml` (uncomment and fill in).

---

## Step 2 — Convert the model (run once)

Run on the AI Pod itself or any machine with matching CUDA + the `.pt` weights:

```bash
# Install conversion deps (not in the inference container)
pip install torch torchvision detectron2 onnx onnxruntime tensorrt pycuda

# Convert — adjust --model-path to wherever the .pt file lives
python resources/inference/scripts/convert_model.py \
    --model-path /path/to/lens_defect_detector.pt \
    --output-dir resources/inference/models/ \
    --input-height 800 \
    --input-width 800
```

Output: `resources/inference/models/lens_defect_detector.engine` (~200–400 MB depending on FP16)

Expected output:
```
[1/3] ONNX export OK  ->  resources/inference/models/lens_defect_detector.onnx
[2/3] FP16 precision enabled
[2/3] Engine written  ->  resources/inference/models/lens_defect_detector.engine
[3/3] Smoke test passed — engine executes without error
```

---

## Step 3 — Build and push images

```bash
REGISTRY=your.registry.example.com

# CPU services
docker build -t $REGISTRY/imgest-mesh/camera:latest         resources/camera/
docker build -t $REGISTRY/imgest-mesh/orchestrator:latest   resources/orchestrator/
docker build -t $REGISTRY/imgest-mesh/webserver:latest      resources/webserver/
docker build -t $REGISTRY/imgest-mesh/docs:latest           -f resources/docs/Containerfile .

# GPU inference image (uses nvcr.io/nvidia/tensorrt:24.01-py3 base — CUDA 12.3)
docker build -t $REGISTRY/imgest-mesh/inference-gpu:latest \
    -f resources/inference/Containerfile.gpu \
    resources/inference/

# Push all
docker push $REGISTRY/imgest-mesh/camera:latest
docker push $REGISTRY/imgest-mesh/orchestrator:latest
docker push $REGISTRY/imgest-mesh/webserver:latest
docker push $REGISTRY/imgest-mesh/docs:latest
docker push $REGISTRY/imgest-mesh/inference-gpu:latest
```

---

## Step 4 — Apply manifests

```bash
# Create namespace + all resources
kubectl apply -k k8s/

# Watch pods come up
kubectl get pods -n imgest-mesh -w
```

Expected steady state (allow ~2 minutes for image pulls on first run):

```
NAME                           READY   STATUS    RESTARTS
camera-xxxxxxxxx-xxxxx         1/1     Running   0
orchestrator-xxxxxxxxx-xxxxx   1/1     Running   0
inference-xxxxxxxxx-xxxxx      1/1     Running   0
webserver-xxxxxxxxx-xxxxx      1/1     Running   0
docs-xxxxxxxxx-xxxxx           1/1     Running   0
```

---

## Step 5 — Seed data into PVCs

### Seed bmp-input source images (camera PVC)

```bash
CAMERA_POD=$(kubectl get pod -n imgest-mesh -l app=camera -o name | head -1)

kubectl cp .data/bmp-input/ imgest-mesh/$CAMERA_POD:/opt/camera/bmp-input/

# Verify
kubectl exec -n imgest-mesh $CAMERA_POD -- ls /opt/camera/bmp-input/ | wc -l
# Expected: 17 files (13 TAM07 + 4 TAM17)
```

### Seed model engine (inference PVC)

```bash
INFERENCE_POD=$(kubectl get pod -n imgest-mesh -l app=inference -o name | head -1)

kubectl cp resources/inference/models/lens_defect_detector.engine \
    imgest-mesh/$INFERENCE_POD:/opt/inference/models/lens_defect_detector.engine

# Verify
kubectl exec -n imgest-mesh $INFERENCE_POD -- ls -lh /opt/inference/models/
```

---

## Step 6 — Verify the stack

```bash
# GPU allocation on inference pod
kubectl describe pod -n imgest-mesh -l app=inference | grep -A5 "Limits:"
# Expected: nvidia.com/gpu: 1

# Inference mode
kubectl exec -n imgest-mesh deploy/inference -- env | grep INFERENCE_MODE
# Expected: INFERENCE_MODE=real

# Watch inference logs for live verdicts
kubectl logs -n imgest-mesh -l app=inference -f --tail=10
# Expected: frame-XXXXX.bmp -> pass (confidence=0.XXX, detections=0)
#        or frame-XXXXX.bmp -> fail (confidence=0.XXX, detections=N)

# Get node IP for browser access
kubectl get nodes -o wide
# Open http://<INTERNAL-IP>:30080 in browser
```

---

## Quick reference — key ports

| Service | ClusterIP port | External NodePort |
|---|---|---|
| Camera | 8081 | — (internal only) |
| Orchestrator | 8082 | — (internal only) |
| Inference | 8083 | — (internal only) |
| Webserver | 8080 | **30080** |
| Docs | 8000 | **30000** |

---

## Teardown

```bash
# Remove all resources (preserves PVCs by default)
kubectl delete -k k8s/

# Also delete PVCs (clears all seeded data — requires re-seeding)
kubectl delete pvc -n imgest-mesh --all
```

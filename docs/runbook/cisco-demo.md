# Cisco AI Pod — Demo Runbook

**Audience:** T3 presenter, SE, or solutions architect running the JNJ Imgest-Mesh demo on the Cisco AI Pod.

See [`setup-cluster.md`](setup-cluster.md) for pre-event cluster prep.
See [`k8s-deployment.md`](../dev/k8s-deployment.md) for the full technical reference.

---

## T-30 — Pre-demo setup checklist

Run through this before the room fills. Expected time: ~10 minutes if the cluster is already up.

```bash
# 1. Verify all pods are Running / Ready
kubectl get pods -n imgest-mesh

# 2. Confirm GPU allocation on the inference pod
kubectl describe pod -n imgest-mesh -l app=inference | grep -A5 "Limits:"
# Expected: nvidia.com/gpu: 1

# 3. Confirm model engine is mounted
kubectl exec -n imgest-mesh deploy/inference -- ls /opt/inference/models/
# Expected: lens_defect_detector.engine

# 4. Confirm bmp-input images are seeded
kubectl exec -n imgest-mesh deploy/camera -- ls /opt/camera/bmp-input/ | wc -l
# Expected: 17 (13 TAM07 + 4 TAM17 BMPs)

# 5. Smoke test — watch one frame flow
kubectl logs -n imgest-mesh -l app=inference --tail=5 -f
# Let it run ~30s; you should see: frame-XXXXX.bmp -> pass/fail (confidence=X.XXX)
```

**Open browser tabs before the audience arrives:**

| Tab | URL | Purpose |
|---|---|---|
| Dashboard | `http://<node-ip>:30080` | Primary demo view |
| Docs | `http://<node-ip>:30000` | MkDocs site |
| Camera status | `http://<node-ip>:30080/api/camera/status` | Optional: raw JSON |
| Inference status | `http://<node-ip>:30080/api/inference/status` | Optional: live verdict |

**Fallback ready?**

If the cluster is having issues: Docker Compose on a local laptop provides full mock-mode demo in under 2 minutes. See [`demo-guide.md`](../dev/demo-guide.md).

---

## Demo narrative — talking track

### Beat 1 — Problem statement (~2 min)

> *"Johnson & Johnson manufactures contact lenses at scale. Every lens goes through an inspection step — historically done by camera rigs with rule-based thresholding. The challenge: defect patterns evolve, rule tuning is expensive, and false positives cost throughput. T3 was brought in to replace that with a trained defect detection model running in the manufacturing pipeline."*

Point at the dashboard header — the JNJ logo in context.

> *"What you're looking at is Imgest-Mesh — an image ingestion and inference mesh. It connects a camera feed directly to a Detectron2 model running on this A100 GPU, and surfaces verdicts in real time."*

---

### Beat 2 — Architecture overview (~2 min)

Point at the pipeline progress bar and the five bubble stages:

> *"Five stages. Camera emits frames from a BMP source — in production that's a physical camera rig. Orchestrator routes each frame to the inference stage. Inference runs the model and writes a pass/fail verdict with a confidence score. The webserver surfaces everything to this dashboard. Two dashed bubbles on the right — System Manager and Compressor — are the target edge architecture; stubs today, same drop-in shape as the services that are live."*

> *"Each stage is one OCI container. FastAPI inside, file-based wire protocol between stages. Same compose file that runs on a laptop becomes Kubernetes manifests for this cluster — no service code changes."*

---

### Beat 3 — Live pipeline (~3 min)

Point at the bottom row panels as they update:

> *"The camera panel shows the thumbnail of the frame currently in flight — that's a real TAM07 or TAM17 lens image from the JNJ dataset. The orchestrator panel shows routing state. The inference panel shows the latest verdict."*

> *"Watch the panels flash when they update — that's the live data moving through the pipeline right now, on this GPU."*

If a `fail` verdict comes up — good, highlight it:

> *"That's a defect detection. Confidence score tells you how certain the model is. In production, a fail verdict triggers a reject signal back to the line controller."*

---

### Beat 4 — Real inference (~2 min)

> *"This is not a mock. The model running on this A100 is the actual Detectron2 model trained on JNJ lens defect data — converted to ONNX and then to a TensorRT FP16 engine specifically for this GPU. FP16 gives us roughly 2x throughput on A100 with negligible accuracy impact."*

> *"The conversion pipeline: PyTorch weights → ONNX opset 16 → TensorRT engine. That script lives in the repo and takes about 10 minutes on this hardware."*

---

### Beat 5 — Model lineage (~1 min)

Switch to the Docs or JNJ-Armor Docs tab:

> *"The model didn't come out of nowhere. The JNJ-Armor project — the CRISP-DM analysis, data preparation, and modeling work — is documented here alongside the platform docs. The model's lineage is part of the deliverable."*

---

### Beat 6 — Platform extensibility (~2 min)

> *"The mesh is the point. Swap any service — different camera protocol, different model framework, different egress target. Add a new stage by scaffolding one container with the same FastAPI + worker pattern. The pipeline shape doesn't change. GPU is optional — mock mode runs the same stack on a laptop with no GPU and no model file."*

> *"The two dashed bubbles drop in exactly this way when we build them."*

---

## Live demo click-through

| Step | Action | Expected outcome |
|---|---|---|
| 1 | Open `http://<node-ip>:30080` | Header loads, pipeline bubbles appear |
| 2 | Wait ~15 seconds | Camera, Orchestrator, Inference bubbles turn indigo; progress bar animates |
| 3 | Point at Camera panel | Thumbnail cycles; filename matches `TAM07-*` or `TAM17-*` source image |
| 4 | Point at Inference panel | Verdict (`pass`/`fail`) + confidence score; panel flashes on update |
| 5 | Click the Camera bubble | Opens `/status` JSON in new tab — show `recent_files` array with `thumb_filename` |
| 6 | Click the Inference bubble | Opens inference `/status` — show `recent_results` with `verdict`, `confidence`, `mode: real-trt` |
| 7 | Open Docs tab | MkDocs site renders; navigate to Developer Guides → K8s Deployment |
| 8 | Open JNJ-Armor Docs tab | Customer-facing docs render; show Executive Overview or CRISP-DM Additional |

---

## Q&A prep

**"How long did the model take to train?"**
> The Detectron2 training was done by the JNJ-Armor project team. Training time depends on dataset size and GPU; for reference, fine-tuning Faster R-CNN R-50-FPN on a few thousand lens images typically takes 2–8 hours on a single V100.

**"What's the accuracy / false positive rate?"**
> Refer to the model evaluation section in JNJ-Armor Docs (CRISP-DM → Evaluation). Metrics are dataset-specific; the demo uses a confidence threshold of 0.5, adjustable via `CONFIDENCE_THRESHOLD` env var without redeploying.

**"Can this run on our own hardware?"**
> Yes. The stack runs on any CUDA-capable GPU with TensorRT support. For CPU-only environments, mock mode runs the entire pipeline with synthetic verdicts — same dashboard, same API, no GPU required.

**"How does it handle new defect categories?"**
> Retrain the Detectron2 model on updated labeled data, re-run the conversion script (`convert_model.py`), seed the new `.engine` into the models PVC, and roll the inference deployment. No pipeline code changes needed.

**"What's the latency from camera to verdict?"**
> End-to-end in the current file-poll architecture: ~2–4 seconds (1s camera interval + poll intervals). In a production message-queue architecture (Kafka/NATS replacing filesystem), sub-second is achievable on this GPU.

**"Is this OpenShift compatible?"**
> The manifests are standard Kubernetes. OpenShift adds SCCs (Security Context Constraints) — inference may need `anyuid` or a custom SCC for the NVIDIA runtime. NodeSelector labels differ by cluster. Everything else is drop-in.

---

## Recovery playbook

| Symptom | Likely cause | Fix |
|---|---|---|
| Inference pod stuck in `Pending` | No GPU node matched `nodeSelector` | `kubectl describe pod -n imgest-mesh -l app=inference` → check node label; update `k8s/deploy-inference.yaml` nodeSelector |
| Inference pod `CrashLoopBackOff` | Engine not mounted or wrong path | `kubectl exec deploy/inference -- ls /opt/inference/models/` — seed engine if missing; check `MODEL_ENGINE_PATH` env var |
| Dashboard shows "Not reachable" for all services | NodePort not reachable from demo machine | Confirm node IP with `kubectl get nodes -o wide`; check firewall rules for port 30080 |
| Thumbnail not updating / same image every cycle | `bmp-input` PVC empty or not mounted | `kubectl exec deploy/camera -- ls /opt/camera/bmp-input/` — re-seed if empty |
| GPU shows `0` in `kubectl describe pod` | NVIDIA device plugin not running | `kubectl get pods -n kube-system | grep nvidia` — plugin must be Running |
| `mode: mock` in inference status JSON | `INFERENCE_MODE` env var not set to `real` | `kubectl set env deploy/inference INFERENCE_MODE=real -n imgest-mesh` |
| Full cluster failure | Any unrecoverable K8s issue | Switch to local Docker Compose fallback — `docker compose up -d` on demo laptop |

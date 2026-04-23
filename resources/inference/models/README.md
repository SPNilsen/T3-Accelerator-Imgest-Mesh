# Inference Models

This directory holds model artifacts baked into the inference container image.

## Current state

Empty — mock mode is in use (see `resources/inference/app/worker.py`).
The container `COPY models ./models` step needs this directory to exist
at build time, which is why this README is here.

## Future: real model integration

When migrating from mock mode to real inference:

1. Place the model file here (e.g. `model.onnx`, `model.pt`, `model.bin`).
2. Update `resources/inference/config/inference-config.yaml`:
   - `model.name`
   - `model.path` (will resolve under `/opt/inference/models/` inside the container)
3. Replace `run_mock_inference_loop` in `worker.py` with a real loader + inference step.

## Note on registry vs. baked

Small demo models (<50 MB) can be baked into the image. Larger artifacts
should live in an external registry / object store and be mounted at
runtime — baking them into git bloats clones and fights versioning.

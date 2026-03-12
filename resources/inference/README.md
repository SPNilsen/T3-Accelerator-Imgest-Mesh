# Inference Service

This container represents the inference stage of the Imgest-Mesh pipeline.

## Purpose

The service will receive image artifacts, run them against a model, and produce JSON output and derivative image output.

For the current demo phase, the service runs in `placeholder-model` mode and exposes status endpoints only.

## Current behavior

- Starts a lightweight status API
- Reports configured model placeholder information
- Holds place for future inference logic

## Planned future behavior

- Read raw images from shared group storage
- Run model inference
- Write JSON results
- Write derived or processed image output

## Status endpoints

- `/healthz`
- `/status`

Default port: `8083`


---

## Build and run

```
mkdir -p resources/inference/models
touch resources/inference/models/.gitkeep
```

```
lima nerdctl build -t inference-test -f resources/inference/Containerfile resources/inference
```

```
lima nerdctl run --rm -it \
  -p 8083:8083 \
  inference-test
```

`http://localhost:8083/status`



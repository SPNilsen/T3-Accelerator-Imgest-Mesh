# Orchestrator Service

This container represents the orchestration stage of the Imgest-Mesh pipeline.

## Purpose

The service receives image/frame artifacts from the camera stage and routes them to downstream inference services.

For the initial demo phase, the orchestrator runs in `file-router` mode and watches a local input directory, then forwards files to a configured inference target.

## Current behavior

- Starts a lightweight status API
- Watches for incoming files
- Routes files to downstream output directories
- Tracks routed file counts

## Current scaling model

For this first implementation, the orchestrator is configured for `N=1`, meaning a single downstream inference target.

Future versions can expand to support `2^N` inference targets per camera source.

## Status endpoints

- `/healthz`
- `/status`

Default port: `8082`


## Build

```
lima nerdctl build -t orchestrator-test -f resources/orchestrator/Containerfile resources/orchestrator
```

## Run

```
lima nerdctl run --rm -it \
  -p 8082:8082 \
  orchestrator-test
```

### Check
`http://localhost:8082/status`

# Camera Service

This container represents the camera/input stage of the Imgest-Mesh pipeline.

## Purpose

The service is responsible for ingesting a visual source and producing individual frames or images for downstream analysis containers.

For the initial demo phase, this service runs in `demo-images` mode and emits placeholder frame artifacts into the output directory.

## Current behavior

- Starts a lightweight status API
- Emits demo frame artifacts on an interval
- Tracks frame counts and timestamps

## Planned future modes

- `video-file`
- `rtsp-stream`
- `usb-camera`

## Status endpoints

- `/healthz`
- `/status`

Default port: `8081`
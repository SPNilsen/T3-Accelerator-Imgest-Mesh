# Role Profile — Data

## Scope in this project
Image data pipeline: capture → preprocess → inference → classification.

## Current state
- `camera/app/capture.py` + `emitter.py` — ingestion entry
- `orchestrator/app/router.py` + `watcher.py` — pipeline routing
- `inference/app/worker.py` — model inference worker

## Reference case study
`docs/armor/` describes the ARMOR / ALI (Automatic Lens Inspection) system for Johnson & Johnson Vistakon — binary and multi-class defect detection on contact lenses. Use this as the canonical shape of an Imgest-Mesh application.

## Methodology reference
`docs/crisp-dm/` documents the CRISP-DM lifecycle Trace3 follows for data-science work.

## Gaps
- No sample images or test fixtures checked in
- No trained model artifact in repo — inference service must load from external source or bundled test model

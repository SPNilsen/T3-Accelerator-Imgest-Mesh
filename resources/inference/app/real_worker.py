"""
Real inference worker — TensorRT engine path.

Selected when INFERENCE_MODE=real and MODEL_ENGINE_PATH is set.
Imports tensorrt and pycuda only when this module is used, so the
mock path continues to work on CPU-only machines without these deps.
"""

import json
import logging
import os
import time
from datetime import datetime, UTC
from pathlib import Path

import cv2
import numpy as np

from .status import note_inference

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# TensorRT engine wrapper
# ---------------------------------------------------------------------------

class _TRTInferenceEngine:
    """Thin wrapper around a serialised TensorRT engine."""

    def __init__(self, engine_path: str):
        import tensorrt as trt
        import pycuda.driver as cuda
        import pycuda.autoinit  # noqa: F401 — initialises CUDA context

        self._cuda = cuda
        TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
        runtime = trt.Runtime(TRT_LOGGER)

        with open(engine_path, "rb") as f:
            self._engine = runtime.deserialize_cuda_engine(f.read())

        self._context = self._engine.create_execution_context()
        log.info("TensorRT engine loaded from %s", engine_path)

    def infer(self, image_bgr: np.ndarray, confidence_threshold: float = 0.5):
        """
        Run inference on a single BGR image (H x W x 3 uint8).
        Returns (verdict, confidence, num_detections).
        """
        import tensorrt as trt

        # Pre-process: resize to engine input shape, CHW float32
        inp_shape = self._engine.get_binding_shape(0)  # (1, 3, H, W)
        _, _, h, w = inp_shape
        resized = cv2.resize(image_bgr, (w, h))
        blob = resized.astype(np.float32).transpose(2, 0, 1)[np.newaxis]  # NCHW

        # Allocate host + device buffers
        d_input  = self._cuda.mem_alloc(blob.nbytes)
        # generous output buffers — max 1000 detections
        max_det  = 1000
        h_boxes  = np.zeros((max_det, 4), dtype=np.float32)
        h_scores = np.zeros(max_det,      dtype=np.float32)
        h_labels = np.zeros(max_det,      dtype=np.int32)
        d_boxes  = self._cuda.mem_alloc(h_boxes.nbytes)
        d_scores = self._cuda.mem_alloc(h_scores.nbytes)
        d_labels = self._cuda.mem_alloc(h_labels.nbytes)

        self._cuda.memcpy_htod(d_input, blob)
        self._context.execute_v2([int(d_input), int(d_boxes), int(d_scores), int(d_labels)])
        self._cuda.memcpy_dtoh(h_scores, d_scores)

        above_thresh = h_scores[h_scores >= confidence_threshold]
        num_det = int(len(above_thresh))

        if num_det == 0:
            verdict    = "pass"
            confidence = float(1.0 - float(np.max(h_scores)) if h_scores.max() > 0 else 1.0)
        else:
            verdict    = "fail"
            confidence = float(np.max(above_thresh))

        return verdict, round(confidence, 3), num_det


# ---------------------------------------------------------------------------
# Prune helper (mirrors worker.py to avoid cross-import)
# ---------------------------------------------------------------------------

def _prune_dir(directory, max_sets, primary_suffixes, sidecar_suffixes):
    primaries: dict[str, Path] = {}
    for suffix in primary_suffixes:
        for f in directory.glob(f"*{suffix}"):
            if f.stem not in primaries:
                primaries[f.stem] = f
    if len(primaries) <= max_sets:
        return
    ordered = sorted(primaries.values(), key=lambda p: p.stat().st_mtime)
    for primary in ordered[: len(ordered) - max_sets]:
        stem = primary.stem
        primary.unlink(missing_ok=True)
        for suf in sidecar_suffixes:
            (directory / f"{stem}{suf}").unlink(missing_ok=True)
        log.debug("pruned %s from %s", stem, directory)


def _read_metadata(src: Path) -> dict | None:
    meta_path = src.with_suffix(".meta.json")
    if meta_path.exists():
        return json.loads(meta_path.read_text(encoding="utf-8"))
    return None


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def run_real_inference_loop(config: dict):
    engine_path = os.environ.get("MODEL_ENGINE_PATH", "")
    if not engine_path or not Path(engine_path).exists():
        raise RuntimeError(
            f"MODEL_ENGINE_PATH not set or file not found: '{engine_path}'. "
            "Run convert_model.py first, then set MODEL_ENGINE_PATH."
        )

    confidence_threshold = float(os.environ.get("CONFIDENCE_THRESHOLD", "0.5"))
    input_dir     = Path(config["storage"]["input_directory"])
    json_out_dir  = Path(config["storage"]["json_output_directory"])
    max_frames    = config.get("storage", {}).get("max_frames", 20)
    poll_interval = 2

    input_dir.mkdir(parents=True, exist_ok=True)
    json_out_dir.mkdir(parents=True, exist_ok=True)

    engine = _TRTInferenceEngine(engine_path)
    log.info("Real inference mode active (threshold=%.2f)", confidence_threshold)

    processed: set[str] = set()

    while True:
        for path in sorted(input_dir.iterdir()):
            if not path.is_file() or path.name in processed:
                continue
            if path.name.endswith(".meta.json"):
                continue

            try:
                image_bgr = cv2.imread(str(path))
                if image_bgr is None:
                    log.warning("could not decode image %s — skipping", path.name)
                    processed.add(path.name)
                    continue

                verdict, confidence, num_det = engine.infer(image_bgr, confidence_threshold)
                ts   = datetime.now(UTC).isoformat()
                meta = _read_metadata(path)

                if meta is not None:
                    meta["pipeline"].append({
                        "stage": "inference",
                        "action": "processed",
                        "timestamp": ts,
                        "details": {
                            "verdict": verdict,
                            "confidence": confidence,
                            "num_detections": num_det,
                            "mode": "real-trt",
                        },
                    })

                result = {
                    "source_file": path.name,
                    "verdict": verdict,
                    "confidence": confidence,
                    "num_detections": num_det,
                    "mode": "real-trt",
                    "timestamp": ts,
                    "metadata": meta,
                }
                result_path = json_out_dir / f"{path.stem}.json"
                result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

                _prune_dir(json_out_dir, max_frames, [".json"], [])
                note_inference(filename=path.name, verdict=verdict, confidence=confidence, meta=meta)
                processed.add(path.name)

                log.info("%s -> %s (confidence=%.3f, detections=%d)", path.name, verdict, confidence, num_det)

            except Exception:
                log.exception("inference failed for %s — skipping", path.name)
                processed.add(path.name)

        processed -= {n for n in processed if not (input_dir / n).exists()}
        time.sleep(poll_interval)

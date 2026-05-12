import json
import logging
import random
import time
from datetime import datetime, UTC
from pathlib import Path

from .status import note_inference

log = logging.getLogger(__name__)


def _prune_dir(
    directory: Path,
    max_sets: int,
    primary_suffixes: list[str],
    sidecar_suffixes: list[str],
) -> None:
    # Collect primary files, group by stem
    primaries: dict[str, Path] = {}
    for suffix in primary_suffixes:
        for f in directory.glob(f"*{suffix}"):
            if f.stem not in primaries:
                primaries[f.stem] = f

    if len(primaries) <= max_sets:
        return

    # Sort oldest-first by mtime
    ordered = sorted(primaries.values(), key=lambda p: p.stat().st_mtime)
    to_delete = ordered[: len(ordered) - max_sets]

    for primary in to_delete:
        stem = primary.stem
        primary.unlink(missing_ok=True)
        for suf in sidecar_suffixes:
            (directory / f"{stem}{suf}").unlink(missing_ok=True)
        log.debug("pruned frame set %s from %s", stem, directory)


def _read_metadata(src: Path) -> dict | None:
    meta_path = src.with_suffix(".meta.json")
    if meta_path.exists():
        return json.loads(meta_path.read_text(encoding="utf-8"))
    return None


def run_mock_inference_loop(config: dict):
    input_dir = Path(config["storage"]["input_directory"])
    json_output_dir = Path(config["storage"]["json_output_directory"])
    max_frames = config.get("storage", {}).get("max_frames", 20)
    poll_interval = 2
    pass_rate = 0.8

    input_dir.mkdir(parents=True, exist_ok=True)
    json_output_dir.mkdir(parents=True, exist_ok=True)
    processed: set[str] = set()

    while True:
        for path in sorted(input_dir.iterdir()):
            if not path.is_file() or path.name in processed:
                continue
            # Sidecar metadata files are not standalone work items.
            if path.name.endswith(".meta.json"):
                continue

            verdict = "pass" if random.random() < pass_rate else "fail"
            confidence = round(random.uniform(0.6, 0.99), 3)
            ts = datetime.now(UTC).isoformat()

            meta = _read_metadata(path)
            if meta is not None:
                meta["pipeline"].append({
                    "stage": "inference",
                    "action": "processed",
                    "timestamp": ts,
                    "details": {"verdict": verdict, "confidence": confidence, "mode": "mock"},
                })

            result = {
                "source_file": path.name,
                "verdict": verdict,
                "confidence": confidence,
                "mode": "mock",
                "timestamp": ts,
                "metadata": meta,
            }
            result_path = json_output_dir / f"{path.stem}.json"
            result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

            _prune_dir(json_output_dir, max_frames, [".json"], [])

            note_inference(filename=path.name, verdict=verdict,
                           confidence=confidence, meta=meta)
            processed.add(path.name)

        processed -= {name for name in processed if not (input_dir / name).exists()}

        time.sleep(poll_interval)

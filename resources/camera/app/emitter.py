import json
import logging
import random
import shutil
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger(__name__)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_metadata(dest: Path, meta: dict) -> None:
    dest.with_suffix(".meta.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )


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


def emit_bmp_frame(
    output_dir: Path,
    bmp_input_dir: Path,
    filename_prefix: str,
    frame_number: int,
    max_frames: int = 20,
) -> str:
    bmps = sorted(bmp_input_dir.glob("*.bmp"))
    chosen = random.choice(bmps)

    stem = f"{filename_prefix}-{frame_number:05d}"
    dest = output_dir / f"{stem}.bmp"
    shutil.copy(chosen, dest)  # copy2 preserves source mtime, breaking prune order

    ts = _now_iso()
    _write_metadata(dest, {
        "frame_id": stem,
        "file_type": "bmp",
        "filename": dest.name,
        "filesize": dest.stat().st_size,
        "created_ts": ts,
        "pipeline": [{
            "stage": "camera",
            "action": "emitted",
            "timestamp": ts,
            "details": {"source_image": chosen.name, "mode": "bmp-image"},
        }],
    })

    _prune_dir(output_dir, max_frames, [".bmp", ".txt"], [".meta.json", ".thumb.png"])
    return str(dest)


def emit_placeholder_frame(
    output_dir: Path | str,
    filename_prefix: str,
    frame_number: int,
    max_frames: int = 20,
) -> str:
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    stem = f"{filename_prefix}-{frame_number:05d}"
    dest = outdir / f"{stem}.txt"
    ts = _now_iso()
    dest.write_text(
        f"demo frame {frame_number}\ncreated: {ts}\n", encoding="utf-8"
    )

    _write_metadata(dest, {
        "frame_id": stem,
        "file_type": "txt",
        "filename": dest.name,
        "filesize": dest.stat().st_size,
        "created_ts": ts,
        "pipeline": [{
            "stage": "camera",
            "action": "emitted",
            "timestamp": ts,
            "details": {"mode": "placeholder-text"},
        }],
    })

    _prune_dir(outdir, max_frames, [".bmp", ".txt"], [".meta.json", ".thumb.png"])
    return str(dest)


def emit_frame(
    output_dir: str,
    bmp_input_dir: str,
    filename_prefix: str,
    frame_number: int,
    max_frames: int = 20,
) -> str:
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    bmp_dir = Path(bmp_input_dir)

    bmps = sorted(bmp_dir.glob("*.bmp")) if bmp_dir.exists() else []
    if bmps:
        return emit_bmp_frame(outdir, bmp_dir, filename_prefix, frame_number, max_frames)
    return emit_placeholder_frame(outdir, filename_prefix, frame_number, max_frames)

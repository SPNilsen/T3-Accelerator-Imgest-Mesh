import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path

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


class Router:
    def __init__(self, targets: list[dict], max_frames: int = 20):
        self.targets = targets
        self.index = 0
        self.max_frames = max_frames

    def route_file(self, source_path: str) -> tuple[str, str]:
        target = self.targets[self.index]
        target_dir = Path(target["output_directory"])
        target_dir.mkdir(parents=True, exist_ok=True)

        source = Path(source_path)
        destination = target_dir / source.name
        shutil.copy2(source, destination)

        self._route_metadata(source, target_dir, target["name"])

        _prune_dir(target_dir, self.max_frames, [".bmp", ".txt"], [".meta.json"])

        self.index = (self.index + 1) % len(self.targets)
        return target["name"], str(destination)

    def _route_metadata(self, source: Path, target_dir: Path, target_name: str) -> None:
        meta_src = source.with_suffix(".meta.json")
        if not meta_src.exists():
            return

        meta = json.loads(meta_src.read_text(encoding="utf-8"))
        meta["pipeline"].append({
            "stage": "orchestrator",
            "action": "routed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": {"target": target_name},
        })
        (target_dir / meta_src.name).write_text(
            json.dumps(meta, indent=2), encoding="utf-8"
        )

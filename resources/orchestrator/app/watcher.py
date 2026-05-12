import json
from pathlib import Path
import time

from .status import note_seen, note_routed


def run_watch_loop(config: dict, router):
    input_dir = Path(config["watcher"]["input_directory"])
    poll_interval = config["watcher"]["poll_interval_seconds"]

    input_dir.mkdir(parents=True, exist_ok=True)
    seen = set()

    while True:
        for path in sorted(input_dir.iterdir()):
            if not path.is_file():
                continue
            # Sidecar metadata files travel with their data file — skip them here.
            if path.name.endswith(".meta.json"):
                continue
            if path.name in seen:
                continue

            note_seen(path.name)
            target_name, _ = router.route_file(str(path))

            # Read updated metadata from destination to include in status.
            meta = None
            meta_src = path.with_suffix(".meta.json")
            if meta_src.exists():
                try:
                    meta = json.loads(meta_src.read_text(encoding="utf-8"))
                except Exception:
                    pass

            note_routed(path.name, target=target_name, meta=meta)
            seen.add(path.name)

        time.sleep(poll_interval)

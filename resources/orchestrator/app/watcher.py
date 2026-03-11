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
            if path.name in seen:
                continue

            note_seen(path.name)
            router.route_file(str(path))
            note_routed(path.name)
            seen.add(path.name)

        time.sleep(poll_interval)
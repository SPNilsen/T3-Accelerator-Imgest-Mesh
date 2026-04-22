import json
import random
import time
from datetime import datetime, UTC
from pathlib import Path

from .status import note_inference


def run_mock_inference_loop(config: dict):
    input_dir = Path(config["storage"]["input_directory"])
    json_output_dir = Path(config["storage"]["json_output_directory"])
    poll_interval = 2
    pass_rate = 0.8

    input_dir.mkdir(parents=True, exist_ok=True)
    json_output_dir.mkdir(parents=True, exist_ok=True)
    processed: set[str] = set()

    while True:
        for path in sorted(input_dir.iterdir()):
            if not path.is_file() or path.name in processed:
                continue

            verdict = "pass" if random.random() < pass_rate else "fail"
            result = {
                "source_file": path.name,
                "verdict": verdict,
                "confidence": round(random.uniform(0.6, 0.99), 3),
                "mode": "mock",
                "timestamp": datetime.now(UTC).isoformat(),
            }
            result_path = json_output_dir / f"{path.stem}.json"
            result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

            note_inference()
            processed.add(path.name)

        time.sleep(poll_interval)

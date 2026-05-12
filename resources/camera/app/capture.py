import os
import time
from pathlib import Path

from .emitter import emit_frame
from .status import increment_frames


def run_capture_loop(config: dict):
    interval = config["capture"]["interval_seconds"]
    max_frames = config["capture"]["max_frames"]
    output_dir = config["output"]["directory"]
    filename_prefix = config["output"]["filename_prefix"]
    bmp_input_dir = config["input"]["bmp_directory"]
    storage_max_frames = config.get("storage", {}).get("max_frames", 20)

    frame_number = 1

    while True:
        result_path = emit_frame(
            output_dir, bmp_input_dir, filename_prefix, frame_number, storage_max_frames
        )
        p = Path(result_path)
        file_type = "bmp" if p.suffix == ".bmp" else "txt"
        increment_frames(filename=p.name, file_type=file_type, filesize=os.path.getsize(result_path))

        if max_frames and frame_number >= max_frames:
            break

        frame_number += 1
        time.sleep(interval)

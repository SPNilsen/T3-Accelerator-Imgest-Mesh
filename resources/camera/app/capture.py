import time
from .emitter import emit_placeholder_frame
from .status import increment_frames


def run_capture_loop(config: dict):
    interval = config["capture"]["interval_seconds"]
    max_frames = config["capture"]["max_frames"]
    output_dir = config["output"]["directory"]
    filename_prefix = config["output"]["filename_prefix"]

    frame_number = 1

    while True:
        emit_placeholder_frame(output_dir, filename_prefix, frame_number)
        increment_frames()

        if max_frames and frame_number >= max_frames:
            break

        frame_number += 1
        time.sleep(interval)
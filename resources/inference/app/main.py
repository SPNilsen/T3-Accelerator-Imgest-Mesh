import os
import threading
import uvicorn

from .config import load_config
from .status import app, set_mode, set_model, set_state
from .worker import run_mock_inference_loop


def run_status_server(host: str, port: int):
    uvicorn.run(app, host=host, port=port)


def main():
    config = load_config()

    inference_mode = os.environ.get("INFERENCE_MODE", "mock").lower()

    set_mode(inference_mode)
    set_model(config["model"]["name"], config["model"]["path"])
    set_state("starting")

    status_thread = threading.Thread(
        target=run_status_server,
        args=(config["status"]["host"], config["status"]["port"]),
        daemon=True,
    )
    status_thread.start()

    set_state("running")

    if inference_mode == "real":
        from .real_worker import run_real_inference_loop
        run_real_inference_loop(config)
    else:
        run_mock_inference_loop(config)


if __name__ == "__main__":
    main()
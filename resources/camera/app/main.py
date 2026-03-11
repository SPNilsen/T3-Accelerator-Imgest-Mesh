import threading
import uvicorn

from .config import load_config
from .capture import run_capture_loop
from .status import app, set_mode, set_state


def run_status_server(host: str, port: int):
    uvicorn.run(app, host=host, port=port)


def main():
    config = load_config()

    set_mode(config["mode"])
    set_state("starting")

    status_thread = threading.Thread(
        target=run_status_server,
        args=(config["status"]["host"], config["status"]["port"]),
        daemon=True,
    )
    status_thread.start()

    set_state("running")
    run_capture_loop(config)
    set_state("completed")


if __name__ == "__main__":
    main()
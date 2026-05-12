import threading
import uvicorn

from .config import load_config
from .router import Router
from .status import app, set_mode, set_state
from .watcher import run_watch_loop

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

    max_frames = config.get("storage", {}).get("max_frames", 20)
    router = Router(config["routing"]["targets"], max_frames=max_frames)

    set_state("running")
    run_watch_loop(config, router)

if __name__ == "__main__":
    main()
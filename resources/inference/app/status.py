from collections import deque
from datetime import datetime, UTC
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATUS = {
    "service": "inference",
    "state": "starting",
    "mode": "unknown",
    "model_name": None,
    "model_path": None,
    "last_inference_ts": None,
    "recent_results": [],   # last 10 inference results with full metadata chain
}

_recent: deque = deque(maxlen=10)


def now_iso():
    return datetime.now(UTC).isoformat()


def set_state(state: str):
    STATUS["state"] = state


def set_mode(mode: str):
    STATUS["mode"] = mode


def set_model(name: str, path: str):
    STATUS["model_name"] = name
    STATUS["model_path"] = path


def note_inference(filename: str = None, verdict: str = None,
                   confidence: float = None, meta: dict = None):
    ts = now_iso()
    STATUS["last_inference_ts"] = ts
    entry = {
        "filename": filename,
        "verdict": verdict,
        "confidence": confidence,
        "ts": ts,
        "metadata": meta,
    }
    _recent.append(entry)
    STATUS["recent_results"] = list(reversed(_recent))


@app.get("/healthz")
def healthz():
    return {"ok": True, "service": STATUS["service"]}


@app.get("/status")
def get_status():
    return STATUS

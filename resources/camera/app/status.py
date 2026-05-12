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
    "service": "camera",
    "state": "starting",
    "mode": "unknown",
    "frames_emitted": 0,
    "last_frame_ts": None,
    "recent_files": [],   # last 10 emitted frames with metadata
}

_recent: deque = deque(maxlen=10)


def now_iso():
    return datetime.now(UTC).isoformat()


def set_state(state: str):
    STATUS["state"] = state


def set_mode(mode: str):
    STATUS["mode"] = mode


def increment_frames(filename: str = None, file_type: str = None, filesize: int = None):
    ts = now_iso()
    STATUS["frames_emitted"] += 1
    STATUS["last_frame_ts"] = ts
    if filename:
        _recent.append({
            "filename": filename,
            "file_type": file_type,
            "filesize": filesize,
            "ts": ts,
        })
        STATUS["recent_files"] = list(reversed(_recent))


@app.get("/healthz")
def healthz():
    return {"ok": True, "service": STATUS["service"]}


@app.get("/status")
def get_status():
    return STATUS

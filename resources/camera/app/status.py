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
}


def now_iso():
    return datetime.now(UTC).isoformat()


def set_state(state: str):
    STATUS["state"] = state


def set_mode(mode: str):
    STATUS["mode"] = mode


def increment_frames():
    STATUS["frames_emitted"] += 1
    STATUS["last_frame_ts"] = now_iso()


@app.get("/healthz")
def healthz():
    return {"ok": True, "service": STATUS["service"]}


@app.get("/status")
def get_status():
    return STATUS

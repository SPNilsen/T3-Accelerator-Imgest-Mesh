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
    "service": "orchestrator",
    "state": "starting",
    "mode": "unknown",
    "files_seen": 0,
    "files_routed": 0,
    "last_file": None,
    "last_route_ts": None,
}

def now_iso():
    return datetime.now(UTC).isoformat()

def set_state(state: str):
    STATUS["state"] = state

def set_mode(mode: str):
    STATUS["mode"] = mode

def note_seen(filename: str):
    STATUS["files_seen"] += 1
    STATUS["last_file"] = filename

def note_routed(filename: str):
    STATUS["files_routed"] += 1
    STATUS["last_file"] = filename
    STATUS["last_route_ts"] = now_iso()

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": STATUS["service"]}

@app.get("/status")
def get_status():
    return STATUS
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
}

def now_iso():
    return datetime.now(UTC).isoformat()

def set_state(state: str):
    STATUS["state"] = state

def set_mode(mode: str):
    STATUS["mode"] = mode

def set_model(name: str, path: str):
    STATUS["model_name"] = name
    STATUS["model_path"] = path

def note_inference():
    STATUS["last_inference_ts"] = now_iso()

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": STATUS["service"]}

@app.get("/status")
def get_status():
    return STATUS
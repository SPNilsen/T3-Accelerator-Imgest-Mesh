from collections import deque
from datetime import datetime, UTC
from pathlib import Path

import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response

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


def _load_output_dir() -> Path:
    """Read output directory from camera-config.yaml, falling back to /opt/camera/output."""
    cfg_path = Path(__file__).parent.parent / "config" / "camera-config.yaml"
    try:
        with cfg_path.open() as f:
            cfg = yaml.safe_load(f)
        return Path(cfg["output"]["directory"])
    except Exception:
        return Path("/opt/camera/output")


def _latest_with_suffix(suffix: str) -> "Path | None":
    out = _load_output_dir()
    if not out.exists():
        return None
    files = sorted(out.glob(f"*{suffix}"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


@app.get("/latest-thumb")
def latest_thumb():
    p = _latest_with_suffix(".thumb.png")
    if not p:
        return Response(status_code=404)
    return FileResponse(str(p), media_type="image/png")


@app.get("/latest-frame")
def latest_frame():
    p = _latest_with_suffix(".bmp")
    if not p:
        return Response(status_code=404)
    return FileResponse(str(p), media_type="image/bmp")


@app.get("/healthz")
def healthz():
    return {"ok": True, "service": STATUS["service"]}


@app.get("/status")
def get_status():
    return STATUS

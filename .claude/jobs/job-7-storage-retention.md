---
id: job-7
title: Per-directory storage retention — max 20 frames across all pipeline stages
status: not-started
branch: feature/storage-retention
base-branch: dev
assigned: Sean
sp: 3
security-scan: not-required
---

# Job 7 — Storage retention

## Why

Camera emits a new frame every 2 seconds. At that rate `.data/frames/` alone
accumulates ~5,400 files per hour. Nothing in the current pipeline deletes
anything. Left unchecked, the demo host's disk fills up.

Each stage has its own output directory that only it writes to:

| Stage | Writes to | File types per frame |
|---|---|---|
| Camera | `.data/frames/` | `*.bmp` (or `*.txt`) + `*.meta.json` + `*.thumb.png` (job-6) |
| Orchestrator | `.data/routed/` | `*.bmp` (or `*.txt`) + `*.meta.json` |
| Inference | `.data/results/json/` | `*.json` (verdict result) |

Each service is the exclusive writer of its output directory and should prune
it after each write. This is the only rule needed — no cross-service
coordination required.

## Scope

**In scope:**

- Add `storage.max_frames: 20` to each service's YAML config. Loader changes
  are minimal — read the key with a default of 20 so existing runs without the
  key do not break.

- Add a `_prune_dir(directory, max_sets, primary_suffixes, sidecar_suffixes)`
  helper to each service. Pruning logic:
  1. Glob the directory for files matching `primary_suffixes` (e.g. `.bmp` and
     `.txt` for camera).
  2. Group by stem. Sort groups by the primary file's `mtime` ascending
     (oldest first).
  3. If `len(groups) > max_sets`: delete all files in the oldest
     `len(groups) - max_sets` groups, including every sidecar extension in
     `sidecar_suffixes` that shares the stem. Use `Path.unlink(missing_ok=True)`
     — don't crash if a sidecar is already gone.
  4. Log one debug line per deleted group:
     `"[camera] pruned frame set {stem} from {directory}"`.
  
  The helper is ~15 lines. Duplicate it in each service's existing module
  (services are separate containers, no shared code layer).

- **Camera** ([emitter.py](resources/camera/app/emitter.py)):
  - After each emit, call prune on the output directory.
  - Primary suffixes: `[".bmp", ".txt"]`.
  - Sidecar suffixes: `[".meta.json", ".thumb.png"]`.

- **Orchestrator** ([router.py](resources/camera/app/router.py)):
  - After each `shutil.copy2()` completes (both file and metadata copied to
    destination), call prune on `target_dir`.
  - Primary suffixes: `[".bmp", ".txt"]`.
  - Sidecar suffixes: `[".meta.json"]`.

- **Inference** ([worker.py](resources/inference/app/worker.py)):
  - After writing the `.json` result file, call prune on `json_output_dir`.
  - Primary suffixes: `[".json"]`.
  - Sidecar suffixes: `[]` (inference result JSON files have no sidecars).
  - **Prune the `processed` set** on every poll cycle after the file scan.
    Remove any entry whose corresponding file no longer exists in `input_dir`
    (orchestrator pruned it upstream). One line at the bottom of the inner
    loop:
    ```python
    processed -= {name for name in processed if not (input_dir / name).exists()}
    ```
    This bounds `processed` to at most `max_frames` entries at steady state —
    it can never grow larger than the number of files currently in `input_dir`,
    which is itself capped by orchestrator's prune. No separate size limit
    is needed; the directory retention policy enforces it transitively.

- Config changes:

  ```yaml
  # camera-config.yaml — add under a new top-level key
  storage:
    max_frames: 20

  # orchestrator-config.yaml
  storage:
    max_frames: 20

  # inference-config.yaml — already has a storage: block; add the key there
  storage:
    input_directory: /opt/inference/input
    json_output_directory: /opt/inference/output/json
    image_output_directory: /opt/inference/output/images
    max_frames: 20
  ```

- Config loader: each service's `config.py` already reads YAML into a dict.
  Access the key with `config.get("storage", {}).get("max_frames", 20)` so a
  missing key silently defaults to 20.

**Out of scope:**

- Pruning `.data/bmp-input/` — that's a user-managed source directory, not a
  pipeline output. The service reads from it but does not own it.
- Pruning `.data/results/images/` — inference config has this path but the
  current worker never writes there. Add max_frames to inference config for
  future use but do not add pruning code for a directory that's currently empty.
- Move semantics (replacing `shutil.copy2` with `shutil.move`). Retention
  by pruning the writer's output is sufficient and is a smaller change.
- Pruning the orchestrator's input directory (`.data/frames/`). Camera owns
  and prunes that directory. Orchestrator must not delete from it — that is
  not its directory.
- Pruning the inference input directory (`.data/routed/`). Orchestrator owns
  and prunes that directory.
- Configurable per-directory limits. One `max_frames` value applies to all
  directories for a given service.
- A global GC daemon or separate cleanup container.
- Pruning `.data/results/images/` — inference config has this path but the
  current worker never writes there.

## Acceptance criteria

1. After running the full compose stack for 10+ minutes, `.data/frames/`,
   `.data/routed/`, and `.data/results/json/` each contain no more than 20
   frame-sets (primary files + sidecars counted as one set).
2. Pruning is triggered per-write — no background thread, no cron, no sleep.
3. Prune only deletes files older than the 20 newest. Newest files are never
   touched.
4. Sidecar files (`*.meta.json`, `*.thumb.png`) are always deleted with their
   parent. No orphaned sidecars remain after a prune pass.
5. If a sidecar file is already missing when pruning tries to delete it (e.g.
   a race with another process), the service does not crash or log an error
   (use `missing_ok=True`).
6. With `max_frames: 20` in config and camera at 2-second interval, steady
   state after 1 minute = ~20 frames in `.data/frames/`, not 30.
7. Changing `max_frames` to `5` in camera-config.yaml, rebuilding, and
   restarting results in `.data/frames/` converging to 5 sets within one
   emit cycle.
8. The existing pipeline data flow is unaffected: orchestrator still sees and
   routes every file camera writes before that file is pruned (camera prunes
   *after* writing, so the newest file is always present; orchestrator polls
   every 2 seconds, same as camera emit interval — overlap is safe).
9. All three existing `/status` endpoints still return `recent_files` /
   `recent_results` with correct data (in-memory deques are not affected by
   on-disk pruning).
10. The inference `processed` set never exceeds `max_frames` entries at
    steady state. After running for 10+ minutes, `len(processed)` ≤ 20
    (verifiable by adding a temporary log line or checking via a debug
    endpoint if desired).

## Design — pruning helper

```python
import logging
from pathlib import Path

log = logging.getLogger(__name__)


def _prune_dir(
    directory: Path,
    max_sets: int,
    primary_suffixes: list[str],
    sidecar_suffixes: list[str],
) -> None:
    # Collect primary files, group by stem
    primaries: dict[str, Path] = {}
    for suffix in primary_suffixes:
        for f in directory.glob(f"*{suffix}"):
            if f.stem not in primaries:
                primaries[f.stem] = f

    if len(primaries) <= max_sets:
        return

    # Sort oldest-first by mtime
    ordered = sorted(primaries.values(), key=lambda p: p.stat().st_mtime)
    to_delete = ordered[: len(ordered) - max_sets]

    for primary in to_delete:
        stem = primary.stem
        primary.unlink(missing_ok=True)
        for suf in sidecar_suffixes:
            (directory / f"{stem}{suf}").unlink(missing_ok=True)
        log.debug("pruned frame set %s from %s", stem, directory)
```

Paste into each service's relevant module. Total code added: ~20 lines per
service.

## Call sites

**Camera** — end of `emit_frame()` in `emitter.py`:
```python
_prune_dir(outdir, max_frames, [".bmp", ".txt"], [".meta.json", ".thumb.png"])
```

**Orchestrator** — end of `route_file()` in `router.py`, after `_route_metadata()`:
```python
_prune_dir(target_dir, max_frames, [".bmp", ".txt"], [".meta.json"])
```

**Inference** — after `result_path.write_text(...)` in `worker.py`:
```python
_prune_dir(json_output_dir, max_frames, [".json"], [])
```

**Inference `processed` set** — at the bottom of the `while True` loop,
after the inner `for path` loop and before `time.sleep(poll_interval)`:
```python
processed -= {name for name in processed if not (input_dir / name).exists()}
```

The `max_frames` value is passed in from the caller in each case (read once
from config at startup, passed down to the loop functions).

## Files expected to change

- `resources/camera/app/emitter.py` (add `_prune_dir`, call after emit)
- `resources/camera/app/config.py` (read `storage.max_frames`, pass to loop)
- `resources/camera/app/capture.py` (pass `max_frames` through to `emit_frame`)
- `resources/camera/config/camera-config.yaml` (add `storage.max_frames: 20`)
- `resources/orchestrator/app/router.py` (add `_prune_dir`, call after route)
- `resources/orchestrator/config/orchestrator-config.yaml` (add `storage.max_frames: 20`)
- `resources/inference/app/worker.py` (add `_prune_dir`, call after write)
- `resources/inference/config/inference-config.yaml` (add `max_frames: 20` inside existing `storage:` block)
- `.claude/jobs/INDEX.md` (add job-7 row)

No new files. No new dependencies.

## Test plan

Tests are targeted per code-quality rule §1. One test file per service
covering the prune helper in isolation:

- `_prune_dir` with 25 fake files, assert only 20 remain after call.
- `_prune_dir` with sidecars: assert `.meta.json` and `.thumb.png` are
  deleted alongside their primary.
- `_prune_dir` with a missing sidecar: assert no exception raised.
- `_prune_dir` with exactly 20 files: assert nothing is deleted.
- Integration smoke: run `emit_bmp_frame` (camera) 25 times against a temp
  directory, assert output dir contains ≤ 20 primary files.
- **Inference `processed` set**: simulate 25 files processed, then remove
  5 from `input_dir` (simulating upstream prune), run the set-prune line,
  assert `len(processed) == 20`.

## Notes

- The orchestrator's pruning covers `.data/routed/`, which is also the
  inference input. Inference polls and marks processed files in its `processed`
  set (in-memory). If orchestrator prunes a file before inference gets to it,
  that file is silently skipped (inference loops over `input_dir.iterdir()` and
  the file simply won't appear). At a 2-second camera interval with 20-frame
  retention = 40-second window, inference has 40 seconds to consume each file.
  This is safe for demo purposes. In production you would use move semantics
  or an event bus.
- The `processed` set prune is deliberately placed at the bottom of the
  `while True` loop (after the inner `for path` scan), not inside the inner
  loop. This avoids mutating the set while iterating over `input_dir` and
  keeps the prune to once per poll cycle rather than once per file.
- Both failure modes are now managed: physical disk (directory prune) and
  process memory (`processed` set prune). Neither can grow unbounded at
  steady state.

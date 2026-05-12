---
id: job-6
title: Dashboard column layout + per-service detail panels (offline-safe)
status: not-started
branch: feature/dashboard-grid-layout
base-branch: dev
assigned: Sean
sp: 5
security-scan: not-required
---

# Job 6 — Dashboard grid layout

## Why

Today's dashboard at `http://localhost:8080/` shows the logo, the animated
pipeline bubbles (job-3), and nothing else. A viewer can confirm the services
are alive but can't see *what's actually flowing through the mesh*. For the
Cisco AI Pod demo (2026-05-20) we need the dashboard to communicate three
things at a glance:

1. The services are up (existing bubbles — preserved).
2. The camera is producing real image data (live thumbnail).
3. The pipeline metadata chains end-to-end (formatted JSON from
   orchestrator + inference `/status` endpoints — the inference panel is the
   showpiece because its `metadata.pipeline[]` carries the full
   camera → orchestrator → inference trail in one blob).

Additional constraint: the demo runs **offline**. Any external asset (Font
Awesome CDN, fonts, frameworks) must either be vendored into the webserver
build context or replaced. The current `index.html` pulls Font Awesome from
`cdnjs.cloudflare.com` — that breaks the demo behind an air gap.

## Scope

**In scope:**

- Plain CSS Grid layout in `resources/webserver/index.html` — no framework.
  Two rows × three columns. Header (logo + future docs links area) spans the
  full width above the grid. Row 1 = existing pipeline bubbles (span all
  three columns). Row 2 = three detail panels.
- Header preserves the existing logo. A right-aligned docs-link slot is
  reserved in the header markup (link target is a follow-on, leave a stubbed
  `<a>` to `#` for now).
- Replace the Font Awesome CDN `<link>` with **inline SVG icons** for the
  five pipeline steps (camera, orchestrator, inference, system-mgr,
  compressor). Existing icon glyphs: `fa-cube`, `fa-layer-group`, `fa-cubes`.
  Replacements should be visually similar minimal SVGs (16×16 viewbox,
  `currentColor` fill so theming continues to work). Bundle them inline —
  no separate `.svg` files.
- New camera endpoints for the live preview:
  - `GET /latest-thumb` → most recent `*.thumb.png` from the camera's output
    directory, `image/png`. Returns 404 if no thumb exists yet.
  - `GET /latest-frame` → most recent `*.bmp` from the camera's output
    directory, `image/bmp`. Returns 404 if no BMP exists yet (e.g. when
    running in text-placeholder mode).
- Pre-generated thumbnails. Add one or two sample BMPs to
  `resources/camera/sample-data/` *and* their matching `*.thumb.png` files
  (200px max on long edge, generated locally via Pillow — Pillow is already
  in [resources/camera/requirements.txt](resources/camera/requirements.txt)).
  Both files are committed to the repo so the build is deterministic. A
  one-shot helper script
  `resources/camera/scripts/generate-thumbnails.py` lives next to them for
  re-running if BMPs are added later — **the script is not invoked at build
  time**.
- Camera emitter ([emitter.py](resources/camera/app/emitter.py)) must copy
  the matching `*.thumb.png` to the output directory alongside each emitted
  `*.bmp` so `/latest-thumb` and `/latest-frame` always have paired files.
  If no thumb exists for a BMP, log a warning and continue.
- Camera config ([camera-config.yaml](resources/camera/config/camera-config.yaml))
  must point `input.bmp_directory` at the actual COPYed location
  (`/opt/camera/sample-data`, not the never-COPYed `/opt/camera/bmp-input`).
- Camera Containerfile already does `COPY sample-data ./sample-data` — no
  change needed there, just confirm the path is right after the config fix.
- Row 2 panel content:
  - **Camera** — `<a target="_blank" href="http://localhost:8081/latest-frame">`
    wrapping `<img src="http://localhost:8081/latest-thumb">`. Image is
    width-constrained to the column (`max-width: 100%`). Caption below:
    filename, file_type, filesize, ts — pulled from
    `recent_files[0]` in `/status`. Auto-refresh every poll cycle (reuse
    existing `STATUS_REFRESH_MS = 10000`).
  - **Orchestrator** — `<pre><code>`-formatted JSON of `recent_files[0]`
    from `/status`. Show: `filename`, `routed_to`, `ts`, and
    `metadata.pipeline[]` (will be camera-stage-only — that's a known
    upstream gap per [watcher.py:30-35](resources/orchestrator/app/watcher.py#L30-L35),
    not this job's problem).
  - **Inference** — `<pre><code>`-formatted JSON of `recent_results[0]`
    from `/status`. Show: `filename`, `verdict`, `confidence`, `ts`, and
    the full three-stage `metadata.pipeline[]`. **This panel is the
    showpiece** — give it slightly more vertical breathing room and ensure
    long pipelines don't overflow horizontally (wrap or scroll, not push
    the column wider).
- Equal column heights are guaranteed by `grid-template-rows` and
  `align-items: stretch` so the panels line up top *and* bottom.
- All three Row-2 panels share a common `.panel` class (border, padding,
  rounded corners, white background) so they look like siblings.
- JSON formatting helper: a small `formatJson(obj)` function that emits
  pretty 2-space-indented JSON. No external library (no
  json-formatter-js, no highlight.js).
- CORS already enabled on all three services via
  `CORSMiddleware(allow_origins=["*"])` — no backend CORS work needed.

**Out of scope:**

- Authentication on `/latest-frame` or `/latest-thumb` (it's a local demo).
- Paginated history of frames — only `[0]` is shown per panel.
- WebSocket / SSE live updates — polling is preserved at the existing
  10-second cadence.
- Fixing the orchestrator's metadata-read-from-source bug
  ([watcher.py:30-35](resources/orchestrator/app/watcher.py#L30-L35)).
  Note it in the orchestrator panel's expected output and move on.
- System-Mgr and Compressor detail panels in Row 2 — those services don't
  exist yet. Row 2 has exactly three columns matching the three live
  services (camera, orchestrator, inference). System-Mgr and Compressor
  remain in Row 1's bubble strip only.
- BMP-to-PNG conversion at emit time. Thumbnails are pre-generated and
  shipped with the BMPs.
- Docs-links functionality. Header has a reserved slot but the link target
  is `#` — wiring is a follow-on job.
- Changes to `resources/webserver/index-bak.html` or `index-orig.html`
  (stale backups).

## Acceptance criteria

1. With all three pipeline services running and the camera emitting BMPs,
   the dashboard renders:
   - Header with logo (and stubbed docs-links slot).
   - Row 1: pipeline bubbles unchanged from job-3 (animation intact).
   - Row 2: three equal-width, equal-height panels (camera | orchestrator |
     inference).
2. Camera panel shows a thumbnail image that updates every poll cycle.
   Clicking the thumbnail opens the full BMP in a new tab via
   `/latest-frame`.
3. Orchestrator panel shows pretty-printed JSON of the most recent routed
   file including its `metadata.pipeline[]` (camera stage only is OK).
4. Inference panel shows pretty-printed JSON of the most recent result
   including a three-stage `metadata.pipeline[]`
   (camera → orchestrator → inference).
5. Page makes **zero external HTTP requests** (verify in DevTools Network
   tab: no `cdnjs.cloudflare.com`, no font CDNs, no Google Fonts).
6. Page is functional with Docker Desktop running on a corporate network
   that blocks `*.cloudflare.com` (the offline test).
7. With the camera service stopped, the camera panel shows a graceful
   placeholder ("Camera not reachable") instead of a broken-image icon.
   Orchestrator and inference panels show "No data yet" if their
   `recent_*` arrays are empty.
8. Columns line up both horizontally and vertically — top edges flush,
   bottom edges flush, even when the inference panel's JSON is much taller
   than the others (inference scrolls internally).
9. Works in Chrome, Edge, and Firefox (current stable).
10. Existing static-degradation guarantee from job-3 still holds: if JS
    fails to load, the static layout still renders.

## Design notes

- Grid template (target):

  ```css
  .dashboard {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    grid-template-rows: auto auto;
    gap: 1.5rem;
    max-width: 1200px;
    margin: 0 auto;
  }
  .row-pipeline { grid-column: 1 / -1; }   /* Row 1 spans all 3 cols */
  .panel { /* shared styling for Row 2 panels */ }
  .panel pre {
    max-height: 400px;
    overflow: auto;
    white-space: pre;
    font-family: ui-monospace, monospace;
    font-size: 12px;
  }
  ```

- Inline SVG icons should set `width="20"` `height="20"` `fill="currentColor"`
  so the existing `.step.up .circle { color: white; }` keeps working
  without modification.
- Camera image refresh trick: append a cache-busting `?t={Date.now()}`
  query string when re-fetching the thumb so the browser doesn't serve a
  stale cached version.
- New camera endpoint impl (sketch):

  ```python
  from fastapi.responses import FileResponse, Response

  def _latest_with_suffix(suffix: str) -> Path | None:
      out = Path(load_config()["output"]["directory"])
      files = sorted(out.glob(f"*{suffix}"), key=lambda p: p.stat().st_mtime, reverse=True)
      return files[0] if files else None

  @app.get("/latest-thumb")
  def latest_thumb():
      p = _latest_with_suffix(".thumb.png")
      if not p: return Response(status_code=404)
      return FileResponse(p, media_type="image/png")

  @app.get("/latest-frame")
  def latest_frame():
      p = _latest_with_suffix(".bmp")
      if not p: return Response(status_code=404)
      return FileResponse(p, media_type="image/bmp")
  ```

- Emitter change: after the `shutil.copy2(chosen, dest)` in
  [emitter.py:29](resources/camera/app/emitter.py#L29), also copy the
  paired thumbnail if it exists:

  ```python
  thumb_src = chosen.parent / f"{chosen.stem}.thumb.png"
  if thumb_src.exists():
      shutil.copy2(thumb_src, dest.parent / f"{dest.stem}.thumb.png")
  ```

- Thumbnail generator script (one-shot, run by a human):

  ```python
  # resources/camera/scripts/generate-thumbnails.py
  from pathlib import Path
  from PIL import Image

  SAMPLE = Path(__file__).parent.parent / "sample-data"
  for bmp in SAMPLE.glob("*.bmp"):
      thumb = bmp.with_suffix(".thumb.png")
      with Image.open(bmp) as img:
          img.thumbnail((200, 200))
          img.save(thumb, "PNG")
      print(f"  wrote {thumb.name}")
  ```

## Files expected to change

- `resources/webserver/index.html` (header markup, CSS Grid, Row 2 panels,
  inline SVGs, fetch logic, JSON formatter helper)
- `resources/webserver/Containerfile` — no change expected (verify after)
- `resources/camera/app/status.py` (two new endpoints)
- `resources/camera/app/emitter.py` (copy thumbnail alongside BMP)
- `resources/camera/config/camera-config.yaml` (fix `bmp_directory` path)
- `resources/camera/sample-data/<name>.bmp` (one or two sample BMPs)
- `resources/camera/sample-data/<name>.thumb.png` (matching thumbnails)
- `resources/camera/scripts/generate-thumbnails.py` (one-shot helper)
- `.claude/jobs/INDEX.md` (add row for job-6, mark done at end)

## Test plan

- **Camera unit**: add a test that `/latest-thumb` returns 404 with empty
  output dir, then writes a fake `.thumb.png` and asserts 200 +
  `image/png`. Repeat for `/latest-frame` with a fake `.bmp`. Keep targeted
  per code-quality rule §1 — no full-suite runs.
- **Emitter**: test that `emit_bmp_frame` copies both the BMP and the
  matching `.thumb.png` to the output dir when both exist in `sample-data`.
- **Dashboard**: manual smoke — `docker compose up -d` (or the three
  individual `docker run` commands), load `http://localhost:8080/`, verify
  all 10 acceptance criteria. Specifically check DevTools Network tab for
  zero external requests (AC #5).
- **Browser matrix**: Chrome, Edge, Firefox (current stable).
- **Offline test**: with Docker Desktop running and the host firewall
  blocking `*.cloudflare.com` (or DevTools "offline" toggled briefly after
  initial load), confirm AC #6.

## Dependencies

- Builds on `job-3` (pipeline animation) — that work is `done` and merged
  into `dev`. This branch cuts from current `dev`.
- No new Python deps (Pillow already present).
- No new JS deps (plain CSS + vanilla JS).

## Notes

- The "showpiece" framing for the inference panel is deliberate. The whole
  point of the demo is the **chained metadata** — that's what proves the
  mesh is doing real work. Make sure the inference JSON renders the
  `pipeline` array readably even when long: enable internal `overflow:
  auto` on the `<pre>`, don't let it push the column wider.
- Inline SVG icons keep the offline story simple, but they're not
  iconographically identical to Font Awesome. Pick shapes that read
  clearly at 20×20 — a cube for camera, stacked layers for orchestrator,
  multiple cubes for inference, gear for system-mgr, archive-box for
  compressor.
- If the corporate firewall (Netskope) blocks the BMP fetch via
  `localhost:8081/latest-frame` due to SSL inspection, that's a different
  problem — it shouldn't apply to loopback, but flag it in `blockers` if
  it does.

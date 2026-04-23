---
id: job-3
title: Dashboard pipeline flow animation — traveling bubble on progress line
status: not-started
branch: feature/pipeline-flow-animation
base-branch: dev
assigned: Sean
sp: 3
security-scan: not-required
---

# Job 3 — Pipeline flow animation

## Why

Today's dashboard at `http://localhost:8080/` shows service-state bubbles (Camera,
Orchestrator, Inference, System Mgr, Compressor) plus a static progress bar that
sits flush out to the last live step. A viewer can't tell at a glance that *data is
actually moving* through the pipeline — only that the services are reachable.

For the Cisco AI Pod demo (2026-05-20) the visual must communicate motion. A
flowing bubble that travels left → right along the progress line, passing through
each `up` component, is the cheapest way to sell "frames are moving through the
mesh" without adding telemetry.

## Scope

**In scope:**

- An animated "packet" bubble (small filled circle) that travels along the
  progress line from the left edge up to the last `up` step, then loops.
- Animation only runs across components whose step state is `.up` (solid indigo).
  A `.down` or `.starting` (dashed) component halts the bubble at the last `.up`
  component to its left.
- Multiple bubbles in flight at once (staggered) so the line always looks active
  when the pipeline is healthy.
- Bubble visually "passes through" each `up` component circle (continues on the
  same Y-axis — does not go over or under the circle).
- CSS + vanilla JS only — no new dependencies, no framework.
- Animation pauses gracefully when the tab is hidden (`document.visibilityState`).

**Out of scope:**

- Coupling bubble speed to real throughput (frames/second from `/status`). That's
  a follow-on. This job ships a constant-speed visual.
- New backend endpoints.
- Any change to `resources/webserver/index-bak.html` (stale backup).
- System Mgr / Compressor status wiring — they remain dashed; the bubble simply
  stops before them.

## Acceptance criteria

1. With all four live services `up`, the bubble travels from the left edge of the
   pipeline to the rightmost `up` step (Inference), then fades out and a new
   bubble starts from the left. Cadence: a new bubble every ~1.5s, travel time
   ~3s across the full visible progress line.
2. With `inference` stopped (`docker compose stop inference`), the bubble
   animation retracts with the progress bar and stops at Orchestrator. No bubble
   travels past the last `up` step.
3. Restarting `inference` resumes bubble travel to the Inference step without a
   page refresh.
4. No visible jank when the browser tab is backgrounded and restored.
5. Works in Chrome, Edge, and Firefox at their current stable versions.
6. Dashboard still functional if JavaScript fails to load — the static progress
   bar and step circles render correctly (graceful degradation).

## Design notes

- Implementation lives entirely in `resources/webserver/index.html` (inline CSS +
  inline JS). No new files. No nginx config changes.
- Preferred technique: a single `.flow-bubble` element per in-flight bubble,
  absolutely positioned over `.pipeline-progress`, animated via CSS
  `@keyframes` + `transform: translateX()`. The animation's end position is a
  CSS custom property (`--flow-max-x`) updated by the same JS that updates the
  progress bar width (`updatePipelineProgress` at `index.html:163`).
- Bubble spawn cadence: a `setInterval` that appends a new `.flow-bubble` node
  and removes it on `animationend`.
- Respect `prefers-reduced-motion: reduce` — fall back to a single static marker
  that hops to each `up` step on status updates instead of continuous animation.

## Files expected to change

- `resources/webserver/index.html` (inline style block + markup + script block)

## Test plan

- Manual smoke: `docker compose up -d`, load dashboard, verify bubble flow.
- Manual degradation: stop each service in turn, confirm bubble retracts.
- Manual browser matrix: Chrome, Edge, Firefox.
- Automated: none required for a CSS/JS-only visual change; the static-dashboard
  graceful-degradation check is an eyeball test during PR review.

## Dependencies

- Blocked on: `job-1` (local-dev-compose) merging into `dev`. This job's feature
  branch must be cut from `dev` after that merge lands.

## Notes

- Keep the bubble subtle — a small dot (6-8px), ~60% opacity, same indigo as
  `.step.up .circle`. The goal is "line is alive," not "look at this bubble."
- If we later want to couple speed to real throughput, the hook is: read
  `frames_emitted` delta from the camera `/status` poll and scale the
  `animation-duration` CSS variable. Deferred.

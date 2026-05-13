---
id: job-8
title: Panel change indicators — cross-fade on content update
status: not-started
branch: feature/panel-change-indicators
base-branch: dev
assigned: Sean
sp: 2
security-scan: not-required
---

# Job 8 — Panel change indicators

## Why

The three bottom-row panels (Camera, Orchestrator, Inference) update on a
10-second poll cycle. There is no visual cue when content changes — a viewer
watching the dashboard can't tell at a glance whether they're looking at fresh
data or the same payload as 10 seconds ago. A snappy cross-fade on actual
change closes that gap without disrupting the layout or adding visual noise.

## Acceptance criteria

1. When the camera thumbnail changes (new `thumb_filename`), the `<img>` element
   cross-fades: opacity 1 → 0.3 → 1 over 250ms.
2. When the orchestrator JSON changes (new `recent_files[0].filename`), the
   `<pre>` block cross-fades over 250ms.
3. When the inference JSON changes (new `recent_results[0].ts`), the `<pre>`
   block cross-fades over 250ms.
4. Animation fires **only when the tracked value differs** from the previous
   poll — not on every poll cycle and not on the initial load.
5. Animation is CSS-only (`@keyframes` + a toggled class). No JS animation
   libraries. No `setTimeout` used to drive the animation itself.
6. `prefers-reduced-motion` is respected — animation is suppressed when set.
7. All three panels use the same CSS class and keyframe. The natural difference
   in visual weight (image vs. text) provides the panel-specific feel without
   special-casing.
8. All existing dashboard behavior (pipeline bubbles, status polling, caption
   text, click-through to /latest-frame) is unaffected.

## Implementation plan

### CSS additions (index.html `<style>`)

```css
@keyframes panel-flash {
  0%   { opacity: 1;   }
  40%  { opacity: 0.3; }
  100% { opacity: 1;   }
}

.panel-updated {
  animation: panel-flash 250ms ease-out forwards;
}

@media (prefers-reduced-motion: reduce) {
  .panel-updated { animation: none; }
}
```

Apply `.panel-updated` to:
- `#camera-thumb` (the `<img>`) — not the panel wrapper
- `#orchestrator-detail` (the `<pre>`)
- `#inference-detail` (the `<pre>`)

### JS additions (index.html `<script>`)

**Change tracking state** — three module-level variables:

```js
let lastCameraThumb      = null;
let lastOrchestratorFile = null;
let lastInferenceTs      = null;
```

**Helper** — adds the class, removes it on `animationend` so it can re-trigger:

```js
function flashElement(el) {
  el.classList.remove("panel-updated");
  // Force reflow so removing + re-adding the class triggers a new animation
  void el.offsetWidth;
  el.classList.add("panel-updated");
  el.addEventListener("animationend", () => el.classList.remove("panel-updated"), { once: true });
}
```

**Camera panel** — in `updateCameraPanel`, after setting `thumb.src`, before
updating the caption:

```js
const newThumb = thumbName || null;
if (lastCameraThumb !== null && newThumb !== lastCameraThumb) {
  flashElement(thumb);
}
lastCameraThumb = newThumb;
```

**Orchestrator panel** — in `updateOrchestratorPanel`, after writing
`pre.textContent`:

```js
const newFile = recent && recent.filename || null;
if (lastOrchestratorFile !== null && newFile !== lastOrchestratorFile) {
  flashElement(pre);
}
lastOrchestratorFile = newFile;
```

**Inference panel** — in `updateInferencePanel`, after writing
`pre.textContent`:

```js
const newTs = recent && recent.ts || null;
if (lastInferenceTs !== null && newTs !== lastInferenceTs) {
  flashElement(pre);
}
lastInferenceTs = newTs;
```

### Why `null` guard on first poll

`lastX === null` on first load — the guard `lastX !== null` prevents the
animation firing on initial data population, which would look like an error
state rather than a meaningful update.

## Files

- `resources/webserver/index.html` — CSS keyframe + class, JS state vars +
  flashElement helper, per-panel change detection

## Out of scope

- Border pulse, badge/chip, or background flash (parked — revisit if fade alone
  is insufficient feedback in demo conditions)
- Any backend changes
- Changes to poll interval or status endpoint shapes

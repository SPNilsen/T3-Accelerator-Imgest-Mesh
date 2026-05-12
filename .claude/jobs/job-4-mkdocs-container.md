---
id: job-4
title: MkDocs site as a standalone container + dashboard link (new tab)
status: not-started
branch: feature/mkdocs-container
base-branch: dev
assigned: Sean
sp: 4
security-scan: not-required
---

# Job 4 — MkDocs site as a standalone container

## Why

`mkdocs.yml` at the repo root describes a Material-for-MkDocs site covering
every section of `docs/` (armor, crisp-dm, hpc, t3, dev, workshop, assessment,
blog, etc.) with a heavy plugin set. `resources/mkdocs/Container` already
extends `squidfunk/mkdocs-material` with the nine plugins the site needs.
None of it is currently served — there's no compose service, no Route, no
dashboard link.

Shipping it as its own container (not bundled into the :8080 dashboard) keeps
concerns separate: the dashboard is a small operational monitor, the docs are
a large content site with a very different rebuild cadence. The split also
gives us a clean OpenShift story for the Cisco AI Pod demo — two Deployments,
two Routes, no coupling.

## Scope

**In scope:**

- New compose service `docs` that builds the Material site and serves it.
- Container strategy: multi-stage Containerfile — stage 1 runs `mkdocs build`
  against the repo-root `mkdocs.yml`; stage 2 is `nginx-unprivileged:stable-alpine`
  serving the built `site/` directory (same base image the status webserver
  uses, same unprivileged pattern).
- Default host port `:8000` (mkdocs convention). Container listens on `8080`
  internally to match the webserver pattern.
- Dashboard link: add a small "Docs" link/button to
  `resources/webserver/index.html` that opens the docs site in a **new tab**
  (`target="_blank" rel="noopener noreferrer"`). Clicking it must not navigate
  the pipeline page away or interrupt the status-polling loop.
- K8s manifest set under `resources/k8s/docs/` mirroring
  `resources/k8s/webserver/deployment.yaml` — Deployment + Service + Route
  (suggested Route host: `docs.<pod>` alongside `pipeline.<pod>`).
- Update `docs/dev/local-dev.md` with the new port/URL and the dashboard link.
- Update `docs/dev/demo-guide.md` to mention the docs link in the 5-minute
  demo as a throwaway (one line — not a new beat).

**Out of scope:**

- MkDocs live-serve / hot-reload mode. We ship a build-once static site; a
  dev `mkdocs serve` workflow can be a future toggle.
- GitHub Pages / object-store publishing. Deferred — the containerized
  deployment is what matters for the Cisco demo's air-gapped story.
- Search-index tuning, theme customization beyond what `mkdocs.yml` already
  defines, or any doc-content edits.
- Any change to `docs/armor/` (read-only constraint).

## Acceptance criteria

1. `docker compose up -d docs` serves the Material site at
   `http://localhost:8000`, full navigation intact.
2. All plugins declared in `mkdocs.yml` build cleanly — no plugin-not-found
   errors, no missing-asset warnings for referenced images/drawio/pdf.
3. `docs/armor/*.md` renders through the site without being modified.
4. The status dashboard at `http://localhost:8080` displays a small,
   unobtrusive "Docs" link that opens `http://localhost:8000` in a new
   browser tab. Clicking it does **not** navigate the pipeline page away.
5. After clicking the Docs link, the pipeline page's status polling and
   flow-bubble animation continue uninterrupted in the original tab.
6. If the `docs` container is stopped, the Docs link remains visible and
   clickable (it will fail to load in the new tab — that's acceptable
   degradation; no JS-driven hide/show needed).
7. `docker compose down docs` stops only the docs service; the pipeline
   stack keeps running.
8. K8s manifest under `resources/k8s/docs/deployment.yaml` follows the
   webserver manifest shape (same image pattern, same readiness probe,
   same Route style).

## Design notes

- **Containerfile** lives at `resources/docs/Containerfile` (new directory),
  multi-stage:

  ```dockerfile
  # Stage 1 — build
  FROM squidfunk/mkdocs-material AS build
  RUN pip install --no-cache-dir \
      mkdocs-macros-plugin mkdocs-glightbox mkdocs-mermaid2-plugin \
      mkdocs-charts-plugin mkdocs-pdf mkdocs-gallery \
      mkdocs-git-latest-changes-plugin \
      mkdocs-git-revision-date-localized-plugin \
      mkdocs-drawio-file
  WORKDIR /site
  COPY mkdocs.yml /site/mkdocs.yml
  COPY docs /site/docs
  RUN mkdocs build --strict=false -d /site/build

  # Stage 2 — serve
  FROM nginxinc/nginx-unprivileged:stable-alpine
  COPY --from=build /site/build /usr/share/nginx/html
  COPY resources/docs/nginx.conf /etc/nginx/conf.d/default.conf
  EXPOSE 8080
  CMD ["nginx", "-g", "daemon off;"]
  ```

  The existing `resources/mkdocs/Container` is a scratch file with the
  plugin list — keep it as reference during migration and remove once the
  new Containerfile ships.
- **Compose block** mirrors `webserver`:

  ```yaml
  docs:
    build:
      context: .
      dockerfile: resources/docs/Containerfile
    image: imgest-mesh/docs:dev
    container_name: imgest-docs
    ports:
      - "8000:8080"
    restart: unless-stopped
  ```

  `build.context` is the repo root (not `resources/docs/`) because the build
  stage needs to `COPY mkdocs.yml` and the whole `docs/` tree. That's a
  compromise — it sends a larger build context to the daemon — but it's the
  simplest shape and matches how mkdocs expects the project layout.
- **Dashboard link** — add to `resources/webserver/index.html`, near the
  logo block. Minimal markup:

  ```html
  <a href="http://localhost:8000" target="_blank" rel="noopener noreferrer"
     class="docs-link" title="Open project documentation in a new tab">
    <i class="fa-solid fa-book"></i> Docs
  </a>
  ```

  `target="_blank"` + `rel="noopener noreferrer"` is the critical pair —
  `noopener` prevents the new tab from accessing the pipeline page via
  `window.opener`, which also forces the browser to open a truly independent
  tab so the pipeline page is never touched.
- **Link styling** should be subtle — fixed-position top-right, small,
  muted-grey text that colors to indigo on hover. Don't compete with the
  pipeline visuals.
- **URL portability.** The hard-coded `http://localhost:8000` is fine for
  laptop demo. For OpenShift, either (a) templating at image-build time via
  a `DOCS_URL` env var and a tiny substitution step in the webserver
  entrypoint, or (b) a relative link assuming `docs.<pod>` is reachable.
  Defer the portability decision to `job-2` when manifests land.

## Files expected to change

- `resources/docs/Containerfile` (new)
- `resources/docs/nginx.conf` (new — same shape as webserver's)
- `docker-compose.yml` — add `docs:` block
- `resources/webserver/index.html` — Docs link markup + CSS
- `resources/k8s/docs/deployment.yaml` (new) + Service + Route siblings
- `docs/dev/local-dev.md` — mention `:8000` and link
- `docs/dev/demo-guide.md` — one-line mention in the 5-min beat

## Test plan

- Build: `docker compose build docs` — no plugin errors.
- Smoke: `docker compose up -d docs && curl -sI http://localhost:8000` → 200.
- Navigation: open `http://localhost:8000`, click through the nav: armor,
  crisp-dm, hpc, t3, dev sections — no 404s.
- Dashboard link: open `http://localhost:8080`, click the Docs link →
  new tab opens at `:8000`. Original tab's URL unchanged. Wait 30 s on the
  original tab and confirm pipeline bubble animation still running
  (status poll log in DevTools Network panel still firing every 10 s).
- Degradation: `docker compose stop docs`, refresh `:8080`, click Docs —
  new tab opens and fails to load. Pipeline page unaffected.
- Browser matrix: Chrome, Edge, Firefox — all honor
  `target="_blank" rel="noopener"` identically; quick smoke only.

## Dependencies

- None. Independent of `job-2` (Cisco manifests) though they'll share the
  Route pattern. Can ship before, after, or in parallel.

## Notes

- Build context is the repo root — add a `.dockerignore` or scope the COPY
  carefully to avoid shipping `.data/`, `.git/`, `.claude/`, or `node_modules`
  into the build stage. These aren't sensitive per se but they bloat the
  image and slow rebuilds.
- The `mkdocs build --strict=false` is deliberate — some of the referenced
  assets (drawio, PDFs) may warn but not fail; strict mode would turn a
  warning into a build failure. We want the site to build even when Sean
  is iterating on docs content. Flip to `--strict` once content is stable.
- The existing `resources/mkdocs/` directory (with `Container` +
  `README.md`) is Doug's scaffolding — preserve the README reference to
  the containerd/nerdctl workflow but move the plugin list into the new
  Containerfile at `resources/docs/Containerfile`. Delete
  `resources/mkdocs/` only after the new path is proven.

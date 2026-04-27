---
id: job-5
title: Linked JNJ-Armor docs container — surface customer docs alongside generic platform docs
status: not-started
branch: feature/jnj-armor-docs-container
base-branch: dev
assigned: Sean
sp: 4
security-scan: not-required
---

# Job 5 — Linked JNJ-Armor docs container

## Why

The Cisco AI Pod demo narrative is *"the generic Imgest-Mesh platform running
JNJ-Armor's customer-specific models."* Imgest-Mesh is the generic
implementation of the Armor project; the demo runs against JNJ-Armor's models
and references customer-specific content. Surfacing both repos' docs side by
side reinforces that narrative.

Today, four `mkdocs.yml` nav entries reference JNJ-Armor-only content
(`t3/exec-overview.md`, `t3/filemap.md`, `crisp-dm/additional.md`,
`crisp-dm/lessons-learned.md`) and 404 in this repo's docs site. Two ways to
fix:

1. Copy the files verbatim — fast, but introduces drift, two-places-to-edit,
   and a `filemap.md` that describes the *wrong* repo.
2. Stand up a second docs container that builds *JNJ-Armor's* MkDocs site
   from the sibling repo on the host, served on its own port. Cross-link from
   Imgest-Mesh's nav and dashboard. No content duplication.

This job picks (2). Cleaner OpenShift story (two Deployments, two Routes),
cleaner content boundary (each repo owns its docs), and matches the demo's
"generic platform + customer engagement, side by side" framing.

The long-term architecture recommendation from `delta/jnj-armor-comparison.md`
(separate repos + a thin shared MkDocs package post-demo) is unchanged — this
is the demo-time bridge, not a permanent merge of concerns.

## Scope

**In scope:**

- New compose service `jnj-armor-docs` that builds JNJ-Armor's MkDocs site
  from the sibling repo on the host. Path resolved via
  `JNJ_ARMOR_REPO_PATH` env var, defaulting to `../T3-Accelerator-JNJ-Armor`
  (sibling-clone convention).
- Container listens on `:8080` internally; exposed on host `:8001`
  (next allocation after `:8000` docs).
- Build spec inline in `docker-compose.yml` via `dockerfile_inline` so this
  repo carries the build instruction without requiring any edit to the
  JNJ-Armor repo.
- Remove the four orphan entries from this repo's `mkdocs.yml` nav. Add an
  optional "JNJ-Armor Project" section with external links to the linked
  container's URLs (defer the URL-portability question to job-2 alongside
  the existing `:8000` dashboard link).
- Add a second top-right "JNJ-Armor Docs" link on the dashboard, same
  `target="_blank" rel="noopener noreferrer"` pattern as the existing Docs
  link. Side-by-side or stacked layout, subtle.
- K8s manifests under `resources/k8s/jnj-armor-docs/` mirroring
  `resources/k8s/docs/`. Suggested Route host: `jnj-armor-docs.<pod>`
  alongside `docs.<pod>` and `pipeline.<pod>`.
- Update `.env.example` to document `JNJ_ARMOR_REPO_PATH`.
- Update `docs/dev/local-dev.md` port table + linked-container note.
- Update `docs/dev/demo-guide.md` 5-min beat to mention the second docs link.

**Out of scope:**

- Any edit to the JNJ-Armor repo. It stays clean. This repo carries the
  build instruction (via `dockerfile_inline`).
- Cross-linking from JNJ-Armor docs back to Imgest-Mesh (would require
  editing JNJ-Armor's `mkdocs.yml`).
- Production CI/registry pipeline for the JNJ-Armor docs image. For
  OpenShift, the build-from-host pattern won't work — the image must be
  built in JNJ-Armor's CI and pushed to a registry. Deferred to job-2 or a
  follow-on, where the manifest will reference a registry tag instead of a
  local build context.
- Search-index unification across the two sites. They search independently.
- Editing any nav or content in `docs/armor/` (read-only constraint
  upheld; the linked container makes the read-only rule even more
  defensible).

## Acceptance criteria

1. `JNJ_ARMOR_REPO_PATH=../T3-Accelerator-JNJ-Armor docker compose up -d jnj-armor-docs`
   builds and serves the full JNJ-Armor MkDocs site at
   `http://localhost:8001` — including the four pages that currently 404
   in this repo (`/t3/exec-overview.html`, `/t3/filemap.html`,
   `/crisp-dm/additional.html`, `/crisp-dm/lessons-learned.html`).
2. Imgest-Mesh's `mkdocs.yml` nav no longer lists the four orphan entries.
   `http://localhost:8000` site has zero broken nav links.
3. Imgest-Mesh dashboard at `http://localhost:8080` has two top-right
   links: **Docs** (→ `:8000`) and **JNJ-Armor Docs** (→ `:8001`). Both
   open in new tabs; clicking either does not navigate the pipeline page
   away. Status polling and flow-bubble animation continue uninterrupted
   in the original tab.
4. With `jnj-armor-docs` stopped, the dashboard's JNJ-Armor Docs link
   remains visible and clickable; the new tab fails to load gracefully;
   the pipeline page is unaffected. (Same degradation contract as the
   existing Docs link.)
5. K8s manifest set under `resources/k8s/jnj-armor-docs/` follows the
   `resources/k8s/docs/` shape: Deployment + Service + Route with
   matching labels and probes.
6. Build is reproducible from a fresh clone of *this* repo plus a sibling
   clone of `T3-Accelerator-JNJ-Armor` at the default path or at the path
   pointed to by `JNJ_ARMOR_REPO_PATH`. README/local-dev doc explains the
   sibling-checkout requirement clearly.
7. `docker compose down jnj-armor-docs` stops only the linked container;
   pipeline + Imgest-Mesh docs stay running.

## Design notes

- **Compose block — `dockerfile_inline` keeps the build spec in this repo.**
  Compose v2.20+ supports inline Dockerfiles. Reuses the same plugin set as
  the existing `resources/docs/Containerfile`:

  ```yaml
  jnj-armor-docs:
    build:
      context: ${JNJ_ARMOR_REPO_PATH:-../T3-Accelerator-JNJ-Armor}
      dockerfile_inline: |
        FROM squidfunk/mkdocs-material AS build
        RUN pip install --no-cache-dir \
            mkdocs-macros-plugin mkdocs-glightbox mkdocs-mermaid2-plugin \
            mkdocs-charts-plugin mkdocs-pdf mkdocs-gallery \
            mkdocs-git-latest-changes-plugin \
            mkdocs-git-revision-date-localized-plugin mkdocs-drawio-file
        WORKDIR /site
        COPY mkdocs.yml /site/mkdocs.yml
        COPY docs /site/docs
        COPY .git /site/.git
        RUN mkdocs build -d /site/build
        FROM nginxinc/nginx-unprivileged:stable-alpine
        COPY --from=build /site/build /usr/share/nginx/html
        EXPOSE 8080
    image: imgest-mesh/jnj-armor-docs:dev
    container_name: imgest-jnj-armor-docs
    ports:
      - "8001:8080"
    restart: unless-stopped
  ```

- **`.env.example` addition** — single line with the default sibling path
  and a comment explaining the override.

- **`mkdocs.yml` nav** — remove the four orphan entries. Optionally add a
  small "JNJ-Armor Project" external-link section near the bottom of the
  nav. The MkDocs format for external links:
  ```yaml
  - 'JNJ-Armor Project':
    - 'Executive Overview': 'http://localhost:8001/t3/exec-overview.html'
    - 'Filemap':            'http://localhost:8001/t3/filemap.html'
    - 'Additional Notes':   'http://localhost:8001/crisp-dm/additional.html'
    - 'Lessons Learned':    'http://localhost:8001/crisp-dm/lessons-learned.html'
  ```
  Hard-coded localhost is fine for the demo; portable templating is a
  job-2 concern (same constraint as the existing dashboard Docs link).

- **Dashboard layout** — second link to the right of the existing Docs
  link, same styling. Stack vertically if width gets cramped.

- **Build context = sibling repo.** This means anyone who clones only this
  repo and tries `docker compose up jnj-armor-docs` will get a build
  failure pointing at the missing path. That's an explicit, documented
  failure mode; the README + `docs/dev/local-dev.md` both call out the
  sibling-checkout prerequisite. For the demo we accept the constraint;
  for OpenShift the image is registry-pulled, not built locally.

- **`.git` requirement** — the `git-revision-date-localized` and
  `git-latest-changes` plugins need it (same constraint as the existing
  `docs` container). Build context includes `.git` from the sibling repo.

## Files expected to change

- `docker-compose.yml` — add `jnj-armor-docs` service block, port comment
- `.env.example` — `JNJ_ARMOR_REPO_PATH` entry
- `mkdocs.yml` — remove 4 orphan nav entries, optional external-link section
- `resources/webserver/index.html` — second dashboard link + minor CSS
- `resources/k8s/jnj-armor-docs/deployment.yaml` (new)
- `resources/k8s/jnj-armor-docs/service.yaml` (new)
- `resources/k8s/jnj-armor-docs/route.yaml` (new)
- `docs/dev/local-dev.md` — port table + sibling-checkout requirement
- `docs/dev/demo-guide.md` — 5-min beat one-liner
- `README.md` — update if it lists ports or the sibling-checkout step

## Test plan

- **Build:** `JNJ_ARMOR_REPO_PATH=../T3-Accelerator-JNJ-Armor docker compose build jnj-armor-docs` — no plugin errors, build completes.
- **Smoke:** `docker compose up -d jnj-armor-docs && curl -sI http://localhost:8001` → 200.
- **Orphan resolution:** `curl -sI http://localhost:8001/t3/exec-overview.html` → 200 (and the other three).
- **Imgest-Mesh nav:** `curl -s http://localhost:8000/` → no internal links to the four removed nav targets.
- **Dashboard:** open `http://localhost:8080`, click each docs link in turn → new tab opens at `:8000` or `:8001`. Pipeline tab URL unchanged. Status polling visible in DevTools Network panel.
- **Degradation:** `docker compose stop jnj-armor-docs` → JNJ-Armor Docs link still visible on dashboard; new tab fails; pipeline page unaffected. Same for stopping `docs`.
- **Browser matrix:** Chrome, Edge, Firefox.

## Dependencies

- `T3-Accelerator-JNJ-Armor` checked out at `../T3-Accelerator-JNJ-Armor`
  (or env-overridden path). Documented requirement; no automation around
  it for now.
- Compose v2.20+ for `dockerfile_inline` support. Verify before starting.

## Notes

- This is a *demo-time* pattern, not a permanent architecture. The
  `delta/jnj-armor-comparison.md` recommendation (separate repos +
  thin shared MkDocs package post-demo) still holds long-term. This
  job is the bridge.
- The `armor/models.md` we copied earlier this session stays where it
  is — it's already in `docs/armor/`, the read-only notice is in place,
  and the linked container surfaces *additional* JNJ-Armor pages
  rather than replacing the few we've already pulled in.
- If later we want a single dashboard link with a dropdown/menu instead
  of two side-by-side links, that's a small UX iteration on top of this
  job — not in this scope.

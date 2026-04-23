# Role Profile — Backend

## Scope in this project
Python 3 + FastAPI services under `resources/`:
- `camera/` — image ingestion (capture, emitter, status, config)
- `orchestrator/` — pipeline routing, watcher
- `inference/` — model worker (GPU-bound in prod, needs CPU/mock mode for dev)

## Conventions
- Each service has `app/` package with `main.py`, `config.py`, `status.py`
- Configs: YAML files in `resources/{service}/config/`
- Dependencies: per-service `requirements.txt`
- Container build: per-service `Containerfile`

## Things to know
- No tests exist yet — new code should add pytest coverage
- No shared library between services — each is self-contained
- Image registry: `registry.gitlab.com/dosayles/t3-imgest-mesh/*`

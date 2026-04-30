#!/usr/bin/env bash
set -euo pipefail

echo "[orchestrator] starting orchestrator service..."
python -m app.main

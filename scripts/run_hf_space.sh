#!/usr/bin/env bash
set -euo pipefail

# Hugging Face Spaces expose a single public port (default 7860 via $PORT).
# OpenEnv evaluators must be able to call POST /reset on the public port.
# Therefore, in Spaces we serve the FastAPI OpenEnv endpoints on 0.0.0.0:$PORT.

LISTEN_PORT="${PORT:-7860}"

exec uvicorn server.app:app --host 0.0.0.0 --port "${LISTEN_PORT}"

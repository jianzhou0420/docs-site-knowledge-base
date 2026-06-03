#!/usr/bin/env bash
# Launch the docs/ live-reload dev server (pure-stdlib HTTP + SSE).
# No pip, no npm, no build — just Python's standard library.
#
# Usage:
#   ./run_dev.sh                  # port 8002
#   ./run_dev.sh 9000             # custom port
#   INTERVAL=1.0 ./run_dev.sh     # slower file-watch poll (default 0.5s)
#   HOST=127.0.0.1 ./run_dev.sh   # bind localhost only (default 0.0.0.0)

set -e
cd "$(dirname "$0")"

PORT=${1:-8002}
INTERVAL=${INTERVAL:-0.5}
HOST=${HOST:-0.0.0.0}

PYTHON=${PYTHON:-python3}
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "error: '$PYTHON' not found on PATH. Install Python 3, or set PYTHON=/path/to/python3." >&2
  exit 1
fi

GREEN='\033[0;32m'; BLUE='\033[0;34m'; DIM='\033[2m'; NC='\033[0m'
echo -e "${GREEN}=== Doc-Site — Live Reload ===${NC}"
echo -e "${BLUE}URL    :${NC} http://${HOST}:${PORT}/"
echo -e "${BLUE}Root   :${NC} $(pwd)/docs"
echo -e "${BLUE}Python :${NC} $(command -v "$PYTHON") ($("$PYTHON" --version 2>&1))"
echo -e "${DIM}Ctrl+C to stop.${NC}"
echo ""

# Forward SIGINT/SIGTERM into the python child so Ctrl+C is responsive.
cleanup() {
  if [ -n "${SERVER_PID:-}" ]; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
  exit 0
}
trap cleanup SIGINT SIGTERM

"$PYTHON" docs/_lib/_serve.py --host "$HOST" --port "$PORT" --interval "$INTERVAL" &
SERVER_PID=$!
wait "$SERVER_PID"

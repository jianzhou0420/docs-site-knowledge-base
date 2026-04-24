#!/usr/bin/env bash
# Launch local dev server with live reload.
# Pick the mkdocs binary from your active environment; default to $PATH.

set -euo pipefail
cd "$(dirname "$0")"
exec mkdocs serve -a 127.0.0.1:8001

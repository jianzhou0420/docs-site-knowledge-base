#!/usr/bin/env bash
# Launch local dev server with live reload.
# Resolves mkdocs in this order:
#   1) on $PATH (your active environment)
#   2) conda env named "docsite-kb" (the convention env for this scaffold)
#   3) ~/.local/bin/mkdocs (user pip install)

set -euo pipefail
cd "$(dirname "$0")"

try_mkdocs() {
  # A candidate counts only if it can actually run --version
  [ -x "$1" ] && "$1" --version >/dev/null 2>&1
}

find_mkdocs() {
  # 1) Project-convention conda env (verified install)
  local conda_env="${HOME}/miniforge3/envs/docsite-kb/bin/mkdocs"
  if try_mkdocs "$conda_env"; then echo "$conda_env"; return 0; fi

  # 2) Active env on $PATH
  if command -v mkdocs >/dev/null 2>&1; then
    local path_bin
    path_bin=$(command -v mkdocs)
    if try_mkdocs "$path_bin"; then echo "$path_bin"; return 0; fi
  fi

  # 3) User pip install
  local local_bin="${HOME}/.local/bin/mkdocs"
  if try_mkdocs "$local_bin"; then echo "$local_bin"; return 0; fi

  return 1
}

if ! MKDOCS=$(find_mkdocs); then
  cat >&2 <<EOF
error: mkdocs not found.

Install dependencies with one of:
  pip install -r requirements.txt
  conda create -n docsite-kb python=3.11 && conda activate docsite-kb && pip install -r requirements.txt

Then re-run ./run_dev.sh
EOF
  exit 1
fi

echo "Using mkdocs at: $MKDOCS"
# --livereload is the documented default but mkdocs 1.6 silently skips
# starting the file watcher when stdout is not a TTY (e.g. backgrounded
# with `&`). Pass it explicitly so watchdog/inotify always engages.
exec "$MKDOCS" serve --livereload -a 0.0.0.0:8002

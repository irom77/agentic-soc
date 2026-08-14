#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"

if [[ -x "$BACKEND_DIR/.venv/Script/python.exe" ]]; then
  PYTHON="$BACKEND_DIR/.venv/Script/python.exe"
elif [[ -x "$BACKEND_DIR/.venv/bin/python" ]]; then
  PYTHON="$BACKEND_DIR/.venv/bin/python"
else
  echo "Backend Python was not found. Run 'cd backend && uv sync --frozen' first." >&2
  exit 1
fi

cd "$BACKEND_DIR"
exec "$PYTHON" manage.py test "$@"

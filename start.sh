#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNTIME_DIR="$ROOT_DIR/.asp-runtime"
COMPOSE_FILE="$ROOT_DIR/development/docker/compose.yaml"

mkdir -p "$RUNTIME_DIR"

start_container() {
  local service="$1"
  local container="$2"

  if docker container inspect "$container" >/dev/null 2>&1; then
    docker start "$container" >/dev/null
  else
    docker compose -f "$COMPOSE_FILE" up -d "$service"
  fi
}

is_running() {
  local pid_file="$1"
  [[ -f "$pid_file" ]] && kill -0 "$(<"$pid_file")" 2>/dev/null
}

start_process() {
  local name="$1"
  local working_dir="$2"
  local command="$3"
  local pid_file="$RUNTIME_DIR/$name.pid"
  local log_file="$RUNTIME_DIR/$name.log"

  if is_running "$pid_file"; then
    echo "$name is already running (PID $(<"$pid_file"))."
    return
  fi

  rm -f "$pid_file"
  (
    cd "$working_dir"
    exec setsid bash -c "exec $command"
  ) >>"$log_file" 2>&1 &
  local pid=$!
  echo "$pid" >"$pid_file"

  sleep 1
  if ! kill -0 "$pid" 2>/dev/null; then
    rm -f "$pid_file"
    echo "$name failed to start. See $log_file" >&2
    tail -n 20 "$log_file" >&2
    return 1
  fi

  echo "$name started (PID $pid; log: $log_file)."
}

command -v docker >/dev/null || { echo "docker is required." >&2; exit 1; }
command -v uv >/dev/null || { echo "uv is required." >&2; exit 1; }
command -v pnpm >/dev/null || { echo "pnpm is required." >&2; exit 1; }

start_container postgres asp-dev-postgres
start_container redis-stack asp-dev-redis-stack
start_container rustfs asp-dev-rustfs

start_process backend "$ROOT_DIR/backend" \
  "uv run python -m uvicorn asp.asgi:application --host 127.0.0.1 --port 8001"
start_process case-analysis-worker "$ROOT_DIR/backend" \
  "uv run python manage.py run_agentic_case_analysis_worker"
start_process frontend "$ROOT_DIR/frontend" \
  "pnpm dev -- --host 127.0.0.1 --port 5173"

echo "ASP is available at http://localhost:5173"

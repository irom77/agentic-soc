#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNTIME_DIR="$ROOT_DIR/.asp-runtime"

stop_process() {
  local name="$1"
  local pid_file="$RUNTIME_DIR/$name.pid"

  if [[ ! -f "$pid_file" ]]; then
    echo "$name is not running (no PID file)."
    return
  fi

  local pid
  pid="$(<"$pid_file")"
  if kill -0 "$pid" 2>/dev/null; then
    kill -TERM -- "-$pid" 2>/dev/null || kill -TERM "$pid" 2>/dev/null || true
    for _ in {1..20}; do
      kill -0 "$pid" 2>/dev/null || break
      sleep 0.25
    done
    if kill -0 "$pid" 2>/dev/null; then
      kill -KILL -- "-$pid" 2>/dev/null || kill -KILL "$pid" 2>/dev/null || true
    fi
    echo "$name stopped."
  else
    echo "$name was not running; removed stale PID file."
  fi
  rm -f "$pid_file"
}

stop_process frontend
stop_process case-analysis-worker
stop_process backend

for container in asp-dev-rustfs asp-dev-redis-stack asp-dev-postgres; do
  if docker container inspect "$container" >/dev/null 2>&1; then
    docker stop "$container" >/dev/null
    echo "$container stopped."
  fi
done

echo "ASP stopped. Database volumes were preserved."

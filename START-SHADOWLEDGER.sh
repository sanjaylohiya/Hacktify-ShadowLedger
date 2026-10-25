#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if [ ! -f ".venv/bin/python" ]; then
    echo "First-time setup..."
    bash setup.sh
fi

echo "Starting ShadowLedger..."

.venv/bin/python -m flask --app app run --host 127.0.0.1 --port 5002 &
SERVER_PID=$!

trap 'kill "$SERVER_PID" 2>/dev/null || true' EXIT

sleep 3
xdg-open http://127.0.0.1:5002/ 2>/dev/null || true

echo "Website: http://127.0.0.1:5002/"
echo "Press Ctrl+C to stop."

wait "$SERVER_PID"
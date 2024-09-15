#! /usr/bin/env sh
set -e

HOST=${SERVER_HOST:-0.0.0.0}
PORT=${SERVER_PORT:-8000}

echo "Starting Uvicorn"
exec uvicorn --reload --host $HOST --port $PORT --log-level debug main_http:app

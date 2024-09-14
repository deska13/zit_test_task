#! /usr/bin/env sh
set -e

echo "Starting Uvicorn with hotreload"
exec uvicorn --reload --host $HOST --port $PORT --log-level debug main_http:app

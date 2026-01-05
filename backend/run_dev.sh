#!/bin/bash

# Kill background processes on exit
trap "kill 0" EXIT

# Define Binary paths explicitly
VENV_BIN="/Users/dallyhermann/Desktop/MultiForge/.venv/bin"
CELERY_BIN="$VENV_BIN/celery"
UVICORN_BIN="$VENV_BIN/uvicorn"

echo "🚀 Starting MultiForge Backend..."

# Configure Python Path to include current directory
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Start Celery Worker
echo "🧵 Starting Celery Worker..."
$CELERY_BIN -A app.workers.celery_worker.celery_app worker --loglevel=info &

# Start FastAPI Server
echo "⚡ Starting FastAPI Server..."
$UVICORN_BIN app.main:app --reload --host 0.0.0.0 --port 8000 &

# Wait for all background processes
wait

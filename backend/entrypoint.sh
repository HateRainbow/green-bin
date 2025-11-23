#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for database..."
sleep 5

# Download model if it doesn't exist
if [ ! -d "app/AI/model" ]; then
    echo "Model not found. Downloading..."
    uv run python app/AI/download_model.py
else
    echo "Model already exists. Skipping download."
fi

# Run database setup (pgcrypto extension)
echo "Setting up database extensions..."
uv run python -c "from app.database.core import setup_database; setup_database()"

# Run migrations
echo "Running database migrations..."
uv run alembic upgrade head

# Start the application
echo "Starting application..."
exec uv run uvicorn app.app:app --host 0.0.0.0 --port 8080

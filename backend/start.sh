#!/bin/bash
set -e

echo "🚀 Starting WAHID Platform..."

# Les tables seront créées automatiquement dans main.py lifespan
# Pas besoin de migrations Alembic pour MVP

echo "🎯 Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
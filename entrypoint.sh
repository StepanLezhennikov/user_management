#!/bin/bash

set -e

alembic upgrade head
uvicorn src.app.main:app --host 0.0.0.0 --port 8001 --reload
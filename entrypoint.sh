#!/bin/bash

set -e

exec uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
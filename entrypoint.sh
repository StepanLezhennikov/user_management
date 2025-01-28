#!/bin/bash

set -e

aws configure set aws_access_key_id "$AWS__ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS__SECRET_ACCESS_KEY"
aws configure set region "$AWS__REGION_NAME"
aws ses verify-email-identity --email-address "$AWS__EMAIL_SOURCE" --endpoint-url "$AWS__ENDPOINT_URL"

alembic upgrade head
uvicorn src.app.main:app --host 0.0.0.0 --port 8001 --reload
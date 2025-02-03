#!/bin/bash

set -e

awslocal configure set aws_access_key_id "$AWS__ACCESS_KEY_ID"
awslocal configure set aws_secret_access_key "$AWS__SECRET_ACCESS_KEY"
awslocal configure set region "$AWS__REGION_NAME"
awslocal ses verify-email-identity --email-address "$AWS__EMAIL_SOURCE" --endpoint-url "$AWS__ENDPOINT_URL" --region "$AWS__REGION_NAME"

alembic upgrade head
uvicorn src.app.main:app --host 0.0.0.0 --port 8001 --reload
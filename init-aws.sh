#!/bin/bash



echo "AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID"
echo "AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY"
echo "AWS_REGION_NAME: $AWS_REGION_NAME"
echo "AWS_ENDPOINT_URL: $AWS_ENDPOINT_URL"
echo "AWS_EMAIL_SOURCE: $AWS_EMAIL_SOURCE"

awslocal ses verify-email-identity --email-address "$AWS_EMAIL_SOURCE" &
docker-entrypoint.sh
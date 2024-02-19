#!/usr/bin/env bash

set -e
set -o pipefail
set -u

echo "############# Deploying the Docker image for the service $SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET"

docker build -f services/move_processed_files_to_cold_bucket_service/Dockerfile -t "$SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET" .
docker tag "$SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET" "$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET:$IMAGE_TAG"
docker push "$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET:$IMAGE_TAG"

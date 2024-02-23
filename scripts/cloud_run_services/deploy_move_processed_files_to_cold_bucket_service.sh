#!/usr/bin/env bash

set -e
set -o pipefail
set -u

echo "############# Deploying the Cloud Run service $SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET"

gcloud run deploy "$SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET" \
  --image "$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET:$IMAGE_TAG" \
  --region="$LOCATION" \
  --no-allow-unauthenticated \
  --set-env-vars PROJECT_ID="$PROJECT_ID"

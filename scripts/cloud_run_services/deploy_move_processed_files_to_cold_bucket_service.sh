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

echo "############# Creating Event Arc trigger for the Cloud Run service $SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET"

gcloud eventarc triggers delete "$SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET" --location="$LOCATION"

gcloud eventarc triggers create "$SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET" \
  --destination-run-service="$SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET" \
  --destination-run-region="$LOCATION" \
  --location="$LOCATION" \
  --event-filters="type=google.cloud.audit.log.v1.written" \
  --event-filters="serviceName=bigquery.googleapis.com" \
  --event-filters="methodName=google.cloud.bigquery.v2.JobService.InsertJob" \
  --service-account="$SERVICE_ACCOUNT"

#!/usr/bin/env bash

set -e
set -o pipefail
set -u

echo "############# Deploying the Cloud Run service $SERVICE_NAME_ADD_FIFA_RANKING_TO_TEAM_STATS"

gcloud run deploy "$SERVICE_NAME_ADD_FIFA_RANKING_TO_TEAM_STATS" \
  --image "$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_ADD_FIFA_RANKING_TO_TEAM_STATS:$IMAGE_TAG" \
  --region="$LOCATION" \
  --no-allow-unauthenticated \
  --set-env-vars PROJECT_ID="$PROJECT_ID"

#!/usr/bin/env bash

set -e
set -o pipefail
set -u

echo "############# Deploying the Docker image for the service $SERVICE_NAME_RAW_TO_DOMAIN"

docker build -f services/world_cup_stats_raw_to_domain_service/Dockerfile -t "$SERVICE_NAME_RAW_TO_DOMAIN" .
docker tag "$SERVICE_NAME_RAW_TO_DOMAIN" "$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_RAW_TO_DOMAIN:$IMAGE_TAG"
docker push "$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_RAW_TO_DOMAIN:$IMAGE_TAG"

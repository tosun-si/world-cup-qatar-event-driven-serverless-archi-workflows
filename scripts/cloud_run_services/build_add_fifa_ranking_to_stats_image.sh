#!/usr/bin/env bash

set -e
set -o pipefail
set -u

echo "############# Deploying the Docker image for the service $SERVICE_NAME_ADD_FIFA_RANKING_TO_TEAM_STATS"

docker build -f services/world_cup_team_add_fifa_ranking_service/Dockerfile -t "$SERVICE_NAME_ADD_FIFA_RANKING_TO_TEAM_STATS" .
docker tag "$SERVICE_NAME_ADD_FIFA_RANKING_TO_TEAM_STATS" "$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_ADD_FIFA_RANKING_TO_TEAM_STATS:$IMAGE_TAG"
docker push "$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_ADD_FIFA_RANKING_TO_TEAM_STATS:$IMAGE_TAG"

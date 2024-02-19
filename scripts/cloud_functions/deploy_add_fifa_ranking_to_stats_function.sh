#!/usr/bin/env bash

set -e
set -o pipefail
set -u

echo "############# Deploying the Cloud Function qatar-world-cup-add-fifa-ranking-to-stats-domain-bq"

gcloud functions deploy qatar-world-cup-add-fifa-ranking-to-stats-domain-bq-wf \
  --gen2 \
  --region=europe-west1 \
  --runtime=python310 \
  --source=functions/world_cup_team_add_fifa_ranking_function \
  --entry-point=add_fifa_ranking_to_stats_domain_and_save_to_bq \
  --trigger-http \
  --service-account="$SERVICE_ACCOUNT"

#!/usr/bin/env bash

set -e
set -o pipefail
set -u

echo "############# Deploying the Cloud Function qatar-world-cup-stats-raw-to-domain-data-gcs"

gcloud functions deploy qatar-world-cup-stats-raw-to-domain-data-gcs-wf \
  --gen2 \
  --region=europe-west1 \
  --runtime=python310 \
  --source=functions/world_cup_stats_raw_to_domain_function \
  --entry-point=raw_to_domain_data_and_upload_to_gcs \
  --trigger-http \
  --service-account="$SERVICE_ACCOUNT"

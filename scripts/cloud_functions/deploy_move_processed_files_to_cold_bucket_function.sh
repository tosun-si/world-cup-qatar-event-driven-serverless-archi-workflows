#!/usr/bin/env bash

set -e
set -o pipefail
set -u

echo "############# Deploying the Cloud Function qatar-world-cup-move-processed-files-to-cold-bucket"

gcloud functions deploy qatar-world-cup-move-processed-files-to-cold-bucket-wf \
  --quiet \
  --gen2 \
  --region=europe-west1 \
  --runtime=go121 \
  --source=functions/move_processed_files_to_cold_bucket_function \
  --entry-point=MoveProcessedFileToColdBucket \
  --trigger-http \
  --service-account="$SERVICE_ACCOUNT"

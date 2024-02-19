# world-cup-qatar-event-driven-serverless-archi

Project showing a use case with a full Event Driven and Serverless Architecture.\
The project uses Event Arc and events on GCS and BigQuery.

This project uses real data for players statistics of Qatar Fifa World Cup.\ 
Transformations are applied to calculate domain data from raw and the result is stored in a BigQuery table.

The use case is executed with Cloud Functions then Cloud Run Services (Python and Go).

At the end of this real world use case, data will be visualized with Looker Studio. 

![qatar_fifa_world_cup_full_event_driven_and_serverless_archi.png](diagram%2Fqatar_fifa_world_cup_full_event_driven_and_serverless_archi.png)

## Use case with Cloud Functions

### Deploy all the Cloud Functions

```bash
gcloud builds submit \
  --project=$PROJECT_ID \
  --region=$LOCATION \
  --config deploy-all-cloud-functions.yaml \
  --substitutions _WORKFLOW_SA="$WORKFLOW_SA" \
  --verbosity="debug" .
```

### Deploy the workflow

```bash
gcloud builds submit \
  --project=$PROJECT_ID \
  --region=$LOCATION \
  --config deploy-workflow-terraform-apply.yaml \
  --substitutions _TF_STATE_BUCKET=$TF_STATE_BUCKET,_TF_STATE_PREFIX=$TF_STATE_PREFIX,_WORKFLOW_NAME=$WORKFLOW_NAME,_WORKFLOW_SA=$WORKFLOW_SA,_GOOGLE_PROVIDER_VERSION=$GOOGLE_PROVIDER_VERSION \
  --verbosity="debug" .
```


### Deploy the Cloud Function that map raw data to domain data and upload the result to GCS

```bash
gcloud functions deploy qatar-world-cup-stats-raw-to-domain-data-gcs \
  --gen2 \
  --region=europe-west1 \
  --runtime=python310 \
  --source=functions/world_cup_stats_raw_to_domain_function \
  --entry-point=raw_to_domain_data_and_upload_to_gcs \
  --run-service-account=sa-cloud-functions-dev@gb-poc-373711.iam.gserviceaccount.com \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=event-driven-functions-qatar-fifa-world-cup-stats-raw" \
  --trigger-location=europe-west1 \
  --trigger-service-account=sa-cloud-functions-dev@gb-poc-373711.iam.gserviceaccount.com
```

### Deploy the Cloud Function that add Fifa ranking to each team stats in the domain data

```bash
gcloud functions deploy qatar-world-cup-add-fifa-ranking-to-stats-domain-bq \
  --gen2 \
  --region=europe-west1 \
  --runtime=python310 \
  --source=functions/world_cup_team_add_fifa_ranking_function \
  --entry-point=add_fifa_ranking_to_stats_domain_and_save_to_bq \
  --run-service-account=sa-cloud-functions-dev@gb-poc-373711.iam.gserviceaccount.com \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=event-driven-functions-qatar-fifa-world-cup-stats" \
  --trigger-location=europe-west1 \
  --trigger-service-account=sa-cloud-functions-dev@gb-poc-373711.iam.gserviceaccount.com
```

### Deploy the Cloud Function that moves the processed files to a cold bucket 

```bash
gcloud functions deploy qatar-world-cup-move-processed-files-to-cold-bucket \
  --quiet \
  --gen2 \
  --region=europe-west1 \
  --runtime=go121 \
  --source=functions/move_processed_files_to_cold_bucket_function \
  --entry-point=MoveProcessedFileToColdBucket \
  --run-service-account=sa-cloud-functions-dev@gb-poc-373711.iam.gserviceaccount.com \
  --trigger-event-filters="type=google.cloud.audit.log.v1.written" \
  --trigger-event-filters="serviceName=bigquery.googleapis.com" \
  --trigger-event-filters="methodName=google.cloud.bigquery.v2.JobService.InsertJob" \
  --trigger-location=europe-west1 \
  --trigger-service-account=sa-cloud-functions-dev@gb-poc-373711.iam.gserviceaccount.com
````

## Use case with Cloud Run Services

### Deploy all the services

```bash
gcloud builds submit \
  --project=$PROJECT_ID \
  --region=$LOCATION \
  --config deploy-all-cloud-run-service.yaml \
  --substitutions _REPO_NAME="$REPO_NAME",_SERVICE_NAME_RAW_TO_DOMAIN="$SERVICE_NAME_RAW_TO_DOMAIN",_SERVICE_NAME_ADD_FIFA_RANKING_TO_TEAM_STATS="$SERVICE_NAME_ADD_FIFA_RANKING_TO_TEAM_STATS",_SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET="$SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET",_WORKFLOW_SA="$WORKFLOW_SA",_IMAGE_TAG="$IMAGE_TAG" \
  --verbosity="debug" .
```

### Map raw to domain Data

#### Build Docker image

```bash
docker build -f services/world_cup_stats_raw_to_domain_service/Dockerfile -t $SERVICE_NAME_RAW_TO_DOMAIN .
docker tag $SERVICE_NAME_RAW_TO_DOMAIN $LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_RAW_TO_DOMAIN:$IMAGE_TAG
docker push $LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_RAW_TO_DOMAIN:$IMAGE_TAG
```

#### Deploy service

```bash
gcloud run deploy "$SERVICE_NAME_RAW_TO_DOMAIN" \
  --image "$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_RAW_TO_DOMAIN:$IMAGE_TAG" \
  --region="$LOCATION" \
  --no-allow-unauthenticated \
  --set-env-vars PROJECT_ID="$PROJECT_ID"
```

#### Create Event Arc Trigger on Service

```bash
gcloud eventarc triggers create "$SERVICE_NAME_RAW_TO_DOMAIN" \
  --destination-run-service="$SERVICE_NAME_RAW_TO_DOMAIN" \
  --destination-run-region="$LOCATION" \
  --location="$LOCATION" \
  --event-filters="type=google.cloud.storage.object.v1.finalized" \
  --event-filters="bucket=event-driven-services-qatar-fifa-world-cup-stats-raw" \
  --service-account=sa-cloud-run-dev@gb-poc-373711.iam.gserviceaccount.com
```

#### Deploy the service and create the Event Arc Trigger with Cloud Build

```bash
gcloud builds submit \
  --project=$PROJECT_ID \
  --region=$LOCATION \
  --config deploy-raw-to-domain-cloud-run-service.yaml \
  --substitutions _REPO_NAME="$REPO_NAME",_SERVICE_NAME_RAW_TO_DOMAIN="$SERVICE_NAME_RAW_TO_DOMAIN",_WORKFLOW_SA="$WORKFLOW_SA",_IMAGE_TAG="$IMAGE_TAG" \
  --verbosity="debug" .
```

### Add Fifa Ranking to team stats

#### Build Docker image

```bash
docker build -f services/world_cup_team_add_fifa_ranking_service/Dockerfile -t $SERVICE_NAME_RAW_TO_DOMAIN .
docker tag $SERVICE_NAME_RAW_TO_DOMAIN $LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_RAW_TO_DOMAIN:$IMAGE_TAG
docker push $LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_RAW_TO_DOMAIN:$IMAGE_TAG
```

#### Deploy service

```bash
gcloud run deploy "$SERVICE_NAME_RAW_TO_DOMAIN" \
  --image "$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME_RAW_TO_DOMAIN:$IMAGE_TAG" \
  --region="$LOCATION" \
  --no-allow-unauthenticated \
  --set-env-vars PROJECT_ID="$PROJECT_ID"
```

#### Create Event Arc Trigger on Service

```bash
gcloud eventarc triggers create "$SERVICE_NAME_RAW_TO_DOMAIN" \
  --destination-run-service="$SERVICE_NAME_RAW_TO_DOMAIN" \
  --destination-run-region="$LOCATION" \
  --location="$LOCATION" \
  --event-filters="type=google.cloud.storage.object.v1.finalized" \
  --event-filters="bucket=event-driven-services-qatar-fifa-world-cup-stats-raw" \
  --service-account=sa-cloud-run-dev@gb-poc-373711.iam.gserviceaccount.com
```

#### Deploy the service and create the Event Arc Trigger with Cloud Build

```bash
gcloud builds submit \
  --project=$PROJECT_ID \
  --region=$LOCATION \
  --config deploy-add-fifa-ranking-to-stats-cloud-run-service.yaml \
  --substitutions _REPO_NAME="$REPO_NAME",_SERVICE_NAME_ADD_FIFA_RANKING_TO_TEAM_STATS="$SERVICE_NAME_ADD_FIFA_RANKING_TO_TEAM_STATS",_WORKFLOW_SA="$WORKFLOW_SA",_IMAGE_TAG="$IMAGE_TAG" \
  --verbosity="debug" .
```

### Move processed files to cold bucket

#### Deploy the service and create the Event Arc Trigger with Cloud Build

```bash
gcloud builds submit \
  --project=$PROJECT_ID \
  --region=$LOCATION \
  --config deploy-move-processed-files-to-cold-service.yaml \
  --substitutions _REPO_NAME="$REPO_NAME",_SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET="$SERVICE_NAME_MOVE_PROCESSED_FILE_TO_COLD_BUCKET",_WORKFLOW_SA="$WORKFLOW_SA",_IMAGE_TAG="$IMAGE_TAG" \
  --verbosity="debug" .
```

from fastapi import FastAPI
from google.cloud import storage

app = FastAPI()


@app.post("/")
async def move_processed_files_to_cold_bucket_service():
    raw_source_bucket = "event-driven-services-qatar-fifa-world-cup-stats-raw-wf"
    raw_source_object = "input/stats/world_cup_team_players_stats_raw_ndjson.json"
    domain_source_bucket = "event-driven-services-qatar-fifa-world-cup-stats-wf"
    domain_source_object = "input/stats/world_cup_team_players_stats_domain.json"

    dest_bucket = "event-driven-qatar-fifa-world-cup-stats-cold"
    raw_dest_object = "input/raw/world_cup_team_players_stats_raw_ndjson.json"
    domain_dest_object = "input/domain/world_cup_team_players_stats_domain.json"

    storage_client = storage.Client()

    move_processed_files(
        storage_client=storage_client,
        source_bucket=raw_source_bucket,
        source_object=raw_source_object,
        dest_bucket=dest_bucket,
        dest_object=raw_dest_object
    )

    move_processed_files(
        storage_client=storage_client,
        source_bucket=domain_source_bucket,
        source_object=domain_source_object,
        dest_bucket=dest_bucket,
        dest_object=domain_dest_object
    )

    success_message = (
        "## After successfully inserted the Data to BigQuery, the processed files are moved to a cold bucket ##"
    )

    print(success_message)
    return success_message, 200


def move_processed_files(
        storage_client,
        source_bucket: str,
        source_object: str,
        dest_bucket: str,
        dest_object: str):
    source_bucket = storage_client.bucket(source_bucket)
    source_blob = source_bucket.blob(source_object)
    destination_bucket = storage_client.bucket(dest_bucket)

    blob_copy = source_bucket.copy_blob(
        blob=source_blob,
        destination_bucket=destination_bucket,
        new_name=dest_object
    )
    source_bucket.delete_blob(source_object)

    print(
        "Blob {} in bucket {} moved to blob {} in bucket {}.".format(
            source_blob.name,
            source_bucket.name,
            blob_copy.name,
            destination_bucket.name,
        )
    )

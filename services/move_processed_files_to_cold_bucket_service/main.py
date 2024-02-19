from cloudevents.http import from_http
from fastapi import FastAPI, Request
from google.cloud import storage

app = FastAPI()


@app.post("/")
async def move_processed_files_to_cold_bucket_service(request: Request):
    event = from_http(dict(request.headers), await request.body())

    # Gets the Payload data from the Audit Log
    event_data = event.data

    print("######################  Event Data  ###############################################################")
    print(event_data)
    print("The type of event data is :", type(event_data))
    print("###############################################################")

    print("######################  HEADER   ###############################################################")
    print(request.headers)
    print("###############################################################")

    expected_dataset = "qatar_fifa_world_cup"
    expected_table = "tables/world_cup_team_players_stat"

    raw_source_bucket = "event-driven-services-qatar-fifa-world-cup-stats-raw"
    raw_source_object = "input/stats/world_cup_team_players_stats_raw_ndjson.json"
    domain_source_bucket = "event-driven-services-qatar-fifa-world-cup-stats"
    domain_source_object = "input/stats/world_cup_team_players_stats_domain.json"

    dest_bucket = "event-driven-qatar-fifa-world-cup-stats-cold"
    raw_dest_object = "input/raw/world_cup_team_players_stats_raw_ndjson.json"
    domain_dest_object = "input/domain/world_cup_team_players_stats_domain.json"

    success_message = ""

    try:
        bq_dataset = event_data['resource']['labels']['dataset_id']
        gcp_project_id = event_data['resource']['labels']['project_id']
        bq_table = event_data['protoPayload']['resourceName']
        inserted_rows_bq = int(event_data['protoPayload']['metadata']['tableDataChange']['insertedRowsCount'])

        print("######################  Dataset   ###############################################################")
        print(bq_dataset)
        print("###############################################################")

        print("######################  Project   ###############################################################")
        print(gcp_project_id)
        print("###############################################################")

        print("######################  Table   ###############################################################")
        print(bq_table)
        print("###############################################################")

        print("######################  Rows   ###############################################################")
        print(inserted_rows_bq)
        print("###############################################################")

        if bq_dataset == expected_dataset and bq_table.endswith(expected_table) and inserted_rows_bq > 0:
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
    except KeyError as e:
        success_message = "## The event doesn't contains the fields concerning the insertion to the BigQuery table ##"
        pass
    except Exception as e:
        print(e)
        raise e

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

import os
from typing import List

import uvicorn
from fastapi import FastAPI, Request
from google.cloud import storage
from toolz.curried import pipe

from services.world_cup_stats_raw_to_domain_service.domain.team_player_stats import TeamPlayerStats
from services.world_cup_stats_raw_to_domain_service.domain.team_player_stats_mapper import to_team_players_stats_domain, \
    to_team_player_stats_as_ndjson_string

app = FastAPI()


@app.post("/")
async def raw_to_domain_data_and_upload_to_gcs_service(request: Request):
    headers = request.headers

    input_bucket = headers["ce-bucket"]
    input_object = headers["ce-subject"].replace("objects/", "")

    print(f"Bucket: {input_bucket}")
    print(f"File: {input_object}")

    storage_client = storage.Client()

    input_bucket = storage_client.get_bucket(input_bucket)
    input_blob = input_bucket.get_blob(input_object)
    team_player_stats_raw_list_as_bytes = input_blob.download_as_bytes()

    team_player_stats_domain: List[TeamPlayerStats] = pipe(
        to_team_players_stats_domain(team_player_stats_raw_list_as_bytes),
    )

    team_player_stats_domain_as_ndjson_str = to_team_player_stats_as_ndjson_string(team_player_stats_domain)

    output_bucket = storage_client.get_bucket('event-driven-services-qatar-fifa-world-cup-stats')
    output_blob = output_bucket.blob('input/stats/world_cup_team_players_stats_domain.json')

    output_blob.upload_from_string(
        data=team_player_stats_domain_as_ndjson_str,
        content_type='application/json'
    )

    success_message = "#######The GCS file for players stats domain data was correctly uploaded to the GCS#######"
    print(success_message)

    return success_message, 200


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

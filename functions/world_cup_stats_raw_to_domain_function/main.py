from typing import List

import functions_framework
from flask import jsonify
from google.cloud import storage
from toolz.curried import pipe

from domain.team_player_stats import TeamPlayerStats
from domain.team_player_stats_mapper import to_team_players_stats_domain, to_team_player_stats_as_ndjson_string


@functions_framework.http
def raw_to_domain_data_and_upload_to_gcs(request):
    input_bucket = 'event-driven-functions-qatar-fifa-world-cup-stats-raw-wf'
    input_object = 'input/stats/world_cup_team_players_stats_raw_ndjson.json'

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

    output_bucket = storage_client.get_bucket('event-driven-functions-qatar-fifa-world-cup-stats-wf')
    output_blob = output_bucket.blob('input/stats/world_cup_team_players_stats_domain.json')

    output_blob.upload_from_string(
        data=team_player_stats_domain_as_ndjson_str,
        content_type='application/json'
    )

    print("#######The GCS file for players stats domain data was correctly uploaded to the GCS#######")

    output = {"status": 201}
    return jsonify(output)

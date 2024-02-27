import pathlib
from typing import Dict, List

import functions_framework
from flask import jsonify
from google.api_core.exceptions import ClientError
from google.cloud import storage, bigquery

from domain.team_player_stats_with_fifa_ranking_mapper import to_stats_domain_dicts_with_fifa_ranking


@functions_framework.http
def add_fifa_ranking_to_stats_domain_and_save_to_bq(request):
    input_bucket = "event-driven-functions-qatar-fifa-world-cup-stats-wf"
    input_object = "input/stats/world_cup_team_players_stats_domain.json"

    print(f"Bucket: {input_bucket}")
    print(f"File: {input_object}")

    storage_client = storage.Client()

    input_bucket = storage_client.get_bucket(input_bucket)
    input_team_stats_domain_blob = input_bucket.get_blob(input_object)
    teams_player_stats_domain_as_bytes = input_team_stats_domain_blob.download_as_bytes()

    input_team_fifa_ranking_blob = input_bucket.get_blob('input/team_fifa_ranking.json')
    teams_fifa_ranking_blob_as_bytes = input_team_fifa_ranking_blob.download_as_bytes()

    teams_player_stats_domain_with_fifa_ranking: List[Dict] = to_stats_domain_dicts_with_fifa_ranking(
        teams_player_stats_domain_as_bytes,
        teams_fifa_ranking_blob_as_bytes
    )

    print('################################################')
    print(teams_player_stats_domain_with_fifa_ranking)
    print('################################################')

    current_directory = pathlib.Path(__file__).parent
    schema_path = str(current_directory / "schema/world_cup_team_player_stat_schema.json")

    bigquery_client = bigquery.Client()
    schema = bigquery_client.schema_from_json(schema_path)

    job_config = bigquery.LoadJobConfig(
        create_disposition=bigquery.CreateDisposition.CREATE_NEVER,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        schema=schema,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    )

    table_id = "qatar_fifa_world_cup.world_cup_team_players_stat_wf"

    load_job = bigquery_client.load_table_from_json(
        json_rows=teams_player_stats_domain_with_fifa_ranking,
        destination=table_id,
        job_config=job_config
    )

    try:
        load_job = load_job.result()

        print("#######The Team players Domain Data with Fifa ranking was correctly loaded to the BigQuery table#######")

        output = {"status": 201}
        return jsonify(output)
    except ClientError as e:
        print(load_job.errors)
        raise e

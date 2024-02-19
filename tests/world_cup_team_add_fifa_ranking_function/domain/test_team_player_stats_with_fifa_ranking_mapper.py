import pathlib
from typing import List, Dict

from google.api_core.exceptions import ClientError
from google.cloud import bigquery

from functions.world_cup_team_add_fifa_ranking_function.domain.team_player_stats_with_fifa_ranking_mapper import \
    to_stats_domain_dicts_with_fifa_ranking
from tests.root import ROOT_DIR
from tests.testing_helper import load_nd_json_file_as_string


class TestTeamPlayerStatsWithFifaRankingMapper:

    def test_given_input_teams_player_stats_when_map_to_stats_domain_with_fifa_ranking_then_expected_result(
            self):
        input_teams_players_stats_domain_file_path = f'{ROOT_DIR}/files/world_cup_team_players_stats_domain_ndjson.json'
        input_teams_fifa_ranking_file_path = f'{ROOT_DIR}/files/team_fifa_ranking.json'

        # Given.
        teams_players_stats_domain_as_byte = (
            load_nd_json_file_as_string(input_teams_players_stats_domain_file_path)
            .encode('utf-8')
        )

        teams_fifa_ranking_as_byte = (
            load_nd_json_file_as_string(input_teams_fifa_ranking_file_path)
            .encode('utf-8')
        )

        teams_player_stats_domain_with_fifa_ranking: List[Dict] = to_stats_domain_dicts_with_fifa_ranking(
            teams_players_stats_domain_as_byte,
            teams_fifa_ranking_as_byte
        )

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

        table_id = "qatar_fifa_world_cup.world_cup_team_players_stat"

        load_job = bigquery_client.load_table_from_json(
            json_rows=teams_player_stats_domain_with_fifa_ranking,
            destination=table_id,
            job_config=job_config
        )

        try:
            load_job.result()
        except ClientError as e:
            print(load_job.errors)
            raise e

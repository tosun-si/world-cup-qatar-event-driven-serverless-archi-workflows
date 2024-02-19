from typing import List

from functions.world_cup_stats_raw_to_domain_function.domain.team_player_stats import TeamPlayerStats
from functions.world_cup_stats_raw_to_domain_function.domain.team_player_stats_mapper import \
    to_team_players_stats_domain, \
    to_team_player_stats_as_ndjson_string
from tests.root import ROOT_DIR
from tests.testing_helper import load_nd_json_file_as_string


class TestTeamPlayerStatsMapper:

    def test_given_input_teams_player_stats_when_map_to_stats_domain_then_expected_result(
            self):
        input_teams_players_stats_raw_file_path = f'{ROOT_DIR}/files/world_cup_team_players_stats_raw_ndjson.json'

        # Given.
        teams_players_stats_raw_as_byte = (
            load_nd_json_file_as_string(input_teams_players_stats_raw_file_path)
            .encode('utf-8')
        )

        team_players_stats: List[TeamPlayerStats] = to_team_players_stats_domain(teams_players_stats_raw_as_byte)

        result_str = to_team_player_stats_as_ndjson_string(team_players_stats)

        ee = ""

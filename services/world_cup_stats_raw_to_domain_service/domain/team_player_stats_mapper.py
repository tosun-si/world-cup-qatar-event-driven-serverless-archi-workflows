import dataclasses
import json
from itertools import groupby
from typing import List, Dict

import ndjson
from toolz.curried import pipe, map, filter

from services.world_cup_stats_raw_to_domain_service.domain.team_player_stats import TeamPlayerStats
from services.world_cup_stats_raw_to_domain_service.domain.team_player_stats_raw import TeamPlayerStatsRaw


def to_team_players_stats_domain(team_player_stats_raw_as_byte: bytes) -> List[TeamPlayerStats]:
    team_players_stats_raw: List[TeamPlayerStatsRaw] = list(pipe(
        team_player_stats_raw_as_byte.strip().split(b'\n'),
        map(lambda team_stats_bytes: json.loads(team_stats_bytes.decode('utf-8'))),
        map(deserialize),
        filter(lambda t: t.nationalTeamKitSponsor != ''),
        filter(lambda t: t.position != '')
    ))

    return list(pipe(
        groupby(team_players_stats_raw, lambda t: t.nationality),
        map(lambda players_stats_with_team_name:
            TeamPlayerStats.compute_team_player_stats(
                team_name=players_stats_with_team_name[0],
                team_players_stats_raw_iterator=players_stats_with_team_name[1]))
    ))


def to_team_player_stats_as_ndjson_string(team_players_stats: List[TeamPlayerStats]) -> str:
    team_players_stats_as_dicts: List[Dict] = list(pipe(
        team_players_stats,
        map(dataclasses.asdict)
    ))

    return ndjson.dumps(team_players_stats_as_dicts)


def deserialize(team_player_stats_raw_as_dict: Dict) -> TeamPlayerStatsRaw:
    from dacite import from_dict

    return from_dict(
        data_class=TeamPlayerStatsRaw,
        data=team_player_stats_raw_as_dict
    )

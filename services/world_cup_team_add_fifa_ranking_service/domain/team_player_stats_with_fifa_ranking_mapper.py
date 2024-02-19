import json
from datetime import datetime
from typing import List, Dict

from toolz.curried import pipe, map

current_iso_datetime = datetime.now().isoformat()


def to_stats_domain_dicts_with_fifa_ranking(teams_player_stats_domain_as_bytes: bytes,
                                            teams_fifa_ranking_blob_as_bytes: bytes) -> List[Dict]:
    fifa_ranking_as_dicts: List[Dict] = list(pipe(
        teams_fifa_ranking_blob_as_bytes.strip().split(b'\n'),
        map(lambda fifa_ranking: json.loads(fifa_ranking.decode('utf-8')))
    ))

    return list(pipe(
        teams_player_stats_domain_as_bytes.strip().split(b'\n'),
        map(lambda team_stats_bytes: json.loads(team_stats_bytes.decode('utf-8'))),
        map(lambda team_stats_dict: add_fifa_ranking_to_team_stats(team_stats_dict, fifa_ranking_as_dicts)),
        map(add_ingestion_date_to_team_stats)
    ))


def add_fifa_ranking_to_team_stats(team_player_stats_domain: Dict, teams_fifa_ranking: List[Dict]) -> Dict:
    current_team_fifa_ranking: Dict = next(
        fifa_ranking for fifa_ranking in teams_fifa_ranking if
        fifa_ranking['teamName'] == team_player_stats_domain['teamName']
    )

    team_player_stats_domain['fifaRanking'] = current_team_fifa_ranking['fifaRanking']

    return team_player_stats_domain


def add_ingestion_date_to_team_stats(team_player_stats_domain: Dict) -> Dict:
    team_player_stats_domain['ingestionDate'] = current_iso_datetime

    return team_player_stats_domain

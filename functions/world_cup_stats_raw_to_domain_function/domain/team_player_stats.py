from __future__ import annotations

from dataclasses import dataclass
from typing import List, Iterable

from domain.team_player_stats_raw import TeamPlayerStatsRaw
from toolz.curried import pipe, filter, map


@dataclass
class Player:
    playerName: str
    playerDob: str
    position: str
    club: str
    brandSponsorAndUsed: str
    appearances: int


@dataclass
class BestPassersStats:
    players: List[Player]
    goalAssists: int


@dataclass
class TopScorersStats:
    players: List[Player]
    goals: int


@dataclass
class BestDribblersStats:
    players: List[Player]
    dribbles: float


@dataclass
class GoalkeeperStats:
    playerName: str
    appearances: str
    savePercentage: str
    cleanSheets: str
    club: str


@dataclass
class PlayersMostAppearancesStats:
    players: List[Player]
    appearances: int


@dataclass
class PlayersMostDuelsWonStats:
    players: List[Player]
    duels: float


@dataclass
class PlayersMostInterceptionStats:
    players: List[Player]
    interceptions: float


@dataclass
class PlayersMostSuccessfulTacklesStats:
    players: List[Player]
    successfulTackles: float


@dataclass
class TeamPlayerStats:
    teamName: str
    teamTotalGoals: int
    nationalTeamKitSponsor: str
    topScorers: TopScorersStats
    bestPassers: BestPassersStats
    bestDribblers: BestDribblersStats
    goalKeeper: GoalkeeperStats
    playersMostAppearances: PlayersMostAppearancesStats
    playersMostDuelsWon: PlayersMostDuelsWonStats
    playersMostInterception: PlayersMostInterceptionStats
    playersMostSuccessfulTackles: PlayersMostSuccessfulTacklesStats

    @classmethod
    def compute_team_player_stats(cls,
                                  team_name: str,
                                  team_players_stats_raw_iterator: Iterable[TeamPlayerStatsRaw]) -> TeamPlayerStats:

        team_players_stats_raw_list = list(team_players_stats_raw_iterator)

        top_scorers_value = max(team_players_stats_raw_list, key=lambda t: cls._to_int(t.goalsScored)).goalsScored

        top_scorers: List[Player] = list(pipe(
            team_players_stats_raw_list,
            filter(lambda t: t.goalsScored == top_scorers_value),
            filter(lambda t: t.goalsScored != '0'),
            map(cls._to_player)
        ))

        best_passers_value = max(
            team_players_stats_raw_list,
            key=lambda t: cls._to_int(t.assistsProvided)
        ).assistsProvided

        best_passers: List[Player] = list(pipe(
            team_players_stats_raw_list,
            filter(lambda t: t.assistsProvided == best_passers_value),
            filter(lambda t: t.assistsProvided != '0'),
            map(cls._to_player)
        ))

        best_dribblers_value = max(
            team_players_stats_raw_list,
            key=lambda t: cls._to_float(t.dribblesPerNinety)
        ).dribblesPerNinety

        best_dribblers: List[Player] = list(pipe(
            team_players_stats_raw_list,
            filter(lambda t: t.dribblesPerNinety == best_dribblers_value),
            map(cls._to_player)
        ))

        players_most_appearances_value = max(
            team_players_stats_raw_list,
            key=lambda t: cls._to_int(t.appearances)
        ).appearances

        players_most_appearances: List[Player] = list(pipe(
            team_players_stats_raw_list,
            filter(lambda t: t.appearances == players_most_appearances_value),
            map(cls._to_player)
        ))

        players_most_duels_won_value = max(
            team_players_stats_raw_list,
            key=lambda t: cls._to_float(t.totalDuelsWonPerNinety)
        ).totalDuelsWonPerNinety

        players_most_duels_won: List[Player] = list(pipe(
            team_players_stats_raw_list,
            filter(lambda t: t.totalDuelsWonPerNinety == players_most_duels_won_value),
            map(cls._to_player)
        ))

        players_most_interceptions_value = max(
            team_players_stats_raw_list,
            key=lambda t: cls._to_float(t.interceptionsPerNinety)
        ).interceptionsPerNinety

        players_most_interceptions: List[Player] = list(pipe(
            team_players_stats_raw_list,
            filter(lambda t: t.interceptionsPerNinety == players_most_interceptions_value),
            map(cls._to_player)
        ))

        players_most_successful_tackles_value = max(
            team_players_stats_raw_list,
            key=lambda t: cls._to_float(t.tacklesPerNinety)
        ).tacklesPerNinety

        players_most_successful_tackles: List[Player] = list(pipe(
            team_players_stats_raw_list,
            filter(lambda t: t.tacklesPerNinety == players_most_successful_tackles_value),
            map(cls._to_player)
        ))

        current_goal_keeper_stats: TeamPlayerStatsRaw = next(
            t for t in team_players_stats_raw_list if t.savePercentage != '-'
        )

        team_total_goals: int = max(
            pipe(
                team_players_stats_raw_list,
                map(lambda t: cls._to_int(t.goalsScored))
            )
        )

        top_scorers_stats = TopScorersStats(
            players=top_scorers,
            goals=cls._to_int_or_none(top_scorers_value)
        )

        best_passers_stats = BestPassersStats(
            players=best_passers,
            goalAssists=cls._to_int_or_none(best_passers_value)
        )

        best_dribblers_stats = BestDribblersStats(
            players=best_dribblers,
            dribbles=cls._to_float_or_none(best_dribblers_value)
        )

        players_most_appearances_stats = PlayersMostAppearancesStats(
            players=players_most_appearances,
            appearances=cls._to_int_or_none(players_most_appearances_value)
        )

        players_most_duels_won_stats = PlayersMostDuelsWonStats(
            players=players_most_duels_won,
            duels=cls._to_float_or_none(players_most_duels_won_value)
        )

        players_most_interception_stats = PlayersMostInterceptionStats(
            players=players_most_interceptions,
            interceptions=cls._to_float_or_none(players_most_interceptions_value)
        )

        players_most_successful_tackles_stats = PlayersMostSuccessfulTacklesStats(
            players=players_most_successful_tackles,
            successfulTackles=cls._to_float_or_none(players_most_successful_tackles_value)
        )

        goalkeeper_stats = GoalkeeperStats(
            playerName=current_goal_keeper_stats.playerName,
            club=current_goal_keeper_stats.club,
            appearances=current_goal_keeper_stats.appearances,
            savePercentage=current_goal_keeper_stats.savePercentage,
            cleanSheets=current_goal_keeper_stats.cleanSheets
        )

        current_team = team_players_stats_raw_list[0]

        return TeamPlayerStats(
            teamName=team_name,
            teamTotalGoals=team_total_goals,
            nationalTeamKitSponsor=current_team.nationalTeamKitSponsor,
            topScorers=top_scorers_stats,
            bestPassers=best_passers_stats,
            bestDribblers=best_dribblers_stats,
            playersMostAppearances=players_most_appearances_stats,
            playersMostDuelsWon=players_most_duels_won_stats,
            playersMostInterception=players_most_interception_stats,
            playersMostSuccessfulTackles=players_most_successful_tackles_stats,
            goalKeeper=goalkeeper_stats
        )

    @classmethod
    def _to_int(cls, string_value) -> int:
        try:
            return int(string_value)
        except Exception:
            return 0

    @classmethod
    def _to_float(cls, string_value) -> float:
        try:
            return float(string_value)
        except Exception:
            return 0.0

    @classmethod
    def _to_float_or_none(cls, string_value) -> float | None:
        try:
            return float(string_value)
        except Exception:
            return None

    @classmethod
    def _to_int_or_none(cls, string_value) -> int | None:
        try:
            return int(string_value)
        except Exception:
            return None

    @classmethod
    def _to_player(cls, team_player_stats: TeamPlayerStatsRaw) -> Player:
        return Player(
            playerName=team_player_stats.playerName,
            playerDob=team_player_stats.playerDob,
            position=team_player_stats.position,
            club=team_player_stats.club,
            brandSponsorAndUsed=team_player_stats.brandSponsorAndUsed,
            appearances=cls._to_int_or_none(team_player_stats.appearances)
        )

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

PLAYER_NATIONALITY_EMPTY_ERROR_MESSAGE = "Player nationality name cannot be null or empty"


class TeamStatsRawValidatorException(Exception):
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__(self.errors)


@dataclass
class TeamPlayerStatsRaw:
    nationality: str
    fifaRanking: int
    nationalTeamKitSponsor: str
    position: str
    nationalTeamJerseyNumber: Optional[int]
    playerDob: str
    club: str
    playerName: str
    appearances: str
    goalsScored: str
    assistsProvided: str
    dribblesPerNinety: str
    interceptionsPerNinety: str
    tacklesPerNinety: str
    totalDuelsWonPerNinety: str
    savePercentage: str
    cleanSheets: str
    brandSponsorAndUsed: str

    def validate_fields(self) -> TeamPlayerStatsRaw:
        if self.nationality is None or self.nationality == '':
            raise TeamStatsRawValidatorException([PLAYER_NATIONALITY_EMPTY_ERROR_MESSAGE])

        return self

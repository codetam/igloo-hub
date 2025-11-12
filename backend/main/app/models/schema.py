from datetime import datetime
from typing import Literal, Optional, List
import uuid
from pydantic import BaseModel, computed_field

# ==========================
# STADIUM
# ==========================
class StadiumRead(BaseModel):
    id: uuid.UUID
    name: str
    address: Optional[str] = None

# ==========================
# Team
# ==========================
class TeamRead(BaseModel):
    id: uuid.UUID
    name: Optional[str]

# ==========================
# Players
# ==========================
class PlayerRead(BaseModel):
    id: uuid.UUID
    name: str
    nickname: Optional[str] = None
    profile: Optional[str] = None

class PlayerStats(BaseModel):
    id: uuid.UUID
    name: str
    nickname: Optional[str] = None
    profile: Optional[str] = None
    games_played: int
    total_goals: int
    total_assists: int
    wins: int
    
    @computed_field
    @property
    def goals_per_game(self) -> int:
        return round(self.total_goals / self.games_played, 2) if self.games_played > 0 else 0

class GamePlayerStats(BaseModel):
    game_id: int
    date: datetime
    stadium: str
    team: Literal['home', 'away']
    score: str
    result: Literal['win', 'loss', 'draw']
    goals: int
    assists: int

# ==========================
# Score
# ==========================
class GameScore(BaseModel):
    home_team: int
    away_team: int

# ==========================
# Game
# ==========================
class GoalRead(BaseModel):
    id: uuid.UUID
    team_id: uuid.UUID
    minute: Optional[datetime] = None
    scorer: Optional[PlayerRead] = None
    assister: Optional[PlayerRead] = None

class GameRead(BaseModel):
    id: uuid.UUID
    date: datetime
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    home_team_id: uuid.UUID
    away_team_id: uuid.UUID

    stadium: Optional[StadiumRead] = None
    goals: List[GoalRead] = []

    @computed_field
    @property
    def status(self) -> Literal['not_started', 'started', 'ended']:
        if not self.started_at:
            return 'not_started'
        if not self.ended_at:
            return 'started'
        return 'ended'
    
    @computed_field
    @property
    def score(self) -> GameScore:
        home_team = sum(1 for goal in self.goals if goal.team_id == self.home_team_id)
        away_team = sum(1 for goal in self.goals if goal.team_id == self.away_team_id)
        return GameScore(home_team=home_team, away_team=away_team)
    
# TODO: add in gameRead home {id, players} and away {id, players}
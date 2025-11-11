from datetime import datetime
from typing import Optional, List
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

class GamePlayerRead(BaseModel):
    player: PlayerRead
    goals: int
    assists: int
           
class GamePlayersRead(BaseModel):
    game_id: uuid.UUID
    team_1: List[GamePlayerRead]
    team_2: List[GamePlayerRead]

# ==========================
# Score
# ==========================
class GameScore(BaseModel):
    game_id: uuid.UUID
    team_1: int
    team_2: int
    winner: Optional[int] = None
    status: str
        
# ==========================
# Game
# ==========================
class GoalRead(BaseModel):
    id: uuid.UUID
    team: int
    minute: Optional[datetime] = None
    scorer: Optional[PlayerRead] = None
    assister: Optional[PlayerRead] = None

class GameRead(BaseModel):
    id: uuid.UUID
    date: datetime
    notes: Optional[str] = None
    stadium: Optional[StadiumRead] = None
    goals: List[GoalRead] = []
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    
class ScoreBoard(BaseModel):
    home: int
    away: int

class GamePlayerStats(BaseModel):
    game_id: int
    date: datetime
    stadium: str
    team: str
    score: str
    result: str
    goals: int
    assists: int
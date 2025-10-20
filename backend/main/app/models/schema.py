from datetime import datetime
from typing import Optional, List
import uuid
from pydantic import BaseModel

# ==========================
# STADIUM
# ==========================
class StadiumRead(BaseModel):
    id: uuid.UUID
    name: str
    address: Optional[str] = None

    class Config:
        orm_mode = True


# ==========================
# Players
# ==========================
class PlayerRead(BaseModel):
    id: uuid.UUID
    name: str
    nickname: Optional[str] = None
    profile: Optional[str] = None

    class Config:
        orm_mode = True

class GamePlayerRead(BaseModel):
    player: PlayerRead
    goals: int
    assists: int

    class Config:
        orm_mode = True
           
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

    class Config:
        orm_mode = True

class GameRead(BaseModel):
    id: uuid.UUID
    date: datetime
    notes: Optional[str] = None
    stadium: Optional[StadiumRead] = None
    goals: List[GoalRead] = []

    class Config:
        orm_mode = True


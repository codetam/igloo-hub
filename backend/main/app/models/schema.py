from datetime import datetime
from typing import Literal, Optional, List
import uuid
from pydantic import BaseModel, ConfigDict, computed_field, field_validator
from sqlmodel import Session

from app.models.model import Game, GamePlayer, Player, Team

# ==========================
# PLAYER
# ==========================

class PlayerCreate(BaseModel):
    name: str
    nickname: Optional[str] = None
    
class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    nickname: Optional[str] = None
    
class PlayerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    name: str
    nickname: Optional[str] = None
    profile: Optional[str] = None
    
class GlobalPlayerStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
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
    def goals_per_game(self) -> float:
        return round(self.total_goals / self.games_played, 2) if self.games_played > 0 else 0

def get_player_stats(player: Player) -> GlobalPlayerStats:
    
    wins = 0
    for game_player in player.game_players:
        game = game_player.game
        player_team_id = game_player.team_id
        
        game = get_game(game)
        
        if player_team_id == game.home_team.id and game.score.home_team > game.score.away_team:
            wins += 1
        elif player_team_id == game.away_team.id and game.score.away_team > game.score.home_team:
            wins += 1
    
    return GlobalPlayerStats(
        id=player.id,
        name=player.name,
        nickname=player.nickname,
        profile=player.profile,
        games_played=len(player.game_players),
        total_goals=len(player.goals_scored),
        total_assists=len(player.assists_made),
        wins=wins
    )

class GamePlayerStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    game_id: uuid.UUID
    date: datetime
    stadium: str
    team: Literal['home', 'away']
    score: str
    result: Literal['win', 'loss', 'draw']
    goals: int
    assists: int

def get_gameplayer_stats(gp: GamePlayer) -> GamePlayerStats:
    game = get_game(gp.game)
    team = "home" if game.home_team.id == gp.team_id else "away"
    score = game.score
    
    player_is_home = game.home_team.id == gp.team_id
    player_goals = score.home_team if player_is_home else score.away_team
    opponent_goals = score.away_team if player_is_home else score.home_team
    
    if player_goals > opponent_goals:
        result = "win"
    elif player_goals < opponent_goals:
        result = "loss"
    else:
        result = "draw"
    
    return GamePlayerStats(
        game_id=game.id, 
        date=game.date, 
        stadium=game.stadium.name, 
        team=team, 
        score=f"{score.home_team} - {score.away_team}",
        result=result, 
        goals=gp.get_goals(), 
        assists=gp.get_assists()
    )

# ==========================
# STADIUM
# ==========================
class StadiumCreate(BaseModel):
    name: str
    address: Optional[str] = None
    
class StadiumRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    name: str
    address: Optional[str] = None
    
# ==========================
# Score
# ==========================
class GameScore(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    home_team: int
    away_team: int

class GoalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    team_id: uuid.UUID
    minute: Optional[datetime] = None
    scorer: Optional[PlayerRead] = None
    assister: Optional[PlayerRead] = None
    
# ==========================
# TEAM
# ==========================
class GamePlayerTeamRead(PlayerRead):
    model_config = ConfigDict(from_attributes=True)
    
    goals: int
    assists: int

class GameTeamRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    name: Optional[str] = None
    players: list[GamePlayerTeamRead]
    
# ==========================
# GAME
# ==========================

class GameCreate(BaseModel):
    stadium_id: uuid.UUID
    date: datetime
    
class GamePlayerCreate(BaseModel):
    player_id: uuid.UUID
    team_id: uuid.UUID
    
class GoalCreate(BaseModel):
    scorer_id: uuid.UUID
    team_id: uuid.UUID
    assister_id: Optional[uuid.UUID] = None
    minute: Optional[datetime] = None
    
    @field_validator('minute', mode='before')
    @classmethod
    def parse_minute(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace('Z', '+00:00'))
        return v
    
class GameRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    date: datetime
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    stadium: Optional[StadiumRead] = None
    home_team: GameTeamRead
    away_team: GameTeamRead
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
        home_team = sum(1 for goal in self.goals if goal.team_id == self.home_team.id)
        away_team = sum(1 for goal in self.goals if goal.team_id == self.away_team.id)
        return GameScore(home_team=home_team, away_team=away_team)
    
def get_team(team: Team):
    game_players = team.players
    team_players: list[GamePlayerTeamRead] = []
    for gp in game_players:
        team_players.append(GamePlayerTeamRead(
            id = gp.player_id,
            name = gp.player.name,
            nickname = gp.player.nickname,
            profile = gp.player.profile,
            goals=gp.get_goals(),
            assists=gp.get_assists()
        ))
    return GameTeamRead(
        id=team.id,
        name=team.name,
        players=team_players
    )
        
def get_game(game: Game) -> GlobalPlayerStats:
    return GameRead(
        id=game.id,
        date=game.date,
        started_at=game.started_at,
        ended_at=game.ended_at,
        stadium=StadiumRead.model_validate(game.stadium),
        home_team=get_team(game.home_team),
        away_team=get_team(game.away_team),
        goals=[GoalRead.model_validate(goal) for goal in game.goals]
    )
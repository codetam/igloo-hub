from datetime import datetime
from typing import Literal, Optional, List
import uuid
from pydantic import BaseModel, computed_field
from sqlmodel import Session

from app.models.model import GamePlayer, Player

# ==========================
# PLAYER
# ==========================
class PlayerRead(BaseModel):
    id: uuid.UUID
    name: str
    nickname: Optional[str] = None
    profile: Optional[str] = None
    
class GlobalPlayerStats(BaseModel):
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

def get_player_stats(player: Player) -> GlobalPlayerStats:
    
    wins = 0
    for game_player in player.game_players:
        game = game_player.game
        player_team_id = game_player.team_id
        
        game = GameRead(**game)
        
        if player_team_id == game.home_team_id and game.score.home > game.score.away:
            wins += 1
        elif player_team_id == game.away_team_id and game.score.away > game.score.home:
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
    game_id: int
    date: datetime
    stadium: str
    team: Literal['home', 'away']
    score: str
    result: Literal['win', 'loss', 'draw']
    goals: int
    assists: int

def get_gameplayer_stats(gp: GamePlayer) -> GamePlayerStats:
    game = gp.game
    team = "home" if game.home_team_id == gp.team_id else "away"
    score = game.get_scoreboard()
    
    player_is_home = game.home_team_id == gp.team_id
    player_goals = score.home if player_is_home else score.away
    opponent_goals = score.away if player_is_home else score.home
    
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
        score=f"{score.home} - {score.away}",
        result=result, 
        goals=gp.get_goals(), 
        assists=gp.get_assists()
    )

# ==========================
# STADIUM
# ==========================
class StadiumRead(BaseModel):
    id: uuid.UUID
    name: str
    address: Optional[str] = None
    
# ==========================
# Score
# ==========================
class GameScore(BaseModel):
    home_team: int
    away_team: int

class GoalRead(BaseModel):
    id: uuid.UUID
    team_id: uuid.UUID
    minute: Optional[datetime] = None
    scorer: Optional[PlayerRead] = None
    assister: Optional[PlayerRead] = None
    
# ==========================
# TEAM
# ==========================
class GamePlayerTeamRead(BaseModel):
    player: PlayerRead
    @computed_field
    @property
    def id(self) -> uuid.UUID:
        return self.player.id
    def name(self) -> str:
        return self.player.name
    def nickname(self) -> str:
        return self.player.nickname
    def goals(self) -> int:
        return self.get_goals()
    def assists(self) -> int:
        return self.get_assists()

class GameTeamRead(BaseModel):
    id: uuid.UUID
    name: Optional[str]
    players: list[GamePlayerTeamRead]
    
# ==========================
# GAME
# ==========================

class GameRead(BaseModel):
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
        home_team = sum(1 for goal in self.goals if goal.team_id == self.home_team_id)
        away_team = sum(1 for goal in self.goals if goal.team_id == self.away_team_id)
        return GameScore(home_team=home_team, away_team=away_team)
from sqlmodel import Column, SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import uuid
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.models.schema import ScoreBoard

if TYPE_CHECKING:
    from typing import List


class Stadium(SQLModel, table=True):
    """Where you play your games"""
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(index=True)
    address: Optional[str] = None

    games: list["Game"] = Relationship(back_populates="stadium")

class Player(SQLModel, table=True):
    """Registered players"""
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(index=True)
    nickname: Optional[str] = None
    profile: Optional[str] = None
    
    game_players: list["GamePlayer"] = Relationship(back_populates="player")
    goals_scored: list["Goal"] = Relationship(back_populates="scorer")
    assists_made: list["Goal"] = Relationship(back_populates="assister")


class Team(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    name: Optional[str] = None


class Game(SQLModel, table=True):
    """A single 5v5 match"""
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    stadium_id: uuid.UUID = Field(foreign_key="stadium.id", ondelete="SET NULL", nullable=True)
    home_team_id: uuid.UUID = Field(foreign_key="team.id", ondelete="RESTRICT") 
    away_team_id: uuid.UUID = Field(foreign_key="team.id", ondelete="RESTRICT") 
    date: datetime = Field(index=True)
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    
    stadium: "Stadium" = Relationship(back_populates="games")
    game_players: list["GamePlayer"] = Relationship(back_populates="game")
    goals: List["Goal"] = Relationship(back_populates="game")
    
    def get_scoreboard(self):
        home_goals = sum(1 for goal in self.goals if goal.team_id == self.home_team_id)
        away_goals = sum(1 for goal in self.goals if goal.team_id == self.away_team_id)
        return ScoreBoard(home=home_goals, away=away_goals)

class GamePlayer(SQLModel, table=True):
    """Links players to games and assigns them to a team"""
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    game_id: uuid.UUID = Field(foreign_key="game.id", ondelete="CASCADE")
    player_id: uuid.UUID = Field(foreign_key="player.id", ondelete="CASCADE")
    team_id: uuid.UUID = Field(foreign_key="team.id", ondelete="RESTRICT")
    
    player: "Player" = Relationship(back_populates="game_players")
    game: "Game" = Relationship(back_populates="game_players")
    
    def get_goals(self) -> int:
        """Count goals scored by this player in this game"""
        return len([g for g in self.game.goals 
                   if g.scorer_id == self.player_id])
    
    def get_assists(self) -> int:
        """Count assists made by this player in this game"""
        return len([g for g in self.game.goals 
                   if g.assister_id == self.player_id])


class Goal(SQLModel, table=True):
    """Individual goal with scorer, assister, and when it happened"""
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    game_id: uuid.UUID = Field(foreign_key="game.id", ondelete="CASCADE")
    team_id: uuid.UUID = Field(foreign_key="team.id", ondelete="RESTRICT")
    scorer_id: uuid.UUID = Field(foreign_key="player.id", ondelete="RESTRICT")
    assister_id: Optional[uuid.UUID] = Field(default=None, foreign_key="player.id", ondelete="SET NULL", nullable=True)
    minute: Optional[datetime] = None  # When the goal was scored
    
    scorer: "Player" = Relationship(back_populates="goals_scored")
    assister: "Player" = Relationship(back_populates="assists_made")
    game: "Game" = Relationship(back_populates="goals")
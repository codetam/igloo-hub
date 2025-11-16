from sqlmodel import Column, SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING, List
import uuid
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

if TYPE_CHECKING:
    pass  # TYPE_CHECKING block is for avoiding circular imports


class Stadium(SQLModel, table=True):
    """Where you play your games"""
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(index=True)
    address: Optional[str] = None

    games: List["Game"] = Relationship(
        back_populates="stadium",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class Player(SQLModel, table=True):
    """Registered players"""
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(index=True)
    nickname: Optional[str] = None
    profile: Optional[str] = None
    
    game_players: List["GamePlayer"] = Relationship(
        back_populates="player",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    goals_scored: List["Goal"] = Relationship(
        back_populates="scorer",
        sa_relationship_kwargs={
            "foreign_keys": "[Goal.scorer_id]",
            "cascade": "all, delete-orphan"
        }
    )
    assists_made: List["Goal"] = Relationship(
        back_populates="assister",
        sa_relationship_kwargs={
            "foreign_keys": "[Goal.assister_id]",
        }
    )


class Team(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    name: Optional[str] = None
    
    players: List["GamePlayer"] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    home_games: List["Game"] = Relationship(
        back_populates="home_team",
        sa_relationship_kwargs={
            "foreign_keys": "[Game.home_team_id]",
        }
    )
    away_games: List["Game"] = Relationship(
        back_populates="away_team",
        sa_relationship_kwargs={
            "foreign_keys": "[Game.away_team_id]",
        }
    )
    goals: List["Goal"] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class Game(SQLModel, table=True):
    """A single 5v5 match"""
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    stadium_id: Optional[uuid.UUID] = Field(default=None, foreign_key="stadium.id")
    home_team_id: uuid.UUID = Field(foreign_key="team.id") 
    away_team_id: uuid.UUID = Field(foreign_key="team.id") 
    date: datetime = Field(index=True)
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    
    stadium: Optional["Stadium"] = Relationship(back_populates="games")
    home_team: "Team" = Relationship(
        back_populates="home_games",
        sa_relationship_kwargs={
            "foreign_keys": "[Game.home_team_id]",
        }
    )
    away_team: "Team" = Relationship(
        back_populates="away_games",
        sa_relationship_kwargs={
            "foreign_keys": "[Game.away_team_id]",
        }
    )
    game_players: List["GamePlayer"] = Relationship(
        back_populates="game",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    goals: List["Goal"] = Relationship(
        back_populates="game",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class GamePlayer(SQLModel, table=True):
    """Links players to games and assigns them to a team"""
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    game_id: uuid.UUID = Field(foreign_key="game.id")
    player_id: uuid.UUID = Field(foreign_key="player.id")
    team_id: uuid.UUID = Field(foreign_key="team.id")
    
    player: "Player" = Relationship(back_populates="game_players")
    game: "Game" = Relationship(back_populates="game_players")
    team: "Team" = Relationship(back_populates="players")
    
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
    game_id: uuid.UUID = Field(foreign_key="game.id")
    team_id: uuid.UUID = Field(foreign_key="team.id")
    scorer_id: uuid.UUID = Field(foreign_key="player.id")
    assister_id: Optional[uuid.UUID] = Field(default=None, foreign_key="player.id")
    minute: Optional[datetime] = None  # When the goal was scored
    
    scorer: "Player" = Relationship(
        back_populates="goals_scored",
        sa_relationship_kwargs={
            "foreign_keys": "[Goal.scorer_id]",
        }
    )
    assister: Optional["Player"] = Relationship(
        back_populates="assists_made",
        sa_relationship_kwargs={
            "foreign_keys": "[Goal.assister_id]",
        }
    )
    team: "Team" = Relationship(back_populates="goals")
    game: "Game" = Relationship(back_populates="goals")
from sqlmodel import Column, SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import uuid
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

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
    """Your friends who play"""
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(index=True)
    nickname: Optional[str] = None
    profile: Optional[str] = None
    
    game_players: list["GamePlayer"] = Relationship(back_populates="player")
    goals_scored: list["Goal"] = Relationship(
        back_populates="scorer",
        sa_relationship_kwargs={
            "foreign_keys": "Goal.scorer_id"
        }
    )
    assists_made: list["Goal"] = Relationship(
        back_populates="assister",
        sa_relationship_kwargs={
            "foreign_keys": "Goal.assister_id"
        }
    )


class Game(SQLModel, table=True):
    """A single 5v5 match"""
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    date: datetime = Field(index=True)
    stadium_id: uuid.UUID = Field(foreign_key="stadium.id")
    notes: Optional[str] = None  # For funny moments or whatever
    
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    
    stadium: Stadium = Relationship(back_populates="games")
    game_players: list["GamePlayer"] = Relationship(back_populates="game")
    goals: list["Goal"] = Relationship(back_populates="game")
    
    def get_score(self) -> tuple[int, int]:
        """Returns (team_1_score, team_2_score)"""
        team_1_goals = len([g for g in self.goals if g.team == 1])
        team_2_goals = len([g for g in self.goals if g.team == 2])
        return (team_1_goals, team_2_goals)
    
    def get_winner(self) -> Optional[int]:
        """Returns winning team number (1 or 2) or None if draw"""
        t1, t2 = self.get_score()
        if t1 > t2:
            return 1
        elif t2 > t1:
            return 2
        return None


class GamePlayer(SQLModel, table=True):
    """Links players to games and assigns them to a team"""
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    game_id: uuid.UUID = Field(foreign_key="game.id")
    player_id: uuid.UUID = Field(foreign_key="player.id")
    team: int = Field()  # 1 or 2
    
    game: Game = Relationship(back_populates="game_players")
    player: Player = Relationship(back_populates="game_players")
    
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
    team: int = Field()  # 1 or 2
    scorer_id: uuid.UUID = Field(foreign_key="player.id")
    assister_id: Optional[uuid.UUID] = Field(default=None, foreign_key="player.id")
    minute: Optional[datetime] = None  # When the goal was scored
    
    game: Game = Relationship(back_populates="goals")
    scorer: Player = Relationship(
        back_populates="goals_scored",
        sa_relationship_kwargs={
            "foreign_keys": "Goal.scorer_id"
        }
    )
    assister: Optional[Player] = Relationship(
        back_populates="assists_made",
        sa_relationship_kwargs={
            "foreign_keys": "Goal.assister_id"
        }
    )
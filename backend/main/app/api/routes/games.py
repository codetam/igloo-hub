from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Optional
import uuid
from datetime import datetime, timezone

from app.models.model import Game, GamePlayer, Goal, Player, Team
from app.api.deps import get_db
from app.models.schema import GameCreate, GamePlayerCreate, GameRead, GoalCreate

router = APIRouter(
    prefix="/api/games",
    tags=["games"],
)

@router.post("/{game_id}/players")
def add_player_to_game(
    game_id: uuid.UUID,
    gameplayer_data: GamePlayerCreate,
    session: Session = Depends(get_db)
):
    """Add a player to a game on a specific team"""
    game = session.get(Game, game_id)
    player = session.get(Player, gameplayer_data.player_id)
    team = session.get(Team, gameplayer_data.team_id)
    
    if not game or not player or not team:
        raise HTTPException(status_code=404, detail="Game or Player not found")

    game_player = GamePlayer(game_id=game_id, player_id=gameplayer_data.player_id, team_id=gameplayer_data.team_id)
    session.add(game_player)
    session.commit()
    return {"message": f"{player.name} added to team {gameplayer_data.team_id}"}


@router.post("/{game_id}/goals")
def add_goal(
    game_id: uuid.UUID,
    goal_data: GoalCreate,
    session: Session = Depends(get_db)
):
    """Record a goal in a game"""
    game = session.get(Game, game_id)
    scorer = session.get(Player, goal_data.scorer_id)
    
    if not game or not scorer:
        raise HTTPException(status_code=404, detail="Game or Player not found")
    
    if goal_data.team_id not in [game.home_team_id, game.away_team_id]:
        raise HTTPException(status_code=400, detail="Team must be participating")
    
    goal = Goal(
        game_id=game_id,
        team_id=goal_data.team_id,
        scorer_id=goal_data.scorer_id,
        assister_id=goal_data.assister_id,
        minute=goal_data.minute
    )
    session.add(goal)
    session.commit()
    return {"message": f"Goal recorded for {scorer.name}"}

@router.put("/{game_id}/start", response_model=GameRead)
def start_game(game_id: uuid.UUID, session: Session = Depends(get_db)):
    """Mark a game as started (set started_at to current UTC time)"""
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.started_at:
        raise HTTPException(status_code=400, detail="Game has already started")

    game.started_at = datetime.now(timezone.utc)
    session.add(game)
    session.commit()
    session.refresh(game)
    return GameRead.model_validate(game)


@router.put("/{game_id}/end", response_model=GameRead)
def end_game(game_id: uuid.UUID, session: Session = Depends(get_db)):
    """Mark a game as ended (set ended_at to current UTC time)"""
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if not game.started_at:
        raise HTTPException(status_code=400, detail="Game has not started yet")

    if game.ended_at:
        raise HTTPException(status_code=400, detail="Game has already ended")

    game.ended_at = datetime.now(timezone.utc)
    session.add(game)
    session.commit()
    session.refresh(game)
    return GameRead.model_validate(game)

@router.get("/{game_id}", response_model=GameRead)
def get_game(game_id: uuid.UUID, session: Session = Depends(get_db)):
    """Return one game with nested stadium, goals, and players"""
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    return GameRead.model_validate(game)


@router.delete("/{game_id}")
def delete_game(game_id: uuid.UUID, session: Session = Depends(get_db)):
    """Delete a game"""
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    session.delete(game)
    session.commit()
    return {"message": "Game deleted"}

@router.post("", response_model=GameRead)
def create_game(
    game_data: GameCreate,
    session: Session = Depends(get_db)
):
    """Create a new game"""
    home_team = Team()
    away_team = Team()
    
    session.add(home_team)
    session.add(away_team)
    session.commit()
    session.refresh(home_team)
    session.refresh(away_team)
    
    game = Game(stadium_id=game_data.stadium_id, date=game_data.date, 
                home_team_id=home_team.id, away_team_id=away_team.id)
    session.add(game)
    session.commit()
    session.refresh(game)
    return GameRead.model_validate(game)

@router.get("", response_model=list[GameRead])
def list_games(
    skip: int = 0,
    limit: int = 20,
    session: Session = Depends(get_db)
):
    """List all games"""
    statement = select(Game).order_by(Game.date.desc()).offset(skip).limit(limit)
    games = session.exec(statement).all()
    return [GameRead.model_validate(game) for game in games]
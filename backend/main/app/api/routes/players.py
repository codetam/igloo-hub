from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Optional
import uuid

from app.models.model import Player
from app.api.deps import get_db
from app.models.schema import GamePlayerStats, GlobalPlayerStats, PlayerRead, get_gameplayer_stats, get_player_stats

router = APIRouter(
    prefix="/api/players",
    tags=["players"],
)

@router.get("/search/by-name", response_model=PlayerRead)
def search_players_by_name(
    name: str,
    session: Session = Depends(get_db)
):
    """Search players by name (case-insensitive partial match)"""
    statement = select(Player).where(Player.name.ilike(f"%{name}%"))
    players = session.exec(statement).all()
    return [PlayerRead(**player) for player in players]


@router.get("/{player_id}/games", response_model=list[GamePlayerStats])
def get_player_games(
    player_id: uuid.UUID,
    session: Session = Depends(get_db)
):
    """Get all games a player has participated in"""
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    games_info = []
    for gp in player.game_players:
        
        games_info.append(get_gameplayer_stats(gp))
    return games_info

@router.get("/{player_id}", response_model=GlobalPlayerStats)
def get_player(player_id: uuid.UUID, session: Session = Depends(get_db)):
    """Get a specific player"""
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return get_player_stats(player)

@router.put("/{player_id}",  response_model=GlobalPlayerStats)
def update_player(
    player_id: uuid.UUID,
    name: Optional[str] = None,
    nickname: Optional[str] = None,
    session: Session = Depends(get_db)
):
    """Update player info"""
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    if name:
        player.name = name
    if nickname is not None:  # Allow setting to None
        player.nickname = nickname
    
    session.add(player)
    session.commit()
    session.refresh(player)
    return get_player_stats(player)


@router.delete("/{player_id}")
def delete_player(player_id: uuid.UUID, session: Session = Depends(get_db)):
    """Delete a player"""
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    session.delete(player)
    session.commit()
    return {"message": "Player deleted"}


@router.post("", response_model=PlayerRead)
def create_player(
    name: str,
    nickname: Optional[str] = None,
    session: Session = Depends(get_db)
):
    """Create a new player"""
    player = Player(name=name, nickname=nickname)
    session.add(player)
    session.commit()
    session.refresh(player)
    return player

@router.get("", response_model=list[GlobalPlayerStats])
def list_players(
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(get_db)
):
    """List all players"""
    statement = select(Player).order_by(Player.name).offset(skip).limit(limit)
    players = session.exec(statement).all()
    return [get_player_stats(player) for player in players]

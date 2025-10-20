from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Optional
import uuid

from app.models.model import Game, GamePlayer, Goal, Stadium, Player
from app.api.deps import get_db

router = APIRouter(
    prefix="/api/players",
    tags=["players"],
)


@router.post("", response_model=Player)
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


@router.get("/{player_id}", response_model=Player)
def get_player(player_id: uuid.UUID, session: Session = Depends(get_db)):
    """Get a specific player"""
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("", response_model=list[Player])
def list_players(
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(get_db)
):
    """List all players"""
    statement = select(Player).order_by(Player.name).offset(skip).limit(limit)
    players = session.exec(statement).all()
    return players


@router.get("/{player_id}/stats")
def get_player_stats(player_id: uuid.UUID, session: Session = Depends(get_db)):
    """Get overall stats for a player across all games"""
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    total_games = len(player.game_players)
    total_goals = len(player.goals_scored)
    total_assists = len(player.assists_made)
    
    # Calculate wins
    wins = 0
    for gp in player.game_players:
        winner = gp.game.get_winner()
        if winner == gp.team:
            wins += 1
    
    return {
        "player_id": player_id,
        "name": player.name,
        "nickname": player.nickname,
        "games_played": total_games,
        "total_goals": total_goals,
        "total_assists": total_assists,
        "wins": wins,
        "goals_per_game": round(total_goals / total_games, 2) if total_games > 0 else 0
    }


@router.get("/{player_id}/games")
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
        game = gp.game
        score = game.get_score()
        winner = game.get_winner()
        
        games_info.append({
            "game_id": game.id,
            "date": game.date,
            "stadium": game.stadium.name,
            "team": gp.team,
            "score": f"{score[0]} - {score[1]}",
            "result": "win" if winner == gp.team else ("draw" if winner is None else "loss"),
            "goals": gp.get_goals(),
            "assists": gp.get_assists()
        })
    
    return games_info


@router.put("/{player_id}")
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
    return player


@router.delete("/{player_id}")
def delete_player(player_id: uuid.UUID, session: Session = Depends(get_db)):
    """Delete a player"""
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    session.delete(player)
    session.commit()
    return {"message": "Player deleted"}


@router.get("/search/by-name")
def search_players_by_name(
    name: str,
    session: Session = Depends(get_db)
):
    """Search players by name (case-insensitive partial match)"""
    statement = select(Player).where(Player.name.ilike(f"%{name}%"))
    players = session.exec(statement).all()
    return players
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Optional
import uuid

from app.models.model import Game, GamePlayer, Goal, Stadium, Player
from app.api.deps import get_db

router = APIRouter(
    prefix="/api/stadiums",
    tags=["stadiums"],
)


@router.post("", response_model=Stadium)
def create_stadium(
    name: str,
    address: Optional[str] = None,
    session: Session = Depends(get_db)
):
    """Create a new stadium"""
    stadium = Stadium(name=name, address=address)
    session.add(stadium)
    session.commit()
    session.refresh(stadium)
    return stadium


@router.get("/{stadium_id}", response_model=Stadium)
def get_stadium(stadium_id: uuid.UUID, session: Session = Depends(get_db)):
    """Get a specific stadium"""
    stadium = session.get(Stadium, stadium_id)
    if not stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    return stadium


@router.get("", response_model=list[Stadium])
def list_stadiums(
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(get_db)
):
    """List all stadiums"""
    statement = select(Stadium).order_by(Stadium.name).offset(skip).limit(limit)
    stadiums = session.exec(statement).all()
    return stadiums


@router.get("/{stadium_id}/games")
def get_stadium_games(
    stadium_id: uuid.UUID,
    session: Session = Depends(get_db)
):
    """Get all games played at a stadium"""
    stadium = session.get(Stadium, stadium_id)
    if not stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    
    games_info = []
    for game in stadium.games:
        score = game.get_score()
        winner = game.get_winner()
        
        games_info.append({
            "game_id": game.id,
            "date": game.date,
            "score": f"{score[0]} - {score[1]}",
            "winner": f"Team {winner}" if winner else "Draw",
            "notes": game.notes
        })
    
    return {
        "stadium_id": stadium_id,
        "stadium_name": stadium.name,
        "total_games": len(stadium.games),
        "games": games_info
    }


@router.put("/{stadium_id}")
def update_stadium(
    stadium_id: uuid.UUID,
    name: Optional[str] = None,
    address: Optional[str] = None,
    session: Session = Depends(get_db)
):
    """Update stadium info"""
    stadium = session.get(Stadium, stadium_id)
    if not stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    
    if name:
        stadium.name = name
    if address is not None:
        stadium.address = address
    
    session.add(stadium)
    session.commit()
    session.refresh(stadium)
    return stadium


@router.delete("/{stadium_id}")
def delete_stadium(stadium_id: uuid.UUID, session: Session = Depends(get_db)):
    """Delete a stadium"""
    stadium = session.get(Stadium, stadium_id)
    if not stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    
    # Check if stadium has games
    if len(stadium.games) > 0:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete stadium with existing games"
        )
    
    session.delete(stadium)
    session.commit()
    return {"message": "Stadium deleted"}
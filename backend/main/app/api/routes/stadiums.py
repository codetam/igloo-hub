from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Optional
import uuid

from app.models.model import Stadium
from app.api.deps import get_db
from app.models.schema import StadiumCreate, StadiumRead

router = APIRouter(
    prefix="/api/stadiums",
    tags=["stadiums"],
)

@router.get("/{stadium_id}", response_model=StadiumRead)
def get_stadium(stadium_id: uuid.UUID, session: Session = Depends(get_db)):
    """Get a specific stadium"""
    stadium = session.get(Stadium, stadium_id)
    if not stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    return StadiumRead.model_validate(stadium)

@router.put("/{stadium_id}", response_model=StadiumRead)
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
    return StadiumRead.model_validate(stadium)


@router.delete("/{stadium_id}")
def delete_stadium(stadium_id: uuid.UUID, session: Session = Depends(get_db)):
    """Delete a stadium"""
    stadium = session.get(Stadium, stadium_id)
    if not stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    
    session.delete(stadium)
    session.commit()
    return {"message": "Stadium deleted"}

@router.post("", response_model=StadiumRead)
def create_stadium(
    stadium_data: StadiumCreate,
    session: Session = Depends(get_db)
):
    """Create a new stadium"""
    stadium = Stadium(name=stadium_data.name, address=stadium_data.address)
    session.add(stadium)
    session.commit()
    session.refresh(stadium)
    return StadiumRead.model_validate(stadium)

@router.get("", response_model=list[StadiumRead])
def list_stadiums(
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(get_db)
):
    """List all stadiums"""
    statement = select(Stadium).order_by(Stadium.name).offset(skip).limit(limit)
    stadiums = session.exec(statement).all()
    return [StadiumRead.model_validate(stadium) for stadium in stadiums]
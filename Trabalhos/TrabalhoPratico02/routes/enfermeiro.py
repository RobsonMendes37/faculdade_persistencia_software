from fastapi import APIRouter, Depends
from typing import List, Optional
from models.enfermeiro import EnfermeiroCreate, EnfermeiroPublic, EnfermeiroUpdate
from crud.enfermeiro import (
    get_all_enfermeiros, get_enfermeiros, get_enfermeiro_by_id, create_enfermeiro, update_enfermeiro, delete_enfermeiro, count_enfermeiros, filter_enfermeiros_by_name
)
from db.database import get_session
from sqlmodel import Session

router = APIRouter()

@router.get("/", response_model=List[EnfermeiroPublic])
def read_enfermeiros(session: Session = Depends(get_session), offset: int = 0, limit: int = 100):
    return get_enfermeiros(session, offset, limit)

@router.get("/quantidade")
def count_enfermeiros_endpoint(session: Session = Depends(get_session)):
    return {"quantidade": count_enfermeiros(session)}

@router.get("/all", response_model=List[EnfermeiroPublic])
def read_all_enfermeiros(session: Session = Depends(get_session)):
    return get_all_enfermeiros(session)

@router.get("/{enfermeiro_id}", response_model=EnfermeiroPublic)
def read_enfermeiro(enfermeiro_id: int, session: Session = Depends(get_session)):
    return get_enfermeiro_by_id(session, enfermeiro_id)

@router.post("/", response_model=EnfermeiroPublic)
def create_enfermeiro_endpoint(enfermeiro: EnfermeiroCreate, session: Session = Depends(get_session)):
    return create_enfermeiro(session, enfermeiro)

@router.patch("/{enfermeiro_id}", response_model=EnfermeiroPublic)
def update_enfermeiro_endpoint(enfermeiro_id: int, enfermeiro: EnfermeiroUpdate, session: Session = Depends(get_session)):
    return update_enfermeiro(session, enfermeiro_id, enfermeiro)

@router.delete("/{enfermeiro_id}")
def delete_enfermeiro_endpoint(enfermeiro_id: int, session: Session = Depends(get_session)):
    return delete_enfermeiro(session, enfermeiro_id)


@router.get("/filter", response_model=List[EnfermeiroPublic])
def filter_enfermeiros_by_name_endpoint(name: Optional[str] = None, session: Session = Depends(get_session)):
    return filter_enfermeiros_by_name(session, name)

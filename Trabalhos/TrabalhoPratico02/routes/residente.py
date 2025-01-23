from fastapi import APIRouter, Depends
from typing import List, Optional
from models.residente import ResidenteCreate, ResidentePublic, ResidenteUpdate
from crud.residente import (
    get_all_residentes, get_residentes, get_residente_by_id, create_residente, update_residente, delete_residente, count_residentes, filter_residentes_by_name
)
from db.database import get_session
from sqlmodel import Session

router = APIRouter()

@router.get("/", response_model=List[ResidentePublic])
def read_residentes(session: Session = Depends(get_session), offset: int = 0, limit: int = 100):
    return get_residentes(session, offset, limit)

@router.get("/quantidade")
def count_residentes_endpoint(session: Session = Depends(get_session)):
    return {"quantidade": count_residentes(session)}


@router.get("/filter", response_model=List[ResidentePublic])
def filter_residentes_by_name_endpoint(name: Optional[str] = None, session: Session = Depends(get_session)):
    return filter_residentes_by_name(session, name)


@router.get("/all", response_model=List[ResidentePublic])
def read_all_residentes(session: Session = Depends(get_session)):
    return get_all_residentes(session)

@router.get("/{residente_id}", response_model=ResidentePublic)
def read_residente(residente_id: int, session: Session = Depends(get_session)):
    return get_residente_by_id(session, residente_id)

@router.post("/", response_model=ResidentePublic)
def create_residente_endpoint(residente: ResidenteCreate, session: Session = Depends(get_session)):
    return create_residente(session, residente)

@router.patch("/{residente_id}", response_model=ResidentePublic)
def update_residente_endpoint(residente_id: int, residente: ResidenteUpdate, session: Session = Depends(get_session)):
    return update_residente(session, residente_id, residente)

@router.delete("/{residente_id}")
def delete_residente_endpoint(residente_id: int, session: Session = Depends(get_session)):
    return delete_residente(session, residente_id)


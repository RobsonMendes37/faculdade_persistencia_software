from fastapi import APIRouter, Depends
from typing import List, Optional
from models.medico import MedicoCreate, MedicoPublic, MedicoUpdate
from crud.medico import (
    get_all_medicos, get_medicos, get_medico_by_id, create_medico, update_medico, delete_medico, count_medicos, filter_medicos_by_name
)
from db.database import get_session
from sqlmodel import Session

router = APIRouter()

@router.get("/", response_model=List[MedicoPublic])
def read_medicos(session: Session = Depends(get_session), offset: int = 0, limit: int = 100):
    return get_medicos(session, offset, limit)

@router.get("/quantidade")
def count_medicos_endpoint(session: Session = Depends(get_session)):
    return {"quantidade": count_medicos(session)}


@router.get("/filter", response_model=List[MedicoPublic])
def filter_medicos_by_name_endpoint(name: Optional[str] = None, session: Session = Depends(get_session)):
    return filter_medicos_by_name(session, name)


@router.get("/all", response_model=List[MedicoPublic])
def read_all_medicos(session: Session = Depends(get_session)):
    return get_all_medicos(session)

@router.get("/{medico_id}", response_model=MedicoPublic)
def read_medico(medico_id: int, session: Session = Depends(get_session)):
    return get_medico_by_id(session, medico_id)

@router.post("/", response_model=MedicoPublic)
def create_medico_endpoint(medico: MedicoCreate, session: Session = Depends(get_session)):
    return create_medico(session, medico)

@router.patch("/{medico_id}", response_model=MedicoPublic)
def update_medico_endpoint(medico_id: int, medico: MedicoUpdate, session: Session = Depends(get_session)):
    return update_medico(session, medico_id, medico)

@router.delete("/{medico_id}")
def delete_medico_endpoint(medico_id: int, session: Session = Depends(get_session)):
    return delete_medico(session, medico_id)


from fastapi import APIRouter, Depends
from typing import List, Optional
from sqlmodel import Session
from models.prescricao import Prescricao, PrescricaoCreate, PrescricaoPublic, PrescricaoUpdate
from crud.prescricao import (
    get_all_prescricoes, get_prescricoes, get_prescricao_by_id, create_prescricao, update_prescricao, delete_prescricao, count_prescricoes, filter_prescricoes_by_medicamentos
)
from db.database import get_session  # Função para obter a sessão

router = APIRouter()

@router.get("/", response_model=List[PrescricaoPublic])
def read_prescricoes(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return get_prescricoes(session, offset, limit)

@router.get("/all", response_model=List[PrescricaoPublic])
def read_all_prescricoes(session: Session = Depends(get_session)):
    return get_all_prescricoes(session)

@router.get("/{prescricao_id}", response_model=PrescricaoPublic)
def read_prescricao(prescricao_id: int, session: Session = Depends(get_session)):
    return get_prescricao_by_id(session, prescricao_id)

@router.post("/", response_model=PrescricaoPublic)
def create_prescricao_endpoint(prescricao: PrescricaoCreate, session: Session = Depends(get_session)):
    return create_prescricao(session, prescricao)

@router.patch("/{prescricao_id}", response_model=PrescricaoPublic)
def update_prescricao_endpoint(prescricao_id: int, prescricao: PrescricaoUpdate, session: Session = Depends(get_session)):
    return update_prescricao(session, prescricao_id, prescricao)

@router.delete("/{prescricao_id}")
def delete_prescricao_endpoint(prescricao_id: int, session: Session = Depends(get_session)):
    return delete_prescricao(session, prescricao_id)

@router.get("/count")
def count_prescricoes_endpoint(session: Session = Depends(get_session)):
    return {"quantidade": count_prescricoes(session)}

@router.get("/filter", response_model=List[PrescricaoPublic])
def filter_prescricoes_by_medicamentos_endpoint(medicamento: Optional[str] = None, session: Session = Depends(get_session)):
    return filter_prescricoes_by_medicamentos(session, medicamento)

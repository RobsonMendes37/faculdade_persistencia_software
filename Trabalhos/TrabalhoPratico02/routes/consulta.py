from fastapi import APIRouter, Depends
from typing import List, Optional
from sqlmodel import Session
from models.consulta import Consulta, ConsultaCreate, ConsultaPublic, ConsultaUpdate
from crud.consulta import (
    get_all_consultas, get_consultas, get_consulta_by_id, create_consulta, update_consulta, delete_consulta, count_consultas, filter_consultas_by_motivo
)
from db.database import get_session  # Importando a função que cria a sessão diretamente

router = APIRouter()

# Funções de CRUD, agora a sessão é passada diretamente para cada uma delas
@router.get("/", response_model=List[ConsultaPublic])
def read_consultas(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return get_consultas(session, offset, limit)

@router.get("/quantidade")
def count_consultas_endpoint(session: Session = Depends(get_session)):
    return {"quantidade": count_consultas(session)}

@router.get("/all", response_model=List[ConsultaPublic])
def read_all_consultas(session: Session = Depends(get_session)):
    return get_all_consultas(session)

@router.get("/{consulta_id}", response_model=ConsultaPublic)
def read_consulta(consulta_id: int, session: Session = Depends(get_session)):
    return get_consulta_by_id(session, consulta_id)

@router.post("/", response_model=ConsultaPublic)
def create_consulta_endpoint(consulta: ConsultaCreate, session: Session = Depends(get_session)):
    return create_consulta(session, consulta)

@router.patch("/{consulta_id}", response_model=ConsultaPublic)
def update_consulta_endpoint(consulta_id: int, consulta: ConsultaUpdate, session: Session = Depends(get_session)):
    return update_consulta(session, consulta_id, consulta)

@router.delete("/{consulta_id}")
def delete_consulta_endpoint(consulta_id: int, session: Session = Depends(get_session)):
    return delete_consulta(session, consulta_id)


@router.get("/filter", response_model=List[ConsultaPublic])
def filter_consultas_by_motivo_endpoint(motivo: Optional[str] = None, session: Session = Depends(get_session)):
    return filter_consultas_by_motivo(session, motivo)

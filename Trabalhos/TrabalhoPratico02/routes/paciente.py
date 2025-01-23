from fastapi import APIRouter, Depends
from typing import List, Optional
from sqlmodel import Session
from models.paciente import Paciente, PacienteCreate, PacientePublic, PacienteUpdate
from crud.paciente import (
    get_all_pacientes, get_pacientes, get_paciente_by_id, create_paciente, update_paciente, delete_paciente, count_pacientes, filter_pacientes_by_name
)
from db.database import get_session  # função que retorna a sessão do banco

router = APIRouter()

@router.get("/", response_model=List[PacientePublic])
def read_pacientes(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return get_pacientes(session, offset, limit)

@router.get("/quantidade")
def count_pacientes_endpoint(session: Session = Depends(get_session)):
    return {"quantidade": count_pacientes(session)}

@router.get("/filter", response_model=List[PacientePublic])
def filter_pacientes_by_name_endpoint(name: Optional[str] = None, session: Session = Depends(get_session)):
    return filter_pacientes_by_name(session, name)


@router.get("/all", response_model=List[PacientePublic])
def read_all_pacientes(session: Session = Depends(get_session)):
    return get_all_pacientes(session)

@router.get("/{paciente_id}", response_model=PacientePublic)
def read_paciente(paciente_id: int, session: Session = Depends(get_session)):
    return get_paciente_by_id(session, paciente_id)

@router.post("/", response_model=PacientePublic)
def create_paciente_endpoint(paciente: PacienteCreate, session: Session = Depends(get_session)):
    return create_paciente(session, paciente)

@router.patch("/{paciente_id}", response_model=PacientePublic)
def update_paciente_endpoint(paciente_id: int, paciente: PacienteUpdate, session: Session = Depends(get_session)):
    return update_paciente(session, paciente_id, paciente)

@router.delete("/{paciente_id}")
def delete_paciente_endpoint(paciente_id: int, session: Session = Depends(get_session)):
    return delete_paciente(session, paciente_id)


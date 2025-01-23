from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException
from models.paciente import Paciente, PacienteCreate, PacienteUpdate
from utils.logger import logger  # Importando o logger

# Função para obter pacientes com paginação
def get_pacientes(session: Session, offset: int = 0, limit: int = 100) -> List[Paciente]:
    pacientes = session.exec(select(Paciente).offset(offset).limit(limit)).all()
    logger.info(f"Retornados {len(pacientes)} pacientes com offset={offset} e limit={limit}")
    return pacientes

# Função para obter todos os pacientes
def get_all_pacientes(session: Session):
    pacientes = session.exec(select(Paciente)).all()
    logger.info(f"Retornados {len(pacientes)} pacientes no total")
    return pacientes

# Função para obter um paciente pelo ID
def get_paciente_by_id(session: Session, paciente_id: int) -> Paciente:
    paciente = session.get(Paciente, paciente_id)
    if not paciente:
        logger.warning(f"Tentativa de acessar paciente com ID {paciente_id}, mas não encontrado")
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    logger.info(f"Paciente com ID {paciente_id} encontrado")
    return paciente

# Função para criar um novo paciente
def create_paciente(session: Session, paciente_data: PacienteCreate) -> Paciente:
    db_paciente = Paciente.model_validate(paciente_data)
    session.add(db_paciente)
    session.commit()
    session.refresh(db_paciente)
    logger.info(f"Paciente {db_paciente.name} criado com sucesso!")
    return db_paciente

# Função para atualizar um paciente
def update_paciente(session: Session, paciente_id: int, paciente_data: PacienteUpdate) -> Paciente:
    paciente_db = session.get(Paciente, paciente_id)
    if not paciente_db:
        logger.warning(f"Tentativa de atualizar paciente com ID {paciente_id}, mas não encontrado")
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    paciente_update_data = paciente_data.model_dump(exclude_unset=True)
    paciente_db.sqlmodel_update(paciente_update_data)
    session.add(paciente_db)
    session.commit()
    session.refresh(paciente_db)
    logger.info(f"Paciente com ID {paciente_id} atualizado com sucesso!")
    return paciente_db

# Função para deletar um paciente
def delete_paciente(session: Session, paciente_id: int) -> dict:
    paciente = session.get(Paciente, paciente_id)
    if not paciente:
        logger.warning(f"Tentativa de deletar paciente com ID {paciente_id}, mas não encontrado")
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    session.delete(paciente)
    session.commit()
    logger.info(f"Paciente com ID {paciente_id} deletado com sucesso!")
    return {"ok": True}

# Função para contar a quantidade de pacientes
def count_pacientes(session: Session) -> int:
    pacientes = session.exec(select(Paciente)).all()  # Retorna todos os registros de pacientes
    count = len(pacientes)  # Conta a quantidade de pacientes
    logger.info(f"Quantidade total de pacientes: {count}")
    return count

# Função para filtrar pacientes por nome
def filter_pacientes_by_name(session: Session, name: Optional[str] = None):
    query = select(Paciente)
    if name:
        query = query.where(Paciente.name.ilike(f"%{name}%"))  # Busca parcial no nome
    pacientes = session.exec(query).all()
    logger.info(f"Filtrados {len(pacientes)} pacientes pelo nome '{name}'")
    return pacientes

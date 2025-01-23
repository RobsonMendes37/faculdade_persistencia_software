from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException
from models.enfermeiro import Enfermeiro, EnfermeiroCreate, EnfermeiroUpdate  # Modificado para importar os modelos de Enfermeiro
from utils.logger import logger  # Importando o logger

# Função para obter médicos com paginação
def get_enfermeiros(session: Session, offset: int = 0, limit: int = 100) -> List[Enfermeiro]:
    enfermeiros = session.exec(select(Enfermeiro).offset(offset).limit(limit)).all()
    logger.info(f"Retornados {len(enfermeiros)} médicos com offset={offset} e limit={limit}")
    return enfermeiros

# Função para obter todos os médicos
def get_all_enfermeiros(session: Session):
    enfermeiros = session.exec(select(Enfermeiro)).all()
    logger.info(f"Retornados {len(enfermeiros)} médicos no total")
    return enfermeiros

# Função para obter um médico pelo ID
def get_enfermeiro_by_id(session: Session, enfermeiro_id: int) -> Enfermeiro:
    enfermeiro = session.get(Enfermeiro, enfermeiro_id)
    if not enfermeiro:
        logger.warning(f"Tentativa de acessar médico com ID {enfermeiro_id}, mas não encontrado")
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    logger.info(f"Médico com ID {enfermeiro_id} encontrado")
    return enfermeiro

# Função para criar um novo médico
def create_enfermeiro(session: Session, enfermeiro_data: EnfermeiroCreate) -> Enfermeiro:
    db_enfermeiro = Enfermeiro.model_validate(enfermeiro_data)
    session.add(db_enfermeiro)
    session.commit()
    session.refresh(db_enfermeiro)
    logger.info(f"Médico {db_enfermeiro.name} criado com sucesso!")
    return db_enfermeiro

# Função para atualizar um médico
def update_enfermeiro(session: Session, enfermeiro_id: int, enfermeiro_data: EnfermeiroUpdate) -> Enfermeiro:
    enfermeiro_db = session.get(Enfermeiro, enfermeiro_id)
    if not enfermeiro_db:
        logger.warning(f"Tentativa de atualizar médico com ID {enfermeiro_id}, mas não encontrado")
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    enfermeiro_update_data = enfermeiro_data.model_dump(exclude_unset=True)
    enfermeiro_db.sqlmodel_update(enfermeiro_update_data)
    session.add(enfermeiro_db)
    session.commit()
    session.refresh(enfermeiro_db)
    logger.info(f"Médico com ID {enfermeiro_id} atualizado com sucesso!")
    return enfermeiro_db

# Função para deletar um médico
def delete_enfermeiro(session: Session, enfermeiro_id: int) -> dict:
    enfermeiro = session.get(Enfermeiro, enfermeiro_id)
    if not enfermeiro:
        logger.warning(f"Tentativa de deletar médico com ID {enfermeiro_id}, mas não encontrado")
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    session.delete(enfermeiro)
    session.commit()
    logger.info(f"Médico com ID {enfermeiro_id} deletado com sucesso!")
    return {"ok": True}

# Função para contar a quantidade de médicos
def count_enfermeiros(session: Session) -> int:
    enfermeiros = session.exec(select(Enfermeiro)).all()  # Retorna todos os registros de enfermeiros
    count = len(enfermeiros)  # Conta a quantidade de enfermeiros
    logger.info(f"Quantidade total de enfermeiros: {count}")
    return count

# Função para filtrar médicos por nome
def filter_enfermeiros_by_name(session: Session, name: Optional[str] = None):
    query = select(Enfermeiro)
    if name:
        query = query.where(Enfermeiro.name.ilike(f"%{name}%"))  # Busca parcial no nome
    enfermeiros = session.exec(query).all()
    logger.info(f"Filtrados {len(enfermeiros)} médicos pelo nome '{name}'")
    return enfermeiros

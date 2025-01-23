from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException
from models.medico import Medico, MedicoCreate, MedicoUpdate  # Modificado para importar os modelos de Medico
from utils.logger import logger  # Importando o logger

# Função para obter médicos com paginação
def get_medicos(session: Session, offset: int = 0, limit: int = 100) -> List[Medico]:
    medicos = session.exec(select(Medico).offset(offset).limit(limit)).all()
    logger.info(f"Retornados {len(medicos)} médicos com offset={offset} e limit={limit}")
    return medicos

# Função para obter todos os médicos
def get_all_medicos(session: Session):
    medicos = session.exec(select(Medico)).all()
    logger.info(f"Retornados {len(medicos)} médicos no total")
    return medicos

# Função para obter um médico pelo ID
def get_medico_by_id(session: Session, medico_id: int) -> Medico:
    medico = session.get(Medico, medico_id)
    if not medico:
        logger.warning(f"Tentativa de acessar médico com ID {medico_id}, mas não encontrado")
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    logger.info(f"Médico com ID {medico_id} encontrado")
    return medico

# Função para criar um novo médico
def create_medico(session: Session, medico_data: MedicoCreate) -> Medico:
    db_medico = Medico.model_validate(medico_data)
    session.add(db_medico)
    session.commit()
    session.refresh(db_medico)
    logger.info(f"Médico {db_medico.name} criado com sucesso!")
    return db_medico

# Função para atualizar um médico
def update_medico(session: Session, medico_id: int, medico_data: MedicoUpdate) -> Medico:
    medico_db = session.get(Medico, medico_id)
    if not medico_db:
        logger.warning(f"Tentativa de atualizar médico com ID {medico_id}, mas não encontrado")
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    medico_update_data = medico_data.model_dump(exclude_unset=True)
    medico_db.sqlmodel_update(medico_update_data)
    session.add(medico_db)
    session.commit()
    session.refresh(medico_db)
    logger.info(f"Médico com ID {medico_id} atualizado com sucesso!")
    return medico_db

# Função para deletar um médico
def delete_medico(session: Session, medico_id: int) -> dict:
    medico = session.get(Medico, medico_id)
    if not medico:
        logger.warning(f"Tentativa de deletar médico com ID {medico_id}, mas não encontrado")
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    session.delete(medico)
    session.commit()
    logger.info(f"Médico com ID {medico_id} deletado com sucesso!")
    return {"ok": True}

# Função para contar a quantidade de médicos
def count_medicos(session: Session) -> int:
    medicos = session.exec(select(Medico)).all()  # Retorna todos os registros de medicos
    count = len(medicos)  # Conta a quantidade de medicos
    logger.info(f"Quantidade total de medicos: {count}")
    return count

# Função para filtrar médicos por nome
def filter_medicos_by_name(session: Session, name: Optional[str] = None):
    query = select(Medico)
    if name:
        query = query.where(Medico.name.ilike(f"%{name}%"))  # Busca parcial no nome
    medicos = session.exec(query).all()
    logger.info(f"Filtrados {len(medicos)} médicos pelo nome '{name}'")
    return medicos

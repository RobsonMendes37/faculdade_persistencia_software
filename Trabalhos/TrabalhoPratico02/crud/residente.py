from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException
from models.residente import Residente, ResidenteCreate, ResidenteUpdate  # Modificado para importar os modelos de Residente
from utils.logger import logger  # Importando o logger

# Função para obter médicos com paginação
def get_residentes(session: Session, offset: int = 0, limit: int = 100) -> List[Residente]:
    residentes = session.exec(select(Residente).offset(offset).limit(limit)).all()
    logger.info(f"Retornados {len(residentes)} médicos com offset={offset} e limit={limit}")
    return residentes

# Função para obter todos os médicos
def get_all_residentes(session: Session):
    residentes = session.exec(select(Residente)).all()
    logger.info(f"Retornados {len(residentes)} médicos no total")
    return residentes

# Função para obter um médico pelo ID
def get_residente_by_id(session: Session, residente_id: int) -> Residente:
    residente = session.get(Residente, residente_id)
    if not residente:
        logger.warning(f"Tentativa de acessar médico com ID {residente_id}, mas não encontrado")
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    logger.info(f"Médico com ID {residente_id} encontrado")
    return residente

# Função para criar um novo médico
def create_residente(session: Session, residente_data: ResidenteCreate) -> Residente:
    db_residente = Residente.model_validate(residente_data)
    session.add(db_residente)
    session.commit()
    session.refresh(db_residente)
    logger.info(f"Médico {db_residente.name} criado com sucesso!")
    return db_residente

# Função para atualizar um médico
def update_residente(session: Session, residente_id: int, residente_data: ResidenteUpdate) -> Residente:
    residente_db = session.get(Residente, residente_id)
    if not residente_db:
        logger.warning(f"Tentativa de atualizar médico com ID {residente_id}, mas não encontrado")
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    residente_update_data = residente_data.model_dump(exclude_unset=True)
    residente_db.sqlmodel_update(residente_update_data)
    session.add(residente_db)
    session.commit()
    session.refresh(residente_db)
    logger.info(f"Médico com ID {residente_id} atualizado com sucesso!")
    return residente_db

# Função para deletar um médico
def delete_residente(session: Session, residente_id: int) -> dict:
    residente = session.get(Residente, residente_id)
    if not residente:
        logger.warning(f"Tentativa de deletar médico com ID {residente_id}, mas não encontrado")
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    session.delete(residente)
    session.commit()
    logger.info(f"Médico com ID {residente_id} deletado com sucesso!")
    return {"ok": True}

# Função para contar a quantidade de médicos
def count_residentes(session: Session) -> int:
    residentes = session.exec(select(Residente)).all()  # Retorna todos os registros de residentes
    count = len(residentes)  # Conta a quantidade de residentes
    logger.info(f"Quantidade total de residentes: {count}")
    return count

# Função para filtrar médicos por nome
def filter_residentes_by_name(session: Session, name: Optional[str] = None):
    query = select(Residente)
    if name:
        query = query.where(Residente.name.ilike(f"%{name}%"))  # Busca parcial no nome
    residentes = session.exec(query).all()
    logger.info(f"Filtrados {len(residentes)} médicos pelo nome '{name}'")
    return residentes

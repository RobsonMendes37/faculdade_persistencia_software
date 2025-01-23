from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException
from models.prescricao import Prescricao, PrescricaoCreate, PrescricaoUpdate
from utils.logger import logger

# Função para obter prescrições com paginação
def get_prescricoes(session: Session, offset: int = 0, limit: int = 100) -> List[Prescricao]:
    prescricoes = session.exec(select(Prescricao).offset(offset).limit(limit)).all()
    logger.info(f"Retornados {len(prescricoes)} prescrições com offset={offset} e limit={limit}")
    return prescricoes

# Função para obter todas as prescrições
def get_all_prescricoes(session: Session):
    prescricoes = session.exec(select(Prescricao)).all()
    logger.info(f"Retornados {len(prescricoes)} prescrições no total")
    return prescricoes

# Função para obter uma prescrição pelo ID
def get_prescricao_by_id(session: Session, prescricao_id: int) -> Prescricao:
    prescricao = session.get(Prescricao, prescricao_id)
    if not prescricao:
        logger.warning(f"Tentativa de acessar prescrição com ID {prescricao_id}, mas não encontrada")
        raise HTTPException(status_code=404, detail="Prescrição não encontrada")
    logger.info(f"Prescrição com ID {prescricao_id} encontrada")
    return prescricao

# Função para criar uma nova prescrição
def create_prescricao(session: Session, prescricao_data: PrescricaoCreate) -> Prescricao:
    db_prescricao = Prescricao.model_validate(prescricao_data)
    session.add(db_prescricao)
    session.commit()
    session.refresh(db_prescricao)
    logger.info(f"Prescrição criada com sucesso! Consulta ID: {db_prescricao.consulta_id}")
    return db_prescricao

# Função para atualizar uma prescrição
def update_prescricao(session: Session, prescricao_id: int, prescricao_data: PrescricaoUpdate) -> Prescricao:
    prescricao_db = session.get(Prescricao, prescricao_id)
    if not prescricao_db:
        logger.warning(f"Tentativa de atualizar prescrição com ID {prescricao_id}, mas não encontrada")
        raise HTTPException(status_code=404, detail="Prescrição não encontrada")
    prescricao_update_data = prescricao_data.model_dump(exclude_unset=True)
    prescricao_db.sqlmodel_update(prescricao_update_data)
    session.add(prescricao_db)
    session.commit()
    session.refresh(prescricao_db)
    logger.info(f"Prescrição com ID {prescricao_id} atualizada com sucesso!")
    return prescricao_db

# Função para deletar uma prescrição
def delete_prescricao(session: Session, prescricao_id: int) -> dict:
    prescricao = session.get(Prescricao, prescricao_id)
    if not prescricao:
        logger.warning(f"Tentativa de deletar prescrição com ID {prescricao_id}, mas não encontrada")
        raise HTTPException(status_code=404, detail="Prescrição não encontrada")
    session.delete(prescricao)
    session.commit()
    logger.info(f"Prescrição com ID {prescricao_id} deletada com sucesso!")
    return {"ok": True}

# Função para contar a quantidade de prescrições
def count_prescricoes(session: Session) -> int:
    count = session.exec(select(Prescricao)).count()
    logger.info(f"Quantidade total de prescrições: {count}")
    return count

# Função para filtrar prescrições por medicamentos
def filter_prescricoes_by_medicamentos(session: Session, medicamento: Optional[str] = None):
    query = select(Prescricao)
    if medicamento:
        query = query.where(Prescricao.medicamentos.any(medicamento))
    prescricoes = session.exec(query).all()
    logger.info(f"Filtrados {len(prescricoes)} prescrições pelo medicamento '{medicamento}'")
    return prescricoes

from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException
from models.consulta import Consulta, ConsultaCreate, ConsultaUpdate
from utils.logger import logger  # Importando o logger

# Função para obter consultas com paginação
def get_consultas(session: Session, offset: int = 0, limit: int = 100) -> List[Consulta]:
    consultas = session.exec(select(Consulta).offset(offset).limit(limit)).all()
    logger.info(f"Retornados {len(consultas)} consultas com offset={offset} e limit={limit}")
    return consultas

# Função para obter todas as consultas
def get_all_consultas(session: Session):
    consultas = session.exec(select(Consulta)).all()
    logger.info(f"Retornados {len(consultas)} consultas no total")
    return consultas

# Função para obter uma consulta pelo ID
def get_consulta_by_id(session: Session, consulta_id: int) -> Consulta:
    consulta = session.get(Consulta, consulta_id)
    if not consulta:
        logger.warning(f"Tentativa de acessar consulta com ID {consulta_id}, mas não encontrada")
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    logger.info(f"Consulta com ID {consulta_id} encontrada")
    return consulta

# Função para criar uma nova consulta
def create_consulta(session: Session, consulta_data: ConsultaCreate) -> Consulta:
    db_consulta = Consulta.model_validate(consulta_data)
    session.add(db_consulta)
    session.commit()
    session.refresh(db_consulta)
    logger.info(f"Consulta criada com sucesso! Paciente: {db_consulta.paciente_id}, Médico: {db_consulta.medico_id}")
    return db_consulta

# Função para atualizar uma consulta
def update_consulta(session: Session, consulta_id: int, consulta_data: ConsultaUpdate) -> Consulta:
    consulta_db = session.get(Consulta, consulta_id)
    if not consulta_db:
        logger.warning(f"Tentativa de atualizar consulta com ID {consulta_id}, mas não encontrada")
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    consulta_update_data = consulta_data.model_dump(exclude_unset=True)
    consulta_db.sqlmodel_update(consulta_update_data)
    session.add(consulta_db)
    session.commit()
    session.refresh(consulta_db)
    logger.info(f"Consulta com ID {consulta_id} atualizada com sucesso!")
    return consulta_db

# Função para deletar uma consulta
def delete_consulta(session: Session, consulta_id: int) -> dict:
    consulta = session.get(Consulta, consulta_id)
    if not consulta:
        logger.warning(f"Tentativa de deletar consulta com ID {consulta_id}, mas não encontrada")
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    session.delete(consulta)
    session.commit()
    logger.info(f"Consulta com ID {consulta_id} deletada com sucesso!")
    return {"ok": True}

# Função para contar a quantidade de consultas
def count_consultas(session: Session) -> int:
    consultas = session.exec(select(Consulta)).all()  # Retorna todos os registros de consultas
    count = len(consultas)  # Conta a quantidade de consultas
    logger.info(f"Quantidade total de consultas: {count}")
    return count

# Função para filtrar consultas por motivo
def filter_consultas_by_motivo(session: Session, motivo: Optional[str] = None):
    query = select(Consulta)
    if motivo:
        query = query.where(Consulta.motivo.ilike(f"%{motivo}%"))  # Busca parcial no motivo
    consultas = session.exec(query).all()
    logger.info(f"Filtrados {len(consultas)} consultas pelo motivo '{motivo}'")
    return consultas

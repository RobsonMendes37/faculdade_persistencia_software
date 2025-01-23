from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException
from models.hero import Hero, HeroCreate, HeroUpdate
from utils.logger import logger  # Importando o logger

def get_heroes(session: Session, offset: int = 0, limit: int = 100) -> List[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    logger.info(f"Retornados {len(heroes)} heróis com offset={offset} e limit={limit}")
    return heroes

def get_all_heroes(session: Session):
    heroes = session.exec(select(Hero)).all()
    logger.info(f"Retornados {len(heroes)} heróis no total")
    return heroes

def get_hero_by_id(session: Session, hero_id: int) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        logger.warning(f"Tentativa de acessar herói com ID {hero_id}, mas não encontrado")
        raise HTTPException(status_code=404, detail="Hero not found")
    logger.info(f"Herói com ID {hero_id} encontrado")
    return hero

def create_hero(session: Session, hero_data: HeroCreate) -> Hero:
    db_hero = Hero.model_validate(hero_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    logger.info(f"Herói {db_hero.name} criado com sucesso!")
    return db_hero

def update_hero(session: Session, hero_id: int, hero_data: HeroUpdate) -> Hero:
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        logger.warning(f"Tentativa de atualizar herói com ID {hero_id}, mas não encontrado")
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_update_data = hero_data.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_update_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    logger.info(f"Herói com ID {hero_id} atualizado com sucesso!")
    return hero_db

def delete_hero(session: Session, hero_id: int) -> dict:
    hero = session.get(Hero, hero_id)
    if not hero:
        logger.warning(f"Tentativa de deletar herói com ID {hero_id}, mas não encontrado")
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    logger.info(f"Herói com ID {hero_id} deletado com sucesso!")
    return {"ok": True}

def count_heroes(session: Session) -> int:
    heroes = session.exec(select(Hero)).all()  # Retorna todos os registros de heróis
    count = len(heroes)  # Conta a quantidade de heróis
    logger.info(f"Quantidade total de heróis: {count}")
    return count
 

def filter_heroes_by_name(session: Session, name: Optional[str] = None):
    query = select(Hero)
    if name:
        query = query.where(Hero.name.ilike(f"%{name}%"))
    heroes = session.exec(query).all()
    logger.info(f"Filtrados {len(heroes)} heróis pelo nome '{name}'")
    return heroes

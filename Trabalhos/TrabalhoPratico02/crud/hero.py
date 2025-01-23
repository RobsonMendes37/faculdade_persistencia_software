from typing import List
from sqlmodel import Session, select
from fastapi import HTTPException

from models.hero import Hero, HeroCreate, HeroUpdate

def get_heroes(session: Session, offset: int = 0, limit: int = 100) -> List[Hero]:
    return session.exec(select(Hero).offset(offset).limit(limit)).all()

def get_hero_by_id(session: Session, hero_id: int) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

def create_hero(session: Session, hero_data: HeroCreate) -> Hero:
    db_hero = Hero.model_validate(hero_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

def update_hero(session: Session, hero_id: int, hero_data: HeroUpdate) -> Hero:
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_update_data = hero_data.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_update_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

def delete_hero(session: Session, hero_id: int) -> dict:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}

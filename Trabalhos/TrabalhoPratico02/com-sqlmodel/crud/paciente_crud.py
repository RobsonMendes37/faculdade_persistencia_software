from sqlmodel import Session, select
from models.paciente import Hero

def create_hero(hero: Hero, session: Session) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

def get_heroes(session: Session, offset: int = 0, limit: int = 100) -> list[Hero]:
    return session.exec(select(Hero).offset(offset).limit(limit)).all()

def get_hero(hero_id: int, session: Session) -> Hero | None:
    return session.get(Hero, hero_id)

def delete_hero(hero_id: int, session: Session) -> bool:
    hero = session.get(Hero, hero_id)
    if hero:
        session.delete(hero)
        session.commit()
        return True
    return False

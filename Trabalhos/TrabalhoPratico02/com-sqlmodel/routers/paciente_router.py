from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated
from database import get_session
from models.paciente import Hero
from crud.paciente_crud import create_hero, get_heroes, get_hero, delete_hero
from sqlmodel import Session

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

@router.post("/")
def create_hero_endpoint(hero: Hero, session: SessionDep) -> Hero:
    return create_hero(hero, session)

@router.get("/")
def read_heroes_endpoint(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    return get_heroes(session, offset, limit)

@router.get("/{hero_id}")
def read_hero_endpoint(hero_id: int, session: SessionDep) -> Hero:
    hero = get_hero(hero_id, session)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@router.delete("/{hero_id}")
def delete_hero_endpoint(hero_id: int, session: SessionDep):
    if not delete_hero(hero_id, session):
        raise HTTPException(status_code=404, detail="Hero not found")
    return {"ok": True}

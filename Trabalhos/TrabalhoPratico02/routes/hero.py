from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from crud.hero import count_heroes, filter_heroes_by_name, get_all_heroes, get_heroes, get_hero_by_id, create_hero, update_hero, delete_hero
from db.database import get_session
from models.hero import Hero, HeroCreate, HeroPublic, HeroUpdate

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/filter", response_model=List[HeroPublic])
def filter_heroes_by_name_endpoint(
    session: SessionDep,
    name: Optional[str] = Query(None, description="Nome parcial ou completo para filtrar"),
):
    return filter_heroes_by_name(session, name=name)


@router.get("/quantidade", response_model=dict)
def get_hero_count(session: SessionDep):
    quantidade = count_heroes(session)
    return {"quantidade": quantidade}



@router.get("/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return get_heroes(session, offset, limit)

@router.get("/all", response_model=List[HeroPublic])
def read_all_heroes(session: SessionDep):
    return get_all_heroes(session)

@router.get("/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    return get_hero_by_id(session, hero_id)

@router.post("/", response_model=HeroPublic)
def create_hero_endpoint(hero: HeroCreate, session: SessionDep):
    return create_hero(session, hero)

@router.patch("/{hero_id}", response_model=HeroPublic)
def update_hero_endpoint(hero_id: int, hero: HeroUpdate, session: SessionDep):
    return update_hero(session, hero_id, hero)

@router.delete("/{hero_id}")
def delete_hero_endpoint(hero_id: int, session: SessionDep):
    return delete_hero(session, hero_id)

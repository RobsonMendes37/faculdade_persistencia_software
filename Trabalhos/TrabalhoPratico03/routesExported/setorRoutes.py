from fastapi import APIRouter, HTTPException
from database.config import db
from models.schemas import Setor
from typing import List
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=Setor)
async def criar_setor(setor: Setor):
    """
    Cria um novo setor no banco de dados.
    """
    # Converte o objeto Setor para um dicionário, removendo o campo 'id' para que o MongoDB gere automaticamente o _id
    setor_dict = setor.dict(by_alias=True, exclude={"id"})
    novo_setor = await db.setores.insert_one(setor_dict)
    
    # Busca o documento recém-criado
    setor_criado = await db.setores.find_one({"_id": novo_setor.inserted_id})
    if not setor_criado:
        raise HTTPException(status_code=400, detail="Erro ao criar setor")
    
    # Converte ObjectId para string antes de retornar
    setor_criado["_id"] = str(setor_criado["_id"])
    return setor_criado


@router.get("/", response_model=List[Setor])
async def listar_setores(skip: int = 0, limit: int = 10):
    """
    Lista os setores com suporte a paginação.
    """
    setores = await db.setores.find().skip(skip).limit(limit).to_list(100)
    for setor in setores:
        setor["_id"] = str(setor["_id"])
    return setores


@router.get("/setor/{setor_id}", response_model=Setor)
async def obter_setor(setor_id: str):
    """
    Busca um setor pelo ID fornecido.
    """
    if not ObjectId.is_valid(setor_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    setor = await db.setores.find_one({"_id": ObjectId(setor_id)})
    if not setor:
        raise HTTPException(status_code=404, detail="Setor não encontrado")
    
    setor["_id"] = str(setor["_id"])
    return setor


@router.put("/{setor_id}", response_model=Setor)
async def atualizar_setor(setor_id: str, setor: Setor):
    """
    Atualiza os dados de um setor pelo ID.
    """
    if not ObjectId.is_valid(setor_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    setor_dict = setor.dict(by_alias=True, exclude={"id"})
    resultado = await db.setores.update_one({"_id": ObjectId(setor_id)}, {"$set": setor_dict})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Setor não encontrado")
    
    setor_atualizado = await db.setores.find_one({"_id": ObjectId(setor_id)})
    setor_atualizado["_id"] = str(setor_atualizado["_id"])
    return setor_atualizado


@router.delete("/{setor_id}")
async def deletar_setor(setor_id: str):
    """
    Deleta um setor do banco de dados pelo ID.
    """
    if not ObjectId.is_valid(setor_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    resultado = await db.setores.delete_one({"_id": ObjectId(setor_id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Setor não encontrado")
    
    return {"message": "Setor deletado com sucesso"}

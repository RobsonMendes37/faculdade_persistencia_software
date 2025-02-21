from fastapi import APIRouter, HTTPException
from database.config import db
from models.schemas import Sessao
from typing import List
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=Sessao)
async def criar_sessao(sessao: Sessao):
    """
    Cria uma nova sessão no banco de dados.
    """
    sessao_dict = sessao.dict(by_alias=True, exclude={"id"})  # Exclui o campo 'id' para que o Mongo gere um novo _id
    nova_sessao = await db.sessoes.insert_one(sessao_dict)
    
    # Busca a sessão recém-criada
    sessao_criada = await db.sessoes.find_one({"_id": nova_sessao.inserted_id})
    if not sessao_criada:
        raise HTTPException(status_code=400, detail="Erro ao criar sessão")
    
    sessao_criada["_id"] = str(sessao_criada["_id"])  # Converte ObjectId para string
    return sessao_criada


@router.get("/", response_model=List[Sessao])
async def listar_sessoes(skip: int = 0, limit: int = 10):
    """
    Lista as sessões com suporte a paginação.
    """
    sessoes = await db.sessoes.find().skip(skip).limit(limit).to_list(100)
    for sessao in sessoes:
        sessao["_id"] = str(sessao["_id"])  # Converte ObjectId para string
    return sessoes


@router.get("/sessao/{sessao_id}", response_model=Sessao)
async def obter_sessao(sessao_id: str):
    """
    Busca uma sessão pelo ID fornecido.
    """
    if not ObjectId.is_valid(sessao_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    sessao = await db.sessoes.find_one({"_id": ObjectId(sessao_id)})
    if not sessao:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    
    sessao["_id"] = str(sessao["_id"])
    return sessao


@router.put("/{sessao_id}", response_model=Sessao)
async def atualizar_sessao(sessao_id: str, sessao: Sessao):
    """
    Atualiza os dados de uma sessão pelo ID.
    """
    if not ObjectId.is_valid(sessao_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    sessao_dict = sessao.dict(by_alias=True, exclude={"id"})
    resultado = await db.sessoes.update_one({"_id": ObjectId(sessao_id)}, {"$set": sessao_dict})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    
    sessao_atualizada = await db.sessoes.find_one({"_id": ObjectId(sessao_id)})
    sessao_atualizada["_id"] = str(sessao_atualizada["_id"])
    return sessao_atualizada


@router.delete("/{sessao_id}")
async def deletar_sessao(sessao_id: str):
    """
    Deleta uma sessão do banco de dados pelo ID.
    """
    if not ObjectId.is_valid(sessao_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    resultado = await db.sessoes.delete_one({"_id": ObjectId(sessao_id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    
    return {"message": "Sessão deletada com sucesso"}

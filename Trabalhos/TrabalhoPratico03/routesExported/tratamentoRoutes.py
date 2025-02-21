from fastapi import APIRouter, HTTPException, Query
from database.config import db
from models.schemas import Tratamento
from typing import List, Dict, Any
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=Tratamento)
async def criar_tratamento(tratamento: Tratamento):
    tratamento_dict = tratamento.dict(by_alias=True, exclude={"id"})  # Remove o campo id para o Mongo gerar um novo
    novo_tratamento = await db.tratamentos.insert_one(tratamento_dict)

    tratamento_criado = await db.tratamentos.find_one({"_id": novo_tratamento.inserted_id})
    if not tratamento_criado:
        raise HTTPException(status_code=400, detail="Erro ao criar tratamento")

    tratamento_criado["_id"] = str(tratamento_criado["_id"])  # Converte ObjectId para string
    return tratamento_criado


@router.get("/", response_model=List[Tratamento])
async def listar_tratamentos(skip: int = 0, limit: int = 10):
    tratamentos = await db.tratamentos.find().skip(skip).limit(limit).to_list(100)

    # Converte ObjectId para string e ajusta a lista de pacientes, se presente
    for trat in tratamentos:
        trat["_id"] = str(trat["_id"])
        if "pacientes" in trat and isinstance(trat["pacientes"], list):
            trat["pacientes"] = [
                str(paciente_id) if isinstance(paciente_id, ObjectId) else paciente_id
                for paciente_id in trat["pacientes"]
            ]
    return tratamentos


@router.get("/tratamentos/{tratamento_id}", response_model=Tratamento)
async def buscar_tratamento_por_id(tratamento_id: str) -> Dict[str, Any]:
    """
    Busca um tratamento pelo ID, aceitando tanto ObjectId quanto string.
    """
    filtro = {"_id": ObjectId(tratamento_id)} if ObjectId.is_valid(tratamento_id) else {"_id": tratamento_id}
    tratamento = await db.tratamentos.find_one(filtro)

    if not tratamento:
        raise HTTPException(status_code=404, detail="Tratamento não encontrado")

    tratamento["_id"] = str(tratamento["_id"])

    if "pacientes" in tratamento and isinstance(tratamento["pacientes"], list):
        tratamento["pacientes"] = [
            str(paciente_id) if isinstance(paciente_id, ObjectId) else paciente_id
            for paciente_id in tratamento["pacientes"]
        ]
    return tratamento


@router.put("/{tratamento_id}", response_model=Tratamento)
async def atualizar_tratamento(tratamento_id: str, tratamento: Tratamento):
    if not ObjectId.is_valid(tratamento_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    tratamento_dict = tratamento.dict(by_alias=True, exclude={"id"})
    resultado = await db.tratamentos.update_one({"_id": ObjectId(tratamento_id)}, {"$set": tratamento_dict})

    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Tratamento não encontrado")

    tratamento_atualizado = await db.tratamentos.find_one({"_id": ObjectId(tratamento_id)})
    tratamento_atualizado["_id"] = str(tratamento_atualizado["_id"])
    return tratamento_atualizado


@router.delete("/{tratamento_id}")
async def deletar_tratamento(tratamento_id: str):
    if not ObjectId.is_valid(tratamento_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    resultado = await db.tratamentos.delete_one({"_id": ObjectId(tratamento_id)})

    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tratamento não encontrado")

    return {"message": "Tratamento deletado com sucesso"}


@router.get("/estatisticas/pacientes_por_tratamento")
async def pacientes_por_tratamento():
    """
    Retorna estatísticas com o nome do tratamento e a quantidade de pacientes envolvidos.
    """
    pipeline = [
        {"$project": {"nome": 1, "total_pacientes": {"$size": "$pacientes"}}},
        {"$sort": {"total_pacientes": -1}}
    ]
    
    resultado = await db.tratamentos.aggregate(pipeline).to_list(100)

    for trat in resultado:
        trat["_id"] = str(trat["_id"])
    
    return resultado


@router.get("/buscar/{nome}", response_model=List[Tratamento])
async def buscar_tratamento(nome: str):
    tratamentos = await db.tratamentos.find({"nome": {"$regex": nome, "$options": "i"}}).to_list(100)
    
    for trat in tratamentos:
        trat["_id"] = str(trat["_id"])

    return tratamentos



@router.get("/tratamentos-pesquisa-termo")
async def buscar_tratamentos(termo: str):
    """
    Busca tratamentos por texto parcial no nome ou descrição.
    """
    try:
        # Cria um padrão de expressão regular que corresponde a qualquer parte do termo
        regex = {
            "$regex": termo,
            "$options": "i"  # Case-insensitive
        }

        # Busca os tratamentos que correspondem ao padrão em qualquer campo
        tratamentos = await db.tratamentos.find({
            "$or": [
                {"nome": regex},
                {"descricao": regex}
            ]
        }).to_list(None)

        # Converte os ObjectIds para string
        for tratamento in tratamentos:
            tratamento["_id"] = str(tratamento["_id"])

        return tratamentos

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {e}")
    


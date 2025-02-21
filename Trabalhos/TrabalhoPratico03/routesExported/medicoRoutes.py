from fastapi import APIRouter, HTTPException, Query
from database.config import db
from models.schemas import Medico
from typing import List, Optional
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=Medico)
async def criar_medico(medico: Medico):
    medico_dict = medico.dict(by_alias=True, exclude={"id"})  # Remove _id para o Mongo gerar automaticamente
    novo_medico = await db.medicos.insert_one(medico_dict)

    medico_criado = await db.medicos.find_one({"_id": novo_medico.inserted_id})
    if not medico_criado:
        raise HTTPException(status_code=400, detail="Erro ao criar médico")

    medico_criado["_id"] = str(medico_criado["_id"])  # Converte ObjectId para string
    return medico_criado


@router.get("/retornar-medicos/", response_model=List[Medico])
async def listar_medicos(skip: int = 0, limit: int = 10):
    medicos = await db.medicos.find().skip(skip).limit(limit).to_list(100)
    for med in medicos:
        med["_id"] = str(med["_id"])  # Converte ObjectId para string
    return medicos


@router.get("/medicos-filtros")
async def filtrar_medicos(
    nome: Optional[str] = Query(None, description="Nome do médico"),
    especialidade: Optional[str] = Query(None, description="Especialidade do médico"),
    registro: Optional[str] = Query(None, description="Registro do médico")
):
    """
    Filtra médicos por nome, especialidade e registro.
    """
    try:
        filtro = {}

        if nome:
            filtro["nome"] = {"$regex": nome, "$options": "i"}  # Busca case-insensitive
        if especialidade:
            filtro["especialidade"] = {"$regex": especialidade, "$options": "i"}  # Busca case-insensitive
        if registro:
            filtro["registrador"] = {"$regex": registro, "$options": "i"}  # Busca case-insensitive

        medicos = await db.medicos.find(filtro).to_list(None)

        # Converte os ObjectIds para string
        for medico in medicos:
            medico["_id"] = str(medico["_id"])

        return medicos

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {e}")



@router.get("/{medico_id}", response_model=Medico)
async def obter_medico(medico_id: str):
    if not ObjectId.is_valid(medico_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    medico = await db.medicos.find_one({"_id": ObjectId(medico_id)})
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    medico["_id"] = str(medico["_id"])
    return medico


@router.put("/{medico_id}", response_model=Medico)
async def atualizar_medico(medico_id: str, medico: Medico):
    if not ObjectId.is_valid(medico_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    medico_dict = medico.dict(by_alias=True, exclude={"id"})
    resultado = await db.medicos.update_one({"_id": ObjectId(medico_id)}, {"$set": medico_dict})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    medico_atualizado = await db.medicos.find_one({"_id": ObjectId(medico_id)})
    medico_atualizado["_id"] = str(medico_atualizado["_id"])
    return medico_atualizado


@router.delete("/{medico_id}")
async def deletar_medico(medico_id: str):
    if not ObjectId.is_valid(medico_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    resultado = await db.medicos.delete_one({"_id": ObjectId(medico_id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    return {"message": "Médico deletado com sucesso"}


    
# Descrição: Retorna os medicos junto com os detalhes dos tratamentos e a contagem de pacientes.
@router.get("/medicos/detalhes")
async def medicos_com_tratamentos_e_contagem_pacientes():
    pipeline = [
        {
            "$lookup": {
                "from": "tratamentos",
                "localField": "_id",
                "foreignField": "medico_id",
                "as": "tratamentos_info"
            }
        },
        {
            "$unwind": {
                "path": "$tratamentos_info",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$lookup": {
                "from": "pacientes",
                "localField": "tratamentos_info.pacientes",
                "foreignField": "_id",
                "as": "pacientes_info"
            }
        },
        {
            "$addFields": {
                "total_pacientes": {"$size": "$pacientes_info"}
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "nome": {"$first": "$nome"},
                "especialidade": {"$first": "$especialidade"},
                "email": {"$first": "$email"},
                "registrador": {"$first": "$registrador"},
                "tratamentos": {"$push": "$tratamentos_info"},
                "total_pacientes": {"$first": "$total_pacientes"}
            }
        },
        {
            "$project": {
                "_id": 1,
                "nome": 1,
                "especialidade": 1,
                "email": 1,
                "registrador": 1,
                "tratamentos": {
                    "_id": 1,
                    "nome": 1,
                    "descricao": 1,
                    "duracao": 1
                },
                "total_pacientes": 1
            }
        }
    ]

    resultado = await db.medicos.aggregate(pipeline).to_list(100)

    for medico in resultado:
        medico["_id"] = str(medico["_id"])
        for tratamento in medico["tratamentos"]:
            tratamento["_id"] = str(tratamento["_id"])

    return resultado

@router.get("/medicos/detalhes")
async def medicos_com_pacientes_tratamentos_e_consultas():
    pipeline = [
        {
            "$lookup": {
                "from": "pacientes",
                "localField": "_id",
                "foreignField": "medico_id",
                "as": "pacientes_info"
            }
        },
        {
            "$lookup": {
                "from": "tratamentos",
                "localField": "_id",
                "foreignField": "medico_id",
                "as": "tratamentos_info"
            }
        },
        {
            "$lookup": {
                "from": "consultas",
                "localField": "_id",
                "foreignField": "medico_id",
                "as": "consultas_info"
            }
        },
        {
            "$project": {
                "_id": 1,
                "nome": 1,
                "especialidade": 1,
                "email": 1,
                "registrador": 1,
                "pacientes": {
                    "$map": {
                        "input": "$pacientes_info",
                        "as": "paciente",
                        "in": {
                            "_id": "$$paciente._id",
                            "nome": "$$paciente.nome",
                            "email": "$$paciente.email",
                            "idade": "$$paciente.idade"
                        }
                    }
                },
                "tratamentos": {
                    "$map": {
                        "input": "$tratamentos_info",
                        "as": "tratamento",
                        "in": {
                            "_id": "$$tratamento._id",
                            "nome": "$$tratamento.nome",
                            "descricao": "$$tratamento.descricao",
                            "duracao": "$$tratamento.duracao"
                        }
                    }
                },
                "consultas": {
                    "$map": {
                        "input": "$consultas_info",
                        "as": "consulta",
                        "in": {
                            "_id": "$$consulta._id",
                            "paciente_id": "$$consulta.paciente_id",
                            "data": "$$consulta.data"
                        }
                    }
                }
            }
        }
    ]

    resultado = await db.medicos.aggregate(pipeline).to_list(100)

    for medico in resultado:
        medico["_id"] = str(medico["_id"])
        for paciente in medico["pacientes"]:
            paciente["_id"] = str(paciente["_id"])
        for tratamento in medico["tratamentos"]:
            tratamento["_id"] = str(tratamento["_id"])
        for consulta in medico["consultas"]:
            consulta["_id"] = str(consulta["_id"])

    return resultado


from fastapi import APIRouter, HTTPException
from database.config import db
from models.schemas import Paciente
from typing import List, Dict, Any
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=Paciente)
async def criar_paciente(paciente: Paciente):
    """
    Cria um novo paciente no banco de dados.
    """
    # Converte o objeto Pydantic para um dicionário, removendo o campo 'id'
    paciente_dict = paciente.dict(by_alias=True, exclude={"id"})
    
    # Insere o paciente no banco de dados
    novo_paciente = await db.pacientes.insert_one(paciente_dict)
    
    # Recupera o paciente recém-criado
    paciente_criado = await db.pacientes.find_one({"_id": novo_paciente.inserted_id})
    if not paciente_criado:
        raise HTTPException(status_code=400, detail="Erro ao criar paciente")
    
    # Converte o ObjectId para string
    paciente_criado["_id"] = str(paciente_criado["_id"])
    return paciente_criado


@router.get("/", response_model=List[Paciente])
async def listar_pacientes(skip: int = 0, limit: int = 10):
    """
    Lista os pacientes com suporte a paginação.
    """
    pacientes = await db.pacientes.find().skip(skip).limit(limit).to_list(100)
    
    for paciente in pacientes:
        paciente["_id"] = str(paciente["_id"])
        # Converte os IDs dos tratamentos para string, se existirem
        if "tratamentos" in paciente and isinstance(paciente["tratamentos"], list):
            paciente["tratamentos"] = [
                str(tratamento_id) if isinstance(tratamento_id, ObjectId) else tratamento_id
                for tratamento_id in paciente["tratamentos"]
            ]
    
    return pacientes


@router.get("/pacientes/{paciente_id}", response_model=Paciente)
async def buscar_paciente_por_id(paciente_id: str) -> Dict[str, Any]:
    """
    Busca um paciente pelo ID fornecido.
    """
    # Ajusta o filtro para buscar pelo ObjectId ou string
    filtro = {"_id": ObjectId(paciente_id)} if ObjectId.is_valid(paciente_id) else {"_id": paciente_id}
    paciente = await db.pacientes.find_one(filtro)
    
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    paciente["_id"] = str(paciente["_id"])
    
    if "tratamentos" in paciente and isinstance(paciente["tratamentos"], list):
        paciente["tratamentos"] = [
            str(tratamento_id) if isinstance(tratamento_id, ObjectId) else tratamento_id
            for tratamento_id in paciente["tratamentos"]
        ]
    
    return paciente


@router.put("/{paciente_id}", response_model=Paciente)
async def atualizar_paciente(paciente_id: str, paciente: Paciente):
    """
    Atualiza as informações de um paciente pelo ID.
    """
    if not ObjectId.is_valid(paciente_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    # Converte os dados do paciente para um dicionário, removendo o campo 'id'
    paciente_dict = paciente.model_dump(by_alias=True, exclude={"id"})
    resultado = await db.pacientes.update_one({"_id": ObjectId(paciente_id)}, {"$set": paciente_dict})
    
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    paciente_atualizado = await db.pacientes.find_one({"_id": ObjectId(paciente_id)})
    paciente_atualizado["_id"] = str(paciente_atualizado["_id"])
    
    return paciente_atualizado


@router.delete("/{paciente_id}", status_code=200)
async def excluir_paciente(paciente_id: str):
    """
    Exclui um paciente do banco de dados e remove sua referência dos tratamentos em que estava associado.
    """
    if not ObjectId.is_valid(paciente_id):
        raise HTTPException(status_code=400, detail="ID de paciente inválido")
    
    paciente_obj_id = ObjectId(paciente_id)
    paciente = await db.pacientes.find_one({"_id": paciente_obj_id})
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    delete_result = await db.pacientes.delete_one({"_id": paciente_obj_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Erro ao excluir paciente")
    
    # Remove o ID do paciente da lista de pacientes dos tratamentos em que estava associado
    await db.tratamentos.update_many(
        {"pacientes": paciente_obj_id},
        {"$pull": {"pacientes": paciente_obj_id}}
    )
    
    return {"message": "Paciente excluído e removido dos tratamentos com sucesso"}


@router.get("/ordenados")
async def obter_pacientes_ordenados(campo: str = "nome", ordem: int = 1):
    """
    Rota para obter a lista de pacientes ordenada 

    Args:
        campo: ex: "nome", "idade").
        ordem: 1 para crescente, -1 para decrescente).
    """
    try:
        pacientes = db.pacientes  # Coleção de pacientes

        # Converte a ordem para int, caso seja recebida como string
        ordem = int(ordem)

        # Ordena os pacientes
        pacientes_ordenados = await pacientes.find().sort([(campo, ordem)]).to_list(None)

        # Converte os ObjectIds para string
        for paciente in pacientes_ordenados:
            paciente["_id"] = str(paciente["_id"])

        return pacientes_ordenados

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na rota: {str(e)}")
    
    
@router.get("/contagem")
async def obter_contagem_pacientes():
    """
    Rota para obter a quantidade total de pacientes cadastrados.
    """
    try:
        pacientes = db.pacientes  # Coleção de pacientes
        total_pacientes = await pacientes.count_documents({})  # Aguarda o resultado da contagem

        return {"total_pacientes": total_pacientes}  # Retorna o resultado (int)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na rota: {str(e)}")


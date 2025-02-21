from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from pydantic import BaseModel, Field
from typing import List, Optional
from database.config import db
from models.schemas import Paciente
from typing import List, Dict, Any
from bson import ObjectId
from datetime import datetime

# Importação das rotas organizadas em módulos separados
from routesExported import ( medicoRoutes,tratamentoRoutes,pacienteRoutes , sessaoRoutes , setorRoutes)

# Criação da instância principal da aplicação FastAPI
app = FastAPI()

# Inclusão das rotas específicas para cada entidade do sistema acadêmico
app.include_router(medicoRoutes.router, prefix="/medicos", tags=["Médicos"])
app.include_router(tratamentoRoutes.router, prefix="/tratamentos", tags=["Tratamentos"])
app.include_router(pacienteRoutes.router, prefix="/pacientes", tags=["Pacientes"])
app.include_router(sessaoRoutes.router, prefix="/sessoes", tags=["Sessões"])
app.include_router(setorRoutes.router, prefix="/setores", tags=["Setores"])


@app.get("/contagem/pacientes")
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




# Rota raiz da API, apenas para verificar se a aplicação está rodando
@app.get("/")
def home():
    return {"message": "API conectada com FastAPI e MongoDB com sucessor!"}
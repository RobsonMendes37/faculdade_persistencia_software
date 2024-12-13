from datetime import datetime
import hashlib
from http.client import CREATED
import zipfile
from fastapi import APIRouter, FastAPI, HTTPException 
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import csv
import os
from typing import Literal
from app.models.produto import Produto
from app.logs.logger import enviar_log
from app.services.lerDadosCsv import ler_dados_csv
from app.services.escreverDadosCsv import escrever_dados_csv
from app.services.calcularHash import calcular_hash_sha256
from app.services.filtrarElementos import filtrar_entidades


filtros_router = APIRouter()
csv_FILE = "app/database/database.csv"



# GET de Filtrar entidades por tipo
@filtros_router.get("/produtos/tipo/{atributo}", response_model=list[Produto])
def filtrar_produtos(atributo: str):
    try:
        enviar_log(f"Iniciando filtragem de produtos pelo tipo '{atributo}' em '/produtos/tipo/{atributo}'...")  # Log de início

        produtosList = ler_dados_csv()  # Lê os dados do CSV
        tipos_validos = ["limpeza", "beleza", "saude", "comida"]
        campo = "tipo"

        # Verifica se o tipo fornecido é válido
        if atributo.lower() not in tipos_validos:
            enviar_log(f"Erro: Tipo '{atributo}' inválido em '/produtos/tipo/{atributo}'")
            raise HTTPException(status_code=400, detail=f"Tipo '{atributo}' não é válido. Tipos válidos são: {', '.join(tipos_validos)}")

        # Chama a função para filtrar as entidades
        resultado = filtrar_entidades(atributo, campo, produtosList, tipos_validos)

        # Verifica se houve resultados e registra no log
        if resultado:
            enviar_log(f"Filtragem de produtos pelo tipo '{atributo}' realizada com sucesso")
        else:
            enviar_log(f"Nenhum produto encontrado para o tipo '{atributo}' em '/produtos/tipo/{atributo}'")

        return resultado

    except Exception as e:
        # Captura e registra qualquer erro inesperado
        erro_msg = f"Erro ao filtrar produtos em '/produtos/tipo/{atributo}': {str(e)}"
        enviar_log(erro_msg)

        # Lança uma exceção HTTP para retornar um erro interno
        raise HTTPException(status_code=500, detail="Erro interno em /produtos/tipo ao processar a requisição.")
    

# GET de Filtrar entidades por tamanho
@filtros_router.get("/produtos/tamanho/{atributo}", response_model=list[Produto])
def filtrar_produtos(atributo: str):
    try:
        enviar_log(f"Iniciando filtragem de produtos pelo tamanho '{atributo}' em '/produtos/tamanho/{atributo}'...")  # Log de início

        produtosList = ler_dados_csv()  # Lê os dados do CSV
        tamanhos_validos = ['muitoPequeno', 'pequeno', 'medio', 'grande', 'muitoGrande']
        campo = "tamanho"

        # Verifica se o tamanho fornecido é válido
        if atributo.lower() not in [t.lower() for t in tamanhos_validos]:  # Considera maiúsculas e minúsculas
            enviar_log(f"Erro: Tamanho '{atributo}' inválido em '/produtos/tamanho/{atributo}'")
            raise HTTPException(status_code=400, detail=f"Tamanho '{atributo}' não é válido. Tamanhos válidos são: {', '.join(tamanhos_validos)}")

        # Chama a função para filtrar as entidades
        resultado = filtrar_entidades(atributo, campo, produtosList, tamanhos_validos)

        # Verifica se houve resultados e registra no log
        if resultado:
            enviar_log(f"Filtragem de produtos pelo tamanho '{atributo}' realizada com sucesso")
        else:
            enviar_log(f"Nenhum produto encontrado para o tamanho '{atributo}' em '/produtos/tamanho/{atributo}'")

        return resultado

    except Exception as e:
        # Captura e registra qualquer erro inesperado
        erro_msg = f"Erro ao filtrar produtos em '/produtos/tamanho/{atributo}': {str(e)}"
        enviar_log(erro_msg)

        # Lança uma exceção HTTP para retornar um erro interno
        raise HTTPException(status_code=500, detail="Erro interno em /produtos/tamanho ao processar a requisição.")



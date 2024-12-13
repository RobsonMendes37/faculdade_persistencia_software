from http.client import CREATED
from fastapi import APIRouter, HTTPException 
from fastapi.responses import  JSONResponse
import os
from app.logs.logger import enviar_log
from app.services.lerDadosCsv import ler_dados_csv
from app.services.calcularHash import calcular_hash_sha256

indicativos_router = APIRouter()
csv_FILE = "app/database/database.csv"


# GET de Contar QUANTIDADE de elementos
@indicativos_router.get("/produtos/quantidade")
def contar_quantidade():
    try:
        enviar_log("Iniciando contagem de elementos por '/produtos/quantidade'...")  # Registro inicial

        produtos = ler_dados_csv()  # Chama a função que lê os dados do CSV
        quantidade = len(produtos)  # Calcula a quantidade de elementos

        # Sucesso: registra a operação no log
        enviar_log("Contagem de elementos por '/produtos/quantidade' realizada com sucesso")
        return {"quantidade_elemento": quantidade}

    except Exception as e:
        # Se ocorrer qualquer erro, captura e registra no log
        erro_msg = f"Erro ao contar elementos em '/produtos/quantidade': {str(e)}"
        enviar_log(erro_msg)

        # Lança uma exceção HTTP para retornar um erro adequado para o cliente
        raise HTTPException(status_code=500, detail="Erro interno em /produtos/quantidade ao processar a requisição.")







# GET de retornar o hash SHA256 do arquivo CSV
@indicativos_router.get("/produtos/hash")
async def get_hash_sha256():
    try:
        enviar_log("Iniciando cálculo do hash SHA256 do arquivo CSV em '/produtos/hash'...")  # Log de início

        # Caminho para o arquivo CSV
        arquivo_path = "app/database/database.csv"

        # Verifica se o arquivo existe
        if not os.path.exists(arquivo_path):
            enviar_log("Erro: Arquivo CSV não encontrado em '/produtos/hash'")
            raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")

        # Chama a função para calcular o hash
        hash_sha256 = calcular_hash_sha256(arquivo_path)

        # Log de sucesso
        enviar_log(f"Cálculo do hash SHA256 realizado com sucesso em '/produtos/hash'. Hash: {hash_sha256}")

        # Retorna o resultado como um JSON
        return JSONResponse(content={"hash_sha256": hash_sha256})

    except Exception as e:
        # Captura e registra qualquer erro inesperado
        erro_msg = f"Erro ao calcular o hash SHA256 em '/produtos/hash': {str(e)}"
        enviar_log(erro_msg)

        # Lança uma exceção HTTP para retornar um erro interno
        raise HTTPException(status_code=500, detail="Erro interno em /produtos/hash ao processar a requisição.")




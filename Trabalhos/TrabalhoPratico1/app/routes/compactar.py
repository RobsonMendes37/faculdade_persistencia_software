from http.client import CREATED
import zipfile
from fastapi import APIRouter, HTTPException 
from fastapi.responses import FileResponse
import os
from app.logs.logger import enviar_log

compactar_router = APIRouter()
csv_FILE = "app/database/database.csv"

# GET de Compactar o arquivo CSV em um ZIP
@compactar_router.get("/produtos/compactar")
def compactar_csv():
    try:
        enviar_log("Iniciando processo de compactação do arquivo CSV por '/produtos/compactar'...")  # Log de início

        # Verifica se o arquivo CSV existe
        if os.path.exists(csv_FILE):
            # Se o arquivo ZIP já existe, exclui-o
            if os.path.exists("app/database/database.zip"):
                os.remove("app/database/database.zip")
                enviar_log("Arquivo ZIP existente removido com sucesso")

            # Cria um novo arquivo ZIP
            with zipfile.ZipFile("app/database/database.zip", 'w') as zipf:
                zipf.write(csv_FILE, os.path.basename(csv_FILE))
            
            # Log de sucesso
            enviar_log("Compactação do arquivo CSV por '/produtos/compactar' realizada com sucesso")
            
            # Retorna o arquivo ZIP como resposta
            return FileResponse("app/database/database.zip", media_type='application/zip', filename="database.zip")
        else:
            # Log de arquivo não encontrado
            enviar_log("Erro: Arquivo CSV não encontrado em '/produtos/compactar'")
            
            # Lança exceção HTTP para arquivo não encontrado
            raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")

    except Exception as e:
        # Se ocorrer qualquer erro, captura e registra no log
        erro_msg = f"Erro ao compactar arquivo CSV em '/produtos/compactar': {str(e)}"
        enviar_log(erro_msg)

        # Lança uma exceção HTTP para retornar um erro adequado para o cliente
        raise HTTPException(status_code=500, detail="Erro interno em /produtos/compactar ao processar a requisição.")




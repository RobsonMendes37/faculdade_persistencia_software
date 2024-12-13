import hashlib
import os
from fastapi import HTTPException

# Função para calcular o hash SHA256 de um arquivo CSV
def calcular_hash_sha256(arquivo_path: str) -> str:
    try:
        # Verifica se o arquivo existe
        if not os.path.isfile(arquivo_path):
            raise FileNotFoundError(f"Arquivo {arquivo_path} não encontrado.")
        
        # Calculando o hash SHA256
        sha256_hash = hashlib.sha256()
        with open(arquivo_path, "rb") as f:
            # Lê o arquivo em blocos para não sobrecarregar a memória
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from fastapi import HTTPException
from app.models.produto import Produto

#Filtrar entidades por atributo
def filtrar_entidades(atributo:str,campo:str , produtos:list[Produto], valores_validos: list[str]):
    produtos_filtrados = []
    if atributo not in valores_validos:
        raise HTTPException(status_code=400, detail="Tipo inválido")
    else:
        # Itera sobre todos os produtos
        for produto in produtos:
            if getattr(produto, campo) == atributo:
                produtos_filtrados.append(produto)

        # Retorna a lista de produtos filtrados
        return produtos_filtrados


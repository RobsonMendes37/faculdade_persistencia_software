from pydantic import BaseModel
from typing import Literal

class Produto(BaseModel):
    id: int
    nome: str
    tipo: Literal['limpeza', 'beleza', 'saude', 'comida']
    peso: str
    tamanho: Literal['muitoPequeno', 'pequeno', 'medio', 'grande', 'muitoGrande']
    preco: float
    quantidade: int
    fornecedor: str
    marca: str

from pydantic import BaseModel
from typing import List 
from datetime import date

class Paciente(BaseModel):
    id: int
    nome: str
    idade: int
    
class Sintoma(BaseModel):
    id:int
    nome:str
    tratamento:str

class PacienteSintoma(BaseModel):
    paciente_id:int
    sintoma_id:int

class Medico(BaseModel):
    id: int
    nome: str
    idade: int

class Remedio(BaseModel):
    id:int
    nome:str
    data_fabricacao:date
    data_validade:date
    prescricao:str

class Receita(BaseModel):
    medico_id:int
    remedio_id:int
    paciente_id:int


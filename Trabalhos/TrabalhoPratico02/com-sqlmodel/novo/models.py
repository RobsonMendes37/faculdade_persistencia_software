from pydantic import BaseModel
from datetime import date

class Paciente(BaseModel):
    nome: str
    idade: int
    genero: str
    telefone: str
    data_nascimento: str

class Sintoma(BaseModel):
    nome: str
    descricao: str
    tratamento: str
    severidade: str
    duracao_estimada: str

class PacienteSintoma(BaseModel):
    paciente_id: int
    sintoma_id: int
    data_diagnostico: date
    severidade: str
    observacoes: str

class Medico(BaseModel):
    nome: str
    idade: int
    genero: str
    especialidade: str
    telefone: str

class Remedio(BaseModel):
    nome: str
    data_fabricacao: date
    data_validade: date
    prescricao: str
    fabricante: str

class Receita(BaseModel):
    medico_id: int
    remedio_id: int
    paciente_id: int
    data_emissao: date
    validade: date

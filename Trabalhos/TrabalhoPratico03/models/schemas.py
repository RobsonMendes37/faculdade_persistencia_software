from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional



#1:1 (Um para Um): Um médico pode ser a chefia de apenas um setor e um setor tem #apenas um
#  chefe (Modelo Setor - campo chefe_id).

#1:N (Um para Muitos):
# Um médico pode realizar vários tratamentos, mas um tratamento é realizado por apenas um médico (Modelo Tratamento - campo medico_id).
# Um setor pode oferecer vários tratamentos, mas um tratamento é oferecido por apenas um setor (Modelo Setor - campo tratamentos). 
# Uma sessão está associada a um tratamento, mas um tratamento pode ter várias sessões (Modelo Sessão - campo tratamento_id).

#N:N (Muitos para Muitos):
#Um paciente pode realizar vários tratamentos
#e um tratamento pode ser realizado por vários pacientes 
# (Modelo Tratamento - campo pacientes e Modelo Paciente - campo tratamentos). 
# Uma sessão pode ter vários pacientes e um paciente pode participar de várias sessões (Modelo Sessão - campo pacientes).

#1:N (Um para Muitos): 
#Um médico pode ter várias consultas, mas uma #consulta é realizada por apenas um médico (Modelo Consulta - campo medico_id).
#Um paciente pode ter várias consultas, mas uma consulta é realizada por apenas um paciente (Modelo Consulta - campo paciente_id).


# Modelo para um Médico
class Medico(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # ID opcional, compatível com MongoDB
    nome: str  # Nome do médico
    especialidade: str  # Especialidade médica do profissional
    email: str  # Email para contato
    registrador: Optional[str] = None

# Modelo para um Tratamento
class Tratamento(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # ID do tratamento
    nome: str  # Nome do tratamento
    descricao: str  # Descrição detalhada do tratamento
    duracao: int  # Duração total do tratamento (ex: em minutos)
    medico_id: str  # ID do médico responsável pelo tratamento (Relacionamento 1:1)
    pacientes: Optional[List[str]] = []  # Lista de IDs dos pacientes submetidos ao tratamento (Relacionamento 1:N)

# Modelo para um Paciente
class Paciente(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # ID do paciente
    nome: str  # Nome do paciente
    email: str  # Email do paciente
    idade: int  # Idade do paciente
    tratamentos: Optional[List[str]] = []  # Lista de IDs dos tratamentos realizados (Relacionamento N:N)

# Modelo para uma Sessão
class Sessao(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # ID da sessão
    nome: str  # Nome ou identificação da sessão (ex: "Grupo de Reabilitação A")
    tratamento_id: str  # ID do tratamento associado à sessão (Relacionamento 1:N)
    pacientes: List[str]  # Lista de IDs dos pacientes participantes da sessão (Relacionamento N:N)
    endereco: str

# Modelo para um Setor
class Setor(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # ID do setor
    nome: str  # Nome do setor (ex: "Cardiologia", "Oncologia")
    chefe_id: Optional[str]  # ID do médico responsável pelo setor (Relacionamento 1:1)
    tratamentos: List[str]  # Lista de IDs dos tratamentos oferecidos pelo setor (Relacionamento 1:N)
    endereco: str


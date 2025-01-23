from sqlmodel import Field, SQLModel
from datetime import datetime

# Atributos básicos de uma consulta
class ConsultaBase(SQLModel):
    data: datetime  # Data e hora da consulta
    motivo: str  # Motivo da consulta (exemplo: "Dor de cabeça", "Exame de rotina")
    diagnostico: str | None = Field(default=None)  # Diagnóstico da consulta (opcional)

# O modelo Consulta representará a tabela no banco de dados
class Consulta(ConsultaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)  # ID único da consulta
    medico_id: int = Field(foreign_key="medico.id")  # Relacionamento com o médico
    paciente_id: int = Field(foreign_key="paciente.id")  # Relacionamento com o paciente

# O modelo ConsultaPublic é usado para expor as informações públicas da consulta
class ConsultaPublic(ConsultaBase):
    id: int  # Retorna o id da consulta
    medico_id: int
    paciente_id: int 

# O modelo de criação da consulta, usado para o POST
class ConsultaCreate(ConsultaBase):
    medico_id: int  # Id do médico relacionado
    paciente_id: int  # Id do paciente relacionado

# O modelo de atualização da consulta, permitindo atualizar parcialmente os campos
class ConsultaUpdate(ConsultaBase):
    data: datetime | None = None
    motivo: str | None = None
    diagnostico: str | None = None

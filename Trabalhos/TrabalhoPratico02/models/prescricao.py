from sqlmodel import Field, SQLModel
from datetime import date
from typing import Optional
import json

class PrescricaoBase(SQLModel):
    medicamentos: str = Field(..., max_length=500)  # Armazenar como string
    posologia: str = Field(..., max_length=255)  # Como o medicamento deve ser tomado
    data_prescricao: date = Field(default_factory=date.today)  # Data da prescrição
    observacoes: Optional[str] = Field(default=None, max_length=500)  # Observações adicionais

    @property
    def medicamentos_list(self):
        return json.loads(self.medicamentos)  # Converte a string JSON de volta para lista

    @medicamentos_list.setter
    def medicamentos_list(self, value):
        self.medicamentos = json.dumps(value)  # Converte a lista para string JSON

# O modelo Prescricao representa a tabela no banco de dados
class Prescricao(PrescricaoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)  # ID único da prescrição
    consulta_id: int = Field(foreign_key="consulta.id")  # Relacionamento com a consulta

# O modelo PrescricaoPublic é usado para expor as informações públicas da prescrição
class PrescricaoPublic(PrescricaoBase):
    id: int  # Retorna o id da prescrição
    consulta_id: int  # Retorna o id da consulta associada à prescrição

# O modelo PrescricaoCreate é usado para criar uma nova prescrição
class PrescricaoCreate(PrescricaoBase):
    pass

# O modelo PrescricaoUpdate permite que atualizações parciais sejam feitas
class PrescricaoUpdate(PrescricaoBase):
    medicamentos: Optional[str] = None  # Agora é uma string JSON
    posologia: Optional[str] = None
    data_prescricao: Optional[date] = None
    observacoes: Optional[str] = None

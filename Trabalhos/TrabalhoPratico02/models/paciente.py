from sqlmodel import Field, SQLModel

class PacienteBase(SQLModel):
    name: str = Field(index=True)  # Nome do paciente
    age: int | None = Field(default=None, index=True)  # Idade do paciente
    gender: str | None = Field(default=None)  # Gênero do paciente
    email: str | None = Field(default=None, index=True)  # E-mail do paciente
    medical_history: str | None = Field(default=None)  # Histórico médico

# O modelo Paciente representará a tabela no banco de dados
class Paciente(PacienteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)  # ID único do paciente

# O modelo PacientePublic é usado para expor as informações públicas do paciente
class PacientePublic(PacienteBase):
    id: int  # Retorna o id para as respostas, mas não inclui o histórico médico, para segurança

# O modelo PacienteCreate é usado para criar um novo paciente
class PacienteCreate(PacienteBase):
    pass  # Não há necessidade de mudanças aqui, pois já inclui todos os campos necessários

# O modelo PacienteUpdate permite que atualizações parciais sejam feitas, ou seja, nem todos os campos precisam ser fornecidos
class PacienteUpdate(PacienteBase):
    name: str | None = None  # O nome pode ser atualizado, mas não é obrigatório
    age: int | None = None  # Idade também pode ser atualizada
    gender: str | None = None  # Gênero pode ser atualizado
    email: str | None = None  # O e-mail pode ser atualizado
    medical_history: str | None = None  # O histórico médico pode ser atualizado

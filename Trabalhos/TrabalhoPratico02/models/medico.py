from sqlmodel import Field, SQLModel

class MedicoBase(SQLModel):
    name: str = Field(index=True)  # Nome do médico
    age: int | None = Field(default=None, index=True)  # Idade do médico
    gender: str | None = Field(default=None)  # Gênero do médico
    email: str | None = Field(default=None, index=True)  # E-mail do médico
    specialty: str | None = Field(default=None)  # Especialidade médica
    crm: str | None = Field(default=None, index=True)  # CRM (registro do médico)

# O modelo Medico representará a tabela no banco de dados
class Medico(MedicoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)  # ID único do médico

# O modelo MedicoPublic é usado para expor as informações públicas do médico
class MedicoPublic(MedicoBase):
    id: int  # Retorna o id para as respostas, mas não inclui informações sensíveis

# O modelo MedicoCreate é usado para criar um novo médico
class MedicoCreate(MedicoBase):
    pass  # Não há necessidade de mudanças aqui, pois já inclui todos os campos necessários

# O modelo MedicoUpdate permite que atualizações parciais sejam feitas
class MedicoUpdate(MedicoBase):
    name: str | None = None  # O nome pode ser atualizado, mas não é obrigatório
    age: int | None = None  # Idade também pode ser atualizada
    gender: str | None = None  # Gênero pode ser atualizado
    email: str | None = None  # O e-mail pode ser atualizado
    specialty: str | None = None  # A especialidade pode ser atualizada
    crm: str | None = None  # O CRM pode ser atualizado

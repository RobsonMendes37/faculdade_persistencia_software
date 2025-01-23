from sqlmodel import Field, SQLModel

class ResidenteBase(SQLModel):
    name: str = Field(index=True)  # Nome do médico
    age: int | None = Field(default=None, index=True)  # Idade do médico
    gender: str | None = Field(default=None)  # Gênero do médico
    email: str | None = Field(default=None, index=True)  # E-mail do médico
    specialty: str | None = Field(default=None)  # Especialidade médica
    crm: str | None = Field(default=None, index=True)  # CRM (registro do médico)

# O modelo Residente representará a tabela no banco de dados
class Residente(ResidenteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)  # ID único do médico

# O modelo ResidentePublic é usado para expor as informações públicas do médico
class ResidentePublic(ResidenteBase):
    id: int  # Retorna o id para as respostas, mas não inclui informações sensíveis

# O modelo ResidenteCreate é usado para criar um novo médico
class ResidenteCreate(ResidenteBase):
    pass  # Não há necessidade de mudanças aqui, pois já inclui todos os campos necessários

# O modelo ResidenteUpdate permite que atualizações parciais sejam feitas
class ResidenteUpdate(ResidenteBase):
    name: str | None = None  # O nome pode ser atualizado, mas não é obrigatório
    age: int | None = None  # Idade também pode ser atualizada
    gender: str | None = None  # Gênero pode ser atualizado
    email: str | None = None  # O e-mail pode ser atualizado
    specialty: str | None = None  # A especialidade pode ser atualizada
    crm: str | None = None  # O CRM pode ser atualizado

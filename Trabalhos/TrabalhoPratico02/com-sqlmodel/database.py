from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os

# Carregar as variáveis do .env
load_dotenv()

# Recuperar a URL do banco de dados do .env
database_url = os.getenv("DATABASE_URL", "sqlite:///default.db")

# Configurar o banco
connect_args = {"check_same_thread": False} if "sqlite" in database_url else {}
engine = create_engine(database_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env, se presente
load_dotenv()

# Obtém a URI do MongoDB a partir das variáveis de ambiente
#MONGO_URI = os.getenv("MONGO_URI")
MONGO_URI = os.getenv("mongodb://localhost:27017")
MONGO_DATABASE = os.getenv("DATABASE_NAME")

# Criação de um cliente assíncrono para o MongoDB
client = AsyncIOMotorClient(MONGO_URI)

# Definição do banco de dados que será utilizado no projeto
db = client[MONGO_DATABASE]
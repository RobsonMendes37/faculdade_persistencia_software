#pra rodar-> 
#            uvicorn main:app --reload

from fastapi import FastAPI
from app.routes.crud import crud_router
from app.routes.indicativos import indicativos_router
from app.routes.compactar import compactar_router
from app.routes.filtros import filtros_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173", 
    "http://127.0.0.1:5174",
    "http://localhost:5174",
    "http://127.0.0.1:5175",
    "http://localhost:5175",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir essas origens
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

# get quantiadade "/produtos/quantidade"
# get hash "/produtos/hash"
app.include_router(indicativos_router) #cuidado, pois a ordem importa em chamar as rotas!

# get tipo "/produtos/tipo/{atributo}"
# get tamanho "/produtos/tipo/{atributo}"
app.include_router(filtros_router)

#compactar "/produtos/compactar"
app.include_router(compactar_router)

# get "/produtos"
# get id "/produtos/{id}"
# put "/produtos/{id}"
# delete "/produtos/{id}"
app.include_router(crud_router)



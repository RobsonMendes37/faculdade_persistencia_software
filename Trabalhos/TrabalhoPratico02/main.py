from fastapi import FastAPI
from db.database import create_db_and_tables
from routes.hero import router as hero_router
from routes.paciente import router as paciente_router
from routes.medico import router as medico_router
from routes.consulta import router as consulta_router
from routes.enfermeiro import router as enfermeiro_router
from routes.residente import router as residente_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(hero_router, prefix="/heroes", tags=["Heroes"])

app.include_router(paciente_router, prefix="/pacientes", tags=["Pacientes"])

app.include_router(medico_router, prefix="/medicos", tags=["Medicos"])

app.include_router(enfermeiro_router, prefix="/enfermeiros", tags=["Enfermeiro"])

app.include_router(residente_router, prefix="/residentes", tags=["Residente"])

app.include_router(consulta_router, prefix="/consultas", tags=["Consultas"])

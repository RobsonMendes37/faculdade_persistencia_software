from fastapi import FastAPI
from db.database import create_db_and_tables
from routes.hero import router as hero_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(hero_router, prefix="/heroes", tags=["Heroes"])

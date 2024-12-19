from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///./escola1/db"

engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})

Base.metadata.create_all(bing=engine)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bing=engine)

def get_db():   
    db= SessionLocal
    try:
        yield db
    finally:
        db.close()
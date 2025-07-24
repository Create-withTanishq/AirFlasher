from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

AIR_FLASHER_DATABASE_URL = "sqlite:///./backend/data/AirFlasher.db"

engine = create_engine(url = AIR_FLASHER_DATABASE_URL ,connect_args= {"check_same_thread" : False})

SessionLocal = sessionmaker(bind = engine, autoflush= False ,autocommit = False)

Base = declarative_base()

#to convert to session format
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

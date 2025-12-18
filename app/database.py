from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# TEMP: hardcode database url to confirm DB works
DATABASE_URL = "postgresql://postgres:YOUR_PASSWORD@localhost/crm_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

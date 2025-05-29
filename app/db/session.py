from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os

# This should point to the central DB for the main application
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL 

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base for declarative models (already in central_models.py, but good to be aware)
# from app.models.central_models import Base

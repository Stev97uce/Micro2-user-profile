from databases import Database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL.replace("+asyncpg", ""), pool_pre_ping=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



URL = "sqlite:///./todos.db"
engine = create_engine(URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autoflush=False, autocommit= False, bind=engine)
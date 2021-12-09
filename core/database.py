import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from app.services.service import Service

SQLALCHEMY_DATABASE_URL = Service.get_database_url()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
database = databases.Database(SQLALCHEMY_DATABASE_URL)

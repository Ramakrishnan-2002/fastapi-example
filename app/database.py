from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine #engine is must to connect to db 
from sqlalchemy.orm import sessionmaker,Session
from .config import settings

from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL =f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}' 
engine=create_engine(SQLALCHEMY_DATABASE_URL) #engine is to map db and args define how the connection should work
                                                                                        #sqlachemy defaultly allows multiple threads but not same thread to communicate to db but for safety we are passing that as our args
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base() #Which is the object of db, so when we have to call db we will call this class

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]
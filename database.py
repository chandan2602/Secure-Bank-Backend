from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

sessionloacal = sessionmaker(
    autoflush = False,
    autocommit = False,
    bind = engine 
    )


# after every session we need to close the session 
def get_db():
    db = sessionloacal()
    try:
        yield db
    finally:
        db.close()
        
# Declarative base is the main important funcion from which all the sqlachemy model inherit
Base = declarative_base()


# Execute SELECT query
def execute_query(query: str):

    db = sessionloacal()

    try:

        result = db.execute(
            text(query)
        )

        rows = result.mappings().all()

        return [dict(row) for row in rows]

    finally:

        db.close()
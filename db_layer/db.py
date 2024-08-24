from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from dotenv import load_dotenv  # pip install python-dotenv
import os
load_dotenv()
DB_CONN_STR = os.getenv('DB_PROD_CONN_STR')

engine = create_engine(DB_CONN_STR)

# Create a sessionmaker factory
Session = sessionmaker(bind=engine)
Base = declarative_base()

@contextmanager
def get_db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

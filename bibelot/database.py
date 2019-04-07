import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db_url import db_url


print('db initiated')
engine = create_engine(db_url, convert_unicode=True, pool_size=5, max_overflow=10, poolclass=QueuePool)
Base = declarative_base()
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = db_session.query_property()

@contextmanager
def session_scope():
  try:
    session = db_session
    yield session
    session.commit()
  except:
    session.rollback()
    raise
  finally:
    session.close()

def init_db():
    from models import Upload
    Base.metadata.create_all(bind=engine)
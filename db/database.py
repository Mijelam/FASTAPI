import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import declarative_base
#from sqlalchemy.ext.declarative import declarative_base

sqlitename = '../movies.sqlite'
base_dir = os.path.dirname(os.path.realpath(__file__))
databaseUrl = f'sqlite:///{os.path.join(base_dir, sqlitename)}'

engine = create_engine(databaseUrl, echo=True)
Session = sessionmaker(bind=engine,autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
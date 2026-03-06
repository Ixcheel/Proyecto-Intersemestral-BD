from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = None
SessionFactory = None

def init_db(database_url: str):
    global engine, SessionFactory
    engine = create_engine(database_url, pool_pre_ping=True)
    SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
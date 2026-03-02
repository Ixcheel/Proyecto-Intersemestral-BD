from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()
migrate = Migrate()
engine = None
SessionFactory = None

def init_db(database_url: str):
    global engine, SessionFactory
    engine = create_engine(database_url, pool_pre_ping=True)
    SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
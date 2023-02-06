from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from core.configs import settings


engine: Engine = create_engine(settings.DB_URL)


Session = sessionmaker(bind=engine)

session = Session()

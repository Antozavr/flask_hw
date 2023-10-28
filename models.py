import os
import atexit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func

PG_USER = os.getenv("PG_USER", "app")
PG_PASSWORD = os.getenv("PG_PASSWORD", "1234")
PG_DB = os.getenv("PG_DB", "app")
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", 5431)

PG_DNS = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'

engine = create_engine(PG_DNS)
atexit.register(engine.dispose)

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class Announcement(Base):
    __tablename__ = 'app_ad'

    id = Column(Integer, primary_key=True)
    header = Column(String, nullable=False)
    description = Column(String)
    creation_date = Column(DateTime, server_default=func.now())
    owner = Column(String)


Base.metadata.create_all()

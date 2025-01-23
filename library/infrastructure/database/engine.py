import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from library.models import metadata

print(os.getenv("DATABASE_URL"))

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for SQLAlchemy engine")

metadata = MetaData()

# Create the SQLAlchemy engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,         # Number of connections to keep in the pool
    max_overflow=20,      # Number of connections allowed in overflow
    pool_timeout=30,      # Time to wait before giving up on getting a connection from the pool
    pool_recycle=1800     # Recycle connections after this many seconds
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Create a new Session
def get_session():
    return SessionLocal()

# Create all tables in the metadata
metadata.create_all(engine)


def get_engine():
    return engine

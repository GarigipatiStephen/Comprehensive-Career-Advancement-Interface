
from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///career.db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# **********  User Table **********

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))


# ********** Resume Table **********

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    content = Column(Text)
    predicted_domain = Column(String(100))


# ********** Job Table **********

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    location = Column(String(100))
    salary = Column(String(50))
    similarity_score = Column(Float)


def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    return SessionLocal()

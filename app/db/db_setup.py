from sqlalchemy import create_engine, insert, String, Column, Integer, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///expenses.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Expense(Base):
    __tablename__ = "expenses"
    username = Column (String)
    transaction_ID = Column(Integer, primary_key=True)
    purchase = Column(String)
    cost = Column(Float)
    category = Column(String)
    timestamp = Column(DateTime)

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

def createSession():
    session = SessionLocal()
    try:
        yield session
    finally: 
        session.close()
# app/models/person.py
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.core.config import Base

class Person(Base):
    __tablename__ = "person"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True)
    dob = Column(Date)
    address = Column(String)
    job_title = Column(String)
    employer = Column(String)
    employment_start_date = Column(Date)

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

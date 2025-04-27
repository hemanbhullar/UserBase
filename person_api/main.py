from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware


# Database URL for PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/person_db"

# Set up the database engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for models
Base = declarative_base()

# Define the Person table model
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

# Create the FastAPI app
app = FastAPI()

# Pydantic model for request body validation
class PersonCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    dob: str
    address: str
    job_title: str
    employer: str

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoint to add a person
@app.post("/person/")
def create_person(person: PersonCreate, db: SessionLocal = Depends(get_db)):
    db_person = Person(
        first_name=person.first_name,
        last_name=person.last_name,
        email=person.email,
        phone_number=person.phone_number,
        dob=person.dob,
        address=person.address,
        job_title=person.job_title,
        employer=person.employer
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

# API endpoint to get a person by email
@app.get("/person/{email}")
def get_person(email: str, db: SessionLocal = Depends(get_db)):
    person = db.query(Person).filter(Person.email == email).first()
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

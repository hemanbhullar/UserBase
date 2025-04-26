# app/schemas/person.py
from pydantic import BaseModel
from datetime import date

class PersonBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    dob: date
    address: str
    job_title: str
    employer: str
    employment_start_date: date | None = None  # Optional field

class PersonCreate(PersonBase):
    pass

class PersonOut(PersonBase):
    id: int
    
    class Config:
        orm_mode = True  # Tells Pydantic to work with SQLAlchemy models

class UserCreate(BaseModel):
    username: str
    email: str
    password: str  # This will be the plain text password

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str  # This will be the plain text password

# app/crud/person.py
from sqlalchemy.orm import Session
from app.models.person import Person
from app.schemas.person import PersonCreate

# Create a person in the database
def create_person(db: Session, person: PersonCreate):
    db_person = Person(
        first_name=person.first_name,
        last_name=person.last_name,
        email=person.email,
        phone_number=person.phone_number,
        dob=person.dob,
        address=person.address,
        job_title=person.job_title,
        employer=person.employer,
        employment_start_date=person.employment_start_date
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

# Get a person by email
def get_person_by_email(db: Session, email: str):
    return db.query(Person).filter(Person.email == email).first()

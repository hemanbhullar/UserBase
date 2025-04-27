from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.crud import person as crud
from app.schemas.person import PersonCreate, PersonOut
from app.schemas.person import UserCreate, UserOut, UserLogin
from app.core.auth import hash_password, verify_password, create_access_token, verify_access_token
from app.core.config import SessionLocal
from app.models.person import User
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL (adjust port if needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
# HTTPBearer will be used to extract the token from the Authorization header
security = HTTPBearer()


# Dependency to get the current user from the JWT token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # This is the JWT token passed in the Authorization header
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload

# Dependency to get the current user role from the JWT token
def get_current_user_role(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # Extract token from the Authorization header
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload["role"]

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoint to add a person
@app.post("/person/", response_model=PersonOut)
def create_person(person: PersonCreate, db: Session = Depends(get_db)):
    db_person = crud.create_person(db=db, person=person)
    return db_person

# API endpoint to get a person by email (now requires authentication)
@app.get("/person/{email}", response_model=PersonOut)
def get_person(email: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_person = crud.get_person_by_email(db=db, email=email)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

# Register endpoint (creates a new user)
@app.post("/register/", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password and create user
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, password_hash=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Login endpoint to authenticate a user and return a JWT token
@app.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user is None or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create JWT token
    access_token = create_access_token(data={"sub": db_user.username, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# Protect routes based on roles
@app.get("/admin/")
def admin_only(current_role: str = Depends(get_current_user_role)):
    if current_role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    return {"message": "Welcome, Admin!"}


@app.post("/refresh/")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    # Verify the refresh token and get the user data
    payload = verify_access_token(refresh_token)
    if not payload or 'sub' not in payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    username = payload["sub"]
    db_user = db.query(User).filter(User.username == username).first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create a new access token and return it
    new_access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": new_access_token, "token_type": "bearer"}

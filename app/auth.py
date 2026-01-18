from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from dotenv import load_dotenv
import os

from app.database import get_db
from app import models, schemas

load_dotenv()

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is missing! Set it in your .env file.")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        org = models.Organization(name=user.organization_name)
        db.add(org)
        db.commit()
        db.refresh(org)

        new_user = models.User(
            email=user.email,
            hashed_password=hash_password(user.password),
            role="owner",
            organization_id=org.id
        )
        db.add(new_user)
        db.commit()

        return {"message": "User registered successfully"}

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization name already exists"
        )

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": db_user.id,
        "organization_id": db_user.organization_id,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

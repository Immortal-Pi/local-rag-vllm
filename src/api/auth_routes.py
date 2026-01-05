from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from src.db import SessionLocal, User
from src.auth.security import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterReq(BaseModel):
    email: EmailStr
    password: str


class LoginReq(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
def register(req: RegisterReq):
    db: Session = SessionLocal()
    if db.get(User, req.email):
        raise HTTPException(400, "User exists")

    user = User(
        email=req.email,
        password_hash=hash_password(req.password),
    )
    db.add(user)
    db.commit()
    return {"status": "ok"}


@router.post("/login")
def login(req: LoginReq):
    db: Session = SessionLocal()
    user = db.get(User, req.email)
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    token = create_token(user.email)
    return {"access_token": token, "token_type": "bearer"}

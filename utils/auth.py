from fastapi import HTTPException, Request, Depends

from typing import Optional
from jwt import PyJWTError
from database import SessionLocal
import jwt
from datetime import datetime, timedelta
from models.user import  User

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

# Funzione per autenticare l'utente
def authenticate_user(username: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username and User.password == password).first()
    db.close()
    if user:
        return user
    return None

# Funzione per generare il token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def check_token(request: Request) -> Optional[str]:
    token = request.cookies.get('access_token')
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    

async def check_is_admin(request: Request) -> Optional[str]:
    try:
        token = request.cookies.get('access_token')
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_role: str = payload.get("role")
        if user_role == "admin":
            return True
        raise HTTPException(status_code=403, detail="Only admin can perform this action")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
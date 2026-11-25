from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from app.core.config import settings
import jwt

hash_password=PasswordHash.recommended()

def password_hash(password:str) -> str:
    return hash_password.hash(password)

def password_verify(password:str, verify_pass:str) -> bool:
    return hash_password.verify(password,verify_pass)

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
import os 
import jwt 

from datetime import datetime,timedelta,timezone 
from dotenv import load_dotenv 
from pwdlib import PasswordHash 
from uuid import uuid4

load_dotenv() 
SECRET_KEY=os.getenv("SECRET_KEY") 
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MIMUTES=30 
REFRESH_TOKEN_EXPIRE_DAYS = 7

password_hash=PasswordHash.recommended() 

def hash_password(password:str) -> str :
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password) 

def create_access_token(user_id:str, session_id:str) -> str :
    expire=datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MIMUTES
    )

    payload={
        "sub":user_id,
        "exp":expire,
        "type":"access",
        "jti":str(uuid4()),
        "sid":session_id
    }
    token=jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token 

def decode_access_token(token:str)->dict:
    payload=jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
    if payload.get("type") != "access":
        raise ValueError("Invalid token type")
    return payload

def create_refresh_token(user_id:str,session_id:str) -> str:
    expire=datetime.now(timezone.utc)+timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS 
    )
    payload={
        "sub":user_id,
        "exp":expire,
        "type":"refresh",
        "jti":str(uuid4()),
        "sid":session_id
    }
    token=jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token


def decode_refresh_token(token:str) -> dict:
    payload=jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    if payload.get("type") != "refresh":
        raise ValueError("Invalid token type")

    return payload

def create_email_verification_token(user_id:str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15) 

    payload={
        "sub":user_id,
        "exp":expire, 
        "type":"email_verification",
        "jti":str(uuid4())
    }
    token=jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    ) 

    return token 

def decode_email_verification_token(token:str) -> dict:
    payload=jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    if payload.get("type") != "email_verification":
        raise ValueError("Invalid email verification token") 

    return payload 

def create_password_reset_token(user_id:str) ->str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15) 

    payload={
        "sub":user_id,
        "exp":expire,
        "type":"password_reset",
        "jti":str(uuid4())
    }
    token=jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    ) 
    return token 

def decode_password_reset_token(token:str) -> dict:
    payload=jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
    if payload.get("type") != "password_reset":
        raise ValueError("Inavlid password reset token")
    return payload 


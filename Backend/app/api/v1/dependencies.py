from fastapi import Depends,HTTPException,status 
from fastapi.security import OAuth2PasswordBearer 
from app.core.security import decode_access_token 
from app.repositories.user_repository import get_user_by_id
from app.repositories.token_repository import (
    revoke_token,
    is_token_revoked
)
from app.repositories.session_repository import create_session,get_session

oauth2_scheme= OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login" 
)

async def get_current_user(token:str = Depends(oauth2_scheme)):
    try:
        payload=decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
            header={"WWW-Authenticate":"Bearer"}
        )

    user_id=payload.get("sub") 
    token_id=payload.get("jti") 
    session_id=payload.get("sid") 

    if not user_id or not token_id or not session_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload",
            headers={"WWW-Authenticate":"Bearer"}
        )

    if is_token_revoked(token_id):
        raise HTTPException(
            status_code=401,
            detail="Session is invalid or revoke",
            headers={"WWW-Authenticate":"Bearer"}
        )

    user= await get_user_by_id(user_id) 
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate":"Bearer"}
        )
    return user

    
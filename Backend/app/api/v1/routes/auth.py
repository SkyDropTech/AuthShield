from fastapi import APIRouter, HTTPException, Depends,status
from app.services.auth_service import register_user,login_user,forgot_password,reset_password
from app.core.security import (
    create_refresh_token,
    create_access_token,
    decode_access_token,
    decode_refresh_token,
    create_email_verification_token,
    decode_email_verification_token,
    create_password_reset_token,
    decode_password_reset_token
    )
from app.repositories.user_repository import get_user_by_id,verify_user_email
from app.repositories.token_repository import revoke_token,is_token_revoked
from app.schemas.auth import RefreshTokenRequest,ForgotPasswordRequest,ResetPasswordRequest
from app.repositories.session_repository import (
    revoke_session,
    get_session,
    set_refresh_token_id,
    was_refresh_token_used
    )
from app.api.v1.dependencies import (
    get_current_user,
    oauth2_scheme
    )
from app.schemas.auth import RefreshTokenRequest 

router = APIRouter() 

@router.get("/")
async def auth_status():
    return {
        "message": "The auth is working perfectly"
    }

@router.post("/register")
async def register(data:dict):
    try:
        user=await register_user(data) 
        return user 
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error) 
        )

@router.post("/login") 
async def login(data:dict):
    try:
        user=await login_user(
            data["email"],
            data["password"]
            )
    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )
    return user

@router.post("/refresh")
async def refresh_access_token(data:RefreshTokenRequest):
    try:
        payload= decode_refresh_token(data.refresh_token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )

    user_id=payload.get("sub") 
    session_id=payload.get("sid") 
    token_id= payload.get("jti") 

    if not user_id or not session_id or not token_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload"
        )    
    session=get_session(session_id)

    if session is None or session["revoked"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is invalid or revoked"
        )
    if was_refresh_token_used(session_id,token_id):
        revoke_session(session_id) 

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token reuse detected. Session revoked;please log in again"
        )
    
    
    if session["refresh_token_id"] != token_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        ) 
    user=await get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found"
    )
    new_access_token=create_access_token(
        user_id=str(user_id),
        session_id=session_id
    )
    new_refresh_token=create_refresh_token(
        user_id=str(user_id),
        session_id=session_id
    )

    new_refresh_payload=decode_refresh_token(new_refresh_token)
    new_refresh_token_id=new_refresh_payload["jti"]

    set_refresh_token_id(
        session_id=session_id,
        token_id=new_refresh_token_id
    )

    return {
        "access_token":new_access_token,
        "refresh_token":new_refresh_token,
        "token_type":"bearer"
    }

@router.post("/logout")
async def logout(
    token:str = Depends(oauth2_scheme),
    current_user:dict = Depends(get_current_user)):

    payload=decode_access_token(token) 
    token_id=payload.get("jti") 
    session_id=payload["sid"] 

    revoke_token(token_id)
    revoke_session(session_id)

    return {
        "message":"Successfully logged out"
    }

@router.post("/verify-email")
async def verify_email(data:RefreshTokenRequest):
    try:
        payload=decode_email_verification_token(data.refresh_token) 

        user_id=payload.get("sub") 

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detial="Invalid verification token"
            )

        user= await verify_user_email(user_id) 

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return {
            "message":"Email verified succesfully",
            "is_email_verified":user["is_email_verified"]
        }

    except HTTPException:
        raise 
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired verification token"
        )

@router.post("/forgot-password")
async def forgot_password_route(data: ForgotPasswordRequest):
    try:
        return await forgot_password(data.email)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.post("/reset-password")
async def reset_password_route(data: ResetPasswordRequest):
    try:
        return await reset_password(
            token=data.token,
            new_password=data.new_password
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
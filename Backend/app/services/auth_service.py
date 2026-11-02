from uuid import uuid4

from app.repositories.user_repository import (
    get_user_by_email,
    create_user,
    get_user_by_id
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    create_email_verification_token,
    create_password_reset_token,
    decode_password_reset_token
    ) 
from app.repositories.session_repository import (
    create_session,
    set_refresh_token_id
    )

async def register_user(user_data:dict):
    existing= await get_user_by_email(user_data["email"]) 
    if existing is not None:
        raise ValueError("Email already registered")

    hashed_password = hash_password(user_data["password"]) 

    new_user_data={
        "username":user_data["username"],
        "email":user_data["email"],
        "hashed_password":hashed_password
    }

    new_user= await create_user(new_user_data)

    verification_token=create_email_verification_token(
        str(new_user["id"])
    )

    return {
        "id":new_user["id"],
        "username":new_user["username"],
        "email":new_user["email"],
        "verification_token":verification_token

    }

async def login_user(email: str, password: str):
    user = await get_user_by_email(email)

    if user is None:
        raise ValueError("Invalid email or password")

    password_is_correct = verify_password(
        password,
        user["hashed_password"]
    )

    if not password_is_correct:
        raise ValueError("Invalid email or password")

    if not user["is_email_verified"]:
        raise ValueError("Please verify your email before logging in")

    session_id = str(uuid4())

    create_session(
        session_id=session_id,
        user_id=str(user["id"])
    )

    access_token = create_access_token(
        user_id=str(user["id"]),
        session_id=session_id
    )

    refresh_token = create_refresh_token(
        user_id=str(user["id"]),
        session_id=session_id
    )

    refresh_payload= decode_refresh_token(refresh_token)
    refresh_token_id = refresh_payload["jti"]

    set_refresh_token_id(
        session_id=session_id,
        token_id=refresh_token_id
    )

    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

async def forgot_password(email:str):
    user= await get_user_by_email(email) 

    if user is None:
        raise ValueError("User not Found") 

    token = create_password_reset_token(str(user["id"])) 

    return {
        "message":"password reset token generated",
        "reset_token":token
    }

async def reset_password(token:str , new_password:str) :
    try:
        payload= decode_password_reset_token(token) 

    except Exception:
        raise ValueError("Invalid or expired password reset token") 

    user_id = payload.get("sub")

    if not user_id:
        raise ValueError("Invalid password reset token")

    user = await get_user_by_id(user_id) 

    if user is None:
        raise ValueError("User Not found") 
    user["hashed_password"] = hash_password(new_password )

    return {
        "message":"Password has reset successfully"
    }
from fastapi import APIRouter, HTTPException,Depends
from app.api.v1.dependencies import get_current_user 

router = APIRouter() 

@router.get("/me")
async def get_my_profile(current_user:dict = Depends(get_current_user)):
    return {
        "id":current_user["id"],
        "username":current_user["username"],
        "email":current_user["email"]
    }

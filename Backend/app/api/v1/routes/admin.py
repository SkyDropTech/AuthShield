from fastapi import APIRouter, HTTPException

router = APIRouter() 

@router.get("/")
async def admin_status():
    return {
            "message": "The admin is working perfectly"
        }

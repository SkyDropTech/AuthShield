from fastapi import APIRouter 
from app.api.v1.routes import admin,auth,users

api_router=APIRouter() 

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)
api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"]
)
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)







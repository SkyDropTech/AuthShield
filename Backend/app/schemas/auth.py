from pydantic import BaseModel,Field ,EmailStr

class UserCreate(BaseModel):
    username:str
    email: EmailStr 
    password:str=Field(min_length=8,max_length=20)

class UserResponse(BaseModel):
    id:str 
    username:str 
    email:EmailStr 

class RefreshTokenRequest(BaseModel):
    refresh_token:str 

class ForgotPasswordRequest(BaseModel):
    email:EmailStr 

class ResetPasswordRequest(BaseModel):
    token:str
    new_password:str = Field(min_length=8)
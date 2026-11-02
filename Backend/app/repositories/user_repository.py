import uuid

users = {}

async def get_user_by_email(email:str):
    for user in users.values():
        if user["email"]==email:
            return user
    return None 

async def get_user_by_id(user_id:str):
    for user in users.values():
        if user["id"]==user_id:
            return user
    return None

async def create_user(user_data: dict):
    user_id = str(uuid.uuid4()) 
    new_user={
        "id": user_id,
        "username":user_data["username"],
        "email":user_data["email"],
        "hashed_password":user_data["hashed_password"],
        "is_email_verified":False
    }
    users[user_id]=new_user 
    return new_user

async def verify_user_email(user_id:str):
    user=users.get(user_id) 
    if user is None:
        return None 

    user["is_email_verified"]= True 
    return user 
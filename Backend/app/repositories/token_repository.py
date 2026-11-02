revoked_token=set() 

def revoke_token(token_id:str)-> None:
    revoked_token.add(token_id) 

def is_token_revoked(token_id:str) -> bool:
    return token_id in revoked_token 
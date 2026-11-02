sessions={} 

def create_session(session_id:str, user_id:str):
    sessions[session_id]={
        "user_id":user_id,
        "revoked":False ,
        "refresh_token_id":None,
        "refresh_token_history":[]
    }

def get_session(session_id:str):
    return sessions.get(session_id) 

def revoke_session(session_id:str):
    session=sessions.get(session_id)

    if session:
        session["revoked"]=True 

def set_refresh_token_id(session_id:str,token_id:str):
    session=sessions.get(session_id)

    if session:
        old_token_id=session["refresh_token_id"] 

    if old_token_id is not None:
        session["refresh_token_history"].append(old_token_id)

    session["refresh_token_id"]=token_id    

def was_refresh_token_used(session_id:str, token_id:str)->bool:
    session=sessions.get(session_id) 
    if session is None:
        return False 
    return token_id in session["refresh_token_history"] 



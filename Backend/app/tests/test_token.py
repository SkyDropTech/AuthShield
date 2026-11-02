from app.core.security import create_access_token,decode_access_token 

token=create_access_token("user_123")

print("Generated token:", token)

payload=decode_access_token(token) 

print("User ID:", payload["sub"])
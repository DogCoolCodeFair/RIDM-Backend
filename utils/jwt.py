from fastapi import Depends, HTTPException
import jwt
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from os import getenv
load_dotenv()

async def generate_token(id: str):
    return jwt.encode({"id": id}, getenv("JWT_SECRET"), algorithm="HS256")

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    try:
        return (jwt.decode(token, getenv("JWT_SECRET"), algorithms=["HS256"])).get("id")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
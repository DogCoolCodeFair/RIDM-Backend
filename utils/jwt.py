from datetime import datetime
from os import getenv

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import utils.database as db

load_dotenv()


async def generate_token(id: str):
    return jwt.encode(
        {"id": id, "createdAt": datetime.now().timestamp()},
        getenv("JWT_SECRET"),
        algorithm="HS256",
    )


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    token = credentials.credentials
    try:
        return (jwt.decode(token, getenv("JWT_SECRET"), algorithms=["HS256"])).get("id")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


async def verify_doctor(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    token = credentials.credentials
    try:
        id = (jwt.decode(token, getenv("JWT_SECRET"), algorithms=["HS256"])).get("id")
        if (await db.find_one("users", "id", id)).get("isDoctor"):
            return id
        else:
            raise HTTPException(
                status_code=403, detail="Should be Doctor to access this endpoint"
            )
    except jwt.exceptions.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

from hashlib import sha256

from fastapi import APIRouter, Form, HTTPException

import utils.database as db
from models import LoginResponse
from utils.jwt import generate_token

auth_router = APIRouter()


@auth_router.post(
    "/login", response_model=LoginResponse, description="ID/PW로 로그인해 엑세스 토큰을 발행받습니다."
)
async def login(id: str = Form(...), password: str = Form(...)):
    authdata = await db.find_one("auth", "id", id)
    if authdata:
        if sha256(password.encode()).hexdigest() == authdata["hash"]:
            return LoginResponse(access_token=await generate_token(id))
        else:
            raise HTTPException(status_code=401, detail="Invalid password")
    else:
        raise HTTPException(401, "ID Not Found")

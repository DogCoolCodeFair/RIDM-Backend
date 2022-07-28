from hashlib import sha256
from typing import List

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from models.disease import Disease

import utils.database as db
from models import LoginResponse
from utils.jwt import generate_token, verify_doctor

disease_router = APIRouter()

@disease_router.get("/listall", response_model=List[Disease], description="DB에 저장된 전체 질환 목록을 반환합니다.")
async def listall():
    documents = await db.get_all_documents("diseases")
    return [Disease.parse_obj(document) for document in documents]
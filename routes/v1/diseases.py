from typing import List

from fastapi import APIRouter, Depends, HTTPException

import utils.database as db
from models.disease import Disease
from models.user import Patient
from utils.jwt import verify_doctor

disease_router = APIRouter()


@disease_router.get(
    "/listall", response_model=List[Disease], description="DB에 저장된 전체 질환 목록을 반환합니다."
)
async def listall():
    documents = await db.get_all_documents("diseases")
    return [Disease.parse_obj(document) for document in documents]


@disease_router.post(
    "/{user}/insert_disease",
    response_model=Patient,
    description="{user}에게 질환정보를 추가합니다. (의사만 접근 가능)",
)
async def insert_disease(
    disease: Disease, user: str, requester: str = Depends(verify_doctor)
):
    user: Patient = await db.get_user(user)
    if user.isDoctor:
        raise HTTPException(status_code=400, detail="Should be Patient to add disease")
    user.diseases.append(disease)
    return await db.update_one("users", "id", user.id, user.dict())

from hashlib import sha256

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request

import utils.database as db
from models.symptom import Symptom
from models.user import Patient
from utils.jwt import generate_token, verify_doctor, verify_token

symptom_router = APIRouter()


@symptom_router.post("/{user}/insert_symptom", response_model=Patient, description="{user}에게 증상정보를 추가합니다. (의사만 접근 가능)")
async def insert_symptom(
    symptom: Symptom, user: str, requester: str = Depends(verify_doctor)
):
    user: Patient = await db.get_user(user)
    if user.isDoctor:
        raise HTTPException(
            status_code=500, detail="Should be Patient to add symptom"
        )
    user.symptoms.append(symptom)
    return await db.update_one("users", "id", user.id, user.dict())


from hashlib import sha256

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request

import utils.database as db
from models import LoginResponse
from models.symptom import Symptom
from models.user import Patient
from utils.jwt import generate_token, verify_doctor, verify_token

symptom_router = APIRouter()


@symptom_router.post("/{user}/insert_symptom", response_model=Patient)
async def insert_symptom(
    symptom: Symptom, user: str, requester: str = Depends(verify_token)
):
    if (await db.get_user(requester)).isDoctor:
        user: Patient = await db.get_user(user)
        if user.isDoctor:
            raise HTTPException(
                status_code=500, detail="Should be Patient to add symptom"
            )
        user.symptoms.append(symptom)
        return await db.update_one("users", "id", user.id, user.dict())
    else:
        raise HTTPException(
            status_code=403, detail="Should be Doctor to access this endpoint"
        )

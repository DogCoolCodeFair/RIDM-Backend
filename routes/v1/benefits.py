from typing import List

from fastapi import APIRouter, Depends, HTTPException
from models.benefit import Benefit, BenefitStatus
from models.user import Patient

import utils.database as db
from models.disease import Disease
from utils.jwt import verify_doctor, verify_token

benefit_router = APIRouter()


@benefit_router.post(
    "/request", response_model=Benefit, description="산정특례를 신청합니다."
)
async def request(disease: Disease,user: str = Depends(verify_token)):
    user: Patient = await db.get_user(user)
    if user.isDoctor:
        raise HTTPException(status_code=403, detail="Should be Patient to access this endpoint")
    benefit = Benefit(status=BenefitStatus.waiting, disease=disease, userId=user.id)
    await db.insert_one("benefits", benefit.dict())
    return benefit

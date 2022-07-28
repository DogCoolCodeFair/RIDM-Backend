from pydoc import doc
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

@benefit_router.get("/{user}", response_model=List[Benefit], description="특정 환자가 신청한 대기중인 산정특례를 반환합니다. (의사만 접근 가능합니다)")
async def find_benefit(user:str, requester: str = Depends(verify_doctor)):
    user: Patient = await db.get_user(user)
    if user.isDoctor:
        raise HTTPException(status_code=403, detail="Should be Patient to query benefits")
    return [Benefit.parse_obj(document) for document in await db.find_many("benefits", "userId", user.id)]
from datetime import date, datetime
import io
from pydoc import doc
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import StreamingResponse

import utils.database as db
from models.benefit import Benefit, BenefitStatus, DiseaseType
from models.disease import Disease
from models.user import Patient
from utils.image import create_image_diagnosis, create_image_document
from utils.jwt import verify_doctor, verify_token

benefit_router = APIRouter()


@benefit_router.post("/request", response_model=Benefit, description="산정특례를 신청합니다.")
async def request(disease: Disease, user: str = Depends(verify_token)):
    user: Patient = await db.get_user(user)
    if user.isDoctor:
        raise HTTPException(
            status_code=403, detail="Should be Patient to access this endpoint"
        )
    benefit = Benefit(
        benefitId=round(datetime.now().timestamp()),
        status=BenefitStatus.waiting,
        disease=disease,
        userId=user.id,
        date=date.today(),
    )
    await db.insert_one("benefits", benefit.dict())
    return benefit


@benefit_router.post("/process/{benefitId}", response_model=Benefit)
async def process(
    benefitId: int,
    memo: str = Query(..., description="의사 소견"),
    type: DiseaseType = Query(..., description="질환 종류"),
    methodIndex: int = Query(..., description="진단 방법 인덱스, 예) 유전학적 검사 -> 2"),
    signature: str = Query(..., description="의사 서명 Base64"),
    user: str = Depends(verify_doctor),
):
    benefit = await db.get_benefit(benefitId)
    if benefit.status != BenefitStatus.waiting:
        raise HTTPException(status_code=400, detail="Benefit is not waiting")
    benefit.memo, benefit.type, benefit.methodIndex, benefit.signature = (
        memo,
        type,
        methodIndex,
        signature,
    )
    benefit.status = BenefitStatus.approved
    return await db.update_one(
        "benefits", "benefitId", benefit.benefitId, benefit.dict()
    )


@benefit_router.post("/reject/{benefitId}", response_model=Benefit)
async def reject(benefitId: int, user: str = Depends(verify_doctor)):
    benefit = await db.get_benefit(benefitId)
    if benefit.status != BenefitStatus.waiting:
        raise HTTPException(status_code=400, detail="Benefit is not waiting")
    benefit.status = BenefitStatus.rejected
    return await db.update_one(
        "benefits", "benefitId", benefit.benefitId, benefit.dict()
    )


@benefit_router.get(
    "/@me",
    response_model=List[Benefit],
    description="자신의 산정특례를 가져옵니다. ",
)
async def my_benefit(user: str = Depends(verify_token)):
    user: Patient = await db.get_user(user)
    if user.isDoctor:
        raise HTTPException(
            status_code=403, detail="Should be Patient to query benefits"
        )
    return [
        Benefit.parse_obj(document)
        for document in await db.find_many("benefits", "userId", user.id)
    ]

@benefit_router.get(
    "/id/{benefitId}", response_model=Benefit, description="산정특례를 가져옵니다."
)
async def get_benefit(benefitId: int, requester: str = Depends(verify_token)):
    benefit = await db.get_benefit(benefitId)
    return Benefit.parse_obj(benefit)

@benefit_router.get(
    "/id/{benefitId}/diagnosis", description="산정특례 신청서 이미지 가져오기"
)
async def get_benefit_diagnosis(benefitId: int):
    benefit = await db.get_benefit(benefitId)
    patient = await db.get_user(benefit.userId)
    doctor = await db.get_user(patient.doctor)
    image = await create_image_diagnosis(benefit, patient, doctor)
    byteobj = io.BytesIO()
    image.save(byteobj, "PNG")
    byteobj.seek(0)
    return StreamingResponse(byteobj, media_type="image/png")

@benefit_router.get(
    "/id/{benefitId}/document", description="산정특례 신청서 이미지 가져오기"
)
async def get_benefit_document(benefitId: int):
    benefit = await db.get_benefit(benefitId)
    patient = await db.get_user(benefit.userId)
    doctor = await db.get_user(patient.doctor)
    image = await create_image_document(benefit, patient, doctor)
    byteobj = io.BytesIO()
    image.save(byteobj, "PNG")
    byteobj.seek(0)
    return StreamingResponse(byteobj, media_type="image/png")

@benefit_router.get(
    "/approved/{user}",
    response_model=List[Benefit],
    description="특정 환자의 승인된 산정특례를 가져옵니다. (의사만 접근 가능합니다)",
)
async def benefit_approved(user: str, requester: str = Depends(verify_doctor)):
    user: Patient = await db.get_user(user)
    if user.isDoctor:
        raise HTTPException(
            status_code=403, detail="Should be Patient to query benefits"
        )
    return [
        Benefit.parse_obj(document)
        for document in await db.find_many("benefits", "userId", user.id)
        if Benefit.parse_obj(document).status == BenefitStatus.approved
    ]


@benefit_router.get(
    "/{user}",
    response_model=List[Benefit],
    description="특정 환자가 신청한 대기중인 산정특례를 반환합니다. (의사만 접근 가능합니다)",
)
async def find_benefit(user: str, requester: str = Depends(verify_doctor)):
    user: Patient = await db.get_user(user)
    if user.isDoctor:
        raise HTTPException(
            status_code=403, detail="Should be Patient to query benefits"
        )
    return [
        Benefit.parse_obj(document)
        for document in await db.find_many("benefits", "userId", user.id)
        if Benefit.parse_obj(document).status == BenefitStatus.waiting
    ]

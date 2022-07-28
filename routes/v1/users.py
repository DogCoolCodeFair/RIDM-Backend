from datetime import date, time
from typing import List, Union

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.security import HTTPBearer
from starlette.responses import JSONResponse

import utils.database as db
from models import Benefit, Disease, Doctor, Patient, Symptom, User
from models.benefit import DiseaseType
from utils.jwt import verify_token

user_router = APIRouter()


@user_router.get("/add_doctor", response_model=Doctor)
async def add_doctor(
    id: str,
    name: str,
    phoneNumber: str,
    isDoctor: bool,
    doctorNumber: int,
    hospital: str,
    hospitalPhone: str,
    issueDate: date,
):
    doc = Doctor(
        id=id,
        name=name,
        phoneNumber=phoneNumber,
        isDoctor=isDoctor,
        doctorNumber=doctorNumber,
        hospital=hospital,
        hospitalPhone=hospitalPhone,
        issueDate=issueDate,
    )
    await db.insert_one("users", doc.dict())
    return doc


@user_router.post("/add_patient", response_model=Patient)
async def add_patient(patient: Patient):
    # pat = Patient(
    #     id=id,
    #     name=name,
    #     phoneNumber=phoneNumber,
    #     isDoctor=isDoctor,
    #     healthInsuranceNumber=healthInsuranceNumber,
    #     doctor=doctor,
    #     symptoms=symptoms,
    #     diseases=diseases
    # )
    await db.insert_one("users", patient.dict())
    return patient


@user_router.get(
    "/@me", response_model=Union[Doctor, Patient], response_model_exclude_unset=True
)
async def get_me(id: str = Depends(verify_token)):
    return await db.get_user(id)

@user_router.get("/{user}", response_model=Patient)
async def get_user(
    user: str, requester: str = Depends(verify_token)
):
    if (await db.get_user(requester)).isDoctor:
        user: Patient = await db.get_user(user)
        if user.isDoctor:
            raise HTTPException(
                status_code=500, detail="Query ID Should be Patient to search user"
            )
        return user
    else:
        raise HTTPException(
            status_code=403, detail="Should be Doctor to access this endpoint"
        )

# @test_router.get("/disease_echo", response_model=Disease)
# async def echo_disease(
#     id: str,
#     name: str,
#     subname: str,
#     symptoms: List[str],
#     affected: List[str],
#     supported: bool,
#     required: bool,
#     code: str,
# ):
#     obj = {
#         "id": id,
#         "name": name,
#         "subname": subname,
#         "symptoms": symptoms,
#         "affected": affected,
#         "supported": supported,
#         "required": required,
#         "code": code,
#     }
#     return Disease.parse_obj(obj)

# @test_router.get("/symptom_echo", response_model=Symptom)
# async def echo_symptom(name: str, date: date, time: time, symptoms: str):
#     obj = {
#         "name": name,
#         "date": date,
#         "time": time,
#         "symptoms": symptoms,
#     }
#     return Symptom.parse_obj(obj)

# @test_router.get("/benifit_echo", response_model=Benefit)
# async def echo_benifit(
#     id: str, memo: str, date: date, type: DiseaseType, detail: str, signature: str
# ):
#     obj = {
#         "id": id,
#         "memo": memo,
#         "date": date,
#         "type": type,
#         "detail": detail,
#         "signature": signature,
#     }
#     return Benefit.parse_obj(obj)

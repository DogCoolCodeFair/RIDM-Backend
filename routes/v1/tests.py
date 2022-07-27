from datetime import date, time
from typing import List
from fastapi import APIRouter, Depends, Query, Request
from fastapi.security import HTTPBearer
from models import User, Disease, Benefit, Symptom, Doctor, Patient
from starlette.responses import JSONResponse

import utils.database as db
from models.benifit import DiseaseType
from utils.jwt import verify_token

test_router = APIRouter()

@test_router.get("/doctor_echo", response_model=Doctor)
async def echo_doctor(
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


@test_router.get("/patient_echo", response_model=Patient)
async def echo_patient(
    id: str,
    name: str,
    phoneNumber: str,
    isDoctor: bool,
    healthInsuranceNumber: int,
    doctor: str,
):
    return Patient(
        id=id,
        name=name,
        phoneNumber=phoneNumber,
        isDoctor=isDoctor,
        healthInsuranceNumber=healthInsuranceNumber,
        doctor=doctor,
    )


@test_router.get("/benifit_echo", response_model=Benefit)
async def echo_benifit(
    id: str, memo: str, date: date, type: DiseaseType, detail: str, signature: str
):
    obj = {
        "id": id,
        "memo": memo,
        "date": date,
        "type": type,
        "detail": detail,
        "signature": signature,
    }
    return Benefit.parse_obj(obj)


@test_router.get("/disease_echo", response_model=Disease)
async def echo_disease(
    id: str,
    name: str,
    subname: str,
    symptoms: List[str],
    affected: List[str],
    supported: bool,
    required: bool,
    code: str,
):
    obj = {
        "id": id,
        "name": name,
        "subname": subname,
        "symptoms": symptoms,
        "affected": affected,
        "supported": supported,
        "required": required,
        "code": code,
    }
    return Disease.parse_obj(obj)


@test_router.get("/symptom_echo", response_model=Symptom)
async def echo_symptom(name: str, date: date, time: time, symptoms: str):
    obj = {
        "name": name,
        "date": date,
        "time": time,
        "symptoms": symptoms,
    }
    return Symptom.parse_obj(obj)


@test_router.get("/auth_test", response_model=Doctor)
async def auth_test(id: str = Depends(verify_token)):
    return Doctor.parse_obj(await db.find_one("users", "id",id))

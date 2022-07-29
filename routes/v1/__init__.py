from fastapi import APIRouter

from .auth import auth_router
from .benefits import benefit_router
from .diseases import disease_router
from .symptoms import symptom_router
from .users import user_router

v1_router = APIRouter()

v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])

v1_router.include_router(user_router, prefix="/user", tags=["user"])

v1_router.include_router(symptom_router, prefix="/symptom", tags=["symptom"])

v1_router.include_router(disease_router, prefix="/disease", tags=["disease"])

v1_router.include_router(benefit_router, prefix="/benefit", tags=["benefit"])

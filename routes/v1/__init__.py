from fastapi import APIRouter

from .tests import test_router
from .auth import auth_router

v1_router = APIRouter()

v1_router.include_router(test_router, prefix="/test", tags=["test"])

v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
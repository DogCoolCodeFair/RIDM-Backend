from fastapi import APIRouter

from .tests import test_router

v1_router = APIRouter()

v1_router.include_router(test_router, prefix="/test", tags=["test"])

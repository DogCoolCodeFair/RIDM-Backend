from fastapi import APIRouter

from .users import user_router
from .auth import auth_router

v1_router = APIRouter()

v1_router.include_router(user_router, prefix="/user", tags=["user"])

v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
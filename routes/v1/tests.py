from fastapi import APIRouter, Query, Request
from models import User, UserRole
from starlette.responses import JSONResponse

test_router = APIRouter()


@test_router.get("/{id}", response_model=User)
async def echo_data(
    id: str, name: str, role: UserRole = Query(UserRole.patient, description="유저 타입")
):
    obj = {"id": id, "role": role, "name": name}
    print(obj)
    return User.parse_obj(obj)

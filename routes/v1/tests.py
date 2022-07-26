from fastapi import APIRouter, Request, Query
from starlette.responses import JSONResponse

from models import User, UserRole

test_router = APIRouter()

@test_router.get("/{id}", response_model=User)
async def echo_data(id: str, name: str, role: UserRole = Query(UserRole.patient, description="유저 타입")):
    obj={"id":id, "role":role, "name":name}
    print(obj)
    return User.parse_obj(obj)

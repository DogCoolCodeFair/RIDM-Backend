from pydantic import BaseModel, Field
from enum import Enum


class UserRole(str, Enum):
    patient = "patient"
    doctor = "doctor"


class User(BaseModel):
    id: str = Field(..., description="유저 아이디", example="iamdoctor")
    role: UserRole = Field(..., description="유저 종류", example=UserRole.doctor)
    name: str = Field(..., description="유저 이름", example="홍길동")
    # 이런식으로 모델 쭉쭉 만들면 됩니다. pydantic에 보면 EmailStr 타입 등 프리셋 있으니 잘 찾아보시고 모델 구축하시면 됩니다.
    # 추가적으로, 이 모델을 바탕으로 Request나 Response Docs가 만들어 지니, 단순히 str이 아닌 나올 수 있는 데이터를 enum등 클래스 타입으로 제작해 사용해주세요.

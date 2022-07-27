from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(..., description="유저 아이디", example="iamdoctor")
    isDoctor: bool = Field(..., description="의사 여부", example=True)
    name: str = Field(..., description="유저 이름", example="홍길동")
    phoneNumber: str = Field(..., description="유저 휴대전화번호", example="01012345678")
    # 이런식으로 모델 쭉쭉 만들면 됩니다. pydantic에 보면 EmailStr 타입 등 프리셋 있으니 잘 찾아보시고 모델 구축하시면 됩니다.
    # 추가적으로, 이 모델을 바탕으로 Request나 Response Docs가 만들어 지니, 단순히 str이 아닌 나올 수 있는 데이터를 enum등 클래스 타입으로 제작해 사용해주세요.


class Doctor(User):
    doctorNumber: int = Field(..., description="의사 면허 번호", example="102505")  # 의사 면허 번호
    hospital: str = Field(..., description="담당 의료 기관", example="서울대병원")
    hospitalPhone: str = Field(..., description="담당 의료 기관", example="031-123-4567")
    issueDate: date = Field(..., description="날짜", example=date.today())  # 발급일자
    pass


class Patient(User):
    healthInsuranceNumber: int = Field(..., description="건강보험번호", example="532423432")
    doctor: str = Field(..., description="담당 의사 id", example="doctor1")
    pass  # 건강 보험증 번호, 등 산정특례에 필요한 애들 넣어야 하나요? @331leo

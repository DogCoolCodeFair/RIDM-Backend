from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from models.disease import Disease
from models.user import User


class DiseaseType(str, Enum):
    cancer = "암"
    other = "기타"


class BenefitStatus(str, Enum):
    waiting = "대기중"
    approved = "승인됨"
    rejected = "거부됨"


class Benefit(BaseModel):  # 산정특례
    benefitId: int = Field(
        round(datetime.now().timestamp()),
        description="산정특례 아이디",
        example=round(datetime.now().timestamp()),
    )
    status: BenefitStatus = Field(
        ..., description="산정특례 상태", example=BenefitStatus.waiting
    )
    userId: str = Field(..., description="산정특례 대상 유저 아이디")
    disease: Disease
    # id: str = Field(..., description="질병코드", example="Q93.5")
    memo: Optional[str] = Field(
        None, description="소견서 작성", example="환자의 증상과 질환을 기준으로 정확히 작성해주세요."
    )
    date: Optional[date] = None  # Field(None, description="날자")
    type: Optional[DiseaseType] = Field(
        None, description="질환 종류", example=DiseaseType.cancer
    )
    methodIndex: Optional[int] = Field(
        None, description="진단방법 인덱스 (몇번째 선택지), 예) 유전학적 검사 -> 2", example=2
    )
    signature: Optional[str] = Field(
        None, description="싸인이 저장된 base64", example="64KY64qUIOyLuOyduA=="
    )  # 싸인, 이상하면 바꿔주세요

from enum import Enum
from typing import List

from pydantic import BaseModel, Field
from datetime import date

class DiseaseType(str, Enum):
    cancer = "암"
    other = "기타"

class Benefit(BaseModel): # 산정특례
    id: str = Field(..., description="질병코드", example="Q93.5")
    memo: str = Field(..., description="소견서 작성", example="환자의 증상과 질환을 기준으로 정확히 작성해주세요.")
    date: date = Field(..., description="날짜", example=date.today())
    type: DiseaseType = Field(..., description="질환 종류", example=DiseaseType.cancer)
    detail: str = Field(..., description="상세한 질환 종류를 선택해주세요.", example="유전학적 검사")
    signature: str = Field(..., description="싸인이 저장된 base64", example="64KY64qUIOyLuOyduA==") # 싸인, 이상하면 바꿔주세요

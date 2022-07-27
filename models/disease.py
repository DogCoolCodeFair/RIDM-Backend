from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Disease(BaseModel):
    id: str = Field(..., description="질병코드", example="Q93.5")
    name: str = Field(..., description="질병 이름", example="엔젤만증후군")
    subname: str = Field(..., description="질병의 풀네임", example="4q21 microdeletion syndrome")
    symptoms: List(str) = Field(..., description="질병의 증상들", example="List['과도한 웃음', '발작']")
    affected: List(str) = Field(..., description="질병에 의해 영향 받는 곳", example="List['신경', '근육']")
    supported: bool = Field(..., description="의료비 지원 여부")
    required: bool = Field(..., description="산정특례 사전승인 신청 필요 여부")
    code: str = Field(..., description="산정특례 코드", example="V901")
    

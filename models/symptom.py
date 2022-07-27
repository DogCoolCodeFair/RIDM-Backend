from enum import Enum
from typing import List
from datetime import date, time
from pydantic import BaseModel, Field


class Symptom(BaseModel): # 증상들
    name: str = Field(..., description="증상 명", example="과도한 웃음")
    date: date = Field(..., description="날짜", example=date.today())
    time: time = Field(..., description="시간", example=time.now())
    symptoms: str = Field(..., description="의심되는 질병의 증상", example="엔젤만증후군 증상")

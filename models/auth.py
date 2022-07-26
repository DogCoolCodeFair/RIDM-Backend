from pydantic import BaseModel, Field

from models.user import User


class LoginResponse(BaseModel):  # 산정특례
    access_token: str = Field(..., description="엑세스 토큰", example="JWT.STYLE.TOKEN")
    user: User

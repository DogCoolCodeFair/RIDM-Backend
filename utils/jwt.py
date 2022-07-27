import jwt
from dotenv import load_dotenv
from os import getenv
load_dotenv()

async def generate_token(id: str):
    return jwt.encode({"id": id}, getenv("JWT_SECRET"), algorithm="HS256")

async def verify_token(token: str):
    try:
        return (jwt.decode(token, getenv("JWT_SECRET"), algorithms=["HS256"])).get("id")
    except:
        return False
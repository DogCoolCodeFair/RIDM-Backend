import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from routes.v1 import v1_router

load_dotenv()

cors_origins = json.loads(os.getenv("origins", '["*"]'))
app_config = {
    "title": "RIDM Backend",
    "description": "RIDM Backend [GitHub](https://github.com/DogCoolCodeFair/RIDM-Backend)",
    "version": "0.0.1",
    "redoc_url": "/docs/redoc",
    "docs_url": "/docs/swagger",
}

app = FastAPI(**app_config)


@app.get("/", include_in_schema=False)
async def route_root():
    return RedirectResponse(url="/docs/swagger")


app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/v1")

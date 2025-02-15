from fastapi import APIRouter

from src.app.api.rest.v1.auth import controllers as auth
from src.app.api.rest.v1.code_verification import controllers as code_verification

api = APIRouter()

api.include_router(
    code_verification.router, prefix="/v1/code_verification", tags=["code_verification"]
)
api.include_router(auth.router, prefix="/v1/auth", tags=["auth"])

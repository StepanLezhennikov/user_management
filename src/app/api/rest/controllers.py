from fastapi import APIRouter

from app.api.rest.v1.auth import controllers as auth
from app.api.rest.v1.password_reset import controllers as password_reset
from app.api.rest.v1.code_verification import controllers as code_verification

api = APIRouter()

api.include_router(
    code_verification.router, prefix="/v1/code_verification", tags=["code_verification"]
)
api.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
api.include_router(
    password_reset.router, prefix="/v1/password_reset", tags=["password_reset"]
)

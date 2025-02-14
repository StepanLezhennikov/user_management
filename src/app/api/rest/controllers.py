from fastapi import APIRouter

from src.app.api.rest.v1.user import controllers

api = APIRouter()

api.include_router(controllers.router, prefix="/v1/signup", tags=["signup"])

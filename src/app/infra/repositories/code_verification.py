from fastapi import HTTPException
from pydantic import EmailStr

from app.db.redis import redis_db
from app.core.config import Constants
from app.services.interfaces.repositories.code_verification_repository import (
    ACodeVerificationRepository,
)


class CodeVerificationRepository(ACodeVerificationRepository):

    def get_code(self, email: EmailStr) -> int:
        code = redis_db.get(email)
        if not code:
            raise HTTPException(status_code=410, detail="Code is expired")
        return int(code)

    def create(self, email: EmailStr, code: int) -> bool:
        return bool(redis_db.set(email, code, ex=Constants.expiration_time_for_code))

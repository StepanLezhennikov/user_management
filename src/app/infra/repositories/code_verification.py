from pydantic import EmailStr

from app.db.redis import redis_db
from app.core.config import Constants
from app.services.exceptions.code_verification_repo import CodeIsExpired
from app.services.interfaces.repositories.code_verification_repository import (
    ACodeVerificationRepository,
)


class CodeVerificationRepository(ACodeVerificationRepository):

    def get_code(self, email: EmailStr) -> int:
        code = redis_db.get(email)
        if not code:
            raise CodeIsExpired()
        return int(code)

    def create(self, email: EmailStr, code: int) -> bool:
        return bool(redis_db.set(email, code, ex=Constants.expiration_time_for_code))

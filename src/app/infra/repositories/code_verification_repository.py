from pydantic import EmailStr

from app.db.redis import redis_db
from app.services.interfaces.repositories.code_verification_repository import (
    ACodeVerificationRepository,
)


class CodeVerificationRepository(ACodeVerificationRepository):

    def get_code(self, email: EmailStr) -> int:
        try:
            return int(redis_db.get(email))
        except TypeError:
            return 0

    def create(self, email: EmailStr, code: int) -> bool:
        return bool(redis_db.set(email, code, ex=300))

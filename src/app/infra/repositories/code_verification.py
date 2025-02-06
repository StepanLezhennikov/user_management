from pydantic import EmailStr

from app.db.redis import redis_db
from app.core.config import Constants
from app.services.interfaces.exceptions.code_verification_repository import ExpiryError
from app.services.interfaces.repositories.code_verification_repository import (
    ACodeVerificationRepository,
)


class CodeVerificationRepository(ACodeVerificationRepository):

    def get_code(self, email: EmailStr) -> int:
        try:
            return int(redis_db.get(email))
        except ExpiryError:
            return 0

    def create(self, email: EmailStr, code: int) -> bool:
        return bool(redis_db.set(email, code, ex=Constants.expiration_time_for_code))

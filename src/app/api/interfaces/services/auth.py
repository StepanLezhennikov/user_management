from abc import ABC

from pydantic import EmailStr

from app.schemas.user import UserCreate


class AAuthService(ABC):

    async def create(self, user_data: UserCreate) -> UserCreate: ...

    async def check_user_exists(self, email: EmailStr) -> bool: ...

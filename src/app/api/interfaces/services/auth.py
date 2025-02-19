from abc import ABC

from pydantic import EmailStr

from app.schemas.user import UserCreate


class AAuthService(ABC):

    async def create(self, user_data: UserCreate) -> UserCreate: ...

    async def check_user_exists(self, email: str) -> bool: ...

    async def reset_password(self, email: EmailStr, password: str) -> bool: ...

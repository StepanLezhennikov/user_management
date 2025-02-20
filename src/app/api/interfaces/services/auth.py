from abc import ABC

from app.schemas.user import UserCreate


class AAuthService(ABC):

    async def create(self, user_data: UserCreate) -> UserCreate: ...

    async def check_user_exists(self, email: str) -> bool: ...

    async def get_user_id(self, email: str) -> int: ...

    async def reset_password(self, user_id: int, password: str) -> bool: ...

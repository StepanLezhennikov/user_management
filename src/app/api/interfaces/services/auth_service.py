from abc import ABC

from app.schemas.user import UserCreate


class AAuthService(ABC):

    async def register(self, user_data: UserCreate) -> UserCreate: ...

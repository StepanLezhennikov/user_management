from abc import ABC

from app.schemas.user import UserCreate


class AAuthService(ABC):

    async def create(self, user_data: UserCreate) -> UserCreate: ...

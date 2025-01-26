from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import User


class AUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User, session: AsyncSession) -> bool:
        pass

    @abstractmethod
    async def get(self, session: AsyncSession, **filters: int) -> User:
        pass

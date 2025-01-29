from abc import ABC, abstractmethod

from app.schemas.user import User, UserCreate


class AUserRepository(ABC):
    @abstractmethod
    async def create(self, user: UserCreate) -> User:
        pass

    @abstractmethod
    async def get(self, **filters: int) -> User:
        pass

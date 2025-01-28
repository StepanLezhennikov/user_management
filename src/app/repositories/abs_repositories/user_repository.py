from abc import ABC, abstractmethod
from typing import Any

from app.schemas.user import User


class AUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User, session: Any) -> bool:
        pass

    @abstractmethod
    async def get(self, session: Any, **filters: int) -> User:
        pass

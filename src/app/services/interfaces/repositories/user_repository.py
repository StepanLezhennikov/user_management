from abc import ABC, abstractmethod

from app.schemas.user import User, UserCreate


class AUserRepository(ABC):
    @abstractmethod
    async def create(self, user: UserCreate, role_ids: list[int] = None) -> User:
        pass

    @abstractmethod
    async def get(self, **filters) -> User:
        pass

    @abstractmethod
    async def get_permissions(self, email: str) -> list[str] | None:
        pass

    @abstractmethod
    async def update_password(self, user_id: int, new_hashed_password: str) -> str:
        pass

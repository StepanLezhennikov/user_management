from abc import ABC, abstractmethod

from app.schemas.user import User, UserCreate, DeletedUser


class AUserRepository(ABC):
    @abstractmethod
    async def create(self, user: UserCreate, role_ids: list[int] = None) -> User:
        pass

    @abstractmethod
    async def get(self, **filters) -> User:
        pass

    @abstractmethod
    async def get_all(self, limit: int, offset: int, **filters) -> list[User]:
        pass

    @abstractmethod
    async def get_permissions(self, email: str) -> list[str] | None:
        pass

    @abstractmethod
    async def update(self, user_id: int, **values) -> User | None:
        pass

    @abstractmethod
    async def update_password(self, user_id: int, new_hashed_password: str) -> str:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> DeletedUser | None:
        pass

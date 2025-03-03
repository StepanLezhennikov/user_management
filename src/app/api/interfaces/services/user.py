from abc import ABC, abstractmethod

from app.schemas.user import User, UserCreate


class AUserService(ABC):
    @abstractmethod
    async def create(self, user_data: UserCreate) -> User: ...

    @abstractmethod
    async def check_user_exists(self, **filters) -> bool: ...

    @abstractmethod
    async def get(self, **filters) -> User: ...

    @abstractmethod
    async def get_all(self, limit: int, offset: int, **filters) -> list[User]: ...

    @abstractmethod
    async def get_user_permissions(self, email: str) -> list[str] | None: ...

    @abstractmethod
    async def reset_password(self, user_id: int, password: str) -> bool: ...

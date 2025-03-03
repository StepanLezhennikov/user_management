from abc import ABC, abstractmethod

from app.services.interfaces.repositories.role_repository import ARoleRepository
from app.services.interfaces.repositories.user_repository import AUserRepository
from app.services.interfaces.repositories.permission_repository import (
    APermissionRepository,
)


class AUnitOfWork(ABC):
    users: AUserRepository
    roles: ARoleRepository
    permissions: APermissionRepository

    async def __aenter__(self) -> "AUnitOfWork":
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, *args, **kwargs
    ) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

        await self.close()

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...

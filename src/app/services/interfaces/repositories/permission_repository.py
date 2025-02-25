from abc import ABC, abstractmethod

from app.schemas.permission import Permission, PermissionCreate


class APermissionRepository(ABC):

    @abstractmethod
    async def create(self, permission: PermissionCreate) -> PermissionCreate:
        pass

    @abstractmethod
    async def get(self, **filters) -> list[Permission] | None:
        pass

    @abstractmethod
    async def update(self, permission_id: int, **values) -> Permission | None:
        pass

    @abstractmethod
    async def delete(self, permission_id: int) -> Permission | None:
        pass

from abc import ABC, abstractmethod

from app.schemas.permission import Permission, PermissionCreate, PermissionUpdate


class APermissionService(ABC):

    @abstractmethod
    async def create(self, permission_create: PermissionCreate) -> PermissionCreate:
        pass

    @abstractmethod
    async def get(self, **filters) -> list[Permission]:
        pass

    @abstractmethod
    async def update(
        self, permission_id: int, permission_update: PermissionUpdate
    ) -> Permission:
        pass

    @abstractmethod
    async def delete(self, permission_create: PermissionCreate) -> PermissionCreate:
        pass

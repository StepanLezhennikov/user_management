from abc import ABC, abstractmethod

from app.schemas.role import RoleCreate, RoleUpdate
from app.infra.repositories.models.user_model import Role


class ARoleService(ABC):

    @abstractmethod
    async def create(self, role_create: RoleCreate) -> RoleCreate:
        pass

    @abstractmethod
    async def get(self, **filters) -> list[Role]:
        pass

    @abstractmethod
    async def update(self, role_id: int, role_update: RoleUpdate) -> Role:
        pass

    @abstractmethod
    async def delete(self, role_id: int) -> Role:
        pass

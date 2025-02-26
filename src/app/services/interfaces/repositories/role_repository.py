from abc import ABC, abstractmethod

from app.schemas.role import Role, RoleCreate


class ARoleRepository(ABC):
    @abstractmethod
    async def create(self, role: RoleCreate) -> RoleCreate:
        pass

    @abstractmethod
    async def get(self, **filters) -> list[Role]:
        pass

    @abstractmethod
    async def update(self, role_id: int, **values) -> Role:
        pass

    @abstractmethod
    async def delete(self, role_id: int) -> Role:
        pass

    @abstractmethod
    async def filter(self, roles: list[str]) -> list[Role] | None:
        pass

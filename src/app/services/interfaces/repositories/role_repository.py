from abc import ABC, abstractmethod

from app.schemas.role import Role, RoleCreate


class ARoleRepository(ABC):
    @abstractmethod
    async def create(self, role: RoleCreate) -> RoleCreate:
        pass

    @abstractmethod
    async def get(self, **filters) -> Role:
        pass

    @abstractmethod
    async def filter(self, roles: list[str]) -> list[Role] | None:
        pass

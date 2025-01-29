from abc import ABC, abstractmethod

from app.repositories.abs_repositories.user_repository import AUserRepository


class AUnitOfWork(ABC):
    users: AUserRepository

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

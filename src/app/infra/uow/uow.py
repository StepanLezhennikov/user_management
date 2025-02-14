import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.infra.repositories.user import UserRepository
from app.services.interfaces.uow.uow import AUnitOfWork

logger = logging.getLogger(__name__)


class Uow(AUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        self._session = None

    async def __aenter__(self) -> AUnitOfWork:
        self._session = self._session_factory()
        self.users = UserRepository(session=self._session)

        return await super().__aenter__()

    async def commit(self) -> None:
        logger.info("UoW commit")
        await self._session.commit()

    async def rollback(self) -> None:
        logger.info("UoW rollback")
        await self._session.rollback()

    async def close(self) -> None:
        logger.info("UoW close")
        await self._session.close()

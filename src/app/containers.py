from dependency_injector import providers, containers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings
from app.infra.uow.uow import Uow
from app.services.services.auth_service import AuthService
from app.services.services.email_service import EmailService


class Container(containers.DeclarativeContainer):
    config = settings

    engine = providers.Singleton(create_async_engine, config.DATABASE_URL)
    session_factory = providers.Singleton(
        async_sessionmaker, autocommit=False, autoflush=False, bind=engine
    )

    uow = providers.Factory(Uow, session_factory=session_factory)

    auth_service = providers.Factory(AuthService, uow=uow)
    email_service = providers.Factory(EmailService)

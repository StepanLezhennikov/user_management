import aioboto3
from dependency_injector import providers, containers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings
from app.infra.uow.uow import Uow
from app.services.services.auth_service import AuthService
from app.services.services.email_service import EmailService
from app.services.services.code_verification_service import CodeVerificationService
from app.infra.repositories.code_verification_repository import (
    CodeVerificationRepository,
)


class Container(containers.DeclarativeContainer):
    config = settings

    engine = providers.Singleton(create_async_engine, config.DATABASE_URL)
    session_factory = providers.Singleton(
        async_sessionmaker, autocommit=False, autoflush=False, bind=engine
    )
    aioboto3_session = providers.Singleton(
        aioboto3.Session,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME,
    )

    code_verification_repository = providers.Factory(CodeVerificationRepository)
    uow = providers.Factory(Uow, session_factory=session_factory)

    auth_service = providers.Factory(AuthService, uow=uow)
    email_service = providers.Factory(EmailService, aioboto3_session=aioboto3_session)
    code_verification_service = providers.Factory(
        CodeVerificationService, code_ver_repo=code_verification_repository
    )

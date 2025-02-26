import aioboto3
from dependency_injector import providers, containers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.session import get_session
from app.core.config import settings
from app.infra.uow.uow import Uow
from app.services.services.jwt import JwtService
from app.services.services.auth import AuthService
from app.services.services.role import RoleService
from app.infra.clients.aws.email import EmailClient
from app.infra.repositories.role import RoleRepository
from app.infra.repositories.user import UserRepository
from app.services.services.email import EmailService
from app.services.services.permission import PermissionService
from app.infra.repositories.permission import PermissionRepository
from app.services.services.code_verification import CodeVerificationService
from app.services.services.password_security import PasswordSecurityService
from app.infra.repositories.code_verification import CodeVerificationRepository


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
    session = providers.Resource(get_session)

    email_client = providers.Factory(EmailClient, aioboto3_session=aioboto3_session)

    code_verification_repository = providers.Factory(CodeVerificationRepository)
    user_repository = providers.Factory(UserRepository, session=session)
    role_repository = providers.Factory(RoleRepository, session=session)
    permission_repository = providers.Factory(PermissionRepository, session=session)
    uow = providers.Factory(Uow, session_factory=session_factory)

    auth_service = providers.Factory(AuthService, uow=uow)
    email_service = providers.Factory(EmailService, email_client=email_client)
    code_verification_service = providers.Factory(
        CodeVerificationService, code_ver_repo=code_verification_repository
    )
    password_security_service = providers.Factory(PasswordSecurityService, uow=uow)
    jwt_service = providers.Factory(JwtService, user_repository=user_repository)
    permission_service = providers.Factory(PermissionService, uow=uow)
    role_service = providers.Factory(RoleService, uow=uow)

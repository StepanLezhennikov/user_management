from dependency_injector import providers, containers

from app.db.session import get_session
from app.core.config import Settings
from app.services.auth import AuthService
from app.repositories.impl_repositories.user_repository import UserRepository


class Container(containers.DeclarativeContainer):
    config = Settings()

    session = providers.Resource(get_session)
    user_repository = providers.Factory(UserRepository, session=session)
    auth_service = providers.Factory(AuthService, user_repository=user_repository)

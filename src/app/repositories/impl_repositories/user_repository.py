from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.user import User as SQLAlchemyUser
from src.app.schemas.user import User, UserCreate
from app.repositories.exceptions.user_repository import UserNotFound
from src.app.repositories.abs_repositories.user_repository import AUserRepository


class UserRepository(AUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: UserCreate) -> UserCreate:
        added_user = SQLAlchemyUser(
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=user.hashed_password,
            is_blocked=user.is_blocked,
        )
        self._session.add(added_user)
        return UserCreate.model_validate(added_user)

    async def get(self, **filters: int) -> User | None:
        query = select(SQLAlchemyUser).filter_by(**filters)
        result = await self._session.execute(query)
        try:
            return result.scalar_one()
        except UserNotFound:
            return None

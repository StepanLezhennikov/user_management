from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.user import User as SQLAlchemyUser
from src.app.schemas.user import User, UserCreate
from app.repositories.exceptions.user_repository import UserNotFound
from src.app.repositories.abs_repositories.user_repository import AUserRepository


class UserRepository(AUserRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: UserCreate) -> User:
        added_user = SQLAlchemyUser(
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=user.hashed_password,
            is_blocked=user.is_blocked,
        )
        self._session.add(added_user)
        await self._session.commit()
        await self._session.refresh(added_user)
        return added_user

    async def get(self, session: AsyncSession, **filters: int) -> User | None:
        query = select(User).filter_by(**filters)
        result = await session.execute(query)
        try:
            user = result.scalar_one()
            return user
        except UserNotFound:
            return None

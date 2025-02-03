from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas.user import User, UserCreate
from app.infra.repositories.models.user_model import User as SQLAlchemyUser
from app.services.interfaces.exceptions.user_repository import UserNotFound
from app.services.interfaces.repositories.user_repository import AUserRepository


class UserRepository(AUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: UserCreate) -> UserCreate:
        added_user = SQLAlchemyUser(
            username=user.username,
            email=str(user.email),
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=user.password,
        )
        self._session.add(added_user)
        return user

    async def get(self, **filters: int) -> User | None:
        query = select(SQLAlchemyUser).filter_by(**filters)
        result = await self._session.execute(query)
        try:
            return result.scalar_one()
        except UserNotFound:
            return None

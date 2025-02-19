from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import User, UserCreate
from app.infra.repositories.models.user_model import User as SQLAlchemyUser
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

    async def get(self, **filters) -> User | None:
        query = select(SQLAlchemyUser).filter_by(**filters)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        return User.model_validate(user) if user else None

    async def update_password(self, user_id: str, new_password: str) -> str:
        query = (
            update(SQLAlchemyUser)
            .where(SQLAlchemyUser.id == user_id)
            .values(hashed_password=new_password)
        )
        await self._session.execute(query)
        return new_password

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import User, UserCreate
from app.infra.repositories.models.user_model import Role
from app.infra.repositories.models.user_model import User as UserModel
from app.services.interfaces.repositories.user_repository import AUserRepository


class UserRepository(AUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: UserCreate, role_ids: list[int] = None) -> User:
        added_user = UserModel(
            username=user.username,
            email=str(user.email),
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=user.password,
        )
        if role_ids:
            query = select(Role).where(Role.id.in_(role_ids))
            result = await self._session.execute(query)
            roles = result.scalars().all()

            added_user.roles = roles

        self._session.add(added_user)
        await self._session.flush()
        return User.model_validate(added_user)

    async def get(self, **filters) -> User | None:
        query = select(UserModel).filter_by(**filters)
        result = await self._session.execute(query)
        user = result.scalars().first()
        return User.model_validate(user) if user else None

    async def get_permissions(self, email: str) -> list[str] | None:
        query = (
            select(UserModel)
            .filter_by(email=email)
            .options(selectinload(UserModel.roles).selectinload(Role.permissions))
        )
        result = await self._session.execute(query)
        user = result.unique().scalar_one_or_none()

        if user is None:
            return None

        permissions = {perm.name for role in user.roles for perm in role.permissions}

        return list(permissions)

    async def update_password(self, user_id: int, new_hashed_password: str) -> str:
        query = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(hashed_password=new_hashed_password)
        )
        await self._session.execute(query)
        return new_hashed_password

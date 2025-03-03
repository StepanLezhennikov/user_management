from sqlalchemy import delete, select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import User, UserCreate, DeletedUser
from app.infra.repositories.models.user_model import Role
from app.infra.repositories.models.user_model import User as UserModel
from app.infra.repositories.models.user_model import UserRole
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

    async def get_all(self, limit: int, offset: int, **filters) -> list[User] | None:
        query = select(UserModel).filter_by(**filters).limit(limit).offset(offset)
        result = await self._session.execute(query)
        users_raw = result.scalars().unique().all()

        users = list(map(User.model_validate, users_raw))
        return users if users else None

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

    async def update(self, user_id: int, **values) -> User | None:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(**values)
            .returning(UserModel)
        )
        result = await self._session.execute(stmt)

        user = result.scalars().first()

        if user:
            await self._session.refresh(user, attribute_names=["roles"])
            return User.model_validate(user)
        return None

    async def update_password(self, user_id: int, new_hashed_password: str) -> str:
        query = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(hashed_password=new_hashed_password)
        )
        await self._session.execute(query)
        return new_hashed_password

    async def delete(self, user_id: int) -> DeletedUser | None:
        delete_user_roles_query = delete(UserRole).where(UserRole.c.user_id == user_id)
        await self._session.execute(delete_user_roles_query)

        query = delete(UserModel).where(UserModel.id == user_id).returning(UserModel)
        result = await self._session.execute(query)
        user = result.scalars().first()

        return DeletedUser.model_validate(user) if user else None

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.role import RoleCreate
from app.schemas.user import User, UserCreate
from app.schemas.permission import PermissionCreate
from app.infra.repositories.user import UserRepository
from app.services.services.password_security import PasswordSecurityService
from app.infra.repositories.models.user_model import User as UserModel


async def test_create_user(
    user_repo: UserRepository,
    session: AsyncSession,
    user_create: UserCreate,
    created_role_admin: RoleCreate,
) -> None:
    created_usr = await user_repo.create(user_create, [1])

    query = select(UserModel).where(UserModel.email == user_create.email)
    result = await session.execute(query)
    user = result.scalars().first()

    assert user is not None
    assert user.id == created_usr.id
    assert user.email == user_create.email
    assert user.first_name == user_create.first_name
    assert user.last_name == user_create.last_name


async def test_get_user_by_email(user_repo: UserRepository, created_user: User) -> None:

    user = await user_repo.get(email=created_user.email)
    assert user is not None
    assert user.id == created_user.id
    assert user.email == created_user.email
    assert user.first_name == created_user.first_name
    assert user.last_name == created_user.last_name


async def test_get_user_by_email_not_found(
    user_repo: UserRepository, created_user: User
) -> None:
    wrong_email = "wrong@example.com"
    user = await user_repo.get(email=wrong_email)
    assert user is None


async def test_update_password(
    user_repo: UserRepository,
    session: AsyncSession,
    created_user: User,
    new_hashed_password: str,
    new_password: str,
    password_security_service: PasswordSecurityService,
) -> None:
    await user_repo.update_password(created_user.id, new_hashed_password)

    query = select(UserModel).where(UserModel.id == created_user.id)
    result = await session.execute(query)
    user = result.scalars().first()

    assert user.hashed_password == new_hashed_password


async def test_get_permissions(
    user_repo: UserRepository,
    session: AsyncSession,
    created_user: User,
    created_role_admin: RoleCreate,
    created_permission_list: list[PermissionCreate],
) -> None:
    permissions = await user_repo.get_permissions(created_user.email)

    assert permissions is not None

    assert permissions[0] in [perm.name for perm in created_permission_list]

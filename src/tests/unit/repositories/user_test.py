from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import User, UserCreate
from app.infra.repositories.user import UserRepository
from app.infra.repositories.models.user_model import User as UserModel


async def test_create_user(
    user_repo: UserRepository, session: AsyncSession, user_create: UserCreate
) -> None:
    await user_repo.create(user_create)

    query = select(UserModel).where(UserModel.email == user_create.email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    assert user is not None
    assert user.id is not None
    assert user.email == user_create.email
    assert user.first_name == user_create.first_name
    assert user.last_name == user_create.last_name


async def test_get_user_by_email(
    user_repo: UserRepository, session: AsyncSession, created_user: User
) -> None:
    user = await user_repo.get(email=created_user.email)
    assert user is not None
    assert user.id == created_user.id
    assert user.email == created_user.email
    assert user.first_name == created_user.first_name
    assert user.last_name == created_user.last_name


async def test_get_user_by_email_not_found(
    user_repo: UserRepository, session: AsyncSession, created_user: User
) -> None:
    wrong_email = "wrong@example.com"
    user = await user_repo.get(email=wrong_email)
    assert user is None

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserPrivate
from src.app.database import Base, engine, get_db
from app.infrastructure.repositories.user.user_repository import UserRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root(session: AsyncSession = Depends(get_db)):
    new_user = UserPrivate(
        username="johndoe 6",
        email="johndoe6@example.com",
        first_name="John",
        last_name="Doe",
        hashed_password="hashed_password",
        is_blocked=False,
    )

    user_rep = UserRepository()
    user = await user_rep.create(new_user, session)
    if user is None:
        return {"message": "User not added"}
    return {"message": f"User added : {new_user.username}"}

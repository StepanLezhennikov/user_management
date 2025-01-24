from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.app.models import User
from src.app.database import engine, Base, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root(session: AsyncSession = Depends(get_db)):
    new_user = User(
        username="johndoe 2",
        email="johndoe2@example.com",
        first_name="John",
        last_name="Doe",
        hashed_password="hashed_password_example",
        is_blocked=False
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"message": f"User added : {new_user.username}"}

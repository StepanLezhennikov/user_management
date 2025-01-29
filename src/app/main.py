from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.db.base import Base
from src.app.containers import Container
from src.app.db.session import engine
from src.app.api.rest.controllers import api


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


container = Container()
container.wire(modules=[__name__, "src.app.api.rest.v1.user.controllers"])

app = FastAPI(lifespan=lifespan)

app.container = container

app.include_router(api)


@app.get("/")
async def read_root():
    return {"message": "Hello World"}

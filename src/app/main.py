from fastapi import FastAPI

from app.containers import Container
from app.api.rest.controllers import api

container = Container()

container.wire(packages=[__name__, "app.api.rest.v1"])
container.wire(packages=[__name__, "app.services.services"])

app = FastAPI()

app.container = container

app.include_router(api)


@app.get("/")
async def read_root():
    return {"message": "Hello World"}

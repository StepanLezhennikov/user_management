from fastapi import FastAPI

from app.containers import Container
from app.api.rest.controllers import api

container = Container()
container.wire(modules=[__name__, "app.api.rest.v1.code_verification.controllers"])
container.wire(modules=[__name__, "app.api.rest.v1.auth.controllers"])
container.wire(modules=[__name__, "app.api.rest.v1.password_reset.controllers"])

app = FastAPI()

app.container = container

app.include_router(api)


@app.get("/")
async def read_root():
    return {"message": "Hello World"}

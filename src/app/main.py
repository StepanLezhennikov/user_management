from fastapi import FastAPI

from src.app.containers import Container
from src.app.api.rest.controllers import api

container = Container()
container.wire(modules=[__name__, "src.app.api.rest.v1.code_verification.controllers"])
container.wire(modules=[__name__, "src.app.api.rest.v1.auth.controllers"])

app = FastAPI()

app.container = container

app.include_router(api)


@app.get("/")
async def read_root():
    return {"message": "Hello World"}

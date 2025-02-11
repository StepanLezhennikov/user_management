import json
from typing import Any
from collections.abc import Callable

import orjson
from pydantic.v1.json import pydantic_encoder
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import Settings


def json_dumps(value: Any, *, default: Callable[[Any], Any] = pydantic_encoder) -> str:
    return json.dumps(value, default=default)


class SqlAlchemyDatabase:
    def __init__(self, settings: Settings) -> None:
        self._engine: AsyncEngine = create_async_engine(
            url=str(settings.RDB.dsn),
            pool_size=settings.RDB.pool_size,
            max_overflow=settings.RDB.max_overflow,
            pool_pre_ping=settings.RDB.pool_pre_ping,
            connect_args={
                "timeout": settings.RDB.connection_timeout,
                "command_timeout": settings.RDB.command_timeout,
                **settings.RDB.connect_args,
                "server_settings": {
                    "jit": "off",
                    **settings.RDB.server_settings,
                    "application_name": settings.RDB.app_naorjsonme,
                    "timezone": settings.RDB.timezone,
                },
            },
            json_serializer=json_dumps,
            json_deserializer=orjson.loads,
            echo=settings.RDB.debug,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory

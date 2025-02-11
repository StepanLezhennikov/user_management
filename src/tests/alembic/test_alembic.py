from typing import AsyncGenerator

import pytest
from pytest_alembic.tests import (  # noqa
    test_upgrade,
    test_up_down_consistency,
    test_single_head_revision,
    test_model_definitions_match_ddl,
)
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection

from alembic.config import Config


@pytest.fixture(scope="module")
def alembic_config() -> Config:
    return Config("/alembic.ini")


@pytest.fixture(scope="module")
async def alembic_engine(
    setup_sqla_db: AsyncEngine,
) -> AsyncGenerator[AsyncConnection, None]:
    async with setup_sqla_db.connect() as connection:
        yield connection

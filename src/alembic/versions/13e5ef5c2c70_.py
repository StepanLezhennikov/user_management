"""empty message

Revision ID: 13e5ef5c2c70
Revises: a28737db5728
Create Date: 2025-02-03 11:13:12.143031

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "13e5ef5c2c70"
down_revision: Union[str, None] = "a28737db5728"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.db.base import Base
from app.infra.repositories.models.role import user_role

if TYPE_CHECKING:
    from app.infra.repositories.models.role import Role


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    hashed_password: Mapped[str]
    is_blocked: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

    roles: Mapped[list["Role"]] = relationship(
        "Role", secondary=user_role, back_populates="users"
    )

from datetime import datetime

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.app.db.base import Base

role_permission_table = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
)


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())

    roles = relationship(
        "Role", secondary=role_permission_table, back_populates="permissions"
    )

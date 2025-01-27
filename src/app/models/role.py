from datetime import datetime

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.app.db.base import Base

user_role_table = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    role: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())

    user = relationship("User", secondary=user_role_table, back_populates="role")

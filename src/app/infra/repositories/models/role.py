from datetime import datetime

from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.db.base import Base

user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    ForeignKeyConstraint(["user_id"], ["users.id"], name="user_role_user_id_fk"),
    ForeignKeyConstraint(["role_id"], ["roles.id"], name="user_role_role_id_fk"),
)


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    role: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

    permissions = relationship(
        "Permission", secondary="role_permission", back_populates="roles"
    )
    users = relationship("User", secondary="user_role", back_populates="roles")

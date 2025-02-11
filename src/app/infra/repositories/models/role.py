from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.db.base import Base


class UserRole(Base):
    __tablename__ = "user_role"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    role: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

    permissions = relationship(
        "RolePermission", back_populates="role", cascade="all, delete-orphan"
    )
    users = relationship("UserRole", back_populates="role")

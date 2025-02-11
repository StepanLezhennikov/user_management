from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.db.base import Base


class RolePermission(Base):
    __tablename__ = "role_permission"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"))

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

    roles = relationship(
        "RolePermission", back_populates="permission", cascade="all, delete-orphan"
    )

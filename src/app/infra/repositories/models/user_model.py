from datetime import datetime

from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.db.base import Base

RolePermission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
    ForeignKeyConstraint(["role_id"], ["roles.id"], name="role_permission_role_id_fk"),
    ForeignKeyConstraint(
        ["permission_id"], ["permissions.id"], name="role_permission_permission_id_fk"
    ),
)


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

    roles = relationship("Role", secondary=RolePermission, back_populates="permissions")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    role: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

    permissions = relationship(
        "Permission", secondary=RolePermission, back_populates="roles"
    )
    users = relationship("User", secondary="user_role", back_populates="roles")


UserRole = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    ForeignKeyConstraint(["user_id"], ["users.id"], name="user_role_user_id_fk"),
    ForeignKeyConstraint(["role_id"], ["roles.id"], name="user_role_role_id_fk"),
)


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

    roles = relationship(
        "Role", secondary=UserRole, back_populates="users", lazy="joined"
    )

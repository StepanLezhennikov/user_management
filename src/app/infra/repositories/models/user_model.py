from datetime import datetime

from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.db.base import Base

# Определение таблицы role_permission
role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
    ForeignKeyConstraint(["role_id"], ["roles.id"], name="role_permission_role_id_fk"),
    ForeignKeyConstraint(
        ["permission_id"], ["permissions.id"], name="role_permission_permission_id_fk"
    ),
)


# Класс Permission
class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

    # Отношение с классом Role через таблицу role_permission
    roles = relationship(
        "Role", secondary=role_permission, back_populates="permissions"
    )


# Класс Role
class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    role: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

    # Отношение с классом Permission через таблицу role_permission
    permissions = relationship(
        "Permission", secondary=role_permission, back_populates="roles"
    )
    users = relationship("User", secondary="user_role", back_populates="roles")


# Таблица user_role для связи между User и Role
user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    ForeignKeyConstraint(["user_id"], ["users.id"], name="user_role_user_id_fk"),
    ForeignKeyConstraint(["role_id"], ["roles.id"], name="user_role_role_id_fk"),
)


# Класс User
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

    # Отношение с классом Role через таблицу user_role
    roles = relationship("Role", secondary=user_role, back_populates="users")

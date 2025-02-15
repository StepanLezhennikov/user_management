# from datetime import datetime
# from sqlalchemy.orm import Mapped, relationship, mapped_column
# from app.db.base import Base
# from app.infra.repositories.models.permission import Permission
# from app.infra.repositories.models.role_permission import role_permission
# from app.infra.repositories.models.user_role import user_role
# from app.infra.repositories.models.user_model import User
#
# class Role(Base):
#     __tablename__ = "roles"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
#     role: Mapped[str] = mapped_column(unique=True)
#     created_at: Mapped[datetime] = mapped_column(default=datetime.now)
#     updated_at: Mapped[datetime] = mapped_column(default=datetime.now)
#
#     permissions = relationship(
#         Permission, secondary=role_permission, back_populates="roles"
#     )
#     users = relationship(User, secondary=user_role, back_populates="roles")

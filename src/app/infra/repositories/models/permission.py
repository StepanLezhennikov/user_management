# from datetime import datetime
# from sqlalchemy.orm import Mapped, relationship, mapped_column
# from app.db.base import Base
# from app.infra.repositories.models.role import Role
# from app.infra.repositories.models.role_permission import role_permission
#
# class Permission(Base):
#     __tablename__ = "permissions"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
#     name: Mapped[str] = mapped_column(unique=True, index=True)
#     description: Mapped[str]
#     created_at: Mapped[datetime] = mapped_column(default=datetime.now)
#     updated_at: Mapped[datetime] = mapped_column(default=datetime.now)
#
#     roles = relationship(
#         Role, secondary=role_permission, back_populates="permissions"
#     )

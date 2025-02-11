# from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint
# from app.db.base import Base
#
# user_role = Table(
#     "user_role",
#     Base.metadata,
#     Column("user_id", ForeignKey("users.id"), primary_key=True),
#     Column("role_id", ForeignKey("roles.id"), primary_key=True),
#     ForeignKeyConstraint(["user_id"], ["users.id"], name="user_role_user_id_fk"),
#     ForeignKeyConstraint(["role_id"], ["roles.id"], name="user_role_role_id_fk"),
# )

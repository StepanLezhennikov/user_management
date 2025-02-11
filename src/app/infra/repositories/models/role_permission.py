# from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint
# from app.db.base import Base
#
# role_permission = Table(
#     "role_permission",
#     Base.metadata,
#     Column("role_id", ForeignKey("roles.id"), primary_key=True),
#     Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
#     ForeignKeyConstraint(["role_id"], ["roles.id"], name="role_permission_role_id_fk"),
#     ForeignKeyConstraint(
#         ["permission_id"], ["permissions.id"], name="role_permission_permission_id_fk"
#     ),
# )

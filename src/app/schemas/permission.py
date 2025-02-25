from pydantic import BaseModel, ConfigDict


class PermissionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str


class PermissionCreate(PermissionBase):
    pass


class Permission(PermissionBase):
    id: int

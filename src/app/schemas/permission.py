from pydantic import BaseModel, ConfigDict


class PermissionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class Permission(PermissionBase):
    id: int


class PermissionFilter(BaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None

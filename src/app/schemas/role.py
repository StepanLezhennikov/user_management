from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str
    first_name: str
    last_name: str
    is_blocked: bool = False


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int

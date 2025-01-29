from pydantic import EmailStr, BaseModel, ConfigDict


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    is_blocked: bool = False

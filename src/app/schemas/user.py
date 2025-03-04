from pydantic import EmailStr, BaseModel, ConfigDict

from app.schemas.role import Role


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str
    roles: list[str]


class DeletedUser(UserBase):
    id: int
    is_blocked: bool
    hashed_password: str


class User(UserBase):
    id: int
    is_blocked: bool = False
    hashed_password: str
    roles: list[Role]


class UserForToken(BaseModel):
    id: int
    permissions: list[str]


class UserAuthenticated(UserForToken):
    pass


class UserSignIn(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    pass


class UserFilter(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_blocked: bool | None = None

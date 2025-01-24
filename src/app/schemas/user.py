from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str
    first_name: str
    last_name: str
    is_blocked: bool = False


class UserPrivate(User):
    hashed_password: str

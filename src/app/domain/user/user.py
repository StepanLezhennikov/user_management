from dataclasses import dataclass

from pydantic import EmailStr

from app.domain.base_entity import BaseDTO


@dataclass
class User(BaseDTO):
    login: str
    name: str
    surname: str
    email: EmailStr
    hashed_password: str
    is_blocked: bool

from dataclasses import dataclass

from src.app.domain.value_objects.email import Email
from src.app.domain.entities.base import BaseMixin


@dataclass
class User(BaseMixin):
    login: str
    name: str
    surname: str
    email: Email
    hashed_password: str
    is_blocked: bool
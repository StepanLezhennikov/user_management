import re
from dataclasses import dataclass

from src.app.domain.exceptions.email import InvalidEmail


@dataclass
class Email:
    email: str

    def __post_init__(self):
        if not self.validate_email():
            raise InvalidEmail(f"Invalid email: {self.email}")

    def validate_email(self) -> bool:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, self.email) is not None
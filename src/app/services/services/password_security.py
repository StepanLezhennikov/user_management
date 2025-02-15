import bcrypt

from app.api.exceptions.password_security_service import IncorrectPassword
from app.api.interfaces.services.password_security import APasswordSecurityService


class PasswordSecurityService(APasswordSecurityService):

    def verify_password(self, password: str, stored_password: str) -> None:
        if not bcrypt.checkpw(password.encode(), stored_password.encode()):
            raise IncorrectPassword()

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

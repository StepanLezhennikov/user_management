import bcrypt
from fastapi import HTTPException

from app.api.interfaces.services.password_security import APasswordSecurityService


class PasswordSecurityService(APasswordSecurityService):

    def verify_password(self, password: str, stored_password: str) -> None:
        if not bcrypt.checkpw(password.encode(), stored_password.encode()):
            raise HTTPException(status_code=404, detail="Incorrect password")

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

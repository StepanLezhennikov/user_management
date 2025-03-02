import bcrypt

from app.schemas.user import UserSignIn
from app.api.exceptions.user_service import UserNotFoundError
from app.services.interfaces.uow.uow import AUnitOfWork
from app.api.exceptions.password_security_service import IncorrectPasswordError
from app.api.interfaces.services.password_security import APasswordSecurityService


class PasswordSecurityService(APasswordSecurityService):

    def __init__(self, uow: AUnitOfWork):
        self._uow = uow

    async def verify_password(self, user_data: UserSignIn) -> None:
        async with self._uow as uow:
            user = await uow.users.get(email=user_data.email)
            if not user:
                raise UserNotFoundError()
        if not bcrypt.checkpw(
            user_data.password.encode(), user.hashed_password.encode()
        ):
            raise IncorrectPasswordError()

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
